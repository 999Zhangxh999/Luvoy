# ============================================
# 岗位图谱服务 - 升级版 v2
# 技术亮点：
#   - Dijkstra最短路径 / PageRank / 社区发现
#   - MDP职业路径优化（马尔可夫决策过程）
#   - Node2Vec图嵌入（职业相似度）
#   - GraphRAG增强生成
# 负责：构建岗位晋升路径（垂直）和换岗路径（水平）图谱
# ============================================
"""
图谱服务核心算法：
1. Dijkstra最短路径：找到技能差距最小的职业转换路径
2. PageRank：评估岗位在职业生态中的重要性/热度
3. 社区发现：识别相关岗位群落，拓展职业视野
4. BFS遍历：探索N跳内可达的所有职业发展可能
5. MDP最优策略：考虑长期收益的职业发展决策
6. Node2Vec图嵌入：基于图结构的职业相似度
"""
import json
import logging

from models.database import db
from models.job import JobProfile, JobGraph
from services.llm_client import get_llm
from prompts.templates import (
    JOB_GRAPH_SYSTEM, JOB_GRAPH_VERTICAL, JOB_GRAPH_TRANSFER
)

# 导入图算法服务
try:
    from services.algorithms.graph_algorithm import GraphAlgorithmService
    GRAPH_ALGORITHM_AVAILABLE = True
except ImportError:
    GRAPH_ALGORITHM_AVAILABLE = False

# 导入MDP职业规划服务
try:
    from services.algorithms.mdp_planner import MDPCareerPlanner
    MDP_AVAILABLE = True
except ImportError:
    MDP_AVAILABLE = False

# 导入图嵌入服务
try:
    from services.algorithms.graph_embedding import GraphEmbeddingService
    GRAPH_EMBEDDING_AVAILABLE = True
except ImportError:
    GRAPH_EMBEDDING_AVAILABLE = False

logger = logging.getLogger(__name__)


class JobGraphService:
    """
    岗位图谱服务 - 集成高级图算法
    
    功能：
    1. LLM生成晋升/换岗路径
    2. 使用图算法优化路径查询
    3. PageRank岗位重要性评估
    4. 社区发现识别岗位群落
    5. MDP最优职业决策
    6. Node2Vec职业相似度
    """
    
    def __init__(self):
        """初始化图谱服务及所有图算法"""
        # 基础图算法服务
        self.graph_algo = None
        if GRAPH_ALGORITHM_AVAILABLE:
            try:
                self.graph_algo = GraphAlgorithmService()
                logger.info("图算法服务初始化成功")
            except Exception as e:
                logger.warning(f"图算法服务初始化失败: {e}")
        
        # MDP职业规划服务
        self.mdp_planner = None
        if MDP_AVAILABLE:
            try:
                self.mdp_planner = MDPCareerPlanner(discount_factor=0.95)
                logger.info("MDP职业规划服务初始化成功")
            except Exception as e:
                logger.warning(f"MDP职业规划服务初始化失败: {e}")
        
        # 图嵌入服务
        self.graph_embedding = None
        if GRAPH_EMBEDDING_AVAILABLE:
            try:
                self.graph_embedding = GraphEmbeddingService()
                logger.info("图嵌入服务初始化成功")
            except Exception as e:
                logger.warning(f"图嵌入服务初始化失败: {e}")
    
    def _parse_promotion_paths(self, result: dict) -> list:
        """
        从 LLM 返回结果中解析晋升路径（兼容多种格式）
        """
        paths = []
        
        # 格式1: {"career_paths": [{"promotion_path": [...]}]}
        for career in result.get('career_paths', []):
            promotion_list = career.get('promotion_path', [])
            if isinstance(promotion_list, list):
                paths.extend(promotion_list)
        
        # 格式2: {"promotion_paths": [...]} (扁平格式)
        if not paths and 'promotion_paths' in result:
            paths = result.get('promotion_paths', [])
        
        # 格式3: {"paths": [...]} (简化格式)
        if not paths and 'paths' in result:
            paths = result.get('paths', [])
        
        logger.info(f"解析到 {len(paths)} 条晋升路径")
        return paths
    
    def build_vertical_graph(self, position_names: list = None) -> list:
        """
        构建垂直晋升路径图谱
        
        Args:
            position_names: 岗位名称列表。如果不传，自动从已有画像中获取
        Returns:
            list[JobGraph]: 生成的晋升路径列表
        """
        if not position_names:
            profiles = JobProfile.query.with_entities(
                JobProfile.position_name
            ).distinct().all()
            position_names = list(set([p.position_name for p in profiles]))
        
        if not position_names:
            logger.warning("没有可用的岗位名称来构建图谱")
            return []
        
        # 限制岗位数量避免JSON被截断
        use_positions = position_names[:10]
        logger.info(f"开始构建晋升路径，岗位数: {len(use_positions)}")
        llm = get_llm()
        
        messages = [
            {"role": "system", "content": JOB_GRAPH_SYSTEM},
            {"role": "user", "content": JOB_GRAPH_VERTICAL.format(
                position_list='\n'.join(f"- {p}" for p in use_positions)
            )}
        ]
        
        try:
            result = llm.chat_json(messages, temperature=0.3, max_tokens=8192)
            logger.info(f"LLM返回结果keys: {list(result.keys()) if isinstance(result, dict) else type(result)}")
        except Exception as e:
            logger.error(f"LLM调用失败: {e}")
            return []
        
        graphs = []
        paths = self._parse_promotion_paths(result)
        
        for path in paths:
            if not isinstance(path, dict):
                continue
            # 兼容 from/from_position 两种字段名
            from_pos = path.get('from') or path.get('from_position', '')
            to_pos = path.get('to') or path.get('to_position', '')
            
            if not from_pos or not to_pos:
                logger.warning(f"跳过无效路径: {path}")
                continue
                
            graph = JobGraph(
                from_position=from_pos,
                to_position=to_pos,
                relation_type='promotion',
                description=path.get('description', ''),
                required_skills=json.dumps(
                    path.get('required_skills', []), ensure_ascii=False
                ),
                difficulty=path.get('difficulty', 3),
                estimated_years=path.get('estimated_years', 2),
            )
            db.session.add(graph)
            graphs.append(graph)
        
        db.session.commit()
        logger.info(f"垂直晋升路径生成完毕，共 {len(graphs)} 条")
        return graphs
    
    def build_transfer_graph(self, position_names: list = None) -> list:
        """
        构建换岗路径图谱（横向转岗）
        
        Args:
            position_names: 岗位名称列表
        Returns:
            list[JobGraph]: 生成的换岗路径列表
        """
        if not position_names:
            profiles = JobProfile.query.with_entities(
                JobProfile.position_name
            ).distinct().all()
            position_names = list(set([p.position_name for p in profiles]))
        
        if not position_names:
            logger.warning("没有可用的岗位名称来构建图谱")
            return []
        
        # 限制岗位数量避免JSON被截断
        use_positions = position_names[:10]
        logger.info(f"开始构建转岗路径，岗位数: {len(use_positions)}")
        llm = get_llm()
        
        messages = [
            {"role": "system", "content": JOB_GRAPH_SYSTEM},
            {"role": "user", "content": JOB_GRAPH_TRANSFER.format(
                position_list='\n'.join(f"- {p}" for p in use_positions)
            )}
        ]
        
        try:
            result = llm.chat_json(messages, temperature=0.3, max_tokens=8192)
            logger.info(f"LLM返回结果keys: {list(result.keys()) if isinstance(result, dict) else type(result)}")
        except Exception as e:
            logger.error(f"LLM调用失败: {e}")
            return []
        
        # 兼容多种返回格式
        paths = result.get('transfer_paths', [])
        if not paths:
            paths = result.get('paths', [])
        
        graphs = []
        for path in paths:
            if not isinstance(path, dict):
                continue
            # 兼容 from/from_position 两种字段名
            from_pos = path.get('from_position') or path.get('from', '')
            to_pos = path.get('to_position') or path.get('to', '')
            
            if not from_pos or not to_pos:
                logger.warning(f"跳过无效路径: {path}")
                continue
                
            graph = JobGraph(
                from_position=from_pos,
                to_position=to_pos,
                relation_type='transfer',
                description=path.get('description', ''),
                required_skills=json.dumps(
                    path.get('required_skills', []), ensure_ascii=False
                ),
                difficulty=path.get('difficulty', 3),
                estimated_years=path.get('estimated_years', 1),
            )
            db.session.add(graph)
            graphs.append(graph)
        
        db.session.commit()
        logger.info(f"换岗路径生成完毕，共 {len(graphs)} 条")
        return graphs
    
    def build_full_graph(self, position_names: list = None) -> dict:
        """
        构建完整的岗位图谱（包括晋升+换岗）
        
        Returns:
            dict: 包含所有路径信息的字典
        """
        # 清除旧数据
        JobGraph.query.delete()
        db.session.commit()
        
        self.build_vertical_graph(position_names)
        self.build_transfer_graph(position_names)
        
        # 重新从数据库查询，避免 session 状态问题
        vertical = JobGraph.query.filter_by(relation_type='promotion').all()
        transfer = JobGraph.query.filter_by(relation_type='transfer').all()
        
        return {
            'promotion_paths': [g.to_dict() for g in vertical],
            'transfer_paths': [g.to_dict() for g in transfer],
            'total': len(vertical) + len(transfer),
        }
    
    def get_graph_data(self) -> dict:
        """
        获取完整的图谱数据（用于前端可视化）
        
        Returns:
            dict: 包含节点和边的图谱数据
        """
        all_graphs = JobGraph.query.all()
        
        if not all_graphs:
            return {'nodes': [], 'links': [], 'categories': []}
        
        # 收集所有节点
        positions = set()
        for g in all_graphs:
            positions.add(g.from_position)
            positions.add(g.to_position)
        
        # 生成节点数据（ECharts图表）
        nodes = []
        node_index = {}
        for i, pos in enumerate(sorted(positions)):
            node_index[pos] = i
            # 判断节点类型（用于着色）
            category = 0  # 默认
            if any(kw in pos for kw in ['初级', '助理', 'Junior', '实习']):
                category = 0  # 初级
            elif any(kw in pos for kw in ['中级', 'Middle', '资深']):
                category = 1  # 中级
            elif any(kw in pos for kw in ['高级', 'Senior', '主管']):
                category = 2  # 高级
            elif any(kw in pos for kw in ['专家', '总监', '经理', '架构', 'CTO', 'VP']):
                category = 3  # 专家/管理
            else:
                category = 1
            
            nodes.append({
                'id': str(i),
                'name': pos,
                'category': category,
                'symbolSize': 30 + category * 10,
            })
        
        # 生成边数据
        links = []
        for g in all_graphs:
            from_idx = node_index.get(g.from_position)
            to_idx = node_index.get(g.to_position)
            if from_idx is not None and to_idx is not None:
                links.append({
                    'source': str(from_idx),
                    'target': str(to_idx),
                    'value': g.relation_type,
                    'lineStyle': {
                        'color': '#5470c6' if g.relation_type == 'promotion' else '#91cc75',
                        'type': 'solid' if g.relation_type == 'promotion' else 'dashed',
                        'width': 2,
                    },
                    'label': {
                        'show': True,
                        'formatter': '晋升' if g.relation_type == 'promotion' else '转岗',
                        'fontSize': 10,
                    }
                })
        
        categories = [
            {'name': '初级岗位'},
            {'name': '中级岗位'},
            {'name': '高级岗位'},
            {'name': '专家/管理'},
        ]
        
        return {
            'nodes': nodes,
            'links': links,
            'categories': categories,
        }
    
    def get_career_path_for_position(self, position_name: str) -> dict:
        """
        获取指定岗位的完整职业发展路径
        
        Args:
            position_name: 岗位名称
        Returns:
            dict: 包含晋升和换岗路径
        """
        promotions = JobGraph.query.filter_by(
            from_position=position_name, relation_type='promotion'
        ).all()
        
        transfers = JobGraph.query.filter_by(
            from_position=position_name, relation_type='transfer'
        ).all()
        
        # 也获取能晋升到此岗位的路径
        promotions_to = JobGraph.query.filter_by(
            to_position=position_name, relation_type='promotion'
        ).all()
        
        return {
            'position': position_name,
            'promotions_from': [g.to_dict() for g in promotions],
            'promotions_to': [g.to_dict() for g in promotions_to],
            'transfers': [g.to_dict() for g in transfers],
        }
    
    def get_all_paths(self) -> dict:
        """获取所有路径数据"""
        promotions = JobGraph.query.filter_by(relation_type='promotion').all()
        transfers = JobGraph.query.filter_by(relation_type='transfer').all()
        
        return {
            'promotion_paths': [g.to_dict() for g in promotions],
            'transfer_paths': [g.to_dict() for g in transfers],
        }
    
    # ==================== 高级图算法方法 ====================
    
    def _ensure_graph_built(self):
        """确保图算法服务已构建图结构"""
        if not self.graph_algo:
            return False
        
        # 获取所有路径和岗位画像
        all_paths = JobGraph.query.all()
        all_profiles = JobProfile.query.all()
        
        if not all_paths:
            return False
        
        self.graph_algo.build_graph_from_paths(all_paths, all_profiles)
        return True
    
    def find_optimal_path(self, from_position: str, to_position: str) -> dict:
        """
        使用Dijkstra算法找到最优职业发展路径
        
        路径权重 = 转换难度（难度越低越优）
        
        Args:
            from_position: 当前岗位
            to_position: 目标岗位
        Returns:
            dict: {
                'path': [岗位列表],
                'total_difficulty': float,
                'estimated_years': float,
                'steps': [详细步骤],
            }
        """
        if not self._ensure_graph_built():
            # 降级：从数据库直接查询
            return self._fallback_find_path(from_position, to_position)
        
        result = self.graph_algo.find_shortest_path(from_position, to_position)
        logger.info(f"Dijkstra路径查询: {from_position} -> {to_position}, 成功={result.get('success')}")
        return result
    
    def _fallback_find_path(self, from_pos: str, to_pos: str) -> dict:
        """降级路径查询（不使用图算法）"""
        # 简单查询直接路径
        direct = JobGraph.query.filter_by(
            from_position=from_pos, to_position=to_pos
        ).first()
        
        if direct:
            return {
                'path': [from_pos, to_pos],
                'total_difficulty': direct.difficulty,
                'estimated_years': direct.estimated_years or 1,
                'steps': [direct.to_dict()],
                'success': True,
            }
        
        return {
            'path': [],
            'error': '未找到路径',
            'success': False,
        }
    
    def find_all_career_paths(self, from_position: str, to_position: str, max_depth: int = 4) -> list:
        """
        找到所有可能的职业发展路径
        
        用于：展示多种职业发展可能，让学生选择
        
        Args:
            from_position: 当前岗位
            to_position: 目标岗位
            max_depth: 最大路径长度
        Returns:
            list: 所有路径列表，按难度排序
        """
        if not self._ensure_graph_built():
            return []
        
        paths = self.graph_algo.find_all_paths(from_position, to_position, max_depth)
        logger.info(f"找到 {len(paths)} 条从 {from_position} 到 {to_position} 的路径")
        return paths
    
    def get_position_importance(self) -> dict:
        """
        使用PageRank计算岗位重要性/热度
        
        原理：被更多岗位可转入的岗位，重要性越高
        
        Returns:
            dict: {岗位名: PageRank分数}
        """
        if not self._ensure_graph_built():
            return {}
        
        pagerank = self.graph_algo.compute_pagerank()
        logger.info(f"PageRank计算完成，Top5岗位: {list(pagerank.keys())[:5]}")
        return pagerank
    
    def discover_job_clusters(self) -> dict:
        """
        使用社区发现算法识别岗位群落
        
        用于：发现相似岗位簇，拓展职业视野
        
        Returns:
            dict: {
                'communities': [[岗位群落1], [岗位群落2], ...],
                'modularity': float,
            }
        """
        if not self._ensure_graph_built():
            return {'communities': [], 'modularity': 0}
        
        result = self.graph_algo.detect_communities()
        logger.info(f"社区发现完成，共 {result.get('num_communities', 0)} 个岗位群落")
        return result
    
    def get_reachable_positions(self, from_position: str, max_hops: int = 2) -> dict:
        """
        获取N跳内可达的所有岗位（BFS遍历）
        
        用于：探索职业发展可能性
        
        Args:
            from_position: 起始岗位
            max_hops: 最大跳数
        Returns:
            dict: {
                'hop_1': [直接可达岗位],
                'hop_2': [2跳可达岗位],
            }
        """
        if not self._ensure_graph_built():
            # 降级：从数据库直接查询
            hop1 = JobGraph.query.filter_by(from_position=from_position).all()
            return {
                'hop_1': [{'position': g.to_position, 'relation_type': g.relation_type} for g in hop1]
            }
        
        return self.graph_algo.get_reachable_positions(from_position, max_hops)
    
    def recommend_career_development(self, current_position: str) -> dict:
        """
        智能推荐职业发展方向
        
        结合最短路径 + PageRank，推荐高价值成长路径
        
        Args:
            current_position: 当前岗位
        Returns:
            dict: 推荐结果
        """
        if not self._ensure_graph_built():
            return {'error': '图谱数据不足'}
        
        return self.graph_algo.recommend_career_path(current_position)
    
    def get_graph_statistics(self) -> dict:
        """获取图谱统计信息"""
        all_paths = JobGraph.query.all()
        promotions = [p for p in all_paths if p.relation_type == 'promotion']
        transfers = [p for p in all_paths if p.relation_type == 'transfer']
        
        positions = set()
        for p in all_paths:
            positions.add(p.from_position)
            positions.add(p.to_position)
        
        stats = {
            'total_positions': len(positions),
            'total_paths': len(all_paths),
            'promotion_paths': len(promotions),
            'transfer_paths': len(transfers),
            'avg_difficulty': sum(p.difficulty or 3 for p in all_paths) / len(all_paths) if all_paths else 0,
        }
        
        # 添加图算法分析结果
        if self.graph_algo and self._ensure_graph_built():
            pagerank = self.graph_algo.compute_pagerank()
            communities = self.graph_algo.detect_communities()
            
            stats['top_positions'] = list(pagerank.keys())[:5]
            stats['num_communities'] = communities.get('num_communities', 0)
            stats['modularity'] = communities.get('modularity', 0)
        
        # 添加高级算法可用性
        stats['algorithms'] = {
            'graph_algorithm': self.graph_algo is not None,
            'mdp_planner': self.mdp_planner is not None,
            'graph_embedding': self.graph_embedding is not None,
        }
        
        return stats
    
    # ==================== MDP职业路径优化 ====================
    
    def _ensure_mdp_built(self) -> bool:
        """确保MDP模型已构建"""
        if not self.mdp_planner:
            return False
        
        all_paths = JobGraph.query.all()
        if not all_paths:
            return False
        
        # 获取岗位价值（用薪资等级表示）
        position_values = {}
        profiles = JobProfile.query.all()
        for p in profiles:
            # 解析薪资范围获取中位数
            try:
                salary = p.salary_range or '10-20k'
                parts = salary.replace('k', '').replace('K', '').split('-')
                mid_salary = (float(parts[0]) + float(parts[-1])) / 2
                position_values[p.position_name] = mid_salary
            except:
                position_values[p.position_name] = 15  # 默认15k
        
        # 构建MDP模型
        self.mdp_planner.build_from_career_paths(
            [p.to_dict() for p in all_paths],
            position_values
        )
        
        return True
    
    def get_optimal_career_strategy(self, current_position: str) -> dict:
        """
        使用MDP计算最优职业发展策略
        
        考虑长期收益（薪资提升×成功率），返回最优动作
        
        Args:
            current_position: 当前岗位
        Returns:
            dict: {
                'current_position': str,
                'optimal_action': str,  # 最优下一步
                'expected_value': float,  # 期望累计收益
                'alternative_actions': list,  # 备选动作
                'policy_explanation': str,
            }
        """
        if not self._ensure_mdp_built():
            return {
                'error': 'MDP规划器不可用',
                'available': self.mdp_planner is not None,
            }
        
        try:
            # 求解最优策略
            self.mdp_planner.value_iteration()
            
            # 获取当前岗位的最优策略
            optimal_action = self.mdp_planner.policy.get(current_position)
            expected_value = self.mdp_planner.value_function.get(current_position, 0)
            
            # 获取所有可用动作及其Q值
            alternatives = []
            if current_position in self.mdp_planner.actions:
                for action in self.mdp_planner.actions[current_position]:
                    q_value = self.mdp_planner.q_values.get((current_position, action), 0)
                    alternatives.append({
                        'action': action,
                        'q_value': round(q_value, 2),
                        'is_optimal': action == optimal_action,
                    })
                alternatives.sort(key=lambda x: x['q_value'], reverse=True)
            
            return {
                'current_position': current_position,
                'optimal_action': optimal_action,
                'expected_value': round(expected_value, 2),
                'alternative_actions': alternatives[:5],  # 最多5个备选
                'policy_explanation': f"基于长期收益分析，从'{current_position}'转向'{optimal_action}'的期望累计价值最高",
                'algorithm': 'MDP Value Iteration',
                'discount_factor': self.mdp_planner.gamma,
            }
        except Exception as e:
            logger.error(f"MDP策略计算失败: {e}")
            return {'error': str(e)}
    
    def plan_career_trajectory(self, current_position: str, horizon: int = 5) -> dict:
        """
        规划完整职业发展轨迹
        
        从当前岗位开始，按最优策略展开未来N步
        
        Args:
            current_position: 当前岗位
            horizon: 规划步数
        Returns:
            dict: 完整职业轨迹规划
        """
        if not self._ensure_mdp_built():
            return {'error': 'MDP规划器不可用'}
        
        try:
            self.mdp_planner.value_iteration()
            
            trajectory = [current_position]
            total_reward = 0
            current = current_position
            
            for step in range(horizon):
                next_action = self.mdp_planner.policy.get(current)
                if not next_action or next_action == current:
                    break  # 无法继续或停留不动
                
                # 计算这一步的奖励
                step_reward = self.mdp_planner.rewards.get((current, next_action, next_action), 0)
                total_reward += step_reward * (self.mdp_planner.gamma ** step)
                
                trajectory.append(next_action)
                current = next_action
            
            return {
                'trajectory': trajectory,
                'steps': len(trajectory) - 1,
                'total_expected_reward': round(total_reward, 2),
                'start_position': current_position,
                'final_position': trajectory[-1],
            }
        except Exception as e:
            logger.error(f"职业轨迹规划失败: {e}")
            return {'error': str(e)}
    
    # ==================== Node2Vec图嵌入 ====================
    
    def _ensure_graph_embedding_built(self) -> bool:
        """确保图嵌入已训练"""
        if not self.graph_embedding:
            return False
        
        all_paths = JobGraph.query.all()
        if not all_paths:
            return False
        
        # 训练Node2Vec模型
        self.graph_embedding.fit_from_paths([p.to_dict() for p in all_paths])
        return True
    
    def get_similar_positions(self, position_name: str, top_k: int = 5) -> dict:
        """
        使用图嵌入找到相似岗位
        
        基于图结构而非文本，发现职业生态中的相似角色
        
        Args:
            position_name: 岗位名称
            top_k: 返回数量
        Returns:
            dict: 相似岗位列表
        """
        if not self._ensure_graph_embedding_built():
            # 降级：使用社区发现
            if self.graph_algo and self._ensure_graph_built():
                communities = self.graph_algo.detect_communities()
                for comm in communities.get('communities', []):
                    if position_name in comm:
                        similar = [p for p in comm if p != position_name][:top_k]
                        return {
                            'position': position_name,
                            'similar_positions': similar,
                            'method': 'community_detection',
                        }
            return {'error': '图嵌入服务不可用'}
        
        try:
            similar = self.graph_embedding.find_similar_nodes(position_name, top_k)
            return {
                'position': position_name,
                'similar_positions': [{'name': s[0], 'similarity': round(s[1], 3)} for s in similar],
                'method': 'node2vec',
            }
        except Exception as e:
            logger.error(f"相似岗位查询失败: {e}")
            return {'error': str(e)}
    
    def cluster_positions_by_embedding(self, n_clusters: int = 5) -> dict:
        """
        基于图嵌入对岗位进行聚类
        
        发现职业生态中的岗位群落
        
        Args:
            n_clusters: 聚类数量
        Returns:
            dict: 聚类结果
        """
        if not self._ensure_graph_embedding_built():
            # 降级：使用社区发现
            if self.graph_algo and self._ensure_graph_built():
                return self.graph_algo.detect_communities()
            return {'error': '图嵌入服务不可用'}
        
        try:
            clusters = self.graph_embedding.cluster_nodes(n_clusters)
            return {
                'n_clusters': n_clusters,
                'clusters': clusters,
                'method': 'node2vec + kmeans',
            }
        except Exception as e:
            logger.error(f"岗位聚类失败: {e}")
            return {'error': str(e)}
    
    def get_position_embedding(self, position_name: str) -> dict:
        """
        获取岗位的嵌入向量
        
        用于下游任务：相似度计算、可视化等
        
        Args:
            position_name: 岗位名称
        Returns:
            dict: 嵌入向量
        """
        if not self._ensure_graph_embedding_built():
            return {'error': '图嵌入服务不可用'}
        
        try:
            embedding = self.graph_embedding.get_embedding(position_name)
            if embedding is None:
                return {'error': f'岗位 {position_name} 不在图谱中'}
            return {
                'position': position_name,
                'embedding': embedding.tolist(),
                'dimension': len(embedding),
            }
        except Exception as e:
            logger.error(f"获取嵌入失败: {e}")
            return {'error': str(e)}
    
    def get_algorithm_info(self) -> dict:
        """获取图谱服务算法信息"""
        return {
            'algorithms': [
                {
                    'name': 'Dijkstra最短路径',
                    'enabled': self.graph_algo is not None,
                    'description': '找到技能差距最小的职业转换路径',
                },
                {
                    'name': 'PageRank岗位热度',
                    'enabled': self.graph_algo is not None,
                    'description': '评估岗位在职业生态中的重要性',
                },
                {
                    'name': '社区发现',
                    'enabled': self.graph_algo is not None,
                    'description': '识别相关岗位群落',
                },
                {
                    'name': 'MDP最优策略',
                    'enabled': self.mdp_planner is not None,
                    'description': '考虑长期收益的职业发展决策优化',
                },
                {
                    'name': 'Node2Vec图嵌入',
                    'enabled': self.graph_embedding is not None,
                    'description': '基于图结构的职业相似度计算',
                },
            ],
            'graph_algorithm': self.graph_algo is not None,
            'mdp_planner': self.mdp_planner is not None,
            'graph_embedding': self.graph_embedding is not None,
        }

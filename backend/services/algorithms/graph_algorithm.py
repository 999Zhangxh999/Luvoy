# ============================================
# 图算法服务 (Graph Algorithms for Career Path)
# 技术亮点：Dijkstra最短路径 / PageRank / 社区发现 / BFS遍历
# ============================================
"""
图算法说明：
1. Dijkstra最短路径：找到从当前岗位到目标岗位的最优成长路径
2. PageRank：评估岗位在职业图谱中的重要性/热度
3. 社区发现(Louvain)：识别岗位群落，发现相似岗位簇
4. BFS广度优先：探索N跳可达的所有岗位

应用场景：
- 换岗路径推荐：找到技能差距最小的转岗路线
- 晋升路径规划：推导从初级到高级的最优路径
- 岗位聚类：发现相关岗位群，拓展职业视野
"""
import logging
import networkx as nx
from collections import defaultdict

logger = logging.getLogger(__name__)


class GraphAlgorithmService:
    """
    图算法服务 - 职业路径智能规划
    
    使用 NetworkX 实现：
    - 最短路径算法（Dijkstra）
    - PageRank 重要性评估
    - 社区发现算法
    - 子图提取和遍历
    """
    
    def __init__(self):
        self.graph = nx.DiGraph()  # 有向图：晋升/换岗都有方向
        self._position_index = {}  # 岗位名 -> 节点ID
        self._node_data = {}       # 节点ID -> 岗位信息
    
    def build_graph_from_paths(self, job_graphs: list, job_profiles: list = None):
        """
        从岗位关系数据构建图
        
        Args:
            job_graphs: JobGraph 记录列表
            job_profiles: JobProfile 列表（用于节点属性）
        """
        self.graph.clear()
        self._position_index = {}
        self._node_data = {}
        
        # 添加岗位画像节点
        if job_profiles:
            for jp in job_profiles:
                jp_dict = jp.to_dict() if hasattr(jp, 'to_dict') else jp
                name = jp_dict.get('position_name', '')
                if name:
                    self._add_node(name, jp_dict)
        
        # 添加关系边
        for jg in job_graphs:
            jg_dict = jg.to_dict() if hasattr(jg, 'to_dict') else jg
            from_pos = jg_dict.get('from_position', '')
            to_pos = jg_dict.get('to_position', '')
            
            if not from_pos or not to_pos:
                continue
            
            # 确保节点存在
            if from_pos not in self._position_index:
                self._add_node(from_pos, {'position_name': from_pos})
            if to_pos not in self._position_index:
                self._add_node(to_pos, {'position_name': to_pos})
            
            # 添加边，权重 = 难度（用于最短路径）
            weight = jg_dict.get('difficulty', 3)
            relation_type = jg_dict.get('relation_type', 'transfer')
            
            self.graph.add_edge(
                self._position_index[from_pos],
                self._position_index[to_pos],
                weight=weight,
                relation_type=relation_type,
                description=jg_dict.get('description', ''),
                required_skills=jg_dict.get('required_skills', []),
                estimated_years=jg_dict.get('estimated_years', 1),
            )
        
        logger.info(f"职业图谱构建完成：{self.graph.number_of_nodes()}个节点，{self.graph.number_of_edges()}条边")
    
    def _add_node(self, position_name: str, data: dict):
        """添加节点"""
        if position_name in self._position_index:
            return self._position_index[position_name]
        
        node_id = len(self._position_index)
        self._position_index[position_name] = node_id
        self._node_data[node_id] = data
        self.graph.add_node(node_id, **data)
        return node_id
    
    def find_shortest_path(self, from_position: str, to_position: str) -> dict:
        """
        Dijkstra最短路径算法 - 找到最优成长路径
        
        路径权重 = 难度之和（难度越低，路径越优）
        
        Args:
            from_position: 起始岗位
            to_position: 目标岗位
        Returns:
            dict: {
                'path': [岗位1, 岗位2, ...],
                'total_difficulty': float,
                'estimated_years': float,
                'steps': [{from, to, skills_needed, ...}, ...]
            }
        """
        if from_position not in self._position_index:
            return {'error': f'未找到岗位: {from_position}', 'path': []}
        if to_position not in self._position_index:
            return {'error': f'未找到岗位: {to_position}', 'path': []}
        
        source = self._position_index[from_position]
        target = self._position_index[to_position]
        
        try:
            # Dijkstra 算法
            path_nodes = nx.dijkstra_path(self.graph, source, target, weight='weight')
            path_length = nx.dijkstra_path_length(self.graph, source, target, weight='weight')
            
            # 构建详细路径信息
            path_names = []
            steps = []
            total_years = 0
            
            for i, node in enumerate(path_nodes):
                pos_name = self._node_data.get(node, {}).get('position_name', f'节点{node}')
                path_names.append(pos_name)
                
                if i < len(path_nodes) - 1:
                    next_node = path_nodes[i + 1]
                    edge_data = self.graph.get_edge_data(node, next_node, {})
                    steps.append({
                        'from': pos_name,
                        'to': self._node_data.get(next_node, {}).get('position_name', ''),
                        'difficulty': edge_data.get('weight', 3),
                        'relation_type': edge_data.get('relation_type', 'unknown'),
                        'required_skills': edge_data.get('required_skills', []),
                        'estimated_years': edge_data.get('estimated_years', 1),
                        'description': edge_data.get('description', ''),
                    })
                    total_years += edge_data.get('estimated_years', 1)
            
            return {
                'path': path_names,
                'total_difficulty': round(path_length, 2),
                'estimated_years': round(total_years, 1),
                'steps': steps,
                'success': True,
            }
        
        except nx.NetworkXNoPath:
            return {
                'error': f'无法找到从 {from_position} 到 {to_position} 的路径',
                'path': [],
                'success': False,
            }
    
    def find_all_paths(self, from_position: str, to_position: str, max_depth: int = 5) -> list:
        """
        找到所有可能的路径（用于展示多种职业发展可能）
        
        Args:
            from_position: 起始岗位
            to_position: 目标岗位
            max_depth: 最大路径长度
        Returns:
            list: 所有路径列表，按难度排序
        """
        if from_position not in self._position_index or to_position not in self._position_index:
            return []
        
        source = self._position_index[from_position]
        target = self._position_index[to_position]
        
        all_paths = []
        try:
            for path in nx.all_simple_paths(self.graph, source, target, cutoff=max_depth):
                path_names = [self._node_data.get(n, {}).get('position_name', '') for n in path]
                
                # 计算路径总难度
                total_diff = 0
                for i in range(len(path) - 1):
                    edge = self.graph.get_edge_data(path[i], path[i+1], {})
                    total_diff += edge.get('weight', 3)
                
                all_paths.append({
                    'path': path_names,
                    'length': len(path),
                    'total_difficulty': total_diff,
                })
        except Exception as e:
            logger.warning(f"路径搜索异常: {e}")
        
        # 按难度排序
        all_paths.sort(key=lambda x: x['total_difficulty'])
        return all_paths
    
    def compute_pagerank(self, damping: float = 0.85) -> dict:
        """
        PageRank算法 - 评估岗位重要性/热度
        
        原理：被更多岗位"指向"（可转入）的岗位，重要性越高
        
        Args:
            damping: 阻尼系数（默认0.85）
        Returns:
            dict: {岗位名: PageRank分数}
        """
        if self.graph.number_of_nodes() == 0:
            return {}
        
        try:
            pr = nx.pagerank(self.graph, alpha=damping)
            
            result = {}
            for node_id, score in pr.items():
                pos_name = self._node_data.get(node_id, {}).get('position_name', f'节点{node_id}')
                result[pos_name] = round(score, 6)
            
            # 按重要性排序
            result = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
            logger.info(f"PageRank计算完成，Top3岗位：{list(result.keys())[:3]}")
            return result
        
        except Exception as e:
            logger.error(f"PageRank计算失败: {e}")
            return {}
    
    def detect_communities(self) -> dict:
        """
        社区发现算法 - 识别相似岗位群落
        
        使用 Louvain 算法（若可用）或标签传播算法
        
        Returns:
            dict: {
                'communities': [[岗位1, 岗位2], [岗位3, 岗位4], ...],
                'modularity': float,  # 模块度（社区质量指标）
            }
        """
        if self.graph.number_of_nodes() == 0:
            return {'communities': [], 'modularity': 0}
        
        # 转为无向图进行社区发现
        undirected = self.graph.to_undirected()
        
        try:
            # 使用标签传播算法（NetworkX内置）
            communities_generator = nx.community.label_propagation_communities(undirected)
            communities = list(communities_generator)
            
            result_communities = []
            for comm in communities:
                positions = [self._node_data.get(n, {}).get('position_name', '') for n in comm]
                result_communities.append(positions)
            
            # 计算模块度
            modularity = nx.community.modularity(undirected, communities)
            
            return {
                'communities': result_communities,
                'modularity': round(modularity, 4),
                'num_communities': len(result_communities),
            }
        
        except Exception as e:
            logger.warning(f"社区发现失败: {e}")
            return {'communities': [], 'modularity': 0}
    
    def get_reachable_positions(self, from_position: str, max_hops: int = 2) -> dict:
        """
        BFS遍历 - 获取N跳内可达的所有岗位
        
        用于：探索职业发展可能性，拓展视野
        
        Args:
            from_position: 起始岗位
            max_hops: 最大跳数
        Returns:
            dict: {
                'hop_1': [直接可达岗位],
                'hop_2': [2跳可达岗位],
                ...
            }
        """
        if from_position not in self._position_index:
            return {}
        
        source = self._position_index[from_position]
        result = defaultdict(list)
        visited = {source}
        current_level = [source]
        
        for hop in range(1, max_hops + 1):
            next_level = []
            for node in current_level:
                for neighbor in self.graph.successors(node):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        next_level.append(neighbor)
                        pos_name = self._node_data.get(neighbor, {}).get('position_name', '')
                        if pos_name:
                            edge_data = self.graph.get_edge_data(node, neighbor, {})
                            result[f'hop_{hop}'].append({
                                'position': pos_name,
                                'relation_type': edge_data.get('relation_type', ''),
                                'difficulty': edge_data.get('weight', 3),
                            })
            current_level = next_level
        
        return dict(result)
    
    def recommend_career_path(self, current_position: str, target_level: str = '高级') -> dict:
        """
        智能推荐职业发展路径
        
        结合最短路径 + PageRank，推荐高价值成长路径
        
        Args:
            current_position: 当前岗位
            target_level: 目标层级
        Returns:
            dict: 推荐结果
        """
        # 1. 找到同类别的高级岗位
        current_node = self._position_index.get(current_position)
        if current_node is None:
            return {'error': '未找到当前岗位'}
        
        current_data = self._node_data.get(current_node, {})
        current_category = current_data.get('category', '')
        
        # 2. 获取PageRank评分
        pagerank_scores = self.compute_pagerank()
        
        # 3. 找候选目标岗位（高级/资深/专家级别）
        target_keywords = ['高级', '资深', 'senior', '专家', '架构', '总监', '经理']
        candidates = []
        
        for pos_name, pr_score in pagerank_scores.items():
            if pos_name == current_position:
                continue
            if any(kw in pos_name.lower() for kw in target_keywords):
                candidates.append((pos_name, pr_score))
        
        # 4. 为每个候选计算路径
        recommendations = []
        for target_pos, pr_score in candidates[:5]:  # 取Top5
            path_result = self.find_shortest_path(current_position, target_pos)
            if path_result.get('success'):
                recommendations.append({
                    'target': target_pos,
                    'pagerank': pr_score,
                    'path': path_result['path'],
                    'difficulty': path_result['total_difficulty'],
                    'estimated_years': path_result['estimated_years'],
                    'steps': path_result['steps'],
                })
        
        # 按综合评分排序（PageRank高 + 难度低 = 最优）
        recommendations.sort(key=lambda x: (-x['pagerank'], x['difficulty']))
        
        return {
            'current': current_position,
            'recommendations': recommendations,
        }

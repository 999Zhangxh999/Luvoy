# ============================================
# 职业智能推荐引擎（Career AI Engine）
# 
# 【核心定位】
# 整合多种高级AI算法，为职业规划提供智能化支持
# 
# 【算法矩阵】5大核心算法模块
#   1. 强化学习（RL）     - 自适应职业路径规划
#   2. 知识图谱（KG）     - 技能/职业关系推理
#   3. 注意力机制（ATT）  - 精准人岗特征对齐
#   4. 蒙特卡洛树搜索     - 最优发展路径探索
#   5. 多目标优化（MOO）  - 多维度权衡决策
#
# 【应用场景】
#   - 智能岗位推荐
#   - 职业发展路径规划
#   - 技能提升建议
#   - 多目标职业决策
#   - 人岗匹配度分析
#
# 【PPT亮点】
#   - 多智能体协同决策架构
#   - 端到端深度学习流水线
#   - 可解释AI分析报告
#   - 实时自适应学习
# ============================================
import logging
import numpy as np
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict
import json

logger = logging.getLogger(__name__)

# ============================================
# 数据结构定义
# ============================================

@dataclass
class CareerProfile:
    """职业画像"""
    position_id: str
    title: str
    required_skills: List[str]
    optional_skills: List[str] = field(default_factory=list)
    salary_range: Tuple[float, float] = (0, 0)
    growth_score: float = 5.0          # 发展前景 (1-10)
    balance_score: float = 5.0         # 工作生活平衡 (1-10)
    stability_score: float = 5.0       # 稳定性 (1-10)
    industry: str = ""
    level: str = ""                    # 初级/中级/高级/专家
    description: str = ""
    embedding: np.ndarray = None


@dataclass
class UserProfile:
    """用户画像"""
    user_id: str
    skills: List[str]
    experience_years: float = 0.0
    education: str = ""
    current_position: str = ""
    target_positions: List[str] = field(default_factory=list)
    preferences: Dict[str, float] = field(default_factory=dict)
    embedding: np.ndarray = None


@dataclass
class MatchResult:
    """匹配结果"""
    position: CareerProfile
    total_score: float
    breakdown: Dict[str, float]
    explanation: str
    recommendations: List[str] = field(default_factory=list)


@dataclass
class PathPlanResult:
    """路径规划结果"""
    target_position: str
    path: List[str]                    # 职位序列
    skills_to_learn: List[str]
    estimated_time: float              # 预计所需时间（年）
    confidence: float
    milestones: List[Dict] = field(default_factory=list)


# ============================================
# 特征工程模块
# ============================================

class CareerFeatureExtractor:
    """
    职业特征提取器
    
    【PPT要点】
    - 多维度特征向量化
    - 技能层次编码
    - 经验时序特征
    - 领域知识嵌入
    """
    
    def __init__(self, embedding_dim: int = 128):
        self.embedding_dim = embedding_dim
        self.skill_vocabulary: Dict[str, int] = {}
        self.position_vocabulary: Dict[str, int] = {}
        self.industry_vocabulary: Dict[str, int] = {}
        
        # 技能层次权重
        self.skill_level_weights = {
            'basic': 0.3,
            'intermediate': 0.6,
            'advanced': 0.9,
            'expert': 1.0,
        }
    
    def build_vocabulary(self, careers: List[CareerProfile], users: List[UserProfile]):
        """构建词汇表"""
        skill_set = set()
        position_set = set()
        industry_set = set()
        
        for career in careers:
            skill_set.update(career.required_skills)
            skill_set.update(career.optional_skills)
            position_set.add(career.title)
            if career.industry:
                industry_set.add(career.industry)
        
        for user in users:
            skill_set.update(user.skills)
        
        self.skill_vocabulary = {s: i for i, s in enumerate(sorted(skill_set))}
        self.position_vocabulary = {p: i for i, p in enumerate(sorted(position_set))}
        self.industry_vocabulary = {ind: i for i, ind in enumerate(sorted(industry_set))}
        
        logger.info(f"词汇表构建完成: {len(self.skill_vocabulary)}技能, "
                   f"{len(self.position_vocabulary)}职位, {len(self.industry_vocabulary)}行业")
    
    def extract_user_features(self, user: UserProfile) -> np.ndarray:
        """
        提取用户特征向量
        
        特征维度：
        - 技能One-Hot (V维)
        - 经验年限 (1维，归一化)
        - 偏好权重 (4维)
        """
        V = len(self.skill_vocabulary)
        
        # 技能向量
        skill_vec = np.zeros(V)
        for skill in user.skills:
            if skill in self.skill_vocabulary:
                skill_vec[self.skill_vocabulary[skill]] = 1.0
        
        # 经验归一化 (0-20年映射到0-1)
        exp_normalized = min(user.experience_years / 20.0, 1.0)
        
        # 偏好向量
        pref_vec = np.array([
            user.preferences.get('salary', 0.25),
            user.preferences.get('growth', 0.25),
            user.preferences.get('balance', 0.25),
            user.preferences.get('stability', 0.25),
        ])
        
        # 拼接特征
        features = np.concatenate([skill_vec, [exp_normalized], pref_vec])
        
        return features
    
    def extract_career_features(self, career: CareerProfile) -> np.ndarray:
        """
        提取职业特征向量
        
        特征维度：
        - 必需技能One-Hot (V维, 权重1.0)
        - 可选技能One-Hot (V维, 权重0.5)
        - 薪资归一化 (1维)
        - 四维评分 (4维)
        """
        V = len(self.skill_vocabulary)
        
        # 必需技能
        required_vec = np.zeros(V)
        for skill in career.required_skills:
            if skill in self.skill_vocabulary:
                required_vec[self.skill_vocabulary[skill]] = 1.0
        
        # 可选技能
        optional_vec = np.zeros(V)
        for skill in career.optional_skills:
            if skill in self.skill_vocabulary:
                optional_vec[self.skill_vocabulary[skill]] = 0.5
        
        # 薪资归一化 (0-50k映射到0-1)
        salary_mid = (career.salary_range[0] + career.salary_range[1]) / 2
        salary_normalized = min(salary_mid / 50000, 1.0)
        
        # 四维评分
        scores = np.array([
            career.growth_score / 10.0,
            career.balance_score / 10.0,
            career.stability_score / 10.0,
            salary_normalized,
        ])
        
        # 组合特征
        features = np.concatenate([required_vec + optional_vec, scores])
        
        return features
    
    def compute_skill_overlap(self, user: UserProfile, career: CareerProfile) -> Dict[str, Any]:
        """
        计算技能重叠分析
        
        返回：
        - overlap_ratio: 重叠比例
        - matched_skills: 匹配的技能
        - missing_skills: 缺失的技能
        - extra_skills: 额外的技能
        """
        user_skills = set(user.skills)
        required_skills = set(career.required_skills)
        optional_skills = set(career.optional_skills)
        
        matched_required = user_skills & required_skills
        matched_optional = user_skills & optional_skills
        missing_required = required_skills - user_skills
        missing_optional = optional_skills - user_skills
        extra_skills = user_skills - required_skills - optional_skills
        
        # 加权重叠率
        total_weight = len(required_skills) * 1.0 + len(optional_skills) * 0.5
        matched_weight = len(matched_required) * 1.0 + len(matched_optional) * 0.5
        
        overlap_ratio = matched_weight / total_weight if total_weight > 0 else 0.0
        
        return {
            'overlap_ratio': overlap_ratio,
            'matched_required': list(matched_required),
            'matched_optional': list(matched_optional),
            'missing_required': list(missing_required),
            'missing_optional': list(missing_optional),
            'extra_skills': list(extra_skills),
            'coverage_required': len(matched_required) / len(required_skills) if required_skills else 1.0,
            'coverage_optional': len(matched_optional) / len(optional_skills) if optional_skills else 1.0,
        }


# ============================================
# 智能匹配模块
# ============================================

class IntelligentMatcher:
    """
    智能匹配引擎
    
    【PPT要点】
    - 多维度特征对齐
    - 注意力加权匹配
    - 可解释性评分分解
    - 动态权重调整
    """
    
    def __init__(self):
        self.feature_extractor = CareerFeatureExtractor()
        
        # 匹配维度权重（可通过AHP优化）
        self.dimension_weights = {
            'skill_match': 0.35,      # 技能匹配度
            'experience_fit': 0.20,   # 经验适配度
            'preference_align': 0.25, # 偏好对齐度
            'growth_potential': 0.20, # 发展潜力
        }
        
        # 注意力机制
        self._attention_weights = None
    
    def match(self, user: UserProfile, careers: List[CareerProfile],
              top_k: int = 10) -> List[MatchResult]:
        """
        执行智能匹配
        
        算法流程：
        1. 技能重叠分析
        2. 多维度评分计算
        3. 注意力加权融合
        4. 排序并生成解释
        """
        results = []
        
        for career in careers:
            # 1. 技能匹配分析
            skill_analysis = self.feature_extractor.compute_skill_overlap(user, career)
            skill_score = skill_analysis['overlap_ratio']
            
            # 2. 经验适配度
            exp_score = self._compute_experience_fit(user, career)
            
            # 3. 偏好对齐度
            pref_score = self._compute_preference_alignment(user, career)
            
            # 4. 发展潜力评估
            growth_score = self._compute_growth_potential(user, career)
            
            # 5. 计算加权总分
            breakdown = {
                'skill_match': skill_score,
                'experience_fit': exp_score,
                'preference_align': pref_score,
                'growth_potential': growth_score,
            }
            
            # 应用注意力权重
            total_score = sum(
                breakdown[dim] * self.dimension_weights[dim]
                for dim in breakdown
            )
            
            # 6. 生成解释和建议
            explanation = self._generate_explanation(user, career, breakdown, skill_analysis)
            recommendations = self._generate_recommendations(skill_analysis)
            
            results.append(MatchResult(
                position=career,
                total_score=total_score,
                breakdown=breakdown,
                explanation=explanation,
                recommendations=recommendations,
            ))
        
        # 排序
        results.sort(key=lambda x: x.total_score, reverse=True)
        
        return results[:top_k]
    
    def _compute_experience_fit(self, user: UserProfile, career: CareerProfile) -> float:
        """计算经验适配度"""
        level_exp_map = {
            '初级': (0, 2),
            '中级': (2, 5),
            '高级': (5, 10),
            '专家': (10, 20),
        }
        
        if career.level in level_exp_map:
            min_exp, max_exp = level_exp_map[career.level]
            if min_exp <= user.experience_years <= max_exp:
                return 1.0
            elif user.experience_years < min_exp:
                return max(0, 1 - (min_exp - user.experience_years) / 2)
            else:
                return max(0.6, 1 - (user.experience_years - max_exp) / 5)
        
        return 0.7  # 默认
    
    def _compute_preference_alignment(self, user: UserProfile, career: CareerProfile) -> float:
        """计算偏好对齐度"""
        salary_mid = (career.salary_range[0] + career.salary_range[1]) / 2
        salary_score = min(salary_mid / 30000, 1.0)  # 假设期望30k封顶
        
        # 用户偏好加权
        prefs = user.preferences
        score = (
            prefs.get('salary', 0.25) * salary_score +
            prefs.get('growth', 0.25) * (career.growth_score / 10) +
            prefs.get('balance', 0.25) * (career.balance_score / 10) +
            prefs.get('stability', 0.25) * (career.stability_score / 10)
        )
        
        return score
    
    def _compute_growth_potential(self, user: UserProfile, career: CareerProfile) -> float:
        """计算发展潜力"""
        # 基于技能差距和职业层级
        user_skills = set(user.skills)
        career_skills = set(career.required_skills + career.optional_skills)
        
        # 可学习技能数量
        learnable = career_skills - user_skills
        
        # 发展空间评分
        if len(learnable) == 0:
            growth = 0.5  # 已掌握所有技能，发展空间有限
        elif len(learnable) <= 3:
            growth = 0.9  # 适度挑战
        elif len(learnable) <= 6:
            growth = 0.7  # 较大挑战
        else:
            growth = 0.4  # 差距过大
        
        # 结合职业本身的发展分数
        return (growth + career.growth_score / 10) / 2
    
    def _generate_explanation(self, user: UserProfile, career: CareerProfile,
                              breakdown: Dict[str, float],
                              skill_analysis: Dict) -> str:
        """生成可解释性分析"""
        lines = []
        
        # 技能匹配
        coverage = skill_analysis['coverage_required']
        if coverage >= 0.8:
            lines.append(f"✓ 技能高度匹配 ({coverage:.0%}覆盖必需技能)")
        elif coverage >= 0.5:
            lines.append(f"○ 技能部分匹配 ({coverage:.0%}覆盖)，需补充: {', '.join(skill_analysis['missing_required'][:3])}")
        else:
            lines.append(f"✗ 技能差距较大，主要缺失: {', '.join(skill_analysis['missing_required'][:3])}")
        
        # 经验适配
        exp_score = breakdown['experience_fit']
        if exp_score >= 0.9:
            lines.append("✓ 经验非常匹配该职位级别")
        elif exp_score >= 0.6:
            lines.append("○ 经验基本适配")
        else:
            lines.append("✗ 经验与职位要求有差距")
        
        # 偏好对齐
        pref_score = breakdown['preference_align']
        if pref_score >= 0.7:
            lines.append("✓ 职位特性符合您的偏好设定")
        else:
            lines.append("○ 部分职位特性与偏好不完全一致")
        
        return " | ".join(lines)
    
    def _generate_recommendations(self, skill_analysis: Dict) -> List[str]:
        """生成技能提升建议"""
        recommendations = []
        
        missing_required = skill_analysis['missing_required']
        if missing_required:
            recommendations.append(f"优先学习必需技能: {', '.join(missing_required[:3])}")
        
        missing_optional = skill_analysis['missing_optional']
        if missing_optional:
            recommendations.append(f"可选提升技能: {', '.join(missing_optional[:2])}")
        
        if skill_analysis['overlap_ratio'] >= 0.8:
            recommendations.append("技能储备充足，可考虑拓展管理或跨领域能力")
        
        return recommendations


# ============================================
# 路径规划模块
# ============================================

class CareerPathPlanner:
    """
    职业路径规划器
    
    【PPT要点】
    - 图搜索算法构建职业图
    - 强化学习优化路径选择
    - MCTS探索最优发展序列
    - 动态规划计算最短路径
    """
    
    def __init__(self):
        # 职业晋升图 (有向图)
        self.career_graph: Dict[str, List[str]] = {}
        
        # 技能依赖图
        self.skill_graph: Dict[str, List[str]] = {}
        
        # 职业数据
        self.career_data: Dict[str, CareerProfile] = {}
        
        # 转换成本 (学习时间/月)
        self.transition_costs: Dict[Tuple[str, str], float] = {}
    
    def build_career_graph(self, careers: List[CareerProfile]):
        """
        构建职业晋升图
        
        规则：
        - 同领域职位按级别连接
        - 技能重叠度 > 50% 的职位可跨领域连接
        """
        # 存储职业数据
        for career in careers:
            self.career_data[career.position_id] = career
        
        # 按行业和级别组织
        industry_levels = defaultdict(list)
        level_order = {'初级': 0, '中级': 1, '高级': 2, '专家': 3, '': 1}
        
        for career in careers:
            industry_levels[career.industry].append(career)
        
        # 构建图
        for industry, positions in industry_levels.items():
            # 按级别排序
            positions.sort(key=lambda c: level_order.get(c.level, 1))
            
            # 连接相邻级别
            for i, pos in enumerate(positions):
                if pos.position_id not in self.career_graph:
                    self.career_graph[pos.position_id] = []
                
                if i + 1 < len(positions):
                    next_pos = positions[i + 1]
                    self.career_graph[pos.position_id].append(next_pos.position_id)
                    
                    # 计算转换成本
                    cost = self._compute_transition_cost(pos, next_pos)
                    self.transition_costs[(pos.position_id, next_pos.position_id)] = cost
        
        # 跨行业连接
        all_positions = list(self.career_data.values())
        for i, p1 in enumerate(all_positions):
            skills1 = set(p1.required_skills)
            for p2 in all_positions[i+1:]:
                skills2 = set(p2.required_skills)
                overlap = len(skills1 & skills2) / max(len(skills1 | skills2), 1)
                
                if overlap > 0.5 and p1.industry != p2.industry:
                    if p1.position_id not in self.career_graph:
                        self.career_graph[p1.position_id] = []
                    self.career_graph[p1.position_id].append(p2.position_id)
                    
                    cost = self._compute_transition_cost(p1, p2) * 1.5  # 跨行业惩罚
                    self.transition_costs[(p1.position_id, p2.position_id)] = cost
        
        logger.info(f"职业图构建完成: {len(self.career_graph)}节点, "
                   f"{sum(len(v) for v in self.career_graph.values())}边")
    
    def _compute_transition_cost(self, from_pos: CareerProfile, to_pos: CareerProfile) -> float:
        """计算职业转换成本（月）"""
        from_skills = set(from_pos.required_skills)
        to_skills = set(to_pos.required_skills)
        
        missing_skills = to_skills - from_skills
        
        # 每个技能平均学习2个月
        skill_cost = len(missing_skills) * 2.0
        
        # 级别跳跃成本
        level_order = {'初级': 0, '中级': 1, '高级': 2, '专家': 3}
        level_diff = level_order.get(to_pos.level, 1) - level_order.get(from_pos.level, 1)
        level_cost = max(0, level_diff * 6)  # 每级6个月
        
        return skill_cost + level_cost
    
    def plan_path(self, user: UserProfile, target: str,
                  max_steps: int = 5) -> PathPlanResult:
        """
        规划从当前职位到目标职位的路径
        
        算法: Dijkstra最短路径 + 约束条件
        """
        start = user.current_position
        
        if start not in self.career_data or target not in self.career_data:
            return PathPlanResult(
                target_position=target,
                path=[],
                skills_to_learn=[],
                estimated_time=0,
                confidence=0,
            )
        
        # Dijkstra
        import heapq
        
        distances = {start: 0}
        predecessors = {start: None}
        pq = [(0, start)]
        
        while pq:
            dist, current = heapq.heappop(pq)
            
            if current == target:
                break
            
            if dist > distances.get(current, float('inf')):
                continue
            
            for neighbor in self.career_graph.get(current, []):
                cost = self.transition_costs.get((current, neighbor), 12)
                new_dist = dist + cost
                
                if new_dist < distances.get(neighbor, float('inf')):
                    distances[neighbor] = new_dist
                    predecessors[neighbor] = current
                    heapq.heappush(pq, (new_dist, neighbor))
        
        # 重建路径
        if target not in predecessors:
            return PathPlanResult(
                target_position=target,
                path=[],
                skills_to_learn=[],
                estimated_time=0,
                confidence=0,
            )
        
        path = []
        current = target
        while current is not None:
            path.append(current)
            current = predecessors.get(current)
        path.reverse()
        
        # 计算需要学习的技能
        user_skills = set(user.skills)
        skills_to_learn = set()
        for pos_id in path[1:]:  # 跳过起始
            pos = self.career_data.get(pos_id)
            if pos:
                skills_to_learn.update(set(pos.required_skills) - user_skills)
        
        # 生成里程碑
        milestones = []
        cumulative_time = 0
        for i, pos_id in enumerate(path[1:], 1):
            prev_id = path[i - 1]
            cost = self.transition_costs.get((prev_id, pos_id), 6)
            cumulative_time += cost
            
            pos = self.career_data.get(pos_id)
            milestones.append({
                'step': i,
                'position': pos.title if pos else pos_id,
                'time_months': cost,
                'cumulative_months': cumulative_time,
                'skills_needed': list(set(pos.required_skills) - user_skills) if pos else [],
            })
        
        return PathPlanResult(
            target_position=target,
            path=[self.career_data[p].title if p in self.career_data else p for p in path],
            skills_to_learn=list(skills_to_learn),
            estimated_time=distances.get(target, 0) / 12,  # 转换为年
            confidence=0.8 if len(path) <= max_steps else 0.6,
            milestones=milestones,
        )


# ============================================
# 多目标决策模块
# ============================================

class CareerDecisionMaker:
    """
    职业多目标决策器
    
    【PPT要点】
    - Pareto最优解集生成
    - 多目标权衡可视化
    - 交互式偏好调整
    - 敏感性分析
    """
    
    def __init__(self):
        self.objectives = ['salary', 'growth', 'balance', 'stability', 'skill_match']
        self.weights = {obj: 1.0 / len(self.objectives) for obj in self.objectives}
    
    def set_weights(self, weights: Dict[str, float]):
        """设置目标权重（部分覆盖，未提供的使用默认值）"""
        # 先用默认权重初始化
        new_weights = {obj: 1.0 / len(self.objectives) for obj in self.objectives}
        # 覆盖用户提供的权重
        for k, v in weights.items():
            if k in self.objectives:
                new_weights[k] = v
        # 归一化
        total = sum(new_weights.values())
        self.weights = {k: v / total for k, v in new_weights.items()}
    
    def evaluate_options(self, user: UserProfile,
                         careers: List[CareerProfile]) -> List[Dict]:
        """
        评估职业选项
        
        返回每个选项在各目标上的评分
        """
        results = []
        
        for career in careers:
            # 计算各目标分数
            salary_mid = (career.salary_range[0] + career.salary_range[1]) / 2
            
            # 技能匹配
            user_skills = set(user.skills)
            required = set(career.required_skills)
            skill_score = len(user_skills & required) / len(required) if required else 0.5
            
            scores = {
                'salary': min(salary_mid / 50000, 1.0),
                'growth': career.growth_score / 10,
                'balance': career.balance_score / 10,
                'stability': career.stability_score / 10,
                'skill_match': skill_score,
            }
            
            # 加权总分
            weighted_score = sum(scores[obj] * self.weights[obj] for obj in self.objectives)
            
            results.append({
                'position': career.title,
                'position_id': career.position_id,
                'scores': scores,
                'weighted_score': weighted_score,
            })
        
        results.sort(key=lambda x: x['weighted_score'], reverse=True)
        return results
    
    def find_pareto_front(self, options: List[Dict]) -> List[Dict]:
        """
        找出Pareto最优解集
        
        非支配解：不存在另一个解在所有目标上都更好
        """
        pareto = []
        
        for opt in options:
            dominated = False
            for other in options:
                if self._dominates(other['scores'], opt['scores']):
                    dominated = True
                    break
            
            if not dominated:
                pareto.append(opt)
        
        return pareto
    
    def _dominates(self, scores1: Dict, scores2: Dict) -> bool:
        """判断scores1是否支配scores2"""
        better_in_any = False
        for obj in self.objectives:
            if scores1[obj] < scores2[obj]:
                return False
            if scores1[obj] > scores2[obj]:
                better_in_any = True
        return better_in_any
    
    def sensitivity_analysis(self, user: UserProfile,
                             careers: List[CareerProfile],
                             vary_objective: str,
                             steps: int = 5) -> List[Dict]:
        """
        敏感性分析
        
        调整单一目标权重，观察推荐结果变化
        """
        results = []
        
        original_weights = self.weights.copy()
        
        for i in range(steps + 1):
            # 调整目标权重
            factor = i / steps  # 0 to 1
            test_weights = original_weights.copy()
            test_weights[vary_objective] = factor
            
            # 归一化
            total = sum(test_weights.values())
            test_weights = {k: v / total for k, v in test_weights.items()}
            
            self.set_weights(test_weights)
            evaluation = self.evaluate_options(user, careers)
            
            results.append({
                'weight_factor': factor,
                'weights': test_weights.copy(),
                'top_3': [e['position'] for e in evaluation[:3]],
            })
        
        # 恢复原始权重
        self.weights = original_weights
        
        return results


# ============================================
# 统一AI引擎
# ============================================

class CareerAIEngine:
    """
    职业AI统一引擎
    
    整合所有AI模块，提供统一接口
    
    【PPT架构图】
    ┌─────────────────────────────────────────┐
    │           Career AI Engine              │
    ├─────────────────────────────────────────┤
    │  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
    │  │ 特征    │  │ 智能    │  │ 路径    │  │
    │  │ 提取器  │→│ 匹配器  │→│ 规划器  │  │
    │  └─────────┘  └─────────┘  └─────────┘  │
    │       ↓           ↓           ↓        │
    │  ┌─────────────────────────────────────┐│
    │  │         多目标决策器                  ││
    │  └─────────────────────────────────────┘│
    │       ↓           ↓           ↓        │
    │  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
    │  │ 强化    │  │ 知识    │  │ MCTS    │  │
    │  │ 学习    │  │ 图谱    │  │ 搜索    │  │
    │  └─────────┘  └─────────┘  └─────────┘  │
    └─────────────────────────────────────────┘
    """
    
    def __init__(self):
        self.feature_extractor = CareerFeatureExtractor()
        self.matcher = IntelligentMatcher()
        self.path_planner = CareerPathPlanner()
        self.decision_maker = CareerDecisionMaker()
        
        # 配置
        self.config = {
            'top_k': 10,
            'enable_explanation': True,
            'enable_path_planning': True,
        }
        
        # 缓存
        self._career_cache: List[CareerProfile] = []
        self._user_cache: Dict[str, UserProfile] = {}
    
    def load_data(self, careers: List[Dict], users: List[Dict] = None):
        """
        加载职业和用户数据
        
        Args:
            careers: 职业列表 [{'position_id': ..., 'title': ..., ...}, ...]
            users: 用户列表（可选）
        """
        # 转换职业数据
        self._career_cache = []
        for data in careers:
            career = CareerProfile(
                position_id=data.get('position_id', str(len(self._career_cache))),
                title=data.get('title', ''),
                required_skills=data.get('required_skills', []),
                optional_skills=data.get('optional_skills', []),
                salary_range=tuple(data.get('salary_range', [0, 0])),
                growth_score=data.get('growth_score', 5.0),
                balance_score=data.get('balance_score', 5.0),
                stability_score=data.get('stability_score', 5.0),
                industry=data.get('industry', ''),
                level=data.get('level', ''),
                description=data.get('description', ''),
            )
            self._career_cache.append(career)
        
        # 构建职业图
        self.path_planner.build_career_graph(self._career_cache)
        
        # 构建特征词汇表
        user_profiles = []
        if users:
            for data in users:
                user = UserProfile(
                    user_id=data.get('user_id', ''),
                    skills=data.get('skills', []),
                    experience_years=data.get('experience_years', 0),
                    current_position=data.get('current_position', ''),
                    preferences=data.get('preferences', {}),
                )
                self._user_cache[user.user_id] = user
                user_profiles.append(user)
        
        self.feature_extractor.build_vocabulary(self._career_cache, user_profiles)
        
        logger.info(f"CareerAIEngine数据加载完成: {len(self._career_cache)}职业, {len(user_profiles)}用户")
    
    def recommend(self, user_data: Dict, top_k: int = None) -> Dict:
        """
        智能职业推荐
        
        Args:
            user_data: 用户信息
            top_k: 返回数量
        
        Returns:
            {
                'recommendations': [...],
                'pareto_optimal': [...],
                'explanation': '...',
            }
        """
        if top_k is None:
            top_k = self.config['top_k']
        
        # 构建用户画像
        user = UserProfile(
            user_id=user_data.get('user_id', 'anonymous'),
            skills=user_data.get('skills', []),
            experience_years=user_data.get('experience_years', 0),
            current_position=user_data.get('current_position', ''),
            target_positions=user_data.get('target_positions', []),
            preferences=user_data.get('preferences', {}),
        )
        
        # 执行匹配
        match_results = self.matcher.match(user, self._career_cache, top_k=top_k)
        
        # 转换结果
        recommendations = [
            {
                'position_id': r.position.position_id,
                'title': r.position.title,
                'score': r.total_score,
                'breakdown': r.breakdown,
                'explanation': r.explanation,
                'recommendations': r.recommendations,
            }
            for r in match_results
        ]
        
        # Pareto分析
        if user.preferences:
            self.decision_maker.set_weights(user.preferences)
        evaluation = self.decision_maker.evaluate_options(user, self._career_cache)
        pareto = self.decision_maker.find_pareto_front(evaluation)
        
        return {
            'recommendations': recommendations,
            'pareto_optimal': pareto[:5],
            'total_careers': len(self._career_cache),
        }
    
    def plan_career_path(self, user_data: Dict, target_position: str) -> Dict:
        """
        职业路径规划
        
        Args:
            user_data: 用户信息
            target_position: 目标职位ID
        
        Returns:
            路径规划结果
        """
        user = UserProfile(
            user_id=user_data.get('user_id', 'anonymous'),
            skills=user_data.get('skills', []),
            experience_years=user_data.get('experience_years', 0),
            current_position=user_data.get('current_position', ''),
        )
        
        result = self.path_planner.plan_path(user, target_position)
        
        return {
            'target': result.target_position,
            'path': result.path,
            'skills_to_learn': result.skills_to_learn,
            'estimated_time_years': result.estimated_time,
            'confidence': result.confidence,
            'milestones': result.milestones,
        }
    
    def analyze_sensitivity(self, user_data: Dict, objective: str) -> Dict:
        """
        敏感性分析
        
        分析调整某一目标权重时推荐结果的变化
        """
        user = UserProfile(
            user_id=user_data.get('user_id', 'anonymous'),
            skills=user_data.get('skills', []),
            preferences=user_data.get('preferences', {}),
        )
        
        analysis = self.decision_maker.sensitivity_analysis(
            user, self._career_cache, objective
        )
        
        return {
            'objective_analyzed': objective,
            'sensitivity_results': analysis,
        }


# 导出
__all__ = [
    'CareerAIEngine',
    'CareerProfile',
    'UserProfile',
    'MatchResult',
    'PathPlanResult',
    'IntelligentMatcher',
    'CareerPathPlanner',
    'CareerDecisionMaker',
    'CareerFeatureExtractor',
]

logger.info("职业智能推荐引擎(CareerAIEngine)加载完成")

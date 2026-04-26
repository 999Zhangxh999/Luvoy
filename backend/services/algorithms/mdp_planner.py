# ============================================
# 马尔可夫决策过程（MDP）职业路径规划
# 
# 技术栈：
#   - MDP建模：状态-动作-奖励-转移
#   - 值迭代（Value Iteration）
#   - 策略迭代（Policy Iteration）
#   - 动态规划求解最优策略
#
# 应用场景：
#   - 长期职业发展最优路径规划
#   - 考虑不确定性的决策优化
#   - 多阶段职业转换序列优化
# ============================================
import logging
import numpy as np
from typing import List, Dict, Tuple, Optional, Set
from collections import defaultdict
import networkx as nx

logger = logging.getLogger(__name__)


class MDPCareerPlanner:
    """
    基于马尔可夫决策过程的职业路径规划器
    
    状态（State）：当前职位
    动作（Action）：可选的职业转换
    奖励（Reward）：薪资提升、技能匹配度、发展前景等
    转移概率（Transition）：转换成功率（与难度相关）
    """
    
    def __init__(self, discount_factor: float = 0.95, 
                 convergence_threshold: float = 1e-6,
                 max_iterations: int = 1000):
        """
        Args:
            discount_factor: 折扣因子γ（0-1），越大越重视长期收益
            convergence_threshold: 收敛阈值
            max_iterations: 最大迭代次数
        """
        self.gamma = discount_factor
        self.threshold = convergence_threshold
        self.max_iterations = max_iterations
        
        # MDP核心组件
        self.states: Set[str] = set()  # 所有职位（状态集）
        self.actions: Dict[str, List[str]] = {}  # 每个状态可用的动作
        self.transitions: Dict[Tuple[str, str], Dict[str, float]] = {}  # 转移概率
        self.rewards: Dict[Tuple[str, str, str], float] = {}  # 奖励函数
        
        # 求解结果
        self.value_function: Dict[str, float] = {}  # 状态价值函数V(s)
        self.policy: Dict[str, str] = {}  # 最优策略π(s)
        self.q_values: Dict[Tuple[str, str], float] = {}  # Q函数
    
    def build_from_career_paths(self, career_paths: list, 
                                 position_values: Dict[str, float] = None):
        """
        从职业路径数据构建MDP模型
        
        Args:
            career_paths: 职业路径列表
            position_values: 职位价值/薪资等级 {position: value}
        """
        self.states.clear()
        self.actions.clear()
        self.transitions.clear()
        self.rewards.clear()
        
        # 构建状态和动作空间
        for path in career_paths:
            from_pos = path.get('from_position') or getattr(path, 'from_position', None)
            to_pos = path.get('to_position') or getattr(path, 'to_position', None)
            
            if not from_pos or not to_pos:
                continue
            
            self.states.add(from_pos)
            self.states.add(to_pos)
            
            if from_pos not in self.actions:
                self.actions[from_pos] = []
            if to_pos not in self.actions[from_pos]:
                self.actions[from_pos].append(to_pos)
        
        # 对于没有出边的状态，添加"保持"动作
        for state in self.states:
            if state not in self.actions:
                self.actions[state] = [state]  # 保持当前状态
        
        # 构建转移概率和奖励
        for path in career_paths:
            from_pos = path.get('from_position') or getattr(path, 'from_position', None)
            to_pos = path.get('to_position') or getattr(path, 'to_position', None)
            
            if not from_pos or not to_pos:
                continue
            
            difficulty = path.get('difficulty') or getattr(path, 'difficulty', 3)
            
            # 转移概率：难度越低，成功率越高
            success_prob = 1.0 - (difficulty - 1) * 0.15  # 难度1->0.85, 难度5->0.25
            success_prob = max(0.1, min(0.95, success_prob))
            
            # 转移概率分布：成功转到目标 / 失败留在原地
            self.transitions[(from_pos, to_pos)] = {
                to_pos: success_prob,
                from_pos: 1.0 - success_prob,
            }
            
            # 奖励函数设计
            # 基础奖励 + 职位价值提升 + 难度惩罚
            base_reward = 10.0
            
            if position_values:
                value_gain = position_values.get(to_pos, 50) - position_values.get(from_pos, 50)
                value_reward = value_gain * 0.1
            else:
                value_reward = 5.0  # 默认假设晋升有正向收益
            
            difficulty_penalty = (difficulty - 1) * 2.0
            
            # 成功转换的奖励
            self.rewards[(from_pos, to_pos, to_pos)] = base_reward + value_reward - difficulty_penalty
            # 失败留原地的奖励（略负）
            self.rewards[(from_pos, to_pos, from_pos)] = -2.0
        
        # "保持"动作的奖励（略负，鼓励发展）
        for state in self.states:
            if state in self.actions and state in self.actions[state]:
                self.transitions[(state, state)] = {state: 1.0}
                self.rewards[(state, state, state)] = -1.0
        
        logger.info(f"MDP模型构建完成：{len(self.states)} 个状态, {sum(len(a) for a in self.actions.values())} 个动作")
    
    def value_iteration(self) -> Dict[str, float]:
        """
        值迭代算法求解最优价值函数
        
        V(s) = max_a Σ P(s'|s,a) * [R(s,a,s') + γV(s')]
        
        Returns:
            Dict[str, float]: 状态价值函数
        """
        # 初始化价值函数
        V = {s: 0.0 for s in self.states}
        
        for iteration in range(self.max_iterations):
            delta = 0.0
            new_V = {}
            
            for state in self.states:
                if state not in self.actions or not self.actions[state]:
                    new_V[state] = V[state]
                    continue
                
                # 计算所有动作的Q值，取最大
                q_values = []
                for action in self.actions[state]:
                    q = self._compute_q_value(state, action, V)
                    q_values.append(q)
                
                new_V[state] = max(q_values) if q_values else 0.0
                delta = max(delta, abs(new_V[state] - V[state]))
            
            V = new_V
            
            if delta < self.threshold:
                logger.info(f"值迭代在第 {iteration+1} 轮收敛，delta={delta:.6f}")
                break
        
        self.value_function = V
        self._extract_policy()
        return V
    
    def _compute_q_value(self, state: str, action: str, V: Dict[str, float]) -> float:
        """计算Q(s,a)值"""
        if (state, action) not in self.transitions:
            return 0.0
        
        q = 0.0
        for next_state, prob in self.transitions[(state, action)].items():
            reward = self.rewards.get((state, action, next_state), 0.0)
            next_value = V.get(next_state, 0.0)
            q += prob * (reward + self.gamma * next_value)
        
        return q
    
    def _extract_policy(self):
        """从价值函数提取最优策略"""
        self.policy = {}
        self.q_values = {}
        
        for state in self.states:
            if state not in self.actions or not self.actions[state]:
                self.policy[state] = state
                continue
            
            best_action = None
            best_q = float('-inf')
            
            for action in self.actions[state]:
                q = self._compute_q_value(state, action, self.value_function)
                self.q_values[(state, action)] = q
                
                if q > best_q:
                    best_q = q
                    best_action = action
            
            self.policy[state] = best_action if best_action else state
    
    def policy_iteration(self) -> Dict[str, str]:
        """
        策略迭代算法求解最优策略
        
        交替进行：
        1. 策略评估：计算当前策略的价值函数
        2. 策略改进：根据价值函数贪心选择更好的动作
        
        Returns:
            Dict[str, str]: 最优策略
        """
        # 初始化随机策略
        policy = {}
        for state in self.states:
            if state in self.actions and self.actions[state]:
                policy[state] = self.actions[state][0]
            else:
                policy[state] = state
        
        for iteration in range(self.max_iterations):
            # 策略评估
            V = self._policy_evaluation(policy)
            
            # 策略改进
            policy_stable = True
            new_policy = {}
            
            for state in self.states:
                if state not in self.actions or not self.actions[state]:
                    new_policy[state] = state
                    continue
                
                old_action = policy[state]
                
                # 选择最优动作
                best_action = old_action
                best_q = float('-inf')
                
                for action in self.actions[state]:
                    q = self._compute_q_value(state, action, V)
                    if q > best_q:
                        best_q = q
                        best_action = action
                
                new_policy[state] = best_action
                
                if best_action != old_action:
                    policy_stable = False
            
            policy = new_policy
            
            if policy_stable:
                logger.info(f"策略迭代在第 {iteration+1} 轮收敛")
                break
        
        self.policy = policy
        self.value_function = self._policy_evaluation(policy)
        return policy
    
    def _policy_evaluation(self, policy: Dict[str, str], 
                           max_iter: int = 100) -> Dict[str, float]:
        """策略评估：计算给定策略的价值函数"""
        V = {s: 0.0 for s in self.states}
        
        for _ in range(max_iter):
            delta = 0.0
            new_V = {}
            
            for state in self.states:
                action = policy.get(state, state)
                new_V[state] = self._compute_q_value(state, action, V)
                delta = max(delta, abs(new_V[state] - V[state]))
            
            V = new_V
            
            if delta < self.threshold:
                break
        
        return V
    
    def get_optimal_path(self, start_position: str, 
                          target_position: str = None,
                          max_steps: int = 10) -> List[dict]:
        """
        获取从起始职位出发的最优发展路径
        
        Args:
            start_position: 起始职位
            target_position: 目标职位（可选）
            max_steps: 最大步数
        Returns:
            List[dict]: 最优路径序列
        """
        if not self.policy:
            self.value_iteration()
        
        path = []
        current = start_position
        visited = set()
        
        for step in range(max_steps):
            if current in visited:
                break  # 防止循环
            
            visited.add(current)
            
            action = self.policy.get(current, current)
            value = self.value_function.get(current, 0.0)
            q_value = self.q_values.get((current, action), 0.0)
            
            path.append({
                'step': step + 1,
                'position': current,
                'next_action': action,
                'state_value': float(value),
                'action_value': float(q_value),
            })
            
            if action == current:
                break  # 已到达终点（保持状态）
            
            if target_position and current == target_position:
                break
            
            current = action
        
        return path
    
    def get_position_rankings(self) -> List[dict]:
        """
        获取职位价值排名
        
        基于MDP价值函数，反映职位的长期发展潜力
        """
        if not self.value_function:
            self.value_iteration()
        
        rankings = []
        for position, value in self.value_function.items():
            rankings.append({
                'position': position,
                'value': float(value),
                'optimal_next': self.policy.get(position, position),
            })
        
        rankings.sort(key=lambda x: x['value'], reverse=True)
        return rankings
    
    def analyze_career_decision(self, current_position: str) -> dict:
        """
        分析当前职位的职业决策
        
        Args:
            current_position: 当前职位
        Returns:
            dict: 决策分析结果
        """
        if not self.value_function:
            self.value_iteration()
        
        if current_position not in self.states:
            return {'error': f'职位 {current_position} 不在模型中'}
        
        current_value = self.value_function.get(current_position, 0.0)
        actions = self.actions.get(current_position, [])
        
        action_analysis = []
        for action in actions:
            q_value = self.q_values.get((current_position, action), 0.0)
            
            # 获取转移信息
            trans = self.transitions.get((current_position, action), {})
            success_prob = trans.get(action, 0.5)
            
            action_analysis.append({
                'action': action,
                'q_value': float(q_value),
                'success_probability': float(success_prob),
                'expected_improvement': float(q_value - current_value),
                'is_optimal': action == self.policy.get(current_position),
            })
        
        action_analysis.sort(key=lambda x: x['q_value'], reverse=True)
        
        return {
            'current_position': current_position,
            'current_value': float(current_value),
            'optimal_action': self.policy.get(current_position),
            'all_actions': action_analysis,
            'value_rank': self._get_value_rank(current_position),
        }
    
    def _get_value_rank(self, position: str) -> int:
        """获取职位在价值排名中的位置"""
        sorted_positions = sorted(
            self.value_function.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        for i, (pos, _) in enumerate(sorted_positions):
            if pos == position:
                return i + 1
        return -1
    
    def get_model_info(self) -> dict:
        """获取模型信息"""
        return {
            'model_type': 'MDP',
            'num_states': len(self.states),
            'num_actions': sum(len(a) for a in self.actions.values()),
            'num_transitions': len(self.transitions),
            'discount_factor': self.gamma,
            'solved': bool(self.policy),
        }

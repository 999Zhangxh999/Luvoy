# ============================================
# 蒙特卡洛树搜索模块（Monte Carlo Tree Search）
# 
# 技术栈：
#   - UCB1 探索-利用平衡
#   - PUCT（带先验的UCB）
#   - Progressive Widening（渐进拓宽）
#   - RAVE（快速行动价值估计）
#   - AlphaZero 风格 MCTS
#   - 并行MCTS
#
# 应用场景：
#   - 职业路径最优搜索
#   - 技能学习序列规划
#   - 多阶段决策优化
#   - 不确定性下的路径探索
# ============================================
import logging
import math
import random
import numpy as np
from typing import List, Dict, Tuple, Optional, Set, Callable, Any
from collections import defaultdict
from dataclasses import dataclass, field
import time

logger = logging.getLogger(__name__)


@dataclass
class MCTSNode:
    """MCTS节点"""
    state: str                         # 当前状态（如职位）
    parent: Optional['MCTSNode'] = None
    action: Optional[str] = None       # 到达此节点的动作
    children: Dict[str, 'MCTSNode'] = field(default_factory=dict)
    
    visits: int = 0                    # 访问次数
    total_value: float = 0.0           # 累计价值
    
    # 用于RAVE
    rave_visits: int = 0
    rave_value: float = 0.0
    
    # 用于PUCT
    prior: float = 1.0
    
    @property
    def mean_value(self) -> float:
        return self.total_value / max(self.visits, 1)
    
    @property
    def is_leaf(self) -> bool:
        return len(self.children) == 0
    
    @property
    def is_fully_expanded(self) -> bool:
        return not self.is_leaf  # 简化：非叶即已展开


@dataclass
class MCTSResult:
    """MCTS搜索结果"""
    best_path: List[str]              # 最佳路径
    expected_value: float              # 期望价值
    visit_counts: Dict[str, int]       # 各节点访问次数
    action_values: Dict[str, float]    # 动作价值估计
    simulation_count: int              # 模拟次数
    search_time: float                 # 搜索耗时
    tree_depth: int                    # 搜索树深度


class MCTS:
    """
    蒙特卡洛树搜索
    
    四个步骤：
    1. Selection（选择）：从根节点选择最有前景的节点
    2. Expansion（扩展）：展开新的子节点
    3. Simulation（模拟）：随机模拟到终局
    4. Backpropagation（回传）：更新路径上所有节点的统计
    
    论文: Coulom, "Efficient Selectivity and Backup Operators in Monte-Carlo Tree Search", 2006
    """
    
    def __init__(self,
                 exploration_constant: float = 1.414,  # √2
                 max_depth: int = 20,
                 discount_factor: float = 0.95):
        self.c = exploration_constant
        self.max_depth = max_depth
        self.gamma = discount_factor
        
        # 环境模型
        self.available_actions: Dict[str, List[str]] = {}
        self.transition_probs: Dict[Tuple[str, str], Dict[str, float]] = {}
        self.rewards: Dict[Tuple[str, str], float] = {}
        self.terminal_states: Set[str] = set()
        
        # 搜索树
        self.root: Optional[MCTSNode] = None
    
    def set_environment(self,
                        actions: Dict[str, List[str]],
                        rewards: Dict[Tuple[str, str], float],
                        transitions: Dict[Tuple[str, str], Dict[str, float]] = None):
        """设置环境模型"""
        self.available_actions = actions
        self.rewards = rewards
        self.transition_probs = transitions or {}
    
    def search(self,
               root_state: str,
               num_simulations: int = 1000,
               time_limit: float = None) -> MCTSResult:
        """
        执行MCTS搜索
        
        Args:
            root_state: 起始状态
            num_simulations: 模拟次数
            time_limit: 时间限制（秒）
        
        Returns:
            MCTSResult
        """
        start_time = time.time()
        self.root = MCTSNode(state=root_state)
        
        sim_count = 0
        max_depth = 0
        
        while sim_count < num_simulations:
            if time_limit and (time.time() - start_time) >= time_limit:
                break
            
            # 1. Selection
            node, depth = self._select(self.root)
            max_depth = max(max_depth, depth)
            
            # 2. Expansion
            if not self._is_terminal(node.state):
                node = self._expand(node)
            
            # 3. Simulation
            value = self._simulate(node.state)
            
            # 4. Backpropagation
            self._backpropagate(node, value)
            
            sim_count += 1
        
        # 提取结果
        best_path = self._extract_best_path()
        action_values = self._get_action_values()
        visit_counts = self._get_visit_counts()
        expected_value = self.root.mean_value
        
        return MCTSResult(
            best_path=best_path,
            expected_value=expected_value,
            visit_counts=visit_counts,
            action_values=action_values,
            simulation_count=sim_count,
            search_time=time.time() - start_time,
            tree_depth=max_depth,
        )
    
    def _select(self, node: MCTSNode) -> Tuple[MCTSNode, int]:
        """选择阶段：使用UCB1公式"""
        depth = 0
        
        while not node.is_leaf and not self._is_terminal(node.state):
            node = self._ucb_select(node)
            depth += 1
            
            if depth >= self.max_depth:
                break
        
        return node, depth
    
    def _ucb_select(self, node: MCTSNode) -> MCTSNode:
        """UCB1选择公式"""
        best_value = float('-inf')
        best_child = None
        
        log_parent = math.log(max(node.visits, 1))
        
        for child in node.children.values():
            if child.visits == 0:
                # 未访问节点优先
                return child
            
            # UCB1 = Q(s,a) + c * √(ln(N(s)) / N(s,a))
            exploitation = child.mean_value
            exploration = self.c * math.sqrt(log_parent / child.visits)
            ucb_value = exploitation + exploration
            
            if ucb_value > best_value:
                best_value = ucb_value
                best_child = child
        
        return best_child or list(node.children.values())[0]
    
    def _expand(self, node: MCTSNode) -> MCTSNode:
        """扩展节点"""
        actions = self.available_actions.get(node.state, [])
        
        if not actions:
            return node
        
        # 扩展所有可能的动作
        for action in actions:
            if action not in node.children:
                # 确定下一状态
                next_state = self._get_next_state(node.state, action)
                child = MCTSNode(
                    state=next_state,
                    parent=node,
                    action=action,
                )
                node.children[action] = child
        
        # 返回一个随机未访问的子节点
        unvisited = [c for c in node.children.values() if c.visits == 0]
        return random.choice(unvisited) if unvisited else random.choice(list(node.children.values()))
    
    def _simulate(self, state: str, depth: int = 0) -> float:
        """随机模拟（rollout）"""
        if self._is_terminal(state) or depth >= self.max_depth:
            return 0.0
        
        actions = self.available_actions.get(state, [])
        if not actions:
            return 0.0
        
        # 随机选择动作
        action = random.choice(actions)
        reward = self.rewards.get((state, action), 0.0)
        
        # 转移到下一状态
        next_state = self._get_next_state(state, action)
        
        # 递归模拟
        future_value = self._simulate(next_state, depth + 1)
        
        return reward + self.gamma * future_value
    
    def _backpropagate(self, node: MCTSNode, value: float):
        """回传更新"""
        while node is not None:
            node.visits += 1
            node.total_value += value
            value *= self.gamma  # 衰减
            node = node.parent
    
    def _get_next_state(self, state: str, action: str) -> str:
        """获取下一状态"""
        if (state, action) in self.transition_probs:
            trans = self.transition_probs[(state, action)]
            states = list(trans.keys())
            probs = [trans[s] for s in states]
            return np.random.choice(states, p=probs)
        return action  # 简化：动作即下一状态
    
    def _is_terminal(self, state: str) -> bool:
        """判断是否终止状态"""
        return state in self.terminal_states or state not in self.available_actions
    
    def _extract_best_path(self) -> List[str]:
        """提取最佳路径"""
        path = [self.root.state]
        node = self.root
        
        while node.children:
            # 选择访问次数最多的子节点
            best_child = max(node.children.values(), key=lambda c: c.visits)
            path.append(best_child.state)
            node = best_child
            
            if len(path) >= self.max_depth:
                break
        
        return path
    
    def _get_action_values(self) -> Dict[str, float]:
        """获取根节点各动作的价值估计"""
        if self.root is None:
            return {}
        
        return {
            action: child.mean_value
            for action, child in self.root.children.items()
        }
    
    def _get_visit_counts(self) -> Dict[str, int]:
        """获取访问计数"""
        counts = {}
        
        def traverse(node: MCTSNode):
            counts[node.state] = counts.get(node.state, 0) + node.visits
            for child in node.children.values():
                traverse(child)
        
        if self.root:
            traverse(self.root)
        
        return counts


class PUCTMCTS(MCTS):
    """
    PUCT MCTS（Predictor + UCB for Trees）
    
    结合神经网络先验的MCTS（AlphaGo/AlphaZero风格）
    
    PUCT = Q(s,a) + c * P(s,a) * √N(s) / (1 + N(s,a))
    
    论文: Silver et al., "Mastering the game of Go with deep neural networks and tree search", 2016
    """
    
    def __init__(self,
                 exploration_constant: float = 1.5,
                 prior_temperature: float = 1.0,
                 **kwargs):
        super().__init__(exploration_constant=exploration_constant, **kwargs)
        self.prior_temp = prior_temperature
        
        # 先验策略网络（简化为函数）
        self.policy_fn: Optional[Callable[[str], Dict[str, float]]] = None
        self.value_fn: Optional[Callable[[str], float]] = None
    
    def set_policy_network(self,
                           policy_fn: Callable[[str], Dict[str, float]],
                           value_fn: Callable[[str], float] = None):
        """设置策略和价值网络"""
        self.policy_fn = policy_fn
        self.value_fn = value_fn
    
    def _expand(self, node: MCTSNode) -> MCTSNode:
        """带先验的扩展"""
        actions = self.available_actions.get(node.state, [])
        
        if not actions:
            return node
        
        # 获取先验概率
        if self.policy_fn:
            priors = self.policy_fn(node.state)
        else:
            # 均匀先验
            priors = {a: 1.0 / len(actions) for a in actions}
        
        # 扩展所有动作
        for action in actions:
            if action not in node.children:
                next_state = self._get_next_state(node.state, action)
                child = MCTSNode(
                    state=next_state,
                    parent=node,
                    action=action,
                    prior=priors.get(action, 1.0 / len(actions)),
                )
                node.children[action] = child
        
        # 按先验概率选择
        unvisited = [c for c in node.children.values() if c.visits == 0]
        if unvisited:
            priors_sum = sum(c.prior for c in unvisited)
            probs = [c.prior / priors_sum for c in unvisited]
            return np.random.choice(unvisited, p=probs)
        
        return random.choice(list(node.children.values()))
    
    def _ucb_select(self, node: MCTSNode) -> MCTSNode:
        """PUCT选择"""
        best_value = float('-inf')
        best_child = None
        
        sqrt_parent = math.sqrt(node.visits)
        
        for child in node.children.values():
            # PUCT = Q + c * P * √N(parent) / (1 + N(child))
            q_value = child.mean_value
            prior_term = self.c * child.prior * sqrt_parent / (1 + child.visits)
            puct_value = q_value + prior_term
            
            if puct_value > best_value:
                best_value = puct_value
                best_child = child
        
        return best_child or list(node.children.values())[0]
    
    def _simulate(self, state: str, depth: int = 0) -> float:
        """使用价值网络（如果有）替代随机rollout"""
        if self._is_terminal(state) or depth >= self.max_depth:
            return 0.0
        
        # 如果有价值网络，直接评估
        if self.value_fn:
            return self.value_fn(state)
        
        # 否则使用随机rollout
        return super()._simulate(state, depth)


class RAVEMCTS(MCTS):
    """
    RAVE MCTS（Rapid Action Value Estimation）
    
    在回传时更新所有后续出现过此动作的节点
    加速学习动作价值
    
    论文: Gelly & Silver, "Monte-Carlo tree search and rapid action value estimation", 2011
    """
    
    def __init__(self, rave_constant: float = 100, **kwargs):
        super().__init__(**kwargs)
        self.k = rave_constant  # RAVE权重参数
    
    def _select(self, node: MCTSNode) -> Tuple[MCTSNode, int]:
        """带RAVE的选择"""
        depth = 0
        path_actions = set()  # 记录路径上的动作
        
        while not node.is_leaf and not self._is_terminal(node.state):
            node = self._rave_select(node)
            if node.action:
                path_actions.add(node.action)
            depth += 1
            
            if depth >= self.max_depth:
                break
        
        return node, depth
    
    def _rave_select(self, node: MCTSNode) -> MCTSNode:
        """RAVE-UCB选择"""
        best_value = float('-inf')
        best_child = None
        
        log_parent = math.log(max(node.visits, 1))
        
        for child in node.children.values():
            if child.visits == 0:
                return child
            
            # RAVE权重 β = sqrt(k / (3n + k))
            beta = math.sqrt(self.k / (3 * child.visits + self.k))
            
            # 混合MC和RAVE估计
            mc_value = child.mean_value
            rave_value = child.rave_value / max(child.rave_visits, 1)
            
            q_value = (1 - beta) * mc_value + beta * rave_value
            
            exploration = self.c * math.sqrt(log_parent / child.visits)
            
            total_value = q_value + exploration
            
            if total_value > best_value:
                best_value = total_value
                best_child = child
        
        return best_child or list(node.children.values())[0]
    
    def _backpropagate(self, node: MCTSNode, value: float):
        """带RAVE的回传"""
        # 收集路径上的所有动作
        path_actions = set()
        temp_node = node
        while temp_node is not None:
            if temp_node.action:
                path_actions.add(temp_node.action)
            temp_node = temp_node.parent
        
        # 更新路径上的节点
        current = node
        while current is not None:
            current.visits += 1
            current.total_value += value
            
            # RAVE更新：更新所有出现在后续路径中的动作
            for action, child in current.children.items():
                if action in path_actions:
                    child.rave_visits += 1
                    child.rave_value += value
            
            value *= self.gamma
            current = current.parent


class ProgressiveWideningMCTS(MCTS):
    """
    渐进拓宽MCTS
    
    在大动作空间中，逐步扩展动作而非一次展开全部
    子节点数限制：k * N^α （N为访问次数）
    
    论文: Coulom, "Computing 'Elo ratings' of move patterns in the game of Go", 2007
    """
    
    def __init__(self, widening_constant: float = 1.0,
                 widening_exponent: float = 0.5, **kwargs):
        super().__init__(**kwargs)
        self.k = widening_constant
        self.alpha = widening_exponent
    
    def _should_expand(self, node: MCTSNode) -> bool:
        """判断是否应该扩展新子节点"""
        current_children = len(node.children)
        allowed_children = self.k * (node.visits ** self.alpha)
        return current_children < allowed_children
    
    def _expand(self, node: MCTSNode) -> MCTSNode:
        """渐进扩展"""
        actions = self.available_actions.get(node.state, [])
        
        if not actions:
            return node
        
        # 获取未扩展的动作
        unexpanded = [a for a in actions if a not in node.children]
        
        if unexpanded and self._should_expand(node):
            # 随机选择一个新动作扩展
            action = random.choice(unexpanded)
            next_state = self._get_next_state(node.state, action)
            child = MCTSNode(
                state=next_state,
                parent=node,
                action=action,
            )
            node.children[action] = child
            return child
        elif node.children:
            # 返回已有子节点中未访问的
            unvisited = [c for c in node.children.values() if c.visits == 0]
            if unvisited:
                return random.choice(unvisited)
            return random.choice(list(node.children.values()))
        
        return node


class ParallelMCTS:
    """
    并行MCTS
    
    使用虚拟损失（Virtual Loss）实现树并行
    """
    
    def __init__(self,
                 num_workers: int = 4,
                 virtual_loss: float = 3.0,
                 **kwargs):
        self.num_workers = num_workers
        self.virtual_loss = virtual_loss
        self.base_mcts = MCTS(**kwargs)
        
        # 虚拟访问计数（用于并行）
        self.virtual_visits: Dict[str, int] = {}
    
    def search(self, root_state: str, num_simulations: int = 1000) -> MCTSResult:
        """并行搜索（简化版：顺序执行但使用虚拟损失）"""
        self.base_mcts.root = MCTSNode(state=root_state)
        self.virtual_visits.clear()
        
        batch_size = self.num_workers
        total_sims = 0
        
        start_time = time.time()
        
        while total_sims < num_simulations:
            batch = min(batch_size, num_simulations - total_sims)
            
            # 批量选择（带虚拟损失）
            selected_nodes = []
            for _ in range(batch):
                node = self._select_with_virtual_loss()
                selected_nodes.append(node)
                self._add_virtual_loss(node)
            
            # 批量扩展和模拟
            values = []
            for node in selected_nodes:
                if not self.base_mcts._is_terminal(node.state):
                    node = self.base_mcts._expand(node)
                value = self.base_mcts._simulate(node.state)
                values.append((node, value))
            
            # 批量回传（移除虚拟损失）
            for node, value in values:
                self._remove_virtual_loss(node)
                self.base_mcts._backpropagate(node, value)
            
            total_sims += batch
        
        # 构建结果
        return MCTSResult(
            best_path=self.base_mcts._extract_best_path(),
            expected_value=self.base_mcts.root.mean_value,
            visit_counts=self.base_mcts._get_visit_counts(),
            action_values=self.base_mcts._get_action_values(),
            simulation_count=total_sims,
            search_time=time.time() - start_time,
            tree_depth=self.base_mcts.max_depth,
        )
    
    def _select_with_virtual_loss(self) -> MCTSNode:
        """带虚拟损失的选择"""
        node = self.base_mcts.root
        
        while not node.is_leaf:
            best_value = float('-inf')
            best_child = None
            
            log_parent = math.log(max(node.visits + self.virtual_visits.get(node.state, 0), 1))
            
            for child in node.children.values():
                effective_visits = child.visits + self.virtual_visits.get(child.state, 0)
                
                if effective_visits == 0:
                    return child
                
                exploitation = child.total_value / max(effective_visits, 1)
                exploration = self.base_mcts.c * math.sqrt(log_parent / effective_visits)
                
                value = exploitation + exploration
                
                if value > best_value:
                    best_value = value
                    best_child = child
            
            node = best_child or list(node.children.values())[0]
        
        return node
    
    def _add_virtual_loss(self, node: MCTSNode):
        """添加虚拟损失"""
        while node is not None:
            self.virtual_visits[node.state] = \
                self.virtual_visits.get(node.state, 0) + int(self.virtual_loss)
            node = node.parent
    
    def _remove_virtual_loss(self, node: MCTSNode):
        """移除虚拟损失"""
        while node is not None:
            if node.state in self.virtual_visits:
                self.virtual_visits[node.state] -= int(self.virtual_loss)
            node = node.parent


class CareerMCTSPlanner:
    """
    职业路径MCTS规划器
    
    使用MCTS探索最优职业发展路径
    """
    
    MCTS_VARIANTS = {
        'basic': MCTS,
        'puct': PUCTMCTS,
        'rave': RAVEMCTS,
        'progressive': ProgressiveWideningMCTS,
        'parallel': ParallelMCTS,
    }
    
    def __init__(self, variant: str = 'puct', **kwargs):
        if variant not in self.MCTS_VARIANTS:
            raise ValueError(f"未知变体: {variant}")
        
        self.variant = variant
        self.mcts_kwargs = kwargs
        self.mcts = None
        
        # 职业数据
        self.position_values: Dict[str, float] = {}
        self.skill_requirements: Dict[str, Set[str]] = {}
    
    def build_career_tree(self,
                          career_paths: list,
                          position_values: Dict[str, float] = None):
        """从职业路径数据构建搜索树环境"""
        actions = defaultdict(list)
        rewards = {}
        transitions = {}
        
        for path in career_paths:
            from_pos = path.get('from_position') or getattr(path, 'from_position', None)
            to_pos = path.get('to_position') or getattr(path, 'to_position', None)
            
            if not from_pos or not to_pos:
                continue
            
            actions[from_pos].append(to_pos)
            
            # 计算奖励
            difficulty = path.get('difficulty') or getattr(path, 'difficulty', 3)
            base_reward = 10.0
            
            if position_values:
                value_gain = position_values.get(to_pos, 50) - position_values.get(from_pos, 50)
                base_reward += value_gain * 0.1
            
            rewards[(from_pos, to_pos)] = base_reward - (difficulty - 1) * 2
            
            # 转移概率
            success_prob = max(0.1, 1.0 - (difficulty - 1) * 0.15)
            transitions[(from_pos, to_pos)] = {
                to_pos: success_prob,
                from_pos: 1.0 - success_prob,
            }
            
            # 技能要求
            skills = path.get('required_skills') or getattr(path, 'required_skills', [])
            if isinstance(skills, str):
                import json
                try:
                    skills = json.loads(skills)
                except:
                    skills = []
            self.skill_requirements[to_pos] = set(skills)
        
        self.position_values = position_values or {}
        
        # 创建MCTS实例
        MCTSClass = self.MCTS_VARIANTS[self.variant]
        self.mcts = MCTSClass(**self.mcts_kwargs)
        self.mcts.set_environment(dict(actions), rewards, transitions)
        
        # 如果是PUCT，设置策略网络
        if isinstance(self.mcts, PUCTMCTS):
            self.mcts.set_policy_network(
                policy_fn=self._default_policy,
                value_fn=self._default_value,
            )
        
        logger.info(f"职业搜索树构建完成，{len(actions)} 个职位")
    
    def _default_policy(self, state: str) -> Dict[str, float]:
        """默认策略（基于职位价值）"""
        actions = self.mcts.available_actions.get(state, [])
        if not actions:
            return {}
        
        # 基于职位价值的softmax策略
        values = [self.position_values.get(a, 50) for a in actions]
        max_val = max(values)
        exp_vals = [math.exp((v - max_val) / 10) for v in values]
        total = sum(exp_vals)
        
        return {a: e / total for a, e in zip(actions, exp_vals)}
    
    def _default_value(self, state: str) -> float:
        """默认价值函数"""
        return self.position_values.get(state, 50) / 100
    
    def plan_career_path(self,
                         current_position: str,
                         current_skills: List[str] = None,
                         target_position: str = None,
                         num_simulations: int = 1000,
                         time_limit: float = 5.0) -> Dict:
        """
        规划职业发展路径
        
        Args:
            current_position: 当前职位
            current_skills: 当前技能列表
            target_position: 目标职位（可选）
            num_simulations: 模拟次数
            time_limit: 时间限制
        
        Returns:
            规划结果字典
        """
        if self.mcts is None:
            raise RuntimeError("请先调用 build_career_tree()")
        
        # 如果有目标，调整终止状态
        if target_position:
            self.mcts.terminal_states.add(target_position)
        
        # 执行MCTS搜索
        result = self.mcts.search(
            current_position,
            num_simulations=num_simulations,
            time_limit=time_limit,
        )
        
        # 分析技能差距
        skill_analysis = []
        if current_skills:
            current_set = set(current_skills)
            for pos in result.best_path[1:]:
                required = self.skill_requirements.get(pos, set())
                gap = required - current_set
                skill_analysis.append({
                    'position': pos,
                    'required_skills': list(required),
                    'missing_skills': list(gap),
                    'readiness': 1 - len(gap) / max(len(required), 1),
                })
        
        return {
            'best_path': result.best_path,
            'expected_value': result.expected_value,
            'path_length': len(result.best_path) - 1,
            'simulation_count': result.simulation_count,
            'search_time': result.search_time,
            'alternative_first_steps': [
                {'action': a, 'value': v, 'visits': result.visit_counts.get(a, 0)}
                for a, v in sorted(result.action_values.items(), key=lambda x: -x[1])[:5]
            ],
            'skill_analysis': skill_analysis,
            'mcts_variant': self.variant,
        }
    
    def compare_paths(self,
                      current_position: str,
                      candidate_targets: List[str],
                      num_simulations: int = 500) -> List[Dict]:
        """
        比较多个目标路径
        
        Returns:
            各目标路径的分析结果
        """
        results = []
        
        for target in candidate_targets:
            plan = self.plan_career_path(
                current_position=current_position,
                target_position=target,
                num_simulations=num_simulations,
            )
            
            results.append({
                'target': target,
                'best_path': plan['best_path'],
                'expected_value': plan['expected_value'],
                'path_length': plan['path_length'],
                'feasibility_score': 100 * min(1.0, 10 / max(plan['path_length'], 1)),
            })
        
        # 按期望价值排序
        results.sort(key=lambda x: -x['expected_value'])
        
        return results


logger.info("蒙特卡洛树搜索模块加载完成")

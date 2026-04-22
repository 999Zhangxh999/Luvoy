# ============================================
# 强化学习增强模块（Advanced Reinforcement Learning）
# 
# 技术栈：
#   - Q-Learning / SARSA：表格型强化学习
#   - Deep Q-Network (DQN)：深度Q学习
#   - Double DQN：解决Q值过估计问题
#   - Dueling DQN：分离状态价值和优势函数
#   - Policy Gradient (REINFORCE)：策略梯度算法
#   - Actor-Critic (A2C)：演员-评论家架构
#   - Prioritized Experience Replay：优先经验回放
#   - TD(λ)：时序差分学习
#
# 应用场景：
#   - 动态职业路径规划
#   - 个性化学习路径推荐
#   - 长期职业发展策略优化
#   - 技能提升序列规划
# ============================================
import logging
import numpy as np
from typing import List, Dict, Tuple, Optional, Callable, Any
from collections import defaultdict, deque
from dataclasses import dataclass
import random
import math

logger = logging.getLogger(__name__)

# 尝试导入PyTorch（深度强化学习）
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    import torch.nn.functional as F
    PYTORCH_AVAILABLE = True
except ImportError:
    PYTORCH_AVAILABLE = False
    logger.info("PyTorch未安装，深度强化学习功能受限")


@dataclass
class Experience:
    """经验元组"""
    state: str
    action: str
    reward: float
    next_state: str
    done: bool
    priority: float = 1.0


@dataclass
class RLResult:
    """强化学习结果"""
    optimal_path: List[str]
    expected_return: float
    q_values: Dict[Tuple[str, str], float]
    policy: Dict[str, str]
    convergence_history: List[float]
    algorithm: str
    iterations: int


class PrioritizedReplayBuffer:
    """
    优先经验回放缓冲区
    
    基于TD误差的优先级采样，重要经验被更频繁地学习
    
    论文: Schaul et al., "Prioritized Experience Replay", 2015
    """
    
    def __init__(self, capacity: int = 10000, alpha: float = 0.6, beta: float = 0.4):
        """
        Args:
            capacity: 缓冲区容量
            alpha: 优先级指数（0=均匀采样, 1=完全按优先级）
            beta: 重要性采样权重指数
        """
        self.capacity = capacity
        self.alpha = alpha
        self.beta = beta
        self.beta_increment = 0.001
        
        self.buffer: List[Experience] = []
        self.priorities = np.zeros(capacity, dtype=np.float32)
        self.position = 0
        self.max_priority = 1.0
    
    def push(self, experience: Experience):
        """添加经验"""
        if len(self.buffer) < self.capacity:
            self.buffer.append(experience)
        else:
            self.buffer[self.position] = experience
        
        self.priorities[self.position] = self.max_priority
        self.position = (self.position + 1) % self.capacity
    
    def sample(self, batch_size: int) -> Tuple[List[Experience], np.ndarray, np.ndarray]:
        """
        按优先级采样
        
        Returns:
            experiences: 经验批次
            weights: 重要性采样权重（用于损失校正）
            indices: 采样索引（用于更新优先级）
        """
        N = len(self.buffer)
        if N == 0:
            return [], np.array([]), np.array([])
        
        # 计算采样概率
        priorities = self.priorities[:N]
        probs = priorities ** self.alpha
        probs /= probs.sum()
        
        # 采样
        indices = np.random.choice(N, min(batch_size, N), p=probs, replace=False)
        experiences = [self.buffer[i] for i in indices]
        
        # 重要性采样权重
        self.beta = min(1.0, self.beta + self.beta_increment)
        weights = (N * probs[indices]) ** (-self.beta)
        weights /= weights.max()
        
        return experiences, weights, indices
    
    def update_priorities(self, indices: np.ndarray, td_errors: np.ndarray):
        """根据TD误差更新优先级"""
        for idx, td_error in zip(indices, td_errors):
            priority = abs(td_error) + 1e-6
            self.priorities[idx] = priority
            self.max_priority = max(self.max_priority, priority)


class QLearningAgent:
    """
    Q-Learning 智能体
    
    经典的离策略（Off-Policy）表格型强化学习算法
    
    Q(s,a) ← Q(s,a) + α [r + γ max_a' Q(s',a') - Q(s,a)]
    """
    
    def __init__(self, 
                 learning_rate: float = 0.1,
                 discount_factor: float = 0.95,
                 epsilon: float = 1.0,
                 epsilon_decay: float = 0.995,
                 epsilon_min: float = 0.01):
        self.alpha = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        
        # Q表
        self.q_table: Dict[Tuple[str, str], float] = defaultdict(float)
        
        # 动作空间
        self.actions: Dict[str, List[str]] = {}
        
        # 训练历史
        self.training_history: List[float] = []
    
    def register_state_actions(self, state: str, actions: List[str]):
        """注册状态的可用动作"""
        self.actions[state] = actions
    
    def get_action(self, state: str, explore: bool = True) -> Optional[str]:
        """
        ε-greedy 策略选择动作
        """
        if state not in self.actions or not self.actions[state]:
            return None
        
        if explore and random.random() < self.epsilon:
            # 探索：随机选择
            return random.choice(self.actions[state])
        else:
            # 利用：选择最大Q值动作
            q_values = [(a, self.q_table[(state, a)]) for a in self.actions[state]]
            return max(q_values, key=lambda x: x[1])[0]
    
    def update(self, state: str, action: str, reward: float, 
               next_state: str, done: bool):
        """
        Q-Learning 更新规则
        """
        current_q = self.q_table[(state, action)]
        
        if done or next_state not in self.actions:
            target = reward
        else:
            # max Q(s', a')
            next_actions = self.actions.get(next_state, [])
            if next_actions:
                max_next_q = max(self.q_table[(next_state, a)] for a in next_actions)
            else:
                max_next_q = 0.0
            target = reward + self.gamma * max_next_q
        
        # TD更新
        td_error = target - current_q
        self.q_table[(state, action)] = current_q + self.alpha * td_error
        
        return td_error
    
    def decay_epsilon(self):
        """衰减探索率"""
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
    
    def get_policy(self) -> Dict[str, str]:
        """提取贪婪策略"""
        policy = {}
        for state in self.actions:
            if self.actions[state]:
                q_values = [(a, self.q_table[(state, a)]) for a in self.actions[state]]
                policy[state] = max(q_values, key=lambda x: x[1])[0]
        return policy


class SARSAAgent(QLearningAgent):
    """
    SARSA 智能体
    
    在策略（On-Policy）表格型强化学习算法
    
    Q(s,a) ← Q(s,a) + α [r + γ Q(s',a') - Q(s,a)]
    
    与Q-Learning的区别：使用实际采取的动作a'而非max
    """
    
    def update(self, state: str, action: str, reward: float,
               next_state: str, next_action: Optional[str], done: bool):
        """SARSA 更新规则"""
        current_q = self.q_table[(state, action)]
        
        if done or next_action is None:
            target = reward
        else:
            target = reward + self.gamma * self.q_table[(next_state, next_action)]
        
        td_error = target - current_q
        self.q_table[(state, action)] = current_q + self.alpha * td_error
        
        return td_error


class DoubleQLearningAgent:
    """
    Double Q-Learning 智能体
    
    使用两个Q表解决Q值过估计问题
    
    Q1(s,a) ← Q1(s,a) + α [r + γ Q2(s', argmax_a' Q1(s',a')) - Q1(s,a)]
    
    论文: van Hasselt, "Double Q-learning", 2010
    """
    
    def __init__(self, 
                 learning_rate: float = 0.1,
                 discount_factor: float = 0.95,
                 epsilon: float = 1.0,
                 epsilon_decay: float = 0.995,
                 epsilon_min: float = 0.01):
        self.alpha = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        
        # 双Q表
        self.q1: Dict[Tuple[str, str], float] = defaultdict(float)
        self.q2: Dict[Tuple[str, str], float] = defaultdict(float)
        
        self.actions: Dict[str, List[str]] = {}
    
    def register_state_actions(self, state: str, actions: List[str]):
        self.actions[state] = actions
    
    def get_action(self, state: str, explore: bool = True) -> Optional[str]:
        if state not in self.actions or not self.actions[state]:
            return None
        
        if explore and random.random() < self.epsilon:
            return random.choice(self.actions[state])
        else:
            # 使用两个Q表的平均值选择
            q_values = []
            for a in self.actions[state]:
                avg_q = (self.q1[(state, a)] + self.q2[(state, a)]) / 2
                q_values.append((a, avg_q))
            return max(q_values, key=lambda x: x[1])[0]
    
    def update(self, state: str, action: str, reward: float,
               next_state: str, done: bool):
        """Double Q-Learning 更新"""
        # 随机选择更新哪个Q表
        if random.random() < 0.5:
            q_update, q_eval = self.q1, self.q2
        else:
            q_update, q_eval = self.q2, self.q1
        
        current_q = q_update[(state, action)]
        
        if done or next_state not in self.actions:
            target = reward
        else:
            next_actions = self.actions.get(next_state, [])
            if next_actions:
                # Q1选动作，Q2评估
                best_action = max(next_actions, key=lambda a: q_update[(next_state, a)])
                target = reward + self.gamma * q_eval[(next_state, best_action)]
            else:
                target = reward
        
        td_error = target - current_q
        q_update[(state, action)] = current_q + self.alpha * td_error
        
        return td_error
    
    def decay_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
    
    def get_policy(self) -> Dict[str, str]:
        policy = {}
        for state in self.actions:
            if self.actions[state]:
                q_values = []
                for a in self.actions[state]:
                    avg_q = (self.q1[(state, a)] + self.q2[(state, a)]) / 2
                    q_values.append((a, avg_q))
                policy[state] = max(q_values, key=lambda x: x[1])[0]
        return policy


class TDLambdaAgent:
    """
    TD(λ) 智能体
    
    资格迹（Eligibility Traces）实现的时序差分学习
    结合了MC（完整回报）和TD(0)（单步bootstrap）
    
    λ=0: 等价于TD(0)
    λ=1: 等价于MC
    
    论文: Sutton, "Learning to predict by the methods of temporal differences", 1988
    """
    
    def __init__(self,
                 learning_rate: float = 0.1,
                 discount_factor: float = 0.95,
                 lambda_param: float = 0.8,
                 epsilon: float = 1.0,
                 epsilon_decay: float = 0.995,
                 epsilon_min: float = 0.01,
                 trace_type: str = 'replacing'):  # replacing / accumulating
        self.alpha = learning_rate
        self.gamma = discount_factor
        self.lambda_param = lambda_param
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.trace_type = trace_type
        
        self.q_table: Dict[Tuple[str, str], float] = defaultdict(float)
        self.eligibility: Dict[Tuple[str, str], float] = defaultdict(float)
        self.actions: Dict[str, List[str]] = {}
    
    def register_state_actions(self, state: str, actions: List[str]):
        self.actions[state] = actions
    
    def get_action(self, state: str, explore: bool = True) -> Optional[str]:
        if state not in self.actions or not self.actions[state]:
            return None
        
        if explore and random.random() < self.epsilon:
            return random.choice(self.actions[state])
        else:
            q_values = [(a, self.q_table[(state, a)]) for a in self.actions[state]]
            return max(q_values, key=lambda x: x[1])[0]
    
    def start_episode(self):
        """开始新回合，重置资格迹"""
        self.eligibility.clear()
    
    def update(self, state: str, action: str, reward: float,
               next_state: str, next_action: Optional[str], done: bool):
        """TD(λ) 更新规则（SARSA(λ)变体）"""
        # 计算TD误差
        current_q = self.q_table[(state, action)]
        
        if done or next_action is None:
            target = reward
        else:
            target = reward + self.gamma * self.q_table[(next_state, next_action)]
        
        td_error = target - current_q
        
        # 更新资格迹
        if self.trace_type == 'replacing':
            # 替换迹：置为1
            self.eligibility[(state, action)] = 1.0
        else:
            # 累积迹：+1
            self.eligibility[(state, action)] += 1.0
        
        # 更新所有状态-动作对
        decay_factor = self.gamma * self.lambda_param
        for (s, a), e in list(self.eligibility.items()):
            self.q_table[(s, a)] += self.alpha * td_error * e
            self.eligibility[(s, a)] = e * decay_factor
            
            # 清理小资格迹
            if self.eligibility[(s, a)] < 1e-6:
                del self.eligibility[(s, a)]
        
        return td_error
    
    def decay_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)


class PolicyGradientAgent:
    """
    策略梯度智能体（REINFORCE）
    
    直接参数化策略 π_θ(a|s)，通过梯度上升优化期望回报
    
    ∇J(θ) = E[∑_t ∇log π_θ(a_t|s_t) G_t]
    
    论文: Williams, "Simple Statistical Gradient-Following Algorithms 
          for Connectionist Reinforcement Learning", 1992
    """
    
    def __init__(self,
                 learning_rate: float = 0.01,
                 discount_factor: float = 0.99,
                 baseline: bool = True):
        self.alpha = learning_rate
        self.gamma = discount_factor
        self.use_baseline = baseline
        
        # 策略参数（简化版：Softmax策略）
        # θ(s,a) = 偏好值，策略 π(a|s) = softmax(θ(s,:))
        self.preferences: Dict[Tuple[str, str], float] = defaultdict(float)
        self.actions: Dict[str, List[str]] = {}
        
        # 基线（状态价值估计）
        self.value_estimates: Dict[str, float] = defaultdict(float)
        
        # 当前回合轨迹
        self.trajectory: List[Tuple[str, str, float]] = []
    
    def register_state_actions(self, state: str, actions: List[str]):
        self.actions[state] = actions
    
    def get_policy_probs(self, state: str) -> Dict[str, float]:
        """计算策略概率分布"""
        if state not in self.actions:
            return {}
        
        actions = self.actions[state]
        prefs = np.array([self.preferences[(state, a)] for a in actions])
        
        # Softmax
        exp_prefs = np.exp(prefs - np.max(prefs))  # 数值稳定
        probs = exp_prefs / exp_prefs.sum()
        
        return dict(zip(actions, probs))
    
    def get_action(self, state: str) -> Optional[str]:
        """按策略分布采样动作"""
        probs = self.get_policy_probs(state)
        if not probs:
            return None
        
        actions, probabilities = zip(*probs.items())
        return np.random.choice(actions, p=probabilities)
    
    def record_step(self, state: str, action: str, reward: float):
        """记录轨迹"""
        self.trajectory.append((state, action, reward))
    
    def update(self):
        """回合结束后更新策略"""
        if not self.trajectory:
            return
        
        T = len(self.trajectory)
        
        # 计算回报（从后往前）
        returns = []
        G = 0
        for t in range(T - 1, -1, -1):
            G = self.trajectory[t][2] + self.gamma * G
            returns.insert(0, G)
        
        # 基线（平均回报）
        if self.use_baseline:
            baseline = np.mean(returns)
        else:
            baseline = 0
        
        # 策略梯度更新
        for t, (state, action, _) in enumerate(self.trajectory):
            advantage = returns[t] - baseline
            
            # 更新偏好值
            probs = self.get_policy_probs(state)
            for a in self.actions.get(state, []):
                if a == action:
                    # ∇log π = 1 - π(a|s) for chosen action
                    grad = 1 - probs.get(a, 0.5)
                else:
                    # ∇log π = -π(a|s) for other actions
                    grad = -probs.get(a, 0)
                
                self.preferences[(state, a)] += self.alpha * grad * advantage
        
        # 更新基线
        for t, (state, _, _) in enumerate(self.trajectory):
            self.value_estimates[state] += 0.1 * (returns[t] - self.value_estimates[state])
        
        # 清空轨迹
        self.trajectory.clear()
    
    def get_policy(self) -> Dict[str, str]:
        """提取确定性策略（最大概率动作）"""
        policy = {}
        for state in self.actions:
            probs = self.get_policy_probs(state)
            if probs:
                policy[state] = max(probs.items(), key=lambda x: x[1])[0]
        return policy


class ActorCriticAgent:
    """
    Actor-Critic 智能体（A2C）
    
    结合策略梯度（Actor）和价值函数（Critic）
    - Actor: 学习策略 π_θ(a|s)
    - Critic: 学习价值函数 V_w(s) 或 Q_w(s,a)
    
    优点：方差比纯REINFORCE更低，因为使用TD误差而非完整回报
    
    论文: Konda & Tsitsiklis, "Actor-Critic Algorithms", 1999
    """
    
    def __init__(self,
                 actor_lr: float = 0.01,
                 critic_lr: float = 0.1,
                 discount_factor: float = 0.99,
                 entropy_coef: float = 0.01):  # 熵正则化系数
        self.actor_lr = actor_lr
        self.critic_lr = critic_lr
        self.gamma = discount_factor
        self.entropy_coef = entropy_coef
        
        # Actor参数
        self.preferences: Dict[Tuple[str, str], float] = defaultdict(float)
        
        # Critic参数
        self.values: Dict[str, float] = defaultdict(float)
        
        self.actions: Dict[str, List[str]] = {}
    
    def register_state_actions(self, state: str, actions: List[str]):
        self.actions[state] = actions
    
    def get_policy_probs(self, state: str) -> Dict[str, float]:
        if state not in self.actions:
            return {}
        
        actions = self.actions[state]
        prefs = np.array([self.preferences[(state, a)] for a in actions])
        exp_prefs = np.exp(prefs - np.max(prefs))
        probs = exp_prefs / exp_prefs.sum()
        return dict(zip(actions, probs))
    
    def get_action(self, state: str) -> Optional[str]:
        probs = self.get_policy_probs(state)
        if not probs:
            return None
        actions, probabilities = zip(*probs.items())
        return np.random.choice(actions, p=probabilities)
    
    def update(self, state: str, action: str, reward: float,
               next_state: str, done: bool):
        """
        Actor-Critic 单步更新
        """
        # Critic: 计算TD误差
        v_current = self.values[state]
        v_next = 0.0 if done else self.values[next_state]
        td_target = reward + self.gamma * v_next
        td_error = td_target - v_current
        
        # 更新Critic(价值函数)
        self.values[state] += self.critic_lr * td_error
        
        # Actor: 策略梯度更新
        probs = self.get_policy_probs(state)
        
        # 计算策略熵（用于探索）
        entropy = -sum(p * np.log(p + 1e-10) for p in probs.values())
        
        for a in self.actions.get(state, []):
            if a == action:
                grad = 1 - probs.get(a, 0.5)
            else:
                grad = -probs.get(a, 0)
            
            # 使用TD误差作为优势估计 + 熵正则化
            self.preferences[(state, a)] += self.actor_lr * (
                grad * td_error + self.entropy_coef * entropy
            )
        
        return td_error
    
    def get_policy(self) -> Dict[str, str]:
        policy = {}
        for state in self.actions:
            probs = self.get_policy_probs(state)
            if probs:
                policy[state] = max(probs.items(), key=lambda x: x[1])[0]
        return policy


class CareerRLPlanner:
    """
    职业路径强化学习规划器
    
    整合多种RL算法进行职业路径优化
    """
    
    ALGORITHMS = {
        'q-learning': QLearningAgent,
        'sarsa': SARSAAgent,
        'double-q': DoubleQLearningAgent,
        'td-lambda': TDLambdaAgent,
        'policy-gradient': PolicyGradientAgent,
        'actor-critic': ActorCriticAgent,
    }
    
    def __init__(self, algorithm: str = 'double-q'):
        if algorithm not in self.ALGORITHMS:
            raise ValueError(f"未知算法: {algorithm}，可用: {list(self.ALGORITHMS.keys())}")
        
        self.algorithm_name = algorithm
        self.agent = None
        
        # 环境模型
        self.states: set = set()
        self.transitions: Dict[Tuple[str, str], Dict[str, float]] = {}
        self.rewards: Dict[Tuple[str, str], float] = {}
        self.terminal_states: set = set()
        
        # 训练结果
        self.training_history: List[float] = []
    
    def build_environment(self, career_paths: list, 
                          position_values: Dict[str, float] = None):
        """从职业路径数据构建环境"""
        logger.info(f"构建RL环境，算法: {self.algorithm_name}")
        
        self.states.clear()
        self.transitions.clear()
        self.rewards.clear()
        
        state_actions: Dict[str, List[str]] = defaultdict(list)
        
        for path in career_paths:
            from_pos = path.get('from_position') or getattr(path, 'from_position', None)
            to_pos = path.get('to_position') or getattr(path, 'to_position', None)
            
            if not from_pos or not to_pos:
                continue
            
            self.states.add(from_pos)
            self.states.add(to_pos)
            
            if to_pos not in state_actions[from_pos]:
                state_actions[from_pos].append(to_pos)
            
            # 转移概率
            difficulty = path.get('difficulty') or getattr(path, 'difficulty', 3)
            success_prob = max(0.1, 1.0 - (difficulty - 1) * 0.15)
            
            self.transitions[(from_pos, to_pos)] = {
                to_pos: success_prob,
                from_pos: 1.0 - success_prob,
            }
            
            # 奖励
            base_reward = 10.0
            if position_values:
                value_gain = position_values.get(to_pos, 50) - position_values.get(from_pos, 50)
                base_reward += value_gain * 0.1
            
            self.rewards[(from_pos, to_pos)] = base_reward - (difficulty - 1) * 2
        
        # 确保所有状态有动作
        for state in self.states:
            if not state_actions[state]:
                state_actions[state] = [state]  # 停留
                self.transitions[(state, state)] = {state: 1.0}
                self.rewards[(state, state)] = -1.0
        
        # 创建智能体
        self.agent = self.ALGORITHMS[self.algorithm_name]()
        for state, actions in state_actions.items():
            self.agent.register_state_actions(state, actions)
        
        logger.info(f"环境构建完成：{len(self.states)} 状态, {sum(len(a) for a in state_actions.values())} 动作")
    
    def train(self, num_episodes: int = 500, max_steps: int = 50) -> RLResult:
        """训练智能体"""
        if self.agent is None:
            raise RuntimeError("请先调用 build_environment()")
        
        logger.info(f"开始训练，回合数: {num_episodes}")
        
        self.training_history.clear()
        states_list = list(self.states)
        
        for episode in range(num_episodes):
            # 随机起始状态
            state = random.choice(states_list)
            total_reward = 0.0
            
            # TD(λ)需要重置资格迹
            if hasattr(self.agent, 'start_episode'):
                self.agent.start_episode()
            
            for step in range(max_steps):
                action = self.agent.get_action(state, explore=True)
                if action is None:
                    break
                
                # 环境交互
                next_state, reward, done = self._step(state, action)
                total_reward += reward
                
                # 策略梯度需要记录轨迹
                if isinstance(self.agent, PolicyGradientAgent):
                    self.agent.record_step(state, action, reward)
                elif isinstance(self.agent, (SARSAAgent, TDLambdaAgent)):
                    next_action = self.agent.get_action(next_state, explore=True)
                    self.agent.update(state, action, reward, next_state, next_action, done)
                elif isinstance(self.agent, ActorCriticAgent):
                    self.agent.update(state, action, reward, next_state, done)
                else:
                    self.agent.update(state, action, reward, next_state, done)
                
                state = next_state
                
                if done:
                    break
            
            # 策略梯度回合结束更新
            if isinstance(self.agent, PolicyGradientAgent):
                self.agent.update()
            
            # 衰减探索率
            if hasattr(self.agent, 'decay_epsilon'):
                self.agent.decay_epsilon()
            
            self.training_history.append(total_reward)
            
            if (episode + 1) % 100 == 0:
                avg_reward = np.mean(self.training_history[-100:])
                logger.info(f"Episode {episode+1}, 平均奖励: {avg_reward:.2f}")
        
        # 提取结果
        policy = self.agent.get_policy()
        
        # 获取Q值
        q_values = {}
        if hasattr(self.agent, 'q_table'):
            q_values = dict(self.agent.q_table)
        elif hasattr(self.agent, 'q1'):
            for key in set(self.agent.q1.keys()) | set(self.agent.q2.keys()):
                q_values[key] = (self.agent.q1[key] + self.agent.q2[key]) / 2
        
        # 计算最优路径
        optimal_path = self._extract_optimal_path(policy)
        expected_return = self._compute_expected_return(optimal_path)
        
        return RLResult(
            optimal_path=optimal_path,
            expected_return=expected_return,
            q_values=q_values,
            policy=policy,
            convergence_history=self.training_history,
            algorithm=self.algorithm_name,
            iterations=num_episodes,
        )
    
    def _step(self, state: str, action: str) -> Tuple[str, float, bool]:
        """环境单步交互"""
        if (state, action) not in self.transitions:
            return state, -1.0, False
        
        trans = self.transitions[(state, action)]
        next_states = list(trans.keys())
        probs = [trans[s] for s in next_states]
        
        next_state = np.random.choice(next_states, p=probs)
        reward = self.rewards.get((state, action), 0.0)
        
        done = next_state in self.terminal_states
        
        return next_state, reward, done
    
    def _extract_optimal_path(self, policy: Dict[str, str], 
                              start: str = None, max_len: int = 10) -> List[str]:
        """提取最优路径"""
        if not policy:
            return []
        
        if start is None:
            start = random.choice(list(policy.keys()))
        
        path = [start]
        current = start
        
        for _ in range(max_len):
            if current not in policy:
                break
            
            next_state = policy[current]
            if next_state == current or next_state in path:
                break
            
            path.append(next_state)
            current = next_state
        
        return path
    
    def _compute_expected_return(self, path: List[str], gamma: float = 0.95) -> float:
        """计算路径期望回报"""
        if len(path) < 2:
            return 0.0
        
        total_return = 0.0
        for i in range(len(path) - 1):
            reward = self.rewards.get((path[i], path[i+1]), 0.0)
            total_return += reward * (gamma ** i)
        
        return total_return


# DQN相关（需要PyTorch）
if PYTORCH_AVAILABLE:
    
    class DQNNetwork(nn.Module):
        """DQN 神经网络"""
        
        def __init__(self, state_dim: int, action_dim: int, hidden_dims: List[int] = [128, 64]):
            super().__init__()
            
            layers = []
            prev_dim = state_dim
            
            for dim in hidden_dims:
                layers.extend([
                    nn.Linear(prev_dim, dim),
                    nn.ReLU(),
                    nn.LayerNorm(dim),
                ])
                prev_dim = dim
            
            layers.append(nn.Linear(prev_dim, action_dim))
            
            self.network = nn.Sequential(*layers)
        
        def forward(self, x: torch.Tensor) -> torch.Tensor:
            return self.network(x)
    
    
    class DuelingDQNNetwork(nn.Module):
        """
        Dueling DQN 网络
        
        分离状态价值V(s)和动作优势A(s,a)
        Q(s,a) = V(s) + A(s,a) - mean(A(s,:))
        
        论文: Wang et al., "Dueling Network Architectures for Deep RL", 2015
        """
        
        def __init__(self, state_dim: int, action_dim: int, hidden_dim: int = 128):
            super().__init__()
            
            # 共享特征提取
            self.feature = nn.Sequential(
                nn.Linear(state_dim, hidden_dim),
                nn.ReLU(),
                nn.LayerNorm(hidden_dim),
            )
            
            # 价值流
            self.value_stream = nn.Sequential(
                nn.Linear(hidden_dim, hidden_dim // 2),
                nn.ReLU(),
                nn.Linear(hidden_dim // 2, 1),
            )
            
            # 优势流
            self.advantage_stream = nn.Sequential(
                nn.Linear(hidden_dim, hidden_dim // 2),
                nn.ReLU(),
                nn.Linear(hidden_dim // 2, action_dim),
            )
        
        def forward(self, x: torch.Tensor) -> torch.Tensor:
            features = self.feature(x)
            values = self.value_stream(features)
            advantages = self.advantage_stream(features)
            
            # Q = V + A - mean(A)
            q_values = values + advantages - advantages.mean(dim=-1, keepdim=True)
            return q_values


logger.info("强化学习模块加载完成")

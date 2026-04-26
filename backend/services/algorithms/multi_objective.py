# ============================================
# 多目标优化模块（Multi-Objective Optimization）
# 
# 技术栈：
#   - NSGA-II（非支配排序遗传算法）
#   - NSGA-III（参考点NSGA）
#   - MOEA/D（基于分解的多目标演化）
#   - Pareto前沿优化
#   - 超体积指标（Hypervolume）
#   - 权重向量法
#   - ε-约束法
#
# 应用场景：
#   - 职业-生活平衡优化
#   - 薪资-发展-稳定性多目标权衡
#   - 技能投资组合优化
#   - 个性化职业路径推荐
# ============================================
import logging
import math
import random
import numpy as np
from typing import List, Dict, Tuple, Optional, Callable
from collections import defaultdict
from dataclasses import dataclass, field
import heapq

logger = logging.getLogger(__name__)


@dataclass
class Solution:
    """多目标优化解"""
    decision_vars: np.ndarray          # 决策变量
    objectives: np.ndarray             # 目标函数值
    constraints: np.ndarray = None     # 约束违反程度
    rank: int = 0                      # Pareto排名
    crowding_distance: float = 0.0     # 拥挤度距离
    metadata: Dict = field(default_factory=dict)  # 额外信息
    
    def __lt__(self, other: 'Solution') -> bool:
        """用于排序（先按rank，后按crowding距离降序）"""
        if self.rank != other.rank:
            return self.rank < other.rank
        return self.crowding_distance > other.crowding_distance
    
    def dominates(self, other: 'Solution') -> bool:
        """判断是否支配另一个解"""
        better_in_any = False
        for i in range(len(self.objectives)):
            if self.objectives[i] > other.objectives[i]:
                return False
            if self.objectives[i] < other.objectives[i]:
                better_in_any = True
        return better_in_any


@dataclass
class MOOResult:
    """多目标优化结果"""
    pareto_front: List[Solution]       # Pareto前沿解集
    all_solutions: List[Solution]      # 所有解
    hypervolume: float                 # 超体积指标
    spacing: float                     # 分布均匀性
    num_generations: int               # 迭代代数
    best_compromise: Solution          # 最佳折中解


class NSGAII:
    """
    NSGA-II（Non-dominated Sorting Genetic Algorithm II）
    
    经典的多目标演化算法，特点：
    1. 快速非支配排序 O(MN²)
    2. 拥挤度距离保持多样性
    3. 精英保留策略
    
    论文: Deb et al., "A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II", 2002
    """
    
    def __init__(self,
                 num_objectives: int,
                 num_variables: int,
                 population_size: int = 100,
                 num_generations: int = 200,
                 crossover_prob: float = 0.9,
                 mutation_prob: float = 0.1,
                 variable_bounds: List[Tuple[float, float]] = None):
        self.num_objectives = num_objectives
        self.num_variables = num_variables
        self.pop_size = population_size
        self.num_generations = num_generations
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        
        # 变量边界
        if variable_bounds:
            self.var_bounds = np.array(variable_bounds)
        else:
            self.var_bounds = np.array([(0, 1)] * num_variables)
        
        # 目标函数
        self.objective_functions: List[Callable] = []
        
        # 约束函数
        self.constraint_functions: List[Callable] = []
    
    def set_objective_functions(self, functions: List[Callable]):
        """设置目标函数（最小化）"""
        self.objective_functions = functions
    
    def optimize(self) -> MOOResult:
        """执行优化"""
        logger.info(f"开始NSGA-II优化，{self.num_objectives}目标, {self.pop_size}种群")
        
        # 初始化种群
        population = self._initialize_population()
        
        for gen in range(self.num_generations):
            # 生成子代
            offspring = self._create_offspring(population)
            
            # 合并父代和子代
            combined = population + offspring
            
            # 非支配排序
            fronts = self._fast_non_dominated_sort(combined)
            
            # 选择下一代
            population = self._select_next_generation(fronts)
            
            if (gen + 1) % 50 == 0:
                logger.info(f"Generation {gen+1}, Pareto front size: {len(fronts[0])}")
        
        # 提取结果
        pareto_front = self._extract_pareto_front(population)
        hypervolume = self._compute_hypervolume(pareto_front)
        spacing = self._compute_spacing(pareto_front)
        best_compromise = self._find_compromise(pareto_front)
        
        return MOOResult(
            pareto_front=pareto_front,
            all_solutions=population,
            hypervolume=hypervolume,
            spacing=spacing,
            num_generations=self.num_generations,
            best_compromise=best_compromise,
        )
    
    def _initialize_population(self) -> List[Solution]:
        """初始化种群"""
        population = []
        
        for _ in range(self.pop_size):
            # 随机生成决策变量
            decision_vars = np.random.uniform(
                self.var_bounds[:, 0],
                self.var_bounds[:, 1],
            )
            
            # 计算目标函数值
            objectives = self._evaluate(decision_vars)
            
            solution = Solution(
                decision_vars=decision_vars,
                objectives=objectives,
            )
            population.append(solution)
        
        return population
    
    def _evaluate(self, decision_vars: np.ndarray) -> np.ndarray:
        """评估目标函数"""
        objectives = np.zeros(self.num_objectives)
        
        for i, func in enumerate(self.objective_functions):
            objectives[i] = func(decision_vars)
        
        return objectives
    
    def _fast_non_dominated_sort(self, population: List[Solution]) -> List[List[Solution]]:
        """
        快速非支配排序
        
        时间复杂度: O(MN²), M为目标数, N为种群大小
        """
        fronts = [[]]
        
        # 每个解的支配数和被支配集
        domination_count = {id(s): 0 for s in population}
        dominated_solutions = {id(s): [] for s in population}
        
        for p in population:
            for q in population:
                if p is q:
                    continue
                
                if p.dominates(q):
                    dominated_solutions[id(p)].append(q)
                elif q.dominates(p):
                    domination_count[id(p)] += 1
            
            if domination_count[id(p)] == 0:
                p.rank = 0
                fronts[0].append(p)
        
        # 构建后续前沿
        i = 0
        while fronts[i]:
            next_front = []
            for p in fronts[i]:
                for q in dominated_solutions[id(p)]:
                    domination_count[id(q)] -= 1
                    if domination_count[id(q)] == 0:
                        q.rank = i + 1
                        next_front.append(q)
            i += 1
            fronts.append(next_front)
        
        # 移除空前沿
        return [f for f in fronts if f]
    
    def _compute_crowding_distance(self, front: List[Solution]):
        """计算拥挤度距离"""
        n = len(front)
        if n <= 2:
            for s in front:
                s.crowding_distance = float('inf')
            return
        
        for s in front:
            s.crowding_distance = 0.0
        
        for m in range(self.num_objectives):
            # 按第m个目标排序
            front.sort(key=lambda s: s.objectives[m])
            
            # 边界解设为无穷大
            front[0].crowding_distance = float('inf')
            front[-1].crowding_distance = float('inf')
            
            # 计算中间解的距离
            obj_range = front[-1].objectives[m] - front[0].objectives[m]
            if obj_range == 0:
                continue
            
            for i in range(1, n - 1):
                front[i].crowding_distance += (
                    (front[i+1].objectives[m] - front[i-1].objectives[m]) / obj_range
                )
    
    def _select_next_generation(self, fronts: List[List[Solution]]) -> List[Solution]:
        """选择下一代"""
        new_population = []
        
        for front in fronts:
            self._compute_crowding_distance(front)
            
            if len(new_population) + len(front) <= self.pop_size:
                new_population.extend(front)
            else:
                # 需要截断
                remaining = self.pop_size - len(new_population)
                front.sort(key=lambda s: s.crowding_distance, reverse=True)
                new_population.extend(front[:remaining])
                break
        
        return new_population
    
    def _create_offspring(self, population: List[Solution]) -> List[Solution]:
        """创建子代"""
        offspring = []
        
        while len(offspring) < self.pop_size:
            # 锦标赛选择
            parent1 = self._tournament_select(population)
            parent2 = self._tournament_select(population)
            
            # 交叉
            if random.random() < self.crossover_prob:
                child1_vars, child2_vars = self._sbx_crossover(
                    parent1.decision_vars, parent2.decision_vars
                )
            else:
                child1_vars = parent1.decision_vars.copy()
                child2_vars = parent2.decision_vars.copy()
            
            # 变异
            child1_vars = self._polynomial_mutation(child1_vars)
            child2_vars = self._polynomial_mutation(child2_vars)
            
            # 创建子代解
            for vars in [child1_vars, child2_vars]:
                if len(offspring) < self.pop_size:
                    objectives = self._evaluate(vars)
                    offspring.append(Solution(
                        decision_vars=vars,
                        objectives=objectives,
                    ))
        
        return offspring
    
    def _tournament_select(self, population: List[Solution], k: int = 2) -> Solution:
        """锦标赛选择"""
        candidates = random.sample(population, k)
        return min(candidates)  # 利用Solution的__lt__
    
    def _sbx_crossover(self, parent1: np.ndarray, parent2: np.ndarray,
                       eta: float = 20) -> Tuple[np.ndarray, np.ndarray]:
        """模拟二进制交叉（SBX）"""
        child1 = np.zeros_like(parent1)
        child2 = np.zeros_like(parent2)
        
        for i in range(len(parent1)):
            if random.random() < 0.5:
                if abs(parent1[i] - parent2[i]) > 1e-14:
                    if parent1[i] < parent2[i]:
                        y1, y2 = parent1[i], parent2[i]
                    else:
                        y1, y2 = parent2[i], parent1[i]
                    
                    yl, yu = self.var_bounds[i]
                    
                    # 计算beta
                    rand = random.random()
                    beta = 1.0 + (2.0 * (y1 - yl) / (y2 - y1))
                    alpha = 2.0 - beta ** (-(eta + 1.0))
                    
                    if rand <= 1.0 / alpha:
                        betaq = (rand * alpha) ** (1.0 / (eta + 1.0))
                    else:
                        betaq = (1.0 / (2.0 - rand * alpha)) ** (1.0 / (eta + 1.0))
                    
                    c1 = 0.5 * ((y1 + y2) - betaq * (y2 - y1))
                    c2 = 0.5 * ((y1 + y2) + betaq * (y2 - y1))
                    
                    child1[i] = np.clip(c1, yl, yu)
                    child2[i] = np.clip(c2, yl, yu)
                else:
                    child1[i] = parent1[i]
                    child2[i] = parent2[i]
            else:
                child1[i] = parent1[i]
                child2[i] = parent2[i]
        
        return child1, child2
    
    def _polynomial_mutation(self, individual: np.ndarray,
                             eta: float = 20) -> np.ndarray:
        """多项式变异"""
        mutant = individual.copy()
        
        for i in range(len(mutant)):
            if random.random() < self.mutation_prob:
                yl, yu = self.var_bounds[i]
                y = mutant[i]
                
                delta1 = (y - yl) / (yu - yl)
                delta2 = (yu - y) / (yu - yl)
                
                rand = random.random()
                mut_pow = 1.0 / (eta + 1.0)
                
                if rand < 0.5:
                    xy = 1.0 - delta1
                    val = 2.0 * rand + (1.0 - 2.0 * rand) * (xy ** (eta + 1.0))
                    deltaq = val ** mut_pow - 1.0
                else:
                    xy = 1.0 - delta2
                    val = 2.0 * (1.0 - rand) + 2.0 * (rand - 0.5) * (xy ** (eta + 1.0))
                    deltaq = 1.0 - val ** mut_pow
                
                mutant[i] = np.clip(y + deltaq * (yu - yl), yl, yu)
        
        return mutant
    
    def _extract_pareto_front(self, population: List[Solution]) -> List[Solution]:
        """提取Pareto前沿"""
        fronts = self._fast_non_dominated_sort(population)
        return fronts[0] if fronts else []
    
    def _compute_hypervolume(self, pareto_front: List[Solution],
                             reference: np.ndarray = None) -> float:
        """
        计算超体积指标
        
        超体积是Pareto前沿与参考点围成的空间体积
        """
        if not pareto_front:
            return 0.0
        
        # 默认参考点（各目标最大值+1）
        if reference is None:
            reference = np.max([s.objectives for s in pareto_front], axis=0) + 1
        
        # 简化的2D超体积计算
        if self.num_objectives == 2:
            points = sorted([s.objectives.tolist() for s in pareto_front],
                           key=lambda x: x[0])
            
            hv = 0.0
            prev_x = points[0][0]
            
            for i, (x, y) in enumerate(points):
                if i > 0:
                    hv += (x - prev_x) * (reference[1] - points[i-1][1])
                prev_x = x
            
            hv += (reference[0] - points[-1][0]) * (reference[1] - points[-1][1])
            
            return hv
        
        # 多维使用近似方法
        return self._approximate_hypervolume(pareto_front, reference)
    
    def _approximate_hypervolume(self, pareto_front: List[Solution],
                                 reference: np.ndarray,
                                 num_samples: int = 10000) -> float:
        """蒙特卡洛近似超体积"""
        # 计算边界
        mins = np.min([s.objectives for s in pareto_front], axis=0)
        
        # 采样
        count = 0
        for _ in range(num_samples):
            sample = np.random.uniform(mins, reference)
            
            # 检查是否被某个解支配
            dominated = False
            for sol in pareto_front:
                if all(sol.objectives <= sample):
                    dominated = True
                    break
            
            if dominated:
                count += 1
        
        # 估计体积
        total_volume = np.prod(reference - mins)
        return (count / num_samples) * total_volume
    
    def _compute_spacing(self, pareto_front: List[Solution]) -> float:
        """计算分布均匀性（Spacing指标）"""
        if len(pareto_front) < 2:
            return 0.0
        
        # 计算每个解到最近解的距离
        distances = []
        for i, sol in enumerate(pareto_front):
            min_dist = float('inf')
            for j, other in enumerate(pareto_front):
                if i != j:
                    dist = np.sum(np.abs(sol.objectives - other.objectives))
                    min_dist = min(min_dist, dist)
            distances.append(min_dist)
        
        d_mean = np.mean(distances)
        spacing = np.sqrt(np.mean([(d - d_mean) ** 2 for d in distances]))
        
        return spacing
    
    def _find_compromise(self, pareto_front: List[Solution]) -> Solution:
        """
        找到折中解
        
        使用归一化后的欧氏距离到理想点
        """
        if not pareto_front:
            return None
        
        # 理想点（各目标最小值）
        ideal = np.min([s.objectives for s in pareto_front], axis=0)
        
        # 最差点（各目标最大值）
        nadir = np.max([s.objectives for s in pareto_front], axis=0)
        
        # 归一化并计算到理想点的距离
        best_sol = None
        best_dist = float('inf')
        
        for sol in pareto_front:
            # 归一化
            normalized = (sol.objectives - ideal) / (nadir - ideal + 1e-8)
            dist = np.linalg.norm(normalized)
            
            if dist < best_dist:
                best_dist = dist
                best_sol = sol
        
        return best_sol


class MOEAD:
    """
    MOEA/D（Multi-Objective Evolutionary Algorithm based on Decomposition）
    
    将多目标问题分解为多个标量子问题
    使用邻域信息进行进化
    
    论文: Zhang & Li, "MOEA/D: A Multiobjective Evolutionary Algorithm Based on Decomposition", 2007
    """
    
    def __init__(self,
                 num_objectives: int,
                 num_variables: int,
                 population_size: int = 100,
                 num_generations: int = 200,
                 neighborhood_size: int = 20,
                 decomposition: str = 'tchebycheff'):  # tchebycheff / weighted_sum / pbi
        self.num_objectives = num_objectives
        self.num_variables = num_variables
        self.pop_size = population_size
        self.num_generations = num_generations
        self.T = neighborhood_size
        self.decomposition = decomposition
        
        # 权重向量
        self.weight_vectors: np.ndarray = None
        
        # 邻域
        self.neighborhoods: List[List[int]] = []
        
        # 理想点
        self.ideal_point: np.ndarray = None
        
        # 变量边界
        self.var_bounds = np.array([(0, 1)] * num_variables)
        
        # 目标函数
        self.objective_functions: List[Callable] = []
    
    def set_objective_functions(self, functions: List[Callable]):
        self.objective_functions = functions
    
    def optimize(self) -> MOOResult:
        """执行优化"""
        logger.info(f"开始MOEA/D优化，分解方法: {self.decomposition}")
        
        # 初始化权重向量
        self._init_weight_vectors()
        
        # 初始化邻域
        self._init_neighborhoods()
        
        # 初始化种群
        population = self._initialize_population()
        
        # 初始化理想点
        self.ideal_point = np.min([s.objectives for s in population], axis=0)
        
        for gen in range(self.num_generations):
            for i in range(self.pop_size):
                # 从邻域中选择父代
                neighbors = self.neighborhoods[i]
                parent_indices = random.sample(neighbors, 2)
                
                # 交叉变异
                child_vars = self._variation(
                    population[parent_indices[0]].decision_vars,
                    population[parent_indices[1]].decision_vars,
                )
                
                child_objectives = self._evaluate(child_vars)
                child = Solution(decision_vars=child_vars, objectives=child_objectives)
                
                # 更新理想点
                self.ideal_point = np.minimum(self.ideal_point, child_objectives)
                
                # 更新邻域解
                for j in neighbors:
                    if self._subproblem_value(child, j) < \
                       self._subproblem_value(population[j], j):
                        population[j] = child
            
            if (gen + 1) % 50 == 0:
                logger.info(f"Generation {gen+1}")
        
        # 提取Pareto前沿
        pareto_front = self._extract_pareto_front(population)
        hypervolume = self._compute_hypervolume(pareto_front)
        
        return MOOResult(
            pareto_front=pareto_front,
            all_solutions=population,
            hypervolume=hypervolume,
            spacing=0.0,
            num_generations=self.num_generations,
            best_compromise=self._find_compromise(pareto_front),
        )
    
    def _init_weight_vectors(self):
        """初始化均匀分布的权重向量"""
        if self.num_objectives == 2:
            self.weight_vectors = np.array([
                [i / (self.pop_size - 1), 1 - i / (self.pop_size - 1)]
                for i in range(self.pop_size)
            ])
        else:
            # 使用Das-Dennis方法生成
            self.weight_vectors = self._das_dennis_weights(
                self.num_objectives, self.pop_size
            )
    
    def _das_dennis_weights(self, num_obj: int, num_points: int) -> np.ndarray:
        """Das-Dennis方法生成参考点"""
        # 简化实现
        weights = []
        H = int(np.ceil(num_points ** (1 / num_obj)))
        
        def recursive_fill(current, remaining, depth):
            if depth == num_obj - 1:
                w = current + [remaining / H]
                weights.append(w)
                return
            
            for i in range(remaining + 1):
                recursive_fill(current + [i / H], remaining - i, depth + 1)
        
        recursive_fill([], H, 0)
        
        # 截断或补充
        if len(weights) > num_points:
            weights = random.sample(weights, num_points)
        elif len(weights) < num_points:
            weights = weights + [weights[i % len(weights)] for i in range(num_points - len(weights))]
        
        return np.array(weights)
    
    def _init_neighborhoods(self):
        """初始化基于权重向量的邻域"""
        self.neighborhoods = []
        
        # 计算权重向量之间的距离
        distances = np.zeros((self.pop_size, self.pop_size))
        for i in range(self.pop_size):
            for j in range(self.pop_size):
                distances[i, j] = np.linalg.norm(
                    self.weight_vectors[i] - self.weight_vectors[j]
                )
        
        # 每个向量的T个最近邻
        for i in range(self.pop_size):
            neighbors = np.argsort(distances[i])[:self.T].tolist()
            self.neighborhoods.append(neighbors)
    
    def _subproblem_value(self, solution: Solution, index: int) -> float:
        """计算子问题目标值"""
        weight = self.weight_vectors[index]
        objectives = solution.objectives
        
        if self.decomposition == 'weighted_sum':
            return np.dot(weight, objectives)
        
        elif self.decomposition == 'tchebycheff':
            # max_i weight_i * |f_i - z_i*|
            return np.max(weight * np.abs(objectives - self.ideal_point))
        
        elif self.decomposition == 'pbi':
            # Penalty-based Boundary Intersection
            theta = 5.0  # 惩罚参数
            d1 = np.dot(objectives - self.ideal_point, weight) / np.linalg.norm(weight)
            d2 = np.linalg.norm(objectives - self.ideal_point - d1 * weight / np.linalg.norm(weight))
            return d1 + theta * d2
        
        return 0.0
    
    def _initialize_population(self) -> List[Solution]:
        """初始化种群"""
        population = []
        
        for _ in range(self.pop_size):
            decision_vars = np.random.uniform(
                self.var_bounds[:, 0],
                self.var_bounds[:, 1],
            )
            objectives = self._evaluate(decision_vars)
            population.append(Solution(
                decision_vars=decision_vars,
                objectives=objectives,
            ))
        
        return population
    
    def _evaluate(self, decision_vars: np.ndarray) -> np.ndarray:
        """评估目标函数"""
        objectives = np.zeros(self.num_objectives)
        for i, func in enumerate(self.objective_functions):
            objectives[i] = func(decision_vars)
        return objectives
    
    def _variation(self, parent1: np.ndarray, parent2: np.ndarray) -> np.ndarray:
        """差分进化变异"""
        # DE/rand/1风格
        F = 0.5  # 缩放因子
        CR = 0.9  # 交叉概率
        
        child = parent1.copy()
        
        for i in range(len(child)):
            if random.random() < CR:
                child[i] = parent1[i] + F * (parent2[i] - parent1[i])
                # 边界处理
                child[i] = np.clip(child[i], self.var_bounds[i, 0], self.var_bounds[i, 1])
        
        return child
    
    def _extract_pareto_front(self, population: List[Solution]) -> List[Solution]:
        """提取Pareto前沿"""
        pareto = []
        for sol in population:
            dominated = False
            for other in population:
                if other.dominates(sol):
                    dominated = True
                    break
            if not dominated:
                pareto.append(sol)
        return pareto
    
    def _compute_hypervolume(self, pareto_front: List[Solution]) -> float:
        """计算超体积"""
        if not pareto_front or self.num_objectives != 2:
            return 0.0
        
        reference = np.max([s.objectives for s in pareto_front], axis=0) + 1
        points = sorted([s.objectives.tolist() for s in pareto_front], key=lambda x: x[0])
        
        hv = 0.0
        prev_x = points[0][0]
        
        for i, (x, y) in enumerate(points):
            if i > 0:
                hv += (x - prev_x) * (reference[1] - points[i-1][1])
            prev_x = x
        
        hv += (reference[0] - points[-1][0]) * (reference[1] - points[-1][1])
        
        return hv
    
    def _find_compromise(self, pareto_front: List[Solution]) -> Solution:
        """找到折中解"""
        if not pareto_front:
            return None
        
        ideal = np.min([s.objectives for s in pareto_front], axis=0)
        nadir = np.max([s.objectives for s in pareto_front], axis=0)
        
        best_sol = None
        best_dist = float('inf')
        
        for sol in pareto_front:
            normalized = (sol.objectives - ideal) / (nadir - ideal + 1e-8)
            dist = np.linalg.norm(normalized)
            
            if dist < best_dist:
                best_dist = dist
                best_sol = sol
        
        return best_sol


class CareerMultiObjectiveOptimizer:
    """
    职业多目标优化器
    
    优化职业选择中的多个目标：
    - 薪资水平
    - 职业发展前景
    - 工作-生活平衡
    - 技能匹配度
    - 地理位置偏好
    """
    
    def __init__(self, algorithm: str = 'nsga2'):
        self.algorithm = algorithm
        self.optimizer = None
        
        # 职业数据
        self.positions: List[str] = []
        self.position_data: Dict[str, Dict] = {}
        
        # 用户偏好
        self.preferences: Dict[str, float] = {}
    
    def load_career_data(self,
                         positions: List[str],
                         position_data: Dict[str, Dict]):
        """
        加载职业数据
        
        position_data格式:
        {
            'position_name': {
                'salary': 15000,          # 薪资
                'growth_potential': 8,    # 发展前景 (1-10)
                'work_life_balance': 6,   # 工作生活平衡 (1-10)
                'required_skills': [...], # 技能要求
                'location': '北京',
            }
        }
        """
        self.positions = positions
        self.position_data = position_data
    
    def set_preferences(self,
                        salary_weight: float = 1.0,
                        growth_weight: float = 1.0,
                        balance_weight: float = 1.0,
                        skill_match_weight: float = 1.0):
        """设置目标权重偏好"""
        self.preferences = {
            'salary': salary_weight,
            'growth': growth_weight,
            'balance': balance_weight,
            'skill_match': skill_match_weight,
        }
    
    def optimize_career_portfolio(self,
                                   current_skills: List[str],
                                   num_positions: int = 3,
                                   population_size: int = 50,
                                   num_generations: int = 100) -> Dict:
        """
        优化职业组合
        
        决策变量: 对每个候选职位的选择权重 (0-1)
        目标: 最大化薪资、发展、平衡，最小化技能差距
        
        Returns:
            优化结果
        """
        num_positions_pool = len(self.positions)
        
        # 定义目标函数（最小化）
        def salary_objective(x):
            # 负的加权薪资（因为NSGA-II最小化）
            total = 0
            for i, weight in enumerate(x):
                pos = self.positions[i]
                data = self.position_data.get(pos, {})
                total += weight * data.get('salary', 0)
            return -total
        
        def growth_objective(x):
            # 负的加权发展分数
            total = 0
            for i, weight in enumerate(x):
                pos = self.positions[i]
                data = self.position_data.get(pos, {})
                total += weight * data.get('growth_potential', 5)
            return -total
        
        def balance_objective(x):
            # 负的加权平衡分数
            total = 0
            for i, weight in enumerate(x):
                pos = self.positions[i]
                data = self.position_data.get(pos, {})
                total += weight * data.get('work_life_balance', 5)
            return -total
        
        def skill_gap_objective(x):
            # 技能差距（需要最小化）
            current_set = set(current_skills)
            gap = 0
            for i, weight in enumerate(x):
                if weight > 0.1:
                    pos = self.positions[i]
                    data = self.position_data.get(pos, {})
                    required = set(data.get('required_skills', []))
                    missing = len(required - current_set)
                    gap += weight * missing
            return gap
        
        # 创建优化器
        if self.algorithm == 'nsga2':
            self.optimizer = NSGAII(
                num_objectives=4,
                num_variables=num_positions_pool,
                population_size=population_size,
                num_generations=num_generations,
                variable_bounds=[(0, 1)] * num_positions_pool,
            )
        else:
            self.optimizer = MOEAD(
                num_objectives=4,
                num_variables=num_positions_pool,
                population_size=population_size,
                num_generations=num_generations,
            )
            self.optimizer.var_bounds = np.array([(0, 1)] * num_positions_pool)
        
        self.optimizer.set_objective_functions([
            salary_objective,
            growth_objective,
            balance_objective,
            skill_gap_objective,
        ])
        
        # 执行优化
        result = self.optimizer.optimize()
        
        # 解析结果
        recommendations = []
        for sol in result.pareto_front[:10]:  # 取前10个Pareto解
            # 选择权重最高的职位
            top_indices = np.argsort(sol.decision_vars)[-num_positions:][::-1]
            
            selected_positions = []
            for idx in top_indices:
                if sol.decision_vars[idx] > 0.1:
                    pos = self.positions[idx]
                    selected_positions.append({
                        'position': pos,
                        'weight': float(sol.decision_vars[idx]),
                        'data': self.position_data.get(pos, {}),
                    })
            
            recommendations.append({
                'positions': selected_positions,
                'objectives': {
                    'salary': -sol.objectives[0],
                    'growth': -sol.objectives[1],
                    'balance': -sol.objectives[2],
                    'skill_gap': sol.objectives[3],
                },
                'rank': sol.rank,
            })
        
        # 找出最佳折中方案
        best_compromise = None
        if result.best_compromise:
            top_indices = np.argsort(result.best_compromise.decision_vars)[-num_positions:][::-1]
            best_compromise = {
                'positions': [
                    {
                        'position': self.positions[idx],
                        'weight': float(result.best_compromise.decision_vars[idx]),
                    }
                    for idx in top_indices
                    if result.best_compromise.decision_vars[idx] > 0.1
                ],
                'objectives': {
                    'salary': -result.best_compromise.objectives[0],
                    'growth': -result.best_compromise.objectives[1],
                    'balance': -result.best_compromise.objectives[2],
                    'skill_gap': result.best_compromise.objectives[3],
                },
            }
        
        return {
            'pareto_recommendations': recommendations,
            'best_compromise': best_compromise,
            'hypervolume': result.hypervolume,
            'num_solutions': len(result.pareto_front),
            'algorithm': self.algorithm,
        }


logger.info("多目标优化模块加载完成")

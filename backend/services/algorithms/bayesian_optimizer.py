# ============================================
# 贝叶斯优化服务（超参数自动调优）
# 
# 技术栈：
#   - 高斯过程回归（Gaussian Process）
#   - 采集函数（Expected Improvement）
#   - 序贯模型优化（SMBO）
#
# 应用场景：
#   - 匹配权重自动优化
#   - 算法超参数调优
#   - 推荐策略优化
# ============================================
import logging
import numpy as np
from typing import List, Dict, Tuple, Callable, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

try:
    from skopt import gp_minimize, forest_minimize
    from skopt.space import Real, Integer, Categorical
    from skopt.utils import use_named_args
    SKOPT_AVAILABLE = True
except ImportError:
    SKOPT_AVAILABLE = False
    logger.warning("scikit-optimize未安装，贝叶斯优化功能禁用")


@dataclass
class OptimizationResult:
    """优化结果"""
    best_params: Dict[str, Any]
    best_score: float
    all_results: List[Tuple[Dict, float]]
    convergence_history: List[float]
    n_iterations: int


class BayesianOptimizer:
    """
    贝叶斯优化器
    
    使用高斯过程建模目标函数，通过采集函数指导搜索，
    高效地找到最优超参数配置。
    """
    
    def __init__(self, n_calls: int = 50, n_random_starts: int = 10,
                 acq_func: str = 'EI', random_state: int = 42):
        """
        Args:
            n_calls: 总迭代次数
            n_random_starts: 随机初始化次数
            acq_func: 采集函数 ('EI'=Expected Improvement, 'LCB'=Lower Confidence Bound)
            random_state: 随机种子
        """
        self.n_calls = n_calls
        self.n_random_starts = n_random_starts
        self.acq_func = acq_func
        self.random_state = random_state
        
        self.optimization_history: List[Tuple[Dict, float]] = []
        self.best_params: Optional[Dict] = None
        self.best_score: Optional[float] = None
    
    def optimize_matching_weights(self, 
                                   evaluation_func: Callable[[Dict], float],
                                   weight_bounds: Dict[str, Tuple[float, float]] = None
                                   ) -> OptimizationResult:
        """
        优化人岗匹配权重
        
        Args:
            evaluation_func: 评估函数，输入权重字典，返回匹配质量分数（越高越好）
            weight_bounds: 权重边界 {权重名: (min, max)}
        Returns:
            OptimizationResult: 优化结果
        """
        if not SKOPT_AVAILABLE:
            logger.warning("scikit-optimize不可用，使用网格搜索替代")
            return self._grid_search_fallback(evaluation_func, weight_bounds)
        
        # 默认权重边界
        if weight_bounds is None:
            weight_bounds = {
                'basic': (0.1, 0.4),
                'skill': (0.2, 0.5),
                'quality': (0.1, 0.3),
                'potential': (0.1, 0.3),
            }
        
        # 构建搜索空间
        space = [Real(low, high, name=name) for name, (low, high) in weight_bounds.items()]
        param_names = list(weight_bounds.keys())
        
        # 目标函数（skopt最小化，所以取负）
        @use_named_args(space)
        def objective(**params):
            # 归一化权重，确保和为1
            total = sum(params.values())
            normalized = {k: v / total for k, v in params.items()}
            
            try:
                score = evaluation_func(normalized)
                self.optimization_history.append((normalized.copy(), score))
                return -score  # 最小化负分数 = 最大化分数
            except Exception as e:
                logger.warning(f"评估失败: {e}")
                return 0.0
        
        # 执行贝叶斯优化
        result = gp_minimize(
            objective,
            space,
            n_calls=self.n_calls,
            n_random_starts=self.n_random_starts,
            acq_func=self.acq_func,
            random_state=self.random_state,
        )
        
        # 提取最佳参数
        best_raw = {name: val for name, val in zip(param_names, result.x)}
        total = sum(best_raw.values())
        self.best_params = {k: v / total for k, v in best_raw.items()}
        self.best_score = -result.fun
        
        return OptimizationResult(
            best_params=self.best_params,
            best_score=self.best_score,
            all_results=self.optimization_history.copy(),
            convergence_history=[-f for f in result.func_vals],
            n_iterations=len(result.func_vals),
        )
    
    def optimize_algorithm_params(self,
                                    evaluation_func: Callable[[Dict], float],
                                    param_space: Dict[str, Tuple]
                                    ) -> OptimizationResult:
        """
        优化算法超参数
        
        Args:
            evaluation_func: 评估函数
            param_space: 参数空间 {参数名: (type, min, max) or (type, choices)}
                        type: 'real', 'integer', 'categorical'
        """
        if not SKOPT_AVAILABLE:
            return self._random_search_fallback(evaluation_func, param_space)
        
        # 构建搜索空间
        space = []
        param_names = []
        
        for name, spec in param_space.items():
            param_type = spec[0]
            param_names.append(name)
            
            if param_type == 'real':
                space.append(Real(spec[1], spec[2], name=name))
            elif param_type == 'integer':
                space.append(Integer(spec[1], spec[2], name=name))
            elif param_type == 'categorical':
                space.append(Categorical(spec[1], name=name))
        
        self.optimization_history = []
        
        @use_named_args(space)
        def objective(**params):
            try:
                score = evaluation_func(params)
                self.optimization_history.append((params.copy(), score))
                return -score
            except Exception as e:
                logger.warning(f"评估失败: {e}")
                return 0.0
        
        result = gp_minimize(
            objective,
            space,
            n_calls=self.n_calls,
            n_random_starts=self.n_random_starts,
            acq_func=self.acq_func,
            random_state=self.random_state,
        )
        
        self.best_params = {name: val for name, val in zip(param_names, result.x)}
        self.best_score = -result.fun
        
        return OptimizationResult(
            best_params=self.best_params,
            best_score=self.best_score,
            all_results=self.optimization_history.copy(),
            convergence_history=[-f for f in result.func_vals],
            n_iterations=len(result.func_vals),
        )
    
    def _grid_search_fallback(self, evaluation_func: Callable, 
                               weight_bounds: Dict) -> OptimizationResult:
        """网格搜索降级方案"""
        logger.info("使用网格搜索...")
        
        if weight_bounds is None:
            weight_bounds = {
                'basic': (0.1, 0.4),
                'skill': (0.2, 0.5),
                'quality': (0.1, 0.3),
                'potential': (0.1, 0.3),
            }
        
        # 生成网格点
        grid_points = 5
        results = []
        
        param_names = list(weight_bounds.keys())
        
        for i in range(grid_points ** len(param_names)):
            params = {}
            idx = i
            for name in param_names:
                low, high = weight_bounds[name]
                step = idx % grid_points
                params[name] = low + (high - low) * step / (grid_points - 1)
                idx //= grid_points
            
            # 归一化
            total = sum(params.values())
            params = {k: v / total for k, v in params.items()}
            
            try:
                score = evaluation_func(params)
                results.append((params, score))
            except:
                continue
        
        if not results:
            return OptimizationResult(
                best_params={k: 0.25 for k in param_names},
                best_score=0.0,
                all_results=[],
                convergence_history=[],
                n_iterations=0,
            )
        
        best = max(results, key=lambda x: x[1])
        
        return OptimizationResult(
            best_params=best[0],
            best_score=best[1],
            all_results=results,
            convergence_history=[r[1] for r in results],
            n_iterations=len(results),
        )
    
    def _random_search_fallback(self, evaluation_func: Callable,
                                 param_space: Dict) -> OptimizationResult:
        """随机搜索降级方案"""
        logger.info("使用随机搜索...")
        
        results = []
        
        for _ in range(self.n_calls):
            params = {}
            for name, spec in param_space.items():
                param_type = spec[0]
                if param_type == 'real':
                    params[name] = np.random.uniform(spec[1], spec[2])
                elif param_type == 'integer':
                    params[name] = np.random.randint(spec[1], spec[2] + 1)
                elif param_type == 'categorical':
                    params[name] = np.random.choice(spec[1])
            
            try:
                score = evaluation_func(params)
                results.append((params, score))
            except:
                continue
        
        if not results:
            return OptimizationResult(
                best_params={},
                best_score=0.0,
                all_results=[],
                convergence_history=[],
                n_iterations=0,
            )
        
        best = max(results, key=lambda x: x[1])
        
        return OptimizationResult(
            best_params=best[0],
            best_score=best[1],
            all_results=results,
            convergence_history=[r[1] for r in results],
            n_iterations=len(results),
        )
    
    def get_optimization_report(self) -> dict:
        """获取优化报告"""
        if not self.optimization_history:
            return {'status': 'not_run'}
        
        scores = [r[1] for r in self.optimization_history]
        
        return {
            'status': 'completed',
            'best_params': self.best_params,
            'best_score': self.best_score,
            'n_iterations': len(self.optimization_history),
            'score_improvement': max(scores) - scores[0] if scores else 0,
            'score_std': float(np.std(scores)) if scores else 0,
            'top_5_configs': sorted(self.optimization_history, 
                                    key=lambda x: x[1], reverse=True)[:5],
        }


class AdaptiveWeightOptimizer:
    """
    自适应权重优化器
    
    根据学生特点和岗位要求动态调整匹配权重
    """
    
    def __init__(self):
        self.bayesian_opt = BayesianOptimizer(n_calls=30, n_random_starts=5)
        self.learned_patterns: Dict[str, Dict] = {}
    
    def optimize_for_student(self, student_features: Dict,
                              job_features: Dict,
                              historical_matches: List[Dict] = None) -> Dict[str, float]:
        """
        为特定学生-岗位组合优化权重
        
        Args:
            student_features: 学生特征
            job_features: 岗位特征
            historical_matches: 历史匹配数据（用于学习）
        """
        # 基于特征的启发式初始权重
        initial_weights = self._compute_initial_weights(student_features, job_features)
        
        if not historical_matches:
            return initial_weights
        
        # 如果有历史数据，使用贝叶斯优化
        def evaluation_func(weights: Dict) -> float:
            total_score = 0.0
            for match in historical_matches:
                # 计算加权分数
                weighted_score = (
                    weights.get('basic', 0.2) * match.get('basic_score', 50) +
                    weights.get('skill', 0.35) * match.get('skill_score', 50) +
                    weights.get('quality', 0.25) * match.get('quality_score', 50) +
                    weights.get('potential', 0.2) * match.get('potential_score', 50)
                )
                
                # 与实际结果对比（假设有满意度反馈）
                satisfaction = match.get('satisfaction', 0.5)
                total_score += weighted_score * satisfaction
            
            return total_score / len(historical_matches)
        
        result = self.bayesian_opt.optimize_matching_weights(evaluation_func)
        
        return result.best_params
    
    def _compute_initial_weights(self, student_features: Dict, 
                                  job_features: Dict) -> Dict[str, float]:
        """基于特征计算初始权重"""
        
        # 默认权重
        weights = {
            'basic': 0.20,
            'skill': 0.35,
            'quality': 0.25,
            'potential': 0.20,
        }
        
        # 根据学生经验调整
        experience_level = student_features.get('experience_level', 'entry')
        if experience_level == 'entry':
            # 新人更看重潜力和学习能力
            weights['potential'] = 0.30
            weights['skill'] = 0.25
        elif experience_level == 'senior':
            # 资深人员更看重技能
            weights['skill'] = 0.45
            weights['potential'] = 0.10
        
        # 根据岗位类型调整
        job_type = job_features.get('type', 'general')
        if job_type == 'technical':
            weights['skill'] = min(0.50, weights['skill'] + 0.10)
        elif job_type == 'management':
            weights['quality'] = min(0.35, weights['quality'] + 0.10)
        
        # 归一化
        total = sum(weights.values())
        return {k: v / total for k, v in weights.items()}
    
    def get_model_info(self) -> dict:
        """获取模型信息"""
        return {
            'model_type': 'AdaptiveWeightOptimizer',
            'bayesian_available': SKOPT_AVAILABLE,
            'learned_patterns': len(self.learned_patterns),
        }

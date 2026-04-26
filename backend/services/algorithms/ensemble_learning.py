# ============================================
# 集成学习服务（多模型融合）
# 
# 技术栈：
#   - Stacking：堆叠多个基分类器
#   - Voting：加权投票融合
#   - Blending：混合预测
#   - 元学习器：学习最优融合策略
#
# 应用场景：
#   - 多维度匹配分数融合
#   - 多算法推荐结果整合
#   - 提升预测稳定性和准确度
# ============================================
import logging
import numpy as np
from typing import List, Dict, Tuple, Callable, Optional, Any
from dataclasses import dataclass
from collections import defaultdict

logger = logging.getLogger(__name__)

try:
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.linear_model import Ridge, ElasticNet
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import cross_val_score
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


@dataclass
class EnsembleResult:
    """集成学习结果"""
    final_score: float
    component_scores: Dict[str, float]
    component_weights: Dict[str, float]
    confidence: float
    explanation: str


class EnsembleMatcher:
    """
    集成匹配器
    
    融合多种匹配算法的结果，提供更可靠的匹配分数
    """
    
    def __init__(self, 
                 fusion_method: str = 'weighted_average',
                 meta_learner: str = 'ridge'):
        """
        Args:
            fusion_method: 融合方法 ('weighted_average', 'voting', 'stacking', 'rank_fusion')
            meta_learner: 元学习器类型 ('ridge', 'rf', 'gbm')
        """
        self.fusion_method = fusion_method
        self.meta_learner_type = meta_learner
        
        # 组件匹配器权重（可学习）
        self.component_weights: Dict[str, float] = {}
        
        # 元学习器（用于Stacking）
        self.meta_learner = None
        self.scaler = StandardScaler() if SKLEARN_AVAILABLE else None
        
        # 历史数据（用于学习）
        self.training_data: List[Tuple[Dict, float]] = []
    
    def register_component(self, name: str, weight: float = 1.0):
        """注册组件匹配器"""
        self.component_weights[name] = weight
        logger.info(f"注册组件: {name}, 权重: {weight}")
    
    def ensemble_match(self, component_scores: Dict[str, float]) -> EnsembleResult:
        """
        集成多个组件的匹配分数
        
        Args:
            component_scores: 各组件分数 {组件名: 分数}
        Returns:
            EnsembleResult: 集成结果
        """
        if not component_scores:
            return EnsembleResult(
                final_score=0.0,
                component_scores={},
                component_weights={},
                confidence=0.0,
                explanation="无组件分数"
            )
        
        if self.fusion_method == 'weighted_average':
            return self._weighted_average_fusion(component_scores)
        elif self.fusion_method == 'voting':
            return self._voting_fusion(component_scores)
        elif self.fusion_method == 'rank_fusion':
            return self._rank_fusion(component_scores)
        elif self.fusion_method == 'stacking':
            return self._stacking_fusion(component_scores)
        else:
            return self._weighted_average_fusion(component_scores)
    
    def _weighted_average_fusion(self, scores: Dict[str, float]) -> EnsembleResult:
        """加权平均融合"""
        total_weight = 0.0
        weighted_sum = 0.0
        
        for name, score in scores.items():
            weight = self.component_weights.get(name, 1.0)
            weighted_sum += score * weight
            total_weight += weight
        
        final_score = weighted_sum / total_weight if total_weight > 0 else 0.0
        
        # 计算置信度（基于组件分数的一致性）
        score_values = list(scores.values())
        if len(score_values) > 1:
            std = np.std(score_values)
            confidence = max(0.0, 1.0 - std / 50)  # 标准差越小，置信度越高
        else:
            confidence = 0.8
        
        return EnsembleResult(
            final_score=final_score,
            component_scores=scores,
            component_weights=self.component_weights.copy(),
            confidence=confidence,
            explanation=f"加权平均融合，{len(scores)}个组件"
        )
    
    def _voting_fusion(self, scores: Dict[str, float]) -> EnsembleResult:
        """
        投票融合
        
        将分数转换为等级，进行多数投票
        """
        # 定义等级边界
        grade_boundaries = [90, 80, 70, 60, 0]
        grade_names = ['优秀', '良好', '中等', '及格', '不及格']
        
        def score_to_grade(score: float) -> int:
            for i, boundary in enumerate(grade_boundaries):
                if score >= boundary:
                    return i
            return len(grade_boundaries) - 1
        
        # 投票统计
        votes = defaultdict(float)
        for name, score in scores.items():
            grade = score_to_grade(score)
            weight = self.component_weights.get(name, 1.0)
            votes[grade] += weight
        
        # 获胜等级
        winning_grade = max(votes.keys(), key=lambda g: votes[g])
        
        # 转换回分数（使用该等级内的平均分数）
        grade_scores = [s for s in scores.values() 
                       if score_to_grade(s) == winning_grade]
        final_score = np.mean(grade_scores) if grade_scores else 50.0
        
        # 置信度：投票一致性
        total_votes = sum(votes.values())
        confidence = votes[winning_grade] / total_votes if total_votes > 0 else 0.5
        
        return EnsembleResult(
            final_score=final_score,
            component_scores=scores,
            component_weights=self.component_weights.copy(),
            confidence=confidence,
            explanation=f"投票融合，最终等级: {grade_names[winning_grade]}"
        )
    
    def _rank_fusion(self, scores: Dict[str, float]) -> EnsembleResult:
        """
        排名融合（Borda Count变种）
        
        在多候选场景中，基于排名而非分数进行融合
        """
        # 对于单个匹配，简单转换排名分
        # 这里实现的是分数标准化后融合
        score_values = list(scores.values())
        
        if len(score_values) < 2:
            return self._weighted_average_fusion(scores)
        
        # Z-score标准化
        mean_score = np.mean(score_values)
        std_score = np.std(score_values) + 1e-8
        
        normalized = {}
        for name, score in scores.items():
            z_score = (score - mean_score) / std_score
            # 转换回百分制
            normalized[name] = 50 + z_score * 15
        
        # 加权平均
        total_weight = 0.0
        weighted_sum = 0.0
        
        for name, norm_score in normalized.items():
            weight = self.component_weights.get(name, 1.0)
            weighted_sum += norm_score * weight
            total_weight += weight
        
        final_score = weighted_sum / total_weight if total_weight > 0 else 50.0
        final_score = max(0, min(100, final_score))  # 限制范围
        
        return EnsembleResult(
            final_score=final_score,
            component_scores=scores,
            component_weights=self.component_weights.copy(),
            confidence=0.75,
            explanation="排名融合（Z-score标准化）"
        )
    
    def _stacking_fusion(self, scores: Dict[str, float]) -> EnsembleResult:
        """
        Stacking融合
        
        使用元学习器学习最优融合策略
        """
        if self.meta_learner is None or not SKLEARN_AVAILABLE:
            return self._weighted_average_fusion(scores)
        
        # 构建特征向量
        feature_names = sorted(scores.keys())
        features = np.array([[scores.get(name, 50.0) for name in feature_names]])
        
        # 标准化
        if self.scaler is not None:
            features = self.scaler.transform(features)
        
        # 预测
        final_score = float(self.meta_learner.predict(features)[0])
        final_score = max(0, min(100, final_score))
        
        return EnsembleResult(
            final_score=final_score,
            component_scores=scores,
            component_weights=self.component_weights.copy(),
            confidence=0.85,
            explanation=f"Stacking融合（{self.meta_learner_type}元学习器）"
        )
    
    def train_meta_learner(self, training_data: List[Tuple[Dict[str, float], float]]):
        """
        训练元学习器
        
        Args:
            training_data: 训练数据 [(组件分数字典, 真实分数), ...]
        """
        if not SKLEARN_AVAILABLE or len(training_data) < 10:
            logger.warning("训练数据不足或sklearn不可用")
            return
        
        # 准备训练数据
        feature_names = sorted(training_data[0][0].keys())
        X = np.array([[d.get(name, 50.0) for name in feature_names] 
                      for d, _ in training_data])
        y = np.array([score for _, score in training_data])
        
        # 标准化
        self.scaler = StandardScaler()
        X = self.scaler.fit_transform(X)
        
        # 选择元学习器
        if self.meta_learner_type == 'ridge':
            self.meta_learner = Ridge(alpha=1.0)
        elif self.meta_learner_type == 'rf':
            self.meta_learner = RandomForestRegressor(n_estimators=50, random_state=42)
        elif self.meta_learner_type == 'gbm':
            self.meta_learner = GradientBoostingRegressor(n_estimators=50, random_state=42)
        else:
            self.meta_learner = Ridge(alpha=1.0)
        
        # 训练
        self.meta_learner.fit(X, y)
        
        # 验证
        cv_scores = cross_val_score(self.meta_learner, X, y, cv=3, scoring='r2')
        logger.info(f"元学习器训练完成，交叉验证R²: {cv_scores.mean():.3f}")
    
    def learn_weights_from_feedback(self, 
                                     feedback_data: List[Tuple[Dict[str, float], float, float]]):
        """
        从反馈数据学习组件权重
        
        Args:
            feedback_data: [(组件分数, 预测分数, 实际满意度), ...]
        """
        if len(feedback_data) < 5:
            return
        
        # 使用简单的相关性分析确定权重
        component_correlations = defaultdict(list)
        
        for comp_scores, pred_score, actual in feedback_data:
            # 计算预测误差
            error = abs(pred_score - actual * 100)  # 假设满意度0-1，转换为0-100
            
            for name, score in comp_scores.items():
                # 组件分数与实际满意度的相关性
                component_correlations[name].append((score, actual))
        
        # 计算每个组件的相关系数
        new_weights = {}
        for name, pairs in component_correlations.items():
            if len(pairs) > 3:
                scores = [p[0] for p in pairs]
                actuals = [p[1] for p in pairs]
                
                # 简单相关系数
                corr = np.corrcoef(scores, actuals)[0, 1]
                if np.isnan(corr):
                    corr = 0.5
                
                # 转换为权重（相关性越高，权重越大）
                new_weights[name] = max(0.1, (corr + 1) / 2)  # 映射到[0.1, 1]
        
        # 归一化
        total = sum(new_weights.values())
        if total > 0:
            self.component_weights = {k: v / total for k, v in new_weights.items()}
        
        logger.info(f"从反馈学习权重: {self.component_weights}")
    
    def get_model_info(self) -> dict:
        """获取模型信息"""
        return {
            'model_type': 'EnsembleMatcher',
            'fusion_method': self.fusion_method,
            'num_components': len(self.component_weights),
            'component_weights': self.component_weights,
            'meta_learner_trained': self.meta_learner is not None,
            'sklearn_available': SKLEARN_AVAILABLE,
        }


class MultiModelRecommender:
    """
    多模型推荐器
    
    整合多种推荐算法的结果
    """
    
    def __init__(self):
        self.recommenders: Dict[str, Callable] = {}
        self.weights: Dict[str, float] = {}
    
    def register_recommender(self, name: str, 
                              recommender: Callable[[Any], List[Tuple[str, float]]],
                              weight: float = 1.0):
        """
        注册推荐器
        
        Args:
            name: 推荐器名称
            recommender: 推荐函数，返回 [(岗位, 分数), ...]
            weight: 权重
        """
        self.recommenders[name] = recommender
        self.weights[name] = weight
    
    def recommend(self, query: Any, top_k: int = 10) -> List[Dict]:
        """
        执行集成推荐
        
        Args:
            query: 查询（学生信息）
            top_k: 返回数量
        """
        all_recommendations = defaultdict(lambda: {'scores': [], 'sources': []})
        
        for name, recommender in self.recommenders.items():
            try:
                results = recommender(query)
                weight = self.weights.get(name, 1.0)
                
                for item, score in results:
                    all_recommendations[item]['scores'].append(score * weight)
                    all_recommendations[item]['sources'].append(name)
            except Exception as e:
                logger.warning(f"推荐器 {name} 失败: {e}")
        
        # 融合分数
        final_results = []
        for item, data in all_recommendations.items():
            # 加权平均
            avg_score = np.mean(data['scores']) if data['scores'] else 0
            
            # 来源多样性加成
            diversity_bonus = len(set(data['sources'])) * 2
            
            final_results.append({
                'item': item,
                'score': avg_score + diversity_bonus,
                'raw_score': avg_score,
                'sources': data['sources'],
                'confidence': len(data['scores']) / len(self.recommenders),
            })
        
        # 排序
        final_results.sort(key=lambda x: x['score'], reverse=True)
        
        return final_results[:top_k]
    
    def get_model_info(self) -> dict:
        """获取模型信息"""
        return {
            'model_type': 'MultiModelRecommender',
            'num_recommenders': len(self.recommenders),
            'recommender_weights': self.weights,
        }

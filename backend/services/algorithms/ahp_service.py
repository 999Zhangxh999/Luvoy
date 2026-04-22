# ============================================
# AHP 层次分析法服务 (Analytic Hierarchy Process)
# 技术亮点：多准则决策 + 一致性检验 + 权重优化
# ============================================
"""
AHP算法说明：
1. 构建判断矩阵：成对比较各维度的相对重要性
2. 计算权重向量：特征值法求解
3. 一致性检验：CR < 0.1 表示判断矩阵一致性可接受
4. 加权综合：用优化后的权重对四维度评分进行加权

应用场景：
- 人岗匹配：四维度（基础/技能/素养/潜力）权重优化
- 岗位排序：Learning to Rank 辅助重排序
"""
import logging
import numpy as np

logger = logging.getLogger(__name__)

# 随机一致性指标 RI（用于一致性检验）
RI_TABLE = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}


class AHPService:
    """
    AHP层次分析法服务 - 多准则决策模型
    
    用于优化人岗匹配的四维度权重：
    - 基础要求 (Basic)
    - 职业技能 (Skill)  
    - 职业素养 (Quality)
    - 发展潜力 (Potential)
    """
    
    def __init__(self):
        # 默认的四维度判断矩阵（基于专家经验）
        # 行列顺序: [基础, 技能, 素养, 潜力]
        self.default_matrix = np.array([
            [1,   1/2, 1,   1],      # 基础要求
            [2,   1,   2,   2],      # 职业技能（最重要）
            [1,   1/2, 1,   1],      # 职业素养
            [1,   1/2, 1,   1],      # 发展潜力
        ])
        
        self.dimension_names = ['basic', 'skill', 'quality', 'potential']
    
    def calculate_weights(self, comparison_matrix: np.ndarray = None) -> dict:
        """
        使用特征值法计算AHP权重
        
        Args:
            comparison_matrix: 成对比较判断矩阵 (n×n)
        Returns:
            dict: {
                'weights': {...},           # 各维度权重
                'consistency_ratio': float, # 一致性比率
                'is_consistent': bool,      # 是否通过一致性检验
            }
        """
        if comparison_matrix is None:
            comparison_matrix = self.default_matrix
        
        n = comparison_matrix.shape[0]
        
        # 方法1: 几何平均法（简单稳定）
        row_products = np.prod(comparison_matrix, axis=1)
        weights_raw = np.power(row_products, 1/n)
        weights = weights_raw / np.sum(weights_raw)  # 归一化
        
        # 计算一致性
        lambda_max, cr = self._calculate_consistency(comparison_matrix, weights)
        
        # 构建返回结果
        weight_dict = {}
        for i, name in enumerate(self.dimension_names[:n]):
            weight_dict[name] = round(float(weights[i]), 4)
        
        result = {
            'weights': weight_dict,
            'lambda_max': round(lambda_max, 4),
            'consistency_index': round((lambda_max - n) / (n - 1), 4) if n > 1 else 0,
            'consistency_ratio': round(cr, 4),
            'is_consistent': cr < 0.1,
        }
        
        logger.info(f"AHP权重计算完成: {weight_dict}, CR={cr:.4f}")
        return result
    
    def _calculate_consistency(self, matrix: np.ndarray, weights: np.ndarray) -> tuple:
        """
        计算一致性比率 CR = CI / RI
        
        Args:
            matrix: 判断矩阵
            weights: 权重向量
        Returns:
            tuple: (最大特征值, 一致性比率)
        """
        n = matrix.shape[0]
        
        # 计算 A*w
        aw = np.dot(matrix, weights)
        
        # 计算最大特征值 λ_max
        lambda_max = np.mean(aw / weights)
        
        # 一致性指标 CI
        if n <= 1:
            return lambda_max, 0.0
        
        ci = (lambda_max - n) / (n - 1)
        
        # 一致性比率 CR = CI / RI
        ri = RI_TABLE.get(n, 1.49)
        cr = ci / ri if ri > 0 else 0
        
        return lambda_max, cr
    
    def optimize_weights_for_job(self, job_profile: dict) -> dict:
        """
        根据岗位特性动态调整权重
        
        不同类型岗位对各维度的重视程度不同：
        - 技术岗：技能权重高
        - 管理岗：素养权重高
        - 初级岗：潜力权重高
        
        Args:
            job_profile: 岗位画像
        Returns:
            dict: 优化后的权重
        """
        # 基础判断矩阵
        matrix = self.default_matrix.copy()
        
        category = job_profile.get('category', '').lower()
        level = job_profile.get('level', '').lower()
        
        # 根据岗位类型调整
        if any(kw in category for kw in ['开发', '工程师', '程序员', '技术', 'java', 'python', '前端', '后端']):
            # 技术岗：技能权重增加
            matrix[1, :] *= 1.3  # 技能行
            matrix[:, 1] /= 1.3  # 技能列（保持互反性）
        
        elif any(kw in category for kw in ['经理', '主管', '总监', '管理', '运营']):
            # 管理岗：素养权重增加
            matrix[2, :] *= 1.3
            matrix[:, 2] /= 1.3
        
        elif any(kw in category for kw in ['产品', '设计', '策划']):
            # 创意岗：创新能力（潜力）权重增加
            matrix[3, :] *= 1.2
            matrix[:, 3] /= 1.2
        
        # 根据岗位层级调整
        if any(kw in level for kw in ['初级', 'junior', '助理', '实习']):
            # 初级岗：降低经验要求，提高潜力权重
            matrix[0, :] *= 0.8  # 基础要求降低
            matrix[:, 0] /= 0.8
            matrix[3, :] *= 1.3  # 潜力提高
            matrix[:, 3] /= 1.3
        
        elif any(kw in level for kw in ['高级', 'senior', '专家', '资深']):
            # 高级岗：技能和基础要求提高
            matrix[0, :] *= 1.2
            matrix[:, 0] /= 1.2
            matrix[1, :] *= 1.2
            matrix[:, 1] /= 1.2
        
        # 重新计算权重
        return self.calculate_weights(matrix)
    
    def weighted_score(self, scores: dict, weights: dict = None) -> float:
        """
        计算加权综合得分
        
        Args:
            scores: {'basic': 80, 'skill': 70, 'quality': 85, 'potential': 75}
            weights: 权重字典，若不提供则使用默认权重
        Returns:
            float: 加权综合得分
        """
        if weights is None:
            weights = self.calculate_weights()['weights']
        
        total = 0.0
        for dim in self.dimension_names:
            score = scores.get(dim, scores.get(f'{dim}_score', 0))
            weight = weights.get(dim, 0.25)
            total += score * weight
        
        return round(total, 2)
    
    def rank_jobs(self, match_results: list, job_profiles: dict = None) -> list:
        """
        使用AHP对匹配结果进行重排序 (Learning to Rank思想)
        
        Args:
            match_results: 匹配结果列表
            job_profiles: 岗位画像字典 {id: profile}
        Returns:
            list: 重排序后的结果
        """
        ranked = []
        
        for mr in match_results:
            scores = {
                'basic': mr.get('basic_score', 50),
                'skill': mr.get('skill_score', 50),
                'quality': mr.get('quality_score', 50),
                'potential': mr.get('potential_score', 50),
            }
            
            # 如果有岗位画像，使用动态权重
            if job_profiles and mr.get('job_profile_id') in job_profiles:
                jp = job_profiles[mr['job_profile_id']]
                weight_result = self.optimize_weights_for_job(jp)
            else:
                weight_result = self.calculate_weights()
            
            ahp_score = self.weighted_score(scores, weight_result['weights'])
            
            ranked.append({
                **mr,
                'ahp_score': ahp_score,
                'ahp_weights': weight_result['weights'],
            })
        
        # 按AHP得分排序
        ranked.sort(key=lambda x: x['ahp_score'], reverse=True)
        
        # 更新排名
        for i, item in enumerate(ranked):
            item['ahp_rank'] = i + 1
        
        return ranked

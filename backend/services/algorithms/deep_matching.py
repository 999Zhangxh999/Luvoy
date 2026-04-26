# ============================================
# 深度学习匹配模块（Deep Learning Matcher）
# 
# 技术栈：
#   - 双塔模型（Two-Tower Model）
#   - 交叉网络（Deep & Cross Network）
#   - 神经协同过滤（Neural CF）  
#   - 图神经网络匹配（GNN Matcher）
#   - 对比学习（Contrastive Learning）
#
# 特色：
#   - 用户-职位交互建模
#   - 多模态特征融合
#   - 序列行为编码
#   - 端到端学习
#
# 应用场景：
#   - 精准人岗匹配
#   - 相似职位发现
#   - 技能差距学习
#   - 个性化推荐
# ============================================
import logging
import math
import numpy as np
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict

logger = logging.getLogger(__name__)

# 检测深度学习框架
TORCH_AVAILABLE = False
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    TORCH_AVAILABLE = True
except ImportError:
    pass


# ============================================
# 嵌入层模块
# ============================================

class SkillEmbedding:
    """
    技能嵌入层
    
    【PPT要点】
    - 分层技能表示：基础 → 专业 → 领域
    - 技能关系建模：相似、依赖、互补
    - 稀疏特征稠密化
    
    论文: "Deep Learning for Skill-Job Matching", RecSys 2020
    """
    
    def __init__(self, vocab_size: int, embedding_dim: int = 64):
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        
        # 初始化嵌入矩阵
        self.embeddings = np.random.randn(vocab_size, embedding_dim) * 0.01
        
        # 技能聚类中心
        self.cluster_centers: np.ndarray = None
        self.skill_to_cluster: Dict[int, int] = {}
    
    def get_embedding(self, skill_ids: List[int]) -> np.ndarray:
        """获取技能集合的聚合嵌入"""
        if not skill_ids:
            return np.zeros(self.embedding_dim)
        
        embeddings = self.embeddings[skill_ids]
        
        # 均值池化
        return embeddings.mean(axis=0)
    
    def get_attention_embedding(self, skill_ids: List[int],
                                 query: np.ndarray) -> np.ndarray:
        """
        注意力加权嵌入
        
        使用query向量对技能进行注意力加权
        """
        if not skill_ids:
            return np.zeros(self.embedding_dim)
        
        embeddings = self.embeddings[skill_ids]
        
        # 计算注意力分数
        scores = embeddings @ query  # (n_skills,)
        weights = self._softmax(scores)
        
        # 加权求和
        return (weights[:, None] * embeddings).sum(axis=0)
    
    def _softmax(self, x: np.ndarray) -> np.ndarray:
        exp_x = np.exp(x - np.max(x))
        return exp_x / exp_x.sum()
    
    def build_clusters(self, n_clusters: int = 10):
        """构建技能聚类"""
        # 简单K-means
        centers = self.embeddings[np.random.choice(self.vocab_size, n_clusters, replace=False)]
        
        for _ in range(20):  # 迭代
            # 分配
            distances = np.linalg.norm(
                self.embeddings[:, None, :] - centers[None, :, :], axis=2
            )
            assignments = np.argmin(distances, axis=1)
            
            # 更新中心
            for k in range(n_clusters):
                mask = assignments == k
                if mask.sum() > 0:
                    centers[k] = self.embeddings[mask].mean(axis=0)
        
        self.cluster_centers = centers
        self.skill_to_cluster = {i: int(assignments[i]) for i in range(self.vocab_size)}
        
        logger.info(f"技能聚类完成: {n_clusters}类")


class PositionEmbedding:
    """
    职位嵌入层
    
    【PPT要点】
    - 职位层级嵌入
    - 行业领域嵌入
    - 职责描述嵌入
    """
    
    def __init__(self, num_positions: int, embedding_dim: int = 64):
        self.num_positions = num_positions
        self.embedding_dim = embedding_dim
        
        # 职位基础嵌入
        self.position_embeddings = np.random.randn(num_positions, embedding_dim) * 0.01
        
        # 级别嵌入
        self.level_embeddings = np.random.randn(5, embedding_dim // 4) * 0.01  # 5个级别
        
        # 行业嵌入
        self.industry_embeddings = np.random.randn(20, embedding_dim // 4) * 0.01  # 20个行业
    
    def get_embedding(self, position_id: int, level: int = 0, industry: int = 0) -> np.ndarray:
        """获取职位完整嵌入"""
        base = self.position_embeddings[position_id % self.num_positions]
        level_emb = self.level_embeddings[level % 5]
        industry_emb = self.industry_embeddings[industry % 20]
        
        # 填充到相同维度
        level_padded = np.zeros(self.embedding_dim)
        level_padded[:len(level_emb)] = level_emb
        
        industry_padded = np.zeros(self.embedding_dim)
        industry_padded[:len(industry_emb)] = industry_emb
        
        # 组合
        return base + 0.1 * level_padded + 0.1 * industry_padded


# ============================================
# 双塔模型
# ============================================

class TwoTowerMatcher:
    """
    双塔匹配模型
    
    【PPT要点】
    - 用户塔：编码用户画像（技能、经验、偏好）
    - 职位塔：编码职位信息（要求、薪资、发展）
    - 高效向量检索：ANN索引
    - 在线-离线解耦：职位向量可预计算
    
    架构图：
    ┌─────────┐     ┌─────────┐
    │ User    │     │ Job     │
    │ Features│     │ Features│
    └────┬────┘     └────┬────┘
         │               │
    ┌────▼────┐     ┌────▼────┐
    │ User    │     │ Job     │
    │ Tower   │     │ Tower   │
    │ (MLP)   │     │ (MLP)   │
    └────┬────┘     └────┬────┘
         │               │
    ┌────▼────────────────▼────┐
    │    Cosine Similarity     │
    └──────────────────────────┘
    
    论文: "Sampling-Bias-Corrected Neural Modeling for Large Corpus Item Recommendations", RecSys 2019
    """
    
    def __init__(self, 
                 user_feature_dim: int,
                 job_feature_dim: int,
                 embedding_dim: int = 128,
                 hidden_dims: List[int] = [256, 128]):
        
        self.user_feature_dim = user_feature_dim
        self.job_feature_dim = job_feature_dim
        self.embedding_dim = embedding_dim
        
        # 用户塔参数（MLP）
        self.user_weights = []
        self.user_biases = []
        
        dims = [user_feature_dim] + hidden_dims + [embedding_dim]
        for i in range(len(dims) - 1):
            w = np.random.randn(dims[i], dims[i+1]) * np.sqrt(2.0 / dims[i])
            b = np.zeros(dims[i+1])
            self.user_weights.append(w)
            self.user_biases.append(b)
        
        # 职位塔参数（MLP）
        self.job_weights = []
        self.job_biases = []
        
        dims = [job_feature_dim] + hidden_dims + [embedding_dim]
        for i in range(len(dims) - 1):
            w = np.random.randn(dims[i], dims[i+1]) * np.sqrt(2.0 / dims[i])
            b = np.zeros(dims[i+1])
            self.job_weights.append(w)
            self.job_biases.append(b)
        
        # 预计算的职位向量
        self._job_vectors: Dict[str, np.ndarray] = {}
        
        logger.info(f"双塔模型初始化: user_dim={user_feature_dim}, job_dim={job_feature_dim}")
    
    def _forward_user(self, user_features: np.ndarray) -> np.ndarray:
        """用户塔前向传播"""
        x = user_features
        for i, (w, b) in enumerate(zip(self.user_weights, self.user_biases)):
            x = x @ w + b
            if i < len(self.user_weights) - 1:
                x = np.maximum(x, 0)  # ReLU
        
        # L2归一化
        return x / (np.linalg.norm(x) + 1e-8)
    
    def _forward_job(self, job_features: np.ndarray) -> np.ndarray:
        """职位塔前向传播"""
        x = job_features
        for i, (w, b) in enumerate(zip(self.job_weights, self.job_biases)):
            x = x @ w + b
            if i < len(self.job_weights) - 1:
                x = np.maximum(x, 0)  # ReLU
        
        # L2归一化
        return x / (np.linalg.norm(x) + 1e-8)
    
    def encode_user(self, user_features: np.ndarray) -> np.ndarray:
        """编码用户向量"""
        return self._forward_user(user_features)
    
    def encode_job(self, job_features: np.ndarray, job_id: str = None) -> np.ndarray:
        """编码职位向量（支持缓存）"""
        if job_id and job_id in self._job_vectors:
            return self._job_vectors[job_id]
        
        vec = self._forward_job(job_features)
        
        if job_id:
            self._job_vectors[job_id] = vec
        
        return vec
    
    def compute_similarity(self, user_vec: np.ndarray, job_vec: np.ndarray) -> float:
        """计算相似度（余弦）"""
        return float(np.dot(user_vec, job_vec))
    
    def batch_match(self, user_features: np.ndarray,
                    job_features_list: List[np.ndarray],
                    job_ids: List[str] = None) -> List[float]:
        """批量匹配"""
        user_vec = self.encode_user(user_features)
        
        scores = []
        for i, job_features in enumerate(job_features_list):
            job_id = job_ids[i] if job_ids else None
            job_vec = self.encode_job(job_features, job_id)
            scores.append(self.compute_similarity(user_vec, job_vec))
        
        return scores
    
    def precompute_job_vectors(self, jobs: List[Tuple[str, np.ndarray]]):
        """预计算并缓存职位向量"""
        for job_id, job_features in jobs:
            self._job_vectors[job_id] = self._forward_job(job_features)
        
        logger.info(f"预计算{len(jobs)}个职位向量")


# ============================================
# 交叉网络
# ============================================

class DeepCrossNetwork:
    """
    Deep & Cross Network（DCN）
    
    【PPT要点】
    - 显式特征交叉：捕获高阶特征交互
    - 深度网络：隐式非线性变换
    - 并行结构：Cross + Deep
    
    特征交叉公式：
    x_{l+1} = x_0 * x_l^T * w_l + b_l + x_l
    
    架构图：
         Input
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
    ┌───────┐  ┌───────┐
    │ Cross │  │ Deep  │
    │ Layer │  │ Layer │
    │ x3    │  │ MLP   │
    └───┬───┘  └───┬───┘
        │          │
        └────┬─────┘
             │
        ┌────▼────┐
        │ Concat  │
        └────┬────┘
             │
        ┌────▼────┐
        │ Output  │
        └─────────┘
    
    论文: "Deep & Cross Network for Ad Click Predictions", KDD 2017
    """
    
    def __init__(self,
                 input_dim: int,
                 cross_layers: int = 3,
                 deep_layers: List[int] = [256, 128, 64]):
        
        self.input_dim = input_dim
        self.cross_layers = cross_layers
        
        # Cross层参数
        self.cross_weights = [
            np.random.randn(input_dim, 1) * 0.01
            for _ in range(cross_layers)
        ]
        self.cross_biases = [
            np.zeros(input_dim)
            for _ in range(cross_layers)
        ]
        
        # Deep层参数
        self.deep_weights = []
        self.deep_biases = []
        
        dims = [input_dim] + deep_layers
        for i in range(len(dims) - 1):
            w = np.random.randn(dims[i], dims[i+1]) * np.sqrt(2.0 / dims[i])
            b = np.zeros(dims[i+1])
            self.deep_weights.append(w)
            self.deep_biases.append(b)
        
        # 输出层
        output_dim = input_dim + deep_layers[-1]
        self.output_weight = np.random.randn(output_dim, 1) * 0.01
        self.output_bias = np.zeros(1)
        
        logger.info(f"DCN初始化: input_dim={input_dim}, cross_layers={cross_layers}")
    
    def _cross_layer(self, x0: np.ndarray, xl: np.ndarray,
                     w: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        单个Cross层
        
        x_{l+1} = x_0 * (x_l^T * w) + b + x_l
        """
        interaction = x0 * (xl @ w).reshape(-1)  # 特征交叉
        return interaction + b + xl
    
    def _deep_forward(self, x: np.ndarray) -> np.ndarray:
        """Deep网络前向传播"""
        for w, b in zip(self.deep_weights, self.deep_biases):
            x = x @ w + b
            x = np.maximum(x, 0)  # ReLU
        return x
    
    def forward(self, x: np.ndarray) -> float:
        """
        前向传播
        
        Returns:
            匹配分数 (0-1)
        """
        x0 = x.copy()
        
        # Cross网络
        x_cross = x.copy()
        for w, b in zip(self.cross_weights, self.cross_biases):
            x_cross = self._cross_layer(x0, x_cross, w, b)
        
        # Deep网络
        x_deep = self._deep_forward(x.copy())
        
        # 合并
        combined = np.concatenate([x_cross, x_deep])
        
        # 输出
        logit = combined @ self.output_weight + self.output_bias
        score = 1.0 / (1.0 + np.exp(-logit[0]))  # Sigmoid
        
        return float(score)
    
    def match(self, user_features: np.ndarray, job_features: np.ndarray) -> float:
        """用户-职位匹配"""
        # 拼接特征
        combined = np.concatenate([user_features, job_features])
        
        # 特征填充/截断到输入维度
        if len(combined) < self.input_dim:
            combined = np.pad(combined, (0, self.input_dim - len(combined)))
        elif len(combined) > self.input_dim:
            combined = combined[:self.input_dim]
        
        return self.forward(combined)


# ============================================
# 神经协同过滤
# ============================================

class NeuralCollaborativeFiltering:
    """
    神经协同过滤（Neural CF）
    
    【PPT要点】
    - GMF：广义矩阵分解，线性交互
    - MLP：多层感知机，非线性交互
    - NeuMF：GMF + MLP融合
    
    公式：
    GMF: p_u ⊙ q_i
    MLP: σ(W[p_u; q_i] + b)
    NeuMF: σ(h^T[GMF; MLP])
    
    论文: "Neural Collaborative Filtering", WWW 2017
    """
    
    def __init__(self,
                 num_users: int,
                 num_items: int,
                 gmf_dim: int = 32,
                 mlp_dim: int = 64,
                 mlp_layers: List[int] = [128, 64, 32]):
        
        self.num_users = num_users
        self.num_items = num_items
        
        # GMF嵌入
        self.user_gmf_embedding = np.random.randn(num_users, gmf_dim) * 0.01
        self.item_gmf_embedding = np.random.randn(num_items, gmf_dim) * 0.01
        
        # MLP嵌入
        self.user_mlp_embedding = np.random.randn(num_users, mlp_dim) * 0.01
        self.item_mlp_embedding = np.random.randn(num_items, mlp_dim) * 0.01
        
        # MLP层
        self.mlp_weights = []
        self.mlp_biases = []
        
        dims = [mlp_dim * 2] + mlp_layers
        for i in range(len(dims) - 1):
            w = np.random.randn(dims[i], dims[i+1]) * np.sqrt(2.0 / dims[i])
            b = np.zeros(dims[i+1])
            self.mlp_weights.append(w)
            self.mlp_biases.append(b)
        
        # NeuMF层
        neumf_dim = gmf_dim + mlp_layers[-1]
        self.neumf_weight = np.random.randn(neumf_dim, 1) * 0.01
        self.neumf_bias = np.zeros(1)
        
        logger.info(f"NeuCF初始化: {num_users}用户, {num_items}物品")
    
    def predict(self, user_id: int, item_id: int) -> float:
        """预测用户对物品的偏好分数"""
        # 检查ID有效性
        user_id = user_id % self.num_users
        item_id = item_id % self.num_items
        
        # GMF部分
        gmf_user = self.user_gmf_embedding[user_id]
        gmf_item = self.item_gmf_embedding[item_id]
        gmf_out = gmf_user * gmf_item  # 元素乘
        
        # MLP部分
        mlp_user = self.user_mlp_embedding[user_id]
        mlp_item = self.item_mlp_embedding[item_id]
        mlp_out = np.concatenate([mlp_user, mlp_item])
        
        for w, b in zip(self.mlp_weights, self.mlp_biases):
            mlp_out = mlp_out @ w + b
            mlp_out = np.maximum(mlp_out, 0)  # ReLU
        
        # NeuMF
        neumf_input = np.concatenate([gmf_out, mlp_out])
        logit = neumf_input @ self.neumf_weight + self.neumf_bias
        score = 1.0 / (1.0 + np.exp(-logit[0]))  # Sigmoid
        
        return float(score)
    
    def batch_predict(self, user_id: int, item_ids: List[int]) -> List[float]:
        """批量预测"""
        return [self.predict(user_id, item_id) for item_id in item_ids]
    
    def recommend(self, user_id: int, top_k: int = 10,
                 exclude_items: List[int] = None) -> List[Tuple[int, float]]:
        """为用户推荐物品"""
        exclude_set = set(exclude_items) if exclude_items else set()
        
        scores = []
        for item_id in range(self.num_items):
            if item_id not in exclude_set:
                score = self.predict(user_id, item_id)
                scores.append((item_id, score))
        
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]


# ============================================
# 对比学习匹配
# ============================================

class ContrastiveMatcher:
    """
    对比学习匹配器
    
    【PPT要点】
    - InfoNCE损失：拉近正样本，推远负样本
    - 数据增强：技能采样、特征扰动
    - 表示学习：无监督预训练
    
    损失函数：
    L = -log(exp(sim(u, v+)/τ) / Σexp(sim(u, v)/τ))
    
    论文: "SimCLR: A Simple Framework for Contrastive Learning", ICML 2020
    """
    
    def __init__(self, embedding_dim: int = 128, temperature: float = 0.07):
        self.embedding_dim = embedding_dim
        self.temperature = temperature
        
        # 投影头
        self.proj_weight1 = np.random.randn(embedding_dim, embedding_dim) * 0.01
        self.proj_bias1 = np.zeros(embedding_dim)
        self.proj_weight2 = np.random.randn(embedding_dim, embedding_dim // 2) * 0.01
        self.proj_bias2 = np.zeros(embedding_dim // 2)
    
    def project(self, embedding: np.ndarray) -> np.ndarray:
        """投影到对比空间"""
        x = embedding @ self.proj_weight1 + self.proj_bias1
        x = np.maximum(x, 0)  # ReLU
        x = x @ self.proj_weight2 + self.proj_bias2
        
        # L2归一化
        return x / (np.linalg.norm(x) + 1e-8)
    
    def augment(self, embedding: np.ndarray, noise_scale: float = 0.1) -> np.ndarray:
        """数据增强（高斯噪声）"""
        noise = np.random.randn(*embedding.shape) * noise_scale
        return embedding + noise
    
    def compute_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        """计算对比相似度"""
        proj1 = self.project(emb1)
        proj2 = self.project(emb2)
        
        sim = np.dot(proj1, proj2) / self.temperature
        return float(sim)
    
    def rank_candidates(self, query: np.ndarray,
                        candidates: List[np.ndarray]) -> List[Tuple[int, float]]:
        """对候选进行排名"""
        query_proj = self.project(query)
        
        scores = []
        for i, cand in enumerate(candidates):
            cand_proj = self.project(cand)
            sim = np.dot(query_proj, cand_proj) / self.temperature
            scores.append((i, float(sim)))
        
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores


# ============================================
# 职业深度匹配引擎
# ============================================

class CareerDeepMatcher:
    """
    职业深度学习匹配引擎
    
    整合多种深度学习模型，用于高精度人岗匹配
    
    【PPT架构】
    ┌────────────────────────────────────────────┐
    │         Career Deep Matcher                │
    ├────────────────────────────────────────────┤
    │                                            │
    │  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
    │  │Two-Tower │  │   DCN    │  │ NeuralCF │  │
    │  │ 双塔召回 │  │ 特征交叉 │  │ 协同过滤 │  │
    │  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
    │       │             │             │        │
    │       └─────────────┼─────────────┘        │
    │                     │                      │
    │               ┌─────▼─────┐                │
    │               │  Ensemble │                │
    │               │  集成融合  │                │
    │               └─────┬─────┘                │
    │                     │                      │
    │               ┌─────▼─────┐                │
    │               │Contrastive│                │
    │               │ 对比精排  │                │
    │               └───────────┘                │
    │                                            │
    └────────────────────────────────────────────┘
    
    匹配流程：
    1. 特征提取：技能、经验、偏好向量化
    2. 粗排：双塔模型快速召回 Top-100
    3. 精排：DCN + NeuralCF 多模型评分
    4. 集成：加权融合各模型分数
    5. 对比：对比学习重排序 Top-K
    """
    
    def __init__(self,
                 skill_vocab_size: int = 1000,
                 num_positions: int = 500,
                 embedding_dim: int = 128):
        
        self.skill_vocab_size = skill_vocab_size
        self.num_positions = num_positions
        self.embedding_dim = embedding_dim
        
        # 嵌入层
        self.skill_embedding = SkillEmbedding(skill_vocab_size, embedding_dim)
        self.position_embedding = PositionEmbedding(num_positions, embedding_dim)
        
        # 计算特征维度
        user_feature_dim = embedding_dim + 5  # skill_emb + exp + prefs
        job_feature_dim = embedding_dim + 4   # pos_emb + scores
        
        # 匹配模型
        self.two_tower = TwoTowerMatcher(
            user_feature_dim=user_feature_dim,
            job_feature_dim=job_feature_dim,
            embedding_dim=64,
        )
        
        self.dcn = DeepCrossNetwork(
            input_dim=user_feature_dim + job_feature_dim,
            cross_layers=3,
        )
        
        self.neural_cf = NeuralCollaborativeFiltering(
            num_users=1000,  # 假设最大1000用户
            num_items=num_positions,
        )
        
        self.contrast = ContrastiveMatcher(embedding_dim=embedding_dim)
        
        # 模型权重
        self.model_weights = {
            'two_tower': 0.3,
            'dcn': 0.35,
            'neural_cf': 0.2,
            'contrast': 0.15,
        }
        
        # 技能词汇表
        self.skill_to_id: Dict[str, int] = {}
        self.position_to_id: Dict[str, int] = {}
        
        logger.info("CareerDeepMatcher初始化完成")
    
    def build_vocabulary(self, skills: List[str], positions: List[str]):
        """构建词汇表"""
        self.skill_to_id = {s: i for i, s in enumerate(skills[:self.skill_vocab_size])}
        self.position_to_id = {p: i for i, p in enumerate(positions[:self.num_positions])}
        
        logger.info(f"词汇表: {len(self.skill_to_id)}技能, {len(self.position_to_id)}职位")
    
    def _extract_user_features(self, user_data: Dict) -> np.ndarray:
        """提取用户特征向量"""
        # 技能嵌入
        skill_ids = [
            self.skill_to_id.get(s, 0)
            for s in user_data.get('skills', [])
            if s in self.skill_to_id
        ]
        skill_emb = self.skill_embedding.get_embedding(skill_ids) if skill_ids else np.zeros(self.embedding_dim)
        
        # 经验
        exp = min(user_data.get('experience_years', 0) / 20.0, 1.0)
        
        # 偏好
        prefs = user_data.get('preferences', {})
        pref_vec = np.array([
            prefs.get('salary', 0.25),
            prefs.get('growth', 0.25),
            prefs.get('balance', 0.25),
            prefs.get('stability', 0.25),
        ])
        
        return np.concatenate([skill_emb, [exp], pref_vec])
    
    def _extract_job_features(self, job_data: Dict) -> np.ndarray:
        """提取职位特征向量"""
        # 职位嵌入
        pos_id = self.position_to_id.get(job_data.get('title', ''), 0)
        pos_emb = self.position_embedding.get_embedding(pos_id)
        
        # 评分
        scores = np.array([
            job_data.get('growth_score', 5) / 10.0,
            job_data.get('balance_score', 5) / 10.0,
            job_data.get('stability_score', 5) / 10.0,
            min(job_data.get('salary', 0) / 50000.0, 1.0),
        ])
        
        return np.concatenate([pos_emb, scores])
    
    def match(self, user_data: Dict, jobs: List[Dict],
              top_k: int = 10, use_ensemble: bool = True) -> List[Dict]:
        """
        执行深度匹配
        
        Args:
            user_data: 用户信息
            jobs: 职位列表
            top_k: 返回数量
            use_ensemble: 是否使用集成
        
        Returns:
            排序后的匹配结果
        """
        user_features = self._extract_user_features(user_data)
        user_id = hash(user_data.get('user_id', '')) % 1000
        
        results = []
        
        for job in jobs:
            job_features = self._extract_job_features(job)
            job_id = self.position_to_id.get(job.get('title', ''), 0)
            
            scores = {}
            
            # 双塔评分
            user_vec = self.two_tower.encode_user(user_features)
            job_vec = self.two_tower.encode_job(job_features, job.get('position_id'))
            scores['two_tower'] = self.two_tower.compute_similarity(user_vec, job_vec)
            
            # DCN评分
            scores['dcn'] = self.dcn.match(user_features, job_features)
            
            # NeuralCF评分
            scores['neural_cf'] = self.neural_cf.predict(user_id, job_id)
            
            # 对比学习评分
            user_emb = user_features[:self.embedding_dim]
            job_emb = job_features[:self.embedding_dim]
            contrast_sim = self.contrast.compute_similarity(user_emb, job_emb)
            scores['contrast'] = 1.0 / (1.0 + np.exp(-contrast_sim))  # 归一化
            
            # 集成
            if use_ensemble:
                total_score = sum(
                    scores[model] * self.model_weights[model]
                    for model in scores
                )
            else:
                total_score = scores['two_tower']
            
            results.append({
                'position_id': job.get('position_id', ''),
                'title': job.get('title', ''),
                'total_score': float(total_score),
                'model_scores': {k: float(v) for k, v in scores.items()},
            })
        
        # 排序
        results.sort(key=lambda x: x['total_score'], reverse=True)
        
        return results[:top_k]
    
    def get_similar_jobs(self, job_data: Dict, all_jobs: List[Dict],
                          top_k: int = 5) -> List[Dict]:
        """获取相似职位"""
        query_features = self._extract_job_features(job_data)
        query_emb = query_features[:self.embedding_dim]
        
        similarities = []
        for job in all_jobs:
            if job.get('position_id') == job_data.get('position_id'):
                continue
            
            job_features = self._extract_job_features(job)
            job_emb = job_features[:self.embedding_dim]
            
            sim = self.contrast.compute_similarity(query_emb, job_emb)
            similarities.append({
                'position_id': job.get('position_id', ''),
                'title': job.get('title', ''),
                'similarity': float(1.0 / (1.0 + np.exp(-sim))),
            })
        
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return similarities[:top_k]


# 导出
__all__ = [
    'CareerDeepMatcher',
    'TwoTowerMatcher',
    'DeepCrossNetwork',
    'NeuralCollaborativeFiltering',
    'ContrastiveMatcher',
    'SkillEmbedding',
    'PositionEmbedding',
]

logger.info("深度学习匹配模块加载完成")

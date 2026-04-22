# ============================================
# 注意力机制模块（Attention Mechanisms）
# 
# 技术栈：
#   - Self-Attention：自注意力机制
#   - Multi-Head Attention：多头注意力
#   - Cross-Attention：交叉注意力
#   - Scaled Dot-Product Attention：缩放点积注意力
#   - Additive Attention (Bahdanau)：加性注意力
#   - Graph Attention (GAT)：图注意力网络
#   - Transformer Encoder：完整Transformer编码器
#
# 应用场景：
#   - 技能权重自动学习
#   - 岗位-学生对齐注意力
#   - 职业路径关键节点识别
#   - 多维度特征融合
# ============================================
import logging
import math
import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# 尝试导入PyTorch
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    PYTORCH_AVAILABLE = True
except ImportError:
    PYTORCH_AVAILABLE = False
    logger.info("PyTorch未安装，深度注意力功能受限")


@dataclass
class AttentionOutput:
    """注意力输出"""
    output: np.ndarray
    attention_weights: np.ndarray
    key_positions: List[int]  # 高注意力位置
    explanation: str


class ScaledDotProductAttention:
    """
    缩放点积注意力
    
    Attention(Q, K, V) = softmax(QK^T / √d_k) V
    
    论文: Vaswani et al., "Attention Is All You Need", 2017
    """
    
    def __init__(self, temperature: float = None):
        """
        Args:
            temperature: 温度参数（默认为√d_k）
        """
        self.temperature = temperature
    
    def __call__(self, 
                 query: np.ndarray, 
                 key: np.ndarray, 
                 value: np.ndarray,
                 mask: np.ndarray = None) -> AttentionOutput:
        """
        计算注意力
        
        Args:
            query: [seq_len, d_k] 或 [batch, seq_len, d_k]
            key: [seq_len, d_k]
            value: [seq_len, d_v]
            mask: [seq_len] 布尔掩码
        
        Returns:
            AttentionOutput
        """
        d_k = query.shape[-1]
        temperature = self.temperature or math.sqrt(d_k)
        
        # QK^T / √d_k
        scores = np.matmul(query, key.T) / temperature
        
        # 应用掩码
        if mask is not None:
            scores = np.where(mask, scores, -1e9)
        
        # Softmax
        attention_weights = self._softmax(scores)
        
        # 加权求和
        output = np.matmul(attention_weights, value)
        
        # 找出高注意力位置
        key_positions = list(np.argsort(attention_weights.mean(axis=0))[-3:][::-1])
        
        return AttentionOutput(
            output=output,
            attention_weights=attention_weights,
            key_positions=key_positions,
            explanation=f"Scaled Dot-Product Attention, d_k={d_k}",
        )
    
    def _softmax(self, x: np.ndarray) -> np.ndarray:
        """数值稳定的softmax"""
        exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=-1, keepdims=True)


class AdditiveAttention:
    """
    加性注意力（Bahdanau Attention）
    
    score(h_i, s_j) = v^T tanh(W_1 h_i + W_2 s_j)
    
    论文: Bahdanau et al., "Neural Machine Translation by Jointly Learning to Align and Translate", 2014
    """
    
    def __init__(self, query_dim: int, key_dim: int, hidden_dim: int = 64):
        self.query_dim = query_dim
        self.key_dim = key_dim
        self.hidden_dim = hidden_dim
        
        # 初始化权重
        self.W_q = np.random.randn(query_dim, hidden_dim) * 0.1
        self.W_k = np.random.randn(key_dim, hidden_dim) * 0.1
        self.v = np.random.randn(hidden_dim) * 0.1
    
    def __call__(self, 
                 query: np.ndarray,
                 keys: np.ndarray,
                 values: np.ndarray) -> AttentionOutput:
        """
        Args:
            query: [query_dim] 单个查询
            keys: [n, key_dim] 键序列
            values: [n, value_dim] 值序列
        """
        # 计算注意力分数
        scores = np.zeros(len(keys))
        
        query_proj = np.dot(query, self.W_q)  # [hidden_dim]
        
        for i, key in enumerate(keys):
            key_proj = np.dot(key, self.W_k)  # [hidden_dim]
            combined = np.tanh(query_proj + key_proj)
            scores[i] = np.dot(self.v, combined)
        
        # Softmax
        attention_weights = np.exp(scores - np.max(scores))
        attention_weights /= attention_weights.sum()
        
        # 加权求和
        output = np.zeros(values.shape[1])
        for i, (weight, value) in enumerate(zip(attention_weights, values)):
            output += weight * value
        
        key_positions = list(np.argsort(attention_weights)[-3:][::-1])
        
        return AttentionOutput(
            output=output,
            attention_weights=attention_weights,
            key_positions=key_positions,
            explanation="Additive (Bahdanau) Attention",
        )


class MultiHeadAttention:
    """
    多头注意力
    
    MultiHead(Q, K, V) = Concat(head_1, ..., head_h) W^O
    head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)
    
    多个注意力头可以关注不同的表示子空间
    """
    
    def __init__(self, d_model: int, num_heads: int = 8):
        assert d_model % num_heads == 0, "d_model必须能被num_heads整除"
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # 投影矩阵
        scale = 1.0 / math.sqrt(d_model)
        self.W_q = np.random.randn(d_model, d_model) * scale
        self.W_k = np.random.randn(d_model, d_model) * scale
        self.W_v = np.random.randn(d_model, d_model) * scale
        self.W_o = np.random.randn(d_model, d_model) * scale
        
        self._attention = ScaledDotProductAttention()
    
    def __call__(self,
                 query: np.ndarray,
                 key: np.ndarray,
                 value: np.ndarray,
                 mask: np.ndarray = None) -> AttentionOutput:
        """
        Args:
            query: [seq_q, d_model]
            key: [seq_k, d_model]
            value: [seq_k, d_model]
        """
        seq_q = query.shape[0]
        seq_k = key.shape[0]
        
        # 线性投影
        Q = np.dot(query, self.W_q)  # [seq_q, d_model]
        K = np.dot(key, self.W_k)
        V = np.dot(value, self.W_v)
        
        # 分割成多头
        Q = Q.reshape(seq_q, self.num_heads, self.d_k).transpose(1, 0, 2)
        K = K.reshape(seq_k, self.num_heads, self.d_k).transpose(1, 0, 2)
        V = V.reshape(seq_k, self.num_heads, self.d_k).transpose(1, 0, 2)
        
        # 每个头独立计算注意力
        heads = []
        all_weights = []
        
        for h in range(self.num_heads):
            result = self._attention(Q[h], K[h], V[h], mask)
            heads.append(result.output)
            all_weights.append(result.attention_weights)
        
        # 拼接并投影
        concat = np.concatenate(heads, axis=-1)  # [seq_q, d_model]
        output = np.dot(concat, self.W_o)
        
        # 平均注意力权重
        avg_weights = np.mean(all_weights, axis=0)
        key_positions = list(np.argsort(avg_weights.mean(axis=0))[-3:][::-1])
        
        return AttentionOutput(
            output=output,
            attention_weights=np.array(all_weights),  # [num_heads, seq_q, seq_k]
            key_positions=key_positions,
            explanation=f"Multi-Head Attention, {self.num_heads} heads",
        )


class CrossAttention:
    """
    交叉注意力
    
    用于对齐两个不同序列（如学生技能和岗位要求）
    """
    
    def __init__(self, query_dim: int, key_dim: int, hidden_dim: int = 128):
        self.query_dim = query_dim
        self.key_dim = key_dim
        self.hidden_dim = hidden_dim
        
        # 投影到统一空间
        scale = 1.0 / math.sqrt(hidden_dim)
        self.W_q = np.random.randn(query_dim, hidden_dim) * scale
        self.W_k = np.random.randn(key_dim, hidden_dim) * scale
        self.W_v = np.random.randn(key_dim, hidden_dim) * scale
    
    def __call__(self,
                 query: np.ndarray,
                 key_value: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Args:
            query: [n_q, query_dim] 查询序列（如学生技能）
            key_value: [n_kv, key_dim] 键值序列（如岗位要求）
        
        Returns:
            aligned_output: [n_q, hidden_dim] 对齐后的表示
            attention_weights: [n_q, n_kv] 注意力权重矩阵
        """
        # 投影
        Q = np.dot(query, self.W_q)      # [n_q, hidden]
        K = np.dot(key_value, self.W_k)  # [n_kv, hidden]
        V = np.dot(key_value, self.W_v)  # [n_kv, hidden]
        
        # 注意力分数
        scores = np.dot(Q, K.T) / math.sqrt(self.hidden_dim)  # [n_q, n_kv]
        
        # Softmax
        attention_weights = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
        attention_weights /= attention_weights.sum(axis=-1, keepdims=True)
        
        # 加权求和
        aligned_output = np.dot(attention_weights, V)  # [n_q, hidden]
        
        return aligned_output, attention_weights


class SelfAttentionPooling:
    """
    自注意力池化
    
    将变长序列聚合为固定长度表示
    """
    
    def __init__(self, input_dim: int, hidden_dim: int = 64):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        
        self.W = np.random.randn(input_dim, hidden_dim) * 0.1
        self.u = np.random.randn(hidden_dim) * 0.1
    
    def __call__(self, sequence: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Args:
            sequence: [seq_len, input_dim]
        
        Returns:
            pooled: [input_dim] 池化后的向量
            weights: [seq_len] 每个位置的权重
        """
        # 计算注意力分数
        hidden = np.tanh(np.dot(sequence, self.W))  # [seq_len, hidden_dim]
        scores = np.dot(hidden, self.u)  # [seq_len]
        
        # Softmax
        weights = np.exp(scores - np.max(scores))
        weights /= weights.sum()
        
        # 加权平均
        pooled = np.dot(weights, sequence)  # [input_dim]
        
        return pooled, weights


class GraphAttentionLayer:
    """
    图注意力层（GAT）
    
    使用注意力机制聚合邻居节点信息
    
    论文: Veličković et al., "Graph Attention Networks", 2017
    """
    
    def __init__(self, in_dim: int, out_dim: int, num_heads: int = 4,
                 negative_slope: float = 0.2):
        self.in_dim = in_dim
        self.out_dim = out_dim
        self.num_heads = num_heads
        self.negative_slope = negative_slope
        
        # 每个头的权重
        scale = 1.0 / math.sqrt(out_dim)
        self.W = np.random.randn(num_heads, in_dim, out_dim) * scale
        self.a = np.random.randn(num_heads, 2 * out_dim) * scale
    
    def __call__(self,
                 node_features: np.ndarray,
                 adjacency: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Args:
            node_features: [num_nodes, in_dim]
            adjacency: [num_nodes, num_nodes] 邻接矩阵
        
        Returns:
            output: [num_nodes, num_heads * out_dim]
            attention: [num_heads, num_nodes, num_nodes]
        """
        num_nodes = node_features.shape[0]
        
        # 线性变换
        h = np.stack([np.dot(node_features, self.W[k]) for k in range(self.num_heads)])
        # h: [num_heads, num_nodes, out_dim]
        
        # 计算注意力系数
        attention = np.zeros((self.num_heads, num_nodes, num_nodes))
        
        for head in range(self.num_heads):
            for i in range(num_nodes):
                for j in range(num_nodes):
                    if adjacency[i, j] > 0:
                        # 拼接节点特征
                        concat = np.concatenate([h[head, i], h[head, j]])
                        # 计算注意力分数
                        e = np.dot(self.a[head], concat)
                        attention[head, i, j] = self._leaky_relu(e)
        
        # Masked Softmax（只在邻居上做softmax）
        for head in range(self.num_heads):
            for i in range(num_nodes):
                mask = adjacency[i] > 0
                if mask.sum() > 0:
                    masked_attn = attention[head, i, mask]
                    exp_attn = np.exp(masked_attn - np.max(masked_attn))
                    attention[head, i, mask] = exp_attn / exp_attn.sum()
        
        # 聚合邻居特征
        output_heads = []
        for head in range(self.num_heads):
            head_output = np.zeros((num_nodes, self.out_dim))
            for i in range(num_nodes):
                for j in range(num_nodes):
                    if adjacency[i, j] > 0:
                        head_output[i] += attention[head, i, j] * h[head, j]
            output_heads.append(head_output)
        
        # 拼接所有头
        output = np.concatenate(output_heads, axis=-1)
        
        return output, attention
    
    def _leaky_relu(self, x: float) -> float:
        return x if x >= 0 else self.negative_slope * x


class PositionalEncoding:
    """
    位置编码
    
    PE(pos, 2i) = sin(pos / 10000^(2i/d))
    PE(pos, 2i+1) = cos(pos / 10000^(2i/d))
    """
    
    def __init__(self, d_model: int, max_len: int = 5000):
        self.d_model = d_model
        
        pe = np.zeros((max_len, d_model))
        position = np.arange(max_len)[:, np.newaxis]
        div_term = np.exp(np.arange(0, d_model, 2) * -(math.log(10000.0) / d_model))
        
        pe[:, 0::2] = np.sin(position * div_term)
        pe[:, 1::2] = np.cos(position * div_term)
        
        self.pe = pe
    
    def __call__(self, x: np.ndarray) -> np.ndarray:
        """添加位置编码"""
        seq_len = x.shape[0]
        return x + self.pe[:seq_len]


class FeedForward:
    """前馈网络"""
    
    def __init__(self, d_model: int, d_ff: int = 2048):
        scale = 1.0 / math.sqrt(d_model)
        self.W1 = np.random.randn(d_model, d_ff) * scale
        self.W2 = np.random.randn(d_ff, d_model) * scale
        self.b1 = np.zeros(d_ff)
        self.b2 = np.zeros(d_model)
    
    def __call__(self, x: np.ndarray) -> np.ndarray:
        h = np.maximum(0, np.dot(x, self.W1) + self.b1)  # ReLU
        return np.dot(h, self.W2) + self.b2


class LayerNorm:
    """层归一化"""
    
    def __init__(self, d_model: int, eps: float = 1e-6):
        self.gamma = np.ones(d_model)
        self.beta = np.zeros(d_model)
        self.eps = eps
    
    def __call__(self, x: np.ndarray) -> np.ndarray:
        mean = x.mean(axis=-1, keepdims=True)
        std = x.std(axis=-1, keepdims=True)
        return self.gamma * (x - mean) / (std + self.eps) + self.beta


class TransformerEncoderLayer:
    """
    Transformer编码器层
    
    包含：Multi-Head Attention + Feed Forward + Residual + LayerNorm
    """
    
    def __init__(self, d_model: int, num_heads: int = 8, d_ff: int = 2048,
                 dropout: float = 0.1):
        self.attention = MultiHeadAttention(d_model, num_heads)
        self.feed_forward = FeedForward(d_model, d_ff)
        self.norm1 = LayerNorm(d_model)
        self.norm2 = LayerNorm(d_model)
        self.dropout_rate = dropout
    
    def __call__(self, x: np.ndarray, mask: np.ndarray = None) -> np.ndarray:
        """
        Args:
            x: [seq_len, d_model]
            mask: [seq_len] 可选掩码
        """
        # Self-Attention + Residual + LayerNorm
        attn_output = self.attention(x, x, x, mask)
        x = self.norm1(x + attn_output.output)
        
        # Feed Forward + Residual + LayerNorm
        ff_output = self.feed_forward(x)
        x = self.norm2(x + ff_output)
        
        return x


class TransformerEncoder:
    """
    完整的Transformer编码器
    
    用于将序列编码为上下文相关的表示
    """
    
    def __init__(self, d_model: int = 256, num_heads: int = 8,
                 num_layers: int = 4, d_ff: int = 1024):
        self.d_model = d_model
        self.pos_encoding = PositionalEncoding(d_model)
        self.layers = [
            TransformerEncoderLayer(d_model, num_heads, d_ff)
            for _ in range(num_layers)
        ]
        self.norm = LayerNorm(d_model)
    
    def __call__(self, x: np.ndarray, mask: np.ndarray = None) -> np.ndarray:
        """
        Args:
            x: [seq_len, d_model]
        
        Returns:
            [seq_len, d_model] 编码后的序列
        """
        # 添加位置编码
        x = self.pos_encoding(x)
        
        # 通过所有层
        for layer in self.layers:
            x = layer(x, mask)
        
        return self.norm(x)


class SkillAttentionMatcher:
    """
    技能注意力匹配器
    
    使用注意力机制计算学生技能与岗位要求的匹配度
    """
    
    def __init__(self, skill_dim: int = 64, hidden_dim: int = 128):
        self.skill_dim = skill_dim
        self.hidden_dim = hidden_dim
        
        self.cross_attention = CrossAttention(skill_dim, skill_dim, hidden_dim)
        self.self_attention = MultiHeadAttention(hidden_dim, num_heads=4)
        self.pooling = SelfAttentionPooling(hidden_dim)
        
        # 技能嵌入查找表（简化）
        self.skill_embeddings: Dict[str, np.ndarray] = {}
    
    def register_skill(self, skill_name: str, embedding: np.ndarray = None):
        """注册技能嵌入"""
        if embedding is None:
            embedding = np.random.randn(self.skill_dim) * 0.1
        self.skill_embeddings[skill_name] = embedding
    
    def compute_match_score(self,
                            student_skills: List[str],
                            job_requirements: List[str]) -> Dict:
        """
        计算技能匹配分数
        
        Returns:
            Dict: 匹配分数、注意力权重、关键技能等
        """
        # 获取嵌入
        student_embs = self._get_embeddings(student_skills)
        job_embs = self._get_embeddings(job_requirements)
        
        if student_embs.shape[0] == 0 or job_embs.shape[0] == 0:
            return {
                'score': 0.0,
                'matched_skills': [],
                'missing_skills': job_requirements,
                'attention_weights': None,
            }
        
        # 交叉注意力：学生技能关注岗位要求
        aligned, attention_weights = self.cross_attention(student_embs, job_embs)
        
        # 自注意力：技能间交互
        if aligned.shape[0] > 1:
            aligned = self.self_attention(aligned, aligned, aligned).output
        
        # 池化得到整体表示
        pooled, skill_weights = self.pooling(aligned)
        
        # 计算匹配分数
        score = np.tanh(np.linalg.norm(pooled)) * 100
        
        # 分析匹配情况
        matched_skills = []
        missing_skills = []
        
        for j, req in enumerate(job_requirements):
            max_attention = attention_weights[:, j].max()
            if max_attention > 0.3:
                best_match_idx = np.argmax(attention_weights[:, j])
                matched_skills.append({
                    'requirement': req,
                    'matched_by': student_skills[best_match_idx],
                    'confidence': float(max_attention),
                })
            else:
                missing_skills.append(req)
        
        # 关键学生技能
        key_skills = []
        for i, skill in enumerate(student_skills):
            importance = skill_weights[i]
            key_skills.append({
                'skill': skill,
                'importance': float(importance),
            })
        key_skills.sort(key=lambda x: x['importance'], reverse=True)
        
        return {
            'score': float(score),
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'key_student_skills': key_skills[:5],
            'attention_weights': attention_weights.tolist(),
        }
    
    def _get_embeddings(self, skills: List[str]) -> np.ndarray:
        """获取技能嵌入矩阵"""
        embeddings = []
        for skill in skills:
            if skill in self.skill_embeddings:
                embeddings.append(self.skill_embeddings[skill])
            else:
                # 未知技能使用随机嵌入
                emb = np.random.randn(self.skill_dim) * 0.1
                self.skill_embeddings[skill] = emb
                embeddings.append(emb)
        
        if not embeddings:
            return np.array([]).reshape(0, self.skill_dim)
        
        return np.array(embeddings)


class CareerPathAttention:
    """
    职业路径注意力
    
    识别职业发展路径中的关键节点
    """
    
    def __init__(self, node_dim: int = 64):
        self.node_dim = node_dim
        self.gat = GraphAttentionLayer(node_dim, node_dim // 4, num_heads=4)
        self.node_embeddings: Dict[str, np.ndarray] = {}
    
    def register_position(self, position: str, features: np.ndarray = None):
        """注册职位节点"""
        if features is None:
            features = np.random.randn(self.node_dim) * 0.1
        self.node_embeddings[position] = features
    
    def analyze_path(self,
                     positions: List[str],
                     adjacency: np.ndarray) -> Dict:
        """
        分析职业路径的关键节点
        
        Args:
            positions: 职位列表
            adjacency: 邻接矩阵
        
        Returns:
            Dict: 节点重要性、关键转折点等
        """
        # 获取节点特征
        features = []
        for pos in positions:
            if pos in self.node_embeddings:
                features.append(self.node_embeddings[pos])
            else:
                features.append(np.random.randn(self.node_dim) * 0.1)
        
        features = np.array(features)
        
        # 图注意力
        output, attention = self.gat(features, adjacency)
        
        # 聚合注意力分数
        importance = attention.mean(axis=0).sum(axis=1)  # 接收到的注意力总和
        importance /= importance.max() + 1e-8
        
        # 识别关键节点
        key_nodes = []
        for i, (pos, imp) in enumerate(zip(positions, importance)):
            if imp > 0.5:
                key_nodes.append({
                    'position': pos,
                    'importance': float(imp),
                    'type': 'hub' if imp > 0.8 else 'milestone',
                })
        
        key_nodes.sort(key=lambda x: x['importance'], reverse=True)
        
        return {
            'node_importance': {pos: float(imp) for pos, imp in zip(positions, importance)},
            'key_nodes': key_nodes,
            'attention_matrix': attention.mean(axis=0).tolist(),
        }


logger.info("注意力机制模块加载完成")

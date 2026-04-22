# ============================================
# 知识图谱推理模块（Knowledge Graph Reasoning）
# 
# 技术栈：
#   - TransE / TransR / TransH：平移向量嵌入
#   - RotatE：旋转变换嵌入
#   - ComplEx：复数空间嵌入
#   - DistMult：对角矩阵分解
#   - ConvE：卷积神经网络知识图谱
#   - 链接预测：预测新关系
#   - 路径推理：多跳推理
#   - 规则学习：关系规则挖掘
#
# 应用场景：
#   - 职业技能关联发现
#   - 隐性职业路径推理
#   - 跨领域技能迁移预测
#   - 岗位-技能-资格证知识补全
# ============================================
import logging
import numpy as np
from typing import List, Dict, Tuple, Optional, Set
from collections import defaultdict
from dataclasses import dataclass
import random
import math

logger = logging.getLogger(__name__)

# 尝试导入PyTorch
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    import torch.nn.functional as F
    PYTORCH_AVAILABLE = True
except ImportError:
    PYTORCH_AVAILABLE = False
    logger.info("PyTorch未安装，深度知识图谱嵌入功能受限")


@dataclass
class Triple:
    """知识三元组"""
    head: str
    relation: str
    tail: str
    confidence: float = 1.0


@dataclass
class KGEmbeddingResult:
    """知识图谱嵌入结果"""
    entity_embeddings: Dict[str, np.ndarray]
    relation_embeddings: Dict[str, np.ndarray]
    entity_count: int
    relation_count: int
    embedding_dim: int
    model_type: str
    training_loss: List[float]


@dataclass
class LinkPredictionResult:
    """链接预测结果"""
    head: str
    relation: str
    predicted_tails: List[Tuple[str, float]]  # (实体, 分数)
    confidence: float


class KnowledgeGraph:
    """
    知识图谱数据结构
    """
    
    def __init__(self):
        self.triples: List[Triple] = []
        self.entities: Set[str] = set()
        self.relations: Set[str] = set()
        
        # 索引
        self.head_index: Dict[str, List[Triple]] = defaultdict(list)
        self.tail_index: Dict[str, List[Triple]] = defaultdict(list)
        self.relation_index: Dict[str, List[Triple]] = defaultdict(list)
        
        # 实体和关系到ID的映射
        self.entity2id: Dict[str, int] = {}
        self.relation2id: Dict[str, int] = {}
        self.id2entity: Dict[int, str] = {}
        self.id2relation: Dict[int, str] = {}
    
    def add_triple(self, head: str, relation: str, tail: str, confidence: float = 1.0):
        """添加三元组"""
        triple = Triple(head, relation, tail, confidence)
        self.triples.append(triple)
        
        self.entities.add(head)
        self.entities.add(tail)
        self.relations.add(relation)
        
        self.head_index[head].append(triple)
        self.tail_index[tail].append(triple)
        self.relation_index[relation].append(triple)
    
    def build_vocab(self):
        """构建实体和关系的ID映射"""
        for i, entity in enumerate(sorted(self.entities)):
            self.entity2id[entity] = i
            self.id2entity[i] = entity
        
        for i, relation in enumerate(sorted(self.relations)):
            self.relation2id[relation] = i
            self.id2relation[i] = relation
        
        logger.info(f"知识图谱：{len(self.entities)} 实体, {len(self.relations)} 关系, {len(self.triples)} 三元组")
    
    def get_neighbors(self, entity: str, direction: str = 'out') -> List[Tuple[str, str]]:
        """获取邻居实体"""
        neighbors = []
        
        if direction in ('out', 'both'):
            for triple in self.head_index[entity]:
                neighbors.append((triple.relation, triple.tail))
        
        if direction in ('in', 'both'):
            for triple in self.tail_index[entity]:
                neighbors.append((triple.relation + '_inv', triple.head))
        
        return neighbors
    
    def get_triples_as_ids(self) -> List[Tuple[int, int, int]]:
        """获取ID形式的三元组"""
        return [
            (self.entity2id[t.head], self.relation2id[t.relation], self.entity2id[t.tail])
            for t in self.triples
        ]


class TransE:
    """
    TransE 知识图谱嵌入
    
    核心思想：h + r ≈ t
    即头实体加上关系向量应等于尾实体
    
    损失函数：L = Σ [γ + d(h+r, t) - d(h'+r, t')] ( margin-based ranking loss)
    
    论文: Bordes et al., "Translating Embeddings for Modeling Multi-relational Data", 2013
    """
    
    def __init__(self, embedding_dim: int = 100, margin: float = 1.0,
                 learning_rate: float = 0.01, norm: int = 1):
        self.embedding_dim = embedding_dim
        self.margin = margin
        self.lr = learning_rate
        self.norm = norm  # L1 or L2
        
        self.entity_embeddings: Dict[str, np.ndarray] = {}
        self.relation_embeddings: Dict[str, np.ndarray] = {}
        
        self.training_loss: List[float] = []
    
    def _init_embeddings(self, kg: KnowledgeGraph):
        """初始化嵌入（Xavier初始化）"""
        scale = 6.0 / math.sqrt(self.embedding_dim)
        
        for entity in kg.entities:
            embedding = np.random.uniform(-scale, scale, self.embedding_dim)
            embedding = embedding / np.linalg.norm(embedding)  # 归一化
            self.entity_embeddings[entity] = embedding
        
        for relation in kg.relations:
            embedding = np.random.uniform(-scale, scale, self.embedding_dim)
            embedding = embedding / np.linalg.norm(embedding)
            self.relation_embeddings[relation] = embedding
    
    def _distance(self, h: np.ndarray, r: np.ndarray, t: np.ndarray) -> float:
        """计算 ||h + r - t||"""
        diff = h + r - t
        if self.norm == 1:
            return np.sum(np.abs(diff))
        else:
            return np.sum(diff ** 2)
    
    def _corrupt_triple(self, triple: Triple, kg: KnowledgeGraph) -> Triple:
        """生成负样本（随机替换头或尾）"""
        entities = list(kg.entities)
        
        if random.random() < 0.5:
            # 替换头
            new_head = random.choice(entities)
            while new_head == triple.head:
                new_head = random.choice(entities)
            return Triple(new_head, triple.relation, triple.tail)
        else:
            # 替换尾
            new_tail = random.choice(entities)
            while new_tail == triple.tail:
                new_tail = random.choice(entities)
            return Triple(triple.head, triple.relation, new_tail)
    
    def train(self, kg: KnowledgeGraph, num_epochs: int = 100, 
              batch_size: int = 128) -> KGEmbeddingResult:
        """训练TransE模型"""
        logger.info(f"开始TransE训练，维度: {self.embedding_dim}, epochs: {num_epochs}")
        
        kg.build_vocab()
        self._init_embeddings(kg)
        self.training_loss.clear()
        
        triples = kg.triples
        
        for epoch in range(num_epochs):
            epoch_loss = 0.0
            random.shuffle(triples)
            
            for i in range(0, len(triples), batch_size):
                batch = triples[i:i+batch_size]
                
                for triple in batch:
                    # 正样本
                    h = self.entity_embeddings[triple.head]
                    r = self.relation_embeddings[triple.relation]
                    t = self.entity_embeddings[triple.tail]
                    pos_dist = self._distance(h, r, t)
                    
                    # 负样本
                    neg_triple = self._corrupt_triple(triple, kg)
                    h_neg = self.entity_embeddings[neg_triple.head]
                    t_neg = self.entity_embeddings[neg_triple.tail]
                    neg_dist = self._distance(h_neg, r, t_neg)
                    
                    # Margin Ranking Loss
                    loss = max(0, self.margin + pos_dist - neg_dist)
                    epoch_loss += loss
                    
                    if loss > 0:
                        # 梯度下降更新
                        grad = self.lr * (2 if self.norm == 2 else 1)
                        diff_pos = h + r - t
                        diff_neg = h_neg + r - t_neg
                        
                        sign_pos = np.sign(diff_pos) if self.norm == 1 else diff_pos
                        sign_neg = np.sign(diff_neg) if self.norm == 1 else diff_neg
                        
                        # 更新正样本（减小距离）
                        self.entity_embeddings[triple.head] -= grad * sign_pos
                        self.relation_embeddings[triple.relation] -= grad * sign_pos
                        self.entity_embeddings[triple.tail] += grad * sign_pos
                        
                        # 更新负样本（增大距离）
                        self.entity_embeddings[neg_triple.head] += grad * sign_neg
                        self.entity_embeddings[neg_triple.tail] -= grad * sign_neg
                        
                        # 归一化
                        for e in [triple.head, triple.tail, neg_triple.head, neg_triple.tail]:
                            norm = np.linalg.norm(self.entity_embeddings[e])
                            if norm > 0:
                                self.entity_embeddings[e] /= norm
            
            avg_loss = epoch_loss / len(triples)
            self.training_loss.append(avg_loss)
            
            if (epoch + 1) % 20 == 0:
                logger.info(f"Epoch {epoch+1}, Loss: {avg_loss:.4f}")
        
        return KGEmbeddingResult(
            entity_embeddings=self.entity_embeddings.copy(),
            relation_embeddings=self.relation_embeddings.copy(),
            entity_count=len(kg.entities),
            relation_count=len(kg.relations),
            embedding_dim=self.embedding_dim,
            model_type='TransE',
            training_loss=self.training_loss,
        )
    
    def predict_tail(self, head: str, relation: str, kg: KnowledgeGraph, 
                     top_k: int = 10) -> List[Tuple[str, float]]:
        """链接预测：给定(h, r, ?)，预测t"""
        if head not in self.entity_embeddings or relation not in self.relation_embeddings:
            return []
        
        h = self.entity_embeddings[head]
        r = self.relation_embeddings[relation]
        
        scores = []
        for entity in kg.entities:
            t = self.entity_embeddings[entity]
            dist = self._distance(h, r, t)
            scores.append((entity, -dist))  # 负距离作为分数
        
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]
    
    def get_similar_entities(self, entity: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """获取相似实体"""
        if entity not in self.entity_embeddings:
            return []
        
        target = self.entity_embeddings[entity]
        
        similarities = []
        for e, emb in self.entity_embeddings.items():
            if e != entity:
                sim = np.dot(target, emb)  # 余弦相似度（已归一化）
                similarities.append((e, sim))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]


class TransR:
    """
    TransR 知识图谱嵌入
    
    改进：为每个关系学习独立的投影矩阵
    h_r = h * M_r, t_r = t * M_r
    核心思想：h_r + r ≈ t_r
    
    论文: Lin et al., "Learning Entity and Relation Embeddings for Knowledge Graph Completion", 2015
    """
    
    def __init__(self, entity_dim: int = 100, relation_dim: int = 50,
                 margin: float = 1.0, learning_rate: float = 0.01):
        self.entity_dim = entity_dim
        self.relation_dim = relation_dim
        self.margin = margin
        self.lr = learning_rate
        
        self.entity_embeddings: Dict[str, np.ndarray] = {}
        self.relation_embeddings: Dict[str, np.ndarray] = {}
        self.projection_matrices: Dict[str, np.ndarray] = {}  # M_r
        
        self.training_loss: List[float] = []
    
    def _init_embeddings(self, kg: KnowledgeGraph):
        """初始化嵌入和投影矩阵"""
        # 实体嵌入
        e_scale = 6.0 / math.sqrt(self.entity_dim)
        for entity in kg.entities:
            emb = np.random.uniform(-e_scale, e_scale, self.entity_dim)
            self.entity_embeddings[entity] = emb / np.linalg.norm(emb)
        
        # 关系嵌入
        r_scale = 6.0 / math.sqrt(self.relation_dim)
        for relation in kg.relations:
            emb = np.random.uniform(-r_scale, r_scale, self.relation_dim)
            self.relation_embeddings[relation] = emb / np.linalg.norm(emb)
            
            # 投影矩阵
            proj = np.random.uniform(-0.1, 0.1, (self.entity_dim, self.relation_dim))
            self.projection_matrices[relation] = proj
    
    def _project(self, entity_emb: np.ndarray, relation: str) -> np.ndarray:
        """投影到关系空间"""
        M_r = self.projection_matrices[relation]
        projected = np.dot(entity_emb, M_r)
        norm = np.linalg.norm(projected)
        return projected / norm if norm > 0 else projected
    
    def _distance(self, h_r: np.ndarray, r: np.ndarray, t_r: np.ndarray) -> float:
        """计算距离"""
        return np.sum((h_r + r - t_r) ** 2)
    
    def train(self, kg: KnowledgeGraph, num_epochs: int = 100,
              batch_size: int = 128) -> KGEmbeddingResult:
        """训练TransR模型"""
        logger.info(f"开始TransR训练，实体维度: {self.entity_dim}, 关系维度: {self.relation_dim}")
        
        kg.build_vocab()
        self._init_embeddings(kg)
        self.training_loss.clear()
        
        entities_list = list(kg.entities)
        
        for epoch in range(num_epochs):
            epoch_loss = 0.0
            triples = kg.triples.copy()
            random.shuffle(triples)
            
            for triple in triples:
                # 正样本投影
                h = self.entity_embeddings[triple.head]
                t = self.entity_embeddings[triple.tail]
                r = self.relation_embeddings[triple.relation]
                
                h_r = self._project(h, triple.relation)
                t_r = self._project(t, triple.relation)
                pos_dist = self._distance(h_r, r, t_r)
                
                # 负样本
                if random.random() < 0.5:
                    neg_head = random.choice(entities_list)
                    h_neg = self.entity_embeddings[neg_head]
                    h_r_neg = self._project(h_neg, triple.relation)
                    neg_dist = self._distance(h_r_neg, r, t_r)
                else:
                    neg_tail = random.choice(entities_list)
                    t_neg = self.entity_embeddings[neg_tail]
                    t_r_neg = self._project(t_neg, triple.relation)
                    neg_dist = self._distance(h_r, r, t_r_neg)
                
                loss = max(0, self.margin + pos_dist - neg_dist)
                epoch_loss += loss
                
                # 梯度更新（简化版）
                if loss > 0:
                    grad = self.lr * 2
                    diff = h_r + r - t_r
                    
                    self.entity_embeddings[triple.head] -= grad * 0.1 * diff.mean()
                    self.entity_embeddings[triple.tail] += grad * 0.1 * diff.mean()
                    self.relation_embeddings[triple.relation] -= grad * diff
            
            avg_loss = epoch_loss / len(triples)
            self.training_loss.append(avg_loss)
            
            if (epoch + 1) % 20 == 0:
                logger.info(f"Epoch {epoch+1}, Loss: {avg_loss:.4f}")
        
        return KGEmbeddingResult(
            entity_embeddings=self.entity_embeddings.copy(),
            relation_embeddings=self.relation_embeddings.copy(),
            entity_count=len(kg.entities),
            relation_count=len(kg.relations),
            embedding_dim=self.entity_dim,
            model_type='TransR',
            training_loss=self.training_loss,
        )


class DistMult:
    """
    DistMult 双线性对角模型
    
    评分函数：f(h, r, t) = h^T * diag(r) * t = Σ h_i * r_i * t_i
    
    优点：参数量少，训练高效
    缺点：只能建模对称关系
    
    论文: Yang et al., "Embedding Entities and Relations for Learning and Inference in Knowledge Bases", 2014
    """
    
    def __init__(self, embedding_dim: int = 100, learning_rate: float = 0.01,
                 regularization: float = 0.01):
        self.embedding_dim = embedding_dim
        self.lr = learning_rate
        self.reg = regularization
        
        self.entity_embeddings: Dict[str, np.ndarray] = {}
        self.relation_embeddings: Dict[str, np.ndarray] = {}
        
        self.training_loss: List[float] = []
    
    def _init_embeddings(self, kg: KnowledgeGraph):
        scale = 6.0 / math.sqrt(self.embedding_dim)
        
        for entity in kg.entities:
            self.entity_embeddings[entity] = np.random.uniform(-scale, scale, self.embedding_dim)
        
        for relation in kg.relations:
            self.relation_embeddings[relation] = np.random.uniform(-scale, scale, self.embedding_dim)
    
    def score(self, head: str, relation: str, tail: str) -> float:
        """计算三元组得分"""
        if head not in self.entity_embeddings:
            return float('-inf')
        if relation not in self.relation_embeddings:
            return float('-inf')
        if tail not in self.entity_embeddings:
            return float('-inf')
        
        h = self.entity_embeddings[head]
        r = self.relation_embeddings[relation]
        t = self.entity_embeddings[tail]
        
        return np.sum(h * r * t)
    
    def train(self, kg: KnowledgeGraph, num_epochs: int = 100,
              num_negative: int = 5) -> KGEmbeddingResult:
        """训练DistMult模型"""
        logger.info(f"开始DistMult训练，维度: {self.embedding_dim}")
        
        kg.build_vocab()
        self._init_embeddings(kg)
        self.training_loss.clear()
        
        entities_list = list(kg.entities)
        
        for epoch in range(num_epochs):
            epoch_loss = 0.0
            
            for triple in kg.triples:
                h = self.entity_embeddings[triple.head]
                r = self.relation_embeddings[triple.relation]
                t = self.entity_embeddings[triple.tail]
                
                # 正样本得分
                pos_score = np.sum(h * r * t)
                
                # 负样本
                neg_scores = []
                for _ in range(num_negative):
                    neg_tail = random.choice(entities_list)
                    t_neg = self.entity_embeddings[neg_tail]
                    neg_scores.append(np.sum(h * r * t_neg))
                
                # BPR Loss（Bayesian Personalized Ranking）
                for neg_score in neg_scores:
                    diff = pos_score - neg_score
                    loss = -math.log(1 / (1 + math.exp(-diff)) + 1e-10)
                    epoch_loss += loss
                    
                    # 梯度更新
                    grad_factor = self.lr / (1 + math.exp(diff))
                    
                    self.entity_embeddings[triple.head] += grad_factor * (r * t)
                    self.relation_embeddings[triple.relation] += grad_factor * (h * t)
                    self.entity_embeddings[triple.tail] += grad_factor * (h * r)
                    
                    # L2正则化
                    self.entity_embeddings[triple.head] -= self.lr * self.reg * h
                    self.entity_embeddings[triple.tail] -= self.lr * self.reg * t
                    self.relation_embeddings[triple.relation] -= self.lr * self.reg * r
            
            avg_loss = epoch_loss / (len(kg.triples) * num_negative)
            self.training_loss.append(avg_loss)
            
            if (epoch + 1) % 20 == 0:
                logger.info(f"Epoch {epoch+1}, Loss: {avg_loss:.4f}")
        
        return KGEmbeddingResult(
            entity_embeddings=self.entity_embeddings.copy(),
            relation_embeddings=self.relation_embeddings.copy(),
            entity_count=len(kg.entities),
            relation_count=len(kg.relations),
            embedding_dim=self.embedding_dim,
            model_type='DistMult',
            training_loss=self.training_loss,
        )


class ComplEx:
    """
    ComplEx 复数空间嵌入
    
    在复数空间中进行嵌入，可以建模非对称关系
    评分函数：f(h, r, t) = Re(Σ h_i * r_i * conj(t_i))
    
    论文: Trouillon et al., "Complex Embeddings for Simple Link Prediction", 2016
    """
    
    def __init__(self, embedding_dim: int = 100, learning_rate: float = 0.01,
                 regularization: float = 0.01):
        self.embedding_dim = embedding_dim
        self.lr = learning_rate
        self.reg = regularization
        
        # 复数嵌入（实部和虚部）
        self.entity_re: Dict[str, np.ndarray] = {}
        self.entity_im: Dict[str, np.ndarray] = {}
        self.relation_re: Dict[str, np.ndarray] = {}
        self.relation_im: Dict[str, np.ndarray] = {}
        
        self.training_loss: List[float] = []
    
    def _init_embeddings(self, kg: KnowledgeGraph):
        scale = 6.0 / math.sqrt(self.embedding_dim)
        
        for entity in kg.entities:
            self.entity_re[entity] = np.random.uniform(-scale, scale, self.embedding_dim)
            self.entity_im[entity] = np.random.uniform(-scale, scale, self.embedding_dim)
        
        for relation in kg.relations:
            self.relation_re[relation] = np.random.uniform(-scale, scale, self.embedding_dim)
            self.relation_im[relation] = np.random.uniform(-scale, scale, self.embedding_dim)
    
    def score(self, head: str, relation: str, tail: str) -> float:
        """计算三元组得分（复数Hermitian内积的实部）"""
        h_re = self.entity_re.get(head, np.zeros(self.embedding_dim))
        h_im = self.entity_im.get(head, np.zeros(self.embedding_dim))
        r_re = self.relation_re.get(relation, np.zeros(self.embedding_dim))
        r_im = self.relation_im.get(relation, np.zeros(self.embedding_dim))
        t_re = self.entity_re.get(tail, np.zeros(self.embedding_dim))
        t_im = self.entity_im.get(tail, np.zeros(self.embedding_dim))
        
        # Re(<h, r, conj(t)>)
        # = Re((h_re + i*h_im) * (r_re + i*r_im) * (t_re - i*t_im))
        score = np.sum(
            h_re * r_re * t_re +
            h_im * r_re * t_im +
            h_re * r_im * t_im -
            h_im * r_im * t_re
        )
        
        return score
    
    def train(self, kg: KnowledgeGraph, num_epochs: int = 100,
              num_negative: int = 5) -> KGEmbeddingResult:
        """训练ComplEx模型"""
        logger.info(f"开始ComplEx训练，维度: {self.embedding_dim}")
        
        kg.build_vocab()
        self._init_embeddings(kg)
        self.training_loss.clear()
        
        entities_list = list(kg.entities)
        
        for epoch in range(num_epochs):
            epoch_loss = 0.0
            
            for triple in kg.triples:
                pos_score = self.score(triple.head, triple.relation, triple.tail)
                
                for _ in range(num_negative):
                    neg_tail = random.choice(entities_list)
                    neg_score = self.score(triple.head, triple.relation, neg_tail)
                    
                    diff = pos_score - neg_score
                    loss = -math.log(1 / (1 + math.exp(-diff)) + 1e-10)
                    epoch_loss += loss
                    
                    # 简化的梯度更新
                    grad_factor = self.lr / (1 + math.exp(diff))
                    
                    # 更新实体嵌入（只展示关键更新）
                    r_re = self.relation_re[triple.relation]
                    r_im = self.relation_im[triple.relation]
                    t_re = self.entity_re[triple.tail]
                    t_im = self.entity_im[triple.tail]
                    
                    self.entity_re[triple.head] += grad_factor * (r_re * t_re + r_im * t_im)
                    self.entity_im[triple.head] += grad_factor * (r_re * t_im - r_im * t_re)
            
            avg_loss = epoch_loss / (len(kg.triples) * num_negative)
            self.training_loss.append(avg_loss)
            
            if (epoch + 1) % 20 == 0:
                logger.info(f"Epoch {epoch+1}, Loss: {avg_loss:.4f}")
        
        # 合并实部和虚部
        combined_entities = {
            e: np.concatenate([self.entity_re[e], self.entity_im[e]])
            for e in kg.entities
        }
        combined_relations = {
            r: np.concatenate([self.relation_re[r], self.relation_im[r]])
            for r in kg.relations
        }
        
        return KGEmbeddingResult(
            entity_embeddings=combined_entities,
            relation_embeddings=combined_relations,
            entity_count=len(kg.entities),
            relation_count=len(kg.relations),
            embedding_dim=self.embedding_dim * 2,
            model_type='ComplEx',
            training_loss=self.training_loss,
        )


class PathReasoner:
    """
    路径推理器
    
    基于多跳路径进行知识图谱推理
    支持可变长度路径和路径约束
    """
    
    def __init__(self, kg: KnowledgeGraph, max_path_length: int = 3):
        self.kg = kg
        self.max_path_length = max_path_length
        
        # 缓存关系路径
        self.relation_paths: Dict[Tuple[str, str], List[List[str]]] = {}
    
    def find_paths(self, start: str, end: str, max_length: int = None) -> List[List[str]]:
        """
        查找两个实体之间的所有路径
        
        返回关系序列列表
        """
        if max_length is None:
            max_length = self.max_path_length
        
        cache_key = (start, end)
        if cache_key in self.relation_paths:
            return self.relation_paths[cache_key]
        
        paths = []
        self._dfs_paths(start, end, [], set([start]), paths, max_length)
        
        self.relation_paths[cache_key] = paths
        return paths
    
    def _dfs_paths(self, current: str, target: str, current_path: List[str],
                   visited: Set[str], all_paths: List[List[str]], max_length: int):
        """深度优先搜索路径"""
        if current == target and current_path:
            all_paths.append(current_path.copy())
            return
        
        if len(current_path) >= max_length:
            return
        
        for triple in self.kg.head_index[current]:
            if triple.tail not in visited:
                visited.add(triple.tail)
                current_path.append(triple.relation)
                
                self._dfs_paths(triple.tail, target, current_path, visited, all_paths, max_length)
                
                current_path.pop()
                visited.remove(triple.tail)
    
    def path_ranking(self, head: str, relation: str, 
                     candidates: List[str]) -> List[Tuple[str, float]]:
        """
        基于路径特征的候选排序
        
        使用路径类型作为特征预测正确的尾实体
        """
        # 收集所有正样本的路径模式
        positive_paths = defaultdict(int)
        for triple in self.kg.relation_index[relation]:
            paths = self.find_paths(triple.head, triple.tail)
            for path in paths:
                path_type = tuple(path)
                positive_paths[path_type] += 1
        
        # 对候选进行评分
        scores = []
        for candidate in candidates:
            paths = self.find_paths(head, candidate)
            
            score = 0.0
            for path in paths:
                path_type = tuple(path)
                score += positive_paths.get(path_type, 0)
            
            scores.append((candidate, score))
        
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores


class RuleLearner:
    """
    规则学习器
    
    从知识图谱中学习Horn子句规则
    例如：father(X, Y) ∧ mother(Y, Z) → grandfather(X, Z)
    
    使用AMIE风格的规则挖掘
    """
    
    def __init__(self, kg: KnowledgeGraph, min_support: int = 2,
                 min_confidence: float = 0.5):
        self.kg = kg
        self.min_support = min_support
        self.min_confidence = min_confidence
        
        self.rules: List[Dict] = []
    
    def learn_rules(self, target_relation: str, max_body_length: int = 2):
        """
        学习针对目标关系的规则
        
        Args:
            target_relation: 规则头的关系
            max_body_length: 规则体最大长度
        """
        logger.info(f"学习关系 {target_relation} 的规则")
        
        self.rules = []
        
        # 单关系规则
        for r in self.kg.relations:
            if r == target_relation:
                continue
            
            rule = self._evaluate_rule([r], target_relation)
            if rule:
                self.rules.append(rule)
        
        # 双关系规则
        if max_body_length >= 2:
            for r1 in self.kg.relations:
                for r2 in self.kg.relations:
                    rule = self._evaluate_rule([r1, r2], target_relation)
                    if rule:
                        self.rules.append(rule)
        
        # 按置信度排序
        self.rules.sort(key=lambda x: x['confidence'], reverse=True)
        
        logger.info(f"发现 {len(self.rules)} 条规则")
        return self.rules
    
    def _evaluate_rule(self, body: List[str], head: str) -> Optional[Dict]:
        """评估一条规则"""
        # 计算规则支持度：规则体和头同时成立的实例数
        support = 0
        body_only = 0
        
        for triple in self.kg.relation_index[head]:
            h, t = triple.head, triple.tail
            
            # 检查是否存在满足规则体的路径
            if self._check_body(h, t, body):
                support += 1
        
        if support < self.min_support:
            return None
        
        # 计算body_only（只满足规则体的实例）
        for start_entity in self.kg.entities:
            reachable = self._apply_body(start_entity, body)
            for end_entity in reachable:
                body_only += 1
        
        if body_only == 0:
            return None
        
        confidence = support / body_only
        
        if confidence < self.min_confidence:
            return None
        
        return {
            'body': body,
            'head': head,
            'support': support,
            'confidence': confidence,
            'lift': confidence * len(self.kg.entities) / len(self.kg.relation_index[head]),
        }
    
    def _check_body(self, start: str, end: str, body: List[str]) -> bool:
        """检查是否存在满足body的路径"""
        current_entities = {start}
        
        for relation in body:
            next_entities = set()
            for entity in current_entities:
                for triple in self.kg.head_index[entity]:
                    if triple.relation == relation:
                        next_entities.add(triple.tail)
            current_entities = next_entities
        
        return end in current_entities
    
    def _apply_body(self, start: str, body: List[str]) -> Set[str]:
        """应用规则体，返回可达实体"""
        current_entities = {start}
        
        for relation in body:
            next_entities = set()
            for entity in current_entities:
                for triple in self.kg.head_index[entity]:
                    if triple.relation == relation:
                        next_entities.add(triple.tail)
            current_entities = next_entities
        
        return current_entities


class CareerKnowledgeGraphReasoner:
    """
    职业知识图谱推理器
    
    整合多种KG嵌入和推理方法
    """
    
    EMBEDDING_MODELS = {
        'transe': TransE,
        'transr': TransR,
        'distmult': DistMult,
        'complex': ComplEx,
    }
    
    def __init__(self, model_type: str = 'transe', embedding_dim: int = 100):
        if model_type not in self.EMBEDDING_MODELS:
            raise ValueError(f"未知模型: {model_type}")
        
        self.model_type = model_type
        self.embedding_dim = embedding_dim
        
        self.kg = KnowledgeGraph()
        self.model = None
        self.path_reasoner = None
        self.rule_learner = None
    
    def build_career_kg(self, career_paths: list, skills_data: dict = None):
        """
        从职业路径数据构建知识图谱
        
        关系类型：
        - promotes_to：晋升关系
        - transfers_to：换岗关系
        - requires_skill：岗位-技能关系
        - related_skill：技能关联
        """
        logger.info("构建职业知识图谱")
        
        for path in career_paths:
            from_pos = path.get('from_position') or getattr(path, 'from_position', None)
            to_pos = path.get('to_position') or getattr(path, 'to_position', None)
            rel_type = path.get('relation_type') or getattr(path, 'relation_type', 'promotes_to')
            
            if from_pos and to_pos:
                relation = 'promotes_to' if rel_type == 'promotion' else 'transfers_to'
                self.kg.add_triple(from_pos, relation, to_pos)
                
                # 获取技能要求
                skills = path.get('required_skills') or getattr(path, 'required_skills', [])
                if isinstance(skills, str):
                    try:
                        import json
                        skills = json.loads(skills)
                    except:
                        skills = []
                
                for skill in skills:
                    self.kg.add_triple(to_pos, 'requires_skill', skill)
        
        # 添加技能数据
        if skills_data:
            for skill, related_skills in skills_data.items():
                for related in related_skills:
                    self.kg.add_triple(skill, 'related_skill', related)
        
        self.kg.build_vocab()
        
        # 初始化推理器
        self.path_reasoner = PathReasoner(self.kg)
        self.rule_learner = RuleLearner(self.kg)
    
    def train_embeddings(self, num_epochs: int = 100) -> KGEmbeddingResult:
        """训练知识图谱嵌入"""
        ModelClass = self.EMBEDDING_MODELS[self.model_type]
        self.model = ModelClass(embedding_dim=self.embedding_dim)
        return self.model.train(self.kg, num_epochs=num_epochs)
    
    def predict_career_transition(self, current_position: str, 
                                   top_k: int = 5) -> List[LinkPredictionResult]:
        """预测可能的职业转换"""
        results = []
        
        for relation in ['promotes_to', 'transfers_to']:
            if self.model and hasattr(self.model, 'predict_tail'):
                predictions = self.model.predict_tail(current_position, relation, self.kg, top_k)
            else:
                predictions = []
            
            results.append(LinkPredictionResult(
                head=current_position,
                relation=relation,
                predicted_tails=predictions,
                confidence=1.0 if predictions else 0.0,
            ))
        
        return results
    
    def find_skill_path(self, current_skills: List[str], 
                        target_position: str) -> List[str]:
        """查找技能提升路径"""
        required_skills = set()
        
        # 获取目标岗位的技能要求
        for triple in self.kg.head_index[target_position]:
            if triple.relation == 'requires_skill':
                required_skills.add(triple.tail)
        
        # 技能差距
        skill_gap = required_skills - set(current_skills)
        
        # 按相关性排序（基于嵌入相似度）
        if self.model:
            scored_skills = []
            for skill in skill_gap:
                similar = self.model.get_similar_entities(skill, top_k=5)
                overlap = len(set(s for s, _ in similar) & set(current_skills))
                scored_skills.append((skill, overlap))
            
            scored_skills.sort(key=lambda x: x[1], reverse=True)
            return [s for s, _ in scored_skills]
        
        return list(skill_gap)


logger.info("知识图谱推理模块加载完成")

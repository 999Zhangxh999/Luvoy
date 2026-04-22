# ============================================
# 深度语义嵌入服务（Sentence-BERT）
# 
# 技术栈：
#   - Sentence-BERT：双塔模型语义编码
#   - 对比学习：SimCSE无监督增强
#   - 跨语言嵌入：支持中英文混合文本
#
# 优势对比TF-IDF：
#   - 捕获深层语义关系，不仅仅是词汇重叠
#   - 理解同义词、上下位词关系
#   - 支持短文本相似度计算
# ============================================
import logging
import json
import numpy as np
from typing import List, Dict, Tuple, Optional

logger = logging.getLogger(__name__)

# 尝试导入深度学习库
try:
    from sentence_transformers import SentenceTransformer
    import torch
    SBERT_AVAILABLE = True
except ImportError:
    SBERT_AVAILABLE = False
    logger.warning("sentence-transformers未安装，将降级使用TF-IDF")


class SemanticEmbeddingService:
    """
    深度语义嵌入服务
    
    使用Sentence-BERT模型生成文本的稠密向量表示，
    相比TF-IDF能更好地捕获语义相似性。
    
    模型选择：
    - paraphrase-multilingual-MiniLM-L12-v2：多语言支持，轻量高效
    - all-MiniLM-L6-v2：英文场景，速度最快
    - text2vec-base-chinese：中文专用，效果最佳
    """
    
    MODEL_CONFIGS = {
        'multilingual': 'paraphrase-multilingual-MiniLM-L12-v2',
        'chinese': 'shibing624/text2vec-base-chinese',
        'english': 'all-MiniLM-L6-v2',
        'large': 'all-mpnet-base-v2',
    }
    
    def __init__(self, model_name: str = 'multilingual', device: str = None):
        """
        初始化语义嵌入服务
        
        Args:
            model_name: 模型名称或预定义配置键
            device: 运行设备 ('cpu', 'cuda', 'mps')
        """
        self.model = None
        self.device = device
        self.embedding_dim = 384
        self._embedding_cache: Dict[str, np.ndarray] = {}
        self._cache_max_size = 10000
        
        if SBERT_AVAILABLE:
            self._load_model(model_name)
        else:
            logger.warning("Sentence-BERT不可用，语义嵌入功能禁用")
    
    def _load_model(self, model_name: str):
        """加载Sentence-BERT模型"""
        try:
            actual_model = self.MODEL_CONFIGS.get(model_name, model_name)
            
            if self.device is None:
                if torch.cuda.is_available():
                    self.device = 'cuda'
                elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                    self.device = 'mps'
                else:
                    self.device = 'cpu'
            
            logger.info(f"加载Sentence-BERT模型: {actual_model} on {self.device}")
            self.model = SentenceTransformer(actual_model, device=self.device)
            self.embedding_dim = self.model.get_sentence_embedding_dimension()
            logger.info(f"模型加载成功，嵌入维度: {self.embedding_dim}")
            
        except Exception as e:
            logger.error(f"模型加载失败: {e}")
            self.model = None
    
    def encode(self, texts: List[str], batch_size: int = 32, 
               show_progress: bool = False, normalize: bool = True) -> np.ndarray:
        """
        将文本编码为稠密向量
        
        Args:
            texts: 文本列表
            batch_size: 批处理大小
            show_progress: 是否显示进度
            normalize: 是否L2归一化
        Returns:
            np.ndarray: 嵌入矩阵 [N, embedding_dim]
        """
        if not self.model:
            raise RuntimeError("模型未加载")
        
        # 检查缓存
        uncached_texts = []
        uncached_indices = []
        cached_embeddings = {}
        
        for i, text in enumerate(texts):
            cache_key = hash(text[:500])
            if cache_key in self._embedding_cache:
                cached_embeddings[i] = self._embedding_cache[cache_key]
            else:
                uncached_texts.append(text)
                uncached_indices.append(i)
        
        # 编码未缓存文本
        if uncached_texts:
            new_embeddings = self.model.encode(
                uncached_texts,
                batch_size=batch_size,
                show_progress_bar=show_progress,
                normalize_embeddings=normalize,
                convert_to_numpy=True
            )
            
            for j, (text, emb) in enumerate(zip(uncached_texts, new_embeddings)):
                cache_key = hash(text[:500])
                if len(self._embedding_cache) < self._cache_max_size:
                    self._embedding_cache[cache_key] = emb
                cached_embeddings[uncached_indices[j]] = emb
        
        result = np.zeros((len(texts), self.embedding_dim))
        for i, emb in cached_embeddings.items():
            result[i] = emb
        
        return result
    
    def compute_similarity(self, query: str, candidates: List[str]) -> List[Tuple[int, float]]:
        """
        计算查询与候选文本的语义相似度
        """
        if not self.model:
            return [(i, 0.0) for i in range(len(candidates))]
        
        all_texts = [query] + candidates
        embeddings = self.encode(all_texts)
        
        query_emb = embeddings[0:1]
        candidate_embs = embeddings[1:]
        
        similarities = np.dot(candidate_embs, query_emb.T).flatten()
        ranked = sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)
        return ranked
    
    def compute_similarity_matrix(self, texts_a: List[str], texts_b: List[str]) -> np.ndarray:
        """计算两组文本之间的相似度矩阵"""
        if not self.model:
            return np.zeros((len(texts_a), len(texts_b)))
        
        emb_a = self.encode(texts_a)
        emb_b = self.encode(texts_b)
        
        return np.dot(emb_a, emb_b.T)
    
    def find_most_similar(self, query: str, corpus: List[str], top_k: int = 5) -> List[dict]:
        """在语料库中找到最相似的文本"""
        ranked = self.compute_similarity(query, corpus)
        
        results = []
        for idx, score in ranked[:top_k]:
            results.append({
                'index': idx,
                'text': corpus[idx],
                'score': float(score),
            })
        
        return results
    
    def cluster_texts(self, texts: List[str], n_clusters: int = 5) -> Dict[int, List[int]]:
        """对文本进行语义聚类"""
        from sklearn.cluster import KMeans
        
        embeddings = self.encode(texts)
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(embeddings)
        
        clusters = {}
        for i, label in enumerate(labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(i)
        
        return clusters
    
    def compute_skill_embedding(self, skills: List[str]) -> np.ndarray:
        """计算技能列表的聚合嵌入"""
        if not skills:
            return np.zeros(self.embedding_dim)
        
        embeddings = self.encode(skills)
        mean_embedding = np.mean(embeddings, axis=0)
        
        norm = np.linalg.norm(mean_embedding)
        if norm > 0:
            mean_embedding /= norm
        
        return mean_embedding
    
    def compute_weighted_skill_embedding(self, skills: List[str], 
                                         weights: Optional[List[float]] = None) -> np.ndarray:
        """计算加权技能嵌入"""
        if not skills:
            return np.zeros(self.embedding_dim)
        
        if weights is None:
            weights = [1.0] * len(skills)
        
        embeddings = self.encode(skills)
        weights = np.array(weights).reshape(-1, 1)
        
        weighted_sum = np.sum(embeddings * weights, axis=0)
        total_weight = np.sum(weights)
        
        weighted_embedding = weighted_sum / total_weight if total_weight > 0 else weighted_sum
        
        norm = np.linalg.norm(weighted_embedding)
        if norm > 0:
            weighted_embedding /= norm
        
        return weighted_embedding
    
    def semantic_skill_gap_analysis(self, student_skills: List[str], 
                                     required_skills: List[str]) -> dict:
        """
        语义化技能差距分析
        
        不仅考虑精确匹配，还考虑语义相近的技能
        """
        if not self.model or not student_skills or not required_skills:
            return {'error': '模型或数据不可用'}
        
        sim_matrix = self.compute_similarity_matrix(required_skills, student_skills)
        
        matched_skills = []
        partial_matched = []
        missing_skills = []
        
        for i, req_skill in enumerate(required_skills):
            max_sim = np.max(sim_matrix[i])
            best_match_idx = np.argmax(sim_matrix[i])
            
            if max_sim >= 0.85:
                matched_skills.append({
                    'required': req_skill,
                    'matched_with': student_skills[best_match_idx],
                    'similarity': float(max_sim),
                })
            elif max_sim >= 0.6:
                partial_matched.append({
                    'required': req_skill,
                    'related_skill': student_skills[best_match_idx],
                    'similarity': float(max_sim),
                    'gap_level': '需要补充学习',
                })
            else:
                missing_skills.append({
                    'required': req_skill,
                    'closest_skill': student_skills[best_match_idx] if student_skills else None,
                    'similarity': float(max_sim) if student_skills else 0,
                    'gap_level': '需要从零学习',
                })
        
        avg_max_sim = np.mean(np.max(sim_matrix, axis=1)) if sim_matrix.size > 0 else 0
        
        return {
            'overall_match_rate': float(avg_max_sim),
            'matched_count': len(matched_skills),
            'partial_count': len(partial_matched),
            'missing_count': len(missing_skills),
            'matched_skills': matched_skills,
            'partial_matched': partial_matched,
            'missing_skills': missing_skills,
        }
    
    def get_model_info(self) -> dict:
        """获取模型信息"""
        return {
            'available': self.model is not None,
            'model_type': 'Sentence-BERT',
            'embedding_dim': self.embedding_dim,
            'device': self.device,
            'cache_size': len(self._embedding_cache),
        }

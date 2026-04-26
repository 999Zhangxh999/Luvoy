# ============================================
# 图嵌入服务（Node2Vec / Graph Neural Network特征）
# 
# 技术栈：
#   - Node2Vec：基于随机游走的图嵌入
#   - DeepWalk：图结构学习
#   - 图特征工程：节点中心性、结构角色等
#
# 应用场景：
#   - 职业相似度计算（基于图结构而非文本）
#   - 职业聚类（发现隐含的职业群落）
#   - 路径推荐（结合图结构特征）
# ============================================
import logging
import numpy as np
import networkx as nx
from typing import List, Dict, Tuple, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)

try:
    from gensim.models import Word2Vec
    GENSIM_AVAILABLE = True
except ImportError:
    GENSIM_AVAILABLE = False
    logger.warning("gensim未安装，Node2Vec功能禁用")


class Node2VecWalker:
    """
    Node2Vec随机游走器
    
    实现有偏随机游走，平衡BFS（同质性）和DFS（结构等价性）
    """
    
    def __init__(self, graph: nx.Graph, p: float = 1.0, q: float = 1.0):
        """
        Args:
            graph: NetworkX图
            p: 返回参数（控制回到前一节点的概率）
            q: 入出参数（控制BFS vs DFS倾向）
        """
        self.graph = graph
        self.p = p
        self.q = q
        self._precompute_transition_probs()
    
    def _precompute_transition_probs(self):
        """预计算转移概率"""
        self.alias_nodes = {}
        self.alias_edges = {}
        
        for node in self.graph.nodes():
            neighbors = list(self.graph.neighbors(node))
            if neighbors:
                probs = [self.graph[node][nbr].get('weight', 1.0) for nbr in neighbors]
                norm_probs = [p / sum(probs) for p in probs]
                self.alias_nodes[node] = {'probs': norm_probs, 'items': neighbors}
        
        for edge in self.graph.edges():
            self._precompute_edge_probs(edge[0], edge[1])
            if not self.graph.is_directed():
                self._precompute_edge_probs(edge[1], edge[0])
    
    def _precompute_edge_probs(self, src, dst):
        """预计算边转移概率"""
        neighbors = list(self.graph.neighbors(dst))
        if not neighbors:
            return
        
        unnorm_probs = []
        for neighbor in neighbors:
            weight = self.graph[dst][neighbor].get('weight', 1.0)
            
            if neighbor == src:
                unnorm_probs.append(weight / self.p)
            elif self.graph.has_edge(neighbor, src):
                unnorm_probs.append(weight)
            else:
                unnorm_probs.append(weight / self.q)
        
        norm_probs = [p / sum(unnorm_probs) for p in unnorm_probs]
        self.alias_edges[(src, dst)] = {'probs': norm_probs, 'items': neighbors}
    
    def random_walk(self, start_node, walk_length: int) -> List:
        """执行一次随机游走"""
        walk = [start_node]
        
        while len(walk) < walk_length:
            cur = walk[-1]
            neighbors = list(self.graph.neighbors(cur))
            
            if not neighbors:
                break
            
            if len(walk) == 1:
                if cur in self.alias_nodes:
                    alias = self.alias_nodes[cur]
                    walk.append(np.random.choice(alias['items'], p=alias['probs']))
                else:
                    walk.append(np.random.choice(neighbors))
            else:
                prev = walk[-2]
                if (prev, cur) in self.alias_edges:
                    alias = self.alias_edges[(prev, cur)]
                    walk.append(np.random.choice(alias['items'], p=alias['probs']))
                else:
                    walk.append(np.random.choice(neighbors))
        
        return walk
    
    def generate_walks(self, num_walks: int, walk_length: int) -> List[List]:
        """生成所有节点的随机游走序列"""
        walks = []
        nodes = list(self.graph.nodes())
        
        for _ in range(num_walks):
            np.random.shuffle(nodes)
            for node in nodes:
                walk = self.random_walk(node, walk_length)
                walks.append([str(n) for n in walk])
        
        return walks


class GraphEmbeddingService:
    """
    图嵌入服务
    
    提供基于图结构的节点表示学习
    """
    
    def __init__(self, embedding_dim: int = 64, walk_length: int = 30,
                 num_walks: int = 10, p: float = 1.0, q: float = 1.0,
                 window: int = 5, workers: int = 4):
        self.embedding_dim = embedding_dim
        self.walk_length = walk_length
        self.num_walks = num_walks
        self.p = p
        self.q = q
        self.window = window
        self.workers = workers
        
        self.model = None
        self.graph = None
        self.node_embeddings: Dict[str, np.ndarray] = {}
    
    def fit(self, graph: nx.Graph):
        """训练图嵌入模型"""
        if not GENSIM_AVAILABLE:
            logger.warning("gensim不可用，跳过Node2Vec训练")
            return
        
        self.graph = graph
        
        if len(graph.nodes()) == 0:
            logger.warning("空图，跳过训练")
            return
        
        logger.info(f"开始Node2Vec训练，节点数: {len(graph.nodes())}")
        
        walker = Node2VecWalker(graph, p=self.p, q=self.q)
        walks = walker.generate_walks(self.num_walks, self.walk_length)
        
        self.model = Word2Vec(
            sentences=walks,
            vector_size=self.embedding_dim,
            window=self.window,
            min_count=1,
            sg=1,
            workers=self.workers,
            epochs=5,
        )
        
        for node in graph.nodes():
            node_str = str(node)
            if node_str in self.model.wv:
                self.node_embeddings[str(node)] = self.model.wv[node_str]
        
        logger.info(f"Node2Vec训练完成，嵌入 {len(self.node_embeddings)} 个节点")
    
    def fit_from_paths(self, career_paths: list):
        """从职业路径数据构建图并训练"""
        G = nx.DiGraph()
        
        for path in career_paths:
            from_pos = path.get('from_position') or getattr(path, 'from_position', None)
            to_pos = path.get('to_position') or getattr(path, 'to_position', None)
            
            if from_pos and to_pos:
                difficulty = path.get('difficulty') or getattr(path, 'difficulty', 3)
                weight = 1.0 / max(difficulty, 1)
                G.add_edge(from_pos, to_pos, weight=weight)
        
        self.fit(G)
    
    def get_embedding(self, node: str) -> Optional[np.ndarray]:
        """获取节点嵌入"""
        return self.node_embeddings.get(str(node))
    
    def compute_similarity(self, node1: str, node2: str) -> float:
        """计算两个节点的图结构相似度"""
        emb1 = self.get_embedding(node1)
        emb2 = self.get_embedding(node2)
        
        if emb1 is None or emb2 is None:
            return 0.0
        
        dot = np.dot(emb1, emb2)
        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)
        
        if norm1 > 0 and norm2 > 0:
            return float(dot / (norm1 * norm2))
        return 0.0
    
    def find_similar_nodes(self, node: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """找到最相似的节点"""
        if not self.model or str(node) not in self.model.wv:
            return []
        
        similar = self.model.wv.most_similar(str(node), topn=top_k)
        return [(n, float(s)) for n, s in similar]
    
    def cluster_nodes(self, n_clusters: int = 5) -> Dict[int, List[str]]:
        """基于嵌入的节点聚类"""
        from sklearn.cluster import KMeans
        
        if not self.node_embeddings:
            return {}
        
        nodes = list(self.node_embeddings.keys())
        embeddings = np.array([self.node_embeddings[n] for n in nodes])
        
        kmeans = KMeans(n_clusters=min(n_clusters, len(nodes)), random_state=42, n_init=10)
        labels = kmeans.fit_predict(embeddings)
        
        clusters = defaultdict(list)
        for node, label in zip(nodes, labels):
            clusters[int(label)].append(node)
        
        return dict(clusters)
    
    def compute_structural_features(self, graph: nx.Graph = None) -> Dict[str, Dict[str, float]]:
        """计算节点的结构特征"""
        G = graph or self.graph
        if G is None:
            return {}
        
        features = {}
        
        in_degree = dict(G.in_degree()) if G.is_directed() else dict(G.degree())
        out_degree = dict(G.out_degree()) if G.is_directed() else dict(G.degree())
        
        try:
            pagerank = nx.pagerank(G, alpha=0.85)
        except:
            pagerank = {n: 0 for n in G.nodes()}
        
        if len(G.nodes()) <= 500:
            betweenness = nx.betweenness_centrality(G)
        else:
            betweenness = {n: 0 for n in G.nodes()}
        
        for node in G.nodes():
            features[str(node)] = {
                'in_degree': in_degree.get(node, 0),
                'out_degree': out_degree.get(node, 0),
                'pagerank': pagerank.get(node, 0),
                'betweenness': betweenness.get(node, 0),
            }
        
        return features
    
    def recommend_career_transition(self, current_position: str) -> List[dict]:
        """基于图嵌入推荐职业转换方向"""
        if not self.graph or current_position not in self.graph.nodes():
            return []
        
        reachable = set()
        for successor in self.graph.successors(current_position):
            reachable.add(successor)
            for s2 in self.graph.successors(successor):
                reachable.add(s2)
        
        if current_position in reachable:
            reachable.remove(current_position)
        
        recommendations = []
        current_emb = self.get_embedding(current_position)
        
        for target in reachable:
            target_emb = self.get_embedding(target)
            
            if current_emb is not None and target_emb is not None:
                similarity = float(np.dot(current_emb, target_emb) / 
                                   (np.linalg.norm(current_emb) * np.linalg.norm(target_emb) + 1e-8))
            else:
                similarity = 0.5
            
            is_direct = self.graph.has_edge(current_position, target)
            
            recommendations.append({
                'position': target,
                'similarity': similarity,
                'is_direct': is_direct,
                'recommendation_score': similarity * (1.5 if is_direct else 1.0),
            })
        
        recommendations.sort(key=lambda x: x['recommendation_score'], reverse=True)
        return recommendations[:10]
    
    def get_model_info(self) -> dict:
        """获取模型信息"""
        return {
            'available': self.model is not None,
            'model_type': 'Node2Vec',
            'embedding_dim': self.embedding_dim,
            'num_nodes': len(self.node_embeddings),
        }

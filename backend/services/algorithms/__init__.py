# ============================================
# 高级算法服务包
# 
# 包含模块：
#   - 基础算法：TF-IDF嵌入 / AHP层次分析 / 图算法 / 技能本体
#   - 深度学习：Sentence-BERT语义嵌入 / Node2Vec图嵌入
#   - 优化算法：贝叶斯优化 / MDP决策规划
#   - 集成学习：多模型融合 / Stacking
#   - 智能体：Multi-Agent协作
# ============================================

# 基础算法
from services.algorithms.embedding_service import EmbeddingService
from services.algorithms.ahp_service import AHPService
from services.algorithms.graph_algorithm import GraphAlgorithmService
from services.algorithms.skill_ontology import SkillOntologyService
from services.algorithms.agent_orchestrator import AgentOrchestrator

# 高级深度学习算法（可选依赖）
try:
    from services.algorithms.semantic_embedding import SemanticEmbeddingService
    SEMANTIC_EMBEDDING_AVAILABLE = True
except ImportError:
    SemanticEmbeddingService = None
    SEMANTIC_EMBEDDING_AVAILABLE = False

try:
    from services.algorithms.graph_embedding import GraphEmbeddingService
    GRAPH_EMBEDDING_AVAILABLE = True
except ImportError:
    GraphEmbeddingService = None
    GRAPH_EMBEDDING_AVAILABLE = False

# MDP决策规划
try:
    from services.algorithms.mdp_planner import MDPCareerPlanner
    MDP_AVAILABLE = True
except ImportError:
    MDPCareerPlanner = None
    MDP_AVAILABLE = False

# 贝叶斯优化
try:
    from services.algorithms.bayesian_optimizer import BayesianOptimizer, AdaptiveWeightOptimizer
    BAYESIAN_AVAILABLE = True
except ImportError:
    BayesianOptimizer = None
    AdaptiveWeightOptimizer = None
    BAYESIAN_AVAILABLE = False

# 集成学习
try:
    from services.algorithms.ensemble_learning import EnsembleMatcher, MultiModelRecommender
    ENSEMBLE_AVAILABLE = True
except ImportError:
    EnsembleMatcher = None
    MultiModelRecommender = None
    ENSEMBLE_AVAILABLE = False

# ========== 新增：扩展算法模块 ==========

# 注意力机制
try:
    from services.algorithms.attention_mechanism import (
        ScaledDotProductAttention, MultiHeadAttention, 
        CrossAttention, SkillAttentionMatcher
    )
    ATTENTION_AVAILABLE = True
except ImportError:
    ScaledDotProductAttention = None
    MultiHeadAttention = None
    CrossAttention = None
    SkillAttentionMatcher = None
    ATTENTION_AVAILABLE = False

# 深度匹配
try:
    from services.algorithms.deep_matching import (
        TwoTowerMatcher, DeepCrossNetwork, CareerDeepMatcher
    )
    DEEP_MATCHING_AVAILABLE = True
except ImportError:
    TwoTowerMatcher = None
    DeepCrossNetwork = None
    CareerDeepMatcher = None
    DEEP_MATCHING_AVAILABLE = False

# MCTS规划器
try:
    from services.algorithms.mcts_planner import CareerMCTSPlanner
    MCTS_AVAILABLE = True
except ImportError:
    CareerMCTSPlanner = None
    MCTS_AVAILABLE = False

# 强化学习
try:
    from services.algorithms.reinforcement_learning import (
        QLearningAgent, CareerRLPlanner
    )
    RL_AVAILABLE = True
except ImportError:
    QLearningAgent = None
    CareerRLPlanner = None
    RL_AVAILABLE = False

# 多目标优化
try:
    from services.algorithms.multi_objective import (
        NSGAII, MOEAD, CareerMultiObjectiveOptimizer
    )
    MOO_AVAILABLE = True
except ImportError:
    NSGAII = None
    MOEAD = None
    CareerMultiObjectiveOptimizer = None
    MOO_AVAILABLE = False

# 知识图谱
try:
    from services.algorithms.knowledge_graph import (
        KnowledgeGraph, TransE, CareerKnowledgeGraphReasoner
    )
    KG_AVAILABLE = True
except ImportError:
    KnowledgeGraph = None
    TransE = None
    CareerKnowledgeGraphReasoner = None
    KG_AVAILABLE = False

# 职业AI引擎
try:
    from services.algorithms.career_ai_engine import (
        CareerAIEngine, CareerFeatureExtractor, IntelligentMatcher
    )
    CAREER_AI_AVAILABLE = True
except ImportError:
    CareerAIEngine = None
    CareerFeatureExtractor = None
    IntelligentMatcher = None
    CAREER_AI_AVAILABLE = False


__all__ = [
    # 基础算法
    'EmbeddingService',
    'AHPService', 
    'GraphAlgorithmService',
    'SkillOntologyService',
    'AgentOrchestrator',
    # 高级算法
    'SemanticEmbeddingService',
    'GraphEmbeddingService',
    'MDPCareerPlanner',
    'BayesianOptimizer',
    'AdaptiveWeightOptimizer',
    'EnsembleMatcher',
    'MultiModelRecommender',
    # 扩展算法
    'ScaledDotProductAttention',
    'MultiHeadAttention',
    'CrossAttention',
    'SkillAttentionWeighter',
    'TwoTowerModel',
    'DeepCrossNetwork',
    'CareerDeepMatcher',
    'CareerMCTSPlanner',
    'QLearningAgent',
    'DQNAgent',
    'CareerRLAgent',
    'NSGAII',
    'MOEAD',
    'CareerMultiObjectiveOptimizer',
    'KnowledgeGraph',
    'TransE',
    'LinkPredictor',
    'CareerKnowledgeGraph',
    'CareerAIEngine',
    'CareerFeatureExtractor',
    'IntelligentMatcher',
    # 可用性标志
    'SEMANTIC_EMBEDDING_AVAILABLE',
    'GRAPH_EMBEDDING_AVAILABLE',
    'MDP_AVAILABLE',
    'BAYESIAN_AVAILABLE',
    'ENSEMBLE_AVAILABLE',
    'ATTENTION_AVAILABLE',
    'DEEP_MATCHING_AVAILABLE',
    'MCTS_AVAILABLE',
    'RL_AVAILABLE',
    'MOO_AVAILABLE',
    'KG_AVAILABLE',
    'CAREER_AI_AVAILABLE',
]


def get_available_algorithms() -> dict:
    """获取所有可用算法的状态"""
    return {
        'basic': {
            'tfidf_embedding': True,
            'ahp_service': True,
            'graph_algorithm': True,
            'skill_ontology': True,
            'agent_orchestrator': True,
        },
        'advanced': {
            'semantic_embedding': SEMANTIC_EMBEDDING_AVAILABLE,
            'graph_embedding': GRAPH_EMBEDDING_AVAILABLE,
            'mdp_planner': MDP_AVAILABLE,
            'bayesian_optimizer': BAYESIAN_AVAILABLE,
            'ensemble_learning': ENSEMBLE_AVAILABLE,
        },
        'extended': {
            'attention_mechanism': ATTENTION_AVAILABLE,
            'deep_matching': DEEP_MATCHING_AVAILABLE,
            'mcts_planner': MCTS_AVAILABLE,
            'reinforcement_learning': RL_AVAILABLE,
            'multi_objective': MOO_AVAILABLE,
            'knowledge_graph': KG_AVAILABLE,
            'career_ai_engine': CAREER_AI_AVAILABLE,
        }
    }

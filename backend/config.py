# ============================================
# 配置文件 - 管理所有可配置项
# ============================================
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """基础配置"""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'career-planning-agent-secret-key-2024')
    
    # 数据库 - 使用绝对路径确保一致性
    _db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'career_planning.db')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{_db_path}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 文件上传
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
    
    # LLM配置 - 使用OpenAI兼容格式，支持各类大模型
    # 支持: OpenAI / 通义千问 / 智谱AI / DeepSeek / Moonshot 等
    LLM_API_KEY = os.getenv('LLM_API_KEY', '')
    LLM_BASE_URL = os.getenv('LLM_BASE_URL', 'https://api.deepseek.com/v1')
    LLM_MODEL = os.getenv('LLM_MODEL', 'deepseek-chat')
    LLM_TEMPERATURE = float(os.getenv('LLM_TEMPERATURE', '0.7'))
    LLM_MAX_TOKENS = int(os.getenv('LLM_MAX_TOKENS', '4096'))
    
    # 岗位数据文件路径
    JOB_DATA_PATH = os.getenv('JOB_DATA_PATH', 
                               os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                           '..', 'tableConvert.com_pn6idf.json'))
    
    # ========== 高级算法配置 ==========
    # 两阶段匹配算法配置
    MATCHING_RECALL_TOP_K = int(os.getenv('MATCHING_RECALL_TOP_K', '20'))  # 向量召回 Top-K
    MATCHING_RERANK_TOP_N = int(os.getenv('MATCHING_RERANK_TOP_N', '5'))   # LLM精排 Top-N
    
    # AHP层次分析法权重优化
    AHP_ENABLED = os.getenv('AHP_ENABLED', 'true').lower() == 'true'
    
    # 图算法配置
    GRAPH_ALGORITHM = os.getenv('GRAPH_ALGORITHM', 'dijkstra')  # dijkstra / bfs
    GRAPH_PAGERANK_DAMPING = float(os.getenv('GRAPH_PAGERANK_DAMPING', '0.85'))
    
    # 多智能体配置
    AGENT_MAX_RETRIES = int(os.getenv('AGENT_MAX_RETRIES', '2'))
    AGENT_ENABLE_COT = os.getenv('AGENT_ENABLE_COT', 'true').lower() == 'true'


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False


# 配置映射
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

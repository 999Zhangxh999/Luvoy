"""
知识库生成脚本
功能：从原始职位数据中筛选计算机类岗位，进行向量化处理，生成JSON格式知识库
"""

import json
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 计算机类岗位关键词（岗位名称、行业、岗位详情匹配）
CS_POSITION_KEYWORDS = [
    # 开发类
    '前端', '后端', '全栈', '软件开发', '程序员', '架构师', '系统开发',
    'java开发', 'python开发', 'c++开发', 'c#开发', 'golang', 'go开发', 'php开发',
    'web开发', 'h5开发', '小程序开发',
    'android开发', 'ios开发', '移动开发', 'flutter', 'app开发',
    '.net开发', 'dotnet',
    
    # 数据类
    '数据分析师', '数据挖掘', '数据工程师', '大数据', 'hadoop', 'spark',
    'dba', '数据库管理', 'etl', '数仓', '数据仓库', 'bi工程师',
    
    # AI/ML
    '算法工程师', '机器学习', '深度学习', '人工智能', 'ai工程师',
    'nlp工程师', '自然语言处理', '计算机视觉', 'cv工程师', '图像算法',
    '推荐算法', '搜索算法',
    
    # 运维/云计算
    '运维工程师', 'devops', 'sre', '云计算', '云架构',
    '容器', '微服务', 'k8s', 'kubernetes',
    'linux运维', '系统运维', '网络工程师', '网络运维',
    
    # 测试
    '测试工程师', '测试开发', 'qa工程师', '自动化测试', '性能测试',
    '软件测试', '功能测试',
    
    # 安全
    '安全工程师', '信息安全', '网络安全', '渗透测试', '安全研发',
    
    # IT相关
    '实施工程师', '技术支持', 'it工程师', '系统集成',
    '嵌入式开发', '嵌入式工程师', '单片机', '物联网', 'iot',
    '区块链', '智能合约',
    
    # 产品/设计（IT领域）
    'it项目经理', '技术项目经理',
]

# 行业白名单（必须包含这些行业关键词之一才考虑）
CS_INDUSTRY_KEYWORDS = [
    '计算机软件', '互联网', 'it服务', '信息技术', '软件', '通信',
    '电子商务', '游戏', '网络', '数据', '人工智能', '云计算',
]

# 明确排除的非计算机类关键词
EXCLUDE_KEYWORDS = [
    '销售', '会计', '财务', '行政', '人事', 'hr', '招聘',
    '客服', '前台', '文员', '秘书', '助理',
    '保安', '保洁', '司机', '厨师', '服务员',
    '医生', '护士', '药剂', '医疗', '生物', '化学', '制药',
    '建筑工程', '土木', '施工', '工地', '混凝土',
    '机械制造', '焊工', '钳工', '车工', '电工',
    '教师', '讲师', '培训师', '辅导',
    '外贸', '报关', '跟单', '采购',
    '金融', '投资', '理财', '保险', '银行',
    '房产', '置业', '中介', '物业',
    '农业', '养殖', '种植',
]


def is_cs_related(job: dict) -> bool:
    """判断是否为计算机类岗位"""
    job_name = job.get('岗位名称', '').lower()
    industry = job.get('所属行业', '').lower()
    job_desc = job.get('岗位详情', '').lower()
    
    # 首先检查排除关键词（在岗位名称中）
    for exclude_kw in EXCLUDE_KEYWORDS:
        if exclude_kw in job_name:
            return False
    
    # 方式1: 岗位名称直接匹配关键词
    for kw in CS_POSITION_KEYWORDS:
        if kw.lower() in job_name:
            return True
    
    # 方式2: 行业是IT类 + 岗位描述包含技术关键词
    is_it_industry = any(ind.lower() in industry for ind in CS_INDUSTRY_KEYWORDS)
    if is_it_industry:
        tech_keywords = ['开发', '编程', '代码', '软件', '系统', '技术', '程序', 
                        'java', 'python', 'c++', '数据库', '服务器', 'web', 'api']
        has_tech_desc = any(tk in job_desc for tk in tech_keywords)
        if has_tech_desc:
            return True
    
    return False


def clean_job_data(job: dict) -> dict:
    """清洗和标准化岗位数据"""
    return {
        'id': job.get('岗位编码', ''),
        'position_name': job.get('岗位名称', '').strip(),
        'location': job.get('地址', '').strip(),
        'salary_range': job.get('薪资范围', '').strip(),
        'company_name': job.get('公司名称', '').strip(),
        'industry': job.get('所属行业', '').strip(),
        'company_size': job.get('公司规模', '').strip(),
        'company_type': job.get('公司类型', '').strip(),
        'job_description': job.get('岗位详情', '').strip().replace('<br>', '\n'),
        'update_date': job.get('更新日期', '').strip(),
        'company_description': job.get('公司详情', '').strip(),
        'source_url': job.get('岗位来源地址', '').strip(),
    }


def extract_text_for_embedding(job: dict) -> str:
    """提取用于向量化的文本"""
    parts = [
        f"岗位名称: {job['position_name']}",
        f"公司: {job['company_name']}",
        f"行业: {job['industry']}",
        f"地点: {job['location']}",
        f"薪资: {job['salary_range']}",
        f"岗位职责: {job['job_description'][:500] if job['job_description'] else '无'}",
    ]
    return '\n'.join(parts)


def main():
    print("=" * 60)
    print("知识库生成脚本 - 计算机类岗位筛选与向量化")
    print("=" * 60)
    
    # 1. 加载原始数据
    input_path = Path(r'E:\work\Luvoy\tableConvert.com_pn6idf.json')
    print(f"\n[1/4] 加载原始数据: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        raw_jobs = json.load(f)
    print(f"原始岗位数量: {len(raw_jobs)}")
    
    # 2. 筛选计算机类岗位
    print(f"\n[2/4] 筛选计算机类岗位...")
    cs_jobs = []
    for job in raw_jobs:
        if is_cs_related(job):
            cleaned = clean_job_data(job)
            cs_jobs.append(cleaned)
    
    print(f"筛选后计算机类岗位数量: {len(cs_jobs)}")
    print(f"筛选比例: {len(cs_jobs)/len(raw_jobs)*100:.1f}%")
    
    # 3. 向量化处理
    print(f"\n[3/4] 向量化处理...")
    try:
        from sentence_transformers import SentenceTransformer
        print("加载向量化模型: paraphrase-multilingual-MiniLM-L12-v2")
        model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        
        # 批量提取文本并向量化
        texts = [extract_text_for_embedding(job) for job in cs_jobs]
        print(f"开始向量化 {len(texts)} 条文本...")
        
        embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)
        print(f"向量维度: {embeddings.shape[1]}")
        
        # 添加向量到每个岗位
        for i, job in enumerate(cs_jobs):
            job['embedding'] = embeddings[i].tolist()
            job['embedding_text'] = texts[i]  # 保存用于生成向量的文本
        
        has_embeddings = True
        print("向量化完成!")
        
    except ImportError:
        print("警告: sentence-transformers 未安装，跳过向量化")
        print("请运行: pip install sentence-transformers")
        has_embeddings = False
    except Exception as e:
        print(f"向量化出错: {e}")
        has_embeddings = False
    
    # 4. 生成知识库JSON
    print(f"\n[4/4] 生成知识库文件...")
    
    knowledge_base = {
        'metadata': {
            'version': '1.0',
            'description': '计算机类岗位知识库 - Luvoy项目',
            'source': 'tableConvert.com_pn6idf.json',
            'total_jobs': len(cs_jobs),
            'has_embeddings': has_embeddings,
            'embedding_model': 'paraphrase-multilingual-MiniLM-L12-v2' if has_embeddings else None,
            'embedding_dim': 384 if has_embeddings else None,
            'filter_keywords': CS_POSITION_KEYWORDS[:20],  # 部分关键词示例
        },
        'jobs': cs_jobs,
    }
    
    # 输出路径
    output_path = Path(r'E:\work\Luvoy\knowledge_base.json')
    print(f"输出文件: {output_path}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(knowledge_base, f, ensure_ascii=False, indent=2)
    
    file_size = output_path.stat().st_size / (1024 * 1024)
    print(f"文件大小: {file_size:.2f} MB")
    
    # 统计信息
    print("\n" + "=" * 60)
    print("知识库生成完成!")
    print("=" * 60)
    print(f"- 原始岗位数: {len(raw_jobs)}")
    print(f"- 计算机类岗位数: {len(cs_jobs)}")
    print(f"- 包含向量: {'是' if has_embeddings else '否'}")
    print(f"- 输出文件: {output_path}")
    
    # 显示示例岗位
    print("\n前5个筛选出的岗位:")
    for i, job in enumerate(cs_jobs[:5], 1):
        print(f"  {i}. {job['position_name']} - {job['company_name']} ({job['salary_range']})")


if __name__ == '__main__':
    main()

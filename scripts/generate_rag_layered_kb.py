"""
RAG知识库生成脚本 - 按照知识库分层设计生成
包含：JD库、高分样本库、术语模板库、ATS规则库
"""

import json
import re
from pathlib import Path
from datetime import datetime

def extract_skills_from_jd(job_desc: str) -> dict:
    """从岗位描述中提取技能要求"""
    # 技术技能关键词
    tech_skills = {
        'languages': ['java', 'python', 'c++', 'c#', 'javascript', 'typescript', 'go', 'rust', 'php', 'ruby', 'kotlin', 'swift'],
        'frontend': ['vue', 'react', 'angular', 'html', 'css', 'webpack', 'vite', '小程序', 'uniapp', 'flutter'],
        'backend': ['spring', 'springboot', 'mybatis', 'django', 'flask', 'fastapi', 'nodejs', 'express', 'gin'],
        'database': ['mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sql server', 'elasticsearch'],
        'devops': ['docker', 'kubernetes', 'k8s', 'jenkins', 'git', 'linux', 'nginx', 'aws', '阿里云', '腾讯云'],
        'ai_ml': ['机器学习', '深度学习', 'tensorflow', 'pytorch', 'nlp', '自然语言', '计算机视觉', 'opencv'],
        'bigdata': ['hadoop', 'spark', 'flink', 'hive', 'kafka', 'presto', '数据仓库', 'etl'],
    }
    
    job_desc_lower = job_desc.lower()
    found_skills = {}
    
    for category, skills in tech_skills.items():
        found = [s for s in skills if s.lower() in job_desc_lower]
        if found:
            found_skills[category] = found
    
    return found_skills


def extract_requirements(job_desc: str) -> dict:
    """提取岗位要求"""
    requirements = {
        'education': None,
        'experience_years': None,
        'soft_skills': [],
        'bonus_items': []
    }
    
    # 学历要求
    edu_patterns = ['博士', '硕士', '本科', '大专', '专科', '学士']
    for edu in edu_patterns:
        if edu in job_desc:
            requirements['education'] = edu
            break
    
    # 工作年限
    exp_match = re.search(r'(\d+)[年\-~到至]+(\d+)?年?[以上]?工作经验|(\d+)年以上', job_desc)
    if exp_match:
        years = exp_match.group(1) or exp_match.group(3)
        requirements['experience_years'] = years
    
    # 软技能
    soft_skills = ['沟通能力', '团队合作', '抗压能力', '学习能力', '责任心', '主动性', '创新能力']
    requirements['soft_skills'] = [s for s in soft_skills if s in job_desc]
    
    # 加分项
    bonus_keywords = ['优先', '加分', '优先考虑', '者优先']
    for kw in bonus_keywords:
        if kw in job_desc:
            # 提取加分项上下文
            idx = job_desc.find(kw)
            context = job_desc[max(0, idx-50):idx+20]
            requirements['bonus_items'].append(context.strip())
    
    return requirements


def build_jd_library(jobs_data: list) -> list:
    """构建JD库：岗位职责、硬技能、加分项"""
    jd_library = []
    
    for job in jobs_data:
        jd_entry = {
            'id': job.get('id', ''),
            'position_name': job.get('position_name', ''),
            'industry': job.get('industry', ''),
            'location': job.get('location', ''),
            'salary_range': job.get('salary_range', ''),
            
            # 提取的结构化信息
            'tech_skills': extract_skills_from_jd(job.get('job_description', '')),
            'requirements': extract_requirements(job.get('job_description', '')),
            
            # 原始描述（截断）
            'job_description': job.get('job_description', '')[:500],
        }
        jd_library.append(jd_entry)
    
    return jd_library


def build_sample_library() -> list:
    """构建高分样本库：优质简历段落模板（脱敏）"""
    samples = [
        # 项目经历模板
        {
            'id': 'sample_project_001',
            'category': '项目经历',
            'position_type': '后端开发',
            'content': '''项目名称：电商平台订单系统优化
技术栈：Java、Spring Boot、MySQL、Redis、Kafka
项目描述：负责订单系统核心模块的性能优化与重构
主要成果：
- 通过引入Redis缓存，将订单查询QPS从500提升至3000，响应时间降低80%
- 设计并实现分布式锁机制，解决高并发场景下的库存超卖问题
- 优化数据库索引和SQL查询，慢查询数量减少95%
- 主导系统重构，代码可维护性评分从C提升至A''',
            'highlights': ['量化成果', '技术栈明确', '问题-解决-结果结构'],
        },
        {
            'id': 'sample_project_002',
            'category': '项目经历',
            'position_type': '前端开发',
            'content': '''项目名称：企业级中后台管理系统
技术栈：Vue3、TypeScript、Element Plus、Vite、Pinia
项目描述：从0到1搭建公司内部管理系统前端架构
主要成果：
- 设计并实现基于RBAC的动态路由权限系统，支持5种角色10+权限组合
- 封装20+通用业务组件，代码复用率提升60%
- 优化首屏加载性能，FCP从4.2s降至1.8s（Lighthouse评分85→95）
- 制定前端代码规范，通过ESLint+Prettier保证团队代码质量''',
            'highlights': ['架构设计能力', '性能优化数据', '团队贡献'],
        },
        {
            'id': 'sample_project_003',
            'category': '项目经历',
            'position_type': '数据分析',
            'content': '''项目名称：用户行为分析与推荐系统
技术栈：Python、Spark、Hive、TensorFlow、Tableau
项目描述：负责用户画像构建与个性化推荐算法开发
主要成果：
- 处理日均5000万条用户行为数据，构建200+维度用户画像
- 设计并实现协同过滤+深度学习混合推荐算法，点击率提升35%
- 搭建AB测试平台，支持20+并行实验，决策周期缩短50%
- 输出10+数据分析报告，驱动产品迭代3个版本''',
            'highlights': ['数据规模', '业务指标提升', '商业价值'],
        },
        # 自我评价模板
        {
            'id': 'sample_summary_001',
            'category': '自我评价',
            'position_type': '通用',
            'content': '''5年Java后端开发经验，熟悉Spring生态和微服务架构。曾主导完成日活百万级系统的架构设计与性能优化。具备良好的系统设计能力和问题定位能力，善于将复杂业务抽象为可扩展的技术方案。热爱技术，保持学习，近期在深入研究分布式事务和云原生技术。''',
            'highlights': ['经验年限', '技术栈', '亮点成果', '学习态度'],
        },
        {
            'id': 'sample_summary_002',
            'category': '自我评价',
            'position_type': '应届生',
            'content': '''计算机专业应届硕士，研究方向为自然语言处理。在校期间发表1篇CCF-B论文，参与2项国家级科研项目。具有扎实的编程基础（Python/Java），熟悉深度学习框架（PyTorch/TensorFlow）。实习期间独立完成文本分类模型优化，准确率提升8%。学习能力强，对技术充满热情。''',
            'highlights': ['学术成果', '实习经历', '技术基础', '学习能力'],
        },
        # 实习经历模板
        {
            'id': 'sample_intern_001',
            'category': '实习经历',
            'position_type': '后端实习',
            'content': '''公司：某互联网大厂
岗位：后端开发实习生
时间：2023.06-2023.09（3个月）
工作内容：
- 参与用户中心服务开发，负责用户标签模块的接口设计与实现
- 编写单元测试100+，代码覆盖率达到85%
- 协助排查线上问题3次，定位并修复内存泄漏Bug
- 参与Code Review，输出技术分享1次''',
            'highlights': ['具体工作', '量化贡献', '学习成长'],
        },
    ]
    return samples


def build_template_library() -> list:
    """构建术语模板库：STAR表达、量化动词模板"""
    templates = [
        # STAR模板
        {
            'id': 'star_template',
            'category': 'STAR表达法',
            'description': 'Situation-Task-Action-Result 结构化表达',
            'structure': {
                'Situation': '项目背景/问题场景',
                'Task': '承担的任务/目标',
                'Action': '采取的行动/方法',
                'Result': '取得的成果（量化）'
            },
            'example': '''【背景】公司订单系统在双11大促期间频繁出现超时，影响用户体验
【任务】作为核心开发，负责识别瓶颈并优化系统性能
【行动】通过链路追踪定位慢接口，引入Redis缓存热点数据，优化数据库索引
【结果】系统QPS从500提升至3000，P99延迟从800ms降至150ms，大促期间零故障'''
        },
        # 量化动词
        {
            'id': 'action_verbs',
            'category': '量化动词',
            'description': '简历中常用的强动词，突出主动性和贡献',
            'verbs': {
                '领导类': ['主导', '负责', '牵头', '统筹', '推动', '带领'],
                '开发类': ['设计', '实现', '开发', '搭建', '构建', '编写'],
                '优化类': ['优化', '重构', '改进', '提升', '升级', '迁移'],
                '分析类': ['分析', '调研', '评估', '定位', '诊断', '排查'],
                '协作类': ['协调', '对接', '配合', '支持', '参与', '贡献'],
            }
        },
        # 成果量化模板
        {
            'id': 'quantify_templates',
            'category': '成果量化表达',
            'description': '用数字说话，让成果可衡量',
            'patterns': [
                '性能提升：从{before}提升至{after}，提升{percent}%',
                '效率优化：{metric}从{before}降至{after}',
                '规模数据：处理{volume}数据/请求/用户',
                '覆盖范围：支持{count}个{object}',
                '质量指标：{metric}达到{value}%',
                '时间节省：{task}周期从{before}缩短至{after}',
            ],
            'examples': [
                '系统响应时间从800ms优化至150ms，提升80%',
                '代码覆盖率从60%提升至90%',
                '日处理数据量5000万条',
                '封装20+通用组件，复用率提升60%',
            ]
        },
        # 技能描述模板
        {
            'id': 'skill_templates',
            'category': '技能描述',
            'description': '技能熟练度表达',
            'levels': {
                '精通': '深入理解原理，能解决复杂问题，有生产环境实践',
                '熟练': '能独立完成开发任务，有项目经验',
                '熟悉': '了解基本用法，能在指导下使用',
                '了解': '学习过基础知识，有简单实践',
            },
            'example': '''- 精通Java，深入理解JVM原理，有性能调优经验
- 熟练使用Spring Boot、MyBatis等主流框架
- 熟悉MySQL，有SQL优化和索引设计经验
- 了解Kubernetes，能进行基本的容器部署'''
        },
    ]
    return templates


def build_ats_rules() -> list:
    """构建ATS规则库：简历规范和优化建议"""
    rules = [
        # 格式规范
        {
            'id': 'format_001',
            'category': '格式规范',
            'rule': '简历长度',
            'description': '应届生1页，有经验者不超过2页',
            'reason': 'HR平均浏览简历时间仅6-10秒，信息需精炼',
            'check_points': ['总页数', '信息密度', '留白比例'],
        },
        {
            'id': 'format_002',
            'category': '格式规范',
            'rule': '文件格式',
            'description': '优先使用PDF格式，确保跨平台显示一致',
            'reason': 'Word文档可能因版本差异导致排版错乱',
            'check_points': ['文件格式', '文件大小<5MB', '可复制文本'],
        },
        # 关键词覆盖
        {
            'id': 'keyword_001',
            'category': '关键词覆盖',
            'rule': 'JD关键词匹配',
            'description': '简历中应包含JD中的核心技术关键词',
            'reason': 'ATS系统通过关键词匹配筛选简历',
            'check_points': ['技术栈匹配度', '技能关键词覆盖率', '岗位相关度'],
            'suggestion': '建议覆盖JD中80%以上的技术关键词',
        },
        {
            'id': 'keyword_002',
            'category': '关键词覆盖',
            'rule': '避免只用缩写',
            'description': '技术名词首次出现时写全称，如"Natural Language Processing (NLP)"',
            'reason': 'ATS可能无法识别所有缩写',
            'check_points': ['缩写使用', '术语规范性'],
        },
        # 内容规范
        {
            'id': 'content_001',
            'category': '内容规范',
            'rule': '成果量化',
            'description': '每个项目至少包含2-3个量化成果',
            'reason': '数字比描述更有说服力，便于面试官评估',
            'check_points': ['数字出现频率', '百分比/倍数表达', '规模指标'],
            'bad_example': '优化了系统性能',
            'good_example': '将系统响应时间从800ms优化至150ms，QPS提升5倍',
        },
        {
            'id': 'content_002',
            'category': '内容规范',
            'rule': '避免主观描述',
            'description': '用事实和数据代替"优秀"、"很好"等主观词汇',
            'reason': '主观描述无法验证，客观数据更有说服力',
            'check_points': ['主观词汇数量', '事实依据'],
            'bad_example': '具有优秀的编程能力',
            'good_example': 'LeetCode完成500+题目，周赛最高排名前5%',
        },
        # 结构规范
        {
            'id': 'structure_001',
            'category': '结构规范',
            'rule': '信息层次',
            'description': '按重要性排序：联系方式 → 教育背景 → 工作/项目经历 → 技能',
            'reason': '确保核心信息在第一眼被看到',
            'check_points': ['信息顺序', '模块完整性', '重点突出'],
        },
        {
            'id': 'structure_002',
            'category': '结构规范',
            'rule': '时间倒序',
            'description': '经历按时间倒序排列，最新的在最前',
            'reason': '最近的经历最能代表当前能力',
            'check_points': ['时间顺序', '日期格式统一'],
        },
    ]
    return rules


def main():
    print("=" * 60)
    print("RAG知识库生成 - 分层设计版")
    print("JD库 | 高分样本库 | 术语模板库 | ATS规则库")
    print("=" * 60)
    
    # 1. 加载已筛选的职位数据
    jobs_path = Path(r'E:\work\Luvoy\knowledge_base.json')
    print(f"\n[1/5] 加载职位数据: {jobs_path}")
    
    with open(jobs_path, 'r', encoding='utf-8') as f:
        jobs_data = json.load(f)
    
    jobs = jobs_data.get('jobs', [])
    print(f"职位数量: {len(jobs)}")
    
    # 2. 构建JD库
    print(f"\n[2/5] 构建JD库...")
    jd_library = build_jd_library(jobs)
    print(f"JD条目数: {len(jd_library)}")
    
    # 统计技能分布
    skill_stats = {}
    for jd in jd_library:
        for category, skills in jd['tech_skills'].items():
            skill_stats[category] = skill_stats.get(category, 0) + len(skills)
    print("技能类别分布:", dict(sorted(skill_stats.items(), key=lambda x: -x[1])[:5]))
    
    # 3. 构建高分样本库
    print(f"\n[3/5] 构建高分样本库...")
    sample_library = build_sample_library()
    print(f"样本数: {len(sample_library)}")
    
    # 4. 构建术语模板库
    print(f"\n[4/5] 构建术语模板库...")
    template_library = build_template_library()
    print(f"模板数: {len(template_library)}")
    
    # 5. 构建ATS规则库
    print(f"\n[5/5] 构建ATS规则库...")
    ats_rules = build_ats_rules()
    print(f"规则数: {len(ats_rules)}")
    
    # 向量化
    print(f"\n[向量化处理]...")
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        
        # JD库向量化
        jd_texts = [f"{jd['position_name']} {jd['industry']} {jd['job_description']}" for jd in jd_library]
        jd_embeddings = model.encode(jd_texts, show_progress_bar=True, batch_size=32)
        for i, jd in enumerate(jd_library):
            jd['embedding'] = jd_embeddings[i].tolist()
        
        # 样本库向量化
        sample_texts = [f"{s['category']} {s['position_type']} {s['content']}" for s in sample_library]
        sample_embeddings = model.encode(sample_texts)
        for i, s in enumerate(sample_library):
            s['embedding'] = sample_embeddings[i].tolist()
        
        has_embeddings = True
        print("向量化完成!")
    except Exception as e:
        print(f"向量化出错: {e}")
        has_embeddings = False
    
    # 组装完整知识库
    knowledge_base = {
        'metadata': {
            'version': '2.0',
            'description': 'RAG分层知识库 - Luvoy项目',
            'created_at': datetime.now().isoformat(),
            'has_embeddings': has_embeddings,
            'embedding_model': 'paraphrase-multilingual-MiniLM-L12-v2' if has_embeddings else None,
            'embedding_dim': 384 if has_embeddings else None,
            'statistics': {
                'jd_count': len(jd_library),
                'sample_count': len(sample_library),
                'template_count': len(template_library),
                'ats_rule_count': len(ats_rules),
            }
        },
        'libraries': {
            'jd_library': jd_library,              # JD库：岗位职责、硬技能、加分项
            'sample_library': sample_library,      # 高分样本库：优质简历段落
            'template_library': template_library,  # 术语模板库：STAR表达、量化动词
            'ats_rules': ats_rules,                # ATS规则库：简历规范
        }
    }
    
    # 输出
    output_path = Path(r'E:\work\Luvoy\rag_knowledge_base.json')
    print(f"\n输出文件: {output_path}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(knowledge_base, f, ensure_ascii=False, indent=2)
    
    file_size = output_path.stat().st_size / (1024 * 1024)
    print(f"文件大小: {file_size:.2f} MB")
    
    print("\n" + "=" * 60)
    print("RAG分层知识库生成完成!")
    print("=" * 60)
    print(f"- JD库: {len(jd_library)} 条（岗位职责、技能要求）")
    print(f"- 高分样本库: {len(sample_library)} 条（优质简历段落模板）")
    print(f"- 术语模板库: {len(template_library)} 条（STAR表达、量化动词）")
    print(f"- ATS规则库: {len(ats_rules)} 条（简历规范检查）")


if __name__ == '__main__':
    main()

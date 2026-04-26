"""
知识库整合脚本
将职位知识库和RAG分层知识库合并为统一的知识库文件
"""

import json
from pathlib import Path
from datetime import datetime


def main():
    print("=" * 60)
    print("知识库整合 - 合并为统一格式")
    print("=" * 60)
    
    # 1. 加载职位知识库
    jobs_path = Path(r'E:\work\Luvoy\knowledge_base.json')
    print(f"\n[1/3] 加载职位知识库: {jobs_path}")
    
    with open(jobs_path, 'r', encoding='utf-8') as f:
        jobs_kb = json.load(f)
    
    jobs = jobs_kb.get('jobs', [])
    print(f"职位数量: {len(jobs)}")
    
    # 2. 加载RAG分层知识库
    rag_path = Path(r'E:\work\Luvoy\rag_knowledge_base.json')
    print(f"\n[2/3] 加载RAG分层知识库: {rag_path}")
    
    with open(rag_path, 'r', encoding='utf-8') as f:
        rag_kb = json.load(f)
    
    libraries = rag_kb.get('libraries', {})
    jd_library = libraries.get('jd_library', [])
    sample_library = libraries.get('sample_library', [])
    template_library = libraries.get('template_library', [])
    ats_rules = libraries.get('ats_rules', [])
    
    print(f"JD库条目: {len(jd_library)}")
    print(f"高分样本: {len(sample_library)}")
    print(f"术语模板: {len(template_library)}")
    print(f"ATS规则: {len(ats_rules)}")
    
    # 3. 整合为统一知识库
    print(f"\n[3/3] 整合知识库...")
    
    unified_kb = {
        'metadata': {
            'version': '3.0',
            'description': '统一知识库 - Luvoy职业规划系统',
            'created_at': datetime.now().isoformat(),
            'source': {
                'jobs_file': 'tableConvert.com_pn6idf.json',
                'original_jobs_count': 9958,
                'filtered_cs_jobs_count': len(jobs),
            },
            'embedding': {
                'model': 'paraphrase-multilingual-MiniLM-L12-v2',
                'dimension': 384,
                'has_embeddings': True,
            },
            'statistics': {
                'total_jobs': len(jobs),
                'jd_library_count': len(jd_library),
                'sample_count': len(sample_library),
                'template_count': len(template_library),
                'ats_rule_count': len(ats_rules),
            }
        },
        
        # 职位数据（原始格式，包含完整信息）
        'jobs': jobs,
        
        # RAG知识库分层
        'rag_libraries': {
            # JD库：从职位中提取的结构化技能要求
            'jd_library': {
                'description': 'JD库：岗位职责、硬技能、加分项',
                'usage': '用于简历与岗位的技能匹配',
                'items': jd_library,
            },
            
            # 高分样本库：优质简历段落模板
            'sample_library': {
                'description': '高分样本库：优质简历段落（脱敏）',
                'usage': '用于简历撰写参考和质量评估',
                'items': sample_library,
            },
            
            # 术语模板库：STAR表达、量化动词
            'template_library': {
                'description': '术语模板库：STAR表达、量化动词模板',
                'usage': '用于简历表达优化',
                'items': template_library,
            },
            
            # ATS规则库：简历规范
            'ats_rules': {
                'description': 'ATS规则库：长度、关键词覆盖、结构规范',
                'usage': '用于简历格式检查和优化建议',
                'items': ats_rules,
            },
        },
    }
    
    # 输出整合后的知识库
    output_path = Path(r'E:\work\Luvoy\unified_knowledge_base.json')
    print(f"\n输出文件: {output_path}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(unified_kb, f, ensure_ascii=False, indent=2)
    
    file_size = output_path.stat().st_size / (1024 * 1024)
    print(f"文件大小: {file_size:.2f} MB")
    
    # 同时生成一个精简版（不含向量，便于查看）
    print("\n生成精简版（无向量，便于查看）...")
    
    # 移除向量以减小文件体积
    slim_kb = {
        'metadata': unified_kb['metadata'].copy(),
        'jobs_preview': [],  # 只保留前10条作为预览
        'rag_libraries': {
            'jd_library': {
                'description': '岗位职责、硬技能、加分项',
                'count': len(jd_library),
                'sample': [],  # 前3条样例
            },
            'sample_library': {
                'description': '优质简历段落模板',
                'items': [],  # 不含向量的完整内容
            },
            'template_library': {
                'description': 'STAR表达、量化动词模板',
                'items': template_library,  # 模板没有向量，保持原样
            },
            'ats_rules': {
                'description': 'ATS简历规范检查',
                'items': ats_rules,  # 规则没有向量，保持原样
            },
        }
    }
    
    slim_kb['metadata']['embedding']['has_embeddings'] = False
    slim_kb['metadata']['description'] += ' (精简版-无向量)'
    
    # 添加预览数据
    for job in jobs[:10]:
        preview = {k: v for k, v in job.items() if k != 'embedding'}
        slim_kb['jobs_preview'].append(preview)
    
    for jd in jd_library[:3]:
        preview = {k: v for k, v in jd.items() if k != 'embedding'}
        slim_kb['rag_libraries']['jd_library']['sample'].append(preview)
    
    for sample in sample_library:
        preview = {k: v for k, v in sample.items() if k != 'embedding'}
        slim_kb['rag_libraries']['sample_library']['items'].append(preview)
    
    slim_path = Path(r'E:\work\Luvoy\unified_knowledge_base_slim.json')
    with open(slim_path, 'w', encoding='utf-8') as f:
        json.dump(slim_kb, f, ensure_ascii=False, indent=2)
    
    slim_size = slim_path.stat().st_size / 1024
    print(f"精简版文件: {slim_path}")
    print(f"精简版大小: {slim_size:.2f} KB")
    
    print("\n" + "=" * 60)
    print("知识库整合完成!")
    print("=" * 60)
    print(f"\n📁 完整版: {output_path} ({file_size:.2f} MB)")
    print(f"📁 精简版: {slim_path} ({slim_size:.2f} KB)")
    print("\n完整版结构:")
    print("├── metadata          # 元数据")
    print("├── jobs              # 2626个计算机类岗位（含384维向量）")
    print("└── rag_libraries     # RAG分层知识库")
    print("    ├── jd_library    # JD库（岗位技能提取）")
    print("    ├── sample_library# 高分样本库")
    print("    ├── template_library # 术语模板库")
    print("    └── ats_rules     # ATS规则库")


if __name__ == '__main__':
    main()

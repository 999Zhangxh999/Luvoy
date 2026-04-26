"""
RAG技术知识库生成脚本
功能：将微调与RAG技术方案文档转换为结构化知识库
"""

import json
from pathlib import Path
from datetime import datetime

def parse_markdown_to_chunks(content: str) -> list:
    """将Markdown内容解析为语义分块"""
    chunks = []
    lines = content.split('\n')
    
    current_section = ""
    current_subsection = ""
    current_content = []
    
    for line in lines:
        # 检测一级标题
        if line.startswith('## '):
            # 保存之前的内容
            if current_content:
                chunk_text = '\n'.join(current_content).strip()
                if chunk_text and len(chunk_text) > 50:
                    chunks.append({
                        'section': current_section,
                        'subsection': current_subsection,
                        'content': chunk_text,
                        'type': 'section'
                    })
            current_section = line[3:].strip()
            current_subsection = ""
            current_content = []
        
        # 检测二级标题
        elif line.startswith('### '):
            # 保存之前的内容
            if current_content:
                chunk_text = '\n'.join(current_content).strip()
                if chunk_text and len(chunk_text) > 50:
                    chunks.append({
                        'section': current_section,
                        'subsection': current_subsection,
                        'content': chunk_text,
                        'type': 'subsection'
                    })
            current_subsection = line[4:].strip()
            current_content = []
        
        else:
            current_content.append(line)
    
    # 保存最后一块
    if current_content:
        chunk_text = '\n'.join(current_content).strip()
        if chunk_text and len(chunk_text) > 50:
            chunks.append({
                'section': current_section,
                'subsection': current_subsection,
                'content': chunk_text,
                'type': 'section'
            })
    
    return chunks


def main():
    print("=" * 60)
    print("RAG技术知识库生成")
    print("=" * 60)
    
    # 读取技术方案文档
    input_path = Path(r'C:\Users\91146\Downloads\微调与RAG (1).md')
    print(f"\n[1/3] 读取技术文档: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析为分块
    print(f"\n[2/3] 解析文档结构...")
    chunks = parse_markdown_to_chunks(content)
    print(f"提取知识块数量: {len(chunks)}")
    
    # 向量化
    print(f"\n[3/3] 向量化处理...")
    try:
        from sentence_transformers import SentenceTransformer
        print("加载向量化模型...")
        model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        
        # 构建向量化文本
        texts = []
        for i, chunk in enumerate(chunks):
            text = f"章节: {chunk['section']}\n"
            if chunk['subsection']:
                text += f"子章节: {chunk['subsection']}\n"
            text += f"内容: {chunk['content']}"
            texts.append(text)
            chunk['embedding_text'] = text
        
        embeddings = model.encode(texts, show_progress_bar=True)
        print(f"向量维度: {embeddings.shape[1]}")
        
        for i, chunk in enumerate(chunks):
            chunk['embedding'] = embeddings[i].tolist()
            chunk['id'] = f"rag_doc_{i+1}"
        
        has_embeddings = True
    except Exception as e:
        print(f"向量化出错: {e}")
        has_embeddings = False
        for i, chunk in enumerate(chunks):
            chunk['id'] = f"rag_doc_{i+1}"
    
    # 生成知识库
    knowledge_base = {
        'metadata': {
            'version': '1.0',
            'description': 'RAG与微调技术方案知识库 - Luvoy项目',
            'source': '微调与RAG (1).md',
            'total_chunks': len(chunks),
            'has_embeddings': has_embeddings,
            'embedding_model': 'paraphrase-multilingual-MiniLM-L12-v2' if has_embeddings else None,
            'embedding_dim': 384 if has_embeddings else None,
            'created_at': datetime.now().isoformat(),
        },
        'documents': chunks,
    }
    
    output_path = Path(r'E:\work\Luvoy\rag_knowledge_base.json')
    print(f"\n输出文件: {output_path}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(knowledge_base, f, ensure_ascii=False, indent=2)
    
    file_size = output_path.stat().st_size / 1024
    print(f"文件大小: {file_size:.2f} KB")
    
    print("\n" + "=" * 60)
    print("RAG知识库生成完成!")
    print("=" * 60)
    
    # 显示章节概览
    print("\n知识块章节分布:")
    sections = {}
    for chunk in chunks:
        sec = chunk['section'] or '(无章节)'
        sections[sec] = sections.get(sec, 0) + 1
    for sec, count in sections.items():
        print(f"  - {sec}: {count}块")


if __name__ == '__main__':
    main()

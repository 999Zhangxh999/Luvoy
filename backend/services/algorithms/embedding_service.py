# ============================================
# 嵌入表征服务 (Embedding & Representation Learning)
# 技术亮点：TF-IDF向量化 + 余弦相似度 + 共享嵌入空间
# ============================================
"""
核心算法说明：
1. TF-IDF (Term Frequency-Inverse Document Frequency)
   - 将文本转为高维稀疏向量，捕捉词汇重要性
   - 公式: TF-IDF(t,d) = TF(t,d) × log(N/DF(t))

2. 余弦相似度 (Cosine Similarity)  
   - 在高维向量空间中度量语义相似性
   - 公式: cos(θ) = (A·B) / (||A|| × ||B||)

3. 共享嵌入空间 (Shared Embedding Space)
   - 将学生画像和岗位画像映射到同一向量空间
   - 实现跨模态的语义匹配
"""
import json
import logging
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    嵌入表征服务 - 两阶段匹配的第一阶段：向量召回
    
    工作流程：
    1. fit_job_corpus(): 对岗位库构建TF-IDF向量索引
    2. compute_student_similarity(): 计算学生与所有岗位的相似度
    3. 返回Top-K候选岗位，交给LLM做精细评估
    """

    def __init__(self):
        self._vectorizer = None
        self._corpus_vectors = None
        self._corpus_ids = []
        self._is_fitted = False

    def _normalize_text_items(self, items) -> list:
        """将技能/证书等字段安全转换为文本列表。"""
        if items is None:
            return []

        if isinstance(items, str):
            try:
                parsed = json.loads(items)
                if isinstance(parsed, list):
                    items = parsed
                else:
                    items = [items]
            except Exception:
                items = [items]

        if not isinstance(items, list):
            items = [items]

        normalized = []
        for item in items:
            if isinstance(item, dict):
                text = item.get('name') or item.get('skill') or item.get('title') or ''
                if not text:
                    text = str(item)
            else:
                text = str(item)

            text = text.strip()
            if text:
                normalized.append(text)
        return normalized

    def _build_profile_text(self, profile_dict: dict, profile_type: str = 'job') -> str:
        """
        将结构化画像转为富文本表示（特征工程核心）
        
        Args:
            profile_dict: 画像字典
            profile_type: 'job' 或 'student'
        Returns:
            str: 用于向量化的文本
        """
        parts = []

        if profile_type == 'job':
            parts.append(f"岗位：{profile_dict.get('position_name', '')}")
            parts.append(f"类别：{profile_dict.get('category', '')}")
            parts.append(f"层级：{profile_dict.get('level', '')}")
            parts.append(f"学历：{profile_dict.get('education_req', '')}")
            parts.append(f"经验：{profile_dict.get('experience_req', '')}")

            skills = self._normalize_text_items(profile_dict.get('technical_skills', []))
            if skills:
                parts.append(f"技能：{' '.join(skills)}")

            certs = self._normalize_text_items(profile_dict.get('certificates', []))
            if certs:
                parts.append(f"证书：{' '.join(certs)}")

            parts.append(f"描述：{profile_dict.get('summary', '')}")

        elif profile_type == 'student':
            parts.append(f"学历：{profile_dict.get('education', '')}")
            parts.append(f"专业：{profile_dict.get('major', '')}")
            parts.append(f"学校：{profile_dict.get('school', '')}")

            skills = profile_dict.get('technical_skills', [])
            if isinstance(skills, list):
                skill_names = []
                for s in skills:
                    if isinstance(s, dict):
                        skill_names.append(s.get('name', ''))
                    elif isinstance(s, str):
                        skill_names.append(s)
                parts.append(f"技能：{' '.join(skill_names)}")

            certs = profile_dict.get('certificates', [])
            if isinstance(certs, list):
                parts.append(f"证书：{' '.join(str(c) for c in certs)}")

            projects = profile_dict.get('project_experience', [])
            if isinstance(projects, list):
                for p in projects:
                    if isinstance(p, dict):
                        parts.append(f"项目：{p.get('name', '')} {p.get('description', '')}")

            internships = profile_dict.get('internship_experience', [])
            if isinstance(internships, list):
                for i in internships:
                    if isinstance(i, dict):
                        parts.append(f"实习：{i.get('position', '')} {i.get('description', '')}")

        return ' '.join(parts)

    def fit_job_corpus(self, job_profiles: list):
        """
        对岗位画像语料库进行 TF-IDF 拟合，构建向量索引
        
        Args:
            job_profiles: 岗位画像列表
        """
        corpus = []
        self._corpus_ids = []

        for jp in job_profiles:
            jp_dict = jp.to_dict() if hasattr(jp, 'to_dict') else jp
            text = self._build_profile_text(jp_dict, 'job')
            corpus.append(text)
            self._corpus_ids.append(jp_dict.get('id', 0))

        if not corpus:
            logger.warning("空语料库，无法拟合 TF-IDF")
            return

        # TF-IDF向量化器配置
        self._vectorizer = TfidfVectorizer(
            max_features=5000,       # 最大特征数
            ngram_range=(1, 2),      # unigram + bigram
            sublinear_tf=True,       # 对数词频平滑
            min_df=1,
            max_df=0.95,
            token_pattern=r'(?u)\b\w+\b',  # 支持中文
        )

        self._corpus_vectors = self._vectorizer.fit_transform(corpus)
        self._is_fitted = True
        logger.info(f"TF-IDF索引构建完成：{len(corpus)}个岗位，{self._corpus_vectors.shape[1]}维特征")

    def compute_student_similarity(self, student_profile_dict: dict, top_k: int = 20) -> list:
        """
        计算学生与所有岗位的余弦相似度，返回Top-K候选
        
        这是"两阶段匹配"的第一阶段：向量召回
        
        Args:
            student_profile_dict: 学生画像字典
            top_k: 返回前K个最相似岗位
        Returns:
            list[dict]: [{'job_profile_id': id, 'similarity': score}, ...]
        """
        if not self._is_fitted:
            logger.warning("TF-IDF尚未拟合")
            return []

        # 学生画像向量化
        student_text = self._build_profile_text(student_profile_dict, 'student')
        student_vector = self._vectorizer.transform([student_text])

        # 余弦相似度计算
        similarities = cosine_similarity(student_vector, self._corpus_vectors).flatten()

        # 取 Top-K
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                'job_profile_id': self._corpus_ids[idx],
                'similarity': round(float(similarities[idx]), 4),
                'rank': len(results) + 1,
            })

        logger.info(f"向量召回完成：Top-{top_k}，最高相似度={results[0]['similarity'] if results else 0}")
        return results

    def compute_skill_overlap(self, student_skills: list, job_skills: list) -> dict:
        """
        基于TF-IDF的技能匹配分析（精确匹配 + 语义模糊匹配）
        
        Returns:
            dict: {
                'exact_matches': [...],       # 精确匹配
                'semantic_matches': [...],    # 语义相似匹配
                'missing_skills': [...],      # 缺失技能
                'match_rate': float,          # 匹配率
            }
        """
        # 标准化处理
        student_skill_texts = self._normalize_text_items(student_skills)
        job_skill_texts = self._normalize_text_items(job_skills)

        s_set = set(s.lower().strip() for s in student_skill_texts if s)
        j_set = set(j.lower().strip() for j in job_skill_texts if j)

        exact_matches = list(s_set & j_set)

        # 语义匹配：用 TF-IDF 找近似技能
        semantic_matches = []
        unmatched_student = list(s_set - j_set)
        unmatched_job = list(j_set - s_set)

        if unmatched_student and unmatched_job:
            all_skills = unmatched_student + unmatched_job
            try:
                vectorizer = TfidfVectorizer(ngram_range=(1, 2), token_pattern=r'(?u)\b\w+\b')
                vectors = vectorizer.fit_transform(all_skills)

                n_student = len(unmatched_student)
                student_vecs = vectors[:n_student]
                job_vecs = vectors[n_student:]

                sim_matrix = cosine_similarity(student_vecs, job_vecs)

                matched_jobs = set()
                for i in range(n_student):
                    best_j = np.argmax(sim_matrix[i])
                    if sim_matrix[i][best_j] > 0.3 and best_j not in matched_jobs:
                        semantic_matches.append({
                            'student_skill': unmatched_student[i],
                            'job_skill': unmatched_job[best_j],
                            'similarity': round(float(sim_matrix[i][best_j]), 3),
                        })
                        matched_jobs.add(best_j)
            except Exception as e:
                logger.warning(f"语义技能匹配失败: {e}")

        # 缺失技能
        semantically_covered = set(m['job_skill'] for m in semantic_matches)
        missing = [s for s in unmatched_job if s not in semantically_covered]

        total_required = len(j_set) if j_set else 1
        total_matched = len(exact_matches) + len(semantic_matches)
        match_rate = round(total_matched / total_required, 4)

        return {
            'exact_matches': exact_matches,
            'semantic_matches': semantic_matches,
            'missing_skills': missing,
            'extra_skills': list(s_set - j_set - set(m['student_skill'] for m in semantic_matches)),
            'match_rate': match_rate,
        }

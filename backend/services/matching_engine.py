# ============================================
# 人岗匹配引擎（Agent 3）- 升级版 v2
# 技术亮点：
#   - 两阶段匹配（向量召回 + LLM精排）
#   - 深度语义嵌入（Sentence-BERT）
#   - AHP权重优化
#   - 贝叶斯超参数调优
#   - 集成学习多模型融合
#   - 技能本体标准化
# 维度: 基础要求 / 职业技能 / 职业素养 / 发展潜力
# ============================================
"""
两阶段匹配算法：
1. 第一阶段 - 向量召回 (Embedding Recall)
   - Sentence-BERT 深度语义嵌入（优先）
   - TF-IDF + 余弦相似度（降级方案）
   
2. 第二阶段 - LLM精排 (LLM Rerank)
   对候选岗位进行四维度深度分析，生成可解释评分

3. AHP权重优化
   根据岗位特性动态调整四维度权重

4. 贝叶斯权重自动调优
   使用高斯过程寻找最优权重配置

5. 集成学习融合
   多种匹配算法结果的加权融合

6. 技能本体标准化
   统一技能名称，提高匹配准确率
"""
import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import current_app

from models.database import db
from models.job import JobProfile
from models.student import Student, StudentProfile, MatchResult
from services.llm_client import get_llm
from prompts.templates import MATCHING_SYSTEM, MATCHING_USER

# 导入基础算法服务
try:
    from services.algorithms.embedding_service import EmbeddingService
    from services.algorithms.ahp_service import AHPService
    from services.algorithms.skill_ontology import SkillOntologyService
    ADVANCED_ALGORITHMS_AVAILABLE = True
except ImportError:
    ADVANCED_ALGORITHMS_AVAILABLE = False

# 导入深度学习算法服务
try:
    from services.algorithms.semantic_embedding import SemanticEmbeddingService
    SEMANTIC_EMBEDDING_AVAILABLE = True
except ImportError:
    SEMANTIC_EMBEDDING_AVAILABLE = False

# 导入贝叶斯优化服务
try:
    from services.algorithms.bayesian_optimizer import BayesianOptimizer
    BAYESIAN_AVAILABLE = True
except ImportError:
    BAYESIAN_AVAILABLE = False

# 导入集成学习服务
try:
    from services.algorithms.ensemble_learning import EnsembleMatcher
    ENSEMBLE_AVAILABLE = True
except ImportError:
    ENSEMBLE_AVAILABLE = False

logger = logging.getLogger(__name__)


class MatchingEngine:
    """
    人岗匹配引擎 - 两阶段匹配 + 多算法融合
    
    算法流程：
    1. 向量召回：Sentence-BERT / TF-IDF 筛选 Top-K 候选
    2. 技能标准化：使用技能本体统一技能名称
    3. LLM精排：四维度深度分析
    4. 集成学习：多模型分数融合
    5. AHP重排序：动态权重优化最终排名
    6. 贝叶斯优化：权重自动调优（可选）
    """
    
    def __init__(self):
        """初始化匹配引擎及所有算法服务"""
        # 基础算法服务
        self.embedding_service = None      # TF-IDF向量召回
        self.ahp_service = None            # AHP权重优化
        self.skill_ontology = None         # 技能本体标准化
        
        # 高级算法服务
        self.semantic_embedding = None     # Sentence-BERT深度语义
        self.bayesian_optimizer = None     # 贝叶斯权重优化
        self.ensemble_matcher = None       # 集成学习融合
        
        self._init_advanced_services()
    
    def _init_advanced_services(self):
        """初始化所有算法服务"""
        # 初始化基础算法
        if ADVANCED_ALGORITHMS_AVAILABLE:
            try:
                self.embedding_service = EmbeddingService()
                self.ahp_service = AHPService()
                self.skill_ontology = SkillOntologyService()
                logger.info("基础算法服务初始化成功: Embedding/AHP/SkillOntology")
            except Exception as e:
                logger.warning(f"基础算法服务初始化失败: {e}")
        else:
            logger.info("基础算法服务不可用，使用LLM单阶段匹配")
        
        # 初始化深度语义嵌入
        enable_semantic = os.getenv('ENABLE_SEMANTIC_EMBEDDING', '0').lower() in ('1', 'true', 'yes')
        if SEMANTIC_EMBEDDING_AVAILABLE and enable_semantic:
            try:
                self.semantic_embedding = SemanticEmbeddingService(model_name='multilingual')
                logger.info("语义嵌入服务初始化成功: Sentence-BERT")
            except Exception as e:
                logger.warning(f"语义嵌入服务初始化失败: {e}")
        elif SEMANTIC_EMBEDDING_AVAILABLE and not enable_semantic:
            logger.info("语义嵌入服务默认关闭（设置 ENABLE_SEMANTIC_EMBEDDING=1 可开启）")
        
        # 初始化贝叶斯优化器
        if BAYESIAN_AVAILABLE:
            try:
                self.bayesian_optimizer = BayesianOptimizer(n_calls=30)
                logger.info("贝叶斯优化器初始化成功")
            except Exception as e:
                logger.warning(f"贝叶斯优化器初始化失败: {e}")
        
        # 初始化集成学习匹配器
        if ENSEMBLE_AVAILABLE:
            try:
                self.ensemble_matcher = EnsembleMatcher(fusion_method='weighted_average')
                # 注册各组件匹配器
                self.ensemble_matcher.register_component('llm_score', weight=0.4)
                self.ensemble_matcher.register_component('embedding_score', weight=0.3)
                self.ensemble_matcher.register_component('skill_score', weight=0.2)
                self.ensemble_matcher.register_component('ahp_score', weight=0.1)
                logger.info("集成学习匹配器初始化成功")
            except Exception as e:
                logger.warning(f"集成学习匹配器初始化失败: {e}")
    
    def _call_llm_for_match(self, sp_dict: dict, jp_dict: dict, weights: tuple) -> dict:
        """
        纯LLM调用，不涉及数据库操作（线程安全）
        
        Args:
            sp_dict: 学生画像字典
            jp_dict: 岗位画像字典
            weights: (weight_basic, weight_skill, weight_quality, weight_potential)
        Returns:
            dict: 匹配结果数据
        """
        llm = get_llm()

        messages = [
            {"role": "system", "content": MATCHING_SYSTEM},
            {"role": "user", "content": MATCHING_USER.format(
                student_profile=json.dumps(sp_dict, ensure_ascii=False, indent=2),
                job_profile=json.dumps(jp_dict, ensure_ascii=False, indent=2),
            )}
        ]

        try:
            result = llm.chat_json(messages, temperature=0.2)
        except Exception as e:
            logger.warning(f"LLM匹配调用失败，启用降级匹配: {e}")
            return self._build_fallback_match_result(sp_dict, jp_dict, weights, str(e))
        
        # 计算加权综合评分
        basic_score = result.get('basic_score', 50)
        skill_score = result.get('skill_score', 50)
        quality_score = result.get('quality_score', 50)
        potential_score = result.get('potential_score', 50)
        
        overall_score = (
            basic_score * weights[0] +
            skill_score * weights[1] +
            quality_score * weights[2] +
            potential_score * weights[3]
        )
        
        return {
            'basic_score': basic_score,
            'skill_score': skill_score,
            'quality_score': quality_score,
            'potential_score': potential_score,
            'overall_score': round(overall_score, 1),
            'detail_analysis': {
                'basic_analysis': result.get('basic_analysis', ''),
                'skill_analysis': result.get('skill_analysis', ''),
                'quality_analysis': result.get('quality_analysis', ''),
                'potential_analysis': result.get('potential_analysis', ''),
                'overall_analysis': result.get('overall_analysis', ''),
                'matched_skills': result.get('matched_skills', []),
                'missing_skills': result.get('missing_skills', []),
            },
            'skill_gaps': result.get('skill_gaps', []),
            'recommendations': result.get('recommendations', []),
        }

    def _normalize_skill_names(self, skills) -> list:
        if skills is None:
            return []
        if isinstance(skills, str):
            try:
                parsed = json.loads(skills)
                if isinstance(parsed, list):
                    skills = parsed
                else:
                    skills = [skills]
            except Exception:
                skills = [skills]
        if not isinstance(skills, list):
            skills = [skills]

        names = []
        for skill in skills:
            if isinstance(skill, dict):
                name = skill.get('name') or skill.get('skill') or ''
            else:
                name = str(skill)
            name = name.strip()
            if name:
                names.append(name)
        return names

    def _build_fallback_match_result(self, sp_dict: dict, jp_dict: dict, weights: tuple, reason: str) -> dict:
        """LLM不可用时的降级匹配结果，保证主流程不中断。"""
        student_skills = set(s.lower() for s in self._normalize_skill_names(sp_dict.get('technical_skills', [])))
        job_skills_raw = self._normalize_skill_names(jp_dict.get('technical_skills', []))
        job_skills = set(s.lower() for s in job_skills_raw)

        matched = sorted(list(student_skills & job_skills))
        missing = sorted(list(job_skills - student_skills))

        if job_skills:
            skill_score = round(len(matched) / len(job_skills) * 100, 1)
        else:
            skill_score = 60.0

        student_edu = (sp_dict.get('education') or '').strip()
        job_edu = (jp_dict.get('education_req') or '').strip()
        if not job_edu:
            basic_score = 70.0
        elif student_edu and student_edu in job_edu:
            basic_score = 85.0
        else:
            basic_score = 60.0

        quality_keys = ['communication_skill', 'teamwork_ability', 'pressure_resistance']
        potential_keys = ['learning_ability', 'innovation_ability', 'internship_ability']

        quality_vals = [float(sp_dict.get(k, 5) or 5) for k in quality_keys]
        potential_vals = [float(sp_dict.get(k, 5) or 5) for k in potential_keys]

        quality_score = round(sum(quality_vals) / len(quality_vals) * 10, 1)
        potential_score = round(sum(potential_vals) / len(potential_vals) * 10, 1)

        overall_score = round(
            basic_score * weights[0] +
            skill_score * weights[1] +
            quality_score * weights[2] +
            potential_score * weights[3],
            1
        )

        recommendations = []
        for s in missing[:3]:
            recommendations.append(f"优先补齐技能：{s}")
        if not recommendations:
            recommendations.append('当前技能与岗位要求较匹配，建议准备项目案例提升竞争力')

        return {
            'basic_score': basic_score,
            'skill_score': skill_score,
            'quality_score': quality_score,
            'potential_score': potential_score,
            'overall_score': overall_score,
            'detail_analysis': {
                'basic_analysis': 'LLM服务暂不可用，采用规则模型进行基础要求评估。',
                'skill_analysis': '基于技能交集计算匹配度。',
                'quality_analysis': '基于画像中的软技能字段进行估算。',
                'potential_analysis': '基于学习/创新/实践能力字段进行估算。',
                'overall_analysis': '当前结果为降级计算结果，可用于继续流程，建议稍后重试获取更精准AI分析。',
                'matched_skills': matched,
                'missing_skills': missing,
                'fallback_reason': reason,
            },
            'skill_gaps': missing,
            'recommendations': recommendations,
        }
    
    def match_student_to_job(self, student_id: int, job_profile_id: int) -> MatchResult:
        """
        对单个学生和岗位进行匹配分析
        
        Args:
            student_id: 学生ID
            job_profile_id: 岗位画像ID
        Returns:
            MatchResult: 匹配结果
        """
        student = Student.query.get(student_id)
        student_profile = StudentProfile.query.filter_by(student_id=student_id).first()
        job_profile = JobProfile.query.get(job_profile_id)
        
        if not student or not student_profile or not job_profile:
            raise ValueError("学生或岗位数据不存在")
        
        # 构建学生画像信息
        sp_dict = student_profile.to_dict()
        sp_dict['student_name'] = student.name
        sp_dict['education'] = student.education
        sp_dict['major'] = student.major
        sp_dict['school'] = student.school
        
        weights = (job_profile.weight_basic, job_profile.weight_skill, 
                   job_profile.weight_quality, job_profile.weight_potential)
        
        # 调用LLM
        result = self._call_llm_for_match(sp_dict, job_profile.to_dict(), weights)
        
        # 创建匹配结果
        match_result = MatchResult(
            student_id=student_id,
            job_profile_id=job_profile_id,
            basic_score=result['basic_score'],
            skill_score=result['skill_score'],
            quality_score=result['quality_score'],
            potential_score=result['potential_score'],
            overall_score=result['overall_score'],
            detail_analysis=json.dumps(result['detail_analysis'], ensure_ascii=False),
            skill_gaps=json.dumps(result['skill_gaps'], ensure_ascii=False),
            recommendations=json.dumps(result['recommendations'], ensure_ascii=False),
        )
        
        db.session.add(match_result)
        db.session.commit()
        
        logger.info(f"匹配完成: 学生[{student.name}] ↔ 岗位[{job_profile.position_name}], 综合得分={result['overall_score']:.1f}")
        return match_result
    
    def match_student_to_all_jobs(self, student_id: int, top_n: int = 5, max_workers: int = 5) -> list:
        """
        将学生与所有岗位画像进行匹配，返回TOP N结果
        使用多线程并行加速LLM调用
        
        Args:
            student_id: 学生ID
            top_n: 返回前N个匹配结果
            max_workers: 并行线程数（默认5，避免API限流）
        Returns:
            list[MatchResult]: 按匹配度排序的结果列表
        """
        # 1. 主线程读取所有数据
        student = Student.query.get(student_id)
        student_profile = StudentProfile.query.filter_by(student_id=student_id).first()
        profiles = self._get_unique_job_profiles()
        
        if not student or not student_profile:
            raise ValueError("学生数据不存在")
        
        if not profiles:
            logger.warning("没有可用的岗位画像进行匹配")
            return []
        
        # 清除该学生旧的匹配结果
        MatchResult.query.filter_by(student_id=student_id).delete()
        db.session.commit()
        
        # 构建学生画像（只读取一次）
        sp_dict = student_profile.to_dict()
        sp_dict['student_name'] = student.name
        sp_dict['education'] = student.education
        sp_dict['major'] = student.major
        sp_dict['school'] = student.school
        
        # 预提取岗位数据（避免在线程中访问数据库）
        job_data = []
        for p in profiles:
            job_data.append({
                'id': p.id,
                'name': p.position_name,
                'dict': p.to_dict(),
                'weights': (p.weight_basic, p.weight_skill, p.weight_quality, p.weight_potential)
            })
        
        total = len(job_data)
        completed = [0]  # 使用列表以便在闭包中修改
        llm_results = []
        
        def call_llm_task(job_info):
            """纯LLM调用任务（线程安全）"""
            try:
                result = self._call_llm_for_match(sp_dict, job_info['dict'], job_info['weights'])
                result['job_profile_id'] = job_info['id']
                result['job_name'] = job_info['name']
                completed[0] += 1
                logger.info(f"匹配进度: {completed[0]}/{total} - {job_info['name']}")
                return result
            except Exception as e:
                completed[0] += 1
                logger.error(f"匹配岗位[{job_info['name']}]失败: {e}")
                return None
        
        # 2. 并行调用LLM
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(call_llm_task, jd) for jd in job_data]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    llm_results.append(result)
        
        # 3. 主线程统一写入数据库
        db_results = []
        for res in llm_results:
            match_result = MatchResult(
                student_id=student_id,
                job_profile_id=res['job_profile_id'],
                basic_score=res['basic_score'],
                skill_score=res['skill_score'],
                quality_score=res['quality_score'],
                potential_score=res['potential_score'],
                overall_score=res['overall_score'],
                detail_analysis=json.dumps(res['detail_analysis'], ensure_ascii=False),
                skill_gaps=json.dumps(res['skill_gaps'], ensure_ascii=False),
                recommendations=json.dumps(res['recommendations'], ensure_ascii=False),
            )
            db.session.add(match_result)
            db_results.append(match_result)
        
        db.session.commit()
        logger.info(f"并行匹配完成，共 {len(db_results)} 个结果")
        
        # 按综合得分排序，返回TOP N
        db_results.sort(key=lambda r: r.overall_score, reverse=True)
        return db_results[:top_n]
    
    def get_match_results(self, student_id: int) -> list:
        """获取学生的所有匹配结果"""
        results = MatchResult.query.filter_by(
            student_id=student_id
        ).order_by(MatchResult.overall_score.desc()).all()
        
        enriched = []
        for r in results:
            data = r.to_dict()
            # 附加岗位信息
            job_profile = JobProfile.query.get(r.job_profile_id)
            if job_profile:
                data['job_name'] = job_profile.position_name
                data['job_category'] = job_profile.category
                data['job_level'] = job_profile.level
                data['job_salary'] = job_profile.salary_range
            enriched.append(data)
        
        return enriched
    
    def get_match_detail(self, match_id: int) -> dict:
        """获取单个匹配的详细结果"""
        result = MatchResult.query.get(match_id)
        if not result:
            return None
        
        data = result.to_dict()
        
        # 附加岗位和学生信息
        job_profile = JobProfile.query.get(result.job_profile_id)
        student = Student.query.get(result.student_id)
        
        if job_profile:
            data['job_profile'] = job_profile.to_dict()
        if student:
            data['student'] = student.to_dict()
        
        return data
    
    def _filter_by_target_positions(self, profiles: list, target_positions: list) -> tuple:
        """
        根据学生目标岗位过滤并排序岗位画像
        
        Args:
            profiles: 所有岗位画像
            target_positions: 学生目标岗位列表
        Returns:
            tuple: (优先匹配的岗位, 其他岗位)
        """
        if not target_positions:
            return [], profiles
        
        # 将目标岗位转为小写用于匹配
        target_keywords = [pos.lower().strip() for pos in target_positions if pos]
        
        priority_profiles = []
        other_profiles = []
        
        for profile in profiles:
            position_name = (profile.position_name or '').lower()
            category = (profile.category or '').lower()
            
            # 检查是否匹配目标岗位
            is_match = False
            for keyword in target_keywords:
                if keyword in position_name or keyword in category:
                    is_match = True
                    break
                # 也检查反向包含
                if position_name and any(kw in keyword for kw in position_name.split()):
                    is_match = True
                    break
            
            if is_match:
                priority_profiles.append(profile)
            else:
                other_profiles.append(profile)
        
        logger.info(f"[目标岗位过滤] 目标岗位: {target_positions}, 优先匹配: {len(priority_profiles)}, 其他: {len(other_profiles)}")
        return priority_profiles, other_profiles
    
    # ==================== 高级算法增强方法 ====================
    
    def match_two_stage(self, student_id: int, recall_k: int = 12, top_n: int = 5,
                        use_ensemble: bool = True) -> list:
        """
        两阶段匹配算法 - 向量召回 + LLM精排 + 集成融合
        
        优化版本：
        - 基于学生目标岗位预过滤，提升匹配准确性
        - 减少候选数量（12个），加速LLM精排
        - 优先处理与目标岗位相关的职位
        
        Args:
            student_id: 学生ID
            recall_k: 向量召回阶段的 Top-K（默认12，减少LLM调用）
            top_n: 最终返回的 Top-N 结果
            use_ensemble: 是否使用集成学习融合
        Returns:
            list[MatchResult]: 匹配结果列表
        """
        student = Student.query.get(student_id)
        student_profile = StudentProfile.query.filter_by(student_id=student_id).first()
        
        if not student or not student_profile:
            raise ValueError("学生数据不存在")
        
        # 构建学生画像
        sp_dict = student_profile.to_dict()
        sp_dict['student_name'] = student.name
        sp_dict['education'] = student.education
        sp_dict['major'] = student.major
        sp_dict['school'] = student.school
        
        # 获取学生目标岗位
        target_positions = student.get_target_positions()
        sp_dict['target_positions'] = target_positions
        
        # 获取所有岗位画像
        all_profiles = self._get_unique_job_profiles()
        if not all_profiles:
            return []
        
        # ====== 目标岗位预过滤 ======
        priority_profiles, other_profiles = self._filter_by_target_positions(all_profiles, target_positions)
        preference_boost = {}  # 存储目标岗位匹配加分
        
        # 为优先匹配的岗位设置加分
        for p in priority_profiles:
            preference_boost[p.id] = 0.15  # 15%加分
        
        # 重新排列岗位列表：优先岗位在前
        sorted_profiles = priority_profiles + other_profiles
        
        # ====== 第一阶段：向量召回（优先使用Sentence-BERT）======
        candidates = []
        recall_scores = {}  # 存储召回分数，用于集成学习
        
        if self.semantic_embedding and self.semantic_embedding.model:
            # 使用Sentence-BERT深度语义召回
            logger.info(f"[两阶段匹配] 第一阶段：Sentence-BERT 语义召回 Top-{recall_k}")
            
            # 构建学生文本描述（包含目标岗位信息）
            student_text = self._build_student_text(sp_dict)
            
            # 构建岗位文本描述列表
            job_texts = []
            for p in sorted_profiles:
                job_texts.append(self._build_job_text(p.to_dict()))
            
            # 计算语义相似度
            ranked = self.semantic_embedding.compute_similarity(student_text, job_texts)
            
            # 获取Top-K候选
            candidate_indices = [idx for idx, _ in ranked[:recall_k]]
            for idx, score in ranked[:recall_k]:
                profile = sorted_profiles[idx]
                candidates.append(profile)
                recall_scores[profile.id] = float(score) + preference_boost.get(profile.id, 0)
            
            logger.info(f"[两阶段匹配] Sentence-BERT召回完成，候选数: {len(candidates)}")
        
        elif self.embedding_service:
            # 降级使用TF-IDF召回
            logger.info(f"[两阶段匹配] 第一阶段：TF-IDF 向量召回 Top-{recall_k}")
            
            # 构建/更新岗位向量索引（使用排序后的列表）
            self.embedding_service.fit_job_corpus(sorted_profiles)
            
            # 计算学生与岗位的相似度
            recall_results = self.embedding_service.compute_student_similarity(sp_dict, top_k=recall_k)
            
            # 获取候选岗位
            candidate_ids = [r['job_profile_id'] for r in recall_results]
            for p in sorted_profiles:
                if p.id in candidate_ids:
                    candidates.append(p)
                    # 找到对应的召回分数（加上目标岗位加分）
                    for r in recall_results:
                        if r['job_profile_id'] == p.id:
                            base_score = r.get('similarity', 0.5)
                            recall_scores[p.id] = base_score + preference_boost.get(p.id, 0)
                            break
            
            # 确保至少包含部分优先岗位（如果有的话）
            included_ids = {p.id for p in candidates}
            for p in priority_profiles[:min(3, len(priority_profiles))]:
                if p.id not in included_ids:
                    candidates.append(p)
                    recall_scores[p.id] = 0.6 + preference_boost.get(p.id, 0)
                    logger.info(f"[两阶段匹配] 强制加入优先岗位: {p.position_name}")
            
            logger.info(f"[两阶段匹配] TF-IDF召回完成，候选数: {len(candidates)}")
        else:
            # 无召回服务，优先使用目标岗位相关的，并补充其他岗位达到 recall_k
            if priority_profiles:
                priority_ids = {p.id for p in priority_profiles}
                candidates = list(priority_profiles[:recall_k])
                # 补充其他岗位，确保候选数量达到 recall_k
                if len(candidates) < recall_k:
                    for p in other_profiles:
                        if len(candidates) >= recall_k:
                            break
                        if p.id not in priority_ids:
                            candidates.append(p)
            else:
                candidates = sorted_profiles[:recall_k]
            for p in candidates:
                recall_scores[p.id] = 0.5 + preference_boost.get(p.id, 0)
            logger.info(f"[两阶段匹配] 向量服务不可用，使用前{len(candidates)}个岗位")
        
        # ====== 技能标准化预处理 ======
        if self.skill_ontology:
            student_skills = sp_dict.get('technical_skills', [])
            sp_dict['normalized_skills'] = self.skill_ontology.normalize_skills(student_skills)
            sp_dict['transferable_skills'] = self.skill_ontology.find_transferable_skills(student_skills)
        
        # 清除旧结果
        MatchResult.query.filter_by(student_id=student_id).delete()
        db.session.commit()
        
        # 准备候选岗位数据
        job_data = []
        for p in candidates:
            jp_dict = p.to_dict()
            
            # 技能标准化
            skill_match_score = 0.5
            if self.skill_ontology:
                job_skills = jp_dict.get('technical_skills', [])
                jp_dict['normalized_skills'] = self.skill_ontology.normalize_skills(job_skills)
                
                # 计算技能差距分析
                skill_gap = self.skill_ontology.compute_skill_gap(
                    sp_dict.get('technical_skills', []),
                    job_skills
                )
                jp_dict['skill_gap_analysis'] = skill_gap
                # 提取技能匹配得分
                skill_match_score = skill_gap.get('match_ratio', 0.5)
            
            job_data.append({
                'id': p.id,
                'name': p.position_name,
                'dict': jp_dict,
                'weights': (p.weight_basic, p.weight_skill, p.weight_quality, p.weight_potential),
                'skill_match_score': skill_match_score,
                'recall_score': recall_scores.get(p.id, 0.5),
            })
        
        # ====== 第二阶段：LLM精排 ======
        logger.info(f"[两阶段匹配] 第二阶段：LLM精排 {len(job_data)} 个候选")
        
        llm_results = []
        for i, jd in enumerate(job_data):
            try:
                result = self._call_llm_for_match(sp_dict, jd['dict'], jd['weights'])
                result['job_profile_id'] = jd['id']
                result['job_name'] = jd['name']
                result['recall_score'] = jd['recall_score']
                result['skill_match_score'] = jd['skill_match_score']
                
                # 附加技能分析
                if 'skill_gap_analysis' in jd['dict']:
                    result['skill_ontology_analysis'] = jd['dict']['skill_gap_analysis']
                
                llm_results.append(result)
                logger.info(f"[两阶段匹配] 精排进度: {i+1}/{len(job_data)} - {jd['name']}")
            except Exception as e:
                logger.error(f"[两阶段匹配] 精排失败 [{jd['name']}]: {e}")
        
        # ====== 第三阶段：集成学习融合（如果启用）======
        if use_ensemble and self.ensemble_matcher and llm_results:
            logger.info("[两阶段匹配] 执行集成学习多模型融合")
            
            for res in llm_results:
                # 构建各组件分数
                component_scores = {
                    'llm_score': res['overall_score'] / 100.0,  # 归一化到0-1
                    'embedding_score': res.get('recall_score', 0.5),
                    'skill_score': res.get('skill_match_score', 0.5),
                    'ahp_score': 0.5,  # AHP稍后计算
                }
                
                # 集成融合
                ensemble_result = self.ensemble_matcher.ensemble_match(component_scores)
                res['ensemble_score'] = ensemble_result.final_score * 100  # 转回0-100
                res['ensemble_confidence'] = ensemble_result.confidence
                res['component_weights'] = ensemble_result.component_weights
        
        # ====== AHP权重优化重排序 ======
        if self.ahp_service and llm_results:
            logger.info("[两阶段匹配] 执行AHP权重优化重排序")
            job_profiles_dict = {jd['id']: jd['dict'] for jd in job_data}
            llm_results = self.ahp_service.rank_jobs(llm_results, job_profiles_dict)
        
        # 写入数据库
        db_results = []
        for res in llm_results:
            # 选择最终得分：集成分数 > AHP分数 > LLM原始分数
            final_score = res.get('ensemble_score', res.get('ahp_score', res['overall_score']))
            
            match_result = MatchResult(
                student_id=student_id,
                job_profile_id=res['job_profile_id'],
                basic_score=res['basic_score'],
                skill_score=res['skill_score'],
                quality_score=res['quality_score'],
                potential_score=res['potential_score'],
                overall_score=final_score,
                detail_analysis=json.dumps({
                    **res.get('detail_analysis', {}),
                    'ahp_weights': res.get('ahp_weights', {}),
                    'skill_ontology': res.get('skill_ontology_analysis', {}),
                    'ensemble': {
                        'enabled': use_ensemble and self.ensemble_matcher is not None,
                        'confidence': res.get('ensemble_confidence', 0),
                        'component_weights': res.get('component_weights', {}),
                    },
                    'recall_score': res.get('recall_score', 0),
                    'algorithm_stack': self._get_algorithm_stack(),
                }, ensure_ascii=False),
                skill_gaps=json.dumps(res.get('skill_gaps', []), ensure_ascii=False),
                recommendations=json.dumps(res.get('recommendations', []), ensure_ascii=False),
            )
            db.session.add(match_result)
            db_results.append(match_result)
        
        db.session.commit()
        logger.info(f"[两阶段匹配] 完成，共 {len(db_results)} 条结果")
        
        # 按最终得分排序，返回 Top-N
        db_results.sort(key=lambda r: r.overall_score, reverse=True)
        return db_results[:top_n]
    
    def _build_student_text(self, sp_dict: dict) -> str:
        """构建学生文本描述（用于语义嵌入）"""
        parts = []
        
        # 加入目标岗位（权重最高）
        target_positions = sp_dict.get('target_positions', [])
        if target_positions:
            parts.append(f"目标岗位: {' '.join(target_positions)}")
        
        parts.append(f"学历: {sp_dict.get('education', '')}")
        parts.append(f"专业: {sp_dict.get('major', '')}")
        parts.append(f"学校: {sp_dict.get('school', '')}")
        
        skills = sp_dict.get('technical_skills', [])
        if isinstance(skills, list):
            skill_names = []
            for s in skills:
                if isinstance(s, dict):
                    skill_names.append(s.get('name', ''))
                elif isinstance(s, str):
                    skill_names.append(s)
            if skill_names:
                parts.append(f"技能: {' '.join(skill_names)}")
        
        certs = sp_dict.get('certificates', [])
        if certs:
            parts.append(f"证书: {' '.join(str(c) for c in certs)}")
        
        return ' '.join(parts)
    
    def _build_job_text(self, jp_dict: dict) -> str:
        """构建岗位文本描述（用于语义嵌入）"""
        parts = []
        parts.append(f"岗位: {jp_dict.get('position_name', '')}")
        parts.append(f"类别: {jp_dict.get('category', '')}")
        parts.append(f"层级: {jp_dict.get('level', '')}")
        parts.append(f"学历要求: {jp_dict.get('education_req', '')}")
        
        skills = jp_dict.get('technical_skills', [])
        if isinstance(skills, str):
            try:
                skills = json.loads(skills)
            except:
                skills = [skills]
        if skills:
            parts.append(f"技能要求: {' '.join(str(s) for s in skills)}")
        
        parts.append(f"描述: {jp_dict.get('summary', '')}")
        return ' '.join(parts)
    
    def _get_algorithm_stack(self) -> list:
        """获取当前启用的算法栈"""
        stack = []
        if self.semantic_embedding and self.semantic_embedding.model:
            stack.append('Sentence-BERT语义召回')
        elif self.embedding_service:
            stack.append('TF-IDF向量召回')
        if self.skill_ontology:
            stack.append('技能本体标准化')
        if self.ahp_service:
            stack.append('AHP权重优化')
        if self.ensemble_matcher:
            stack.append('集成学习融合')
        if self.bayesian_optimizer:
            stack.append('贝叶斯权重调优')
        stack.append('LLM四维度精排')
        return stack

    def _get_unique_job_profiles(self) -> list:
        """按岗位名称去重，优先保留最新画像，避免 group_by 的方言兼容问题。"""
        profiles = JobProfile.query.order_by(JobProfile.id.desc()).all()
        seen = set()
        unique_profiles = []

        for profile in profiles:
            key = (profile.position_name or '').strip().lower()
            if key and key in seen:
                continue
            if key:
                seen.add(key)
            unique_profiles.append(profile)

        return unique_profiles
    
    def get_skill_analysis(self, student_id: int, job_profile_id: int) -> dict:
        """
        获取详细的技能匹配分析（使用技能本体标准化）
        
        Args:
            student_id: 学生ID
            job_profile_id: 岗位画像ID
        Returns:
            dict: 技能分析结果
        """
        if not self.skill_ontology:
            return {'error': '技能本体服务不可用'}
        
        student_profile = StudentProfile.query.filter_by(student_id=student_id).first()
        job_profile = JobProfile.query.get(job_profile_id)
        
        if not student_profile or not job_profile:
            return {'error': '数据不存在'}
        
        student_skills = student_profile.get_technical_skills()
        job_skills = job_profile.get_technical_skills()
        
        # 使用技能本体进行分析
        analysis = self.skill_ontology.compute_skill_gap(student_skills, job_skills)
        
        # 添加学习路径建议
        if analysis.get('missing'):
            analysis['learning_path'] = self.skill_ontology.suggest_learning_path(analysis['missing'])
        
        return analysis
    
    def get_algorithm_info(self) -> dict:
        """获取当前使用的算法信息（用于前端展示）"""
        return {
            'embedding_service': self.embedding_service is not None,
            'semantic_embedding': self.semantic_embedding is not None and self.semantic_embedding.model is not None,
            'ahp_service': self.ahp_service is not None,
            'skill_ontology': self.skill_ontology is not None,
            'bayesian_optimizer': self.bayesian_optimizer is not None,
            'ensemble_matcher': self.ensemble_matcher is not None,
            'algorithm_stack': self._get_algorithm_stack(),
            'algorithms': [
                {
                    'name': 'Sentence-BERT深度语义',
                    'enabled': self.semantic_embedding is not None and self.semantic_embedding.model is not None,
                    'description': '使用Sentence-BERT生成稠密向量，捕获深层语义关系',
                    'category': 'embedding',
                },
                {
                    'name': 'TF-IDF向量召回',
                    'enabled': self.embedding_service is not None,
                    'description': '使用TF-IDF+余弦相似度快速筛选候选岗位',
                    'category': 'embedding',
                },
                {
                    'name': 'AHP层次分析法',
                    'enabled': self.ahp_service is not None,
                    'description': '多准则决策优化四维度权重分配',
                    'category': 'optimization',
                },
                {
                    'name': '贝叶斯权重优化',
                    'enabled': self.bayesian_optimizer is not None,
                    'description': '使用高斯过程自动寻找最优权重配置',
                    'category': 'optimization',
                },
                {
                    'name': '集成学习融合',
                    'enabled': self.ensemble_matcher is not None,
                    'description': '多模型结果加权融合，提升匹配稳定性',
                    'category': 'ensemble',
                },
                {
                    'name': '技能本体标准化',
                    'enabled': self.skill_ontology is not None,
                    'description': '统一技能名称，提高匹配准确率',
                    'category': 'preprocessing',
                },
                {
                    'name': 'LLM四维度精排',
                    'enabled': True,
                    'description': '大语言模型对候选岗位进行四维度深度分析',
                    'category': 'ranking',
                },
            ]
        }
    
    def optimize_weights_bayesian(self, student_id: int, n_iterations: int = 20) -> dict:
        """
        使用贝叶斯优化自动调优匹配权重
        
        Args:
            student_id: 学生ID（用于评估优化效果）
            n_iterations: 优化迭代次数
        Returns:
            dict: 优化结果
        """
        if not self.bayesian_optimizer:
            return {'error': '贝叶斯优化器不可用', 'available': False}
        
        logger.info(f"[贝叶斯优化] 开始权重优化，目标学生ID={student_id}")
        
        # 定义评估函数
        def evaluate_weights(params: dict) -> float:
            """评估当前权重配置的匹配质量"""
            # 这里可以基于已有的匹配结果计算质量分数
            # 简化版：使用多样性 + 平均分作为评估指标
            basic_w = params.get('basic', 0.25)
            skill_w = params.get('skill', 0.35)
            quality_w = params.get('quality', 0.2)
            potential_w = params.get('potential', 0.2)
            
            # 归一化
            total = basic_w + skill_w + quality_w + potential_w
            basic_w, skill_w, quality_w, potential_w = (
                basic_w/total, skill_w/total, quality_w/total, potential_w/total
            )
            
            # 获取当前匹配结果
            results = MatchResult.query.filter_by(student_id=student_id).all()
            if not results:
                return 0.5
            
            # 计算多样性（标准差）和平均分
            scores = [r.overall_score for r in results]
            avg_score = sum(scores) / len(scores)
            variance = sum((s - avg_score)**2 for s in scores) / len(scores)
            std_dev = variance ** 0.5
            
            # 评估指标：平均分 + 多样性（避免所有分数相同）
            diversity_bonus = min(std_dev / 10, 0.1)  # 最多10%加分
            return (avg_score / 100) + diversity_bonus
        
        # 执行贝叶斯优化
        try:
            result = self.bayesian_optimizer.optimize_matching_weights(evaluate_weights)
            
            logger.info(f"[贝叶斯优化] 完成，最优权重: {result.best_params}")
            
            return {
                'success': True,
                'best_weights': result.best_params,
                'best_score': result.best_score,
                'iterations': result.n_iterations,
                'convergence_history': result.convergence_history[-10:],  # 最近10次
            }
        except Exception as e:
            logger.error(f"[贝叶斯优化] 失败: {e}")
            return {'error': str(e), 'available': True}

# ============================================
# 岗位分析服务（Agent 1）
# 负责：岗位画像生成、岗位分类归纳
# ============================================
import json
import logging
from collections import Counter

from models.database import db
from models.job import Job, JobProfile
from services.llm_client import get_llm
from prompts.templates import (
    JOB_PROFILE_SYSTEM, JOB_PROFILE_USER,
    BATCH_JOB_CLASSIFY
)

logger = logging.getLogger(__name__)


class JobAnalyzer:
    """岗位分析Agent - 从原始岗位数据中提取结构化画像"""
    
    def analyze_single_job(self, job: Job) -> JobProfile:
        """
        分析单个岗位，生成岗位画像
        
        Args:
            job: 原始岗位数据
        Returns:
            JobProfile: 生成的岗位画像
        """
        llm = get_llm()
        
        messages = [
            {"role": "system", "content": JOB_PROFILE_SYSTEM},
            {"role": "user", "content": JOB_PROFILE_USER.format(
                title=job.title,
                address=job.address or '未知',
                salary_range=job.salary_range or '面议',
                company_name=job.company_name or '未知',
                industry=job.industry or '未知',
                company_size=job.company_size or '未知',
                description=job.description or '无详情',
            )}
        ]
        
        result = llm.chat_json(messages, temperature=0.3)
        
        profile = JobProfile(
            job_id=job.id,
            position_name=result.get('position_name', job.title),
            category=result.get('category', '未分类'),
            level=result.get('level', '初级'),
            education_req=result.get('education_req', '不限'),
            experience_req=result.get('experience_req', '不限'),
            innovation_ability=result.get('innovation_ability', 5),
            learning_ability=result.get('learning_ability', 5),
            pressure_resistance=result.get('pressure_resistance', 5),
            communication_skill=result.get('communication_skill', 5),
            teamwork_ability=result.get('teamwork_ability', 5),
            internship_ability=result.get('internship_ability', 5),
            summary=result.get('summary', ''),
            salary_range=job.salary_range,
            weight_basic=result.get('weight_basic', 0.2),
            weight_skill=result.get('weight_skill', 0.35),
            weight_quality=result.get('weight_quality', 0.25),
            weight_potential=result.get('weight_potential', 0.2),
        )
        profile.set_technical_skills(result.get('technical_skills', []))
        profile.set_certificates(result.get('certificates', []))
        
        db.session.add(profile)
        db.session.commit()
        
        logger.info(f"岗位画像生成成功: {profile.position_name} ({profile.category})")
        return profile
    
    def batch_analyze_jobs(self, jobs: list, max_count=10) -> list:
        """
        批量分析岗位，生成画像
        为节省API调用，相同岗位名称只分析一次
        优先选择描述最丰富的岗位进行分析
        """
        # 已存在画像的标题
        existing_titles = set(
            t[0] for t in db.session.query(JobProfile.position_name).all()
        )

        # 按标题去重，优先选描述最长的
        best_per_title = {}
        for job in jobs:
            if job.title in existing_titles:
                continue
            prev = best_per_title.get(job.title)
            if prev is None or len(job.description or '') > len(prev.description or ''):
                best_per_title[job.title] = job

        candidates = list(best_per_title.values())[:max_count]
        logger.info(f"准备分析 {len(candidates)} 个不重复岗位（已有画像 {len(existing_titles)} 个）")

        profiles = []
        for idx, job in enumerate(candidates, 1):
            try:
                logger.info(f"[{idx}/{len(candidates)}] 正在分析: {job.title}")
                profile = self.analyze_single_job(job)
                profiles.append(profile)
                logger.info(f"[{idx}/{len(candidates)}] 完成: {profile.position_name} ({profile.category})")
            except Exception as e:
                logger.error(f"[{idx}/{len(candidates)}] 分析岗位 [{job.title}] 失败: {e}", exc_info=True)
                continue

        return profiles
    
    def classify_job_titles(self, limit=500) -> dict:
        """
        对岗位名称进行分类归纳
        先统计频率，再用LLM归纳
        
        Returns:
            dict: 分类结果
        """
        # 统计所有岗位名称
        jobs = Job.query.with_entities(Job.title).all()
        title_counts = Counter([j.title for j in jobs])
        
        # 取出高频岗位（去重后的）
        top_titles = [t for t, c in title_counts.most_common(limit)]
        
        if len(top_titles) > 100:
            # 如果太多，分批处理
            top_titles = top_titles[:100]
        
        llm = get_llm()
        messages = [
            {"role": "system", "content": "你是一位IT人力资源专家，擅长岗位分类。"},
            {"role": "user", "content": BATCH_JOB_CLASSIFY.format(
                job_titles='\n'.join(f"- {t} ({title_counts[t]}条)" for t in top_titles)
            )}
        ]
        
        result = llm.chat_json(messages, temperature=0.2)
        return result
    
    def get_all_profiles(self) -> list:
        """获取所有已生成的岗位画像"""
        profiles = JobProfile.query.all()
        return [p.to_dict() for p in profiles]
    
    def get_profile_by_id(self, profile_id: int) -> dict:
        """获取指定岗位画像"""
        profile = JobProfile.query.get(profile_id)
        if profile:
            return profile.to_dict()
        return None
    
    def get_unique_categories(self) -> list:
        """获取所有已分析的岗位类别"""
        categories = db.session.query(JobProfile.category).distinct().all()
        return [c[0] for c in categories if c[0]]
    
    def get_profiles_by_category(self, category: str) -> list:
        """按类别获取岗位画像"""
        profiles = JobProfile.query.filter_by(category=category).all()
        return [p.to_dict() for p in profiles]

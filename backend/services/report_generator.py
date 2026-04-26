# ============================================
# 报告生成服务（Agent 4）- 增强版
# 负责：职业生涯发展报告的生成、润色、编辑、导出
# 升级特性：
#   - Multi-Agent协作生成各章节
#   - CoT思维链推理提升内容质量
#   - 融入算法分析结果（技能差距、图谱路径、岗位热度）
# ============================================
import json
import logging
import markdown
from datetime import datetime
from typing import Optional

from models.database import db
from models.student import Student, StudentProfile, MatchResult, CareerReport
from models.job import JobProfile, JobGraph
from services.llm_client import get_llm
from prompts.templates import (
    REPORT_SYSTEM,
    REPORT_SELF_ASSESSMENT,
    REPORT_JOB_EXPLORATION,
    REPORT_CAREER_GOAL,
    REPORT_ACTION_PLAN,
    REPORT_POLISH,
)

logger = logging.getLogger(__name__)

# 尝试导入高级算法模块
try:
    from services.algorithms import AgentOrchestrator, SkillOntologyService
    ADVANCED_REPORT_AVAILABLE = True
except ImportError:
    ADVANCED_REPORT_AVAILABLE = False
    logger.info("高级报告生成模块未加载，使用基础生成器")


class ReportGenerator:
    """
    报告生成Agent - 生成个性化职业生涯发展报告
    
    升级特性：
    - 支持Multi-Agent协作（ParserAgent->AnalyzerAgent->PlannerAgent->WriterAgent）
    - 启用CoT思维链推理，提升报告内容的逻辑性
    - 融入算法分析结果（技能差距分析、职业路径图谱、岗位热度排名）
    """
    
    def __init__(self):
        """初始化报告生成器及可选的高级组件"""
        self.orchestrator = None
        self.skill_ontology = None
        
        if ADVANCED_REPORT_AVAILABLE:
            try:
                self.orchestrator = AgentOrchestrator()
                self.skill_ontology = SkillOntologyService()
                logger.info("ReportGenerator高级组件初始化完成")
            except Exception as e:
                logger.warning(f"高级组件初始化失败: {e}")
    
    def generate_full_report(self, student_id: int, use_multi_agent: bool = True) -> CareerReport:
        """
        生成完整的职业生涯发展报告
        
        Args:
            student_id: 学生ID
            use_multi_agent: 是否使用Multi-Agent协作模式
        Returns:
            CareerReport: 生成的报告
        """
        student = Student.query.get(student_id)
        student_profile = StudentProfile.query.filter_by(student_id=student_id).first()
        
        if not student or not student_profile:
            raise ValueError("学生或画像数据不存在，请先创建学生画像")
        
        # 获取匹配结果
        match_results = MatchResult.query.filter_by(
            student_id=student_id
        ).order_by(MatchResult.overall_score.desc()).all()
        
        if not match_results:
            raise ValueError("没有匹配结果，请先执行人岗匹配")
        
        # 尝试使用Multi-Agent模式
        if use_multi_agent and self.orchestrator:
            return self._generate_with_multi_agent(student, student_profile, match_results)
        
        # 降级到传统模式
        return self._generate_traditional(student, student_profile, match_results)
    
    def _generate_with_multi_agent(self, student: Student, student_profile: StudentProfile, 
                                    match_results: list) -> CareerReport:
        """
        使用Multi-Agent协作模式生成报告
        
        工作流：
        1. ParserAgent: 解析学生画像和匹配结果
        2. AnalyzerAgent: 深度分析技能差距、职业匹配度
        3. PlannerAgent: 规划职业路径、生成行动计划
        4. WriterAgent: 撰写高质量报告内容
        """
        logger.info(f"使用Multi-Agent模式为学生 {student.name} 生成报告...")
        
        # 准备输入数据
        sp_dict = student_profile.to_dict()
        sp_dict['student_name'] = student.name
        sp_dict['education'] = student.education
        sp_dict['major'] = student.major
        sp_dict['school'] = student.school
        
        match_data = self._prepare_match_data(match_results)
        
        # 准备职业路径数据
        best_job = None
        career_paths = []
        if match_results:
            best_jp = JobProfile.query.get(match_results[0].job_profile_id)
            if best_jp:
                best_job = best_jp.to_dict()
                paths = JobGraph.query.filter(
                    (JobGraph.from_position.contains(best_job['position_name'])) |
                    (JobGraph.to_position.contains(best_job['position_name']))
                ).all()
                career_paths = [p.to_dict() for p in paths]
        
        # 获取技能差距分析（使用算法）
        skill_analysis = self._get_skill_analysis(student_profile, best_job)
        
        # 执行Multi-Agent工作流
        input_data = {
            'student_profile': sp_dict,
            'match_results': match_data,
            'best_match_job': best_job,
            'career_paths': career_paths,
            'skill_analysis': skill_analysis,
        }
        
        result = self.orchestrator.execute_workflow('full_report', input_data)
        
        if result.get('status') == 'success':
            # 从Agent输出提取各章节
            sections = result.get('sections', {})
            reasoning_chain = result.get('reasoning_chain', [])
            
            section1 = sections.get('self_assessment', '')
            section2 = sections.get('job_exploration', '')
            section3 = sections.get('career_goal', '')
            section4 = sections.get('action_plan', '')
            
            # 添加CoT推理过程作为附录（可选）
            cot_appendix = self._format_reasoning_chain(reasoning_chain) if reasoning_chain else ''
        else:
            # Agent执行失败，降级到传统模式
            logger.warning("Multi-Agent执行失败，降级到传统模式")
            return self._generate_traditional(student, student_profile, match_results)
        
        # 组装完整报告
        full_report = self._assemble_full_report(
            student, section1, section2, section3, section4, cot_appendix
        )
        
        return self._save_report(student.id, student.name, section1, section2, section3, section4, 
                                  full_report, match_results)
    
    def _generate_traditional(self, student: Student, student_profile: StudentProfile, 
                               match_results: list) -> CareerReport:
        """传统模式生成报告（带CoT增强）"""
        
        llm = get_llm()
        sp_dict = student_profile.to_dict()
        sp_dict['student_name'] = student.name
        sp_dict['education'] = student.education
        sp_dict['major'] = student.major
        sp_dict['school'] = student.school
        student_json = json.dumps(sp_dict, ensure_ascii=False, indent=2)
        
        # ---- 第1章：自我评估 ----
        logger.info("生成报告第1章：自我评估...")
        section1 = self._generate_section_with_cot(
            llm, REPORT_SELF_ASSESSMENT.format(student_profile=student_json),
            section_name="自我评估"
        )
        
        # ---- 第2章：职业探索与岗位匹配 ----
        logger.info("生成报告第2章：职业探索与岗位匹配...")
        match_data = self._prepare_match_data(match_results)
        
        section2 = self._generate_section_with_cot(
            llm, REPORT_JOB_EXPLORATION.format(
                student_profile=student_json,
                match_results=json.dumps(match_data, ensure_ascii=False, indent=2),
            ),
            section_name="职业探索"
        )
        
        # ---- 第3章：职业目标与路径规划 ----
        logger.info("生成报告第3章：职业目标与路径规划...")
        best_match_job = None
        career_paths = []
        if match_results:
            best_jp = JobProfile.query.get(match_results[0].job_profile_id)
            if best_jp:
                best_match_job = best_jp.to_dict()
                paths = JobGraph.query.filter(
                    (JobGraph.from_position.contains(best_match_job['position_name'])) |
                    (JobGraph.to_position.contains(best_match_job['position_name']))
                ).all()
                career_paths = [p.to_dict() for p in paths]
        
        section3 = self._generate_section_with_cot(
            llm, REPORT_CAREER_GOAL.format(
                student_profile=student_json,
                best_match=json.dumps(best_match_job or {}, ensure_ascii=False, indent=2),
                career_paths=json.dumps(career_paths, ensure_ascii=False, indent=2),
            ),
            section_name="职业目标"
        )
        
        # ---- 第4章：行动计划 ----
        logger.info("生成报告第4章：行动计划...")
        skill_gaps = self._extract_skill_gaps(match_results)
        
        section4 = self._generate_section_with_cot(
            llm, REPORT_ACTION_PLAN.format(
                student_profile=student_json,
                target_job=json.dumps(best_match_job or {}, ensure_ascii=False, indent=2),
                skill_gaps=json.dumps(skill_gaps, ensure_ascii=False, indent=2),
            ),
            section_name="行动计划"
        )
        
        # ---- 组装完整报告 ----
        full_report = self._assemble_full_report(student, section1, section2, section3, section4)
        
        return self._save_report(student.id, student.name, section1, section2, section3, section4, 
                                  full_report, match_results)
    
    def _prepare_match_data(self, match_results: list) -> list:
        """准备匹配结果数据"""
        match_data = []
        for mr in match_results[:5]:
            jp = JobProfile.query.get(mr.job_profile_id)
            if jp:
                match_data.append({
                    'job_name': jp.position_name,
                    'job_category': jp.category,
                    'overall_score': mr.overall_score,
                    'basic_score': mr.basic_score,
                    'skill_score': mr.skill_score,
                    'quality_score': mr.quality_score,
                    'potential_score': mr.potential_score,
                    'detail': json.loads(mr.detail_analysis) if mr.detail_analysis else {},
                })
        return match_data
    
    def _extract_skill_gaps(self, match_results: list) -> list:
        """提取技能差距"""
        skill_gaps = []
        if match_results:
            try:
                skill_gaps = json.loads(match_results[0].skill_gaps or '[]')
            except:
                pass
        return skill_gaps
    
    def _get_skill_analysis(self, student_profile: StudentProfile, target_job: dict) -> dict:
        """使用算法服务进行技能分析"""
        if not self.skill_ontology or not target_job:
            return {}
        
        try:
            # 获取学生技能 (使用 technical_skills 字段)
            student_skills = json.loads(student_profile.technical_skills or '[]')
            if isinstance(student_skills, str):
                student_skills = [s.strip() for s in student_skills.split(',')]
            
            # 获取岗位要求技能
            job_skills = target_job.get('skill_requirements', [])
            if isinstance(job_skills, str):
                job_skills = json.loads(job_skills)
            
            # 计算技能差距
            gap_analysis = self.skill_ontology.compute_skill_gap(student_skills, job_skills)
            
            # 生成学习路径建议
            learning_path = self.skill_ontology.suggest_learning_path(
                student_skills, job_skills
            )
            
            return {
                'gap_analysis': gap_analysis,
                'learning_path': learning_path,
            }
        except Exception as e:
            logger.warning(f"技能分析失败: {e}")
            return {}
    
    def _generate_section_with_cot(self, llm, user_prompt: str, section_name: str = "") -> str:
        """生成报告章节（带CoT思维链增强）"""
        # 添加CoT指令
        cot_prompt = f"""请按照以下思维过程生成{section_name}章节：

【思考步骤】
1. 首先分析输入数据的关键信息
2. 识别核心观点和重要发现
3. 规划章节结构和逻辑主线
4. 撰写内容，确保论据充分、建议具体

{user_prompt}

请直接输出最终内容（不需要显示思考步骤）："""
        
        messages = [
            {"role": "system", "content": REPORT_SYSTEM},
            {"role": "user", "content": cot_prompt},
        ]
        return llm.chat(messages, temperature=0.6, max_tokens=3000)
    
    def _format_reasoning_chain(self, reasoning_chain: list) -> str:
        """格式化推理链为附录内容"""
        if not reasoning_chain:
            return ""
        
        appendix = "\n\n---\n\n## 附录：AI分析推理过程\n\n"
        for i, step in enumerate(reasoning_chain, 1):
            agent = step.get('agent', 'Unknown')
            reasoning = step.get('reasoning', '')
            appendix += f"### 步骤{i} - {agent}\n{reasoning}\n\n"
        
        return appendix
    
    def _assemble_full_report(self, student: Student, section1: str, section2: str, 
                               section3: str, section4: str, appendix: str = "") -> str:
        """组装完整报告"""
        return f"""# {student.name}的职业生涯发展报告

> 生成时间：{datetime.now().strftime('%Y年%m月%d日')}
> 学校专业：{student.school or ''} {student.major or ''}
> 学历层次：{student.education or ''}

---

## 第一章 自我评估

{section1}

---

## 第二章 职业探索与岗位匹配

{section2}

---

## 第三章 职业目标设定与路径规划

{section3}

---

## 第四章 行动计划与成长方案

{section4}

---

*本报告由"AI职业规划智能体"自动生成，仅供参考。建议结合个人实际情况和专业指导进行决策。*
{appendix}"""
    
    def _save_report(self, student_id: int, student_name: str, section1: str, section2: str,
                      section3: str, section4: str, full_report: str, match_results: list) -> CareerReport:
        """保存报告到数据库"""
        report = CareerReport.query.filter_by(student_id=student_id).first()
        if not report:
            report = CareerReport(student_id=student_id)
        
        report.title = f"{student_name}的职业生涯发展报告"
        report.section_self_assessment = section1
        report.section_job_exploration = section2
        report.section_career_goal = section3
        report.section_action_plan = section4
        report.full_report = full_report
        report.status = 'generated'
        report.match_result_ids = json.dumps([mr.id for mr in match_results[:5]])
        
        db.session.add(report)
        db.session.commit()
        
        logger.info(f"职业规划报告生成完毕: {report.title}")
        return report
    
    def polish_report(self, report_id: int) -> CareerReport:
        """
        对报告进行智能润色
        
        Args:
            report_id: 报告ID
        Returns:
            CareerReport: 润色后的报告
        """
        report = CareerReport.query.get(report_id)
        if not report:
            raise ValueError("报告不存在")
        
        llm = get_llm()
        
        messages = [
            {"role": "system", "content": REPORT_SYSTEM},
            {"role": "user", "content": REPORT_POLISH.format(
                report_content=report.full_report
            )},
        ]
        
        polished = llm.chat(messages, temperature=0.4, max_tokens=6000)
        report.full_report = polished
        report.status = 'edited'
        
        db.session.commit()
        logger.info(f"报告润色完成: {report.title}")
        return report
    
    def update_report_section(self, report_id: int, section_name: str, content: str) -> CareerReport:
        """
        手动编辑报告的某一章节
        
        Args:
            report_id: 报告ID
            section_name: 章节名 (self_assessment/job_exploration/career_goal/action_plan)
            content: 新内容
        """
        report = CareerReport.query.get(report_id)
        if not report:
            raise ValueError("报告不存在")
        
        field_name = f'section_{section_name}'
        if hasattr(report, field_name):
            setattr(report, field_name, content)
            
            # 重新组装完整报告
            student = Student.query.get(report.student_id)
            report.full_report = f"""# {report.title}

> 生成时间：{datetime.now().strftime('%Y年%m月%d日')}
> 学校专业：{student.school or ''} {student.major or ''}

---

## 第一章 自我评估

{report.section_self_assessment or ''}

---

## 第二章 职业探索与岗位匹配

{report.section_job_exploration or ''}

---

## 第三章 职业目标设定与路径规划

{report.section_career_goal or ''}

---

## 第四章 行动计划与成长方案

{report.section_action_plan or ''}

---

*本报告由"AI职业规划智能体"自动生成，仅供参考。*
"""
            report.status = 'edited'
            db.session.commit()
        
        return report
    
    def export_html(self, report_id: int) -> str:
        """
        将报告导出为HTML
        
        Args:
            report_id: 报告ID
        Returns:
            str: HTML内容
        """
        report = CareerReport.query.get(report_id)
        if not report or not report.full_report:
            raise ValueError("报告不存在或内容为空")
        
        # Markdown转HTML
        html_content = markdown.markdown(
            report.full_report,
            extensions=['tables', 'fenced_code', 'toc']
        )
        
        # 包装完整HTML页面
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report.title}</title>
    <style>
        body {{
            font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            color: #333;
            line-height: 1.8;
        }}
        h1 {{ color: #1a73e8; border-bottom: 3px solid #1a73e8; padding-bottom: 10px; }}
        h2 {{ color: #333; border-bottom: 1px solid #e0e0e0; padding-bottom: 8px; margin-top: 40px; }}
        h3 {{ color: #555; }}
        blockquote {{ 
            border-left: 4px solid #1a73e8; 
            padding: 10px 20px; 
            background: #f8f9fa; 
            margin: 15px 0;
        }}
        table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        th {{ background: #f0f4ff; }}
        ul, ol {{ padding-left: 25px; }}
        li {{ margin: 5px 0; }}
        hr {{ border: none; border-top: 1px solid #e0e0e0; margin: 30px 0; }}
        .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 50px; }}
        @media print {{
            body {{ padding: 20px; }}
            h2 {{ page-break-before: always; }}
        }}
    </style>
</head>
<body>
    {html_content}
    <div class="footer">
        <p>本报告由"基于AI的大学生职业规划智能体"自动生成 | 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    </div>
</body>
</html>"""
        
        report.status = 'exported'
        db.session.commit()
        
        return html
    
    def export_markdown(self, report_id: int) -> str:
        """导出Markdown格式"""
        report = CareerReport.query.get(report_id)
        if not report or not report.full_report:
            raise ValueError("报告不存在或内容为空")
        return report.full_report
    
    def get_report(self, report_id: int) -> dict:
        """获取报告"""
        report = CareerReport.query.get(report_id)
        if report:
            return report.to_dict()
        return None
    
    def get_student_report(self, student_id: int) -> dict:
        """获取学生的最新报告"""
        report = CareerReport.query.filter_by(
            student_id=student_id
        ).order_by(CareerReport.updated_at.desc()).first()
        if report:
            return report.to_dict()
        return None

# ============================================
# 学生相关数据模型
# ============================================
import json
from datetime import datetime
from models.database import db


class Student(db.Model):
    """学生基础信息"""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    education = db.Column(db.String(50))            # 学历: 专科/本科/硕士/博士
    major = db.Column(db.String(200))                # 专业
    school = db.Column(db.String(200))               # 学校
    graduation_year = db.Column(db.Integer)           # 毕业年份
    email = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    
    # 原始简历文本
    resume_text = db.Column(db.Text)
    resume_file_path = db.Column(db.String(500))
    
    # 职业意愿
    target_positions = db.Column(db.Text, default='[]')      # 目标岗位列表
    target_cities = db.Column(db.Text, default='[]')          # 目标城市
    salary_expectation = db.Column(db.String(100))             # 期望薪资
    career_preference = db.Column(db.Text)                     # 职业偏好说明
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    profile = db.relationship('StudentProfile', backref='student', uselist=False, lazy=True)
    reports = db.relationship('CareerReport', backref='student', lazy=True)

    def get_target_positions(self):
        try:
            return json.loads(self.target_positions) if self.target_positions else []
        except:
            return []
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
            'education': self.education,
            'major': self.major,
            'school': self.school,
            'graduation_year': self.graduation_year,
            'email': self.email,
            'phone': self.phone,
            'resume_text': self.resume_text,
            'target_positions': self.get_target_positions(),
            'salary_expectation': self.salary_expectation,
            'career_preference': self.career_preference,
        }


class StudentProfile(db.Model):
    """学生就业能力画像 - 由LLM从简历中提取"""
    __tablename__ = 'student_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    
    # 结构化能力数据（JSON格式）
    technical_skills = db.Column(db.Text, default='[]')      # 专业技能列表
    certificates = db.Column(db.Text, default='[]')           # 持有证书
    project_experience = db.Column(db.Text, default='[]')     # 项目经历
    internship_experience = db.Column(db.Text, default='[]')  # 实习经历
    awards = db.Column(db.Text, default='[]')                 # 获奖情况
    
    # 软技能评分（1-10分，由LLM根据简历内容评估）
    innovation_ability = db.Column(db.Float, default=5.0)     # 创新能力
    learning_ability = db.Column(db.Float, default=5.0)       # 学习能力
    pressure_resistance = db.Column(db.Float, default=5.0)    # 抗压能力
    communication_skill = db.Column(db.Float, default=5.0)    # 沟通能力
    teamwork_ability = db.Column(db.Float, default=5.0)       # 团队协作能力
    internship_ability = db.Column(db.Float, default=5.0)     # 实习/实践能力
    
    # 综合评分
    completeness_score = db.Column(db.Float, default=0.0)     # 完整度评分(0-100)
    competitiveness_score = db.Column(db.Float, default=0.0)  # 竞争力评分(0-100)
    
    # LLM生成的综合评价
    overall_evaluation = db.Column(db.Text)                    # 综合评价
    strengths = db.Column(db.Text, default='[]')              # 优势
    weaknesses = db.Column(db.Text, default='[]')             # 不足
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_technical_skills(self):
        try:
            return json.loads(self.technical_skills) if self.technical_skills else []
        except:
            return []
    
    def get_certificates(self):
        try:
            return json.loads(self.certificates) if self.certificates else []
        except:
            return []
    
    def get_project_experience(self):
        try:
            return json.loads(self.project_experience) if self.project_experience else []
        except:
            return []
    
    def get_internship_experience(self):
        try:
            return json.loads(self.internship_experience) if self.internship_experience else []
        except:
            return []
    
    def get_strengths(self):
        try:
            return json.loads(self.strengths) if self.strengths else []
        except:
            return []
    
    def get_weaknesses(self):
        try:
            return json.loads(self.weaknesses) if self.weaknesses else []
        except:
            return []

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'technical_skills': self.get_technical_skills(),
            'certificates': self.get_certificates(),
            'project_experience': self.get_project_experience(),
            'internship_experience': self.get_internship_experience(),
            'innovation_ability': self.innovation_ability,
            'learning_ability': self.learning_ability,
            'pressure_resistance': self.pressure_resistance,
            'communication_skill': self.communication_skill,
            'teamwork_ability': self.teamwork_ability,
            'internship_ability': self.internship_ability,
            'completeness_score': self.completeness_score,
            'competitiveness_score': self.competitiveness_score,
            'overall_evaluation': self.overall_evaluation,
            'strengths': self.get_strengths(),
            'weaknesses': self.get_weaknesses(),
        }


class MatchResult(db.Model):
    """人岗匹配结果"""
    __tablename__ = 'match_results'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    job_profile_id = db.Column(db.Integer, db.ForeignKey('job_profiles.id'), nullable=False)
    
    # 四维度评分（0-100）
    basic_score = db.Column(db.Float, default=0.0)        # 基础要求匹配度
    skill_score = db.Column(db.Float, default=0.0)        # 职业技能匹配度
    quality_score = db.Column(db.Float, default=0.0)      # 职业素养匹配度
    potential_score = db.Column(db.Float, default=0.0)     # 发展潜力匹配度
    
    # 综合得分
    overall_score = db.Column(db.Float, default=0.0)       # 加权综合得分
    
    # 详细分析（JSON）
    detail_analysis = db.Column(db.Text, default='{}')     # 详细分析报告
    skill_gaps = db.Column(db.Text, default='[]')          # 技能差距
    recommendations = db.Column(db.Text, default='[]')     # 提升建议
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联
    job_profile = db.relationship('JobProfile', backref='match_results')

    def to_dict(self):
        detail = {}
        gaps = []
        recs = []
        try:
            detail = json.loads(self.detail_analysis) if self.detail_analysis else {}
            gaps = json.loads(self.skill_gaps) if self.skill_gaps else []
            recs = json.loads(self.recommendations) if self.recommendations else []
        except:
            pass
        return {
            'id': self.id,
            'student_id': self.student_id,
            'job_profile_id': self.job_profile_id,
            'basic_score': self.basic_score,
            'skill_score': self.skill_score,
            'quality_score': self.quality_score,
            'potential_score': self.potential_score,
            'overall_score': self.overall_score,
            'detail_analysis': detail,
            'skill_gaps': gaps,
            'recommendations': recs,
        }


class CareerReport(db.Model):
    """职业生涯发展报告"""
    __tablename__ = 'career_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    
    # 报告标题
    title = db.Column(db.String(300), default='职业生涯发展报告')
    
    # 报告各章节内容（Markdown格式）
    section_self_assessment = db.Column(db.Text)      # 自我评估
    section_job_exploration = db.Column(db.Text)       # 职业探索与岗位匹配
    section_career_goal = db.Column(db.Text)           # 职业目标设定
    section_career_path = db.Column(db.Text)           # 职业路径规划
    section_action_plan = db.Column(db.Text)           # 行动计划
    section_evaluation = db.Column(db.Text)            # 评估与调整
    
    # 完整报告（合并所有章节）
    full_report = db.Column(db.Text)
    
    # 报告状态
    status = db.Column(db.String(20), default='draft')  # draft/generated/edited/exported
    
    # 关联的匹配结果IDs
    match_result_ids = db.Column(db.Text, default='[]')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'title': self.title,
            'section_self_assessment': self.section_self_assessment,
            'section_job_exploration': self.section_job_exploration,
            'section_career_goal': self.section_career_goal,
            'section_career_path': self.section_career_path,
            'section_action_plan': self.section_action_plan,
            'section_evaluation': self.section_evaluation,
            'full_report': self.full_report,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

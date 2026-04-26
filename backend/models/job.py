# ============================================
# 岗位相关数据模型
# ============================================
import json
from datetime import datetime
from models.database import db


class Job(db.Model):
    """原始岗位数据"""
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)       # 岗位名称
    address = db.Column(db.String(200))                                  # 工作地址
    salary_range = db.Column(db.String(100))                             # 薪资范围
    company_name = db.Column(db.String(300))                             # 公司名称
    industry = db.Column(db.String(200))                                 # 所属行业
    company_size = db.Column(db.String(100))                             # 公司规模
    company_type = db.Column(db.String(100))                             # 公司类型
    job_code = db.Column(db.String(100), index=True)                      # 岗位编码
    description = db.Column(db.Text)                                     # 岗位详情
    update_date = db.Column(db.String(50))                               # 更新日期
    company_description = db.Column(db.Text)                             # 公司简介
    source_url = db.Column(db.String(500))                               # 来源地址
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联：一个岗位可以有一个画像
    profile = db.relationship('JobProfile', backref='job', uselist=False, lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'address': self.address,
            'salary_range': self.salary_range,
            'company_name': self.company_name,
            'industry': self.industry,
            'company_size': self.company_size,
            'company_type': self.company_type,
            'description': self.description,
        }


class JobProfile(db.Model):
    """岗位画像 - 由LLM从岗位数据中提取的结构化能力要求"""
    __tablename__ = 'job_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=True)
    
    # 基础信息
    position_name = db.Column(db.String(200), nullable=False, index=True)  # 标准岗位名称
    category = db.Column(db.String(100))                                    # 岗位类别
    level = db.Column(db.String(50))                                        # 岗位层级(初级/中级/高级/专家)
    
    # 结构化能力要求（JSON格式存储）
    technical_skills = db.Column(db.Text, default='[]')      # 专业技能要求
    certificates = db.Column(db.Text, default='[]')           # 证书要求
    education_req = db.Column(db.String(100))                 # 学历要求
    experience_req = db.Column(db.String(100))                # 经验要求
    
    # 软技能评分要求（1-10分）
    innovation_ability = db.Column(db.Float, default=5.0)     # 创新能力要求
    learning_ability = db.Column(db.Float, default=5.0)       # 学习能力要求
    pressure_resistance = db.Column(db.Float, default=5.0)    # 抗压能力要求
    communication_skill = db.Column(db.Float, default=5.0)    # 沟通能力要求
    teamwork_ability = db.Column(db.Float, default=5.0)       # 团队协作能力
    internship_ability = db.Column(db.Float, default=5.0)     # 实习/实践能力要求
    
    # 维度权重（用于人岗匹配加权计算）
    weight_basic = db.Column(db.Float, default=0.2)           # 基础要求权重
    weight_skill = db.Column(db.Float, default=0.35)          # 职业技能权重
    weight_quality = db.Column(db.Float, default=0.25)        # 职业素养权重
    weight_potential = db.Column(db.Float, default=0.2)       # 发展潜力权重
    
    # 岗位描述摘要
    summary = db.Column(db.Text)                               # 岗位概述
    salary_range = db.Column(db.String(100))                   # 薪资范围
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_technical_skills(self):
        try:
            return json.loads(self.technical_skills) if self.technical_skills else []
        except:
            return []
    
    def set_technical_skills(self, skills):
        self.technical_skills = json.dumps(skills, ensure_ascii=False)
    
    def get_certificates(self):
        try:
            return json.loads(self.certificates) if self.certificates else []
        except:
            return []
    
    def set_certificates(self, certs):
        self.certificates = json.dumps(certs, ensure_ascii=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'position_name': self.position_name,
            'category': self.category,
            'level': self.level,
            'technical_skills': self.get_technical_skills(),
            'certificates': self.get_certificates(),
            'education_req': self.education_req,
            'experience_req': self.experience_req,
            'innovation_ability': self.innovation_ability,
            'learning_ability': self.learning_ability,
            'pressure_resistance': self.pressure_resistance,
            'communication_skill': self.communication_skill,
            'teamwork_ability': self.teamwork_ability,
            'internship_ability': self.internship_ability,
            'weight_basic': self.weight_basic,
            'weight_skill': self.weight_skill,
            'weight_quality': self.weight_quality,
            'weight_potential': self.weight_potential,
            'summary': self.summary,
            'salary_range': self.salary_range,
        }


class JobGraph(db.Model):
    """岗位关联图谱 - 存储岗位间的晋升/换岗关系"""
    __tablename__ = 'job_graphs'
    
    id = db.Column(db.Integer, primary_key=True)
    from_position = db.Column(db.String(200), nullable=False, index=True)  # 源岗位
    to_position = db.Column(db.String(200), nullable=False)                 # 目标岗位
    relation_type = db.Column(db.String(50), nullable=False)               # 关系类型: promotion(晋升)/transfer(换岗)
    description = db.Column(db.Text)                                        # 路径说明
    required_skills = db.Column(db.Text, default='[]')                     # 需要补充的技能
    difficulty = db.Column(db.Integer, default=3)                           # 转换难度(1-5)
    estimated_years = db.Column(db.Float)                                   # 预计所需年限
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        skills = []
        try:
            skills = json.loads(self.required_skills) if self.required_skills else []
        except:
            pass
        return {
            'id': self.id,
            'from_position': self.from_position,
            'to_position': self.to_position,
            'relation_type': self.relation_type,
            'description': self.description,
            'required_skills': skills,
            'difficulty': self.difficulty,
            'estimated_years': self.estimated_years,
        }

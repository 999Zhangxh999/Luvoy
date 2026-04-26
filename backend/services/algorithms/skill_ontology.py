# ============================================
# 技能本体标准化服务 (Skill Ontology & Standardization)
# 技术亮点：可迁移技能映射 / 技能标准化 / 同义词消歧
# ============================================
"""
技能本体说明：
1. 技能标准化：将不同表述映射到标准技能名（如 "JS"→"JavaScript"）
2. 技能分类：将技能归类到领域（前端/后端/数据/管理等）
3. 可迁移技能识别：识别跨岗位通用的核心能力
4. 技能层级：初级→中级→高级技能的演进关系

应用价值：
- 提高技能匹配准确率（>80%）
- 支持跨岗位技能迁移分析
- 减少大模型的"幻觉"输出
"""
import re
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


class SkillOntologyService:
    """
    技能本体服务 - 职业/技能标准化与映射
    
    核心功能：
    1. normalize_skill(): 技能名标准化
    2. get_skill_category(): 获取技能所属领域
    3. find_transferable_skills(): 识别可迁移技能
    4. compute_skill_gap(): 计算技能差距
    """
    
    def __init__(self):
        # ========== 技能同义词映射表 ==========
        self.skill_synonyms = {
            # 编程语言
            'javascript': ['js', 'javascript', 'ecmascript', 'es6', 'es2015'],
            'typescript': ['ts', 'typescript'],
            'python': ['python', 'python3', 'py'],
            'java': ['java', 'jdk', 'j2ee', 'javaee'],
            'golang': ['go', 'golang'],
            'c++': ['c++', 'cpp', 'cplusplus'],
            'c#': ['c#', 'csharp', 'dotnet', '.net'],
            'php': ['php', 'php7', 'php8'],
            'ruby': ['ruby', 'ruby on rails', 'ror'],
            'rust': ['rust', 'rustlang'],
            'swift': ['swift', 'ios开发'],
            'kotlin': ['kotlin', 'kt'],
            
            # 前端框架
            'vue.js': ['vue', 'vue.js', 'vuejs', 'vue3', 'vue2'],
            'react': ['react', 'reactjs', 'react.js'],
            'angular': ['angular', 'angularjs', 'ng'],
            'html/css': ['html', 'css', 'html5', 'css3', 'html/css'],
            'webpack': ['webpack', 'vite', 'rollup', '构建工具'],
            'node.js': ['node', 'nodejs', 'node.js', 'express'],
            
            # 后端框架
            'spring': ['spring', 'springboot', 'spring boot', 'springmvc', 'spring cloud'],
            'django': ['django', 'drf', 'django rest'],
            'flask': ['flask', 'flask框架'],
            'fastapi': ['fastapi', 'fast api'],
            'mybatis': ['mybatis', 'mybatis-plus'],
            
            # 数据库
            'mysql': ['mysql', 'mariadb'],
            'postgresql': ['postgresql', 'postgres', 'pg'],
            'mongodb': ['mongodb', 'mongo'],
            'redis': ['redis', '缓存'],
            'elasticsearch': ['elasticsearch', 'es', 'elk'],
            'oracle': ['oracle', 'oracle数据库'],
            
            # 大数据
            'hadoop': ['hadoop', 'hdfs', 'mapreduce'],
            'spark': ['spark', 'pyspark', 'spark sql'],
            'flink': ['flink', 'apache flink'],
            'hive': ['hive', 'hive sql'],
            'kafka': ['kafka', 'mq', '消息队列'],
            
            # AI/ML
            '机器学习': ['机器学习', 'ml', 'machine learning'],
            '深度学习': ['深度学习', 'dl', 'deep learning'],
            'pytorch': ['pytorch', 'torch'],
            'tensorflow': ['tensorflow', 'tf', 'keras'],
            'nlp': ['nlp', '自然语言处理', 'natural language processing'],
            'cv': ['cv', '计算机视觉', 'computer vision', '图像处理'],
            
            # 运维/云
            'docker': ['docker', '容器', 'dockerfile'],
            'kubernetes': ['kubernetes', 'k8s', 'k8s集群'],
            'linux': ['linux', 'shell', 'bash', 'centos', 'ubuntu'],
            'aws': ['aws', 'amazon web services'],
            'azure': ['azure', '微软云'],
            '阿里云': ['阿里云', 'aliyun', 'oss'],
            'cicd': ['ci/cd', 'cicd', 'jenkins', 'gitlab ci', '持续集成'],
            
            # 软技能
            '沟通能力': ['沟通能力', '沟通', '表达能力', '交流能力'],
            '团队协作': ['团队协作', '团队合作', '协作能力', 'teamwork'],
            '项目管理': ['项目管理', 'pmp', 'scrum', 'agile', '敏捷开发'],
            '领导力': ['领导力', '领导能力', 'leadership', '带团队'],
            '学习能力': ['学习能力', '快速学习', '自学能力'],
            '问题解决': ['问题解决', '解决问题', '分析问题', '问题分析'],
        }
        
        # ========== 技能分类体系 ==========
        self.skill_categories = {
            '编程语言': ['javascript', 'typescript', 'python', 'java', 'golang', 'c++', 'c#', 'php', 'ruby', 'rust', 'swift', 'kotlin'],
            '前端开发': ['vue.js', 'react', 'angular', 'html/css', 'webpack', 'node.js', '小程序'],
            '后端开发': ['spring', 'django', 'flask', 'fastapi', 'mybatis', '微服务'],
            '数据库': ['mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle'],
            '大数据': ['hadoop', 'spark', 'flink', 'hive', 'kafka', '数据仓库', 'etl'],
            '人工智能': ['机器学习', '深度学习', 'pytorch', 'tensorflow', 'nlp', 'cv', '大模型'],
            '云原生/运维': ['docker', 'kubernetes', 'linux', 'aws', 'azure', '阿里云', 'cicd'],
            '测试': ['自动化测试', '性能测试', 'selenium', 'jmeter', '单元测试'],
            '产品/设计': ['产品设计', 'axure', 'figma', 'sketch', 'ui设计', 'ux'],
            '管理/软技能': ['沟通能力', '团队协作', '项目管理', '领导力', '学习能力', '问题解决'],
        }
        
        # ========== 可迁移核心技能 ==========
        self.transferable_skills = {
            '沟通能力', '团队协作', '项目管理', '领导力', '学习能力', '问题解决',
            '数据分析', '逻辑思维', '创新思维', '时间管理', '抗压能力',
        }
        
        # 构建反向索引
        self._build_index()
    
    def _build_index(self):
        """构建同义词反向索引"""
        self._synonym_to_standard = {}
        for standard, synonyms in self.skill_synonyms.items():
            for syn in synonyms:
                self._synonym_to_standard[syn.lower()] = standard
        
        self._standard_to_category = {}
        for category, skills in self.skill_categories.items():
            for skill in skills:
                self._standard_to_category[skill.lower()] = category
    
    def normalize_skill(self, skill: str) -> str:
        """
        技能名标准化
        
        Args:
            skill: 原始技能名
        Returns:
            str: 标准化后的技能名
        """
        if not skill:
            return ''
        
        skill_lower = skill.lower().strip()
        
        # 精确匹配
        if skill_lower in self._synonym_to_standard:
            return self._synonym_to_standard[skill_lower]
        
        # 模糊匹配
        for standard, synonyms in self.skill_synonyms.items():
            for syn in synonyms:
                if syn in skill_lower or skill_lower in syn:
                    return standard
        
        return skill  # 无法标准化则返回原值
    
    def normalize_skills(self, skills: list) -> list:
        """批量标准化技能列表"""
        normalized = []
        seen = set()
        for skill in skills:
            if isinstance(skill, dict):
                skill = skill.get('name', '')
            std = self.normalize_skill(skill)
            if std and std.lower() not in seen:
                seen.add(std.lower())
                normalized.append(std)
        return normalized
    
    def get_skill_category(self, skill: str) -> str:
        """获取技能所属分类"""
        std_skill = self.normalize_skill(skill).lower()
        return self._standard_to_category.get(std_skill, '其他')
    
    def categorize_skills(self, skills: list) -> dict:
        """
        将技能列表按类别分组
        
        Returns:
            dict: {类别: [技能列表]}
        """
        result = defaultdict(list)
        for skill in skills:
            if isinstance(skill, dict):
                skill = skill.get('name', '')
            std = self.normalize_skill(skill)
            cat = self.get_skill_category(std)
            if std not in result[cat]:
                result[cat].append(std)
        return dict(result)
    
    def is_transferable(self, skill: str) -> bool:
        """判断是否为可迁移技能"""
        std = self.normalize_skill(skill).lower()
        return std in self.transferable_skills or self.get_skill_category(skill) == '管理/软技能'
    
    def find_transferable_skills(self, skills: list) -> list:
        """
        从技能列表中识别出可迁移技能
        
        可迁移技能：跨岗位通用的核心能力（沟通/协作/学习/问题解决等）
        """
        return [s for s in self.normalize_skills(skills) if self.is_transferable(s)]
    
    def compute_skill_gap(self, student_skills: list, job_skills: list) -> dict:
        """
        计算标准化后的技能差距
        
        Args:
            student_skills: 学生技能列表
            job_skills: 岗位要求技能列表
        Returns:
            dict: {
                'matched': [...],        # 匹配的技能
                'missing': [...],        # 缺失的技能
                'extra': [...],          # 额外的技能
                'transferable': [...],   # 可迁移技能
                'match_rate': float,
                'category_coverage': {...},
            }
        """
        std_student = set(self.normalize_skills(student_skills))
        std_job = set(self.normalize_skills(job_skills))
        
        matched = list(std_student & std_job)
        missing = list(std_job - std_student)
        extra = list(std_student - std_job)
        transferable = self.find_transferable_skills(list(std_student))
        
        # 按类别分析覆盖度
        job_by_cat = self.categorize_skills(list(std_job))
        student_by_cat = self.categorize_skills(list(std_student))
        
        category_coverage = {}
        for cat, job_cat_skills in job_by_cat.items():
            student_cat_skills = student_by_cat.get(cat, [])
            covered = len(set(job_cat_skills) & set(student_cat_skills))
            total = len(job_cat_skills)
            category_coverage[cat] = {
                'required': job_cat_skills,
                'have': student_cat_skills,
                'coverage': round(covered / total, 2) if total > 0 else 1.0,
            }
        
        match_rate = len(matched) / len(std_job) if std_job else 1.0
        
        return {
            'matched': matched,
            'missing': missing,
            'extra': extra,
            'transferable': transferable,
            'match_rate': round(match_rate, 4),
            'category_coverage': category_coverage,
        }
    
    def suggest_learning_path(self, missing_skills: list) -> list:
        """
        根据缺失技能推荐学习顺序
        
        原则：
        1. 基础技能优先（编程语言 > 框架）
        2. 相关技能聚合学习
        """
        categorized = self.categorize_skills(missing_skills)
        
        # 定义学习优先级
        priority_order = ['编程语言', '后端开发', '前端开发', '数据库', '大数据', '人工智能', '云原生/运维', '测试', '产品/设计', '管理/软技能', '其他']
        
        path = []
        for cat in priority_order:
            if cat in categorized:
                for skill in categorized[cat]:
                    path.append({
                        'skill': skill,
                        'category': cat,
                        'priority': priority_order.index(cat) + 1,
                    })
        
        return path

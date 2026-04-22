#!/usr/bin/env python
"""
添加示例学生数据 - 使用虚构信息
"""
import sys
import os
import json
import random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models.database import db
from models.student import Student, StudentProfile

# 虚构学生数据
FAKE_STUDENTS = [
    {
        "name": "张伟明",
        "gender": "男",
        "age": 23,
        "education": "本科",
        "major": "计算机科学与技术",
        "school": "北京理工大学",
        "graduation_year": 2025,
        "email": "zhangwm@example.com",
        "phone": "138****1234",
        "target_positions": ["前端开发工程师", "全栈开发工程师"],
        "salary_expectation": "15-20K",
        "resume_text": """
张伟明
北京理工大学 | 计算机科学与技术 | 本科
联系方式: zhangwm@example.com

教育经历:
- 北京理工大学 计算机科学与技术 2021-2025
- GPA: 3.6/4.0 专业前15%

技能:
- 前端: React, Vue3, TypeScript, Webpack
- 后端: Node.js, Python, Java
- 数据库: MySQL, MongoDB, Redis

项目经历:
1. 在线教育平台前端开发
   - 使用React+TypeScript开发课程管理系统
   - 实现视频播放器、弹幕、笔记等功能
   
2. 校园二手交易小程序
   - 微信小程序全栈开发
   - 用户量5000+

竞赛获奖:
- 全国大学生程序设计竞赛 省级二等奖
- 计算机设计大赛 省级一等奖
""",
        "profile": {
            "technical_skills": ["React", "Vue3", "TypeScript", "Node.js", "Python", "MySQL"],
            "certificates": ["软件设计师", "英语六级"],
            "project_experience": [
                {"name": "在线教育平台", "role": "前端开发", "description": "React+TypeScript课程管理系统"},
                {"name": "校园二手交易小程序", "role": "全栈开发", "description": "微信小程序开发"}
            ],
            "awards": ["全国大学生程序设计竞赛 省级二等奖", "计算机设计大赛 省级一等奖"],
            "innovation_ability": 7.5,
            "learning_ability": 8.0,
            "pressure_resistance": 7.0,
            "communication_skill": 7.5,
            "teamwork_ability": 8.0,
            "completeness_score": 85,
            "competitiveness_score": 78,
            "overall_evaluation": "技术基础扎实，项目经验丰富，有良好的学习能力和团队协作精神。",
            "strengths": ["前端技术扎实", "有完整项目经验", "竞赛获奖"],
            "weaknesses": ["后端经验相对较少", "大型项目经验不足"]
        }
    },
    {
        "name": "李思琪",
        "gender": "女",
        "age": 24,
        "education": "硕士",
        "major": "软件工程",
        "school": "浙江大学",
        "graduation_year": 2025,
        "email": "lisiqi@example.com",
        "phone": "139****5678",
        "target_positions": ["算法工程师", "机器学习工程师"],
        "salary_expectation": "25-35K",
        "resume_text": """
李思琪
浙江大学 | 软件工程 | 硕士研究生
联系方式: lisiqi@example.com

教育经历:
- 浙江大学 软件工程 硕士 2023-2025
- 南京大学 计算机科学 本科 2019-2023
- GPA: 3.8/4.0 专业前5%

研究方向: 自然语言处理、知识图谱

技能:
- 编程语言: Python, C++, Java
- 深度学习: PyTorch, TensorFlow, Transformers
- 大数据: Spark, Hadoop

论文发表:
1. 基于预训练模型的命名实体识别研究 - CCF B类会议
2. 知识增强的文本分类方法 - 核心期刊

项目经历:
1. 企业智能客服系统
   - 基于BERT的意图识别和槽位填充
   - 上线后准确率提升20%

2. 学术论文推荐系统
   - 构建学术知识图谱
   - 个性化推荐准确率85%

实习经历:
- 阿里巴巴 算法实习生 2024.6-2024.9
  自然语言处理相关项目开发
""",
        "profile": {
            "technical_skills": ["Python", "PyTorch", "TensorFlow", "NLP", "知识图谱", "Spark"],
            "certificates": ["CET-6 620分", "PAT甲级"],
            "project_experience": [
                {"name": "企业智能客服系统", "role": "算法开发", "description": "BERT意图识别"},
                {"name": "学术论文推荐系统", "role": "核心开发", "description": "知识图谱构建"}
            ],
            "internship_experience": [
                {"company": "阿里巴巴", "position": "算法实习生", "duration": "2024.6-2024.9"}
            ],
            "awards": ["CCF B类会议论文", "研究生学业奖学金一等奖"],
            "innovation_ability": 8.5,
            "learning_ability": 9.0,
            "pressure_resistance": 8.0,
            "communication_skill": 7.5,
            "teamwork_ability": 8.0,
            "completeness_score": 92,
            "competitiveness_score": 88,
            "overall_evaluation": "学术背景优秀，有大厂实习经验，算法能力强，适合算法研究相关岗位。",
            "strengths": ["顶会论文发表", "大厂实习经验", "深度学习技术扎实"],
            "weaknesses": ["工程化经验可进一步加强"]
        }
    },
    {
        "name": "王浩然",
        "gender": "男",
        "age": 22,
        "education": "本科",
        "major": "数据科学与大数据技术",
        "school": "华中科技大学",
        "graduation_year": 2025,
        "email": "wanghr@example.com",
        "phone": "137****9012",
        "target_positions": ["数据分析师", "数据工程师"],
        "salary_expectation": "12-18K",
        "resume_text": """
王浩然
华中科技大学 | 数据科学与大数据技术 | 本科
联系方式: wanghr@example.com

教育经历:
- 华中科技大学 数据科学与大数据技术 2021-2025
- GPA: 3.5/4.0

技能:
- 数据分析: Python, SQL, Pandas, NumPy
- 可视化: Tableau, PowerBI, ECharts
- 大数据: Spark, Hive, Flink

项目经历:
1. 电商用户行为分析系统
   - 用户画像构建和RFM模型分析
   - 提供可视化数据报表

2. 股票量化分析工具
   - 基于历史数据的技术指标计算
   - 回测系统开发

竞赛获奖:
- 全国大学生数学建模竞赛 国家二等奖
- 数据分析挑战赛 省级一等奖
""",
        "profile": {
            "technical_skills": ["Python", "SQL", "Pandas", "Tableau", "Spark", "Hive"],
            "certificates": ["数据分析师", "CET-4"],
            "project_experience": [
                {"name": "电商用户行为分析", "role": "数据分析", "description": "用户画像和RFM分析"},
                {"name": "股票量化分析工具", "role": "开发", "description": "技术指标和回测"}
            ],
            "awards": ["全国大学生数学建模竞赛 国家二等奖", "数据分析挑战赛 省级一等奖"],
            "innovation_ability": 7.0,
            "learning_ability": 7.5,
            "pressure_resistance": 7.5,
            "communication_skill": 8.0,
            "teamwork_ability": 7.5,
            "completeness_score": 80,
            "competitiveness_score": 75,
            "overall_evaluation": "数据分析能力出色，有建模竞赛获奖经历，适合数据分析相关岗位。",
            "strengths": ["数据分析技能全面", "建模能力强", "可视化能力好"],
            "weaknesses": ["实习经验不足", "机器学习经验较少"]
        }
    },
    {
        "name": "陈雨涵",
        "gender": "女",
        "age": 23,
        "education": "本科",
        "major": "人工智能",
        "school": "电子科技大学",
        "graduation_year": 2025,
        "email": "chenyh@example.com",
        "phone": "136****3456",
        "target_positions": ["后端开发工程师", "Java开发工程师"],
        "salary_expectation": "14-20K",
        "resume_text": """
陈雨涵
电子科技大学 | 人工智能 | 本科
联系方式: chenyh@example.com

教育经历:
- 电子科技大学 人工智能 2021-2025
- GPA: 3.7/4.0 专业前10%

技能:
- 后端: Java, Spring Boot, Spring Cloud
- 数据库: MySQL, Redis, PostgreSQL
- 中间件: RabbitMQ, Kafka, Elasticsearch

项目经历:
1. 分布式电商系统
   - 微服务架构设计与开发
   - 实现高并发订单处理

2. 智能问答系统后端
   - RESTful API设计
   - 接口响应时间优化50%

实习经历:
- 字节跳动 后端开发实习生 2024.7-2024.10
  参与抖音推荐系统后端开发

竞赛获奖:
- 蓝桥杯程序设计竞赛 省级一等奖
- ACM校赛 银奖
""",
        "profile": {
            "technical_skills": ["Java", "Spring Boot", "MySQL", "Redis", "Kafka", "微服务"],
            "certificates": ["CET-6 580分", "软件设计师"],
            "project_experience": [
                {"name": "分布式电商系统", "role": "后端开发", "description": "微服务架构"},
                {"name": "智能问答系统后端", "role": "后端开发", "description": "API设计与优化"}
            ],
            "internship_experience": [
                {"company": "字节跳动", "position": "后端开发实习生", "duration": "2024.7-2024.10"}
            ],
            "awards": ["蓝桥杯 省级一等奖", "ACM校赛 银奖"],
            "innovation_ability": 7.5,
            "learning_ability": 8.5,
            "pressure_resistance": 8.0,
            "communication_skill": 8.0,
            "teamwork_ability": 8.5,
            "completeness_score": 88,
            "competitiveness_score": 85,
            "overall_evaluation": "后端技术扎实，有大厂实习经验，综合素质优秀。",
            "strengths": ["Java后端技术全面", "有字节实习经验", "竞赛成绩优秀"],
            "weaknesses": ["分布式系统实战经验可加强"]
        }
    },
    {
        "name": "刘子轩",
        "gender": "男",
        "age": 25,
        "education": "硕士",
        "major": "计算机技术",
        "school": "上海交通大学",
        "graduation_year": 2025,
        "email": "liuzx@example.com",
        "phone": "135****7890",
        "target_positions": ["产品经理", "技术产品经理"],
        "salary_expectation": "20-30K",
        "resume_text": """
刘子轩
上海交通大学 | 计算机技术 | 硕士研究生
联系方式: liuzx@example.com

教育经历:
- 上海交通大学 计算机技术 硕士 2023-2025
- 西安交通大学 软件工程 本科 2019-2023
- GPA: 3.6/4.0

技能:
- 产品: Axure, Figma, SQL, Python
- 技术: 了解前后端开发流程
- 数据: 数据分析、用户研究

项目经历:
1. AI教育产品规划
   - 负责产品从0到1设计
   - 用户调研和需求分析
   - DAU增长200%

2. 校园服务APP产品设计
   - 产品原型设计
   - 用户留存率提升30%

实习经历:
- 腾讯 产品实习生 2024.5-2024.9
  参与微信小程序产品迭代
- 美团 产品实习生 2023.6-2023.9
  负责用户增长相关产品

证书:
- PMP项目管理证书
""",
        "profile": {
            "technical_skills": ["Axure", "Figma", "SQL", "Python", "用户研究", "数据分析"],
            "certificates": ["PMP", "CET-6 600分"],
            "project_experience": [
                {"name": "AI教育产品", "role": "产品负责人", "description": "产品从0到1设计"},
                {"name": "校园服务APP", "role": "产品设计", "description": "原型设计与迭代"}
            ],
            "internship_experience": [
                {"company": "腾讯", "position": "产品实习生", "duration": "2024.5-2024.9"},
                {"company": "美团", "position": "产品实习生", "duration": "2023.6-2023.9"}
            ],
            "awards": ["优秀毕业生", "研究生学业奖学金"],
            "innovation_ability": 8.5,
            "learning_ability": 8.0,
            "pressure_resistance": 8.5,
            "communication_skill": 9.0,
            "teamwork_ability": 9.0,
            "completeness_score": 90,
            "competitiveness_score": 86,
            "overall_evaluation": "有丰富的大厂产品实习经验，沟通协作能力强，产品思维清晰。",
            "strengths": ["双大厂实习经验", "PMP证书", "产品sense好"],
            "weaknesses": ["技术深度可进一步加强"]
        }
    }
]


def seed_fake_students():
    """添加虚构学生数据"""
    app = create_app()
    
    with app.app_context():
        print("开始添加虚构学生数据...")
        
        for student_data in FAKE_STUDENTS:
            # 检查是否已存在
            existing = Student.query.filter_by(email=student_data['email']).first()
            if existing:
                print(f"学生 {student_data['name']} 已存在，跳过")
                continue
            
            # 创建学生
            student = Student(
                name=student_data['name'],
                gender=student_data['gender'],
                age=student_data['age'],
                education=student_data['education'],
                major=student_data['major'],
                school=student_data['school'],
                graduation_year=student_data['graduation_year'],
                email=student_data['email'],
                phone=student_data['phone'],
                resume_text=student_data['resume_text'],
                target_positions=json.dumps(student_data['target_positions'], ensure_ascii=False),
                salary_expectation=student_data['salary_expectation']
            )
            db.session.add(student)
            db.session.flush()  # 获取student.id
            
            # 创建画像
            profile_data = student_data['profile']
            profile = StudentProfile(
                student_id=student.id,
                technical_skills=json.dumps(profile_data['technical_skills'], ensure_ascii=False),
                certificates=json.dumps(profile_data['certificates'], ensure_ascii=False),
                project_experience=json.dumps(profile_data['project_experience'], ensure_ascii=False),
                internship_experience=json.dumps(profile_data.get('internship_experience', []), ensure_ascii=False),
                awards=json.dumps(profile_data['awards'], ensure_ascii=False),
                innovation_ability=profile_data['innovation_ability'],
                learning_ability=profile_data['learning_ability'],
                pressure_resistance=profile_data['pressure_resistance'],
                communication_skill=profile_data['communication_skill'],
                teamwork_ability=profile_data['teamwork_ability'],
                completeness_score=profile_data['completeness_score'],
                competitiveness_score=profile_data['competitiveness_score'],
                overall_evaluation=profile_data['overall_evaluation'],
                strengths=json.dumps(profile_data['strengths'], ensure_ascii=False),
                weaknesses=json.dumps(profile_data['weaknesses'], ensure_ascii=False)
            )
            db.session.add(profile)
            
            print(f"✅ 添加学生: {student_data['name']} ({student_data['school']})")
        
        db.session.commit()
        print(f"\n✅ 完成! 共添加 {len(FAKE_STUDENTS)} 个虚构学生数据")


if __name__ == '__main__':
    seed_fake_students()

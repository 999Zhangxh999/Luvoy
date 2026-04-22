#!/usr/bin/env python
"""
清理学生数据 - 只保留虚假学生，删除其他
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models.database import db
from models.student import Student, StudentProfile, CareerReport

# 虚假学生的邮箱（用于识别）
FAKE_EMAILS = [
    'zhangwm@example.com',
    'lisiqi@example.com', 
    'wanghr@example.com',
    'chenyh@example.com',
    'liuzx@example.com',
]

def cleanup_students():
    """删除非虚假学生数据"""
    app = create_app()
    
    with app.app_context():
        # 获取所有学生
        all_students = Student.query.all()
        print(f"当前学生总数: {len(all_students)}")
        
        # 收集要删除的学生ID
        to_delete_ids = []
        for student in all_students:
            if student.email not in FAKE_EMAILS:
                to_delete_ids.append(student.id)
                print(f"标记删除: {student.name} (ID={student.id})")
        
        if not to_delete_ids:
            print("没有需要删除的数据")
            return
        
        # 先删除相关的报告
        CareerReport.query.filter(CareerReport.student_id.in_(to_delete_ids)).delete(synchronize_session=False)
        print("已删除相关报告")
        
        # 删除画像
        StudentProfile.query.filter(StudentProfile.student_id.in_(to_delete_ids)).delete(synchronize_session=False)
        print("已删除画像")
        
        # 删除学生
        Student.query.filter(Student.id.in_(to_delete_ids)).delete(synchronize_session=False)
        print("已删除学生")
        
        db.session.commit()
        
        remaining = Student.query.count()
        print(f"\n✅ 已删除 {len(to_delete_ids)} 条非虚假数据")
        print(f"✅ 剩余 {remaining} 条虚假学生数据")


if __name__ == '__main__':
    cleanup_students()

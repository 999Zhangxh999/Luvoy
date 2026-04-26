#!/usr/bin/env python
"""
数据导入脚本 - 从JSON文件导入岗位数据
"""
import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models.database import db
from models.job import Job, JobProfile

# JSON字段映射到数据库字段
FIELD_MAPPING = {
    "岗位名称": "title",
    "地址": "address",
    "薪资范围": "salary_range",
    "公司名称": "company_name",
    "所属行业": "industry",
    "公司规模": "company_size",
    "公司类型": "company_type",
    "岗位编码": "job_code",
    "岗位详情": "description",
    "更新日期": "update_date",
    "公司详情": "company_description",
    "岗位来源地址": "source_url"
}

def import_jobs_from_json(json_path):
    """从JSON文件导入岗位数据"""
    app = create_app()
    
    with app.app_context():
        # 清空现有数据
        print("清空现有数据...")
        JobProfile.query.delete()
        Job.query.delete()
        db.session.commit()
        
        # 读取JSON文件
        print(f"读取JSON文件: {json_path}")
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"共有 {len(data)} 条记录")
        
        # 批量导入
        batch_size = 500
        imported = 0
        
        for i in range(0, len(data), batch_size):
            batch = data[i:i+batch_size]
            jobs_to_add = []
            
            for item in batch:
                # 映射字段
                job_data = {}
                for cn_field, en_field in FIELD_MAPPING.items():
                    value = item.get(cn_field, '')
                    # 清理HTML标签
                    if value and isinstance(value, str):
                        value = value.replace('<br>', '\n').replace('<br/>', '\n')
                    job_data[en_field] = value
                
                # 跳过没有岗位名称的记录
                if not job_data.get('title'):
                    continue
                
                job = Job(**job_data)
                jobs_to_add.append(job)
            
            db.session.bulk_save_objects(jobs_to_add)
            db.session.commit()
            imported += len(jobs_to_add)
            print(f"已导入: {imported}/{len(data)}")
        
        print(f"\n✅ 导入完成! 共导入 {imported} 条岗位数据")
        return imported

if __name__ == '__main__':
    json_path = r'E:\work\Neo-Mapper-main\tableConvert.com_pn6idf.json'
    if len(sys.argv) > 1:
        json_path = sys.argv[1]
    import_jobs_from_json(json_path)

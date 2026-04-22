# ============================================
# 岗位数据导入脚本
# 将JSON格式的岗位数据导入SQLite数据库
# 使用方法: python import_jobs.py
# ============================================
import json
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models.database import db
from models.job import Job


def import_jobs(json_path: str, batch_size: int = 500):
    """
    从JSON文件导入岗位数据
    
    Args:
        json_path: JSON文件路径
        batch_size: 每批次提交数量
    """
    app = create_app('development')
    
    with app.app_context():
        # 检查是否已有数据
        existing_count = Job.query.count()
        if existing_count > 0:
            print(f"数据库中已有 {existing_count} 条岗位数据。")
            choice = input("是否清空并重新导入？(y/n): ").strip().lower()
            if choice == 'y':
                Job.query.delete()
                db.session.commit()
                print("已清空旧数据。")
            else:
                print("跳过导入。")
                return
        
        # 读取JSON文件
        print(f"正在读取文件: {json_path}")
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"文件中共有 {len(data)} 条记录")
        
        # 批量导入
        imported = 0
        skipped = 0
        seen_codes = set()
        
        for i, item in enumerate(data):
            try:
                code = item.get('岗位编码', '').strip()
                if code in seen_codes:
                    skipped += 1
                    continue
                seen_codes.add(code)

                job = Job(
                    title=item.get('岗位名称', '').strip(),
                    address=item.get('地址', '').strip(),
                    salary_range=item.get('薪资范围', '').strip(),
                    company_name=item.get('公司名称', '').strip(),
                    industry=item.get('所属行业', '').strip(),
                    company_size=item.get('公司规模', '').strip(),
                    company_type=item.get('公司类型', '').strip(),
                    job_code=code or None,
                    description=item.get('岗位详情', '').strip(),
                    update_date=item.get('更新日期', '').strip(),
                    company_description=item.get('公司详情', '').strip(),
                    source_url=item.get('岗位来源地址', '').strip(),
                )
                db.session.add(job)
                imported += 1
            except Exception as e:
                skipped += 1
                if skipped <= 5:
                    print(f"  跳过第{i+1}条: {e}")
            
            # 批量提交
            if (i + 1) % batch_size == 0:
                try:
                    db.session.commit()
                    print(f"  已导入 {imported}/{len(data)} 条...")
                except Exception as e:
                    db.session.rollback()
                    print(f"  批次提交失败: {e}")
        
        # 提交剩余
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"最终提交失败: {e}")
        
        print(f"\n导入完成！")
        print(f"  成功: {imported} 条")
        print(f"  跳过: {skipped} 条")
        print(f"  数据库总数: {Job.query.count()} 条")


def show_stats():
    """显示数据库统计信息"""
    app = create_app('development')
    
    with app.app_context():
        total = Job.query.count()
        if total == 0:
            print("数据库为空，请先导入数据。")
            return
        
        print(f"\n数据库统计:")
        print(f"  岗位总数: {total}")
        
        # 统计岗位名称分布（前20）
        from sqlalchemy import func
        title_stats = db.session.query(
            Job.title, func.count(Job.id)
        ).group_by(Job.title).order_by(func.count(Job.id).desc()).limit(20).all()
        
        print(f"\nTOP 20 岗位名称:")
        for title, count in title_stats:
            print(f"  {title}: {count} 条")


if __name__ == '__main__':
    # 默认JSON文件路径
    default_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..', 'tableConvert.com_pn6idf.json'
    )
    
    json_path = default_path
    if len(sys.argv) > 1:
        json_path = sys.argv[1]
    
    if not os.path.exists(json_path):
        print(f"错误: 文件不存在: {json_path}")
        print(f"请指定正确的JSON文件路径:")
        print(f"  python import_jobs.py <json文件路径>")
        sys.exit(1)
    
    import_jobs(json_path)
    show_stats()

"""诊断职业图谱生成问题"""
from app import create_app
from models.database import db
from models.job import Job, JobProfile, JobGraph
from services.job_graph import JobGraphService

app = create_app()
with app.app_context():
    print("=" * 50)
    print("数据库状态检查")
    print("=" * 50)
    print(f"岗位数据(Jobs): {Job.query.count()} 条")
    print(f"岗位画像(JobProfiles): {JobProfile.query.count()} 条")
    print(f"图谱路径(JobGraph): {JobGraph.query.count()} 条")
    
    # 检查岗位画像
    profiles = JobProfile.query.with_entities(JobProfile.position_name).distinct().all()
    position_names = [p.position_name for p in profiles]
    print(f"\n唯一岗位名称: {len(position_names)} 个")
    
    if not position_names:
        print("\n❌ 错误: 没有岗位画像！请先生成岗位画像再构建图谱。")
    else:
        print("岗位名称列表（前10个）:")
        for name in position_names[:10]:
            print(f"  - {name}")
        
        # 检查现有图谱
        print("\n现有图谱路径:")
        promotions = JobGraph.query.filter_by(relation_type='promotion').all()
        transfers = JobGraph.query.filter_by(relation_type='transfer').all()
        print(f"  晋升路径: {len(promotions)} 条")
        print(f"  转岗路径: {len(transfers)} 条")
        
        if promotions:
            print("\n晋升路径示例（前5条）:")
            for p in promotions[:5]:
                print(f"  {p.from_position} → {p.to_position}")
        
        # 尝试构建图谱
        print("\n" + "=" * 50)
        print("尝试构建图谱...")
        print("=" * 50)
        
        try:
            graph_service = JobGraphService()
            result = graph_service.build_full_graph()
            print(f"\n✅ 成功! 共生成 {result['total']} 条路径")
            print(f"  晋升路径: {len(result['promotion_paths'])} 条")
            print(f"  转岗路径: {len(result['transfer_paths'])} 条")
            
            if result['promotion_paths']:
                print("\n新晋升路径示例:")
                for p in result['promotion_paths'][:3]:
                    print(f"  {p['from_position']} → {p['to_position']}")
                    
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"\n❌ 错误: {type(e).__name__}: {e}")

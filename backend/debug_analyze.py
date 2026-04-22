"""诊断岗位画像生成问题"""
from app import create_app
from models.database import db
from models.job import Job, JobProfile
from services.job_analyzer import JobAnalyzer

app = create_app()
with app.app_context():
    print("Jobs:", Job.query.count())
    print("Profiles:", JobProfile.query.count())

    analyzer = JobAnalyzer()
    jobs = Job.query.all()

    # 去重取样
    best = {}
    existing_titles = set(t[0] for t in db.session.query(JobProfile.position_name).all())
    print("Existing profile titles:", len(existing_titles))

    for j in jobs:
        if j.title in existing_titles:
            continue
        prev = best.get(j.title)
        if prev is None or len(j.description or "") > len(prev.description or ""):
            best[j.title] = j

    candidates = list(best.values())[:3]
    print(f"Unique candidates: {len(candidates)}")
    for c in candidates:
        print(f"  [{c.id}] {c.title} | desc_len={len(c.description or '')}")

    if not candidates:
        print("\nNO CANDIDATES - all titles already have profiles!")
    else:
        print(f"\nTrying to analyze: {candidates[0].title}")
        try:
            profile = analyzer.analyze_single_job(candidates[0])
            print(f"SUCCESS: {profile.position_name} ({profile.category})")
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"\nERROR: {type(e).__name__}: {e}")

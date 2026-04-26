# ============================================
# Flask 纯 REST API 后端
# 基于AI的大学生职业规划智能体
# ============================================
import os
import json
import logging
import time
import markdown
from flask import Flask, request, jsonify, Response, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from config import config_map
from models.database import db
from models.job import Job, JobProfile, JobGraph
from models.student import Student, StudentProfile, MatchResult, CareerReport, User, User, User, User, User, User
from services.llm_client import init_llm
from services.job_analyzer import JobAnalyzer
from services.job_graph import JobGraphService
from services.resume_parser import ResumeParser
from services.matching_engine import MatchingEngine
from services.report_generator import ReportGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app(config_name='default'):
    """应用工厂"""
    # 使用绝对路径指向 dist 目录
    dist_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dist')
    app = Flask(__name__, static_folder=dist_path, static_url_path='')
    app.config.from_object(config_map.get(config_name, config_map['default']))

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    # 初始化JWT
    jwt = JWTManager(app)

    with app.app_context():
        try:
            init_llm(app)
            logger.info("LLM客户端初始化成功")
        except Exception as e:
            logger.warning(f"LLM客户端初始化失败: {e}")

    register_api(app)
    return app


def allowed_file(filename):
    from config import Config
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def register_api(app):
        """注册所有 REST API 路由"""

        # 复用重量级服务，避免每个请求重复加载模型导致超时
        service_cache = {
            'matching_engine': None,
            'report_generator': None,
        }

        def get_matching_engine() -> MatchingEngine:
            if service_cache['matching_engine'] is None:
                service_cache['matching_engine'] = MatchingEngine()
            return service_cache['matching_engine']

        def get_report_generator() -> ReportGenerator:
            if service_cache['report_generator'] is None:
                service_cache['report_generator'] = ReportGenerator()
            return service_cache['report_generator']

        # 权限控制装饰器
        def admin_required():
            def wrapper(fn):
                @jwt_required()
                def decorated_view(*args, **kwargs):
                    current_user = get_jwt_identity()
                    user = User.query.filter_by(username=current_user).first()
                    if not user or user.role != 'admin':
                        return jsonify({'success': False, 'message': '管理员权限 required'}), 403
                    return fn(*args, **kwargs)
                return decorated_view
            return wrapper

        # 用户认证相关API
        @app.route('/api/auth/register', methods=['POST'])
        def api_register():
            """用户注册"""
            try:
                data = request.get_json()
                username = data.get('username')
                email = data.get('email')
                password = data.get('password')

                if not username or not email or not password:
                    return jsonify({'success': False, 'message': '缺少必要参数'}), 400

                # 检查用户名是否已存在
                if User.query.filter_by(username=username).first():
                    return jsonify({'success': False, 'message': '用户名已存在'}), 400

                # 检查邮箱是否已存在
                if User.query.filter_by(email=email).first():
                    return jsonify({'success': False, 'message': '邮箱已存在'}), 400

                # 创建新用户
                password_hash = generate_password_hash(password)
                user = User(
                    username=username,
                    email=email,
                    password_hash=password_hash,
                    role='user'  # 默认角色
                )
                db.session.add(user)
                db.session.commit()

                return jsonify({
                    'success': True,
                    'message': '注册成功',
                    'data': user.to_dict()
                })
            except Exception as e:
                logger.error(f"注册失败: {e}")
                return jsonify({'success': False, 'message': str(e)}), 500

        @app.route('/api/auth/login', methods=['POST'])
        def api_login():
            """用户登录"""
            try:
                data = request.get_json()
                username = data.get('username')
                password = data.get('password')

                if not username or not password:
                    return jsonify({'success': False, 'message': '缺少必要参数'}), 400

                # 查找用户
                user = User.query.filter_by(username=username).first()
                if not user or not check_password_hash(user.password_hash, password):
                    return jsonify({'success': False, 'message': '用户名或密码错误'}), 401

                # 创建访问令牌
                access_token = create_access_token(identity=user.username)

                return jsonify({
                    'success': True,
                    'message': '登录成功',
                    'data': {
                        'access_token': access_token,
                        'user': user.to_dict()
                    }
                })
            except Exception as e:
                logger.error(f"登录失败: {e}")
                return jsonify({'success': False, 'message': str(e)}), 500

        @app.route('/api/auth/me', methods=['GET'])
        @jwt_required()
        def api_get_current_user():
            """获取当前用户信息"""
            try:
                current_user = get_jwt_identity()
                user = User.query.filter_by(username=current_user).first()
                if not user:
                    return jsonify({'success': False, 'message': '用户不存在'}), 404
                return jsonify({
                    'success': True,
                    'data': user.to_dict()
                })
            except Exception as e:
                logger.error(f"获取用户信息失败: {e}")
                return jsonify({'success': False, 'message': str(e)}), 500

    # ---------- 前端 SPA 入口 ----------
    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.errorhandler(404)
    def fallback(e):
        if request.path.startswith('/api/'):
            return jsonify({'success': False, 'message': 'Not Found'}), 404
        return send_from_directory(app.static_folder, 'index.html')

    # ============ 统计概览 ============
    @app.route('/api/stats')
    def api_stats():
        return jsonify({
            'total_jobs': Job.query.count(),
            'total_profiles': JobProfile.query.count(),
            'total_students': Student.query.count(),
            'total_reports': CareerReport.query.count(),
            'total_graph_paths': JobGraph.query.count(),
        })

    # ============ 岗位数据 ============
    @app.route('/api/jobs')
    def api_jobs():
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')

        query = Job.query
        if search:
            query = query.filter(Job.title.contains(search))

        pagination = query.order_by(Job.id).paginate(
            page=page, per_page=per_page, error_out=False)

        return jsonify({
            'items': [j.to_dict() for j in pagination.items],
            'total': pagination.total,
            'page': pagination.page,
            'pages': pagination.pages,
        })

    @app.route('/api/jobs/<int:job_id>')
    def api_job_detail(job_id):
        job = Job.query.get_or_404(job_id)
        return jsonify(job.to_dict())

    # ============ 岗位画像 ============
    @app.route('/api/jobs/profiles')
    def api_job_profiles():
        category = request.args.get('category', '')
        query = JobProfile.query
        if category:
            query = query.filter_by(category=category)
        profiles = query.all()

        categories = [c[0] for c in
                      db.session.query(JobProfile.category).distinct().all()
                      if c[0]]

        return jsonify({
            'profiles': [p.to_dict() for p in profiles],
            'categories': categories,
        })

    @app.route('/api/jobs/profiles/<int:profile_id>')
    def api_job_profile_detail(profile_id):
        profile = JobProfile.query.get_or_404(profile_id)
        graph_service = JobGraphService()
        career_path = graph_service.get_career_path_for_position(profile.position_name)
        data = profile.to_dict()
        data['career_path'] = career_path
        return jsonify(data)

    @app.route('/api/jobs/analyze', methods=['POST'])
    def api_analyze_jobs():
        try:
            count = request.json.get('count', 10) if request.is_json else 10
            analyzer = JobAnalyzer()
            # 取足够多的岗位以覆盖更多不同标题
            jobs = Job.query.all()
            profiles = analyzer.batch_analyze_jobs(jobs, max_count=count)
            total = JobProfile.query.count()
            return jsonify({
                'success': True,
                'message': f'本次生成 {len(profiles)} 个岗位画像，累计 {total} 个',
                'data': [p.to_dict() for p in profiles]
            })
        except Exception as e:
            logger.error(f"岗位分析失败: {e}", exc_info=True)
            return jsonify({'success': False, 'message': str(e)}), 500

    @app.route('/api/jobs/analyze-one/<int:job_id>', methods=['POST'])
    def api_analyze_single_job(job_id):
        try:
            job = Job.query.get_or_404(job_id)
            analyzer = JobAnalyzer()
            profile = analyzer.analyze_single_job(job)
            return jsonify({
                'success': True,
                'message': f'岗位画像生成成功: {profile.position_name}',
                'data': profile.to_dict()
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

    # ============ 职业图谱 ============
    @app.route('/api/graph/data')
    def api_graph_data():
        graph_service = JobGraphService()
        data = graph_service.get_graph_data()
        paths = graph_service.get_all_paths()
        return jsonify({**data, 'paths': paths})

    @app.route('/api/graph/build', methods=['POST'])
    def api_build_graph():
        try:
            graph_service = JobGraphService()
            result = graph_service.build_full_graph()
            return jsonify({
                'success': True,
                'message': f'图谱构建完成，共 {result["total"]} 条路径',
                'data': result
            })
        except Exception as e:
            logger.error(f"图谱构建失败: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500

    # ============ 学生管理 ============
    @app.route('/api/students')
    @jwt_required()
    def api_students():
        students = Student.query.order_by(Student.created_at.desc()).all()
        result = []
        for s in students:
            d = s.to_dict()
            d['has_profile'] = StudentProfile.query.filter_by(student_id=s.id).first() is not None
            d['has_report'] = CareerReport.query.filter_by(student_id=s.id).first() is not None
            d['match_count'] = MatchResult.query.filter_by(student_id=s.id).count()
            result.append(d)
        return jsonify(result)

    @app.route('/api/students', methods=['POST'])
    @jwt_required()
    def api_create_student():
        try:
            parser = ResumeParser()
            resume_text = request.form.get('resume_text', '')
            resume_parse_warning = None

            if 'resume_file' in request.files:
                file = request.files['resume_file']
                if file and file.filename and allowed_file(file.filename):
                    # 提取原始扩展名（secure_filename可能丢失中文文件名的扩展名）
                    original_ext = os.path.splitext(file.filename)[1].lower()
                    # 生成安全文件名：UUID + 原始扩展名
                    import uuid
                    safe_filename = f"{uuid.uuid4()}{original_ext}"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
                    file.save(filepath)
                    logger.info(f"文件上传成功: {file.filename} -> {safe_filename}")
                    parsed = parser.parse_file(filepath)
                    if parsed:
                        resume_text = parsed
                    else:
                        # PDF解析失败，可能是扫描版
                        resume_parse_warning = '简历文件解析为空（可能是扫描版PDF），请手动填写简历内容或上传文本格式简历'
                        logger.warning(f"简历解析为空: {safe_filename}")

            form = request.form.to_dict()
            form['resume_text'] = resume_text
            student = parser.create_student_from_form(form)

            result = {
                'success': True,
                'message': f'学生创建成功 (ID: {student.id})',
                'data': student.to_dict()
            }
            if resume_parse_warning:
                result['warning'] = resume_parse_warning
            
            return jsonify(result)
        except Exception as e:
            logger.error(f"创建学生失败: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500

    @app.route('/api/students/<int:sid>', methods=['DELETE'])
    @admin_required()
    def api_delete_student(sid):
        """删除学生及其所有关联数据"""
        try:
            student = Student.query.get_or_404(sid)
            # 删除关联的匹配结果
            MatchResult.query.filter_by(student_id=sid).delete()
            # 删除关联的报告
            CareerReport.query.filter_by(student_id=sid).delete()
            # 删除关联的画像
            StudentProfile.query.filter_by(student_id=sid).delete()
            # 删除学生
            db.session.delete(student)
            db.session.commit()
            logger.info(f"学生删除成功: {student.name} (ID={sid})")
            return jsonify({'success': True, 'message': f'学生 {student.name} 已删除'})
        except Exception as e:
            db.session.rollback()
            logger.error(f"删除学生失败: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500

    @app.route('/api/students/<int:sid>')
    @jwt_required()
    def api_student_detail(sid):
        student = Student.query.get_or_404(sid)
        profile = StudentProfile.query.filter_by(student_id=sid).first()
        matches = MatchResult.query.filter_by(
            student_id=sid
        ).order_by(MatchResult.overall_score.desc()).all()

        enriched = []
        for mr in matches:
            jp = JobProfile.query.get(mr.job_profile_id)
            d = mr.to_dict()
            d['job_name'] = jp.position_name if jp else '未知'
            d['job_category'] = jp.category if jp else ''
            enriched.append(d)

        report = CareerReport.query.filter_by(student_id=sid).first()

        return jsonify({
            'student': student.to_dict(),
            'profile': profile.to_dict() if profile else None,
            'match_results': enriched,
            'report': report.to_dict() if report else None,
        })

    @app.route('/api/students/<int:sid>/generate-profile', methods=['POST'])
    @jwt_required()
    def api_gen_profile(sid):
        try:
            student = Student.query.get_or_404(sid)
            parser = ResumeParser()
            profile = parser.generate_student_profile(student)
            return jsonify({
                'success': True,
                'message': '学生画像生成成功',
                'data': profile.to_dict()
            })
        except Exception as e:
            logger.error(f"学生画像生成失败: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500

    # ============ 人岗匹配 ============
    @app.route('/api/matching/<int:sid>')
    def api_matching_results(sid):
        engine = MatchingEngine()
        results = engine.get_match_results(sid)
        return jsonify([r.to_dict() if hasattr(r, 'to_dict') else r for r in results])

    @app.route('/api/matching/<int:sid>/run', methods=['POST'])
    def api_run_matching(sid):
        try:
            payload = request.get_json(silent=True) or {}
            top_n = int(payload.get('top_n', 5))
            strategy = payload.get('strategy', 'two_stage')
            recall_k = int(payload.get('recall_k', min(max(top_n * 3, 6), 20)))
            use_ensemble = bool(payload.get('use_ensemble', True))
            max_workers = int(payload.get('max_workers', 5))

            engine = get_matching_engine()
            started_at = time.time()

            if strategy == 'full':
                results = engine.match_student_to_all_jobs(sid, top_n=top_n, max_workers=max_workers)
                algorithm_used = 'full_llm'
            elif hasattr(engine, 'match_two_stage'):
                results = engine.match_two_stage(
                    sid,
                    recall_k=recall_k,
                    top_n=top_n,
                    use_ensemble=use_ensemble,
                )
                algorithm_used = 'two_stage'
            else:
                results = engine.match_student_to_all_jobs(sid, top_n=top_n, max_workers=max_workers)
                algorithm_used = 'fallback_full_llm'

            elapsed = round(time.time() - started_at, 2)
            
            # 丰富返回数据，添加岗位信息
            enriched_results = []
            for r in results:
                data = r.to_dict()
                jp = JobProfile.query.get(r.job_profile_id)
                if jp:
                    data['job_name'] = jp.position_name
                    data['job_category'] = jp.category
                    data['job_level'] = jp.level
                    data['job_salary'] = jp.salary_range
                else:
                    data['job_name'] = '未知岗位'
                    data['job_category'] = ''
                    data['job_level'] = ''
                    data['job_salary'] = ''
                enriched_results.append(data)
            
            return jsonify({
                'success': True,
                'message': f'匹配完成，共 {len(results)} 条结果',
                'algorithm_used': algorithm_used,
                'elapsed_seconds': elapsed,
                'data': enriched_results
            })
        except Exception as e:
            logger.error(f"人岗匹配失败: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500

    @app.route('/api/matching/<int:sid>/single/<int:pid>', methods=['POST'])
    def api_match_single(sid, pid):
        try:
            engine = get_matching_engine()
            result = engine.match_student_to_job(sid, pid)
            return jsonify({'success': True, 'data': result.to_dict()})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

    # ============ 报告 ============
    @app.route('/api/reports/<int:sid>')
    def api_report(sid):
        report = CareerReport.query.filter_by(student_id=sid).first()
        if not report:
            return jsonify({'success': False, 'message': '暂无报告'}), 404

        report_html = markdown.markdown(
            report.full_report or '',
            extensions=['tables', 'fenced_code', 'toc']
        )
        data = report.to_dict()
        data['report_html'] = report_html
        return jsonify(data)

    @app.route('/api/reports/<int:sid>/generate', methods=['POST'])
    def api_generate_report(sid):
        try:
            # 若无匹配结果，自动先执行快速匹配，避免报告接口直接500
            existing_count = MatchResult.query.filter_by(student_id=sid).count()
            auto_matched = False
            if existing_count == 0:
                engine = get_matching_engine()
                if hasattr(engine, 'match_two_stage'):
                    engine.match_two_stage(sid, recall_k=12, top_n=5, use_ensemble=True)
                else:
                    engine.match_student_to_all_jobs(sid, top_n=5, max_workers=5)
                auto_matched = True

            generator = get_report_generator()
            report = generator.generate_full_report(sid)
            return jsonify({
                'success': True,
                'message': '报告生成成功' + ('（已自动先执行匹配）' if auto_matched else ''),
                'data': report.to_dict()
            })
        except Exception as e:
            logger.error(f"报告生成失败: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500

    @app.route('/api/reports/<int:rid>/polish', methods=['POST'])
    def api_polish_report(rid):
        try:
            generator = ReportGenerator()
            report = generator.polish_report(rid)
            return jsonify({
                'success': True,
                'message': '报告润色完成',
                'data': report.to_dict()
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

    @app.route('/api/reports/<int:rid>/update-section', methods=['POST'])
    def api_update_section(rid):
        try:
            section = request.json.get('section')
            content = request.json.get('content')
            generator = ReportGenerator()
            generator.update_report_section(rid, section, content)
            return jsonify({'success': True, 'message': '章节更新成功'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

    @app.route('/api/reports/<int:rid>/export/<fmt>')
    def api_report_export(rid, fmt):
        generator = ReportGenerator()
        try:
            if fmt == 'html':
                html = generator.export_html(rid)
                return Response(html, mimetype='text/html',
                                headers={'Content-Disposition':
                                         f'attachment; filename=report_{rid}.html'})
            elif fmt == 'markdown':
                md = generator.export_markdown(rid)
                return Response(md, mimetype='text/markdown',
                                headers={'Content-Disposition':
                                         f'attachment; filename=report_{rid}.md'})
            else:
                return jsonify({'success': False, 'message': '不支持的格式'}), 400
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

    # ============ 高级算法接口 ============
    
    @app.route('/api/matching/<int:sid>/run-advanced', methods=['POST'])
    def api_run_advanced_matching(sid):
        """
        执行高级双阶段匹配（融合TF-IDF召回 + LLM精排 + AHP重排）
        """
        try:
            data = request.get_json() or {}
            top_n = data.get('top_n', 5)
            use_ahp = data.get('use_ahp', True)
            
            engine = MatchingEngine()
            
            # 检查是否支持高级算法
            algo_info = engine.get_algorithm_info()
            
            if algo_info.get('advanced_available'):
                results = engine.match_two_stage(sid, recall_k=20, rerank_top_n=top_n)
                algorithm_used = 'two_stage_matching'
            else:
                results = engine.match_student_to_all_jobs(sid, top_n=top_n)
                algorithm_used = 'basic_llm_matching'
            
            return jsonify({
                'success': True,
                'message': f'高级匹配完成，共 {len(results)} 条结果',
                'algorithm_used': algorithm_used,
                'algorithm_info': algo_info,
                'data': [r.to_dict() for r in results]
            })
        except Exception as e:
            logger.error(f"高级人岗匹配失败: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500
    
    @app.route('/api/matching/<int:sid>/skill-analysis')
    def api_skill_analysis(sid):
        """
        获取学生技能差距分析（使用技能本体服务）
        """
        try:
            pid = request.args.get('job_profile_id', type=int)
            engine = get_matching_engine()
            
            # 获取技能分析
            analysis = engine.get_skill_analysis(sid, pid)
            
            return jsonify({
                'success': True,
                'data': analysis
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    
    @app.route('/api/graph/find-path', methods=['POST'])
    def api_graph_find_path():
        """
        使用图算法查找职业发展路径
        """
        try:
            data = request.get_json()
            from_pos = data.get('from_position')
            to_pos = data.get('to_position')
            
            if not from_pos or not to_pos:
                return jsonify({'success': False, 'message': '请提供from_position和to_position'}), 400
            
            graph_service = JobGraphService()
            
            # 尝试使用高级图算法
            if hasattr(graph_service, 'find_optimal_path'):
                result = graph_service.find_optimal_path(from_pos, to_pos)
            else:
                result = graph_service.get_career_path_for_position(from_pos)
            
            return jsonify({
                'success': True,
                'data': result
            })
        except Exception as e:
            logger.error(f"路径查找失败: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500
    
    @app.route('/api/graph/all-paths', methods=['POST'])
    def api_graph_all_paths():
        """
        查找两个岗位之间的所有可能路径
        """
        try:
            data = request.get_json()
            from_pos = data.get('from_position')
            to_pos = data.get('to_position')
            max_depth = data.get('max_depth', 4)
            
            graph_service = JobGraphService()
            
            if hasattr(graph_service, 'find_all_career_paths'):
                paths = graph_service.find_all_career_paths(from_pos, to_pos, max_depth)
                return jsonify({
                    'success': True,
                    'data': paths
                })
            else:
                return jsonify({
                    'success': False,
                    'message': '高级图算法模块未加载'
                }), 400
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    
    @app.route('/api/graph/position-importance')
    def api_position_importance():
        """
        获取岗位重要性排名（基于PageRank）
        """
        try:
            graph_service = JobGraphService()
            
            if hasattr(graph_service, 'get_position_importance'):
                importance = graph_service.get_position_importance()
                return jsonify({
                    'success': True,
                    'algorithm': 'PageRank',
                    'data': importance
                })
            else:
                return jsonify({
                    'success': False,
                    'message': '高级图算法模块未加载'
                }), 400
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    
    @app.route('/api/graph/job-clusters')
    def api_job_clusters():
        """
        获取岗位聚类结果（社区发现）
        """
        try:
            graph_service = JobGraphService()
            
            if hasattr(graph_service, 'discover_job_clusters'):
                clusters = graph_service.discover_job_clusters()
                return jsonify({
                    'success': True,
                    'algorithm': 'Community Detection',
                    'data': clusters
                })
            else:
                return jsonify({
                    'success': False,
                    'message': '高级图算法模块未加载'
                }), 400
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    
    @app.route('/api/graph/reachable/<position>')
    def api_reachable_positions(position):
        """
        获取从某岗位出发可达的所有岗位
        """
        try:
            max_hops = request.args.get('max_hops', 2, type=int)
            graph_service = JobGraphService()
            
            if hasattr(graph_service, 'get_reachable_positions'):
                reachable = graph_service.get_reachable_positions(position, max_hops)
                return jsonify({
                    'success': True,
                    'data': reachable
                })
            else:
                return jsonify({
                    'success': False,
                    'message': '高级图算法模块未加载'
                }), 400
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    
    @app.route('/api/graph/recommend/<position>')
    def api_career_recommend(position):
        """
        智能推荐职业发展方向
        """
        try:
            graph_service = JobGraphService()
            
            if hasattr(graph_service, 'recommend_career_development'):
                recommend = graph_service.recommend_career_development(position)
                return jsonify({
                    'success': True,
                    'data': recommend
                })
            else:
                # 降级到基础推荐
                result = graph_service.get_career_path_for_position(position)
                return jsonify({
                    'success': True,
                    'data': result
                })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    
    @app.route('/api/graph/statistics')
    def api_graph_statistics():
        """
        获取图谱统计信息
        """
        try:
            graph_service = JobGraphService()
            
            if hasattr(graph_service, 'get_graph_statistics'):
                stats = graph_service.get_graph_statistics()
            else:
                stats = {
                    'total_paths': JobGraph.query.count(),
                    'promotion_paths': JobGraph.query.filter_by(relation_type='promotion').count(),
                    'transfer_paths': JobGraph.query.filter_by(relation_type='transfer').count(),
                }
            
            return jsonify({
                'success': True,
                'data': stats
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    
    @app.route('/api/algorithms/info')
    def api_algorithms_info():
        """
        获取当前可用的算法信息（完整版）
        """
        try:
            engine = get_matching_engine()
            algo_info = engine.get_algorithm_info()
            
            # 添加图谱算法信息
            graph_service = JobGraphService()
            graph_algo_info = graph_service.get_algorithm_info()
            
            algo_info['graph_algorithms'] = graph_algo_info.get('algorithms', [])
            algo_info['graph_services'] = {
                'dijkstra': hasattr(graph_service, 'find_optimal_path'),
                'pagerank': hasattr(graph_service, 'get_position_importance'),
                'community_detection': hasattr(graph_service, 'discover_job_clusters'),
                'mdp_planner': graph_algo_info.get('mdp_planner', False),
                'graph_embedding': graph_algo_info.get('graph_embedding', False),
            }
            
            return jsonify({
                'success': True,
                'data': algo_info
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    
    # ==================== MDP职业规划API ====================
    
    @app.route('/api/career/mdp-strategy')
    def api_mdp_strategy():
        """
        获取MDP最优职业发展策略
        
        Query Params:
            position: 当前岗位名称
        """
        try:
            position = request.args.get('position')
            if not position:
                return jsonify({'success': False, 'message': '缺少position参数'}), 400
            
            graph_service = JobGraphService()
            result = graph_service.get_optimal_career_strategy(position)
            
            if 'error' in result:
                return jsonify({'success': False, 'message': result['error']}), 400
            
            return jsonify({'success': True, 'data': result})
        except Exception as e:
            logger.error(f"MDP策略查询失败: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500
    
    @app.route('/api/career/trajectory')
    def api_career_trajectory():
        """
        规划完整职业发展轨迹
        
        Query Params:
            position: 当前岗位名称
            horizon: 规划步数（默认5）
        """
        try:
            position = request.args.get('position')
            horizon = int(request.args.get('horizon', 5))
            
            if not position:
                return jsonify({'success': False, 'message': '缺少position参数'}), 400
            
            graph_service = JobGraphService()
            result = graph_service.plan_career_trajectory(position, horizon)
            
            if 'error' in result:
                return jsonify({'success': False, 'message': result['error']}), 400
            
            return jsonify({'success': True, 'data': result})
        except Exception as e:
            logger.error(f"职业轨迹规划失败: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500
    
    # ==================== 图嵌入API ====================
    
    @app.route('/api/positions/similar')
    def api_similar_positions():
        """
        使用图嵌入找到相似岗位
        
        Query Params:
            position: 岗位名称
            top_k: 返回数量（默认5）
        """
        try:
            position = request.args.get('position')
            top_k = int(request.args.get('top_k', 5))
            
            if not position:
                return jsonify({'success': False, 'message': '缺少position参数'}), 400
            
            graph_service = JobGraphService()
            result = graph_service.get_similar_positions(position, top_k)
            
            if 'error' in result:
                return jsonify({'success': False, 'message': result['error']}), 400
            
            return jsonify({'success': True, 'data': result})
        except Exception as e:
            logger.error(f"相似岗位查询失败: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500
    
    @app.route('/api/positions/clusters')
    def api_position_clusters():
        """
        基于图嵌入对岗位进行聚类
        
        Query Params:
            n_clusters: 聚类数量（默认5）
        """
        try:
            n_clusters = int(request.args.get('n_clusters', 5))
            
            graph_service = JobGraphService()
            result = graph_service.cluster_positions_by_embedding(n_clusters)
            
            if 'error' in result:
                return jsonify({'success': False, 'message': result['error']}), 400
            
            return jsonify({'success': True, 'data': result})
        except Exception as e:
            logger.error(f"岗位聚类失败: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500
    
    # ==================== 贝叶斯优化API ====================
    
    @app.route('/api/match/optimize-weights', methods=['POST'])
    def api_optimize_weights():
        """
        使用贝叶斯优化自动调优匹配权重
        
        Body:
            student_id: 学生ID（用于评估）
            n_iterations: 迭代次数（默认20）
        """
        try:
            data = request.get_json() or {}
            student_id = data.get('student_id')
            n_iterations = data.get('n_iterations', 20)
            
            if not student_id:
                return jsonify({'success': False, 'message': '缺少student_id参数'}), 400
            
            engine = MatchingEngine()
            result = engine.optimize_weights_bayesian(student_id, n_iterations)
            
            if 'error' in result:
                return jsonify({'success': False, 'message': result['error']}), 400
            
            return jsonify({'success': True, 'data': result})
        except Exception as e:
            logger.error(f"贝叶斯优化失败: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500
    
    @app.route('/api/graph/algorithm-info')
    def api_graph_algorithm_info():
        """获取图谱算法信息"""
        try:
            graph_service = JobGraphService()
            info = graph_service.get_algorithm_info()
            return jsonify({'success': True, 'data': info})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    
    @app.route('/api/reports/<int:sid>/generate-advanced', methods=['POST'])
    def api_generate_advanced_report(sid):
        """
        使用Multi-Agent模式生成报告
        """
        try:
            data = request.get_json() or {}
            use_multi_agent = data.get('use_multi_agent', True)
            
            generator = ReportGenerator()
            report = generator.generate_full_report(sid, use_multi_agent=use_multi_agent)
            
            return jsonify({
                'success': True,
                'message': '报告生成成功',
                'mode': 'multi_agent' if use_multi_agent else 'traditional',
                'data': report.to_dict()
            })
        except Exception as e:
            logger.error(f"高级报告生成失败: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500

    # ============ 系统设置 ============
    @app.route('/api/settings', methods=['GET'])
    def api_get_settings():
        key = app.config.get('LLM_API_KEY', '')
        return jsonify({
            'api_key_masked': key[:8] + '****' if len(key) > 8 else '****',
            'base_url': app.config.get('LLM_BASE_URL', ''),
            'model': app.config.get('LLM_MODEL', ''),
            'temperature': app.config.get('LLM_TEMPERATURE', 0.7),
            'max_tokens': app.config.get('LLM_MAX_TOKENS', 4096),
        })

    # ============ AI 助手对话 ============
    @app.route('/api/chat', methods=['POST'])
    def api_chat():
        """AI助手对话接口，用于简历中心的智能助手"""
        try:
            from services.llm_client import get_llm
            llm = get_llm()
            if not llm:
                return jsonify({'success': False, 'message': 'LLM未配置'}), 500

            data = request.get_json()
            user_message = (data.get('message') or '').strip()
            context = data.get('context', {})
            if not user_message:
                return jsonify({'success': False, 'message': '消息不能为空'}), 400

            # 构建系统提示
            system_prompt = (
                '你是Luvoy职业规划系统的AI助手"小智"。你的主要职能：\n'
                "1. 帮助用户管理简历（上传、解析、优化建议）\n"
                "2. 分析学生档案数据，给出职业规划建议\n"
                "3. 解答关于就业、求职、简历撰写的问题\n"
                "4. 推荐适合的岗位匹配策略\n\n"
                "回复要求：简洁友好，适当使用emoji，每次回复控制在200字以内。\n"
                "如果用户问到具体操作（如删除、上传），告诉用户在页面上如何操作。\n"
            )

            # 附加上下文
            if context.get('student_count') is not None:
                system_prompt += f"\n当前系统数据：共{context['student_count']}名学生"
            if context.get('profile_count') is not None:
                system_prompt += f"，{context['profile_count']}人已有画像"
            if context.get('match_count') is not None:
                system_prompt += f"，{context['match_count']}人已匹配"

            messages = [{'role': 'system', 'content': system_prompt}]

            # 附加历史消息(最多6轮)
            history = data.get('history', [])
            for msg in history[-12:]:
                role = msg.get('role', 'user')
                if role in ('user', 'assistant'):
                    messages.append({'role': role, 'content': msg.get('content', '')})

            messages.append({'role': 'user', 'content': user_message})

            reply = llm.chat(messages, temperature=0.8, max_tokens=512)
            return jsonify({'success': True, 'reply': reply})
        except Exception as e:
            logger.error(f"AI对话失败: {e}")
            return jsonify({'success': False, 'message': f'AI对话失败: {str(e)}'}), 500

    @app.route('/api/settings', methods=['POST'])
    @admin_required()
    def api_update_settings():
        try:
            data = request.get_json()
            if data.get('api_key') and '****' not in data['api_key']:
                app.config['LLM_API_KEY'] = data['api_key']
            if data.get('base_url'):
                app.config['LLM_BASE_URL'] = data['base_url']
            if data.get('model'):
                app.config['LLM_MODEL'] = data['model']

            init_llm(app)
            return jsonify({'success': True, 'message': 'LLM配置更新成功'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

    # ==================== 扩展算法API ====================
    
    @app.route('/api/algorithms/extended-info')
    def api_extended_algorithms_info():
        """获取所有扩展算法的可用性状态"""
        try:
            from services.algorithms import (
                ATTENTION_AVAILABLE, DEEP_MATCHING_AVAILABLE,
                MCTS_AVAILABLE, RL_AVAILABLE, MOO_AVAILABLE,
                KG_AVAILABLE, CAREER_AI_AVAILABLE, get_available_algorithms
            )
            
            return jsonify({
                'success': True,
                'data': get_available_algorithms()
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    
    @app.route('/api/career/mcts-search', methods=['POST'])
    def api_mcts_career_search():
        """
        使用蒙特卡洛树搜索探索最优职业路径
        
        Body:
            start_position: 起始岗位
            target_position: 目标岗位（可选）
            num_simulations: 模拟次数（默认100）
            exploration_weight: 探索权重（默认1.4）
        """
        try:
            from services.algorithms import CareerMCTSPlanner, MCTS_AVAILABLE
            
            if not MCTS_AVAILABLE:
                return jsonify({'success': False, 'message': 'MCTS模块未加载'}), 400
            
            data = request.get_json() or {}
            start_position = data.get('start_position')
            target_position = data.get('target_position')
            num_simulations = data.get('num_simulations', 100)
            
            if not start_position:
                return jsonify({'success': False, 'message': '请提供start_position'}), 400
            
            # 从图谱获取职业转换数据
            graph_service = JobGraphService()
            paths = JobGraph.query.all()
            career_paths = [{
                'from_position': p.from_position,
                'to_position': p.to_position,
                'difficulty': p.difficulty,
                'relation_type': p.relation_type,
                'required_skills': p.required_skills or []
            } for p in paths]
            
            # 创建MCTS规划器
            planner = CareerMCTSPlanner(variant='puct')
            planner.build_career_tree(career_paths)
            
            result = planner.plan_career_path(
                current_position=start_position,
                target_position=target_position,
                num_simulations=num_simulations,
                time_limit=5.0
            )
            
            return jsonify({
                'success': True,
                'algorithm': 'Monte Carlo Tree Search',
                'data': result
            })
        except Exception as e:
            logger.error(f"MCTS搜索失败: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500
    
    @app.route('/api/career/rl-recommend', methods=['POST'])
    def api_rl_career_recommend():
        """
        使用强化学习推荐职业发展动作
        
        Body:
            current_position: 当前岗位
            current_skills: 当前技能列表
            training_episodes: 训练轮数（默认50）
        """
        try:
            from services.algorithms import CareerRLPlanner, RL_AVAILABLE
            
            if not RL_AVAILABLE:
                return jsonify({'success': False, 'message': '强化学习模块未加载'}), 400
            
            data = request.get_json() or {}
            current_position = data.get('current_position')
            current_skills = data.get('current_skills', [])
            training_episodes = data.get('training_episodes', 50)
            algorithm = data.get('algorithm', 'double-q')
            
            if not current_position:
                return jsonify({'success': False, 'message': '请提供current_position'}), 400
            
            # 从图谱构建环境
            paths = JobGraph.query.all()
            career_paths = [{
                'from_position': p.from_position,
                'to_position': p.to_position,
                'difficulty': p.difficulty,
                'relation_type': p.relation_type
            } for p in paths]
            
            # 创建RL规划器
            planner = CareerRLPlanner(algorithm=algorithm)
            planner.build_environment(career_paths)
            
            # 训练
            rl_result = planner.train(num_episodes=training_episodes)
            
            return jsonify({
                'success': True,
                'algorithm': f'Reinforcement Learning ({algorithm})',
                'data': {
                    'current_position': current_position,
                    'optimal_path': rl_result.optimal_path,
                    'expected_return': rl_result.expected_return,
                    'policy': {k: v for k, v in (rl_result.policy or {}).items()},
                    'convergence_history': rl_result.convergence_history[-20:] if rl_result.convergence_history else [],
                    'iterations': rl_result.iterations,
                    'algorithm_name': rl_result.algorithm
                }
            })
        except Exception as e:
            logger.error(f"RL推荐失败: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500
    
    @app.route('/api/career/multi-objective', methods=['POST'])
    def api_multi_objective_optimize():
        """
        多目标职业优化（薪资/发展/平衡权衡）
        
        Body:
            current_skills: 当前技能列表
            salary_weight: 薪资权重 (0-1)
            growth_weight: 成长权重 (0-1)
            balance_weight: 工作生活平衡权重 (0-1)
            num_positions: 推荐岗位数量
        """
        try:
            from services.algorithms import CareerMultiObjectiveOptimizer, MOO_AVAILABLE
            
            if not MOO_AVAILABLE:
                return jsonify({'success': False, 'message': '多目标优化模块未加载'}), 400
            
            data = request.get_json() or {}
            current_skills = data.get('current_skills', [])
            salary_weight = data.get('salary_weight', 1.0)
            growth_weight = data.get('growth_weight', 1.0)
            balance_weight = data.get('balance_weight', 1.0)
            num_positions = data.get('num_positions', 3)
            
            # 获取岗位数据
            job_profiles = JobProfile.query.all()
            positions = []
            position_data = {}
            
            for jp in job_profiles:
                positions.append(jp.position_name)
                # 解析薪资范围
                salary = 15000
                if jp.salary_range:
                    try:
                        parts = jp.salary_range.replace('k', '').replace('K', '').split('-')
                        if len(parts) == 2:
                            salary = (float(parts[0]) + float(parts[1])) / 2 * 1000
                    except:
                        pass
                
                position_data[jp.position_name] = {
                    'salary': salary,
                    'growth_potential': 7,
                    'work_life_balance': 6,
                    'required_skills': jp.get_technical_skills(),
                }
            
            optimizer = CareerMultiObjectiveOptimizer(algorithm='nsga2')
            optimizer.load_career_data(positions, position_data)
            optimizer.set_preferences(
                salary_weight=salary_weight,
                growth_weight=growth_weight,
                balance_weight=balance_weight
            )
            
            result = optimizer.optimize_career_portfolio(
                current_skills=current_skills,
                num_positions=num_positions,
                population_size=30,
                num_generations=50
            )
            
            return jsonify({
                'success': True,
                'algorithm': 'NSGA-II Multi-Objective Optimization',
                'data': result
            })
        except Exception as e:
            logger.error(f"多目标优化失败: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500
    
    @app.route('/api/knowledge-graph/build', methods=['POST'])
    def api_build_knowledge_graph():
        """
        构建职业技能知识图谱
        """
        try:
            from services.algorithms import CareerKnowledgeGraphReasoner, KG_AVAILABLE
            
            if not KG_AVAILABLE:
                return jsonify({'success': False, 'message': '知识图谱模块未加载'}), 400
            
            # 从岗位画像和图谱构建知识图谱
            kg = CareerKnowledgeGraphReasoner()
            
            # 构建知识图谱数据
            job_profiles = JobProfile.query.all()
            paths = JobGraph.query.all()
            career_paths = [{
                'from_position': p.from_position,
                'to_position': p.to_position,
                'difficulty': p.difficulty,
                'relation_type': p.relation_type,
                'required_skills': p.get_required_skills() if hasattr(p, 'get_required_skills') else []
            } for p in paths]
            
            # 岗位技能数据
            for jp in job_profiles:
                for skill in jp.get_technical_skills():
                    kg.kg.add_triple(jp.position_name, 'requires_skill', skill)
            
            kg.build_career_kg(career_paths)
            
            # 训练嵌入
            kg.train_embeddings(num_epochs=100)
            
            return jsonify({
                'success': True,
                'message': '知识图谱构建完成',
                'data': {
                    'num_entities': len(kg.kg.entities),
                    'num_relations': len(kg.kg.relations),
                    'num_triples': len(kg.kg.triples)
                }
            })
        except Exception as e:
            logger.error(f"知识图谱构建失败: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500
    
    @app.route('/api/knowledge-graph/predict-link', methods=['POST'])
    def api_predict_link():
        """
        知识图谱链接预测
        
        Body:
            head: 头实体（如岗位名）
            relation: 关系类型
            top_k: 返回数量
        """
        try:
            from services.algorithms import CareerKnowledgeGraphReasoner, KG_AVAILABLE
            
            if not KG_AVAILABLE:
                return jsonify({'success': False, 'message': '知识图谱模块未加载'}), 400
            
            data = request.get_json() or {}
            head = data.get('head')
            relation = data.get('relation', 'requires_skill')
            top_k = data.get('top_k', 5)
            
            if not head:
                return jsonify({'success': False, 'message': '请提供head实体'}), 400
            
            # 构建并训练知识图谱
            kg = CareerKnowledgeGraphReasoner()
            
            # 从数据库加载数据
            job_profiles = JobProfile.query.all()
            paths = JobGraph.query.all()
            career_paths = [{
                'from_position': p.from_position,
                'to_position': p.to_position,
                'relation_type': p.relation_type,
                'required_skills': []
            } for p in paths]
            
            for jp in job_profiles:
                for skill in jp.get_technical_skills():
                    kg.kg.add_triple(jp.position_name, 'requires_skill', skill)
            
            kg.build_career_kg(career_paths)
            kg.train_embeddings(num_epochs=50)
            
            # 使用预测职业转换来做链接预测
            predictions = kg.predict_career_transition(head, top_k=top_k)
            result_data = []
            for pred in predictions:
                result_data.append({
                    'head': pred.head,
                    'relation': pred.relation,
                    'predicted_tails': [(t, float(s)) for t, s in pred.predicted_tails],
                    'confidence': pred.confidence
                })
            
            return jsonify({
                'success': True,
                'algorithm': 'TransE Link Prediction',
                'data': result_data
            })
        except Exception as e:
            logger.error(f"链接预测失败: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500
    
    @app.route('/api/matching/<int:sid>/attention-analysis')
    def api_attention_analysis(sid):
        """
        使用注意力机制分析学生与岗位的关键匹配点
        
        Query Params:
            job_profile_id: 岗位画像ID
        """
        try:
            from services.algorithms import SkillAttentionMatcher, ATTENTION_AVAILABLE
            
            if not ATTENTION_AVAILABLE:
                return jsonify({'success': False, 'message': '注意力机制模块未加载'}), 400
            
            job_profile_id = request.args.get('job_profile_id', type=int)
            
            student = Student.query.get_or_404(sid)
            profile = StudentProfile.query.filter_by(student_id=sid).first()
            
            if not profile:
                return jsonify({'success': False, 'message': '学生画像不存在'}), 404
            
            job_profile = JobProfile.query.get(job_profile_id) if job_profile_id else None
            
            # 使用注意力机制分析
            matcher = SkillAttentionMatcher()
            
            raw_student_skills = profile.get_technical_skills() if profile else []
            # 学生技能可能是dict列表，提取技能名称
            student_skills = [s['name'] if isinstance(s, dict) else str(s) for s in raw_student_skills]
            job_skills = [s['name'] if isinstance(s, dict) else str(s) for s in (job_profile.get_technical_skills() if job_profile else [])]
            
            result = matcher.compute_match_score(
                student_skills=student_skills,
                job_requirements=job_skills
            )
            
            return jsonify({
                'success': True,
                'algorithm': 'Skill Attention Mechanism',
                'data': result
            })
        except Exception as e:
            logger.error(f"注意力分析失败: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500
    
    @app.route('/api/matching/<int:sid>/deep-match', methods=['POST'])
    def api_deep_match(sid):
        """
        使用深度学习模型进行人岗匹配
        
        Body:
            job_profile_ids: 岗位ID列表（可选，默认匹配所有）
            model_type: 模型类型 (two_tower / deep_cross)
        """
        try:
            from services.algorithms import CareerDeepMatcher, DEEP_MATCHING_AVAILABLE
            
            if not DEEP_MATCHING_AVAILABLE:
                return jsonify({'success': False, 'message': '深度匹配模块未加载'}), 400
            
            data = request.get_json() or {}
            job_profile_ids = data.get('job_profile_ids')
            model_type = data.get('model_type', 'two_tower')
            
            student = Student.query.get_or_404(sid)
            profile = StudentProfile.query.filter_by(student_id=sid).first()
            
            if not profile:
                return jsonify({'success': False, 'message': '学生画像不存在'}), 404
            
            # 获取岗位
            if job_profile_ids:
                job_profiles = JobProfile.query.filter(JobProfile.id.in_(job_profile_ids)).all()
            else:
                job_profiles = JobProfile.query.limit(20).all()
            
            # 使用深度匹配器
            matcher = CareerDeepMatcher()
            
            # 构建词汇表
            all_skills = set()
            all_positions = []
            for jp in job_profiles:
                all_positions.append(jp.position_name)
                for s in jp.get_technical_skills():
                    skill_name = s['name'] if isinstance(s, dict) else str(s)
                    all_skills.add(skill_name)
            raw_stu_skills = profile.get_technical_skills() if profile else []
            for s in raw_stu_skills:
                skill_name = s['name'] if isinstance(s, dict) else str(s)
                all_skills.add(skill_name)
            
            matcher.build_vocabulary(list(all_skills), all_positions)
            
            jobs_data = [{
                'position_id': str(jp.id),
                'title': jp.position_name,
                'required_skills': [s['name'] if isinstance(s, dict) else str(s) for s in jp.get_technical_skills()],
                'growth_score': 7,
                'balance_score': 6,
                'stability_score': 7,
                'salary': 15000,
            } for jp in job_profiles]
            
            student_skill_names = [s['name'] if isinstance(s, dict) else str(s) for s in raw_stu_skills]
            user_data = {
                'user_id': str(sid),
                'skills': student_skill_names,
                'experience_years': 0,
                'preferences': {},
            }
            
            results = matcher.match(
                user_data=user_data,
                jobs=jobs_data,
                top_k=10,
                use_ensemble=True
            )
            
            return jsonify({
                'success': True,
                'algorithm': f'Deep Matching ({model_type})',
                'data': results
            })
        except Exception as e:
            logger.error(f"深度匹配失败: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500
    
    @app.route('/api/career/ai-recommend', methods=['POST'])
    def api_career_ai_recommend():
        """
        使用职业AI引擎进行智能推荐
        
        Body:
            user_skills: 用户技能列表
            experience_years: 工作年限
            preferences: 偏好设置
            top_k: 推荐数量
        """
        try:
            from services.algorithms import CareerAIEngine, CAREER_AI_AVAILABLE
            
            if not CAREER_AI_AVAILABLE:
                return jsonify({'success': False, 'message': '职业AI引擎未加载'}), 400
            
            data = request.get_json() or {}
            user_skills = data.get('user_skills', [])
            experience_years = data.get('experience_years', 0)
            preferences = data.get('preferences', {})
            top_k = data.get('top_k', 10)
            
            # 加载职业数据
            engine = CareerAIEngine()
            
            job_profiles = JobProfile.query.all()
            careers = [{
                'position_id': str(jp.id),
                'title': jp.position_name,
                'required_skills': jp.get_technical_skills(),
                'optional_skills': [],
                'salary_range': [0, 0],
                'industry': jp.category or '',
                'description': jp.summary or '',
            } for jp in job_profiles]
            
            engine.load_data(careers)
            
            result = engine.recommend(
                user_data={
                    'skills': user_skills,
                    'experience_years': experience_years,
                    'preferences': preferences,
                },
                top_k=top_k
            )
            
            return jsonify({
                'success': True,
                'algorithm': 'Career AI Engine',
                'data': result
            })
        except Exception as e:
            logger.error(f"AI推荐失败: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500


# ============================================
app = create_app('development')

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', '0').lower() in ('1', 'true', 'yes')
    port = int(os.getenv('PORT', '5000'))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode,
        use_reloader=debug_mode,
    )
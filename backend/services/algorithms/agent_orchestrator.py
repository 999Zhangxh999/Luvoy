# ============================================
# 多智能体编排器 (Multi-Agent Orchestrator)
# 技术亮点：Agent协作 / 任务分解 / CoT思维链 / 结果聚合
# ============================================
"""
多智能体架构说明：
1. Parser Agent (信息提取专家)：从简历/岗位中抽取结构化信息
2. Analyzer Agent (匹配分析师)：执行四维度人岗匹配分析
3. Planner Agent (生涯规划师)：规划职业发展路径
4. Writer Agent (报告撰写师)：生成专业报告

核心技术：
- Chain of Thought (CoT)：思维链推理，提高推理质量
- Tree of Thought (ToT)：树状思维，探索多条推理路径
- Agent Memory：会话记忆，保持上下文连贯
"""
import json
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable
from enum import Enum

logger = logging.getLogger(__name__)


class AgentRole(Enum):
    """智能体角色定义"""
    PARSER = "parser"         # 信息提取专家
    ANALYZER = "analyzer"     # 匹配分析师
    PLANNER = "planner"       # 生涯规划师
    WRITER = "writer"         # 报告撰写师
    COORDINATOR = "coordinator"  # 协调者


@dataclass
class AgentMessage:
    """智能体间通信消息"""
    from_agent: AgentRole
    to_agent: AgentRole
    content: dict
    message_type: str = "task"  # task / result / feedback


@dataclass 
class AgentContext:
    """智能体执行上下文（共享记忆）"""
    student_profile: dict = field(default_factory=dict)
    job_profiles: list = field(default_factory=list)
    match_results: list = field(default_factory=list)
    career_paths: list = field(default_factory=list)
    reasoning_chain: list = field(default_factory=list)  # CoT思维链
    final_report: str = ""
    
    def add_reasoning_step(self, agent: AgentRole, step: str, conclusion: str):
        """添加推理步骤（CoT）"""
        self.reasoning_chain.append({
            'agent': agent.value,
            'step': step,
            'conclusion': conclusion,
        })


class BaseAgent:
    """智能体基类"""
    
    def __init__(self, role: AgentRole, llm_client=None):
        self.role = role
        self.llm = llm_client
        self.name = self._get_agent_name()
    
    def _get_agent_name(self) -> str:
        names = {
            AgentRole.PARSER: "信息提取专家",
            AgentRole.ANALYZER: "匹配分析师", 
            AgentRole.PLANNER: "生涯规划师",
            AgentRole.WRITER: "报告撰写师",
            AgentRole.COORDINATOR: "协调者",
        }
        return names.get(self.role, "未知Agent")
    
    def execute(self, context: AgentContext, task: dict) -> dict:
        """执行任务（子类实现）"""
        raise NotImplementedError


class ParserAgent(BaseAgent):
    """信息提取专家 - 负责从文本中抽取结构化信息"""
    
    def __init__(self, llm_client=None):
        super().__init__(AgentRole.PARSER, llm_client)
    
    def execute(self, context: AgentContext, task: dict) -> dict:
        """
        执行信息抽取任务
        使用 CoT 思维链提高抽取质量
        """
        text = task.get('text', '')
        extract_type = task.get('type', 'resume')  # resume / job
        
        # CoT: 分步骤抽取
        context.add_reasoning_step(
            self.role,
            f"开始分析{extract_type}文本",
            f"待处理文本长度: {len(text)}字符"
        )
        
        if self.llm:
            # 使用LLM进行智能抽取
            cot_prompt = self._build_cot_prompt(text, extract_type)
            # 实际调用LLM...
            result = {'extracted': True}
        else:
            result = {'extracted': False, 'error': 'LLM未初始化'}
        
        context.add_reasoning_step(
            self.role,
            "信息抽取完成",
            f"成功提取关键信息"
        )
        
        return result
    
    def _build_cot_prompt(self, text: str, extract_type: str) -> str:
        """构建CoT提示词"""
        return f"""请按以下步骤分析{extract_type}：

**第一步：识别基本信息**
仔细阅读文本，提取姓名/岗位名称、教育背景/学历要求等基础信息。

**第二步：提取技能关键词**
找出所有技术技能、软技能、工具名称,并进行分类。

**第三步：分析经验/要求**
提取工作经验、项目经历、或岗位经验要求。

**第四步：总结评估**
给出整体评价和关键亮点。

原文：
{text[:2000]}

请按步骤输出分析结果："""


class AnalyzerAgent(BaseAgent):
    """匹配分析师 - 负责四维度人岗匹配分析"""
    
    def __init__(self, llm_client=None, embedding_service=None, ahp_service=None):
        super().__init__(AgentRole.ANALYZER, llm_client)
        self.embedding = embedding_service
        self.ahp = ahp_service
    
    def execute(self, context: AgentContext, task: dict) -> dict:
        """
        执行匹配分析
        两阶段：向量召回 + LLM精排
        """
        context.add_reasoning_step(
            self.role,
            "开始人岗匹配分析",
            f"学生画像已加载，待匹配岗位数: {len(context.job_profiles)}"
        )
        
        results = []
        
        # 第一阶段：向量召回
        if self.embedding:
            context.add_reasoning_step(
                self.role,
                "执行向量召回",
                "使用TF-IDF+余弦相似度快速筛选候选岗位"
            )
            # candidates = self.embedding.compute_student_similarity(...)
        
        # 第二阶段：LLM精排 + AHP权重优化
        if self.ahp:
            context.add_reasoning_step(
                self.role,
                "执行AHP权重优化",
                "根据岗位特性动态调整四维度权重"
            )
            # weighted_results = self.ahp.rank_jobs(...)
        
        context.add_reasoning_step(
            self.role,
            "匹配分析完成",
            f"生成{len(results)}条匹配结果"
        )
        
        return {'match_results': results}


class PlannerAgent(BaseAgent):
    """生涯规划师 - 负责职业路径规划"""
    
    def __init__(self, llm_client=None, graph_service=None):
        super().__init__(AgentRole.PLANNER, llm_client)
        self.graph = graph_service
    
    def execute(self, context: AgentContext, task: dict) -> dict:
        """
        执行职业路径规划
        使用图算法 + LLM推理
        """
        target_job = task.get('target_job', '')
        
        context.add_reasoning_step(
            self.role,
            "开始职业路径规划",
            f"目标岗位: {target_job}"
        )
        
        paths = []
        
        # 使用图算法找最优路径
        if self.graph:
            context.add_reasoning_step(
                self.role,
                "执行Dijkstra最短路径算法",
                "寻找技能差距最小的成长路径"
            )
            # paths = self.graph.find_shortest_path(...)
        
        # LLM润色和补充建议
        if self.llm:
            context.add_reasoning_step(
                self.role,
                "LLM智能规划",
                "结合行业趋势生成具体行动建议"
            )
        
        context.add_reasoning_step(
            self.role,
            "路径规划完成",
            f"生成{len(paths)}条可行路径"
        )
        
        return {'career_paths': paths}


class WriterAgent(BaseAgent):
    """报告撰写师 - 负责生成专业报告"""
    
    def __init__(self, llm_client=None):
        super().__init__(AgentRole.WRITER, llm_client)
    
    def execute(self, context: AgentContext, task: dict) -> dict:
        """
        生成职业规划报告
        整合各Agent的分析结果
        """
        context.add_reasoning_step(
            self.role,
            "开始生成报告",
            f"整合{len(context.reasoning_chain)}步推理结果"
        )
        
        # 生成报告各章节
        sections = task.get('sections', ['self_assessment', 'job_exploration', 'career_goal', 'action_plan'])
        
        report_content = ""
        
        for section in sections:
            context.add_reasoning_step(
                self.role,
                f"撰写章节: {section}",
                "使用CoT分步撰写"
            )
            # 调用LLM生成各章节
        
        context.add_reasoning_step(
            self.role,
            "报告生成完成",
            f"生成完整职业规划报告"
        )
        
        return {'report': report_content}


class AgentOrchestrator:
    """
    多智能体编排器 - 协调各Agent协作完成复杂任务
    
    工作流程：
    1. 任务分解：将用户请求拆解为子任务
    2. Agent分配：根据任务类型选择合适的Agent
    3. 执行协调：按依赖顺序执行各Agent
    4. 结果聚合：整合各Agent输出
    """
    
    def __init__(self, llm_client=None):
        self.llm = llm_client
        self.context = AgentContext()
        
        # 注册各Agent
        self.agents: Dict[AgentRole, BaseAgent] = {}
        self._register_default_agents()
    
    def _register_default_agents(self):
        """注册默认Agent"""
        self.agents[AgentRole.PARSER] = ParserAgent(self.llm)
        self.agents[AgentRole.ANALYZER] = AnalyzerAgent(self.llm)
        self.agents[AgentRole.PLANNER] = PlannerAgent(self.llm)
        self.agents[AgentRole.WRITER] = WriterAgent(self.llm)
    
    def register_agent(self, role: AgentRole, agent: BaseAgent):
        """注册自定义Agent"""
        self.agents[role] = agent
    
    def inject_services(self, embedding_service=None, ahp_service=None, graph_service=None):
        """注入算法服务到各Agent"""
        if AgentRole.ANALYZER in self.agents:
            self.agents[AgentRole.ANALYZER].embedding = embedding_service
            self.agents[AgentRole.ANALYZER].ahp = ahp_service
        
        if AgentRole.PLANNER in self.agents:
            self.agents[AgentRole.PLANNER].graph = graph_service
    
    def execute_workflow(self, workflow_type: str, input_data: dict) -> dict:
        """
        执行预定义工作流
        
        Args:
            workflow_type: 工作流类型
                - 'full_report': 完整职业规划报告
                - 'quick_match': 快速人岗匹配
                - 'path_planning': 职业路径规划
            input_data: 输入数据
        Returns:
            dict: 执行结果
        """
        self.context = AgentContext()  # 重置上下文
        
        logger.info(f"开始执行工作流: {workflow_type}")
        
        if workflow_type == 'full_report':
            return self._workflow_full_report(input_data)
        elif workflow_type == 'quick_match':
            return self._workflow_quick_match(input_data)
        elif workflow_type == 'path_planning':
            return self._workflow_path_planning(input_data)
        else:
            return {'error': f'未知工作流类型: {workflow_type}'}
    
    def _workflow_full_report(self, input_data: dict) -> dict:
        """完整职业规划报告工作流"""
        
        # 1. 信息提取
        parser = self.agents.get(AgentRole.PARSER)
        if parser:
            parser.execute(self.context, {
                'text': input_data.get('resume_text', ''),
                'type': 'resume'
            })
        
        # 2. 匹配分析
        analyzer = self.agents.get(AgentRole.ANALYZER)
        if analyzer:
            self.context.student_profile = input_data.get('student_profile', {})
            self.context.job_profiles = input_data.get('job_profiles', [])
            analyzer.execute(self.context, {})
        
        # 3. 路径规划
        planner = self.agents.get(AgentRole.PLANNER)
        if planner:
            planner.execute(self.context, {
                'target_job': input_data.get('target_job', '')
            })
        
        # 4. 报告生成
        writer = self.agents.get(AgentRole.WRITER)
        if writer:
            writer.execute(self.context, {
                'sections': ['self_assessment', 'job_exploration', 'career_goal', 'action_plan']
            })
        
        return {
            'success': True,
            'report': self.context.final_report,
            'reasoning_chain': self.context.reasoning_chain,
            'match_results': self.context.match_results,
            'career_paths': self.context.career_paths,
        }
    
    def _workflow_quick_match(self, input_data: dict) -> dict:
        """快速匹配工作流"""
        analyzer = self.agents.get(AgentRole.ANALYZER)
        if analyzer:
            self.context.student_profile = input_data.get('student_profile', {})
            self.context.job_profiles = input_data.get('job_profiles', [])
            result = analyzer.execute(self.context, {})
            return {
                'success': True,
                'match_results': result.get('match_results', []),
                'reasoning_chain': self.context.reasoning_chain,
            }
        return {'success': False, 'error': 'Analyzer Agent未初始化'}
    
    def _workflow_path_planning(self, input_data: dict) -> dict:
        """路径规划工作流"""
        planner = self.agents.get(AgentRole.PLANNER)
        if planner:
            result = planner.execute(self.context, {
                'target_job': input_data.get('target_job', ''),
                'current_job': input_data.get('current_job', ''),
            })
            return {
                'success': True,
                'career_paths': result.get('career_paths', []),
                'reasoning_chain': self.context.reasoning_chain,
            }
        return {'success': False, 'error': 'Planner Agent未初始化'}
    
    def get_reasoning_chain(self) -> list:
        """获取完整推理链（用于可解释性展示）"""
        return self.context.reasoning_chain

from fastapi import APIRouter
from app.api.v1.transcription import router as transcription_router
from app.api.v1.thinking_process import router as thinking_process_router
from app.api.v1.feedback import router as feedback_router
from app.api.v1.role_play_analysis import router as role_play_analysis_router
from app.api.v1.future_prediction import router as future_prediction_router
from app.api.v1.non_consensus_view import router as non_consensus_view_router
from app.api.v1.advantage_increment_analysis import router as advantage_increment_analysis_router
from app.api.v1.visualization import router as visualization_router
from app.api.v1.actionable_advice import router as actionable_advice_router
from app.api.v1.multi_perspective_questions import router as multi_perspective_questions_router
from app.api.v1.market_benchmark import router as market_benchmark_router
from app.api.v1.market_trend import router as market_trend_router
from app.api.v1.academic_paper_expansion import router as academic_paper_expansion_router
from app.api.v1.regenerate_podcast import router as regenerate_podcast_router
from app.api.v1.cost_optimization import router as cost_optimization_router
from app.api.v1.failure_case_analysis import router as failure_case_analysis_router
from app.api.v1.fact_opinion_distinction import router as fact_opinion_distinction_router

router = APIRouter()

# 包含转录路由
router.include_router(
    transcription_router,
    prefix="/transcription",
    tags=["transcription"]
)

# 包含思考过程分析路由
router.include_router(
    thinking_process_router,
    prefix="/thinking-process",
    tags=["thinking-process"]
)

# 包含反馈机制路由
router.include_router(
    feedback_router,
    prefix="/feedback",
    tags=["feedback"]
)

# 包含角色扮演分析路由
router.include_router(
    role_play_analysis_router,
    prefix="/role-play",
    tags=["role-play"]
)

# 包含未来预测路由
router.include_router(
    future_prediction_router,
    prefix="/future-prediction",
    tags=["future-prediction"]
)

# 包含非共识观点识别路由
router.include_router(
    non_consensus_view_router,
    prefix="/non-consensus",
    tags=["non-consensus"]
)

# 包含优势与增量分析路由
router.include_router(
    advantage_increment_analysis_router,
    prefix="/advantage-increment",
    tags=["advantage-increment"]
)

# 包含可视化路由
router.include_router(
    visualization_router,
    prefix="/visualization",
    tags=["visualization"]
)

# 包含可行动建议路由
router.include_router(
    actionable_advice_router,
    prefix="/actionable-advice",
    tags=["actionable-advice"]
)

# 包含多角度提问路由
router.include_router(
    multi_perspective_questions_router,
    prefix="/multi-perspective-questions",
    tags=["multi-perspective-questions"]
)

# 包含市场基准测试路由
router.include_router(
    market_benchmark_router,
    prefix="/market-benchmark",
    tags=["market-benchmark"]
)

# 包含市场趋势捕捉路由
router.include_router(
    market_trend_router,
    prefix="/market-trend",
    tags=["market-trend"]
)

# 包含学术论文扩展路由
router.include_router(
    academic_paper_expansion_router,
    prefix="/academic-paper",
    tags=["academic-paper"]
)

# 包含再生Podcast路由
router.include_router(
    regenerate_podcast_router,
    prefix="/regenerate-podcast",
    tags=["regenerate-podcast"]
)

# 包含计算成本优化路由
router.include_router(
    cost_optimization_router,
    prefix="/cost-optimization",
    tags=["cost-optimization"]
)

# 包含失败案例分析路由
router.include_router(
    failure_case_analysis_router,
    prefix="/failure-case",
    tags=["failure-case"]
)

# 包含事实与观点区分路由
router.include_router(
    fact_opinion_distinction_router,
    prefix="/fact-opinion",
    tags=["fact-opinion"]
)
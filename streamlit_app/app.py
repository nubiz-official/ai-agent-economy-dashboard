"""
AI Agent Economy 플랫폼 타당성 분석 대시보드
종합 타당성: 7.6/10 (76점), 조건부 Go
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# ─── Plotly 공통 레이아웃 ───
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Noto Sans KR, sans-serif", color="#e8eaf2"),
)

MINT = "#00c2a8"
PURPLE = "#8b5cf6"
YELLOW = "#e8b84b"
RED = "#ef4444"
GRAY = "#9ca3af"
BG_CARD = "#101828"
BORDER = "#1e293b"

plotly_config = lambda: {"displayModeBar": False}

# ═══════════════════════════════════════════════════
# 데이터 정의
# ═══════════════════════════════════════════════════

TOTAL_SCORE = 76
GO_DECISION = "조건부 Go"

# 5계층 아키텍처
ARCHITECTURE_LAYERS = [
    {"id": 1, "name": "Compute (물리인프라)", "trl": 9, "desc": "빅테크 과점, GPU/TPU 인프라", "biz": 30},
    {"id": 2, "name": "Identity (정체성)", "trl": 4.5, "desc": "에이전트 DID, 선점 기회", "biz": 85},
    {"id": 3, "name": "Intelligence (인지/도구)", "trl": 8.5, "desc": "MCP 표준, 9700만 DL", "biz": 60},
    {"id": 4, "name": "Payment (결제/경제)", "trl": 5.5, "desc": "스테이블코인, A2A 결제", "biz": 75},
    {"id": 5, "name": "Governance (거버넌스)", "trl": 4.5, "desc": "AI기본법 2026.1 시행", "biz": 80},
]

# 시장 데이터
MARKET_TAM = {
    "global": {"2024": 5.4, "2030": 50, "cagr": 45.8},
    "apac": {"2024": 1.1, "2030": 5.0},
    "som": {"2024": 0.011, "2030": 0.25},
    "korea": {"2025": 2, "2030": 61, "cagr": 175, "unit": "조원"},
}

MARKET_GROWTH = [
    {"year": 2024, "TAM": 5.4, "SAM": 1.1, "SOM": 0.011},
    {"year": 2025, "TAM": 7.9, "SAM": 1.6, "SOM": 0.025},
    {"year": 2026, "TAM": 11.5, "SAM": 2.3, "SOM": 0.055},
    {"year": 2027, "TAM": 16.8, "SAM": 3.0, "SOM": 0.095},
    {"year": 2028, "TAM": 24.5, "SAM": 3.6, "SOM": 0.14},
    {"year": 2029, "TAM": 35.7, "SAM": 4.3, "SOM": 0.19},
    {"year": 2030, "TAM": 50.0, "SAM": 5.0, "SOM": 0.25},
]

ENTERPRISE_ADOPTION = {"2025": 5, "2026": 40, "source": "Gartner"}

# SWOT
SWOT = {
    "강점 (Strengths)": [
        "폭발적 성장 CAGR 41~46%",
        "MCP 표준화 완료",
        "5계층 구조 명확",
        "AI 거래 혁신",
        "빅테크 전면 투자",
    ],
    "약점 (Weaknesses)": [
        "AI 결제 신뢰도 16%",
        "프로젝트 실패율 40%",
        "GPU 인프라 병목",
        "BM 미성숙",
        "법적 주체 불명확",
    ],
    "기회 (Opportunities)": [
        "한국 AI기본법 2026.1",
        "SaaS → Agent-aaS 전환",
        "멀티에이전트 시대",
        "EU-한국 협력",
        "생산성 200% 향상",
    ],
    "위협 (Threats)": [
        "빅테크 독점",
        "투자과열 $220B",
        "규제 불확실",
        "보안 위험",
        "기술변화 속도",
    ],
}

# 재무
INVESTMENT = {
    "total": 45,
    "phase1": 9,
    "phase2_3": 36,
    "bep_month": 18,
    "bep_clients": 67,
}

ROI_SCENARIOS = {
    "낙관": {"roi": 89, "color": MINT},
    "기본": {"roi": 22, "color": YELLOW},
    "비관": {"roi": -33, "color": RED},
}

REVENUE_MODELS = [
    {"name": "플랫폼 구독 (하이브리드)", "share": 40, "price": "월 300만~1000만원"},
    {"name": "API 트랜잭션 수수료", "share": 30, "price": "건당 $0.001~$0.01"},
    {"name": "성과 기반 과금", "share": 15, "price": "$0.99/건"},
    {"name": "컨설팅/구축", "share": 15, "price": "5천만~3억원"},
]

BEP_DATA = {
    "months": list(range(0, 25)),
    "cost": [0, 1.5, 3.0, 4.5, 6.0, 7.5, 9.0, 11.0, 13.0, 15.0, 17.0, 19.0, 21.0,
             23.5, 26.0, 28.5, 31.0, 33.5, 36.0, 38.0, 40.0, 41.5, 43.0, 44.0, 45.0],
    "revenue": [0, 0, 0.1, 0.3, 0.6, 1.0, 1.5, 2.5, 4.0, 6.0, 8.5, 11.5, 15.0,
                19.0, 23.5, 28.5, 33.0, 36.0, 39.0, 42.0, 45.0, 48.5, 52.0, 56.0, 60.0],
}

# KPI
KPIS = [
    {"name": "MRR", "unit": "억원", "p1": 1, "p2": 3, "p3": 5},
    {"name": "고객수", "unit": "개사", "p1": 10, "p2": 30, "p3": 70},
    {"name": "API 트랜잭션", "unit": "만건/일", "p1": 10, "p2": 100, "p3": 1000},
    {"name": "MCP 서버 연동", "unit": "개", "p1": 50, "p2": 200, "p3": 500},
    {"name": "가동률", "unit": "%", "p1": 99.5, "p2": 99.9, "p3": 99.9},
    {"name": "이탈률", "unit": "%", "p1": 5, "p2": 3, "p3": 3},
]

# 리스크
RISKS = [
    {"id": 1, "name": "빅테크 수직통합", "prob": 70, "impact": 90, "grade": "극심", "response": "니치 마켓 집중, 개방형 생태계 전략"},
    {"id": 2, "name": "AI 보안 사고", "prob": 40, "impact": 95, "grade": "극심", "response": "보안 프레임워크 구축, 침투 테스트 상시화"},
    {"id": 3, "name": "규제 급변", "prob": 50, "impact": 80, "grade": "높음", "response": "규제 모니터링 TF, 사전 컴플라이언스"},
    {"id": 4, "name": "프로젝트 실패 40%", "prob": 40, "impact": 85, "grade": "높음", "response": "애자일 MVP, 단계별 검증"},
    {"id": 5, "name": "기술 진부화", "prob": 35, "impact": 70, "grade": "중간", "response": "R&D 투자 20%, 기술 로드맵 분기 갱신"},
    {"id": 6, "name": "핵심 인력 이탈", "prob": 40, "impact": 80, "grade": "높음", "response": "스톡옵션, 기술 문서화, 지식 공유 체계"},
    {"id": 7, "name": "투자 버블", "prob": 30, "impact": 75, "grade": "높음", "response": "보수적 자금 운용, 단계별 투자 집행"},
    {"id": 8, "name": "소비자 신뢰 부족", "prob": 60, "impact": 65, "grade": "높음", "response": "투명성 보고서, 신뢰 지표 공개"},
    {"id": 9, "name": "GPU 병목", "prob": 35, "impact": 60, "grade": "중간", "response": "멀티클라우드 전략, 경량화 모델 개발"},
]

# 경쟁사
COMPETITORS = [
    {"name": "OpenAI", "type": "모델 제공", "maturity": 90, "market_share": 35, "color": MINT},
    {"name": "Anthropic", "type": "모델 제공", "maturity": 85, "market_share": 20, "color": PURPLE},
    {"name": "Google", "type": "모델 제공", "maturity": 88, "market_share": 25, "color": YELLOW},
    {"name": "LangGraph", "type": "프레임워크", "maturity": 70, "market_share": 15, "color": "#06b6d4"},
    {"name": "CrewAI", "type": "프레임워크", "maturity": 60, "market_share": 10, "color": "#f97316"},
    {"name": "AutoGen", "type": "프레임워크", "maturity": 65, "market_share": 12, "color": "#22c55e"},
    {"name": "Salesforce", "type": "애플리케이션", "maturity": 80, "market_share": 18, "color": "#3b82f6"},
    {"name": "삼성SDS", "type": "국내", "maturity": 55, "market_share": 8, "color": "#a855f7"},
    {"name": "네이버", "type": "국내", "maturity": 60, "market_share": 10, "color": "#22c55e"},
    {"name": "NuBiz (우리)", "type": "플랫폼", "maturity": 30, "market_share": 1, "color": RED},
]

# 로드맵
ROADMAP = [
    {
        "phase": "Phase 1", "title": "기반 구축 (MVP)", "period": "0~6개월", "budget": "9억원",
        "tasks": ["MCP 게이트웨이 MVP 개발", "에이전트 오케스트레이션 기본 구현", "파일럿 고객 확보"],
        "milestones": ["MCP 게이트웨이 v1.0 출시", "파일럿 10개사 확보", "MRR 1억원 달성"],
    },
    {
        "phase": "Phase 2", "title": "확장 및 BEP 달성", "period": "6~12개월", "budget": "18억원",
        "tasks": ["AI 결제 인프라 구축", "A2A (Agent-to-Agent) 연동", "기업 고객 30개사 확보"],
        "milestones": ["AI 결제 시스템 런칭", "BEP 달성 (67개사)", "MRR 3억원 달성"],
    },
    {
        "phase": "Phase 3", "title": "풀스케일 상용화", "period": "12~24개월", "budget": "18억원",
        "tasks": ["풀스케일 상용화", "70개사 확보", "해외 확장 (APAC)"],
        "milestones": ["70개사 온보딩 완료", "해외 첫 고객 확보", "MRR 5억원 달성"],
    },
]

# 핵심 메트릭
FEASIBILITY_SCORES = {
    "시장성": {"score": 17, "max": 20, "pct": 85},
    "기술성": {"score": 14, "max": 20, "pct": 70},
    "수익성": {"score": 14, "max": 20, "pct": 70},
    "실행력": {"score": 16, "max": 20, "pct": 80},
    "리스크": {"score": 15, "max": 20, "pct": 75},
}


# ─── Page Config ───
st.set_page_config(
    page_title="AI Agent Economy 플랫폼 타당성 분석",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ───
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;800;900&family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0&display=swap');
html, body, [class*="st-"], h1, h2, h3, h4, h5, h6, p, span, div, li, a, button, label {
    font-family: 'Noto Sans KR', sans-serif !important;
}
[data-testid="stIconMaterial"], [data-testid="stIconMaterial"] * {
    font-family: 'Material Symbols Rounded' !important;
}
h1 { font-weight: 900 !important; }
h2 { font-weight: 700 !important; }
h3 { font-weight: 600 !important; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] { background: transparent !important; }
.stDeployButton {display: none;}
section[data-testid="stSidebar"] { background: #060b16; border-right: 1px solid #1e293b; }
.nav-link {
    display: block; padding: 5px 12px; margin: 2px 0;
    color: #9ca3af; text-decoration: none !important;
    border-radius: 6px; font-size: 0.82rem; transition: all 0.2s ease;
}
.nav-link:hover { color: #00c2a8 !important; background: rgba(0,194,168,0.08); padding-left: 16px; }
.mc {
    background: linear-gradient(135deg, #101828, #1a2540);
    border: 1px solid #1e293b; border-radius: 16px; padding: 24px; text-align: center;
}
.mc-v { font-size: 2rem; font-weight: 900; margin: 8px 0 4px; }
.mc-l { font-size: 0.82rem; color: #9ca3af; }
.hero-card {
    background: linear-gradient(135deg, #0f1729 0%, #1a1040 50%, #0f1729 100%);
    border: 1px solid #2d1b69; border-radius: 20px; padding: 40px; text-align: center;
    position: relative; overflow: hidden;
}
.hero-card::before {
    content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(0,194,168,0.05) 0%, transparent 70%);
}
.score-big { font-size: 4.5rem; font-weight: 900; line-height: 1; }
.go-badge {
    display: inline-block; padding: 6px 20px; border-radius: 30px; font-weight: 700; font-size: 0.9rem;
    background: linear-gradient(135deg, rgba(0,194,168,0.15), rgba(139,92,246,0.15));
    border: 1px solid rgba(0,194,168,0.4); color: #00c2a8; margin-top: 12px;
}
.swot-card {
    border-radius: 14px; padding: 20px; min-height: 200px;
}
.swot-s { background: linear-gradient(135deg, rgba(0,194,168,0.12), rgba(0,194,168,0.04)); border: 1px solid rgba(0,194,168,0.25); }
.swot-w { background: linear-gradient(135deg, rgba(239,68,68,0.12), rgba(239,68,68,0.04)); border: 1px solid rgba(239,68,68,0.25); }
.swot-o { background: linear-gradient(135deg, rgba(139,92,246,0.12), rgba(139,92,246,0.04)); border: 1px solid rgba(139,92,246,0.25); }
.swot-t { background: linear-gradient(135deg, rgba(232,184,75,0.12), rgba(232,184,75,0.04)); border: 1px solid rgba(232,184,75,0.25); }
.swot-title { font-size: 1.1rem; font-weight: 700; margin-bottom: 10px; }
.swot-item { font-size: 0.85rem; color: #d1d5db; padding: 4px 0; }
.risk-critical { color: #ef4444; font-weight: 700; }
.risk-high { color: #f97316; font-weight: 700; }
.risk-medium { color: #e8b84b; font-weight: 600; }
.phase-card {
    border-radius: 14px; padding: 24px; position: relative;
    background: linear-gradient(135deg, #101828, #1a2540);
    border: 1px solid #1e293b;
}
.phase-badge {
    display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700;
    margin-bottom: 8px;
}
.conclusion-card {
    background: linear-gradient(135deg, #101828, #1a2540);
    border-left: 3px solid #00c2a8; border-radius: 0 12px 12px 0;
    padding: 14px 18px; margin: 6px 0; font-size: 0.88rem; color: #d1d5db;
}
.layer-card {
    background: linear-gradient(135deg, #101828, #1a2540);
    border: 1px solid #1e293b; border-radius: 12px; padding: 16px; margin-bottom: 8px;
}
.tab-section { padding-top: 8px; }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ───
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:1.2rem 0 0.5rem;">
        <div style="font-size:1.5rem; font-weight:900; background:linear-gradient(135deg,#00c2a8,#8b5cf6);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent; letter-spacing:2px;">NUBIZ</div>
        <div style="font-size:0.72rem; color:#9ca3af; margin-top:4px;">AI Agent Economy 타당성 분석</div>
    </div>
    <hr style="border-color:#1e293b;">
    """, unsafe_allow_html=True)

    st.markdown("""
    <a class="nav-link" href="#" onclick="clickTab(0);return false;">경영 요약</a>
    <a class="nav-link" href="#" onclick="clickTab(1);return false;">SWOT 분석</a>
    <a class="nav-link" href="#" onclick="clickTab(2);return false;">시장 분석</a>
    <a class="nav-link" href="#" onclick="clickTab(3);return false;">5계층 분석</a>
    <a class="nav-link" href="#" onclick="clickTab(4);return false;">재무 분석</a>
    <a class="nav-link" href="#" onclick="clickTab(5);return false;">리스크 매트릭스</a>
    <a class="nav-link" href="#" onclick="clickTab(6);return false;">KPI 대시보드</a>
    <a class="nav-link" href="#" onclick="clickTab(7);return false;">실행 로드맵</a>
    <script>
    function clickTab(idx){
        const tabs=window.parent.document.querySelectorAll('[data-baseweb="tab"]');
        if(tabs[idx]) tabs[idx].click();
    }
    </script>
    <hr style="border-color:#1e293b;">
    """, unsafe_allow_html=True)

    st.markdown("""
    <a class="nav-link" href="https://www.teamnubiz.com" target="_blank">홈</a>
    <a class="nav-link" href="https://www.teamnubiz.com/projects" target="_blank">프로젝트</a>
    <hr style="border-color:#1e293b;">
    <div style="text-align:center; padding:6px 0;">
        <a href="https://teamnubiz.com" target="_blank" style="color:#00c2a8; text-decoration:none; font-size:0.8rem;">teamnubiz.com</a><br>
        <span style="color:#4b5563; font-size:0.7rem;">contact@teamnubiz.com</span>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# 탭 구성
# ═══════════════════════════════════════════════════

tabs = st.tabs([
    "경영 요약",
    "SWOT 분석",
    "시장 분석",
    "5계층 분석",
    "재무 분석",
    "리스크 매트릭스",
    "KPI 대시보드",
    "실행 로드맵",
])


# ───────────────────────────────────────────────────
# TAB 1: 경영 요약
# ───────────────────────────────────────────────────
def render_executive_summary():
    st.markdown('<div id="executive-summary" class="tab-section"></div>', unsafe_allow_html=True)
    st.markdown("## AI Agent Economy 플랫폼")
    st.markdown(
        '<span style="color:#9ca3af; font-size:0.85rem;">사업 타당성 분석 | 분석일: 2026-03-24</span>',
        unsafe_allow_html=True,
    )
    st.markdown("")

    # 히어로 카드: 종합 점수
    c1, c2 = st.columns([1, 1])
    with c1:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=TOTAL_SCORE,
            number={"suffix": " / 100", "font": {"size": 42, "color": "#e8eaf2"}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#2d3748", "dtick": 20},
                "bar": {"color": MINT, "thickness": 0.3},
                "bgcolor": "#1e293b",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 40], "color": "rgba(239,68,68,0.15)"},
                    {"range": [40, 60], "color": "rgba(232,184,75,0.15)"},
                    {"range": [60, 80], "color": "rgba(0,194,168,0.15)"},
                    {"range": [80, 100], "color": "rgba(139,92,246,0.15)"},
                ],
                "threshold": {
                    "line": {"color": PURPLE, "width": 3},
                    "thickness": 0.8,
                    "value": TOTAL_SCORE,
                },
            },
            title={"text": "타당성 종합 점수", "font": {"size": 16, "color": GRAY}},
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=320, margin=dict(l=40, r=40, t=50, b=40))
        st.plotly_chart(fig, use_container_width=True, config=plotly_config())

    with c2:
        st.markdown(f"""
        <div class="hero-card">
            <div style="font-size:0.85rem; color:{GRAY}; margin-bottom:8px;">Go / No-Go 판정</div>
            <div class="go-badge">{GO_DECISION}</div>
            <div style="margin-top:24px; font-size:0.85rem; color:#d1d5db; line-height:1.7; text-align:left;">
                AI Agent Economy는 2024 $5.4B에서 2030 $50B(CAGR 45.8%)로 급성장하는 시장입니다.
                5계층 아키텍처(Compute-Identity-Intelligence-Payment-Governance) 기반
                플랫폼으로 SaaS에서 Agent-aaS로의 전환을 선도합니다.<br><br>
                <span style="color:{YELLOW};">단, 빅테크 수직통합 대응, AI 결제 신뢰도 확보, 규제 컴플라이언스가 전제 조건입니다.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # 영역별 레이더 차트
    categories = list(FEASIBILITY_SCORES.keys())
    values = [v["pct"] for v in FEASIBILITY_SCORES.values()]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill="toself",
        fillcolor="rgba(0,194,168,0.12)",
        line=dict(color=MINT, width=2),
        name="달성률 (%)",
        text=[f"{v['score']}/{v['max']} ({v['pct']}%)" for v in FEASIBILITY_SCORES.values()],
        hovertemplate="%{theta}<br>%{text}<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True, range=[0, 100],
                gridcolor="rgba(148,163,184,0.1)", linecolor="rgba(148,163,184,0.1)",
                tickfont=dict(size=10, color=GRAY),
            ),
            angularaxis=dict(
                gridcolor="rgba(148,163,184,0.1)", linecolor="rgba(148,163,184,0.1)",
                tickfont=dict(size=12, color="#e8eaf2"),
            ),
        ),
        showlegend=False,
        height=400,
        margin=dict(l=80, r=80, t=50, b=40),
        title=dict(text="영역별 타당성 평가", font=dict(size=16)),
    )
    st.plotly_chart(fig, use_container_width=True, config=plotly_config())

    # 영역별 점수 메트릭 카드
    cols = st.columns(5)
    colors = [MINT, PURPLE, YELLOW, MINT, PURPLE]
    for i, (area, data) in enumerate(FEASIBILITY_SCORES.items()):
        with cols[i]:
            st.markdown(f'''
            <div class="mc">
                <div class="mc-l">{area}</div>
                <div class="mc-v" style="color:{colors[i]};">{data["pct"]}%</div>
                <div class="mc-l">{data["score"]} / {data["max"]}</div>
            </div>
            ''', unsafe_allow_html=True)

    st.markdown("")

    # 핵심 메트릭
    st.markdown("### 핵심 메트릭")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'''
        <div class="mc">
            <div class="mc-l">TAM (2030)</div>
            <div class="mc-v" style="color:{MINT};">$50B</div>
            <div class="mc-l">CAGR 45.8%</div>
        </div>''', unsafe_allow_html=True)
    with m2:
        st.markdown(f'''
        <div class="mc">
            <div class="mc-l">총 투자</div>
            <div class="mc-v" style="color:{PURPLE};">45억원</div>
            <div class="mc-l">24개월</div>
        </div>''', unsafe_allow_html=True)
    with m3:
        st.markdown(f'''
        <div class="mc">
            <div class="mc-l">BEP</div>
            <div class="mc-v" style="color:{YELLOW};">18개월</div>
            <div class="mc-l">67개사 확보시</div>
        </div>''', unsafe_allow_html=True)
    with m4:
        st.markdown(f'''
        <div class="mc">
            <div class="mc-l">기업도입률 (Gartner)</div>
            <div class="mc-v" style="color:{MINT};">5%→40%</div>
            <div class="mc-l">2025 → 2026</div>
        </div>''', unsafe_allow_html=True)


with tabs[0]:
    render_executive_summary()


# ───────────────────────────────────────────────────
# TAB 2: SWOT 분석
# ───────────────────────────────────────────────────
def render_swot():
    st.markdown('<div id="swot" class="tab-section"></div>', unsafe_allow_html=True)
    st.markdown("## SWOT 분석")
    st.markdown('<span style="color:#9ca3af; font-size:0.85rem;">AI Agent Economy 플랫폼의 전략적 포지션</span>', unsafe_allow_html=True)
    st.markdown("")

    swot_configs = [
        ("강점 (Strengths)", "swot-s", MINT),
        ("약점 (Weaknesses)", "swot-w", RED),
        ("기회 (Opportunities)", "swot-o", PURPLE),
        ("위협 (Threats)", "swot-t", YELLOW),
    ]

    row1 = st.columns(2)
    row2 = st.columns(2)
    grid = [row1[0], row1[1], row2[0], row2[1]]

    for i, (key, css_class, color) in enumerate(swot_configs):
        with grid[i]:
            items = SWOT[key]
            items_html = "".join(
                f'<div class="swot-item">- {item}</div>' for item in items
            )
            st.markdown(f'''
            <div class="swot-card {css_class}">
                <div class="swot-title" style="color:{color};">{key}</div>
                {items_html}
            </div>
            ''', unsafe_allow_html=True)


with tabs[1]:
    render_swot()


# ───────────────────────────────────────────────────
# TAB 3: 시장 분석
# ───────────────────────────────────────────────────
def render_market():
    st.markdown('<div id="market" class="tab-section"></div>', unsafe_allow_html=True)
    st.markdown("## 시장 분석")
    st.markdown("")

    # TAM/SAM/SOM 파이
    st.markdown("### TAM / SAM / SOM (2030년 전망)")
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=["TAM (글로벌)", "SAM (아태)", "SOM (목표)"],
        values=[50, 5.0, 0.25],
        hole=0.0,
        marker=dict(colors=["rgba(139,92,246,0.3)", "rgba(0,194,168,0.4)", MINT]),
        textinfo="label+value",
        texttemplate="%{label}<br>$%{value}B",
        textfont=dict(size=13, color="#e8eaf2"),
        hovertemplate="%{label}<br>$%{value}B<extra></extra>",
        sort=False,
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=380,
        showlegend=False,
        margin=dict(l=40, r=40, t=50, b=40),
        annotations=[dict(
            text="SOM<br>$250M",
            x=0.5, y=0.5, font_size=14, font_color=MINT, showarrow=False,
        )],
    )
    st.plotly_chart(fig, use_container_width=True, config=plotly_config())

    # TAM/SAM/SOM 메트릭
    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        st.markdown(f'''
        <div class="mc">
            <div class="mc-l">TAM (글로벌 2030)</div>
            <div class="mc-v" style="color:{PURPLE};">$50B</div>
            <div class="mc-l">2024 $5.4B → CAGR 45.8%</div>
        </div>''', unsafe_allow_html=True)
    with mc2:
        st.markdown(f'''
        <div class="mc">
            <div class="mc-l">SAM (아태 2030)</div>
            <div class="mc-v" style="color:{MINT};">$5.0B</div>
            <div class="mc-l">2024 $1.1B</div>
        </div>''', unsafe_allow_html=True)
    with mc3:
        st.markdown(f'''
        <div class="mc">
            <div class="mc-l">SOM (목표 2030)</div>
            <div class="mc-v" style="color:{YELLOW};">$250M</div>
            <div class="mc-l">2024 $11M</div>
        </div>''', unsafe_allow_html=True)

    st.markdown("")

    # 성장 추이 라인차트
    st.markdown("### 글로벌 시장 성장 추이 ($B)")
    years = [d["year"] for d in MARKET_GROWTH]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=[d["TAM"] for d in MARKET_GROWTH],
        name="TAM", line=dict(color=PURPLE, width=3), mode="lines+markers",
        fill="tozeroy", fillcolor="rgba(139,92,246,0.08)",
    ))
    fig.add_trace(go.Scatter(
        x=years, y=[d["SAM"] for d in MARKET_GROWTH],
        name="SAM", line=dict(color=MINT, width=2), mode="lines+markers",
    ))
    fig.add_trace(go.Scatter(
        x=years, y=[d["SOM"] for d in MARKET_GROWTH],
        name="SOM", line=dict(color=YELLOW, width=2, dash="dot"), mode="lines+markers",
        yaxis="y2",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=420,
        margin=dict(l=40, r=60, t=50, b=40),
        xaxis=dict(dtick=1, gridcolor="rgba(148,163,184,0.08)"),
        yaxis=dict(title="TAM/SAM ($B)", gridcolor="rgba(148,163,184,0.08)"),
        yaxis2=dict(title="SOM ($B)", overlaying="y", side="right", gridcolor="rgba(148,163,184,0.08)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig, use_container_width=True, config=plotly_config())

    st.markdown("")

    # 국내 시장
    st.markdown("### 국내 AI Agent 시장")
    kc1, kc2 = st.columns(2)
    with kc1:
        st.markdown(f'''
        <div class="mc">
            <div class="mc-l">국내 시장 (2025)</div>
            <div class="mc-v" style="color:{MINT};">2조원</div>
            <div class="mc-l">CAGR 175%</div>
        </div>''', unsafe_allow_html=True)
    with kc2:
        st.markdown(f'''
        <div class="mc">
            <div class="mc-l">국내 시장 (2030)</div>
            <div class="mc-v" style="color:{PURPLE};">61조원</div>
            <div class="mc-l">30배 성장</div>
        </div>''', unsafe_allow_html=True)

    st.markdown("")

    # 경쟁사 산점도
    st.markdown("### 경쟁사 포지셔닝 맵")
    fig = go.Figure()
    for comp in COMPETITORS:
        fig.add_trace(go.Scatter(
            x=[comp["maturity"]], y=[comp["market_share"]],
            mode="markers+text",
            marker=dict(size=20 if comp["name"] == "NuBiz (우리)" else 14,
                        color=comp["color"], opacity=0.8,
                        line=dict(width=2 if comp["name"] == "NuBiz (우리)" else 1, color="#e8eaf2")),
            text=[comp["name"]],
            textposition="top center",
            textfont=dict(size=10, color="#e8eaf2"),
            name=comp["name"],
            hovertemplate=f"{comp['name']}<br>유형: {comp['type']}<br>기술 성숙도: {comp['maturity']}<br>시장 점유: {comp['market_share']}%<extra></extra>",
        ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=450,
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis=dict(title="기술 성숙도", range=[0, 100], gridcolor="rgba(148,163,184,0.08)"),
        yaxis=dict(title="시장 점유율 (%)", range=[0, 40], gridcolor="rgba(148,163,184,0.08)"),
        showlegend=False,
    )
    fig.add_hline(y=15, line_dash="dot", line_color="rgba(148,163,184,0.2)")
    fig.add_vline(x=50, line_dash="dot", line_color="rgba(148,163,184,0.2)")
    st.plotly_chart(fig, use_container_width=True, config=plotly_config())


with tabs[2]:
    render_market()


# ───────────────────────────────────────────────────
# TAB 4: 5계층 분석
# ───────────────────────────────────────────────────
def render_architecture():
    st.markdown('<div id="architecture" class="tab-section"></div>', unsafe_allow_html=True)
    st.markdown("## 5계층 아키텍처 분석")
    st.markdown('<span style="color:#9ca3af; font-size:0.85rem;">AI Agent Economy의 5계층 스택: Compute → Identity → Intelligence → Payment → Governance</span>', unsafe_allow_html=True)
    st.markdown("")

    # TRL 바 차트
    layer_names = [l["name"] for l in ARCHITECTURE_LAYERS]
    layer_trls = [l["trl"] for l in ARCHITECTURE_LAYERS]
    layer_colors = [MINT if t >= 7 else YELLOW if t >= 5 else RED for t in layer_trls]

    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("### 계층별 기술 성숙도 (TRL)")
        fig = go.Figure(go.Bar(
            x=layer_trls, y=layer_names, orientation="h",
            marker_color=layer_colors,
            text=[f"TRL {t}" for t in layer_trls],
            textposition="outside", textfont=dict(size=11),
        ))
        fig.update_layout(
            **PLOTLY_LAYOUT,
            height=350,
            margin=dict(l=180, r=60, t=30, b=40),
            xaxis=dict(range=[0, 10], title="TRL Level", gridcolor="rgba(148,163,184,0.08)"),
            yaxis=dict(autorange="reversed"),
        )
        st.plotly_chart(fig, use_container_width=True, config=plotly_config())

    with c2:
        st.markdown("### 사업화 가능성 히트맵")
        layer_biz = [l["biz"] for l in ARCHITECTURE_LAYERS]
        short_names = [f"L{l['id']}" for l in ARCHITECTURE_LAYERS]
        metrics = ["TRL", "사업화"]
        z_data = [layer_trls, layer_biz]
        # 정규화 (0~1)
        z_norm = [
            [t / 9.0 for t in layer_trls],
            [b / 100.0 for b in layer_biz],
        ]

        fig = go.Figure(go.Heatmap(
            z=z_norm,
            x=short_names,
            y=metrics,
            text=[[f"TRL {t}" for t in layer_trls], [f"{b}%" for b in layer_biz]],
            texttemplate="%{text}",
            textfont=dict(size=12),
            colorscale=[[0, "#1e293b"], [0.5, YELLOW], [1, MINT]],
            showscale=False,
            hovertemplate="계층: %{x}<br>지표: %{y}<br>%{text}<extra></extra>",
        ))
        fig.update_layout(
            **PLOTLY_LAYOUT,
            height=350,
            margin=dict(l=80, r=40, t=30, b=40),
            xaxis=dict(tickangle=0),
        )
        st.plotly_chart(fig, use_container_width=True, config=plotly_config())

    st.markdown("")

    # 각 계층 카드
    st.markdown("### 5계층 상세")
    layer_colors_list = [MINT, PURPLE, YELLOW, "#06b6d4", "#f97316"]
    layer_cols = st.columns(5)
    for i, layer in enumerate(ARCHITECTURE_LAYERS):
        with layer_cols[i]:
            trl_color = MINT if layer["trl"] >= 7 else YELLOW if layer["trl"] >= 5 else RED
            st.markdown(f'''
            <div class="layer-card" style="border-top: 3px solid {layer_colors_list[i]};">
                <div style="color:{layer_colors_list[i]}; font-weight:700; font-size:0.85rem;">Layer {layer["id"]}</div>
                <div style="font-weight:700; font-size:0.95rem; margin:4px 0;">{layer["name"]}</div>
                <div style="font-size:0.78rem; color:#9ca3af;">{layer["desc"]}</div>
                <div style="margin-top:10px; display:flex; justify-content:space-between;">
                    <span style="font-size:0.75rem; color:{trl_color};">TRL {layer["trl"]}</span>
                    <span style="font-size:0.75rem; color:{MINT};">사업화 {layer["biz"]}%</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)


with tabs[3]:
    render_architecture()


# ───────────────────────────────────────────────────
# TAB 5: 재무 분석
# ───────────────────────────────────────────────────
def render_finance():
    st.markdown('<div id="finance" class="tab-section"></div>', unsafe_allow_html=True)
    st.markdown("## 재무 분석")
    st.markdown("")

    # ROI 시나리오 카드
    st.markdown("### ROI 시나리오 비교")
    sc_cols = st.columns(3)
    for i, (scenario, data) in enumerate(ROI_SCENARIOS.items()):
        with sc_cols[i]:
            roi_sign = "+" if data["roi"] > 0 else ""
            st.markdown(f'''
            <div class="mc" style="border-top: 3px solid {data["color"]};">
                <div class="mc-l">{scenario} 시나리오</div>
                <div class="mc-v" style="color:{data["color"]};">{roi_sign}{data["roi"]}%</div>
                <div class="mc-l">투자 수익률 (ROI)</div>
            </div>
            ''', unsafe_allow_html=True)

    st.markdown("")

    # ROI 바 차트
    fig = go.Figure()
    scenarios = list(ROI_SCENARIOS.keys())
    rois = [ROI_SCENARIOS[s]["roi"] for s in scenarios]
    colors = [ROI_SCENARIOS[s]["color"] for s in scenarios]

    fig.add_trace(go.Bar(
        x=scenarios, y=rois, marker_color=colors,
        text=[f"{r:+}%" for r in rois], textposition="outside",
        textfont=dict(size=14, color="#e8eaf2"),
    ))
    fig.add_hline(y=0, line_color="rgba(148,163,184,0.3)", line_width=1)
    fig.update_layout(
        **PLOTLY_LAYOUT, height=350,
        margin=dict(l=40, r=40, t=50, b=40),
        yaxis=dict(title="ROI (%)", gridcolor="rgba(148,163,184,0.08)"),
        title=dict(text="시나리오별 ROI", font=dict(size=14)),
    )
    st.plotly_chart(fig, use_container_width=True, config=plotly_config())

    st.markdown("")

    # BEP 라인차트
    st.markdown("### 손익분기점 분석 (누적 비용 vs 누적 수익)")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=BEP_DATA["months"], y=BEP_DATA["cost"],
        name="누적 비용", line=dict(color=RED, width=2, dash="dot"), mode="lines",
    ))
    fig.add_trace(go.Scatter(
        x=BEP_DATA["months"], y=BEP_DATA["revenue"],
        name="누적 수익", line=dict(color=MINT, width=3), mode="lines",
        fill="tonexty", fillcolor="rgba(0,194,168,0.05)",
    ))
    fig.add_vline(x=18, line_dash="dash", line_color=YELLOW,
                  annotation_text="BEP (18개월)", annotation_font_color=YELLOW)
    fig.update_layout(
        **PLOTLY_LAYOUT, height=400,
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis=dict(title="개월", dtick=3, gridcolor="rgba(148,163,184,0.08)"),
        yaxis=dict(title="누적 금액 (억원)", gridcolor="rgba(148,163,184,0.08)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig, use_container_width=True, config=plotly_config())

    st.markdown("")

    # 투자 및 수익모델
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 투자 구조")
        fig = go.Figure(go.Pie(
            labels=["Phase 1 (0-6개월)", "Phase 2-3 (6-24개월)"],
            values=[9, 36],
            marker=dict(colors=[MINT, PURPLE]),
            textinfo="label+percent",
            textfont=dict(size=11, color="#e8eaf2"),
            hole=0.45,
            hovertemplate="%{label}<br>%{value}억원 (%{percent})<extra></extra>",
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=350, showlegend=False,
                          margin=dict(l=20, r=20, t=30, b=20),
                          annotations=[dict(text="총<br>45억원", x=0.5, y=0.5,
                                            font_size=14, font_color=MINT, showarrow=False)])
        st.plotly_chart(fig, use_container_width=True, config=plotly_config())

    with col_b:
        st.markdown("### 수익 모델")
        fig = go.Figure(go.Pie(
            labels=[r["name"] for r in REVENUE_MODELS],
            values=[r["share"] for r in REVENUE_MODELS],
            marker=dict(colors=[MINT, PURPLE, YELLOW, "#06b6d4"]),
            textinfo="label+percent",
            textfont=dict(size=10, color="#e8eaf2"),
            hole=0.45,
            hovertemplate="%{label}<br>비중: %{percent}<extra></extra>",
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=350, showlegend=False,
                          margin=dict(l=20, r=20, t=30, b=20),
                          annotations=[dict(text="수익<br>모델", x=0.5, y=0.5,
                                            font_size=14, font_color=PURPLE, showarrow=False)])
        st.plotly_chart(fig, use_container_width=True, config=plotly_config())

    # 수익 모델 상세 카드
    for rm in REVENUE_MODELS:
        st.markdown(f'''
        <div style="background: linear-gradient(135deg, #101828, #1a2540); border: 1px solid #1e293b;
                    border-radius: 10px; padding: 12px 16px; margin: 6px 0;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-weight:700; font-size:0.9rem; color:{MINT};">{rm["name"]}</span>
                <span style="color:{PURPLE}; font-weight:700;">{rm["share"]}%</span>
            </div>
            <div style="font-size:0.8rem; color:#d1d5db; margin-top:4px;">{rm["price"]}</div>
        </div>
        ''', unsafe_allow_html=True)


with tabs[4]:
    render_finance()


# ───────────────────────────────────────────────────
# TAB 6: 리스크 매트릭스
# ───────────────────────────────────────────────────
def render_risk():
    st.markdown('<div id="risk-matrix" class="tab-section"></div>', unsafe_allow_html=True)
    st.markdown("## 리스크 매트릭스")
    st.markdown("")

    grade_colors = {"극심": RED, "높음": "#f97316", "중간": YELLOW}

    # 산점도 (발생확률 x 영향도)
    st.markdown("### 리스크 히트맵 (발생확률 x 영향도)")
    fig = go.Figure()
    for risk in RISKS:
        gc = grade_colors[risk["grade"]]
        fig.add_trace(go.Scatter(
            x=[risk["prob"]], y=[risk["impact"]],
            mode="markers+text",
            marker=dict(size=22, color=gc, opacity=0.8,
                        line=dict(width=1, color="#e8eaf2")),
            text=[f"R{risk['id']}"],
            textposition="middle center",
            textfont=dict(size=9, color="#ffffff", family="Noto Sans KR"),
            name=f"R{risk['id']}: {risk['name']}",
            hovertemplate=f"R{risk['id']}: {risk['name']}<br>확률: {risk['prob']}%<br>영향도: {risk['impact']}%<br>등급: {risk['grade']}<extra></extra>",
        ))

    # 배경 영역
    fig.add_shape(type="rect", x0=50, y0=70, x1=100, y1=100,
                  fillcolor="rgba(239,68,68,0.06)", line=dict(width=0))
    fig.add_shape(type="rect", x0=30, y0=50, x1=50, y1=100,
                  fillcolor="rgba(249,115,22,0.06)", line=dict(width=0))
    fig.add_shape(type="rect", x0=50, y0=50, x1=100, y1=70,
                  fillcolor="rgba(249,115,22,0.06)", line=dict(width=0))

    fig.update_layout(
        **PLOTLY_LAYOUT, height=480,
        margin=dict(l=60, r=40, t=50, b=60),
        xaxis=dict(title="발생 확률 (%)", range=[20, 80], dtick=10, gridcolor="rgba(148,163,184,0.08)"),
        yaxis=dict(title="영향도 (%)", range=[50, 100], dtick=10, gridcolor="rgba(148,163,184,0.08)"),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, config=plotly_config())

    # 범례
    st.markdown(f'''
    <div style="display:flex; gap:20px; justify-content:center; margin-bottom:20px; flex-wrap:wrap;">
        <span style="font-size:0.78rem; color:{RED};">&#9679; 극심</span>
        <span style="font-size:0.78rem; color:#f97316;">&#9679; 높음</span>
        <span style="font-size:0.78rem; color:{YELLOW};">&#9679; 중간</span>
    </div>
    ''', unsafe_allow_html=True)

    # 리스크 카드
    st.markdown("### 리스크 상세 및 대응 방안")
    sorted_risks = sorted(RISKS, key=lambda r: r["prob"] * r["impact"] / 100, reverse=True)

    for risk in sorted_risks:
        gc = grade_colors[risk["grade"]]
        severity = risk["prob"] * risk["impact"] / 100
        st.markdown(f'''
        <div style="background: linear-gradient(135deg, #101828, #1a2540); border: 1px solid #1e293b;
                    border-left: 4px solid {gc}; border-radius: 0 12px 12px 0; padding: 16px 20px; margin: 8px 0;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-weight:700; font-size:0.95rem;">R{risk["id"]}. {risk["name"]}</span>
                <span style="color:{gc}; font-size:0.8rem; font-weight:600;">{risk["grade"]} (위험도: {severity:.0f})</span>
            </div>
            <div style="font-size:0.82rem; color:#9ca3af; margin-top:4px;">
                확률: {risk["prob"]}% | 영향도: {risk["impact"]}%
            </div>
            <div style="font-size:0.82rem; color:#9ca3af; margin-top:8px;">
                <strong style="color:#d1d5db;">대응 방안:</strong> {risk["response"]}
            </div>
        </div>
        ''', unsafe_allow_html=True)


with tabs[5]:
    render_risk()


# ───────────────────────────────────────────────────
# TAB 7: KPI 대시보드
# ───────────────────────────────────────────────────
def render_kpi():
    st.markdown('<div id="kpi" class="tab-section"></div>', unsafe_allow_html=True)
    st.markdown("## KPI 대시보드")
    st.markdown("")

    # Phase별 KPI 바차트
    st.markdown("### Phase별 KPI 목표")
    kpi_select = st.selectbox(
        "KPI 선택",
        options=[k["name"] for k in KPIS],
        key="kpi_select",
    )
    selected = next(k for k in KPIS if k["name"] == kpi_select)

    phases = ["Phase 1", "Phase 2", "Phase 3"]
    vals = [selected["p1"], selected["p2"], selected["p3"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=phases, y=vals,
        marker=dict(
            color=[MINT, PURPLE, YELLOW],
            line=dict(width=0),
        ),
        text=[f"{v} {selected['unit']}" for v in vals],
        textposition="outside",
        textfont=dict(size=12),
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT, height=350,
        margin=dict(l=40, r=40, t=50, b=40),
        yaxis=dict(title=selected["unit"], gridcolor="rgba(148,163,184,0.08)"),
        title=dict(text=f"{selected['name']} 목표 추이", font=dict(size=14)),
    )
    st.plotly_chart(fig, use_container_width=True, config=plotly_config())

    st.markdown("")

    # KPI 메트릭 카드
    st.markdown("### Phase 3 최종 목표")
    kpi_cols = st.columns(3)
    kpi_colors = [MINT, PURPLE, YELLOW, MINT, PURPLE, YELLOW]
    for i, kpi in enumerate(KPIS):
        with kpi_cols[i % 3]:
            st.markdown(f'''
            <div class="mc" style="margin-bottom:12px;">
                <div class="mc-l">{kpi["name"]}</div>
                <div class="mc-v" style="color:{kpi_colors[i]}; font-size:1.5rem;">{kpi["p3"]}</div>
                <div class="mc-l">{kpi["unit"]} (Phase 3 목표)</div>
            </div>
            ''', unsafe_allow_html=True)

    st.markdown("")

    # Phase별 전체 비교 차트
    st.markdown("### Phase별 주요 KPI 비교")
    fig = go.Figure()
    kpi_names_short = [k["name"] for k in KPIS[:4]]  # 상위 4개만
    for pi, (phase, color) in enumerate([("p1", MINT), ("p2", PURPLE), ("p3", YELLOW)]):
        fig.add_trace(go.Bar(
            name=f"Phase {pi+1}",
            x=kpi_names_short,
            y=[KPIS[j][phase] for j in range(4)],
            marker_color=color,
            text=[f"{KPIS[j][phase]}" for j in range(4)],
            textposition="outside", textfont=dict(size=10),
        ))
    fig.update_layout(
        **PLOTLY_LAYOUT, barmode="group", height=400,
        margin=dict(l=40, r=40, t=50, b=40),
        yaxis=dict(gridcolor="rgba(148,163,184,0.08)", type="log", title="값 (로그 스케일)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig, use_container_width=True, config=plotly_config())


with tabs[6]:
    render_kpi()


# ───────────────────────────────────────────────────
# TAB 8: 실행 로드맵
# ───────────────────────────────────────────────────
def render_roadmap():
    st.markdown('<div id="roadmap" class="tab-section"></div>', unsafe_allow_html=True)
    st.markdown("## 실행 로드맵")
    st.markdown("")

    # Gantt 타임라인
    st.markdown("### 프로젝트 타임라인")
    phase_data = [
        {"phase": "Phase 1: 기반 구축 (MVP)", "start": 0, "end": 6, "color": MINT},
        {"phase": "Phase 2: 확장 및 BEP 달성", "start": 6, "end": 12, "color": PURPLE},
        {"phase": "Phase 3: 풀스케일 상용화", "start": 12, "end": 24, "color": YELLOW},
    ]
    fig = go.Figure()
    for p in phase_data:
        fig.add_trace(go.Bar(
            y=[p["phase"]], x=[p["end"] - p["start"]],
            base=[p["start"]], orientation="h",
            marker_color=p["color"],
            text=[f'{p["start"]}~{p["end"]}개월'],
            textposition="inside",
            textfont=dict(size=12, color="#ffffff"),
            name=p["phase"],
            hovertemplate=f'{p["phase"]}<br>{p["start"]}~{p["end"]}개월<extra></extra>',
        ))
    fig.update_layout(
        **PLOTLY_LAYOUT, height=220,
        margin=dict(l=220, r=40, t=30, b=40),
        xaxis=dict(title="개월", dtick=3, gridcolor="rgba(148,163,184,0.08)"),
        yaxis=dict(autorange="reversed"),
        showlegend=False,
        barmode="overlay",
    )
    st.plotly_chart(fig, use_container_width=True, config=plotly_config())

    st.markdown("")

    # Phase 카드 상세
    phase_colors = [MINT, PURPLE, YELLOW]
    for i, phase in enumerate(ROADMAP):
        color = phase_colors[i]
        st.markdown(f'''
        <div class="phase-card" style="border-top: 3px solid {color}; margin-bottom: 16px;">
            <div class="phase-badge" style="background: {color}20; color: {color}; border: 1px solid {color}50;">
                {phase["phase"]}
            </div>
            <div style="font-size:1.2rem; font-weight:700; margin:4px 0;">{phase["title"]}</div>
            <div style="font-size:0.85rem; color:{GRAY};">{phase["period"]} | 예산: {phase["budget"]}</div>
        </div>
        ''', unsafe_allow_html=True)

        tc, mc2 = st.columns(2)
        with tc:
            st.markdown("**주요 과제**")
            for task in phase["tasks"]:
                st.markdown(f'<div style="font-size:0.85rem; color:#d1d5db; padding:3px 0;">- {task}</div>', unsafe_allow_html=True)
        with mc2:
            st.markdown("**마일스톤**")
            for ms in phase["milestones"]:
                st.markdown(f'<div style="font-size:0.85rem; color:{color}; padding:3px 0;">&#10003; {ms}</div>', unsafe_allow_html=True)

        st.markdown("")


with tabs[7]:
    render_roadmap()

import pandas as pd
import plotly.express as px
import streamlit as st

# ─────────────────────────────────────────────
# 기본 설정
# ─────────────────────────────────────────────
st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", page_icon="🎬", layout="wide")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
WARM = "#E4572E"  # 따뜻한 주황빛 붉은색

# 그래프마다 '이 그래프로 알 수 있는 것' 한 문장을 여기에 적어 두면 그래프 아래에 표시돼요.
# 새 그래프를 추가하면 키를 하나 더 만들어 주세요.
INSIGHTS = {
    "graph1": "",  # 예: "이 영화는 개봉 직후 관객이 가장 많았고 이후 빠르게 줄었다."
}


# ─────────────────────────────────────────────
# 데이터 불러오기
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    # 하이픈 없는 여덟 자리 숫자(예: 20240101) → 진짜 날짜로 변환
    df["날짜"] = pd.to_datetime(df["날짜"].astype(str), format="%Y%m%d")
    return df


def show_insight(key):
    """그래프 아래 '이 그래프로 알 수 있는 것' 문구 자리"""
    text = INSIGHTS.get(key, "").strip()
    if text:
        st.info(f"💡 **이 그래프로 알 수 있는 것**  \n{text}")
    else:
        st.caption("💡 이 그래프로 알 수 있는 것: (INSIGHTS에 한 문장을 적어 주세요)")


df = load_data()

# ─────────────────────────────────────────────
# 제목
# ─────────────────────────────────────────────
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.write("1년치 일별 박스오피스 10위권 기록으로, 시간에 따른 변화를 살펴봐요.")

# ─────────────────────────────────────────────
# 구역 1 : 영화 한 편의 일관객 변화
# ─────────────────────────────────────────────
st.divider()
st.header("구역 1. 영화별 일관객 변화")

# 10위권에 든 총 일관객이 많은 영화가 먼저 나오도록 정렬
movie_order = (
    df.groupby("영화명")["일관객"].sum().sort_values(ascending=False).index.tolist()
)
movie = st.selectbox("영화를 골라 보세요", movie_order)

one = df[df["영화명"] == movie].sort_values("날짜")

fig1 = px.line(one, x="날짜", y="일관객", title=f"{movie} - 날짜별 일관객")
fig1.update_traces(
    line_color=WARM,
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>",
)
fig1.update_layout(xaxis_title="날짜", yaxis_title="일관객(명)", hovermode="x unified")
st.plotly_chart(fig1, use_container_width=True)
show_insight("graph1")

# ─────────────────────────────────────────────
# 구역 2 : (다음 그래프를 여기에 추가)
# ─────────────────────────────────────────────
# st.divider()
# st.header("구역 2. ...")

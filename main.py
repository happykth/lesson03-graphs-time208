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
    "graph2": "",
    "graph3": "",
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
# 구역 2 : 일관객 합계 상위 5편 비교
# ─────────────────────────────────────────────
st.divider()
st.header("구역 2. 관객이 가장 많았던 5편 비교")
st.caption("범례의 영화 이름을 누르면 그 영화를 켜고 끌 수 있어요. 10위권 밖이던 날은 선이 끊겨요.")

# 기간 내 일관객 합계가 가장 큰 5편
top5 = df.groupby("영화명")["일관객"].sum().nlargest(5).index.tolist()

# 영화 × 날짜 표로 바꾼 뒤, 전체 날짜로 늘려서 빈 날은 비워 둠(선이 끊기도록)
wide = df[df["영화명"].isin(top5)].pivot_table(index="날짜", columns="영화명", values="일관객", aggfunc="sum")
wide = wide.reindex(pd.date_range(df["날짜"].min(), df["날짜"].max()))[top5]
wide.index.name = "날짜"
long = wide.reset_index().melt(id_vars="날짜", var_name="영화명", value_name="일관객")

fig2 = px.line(
    long,
    x="날짜",
    y="일관객",
    color="영화명",
    category_orders={"영화명": top5},
    color_discrete_sequence=["#E4572E", "#F3A712", "#7B3F61", "#669BBC", "#5B8E7D"],
    title="일관객 합계 상위 5편 - 날짜별 일관객",
)
fig2.update_traces(hovertemplate="%{fullData.name}<br>날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>")
fig2.update_layout(xaxis_title="날짜", yaxis_title="일관객(명)", legend_title_text="영화(눌러서 켜기/끄기)")
st.plotly_chart(fig2, use_container_width=True)
show_insight("graph2")

# ─────────────────────────────────────────────
# 구역 3 : 날짜별 10위권 일관객 합계
# ─────────────────────────────────────────────
st.divider()
st.header("구역 3. 하루 전체 관객수 (10위권 합계)")
st.caption("표시한 세 점은 합계가 가장 컸던 날이에요.")

# 날짜별로 그날 10위권 일관객을 모두 더함
daily = df.groupby("날짜", as_index=False)["일관객"].sum()
peak3 = daily.nlargest(3, "일관객")  # 합계가 가장 컸던 3일

fig3 = px.area(daily, x="날짜", y="일관객", title="날짜별 10위권 일관객 합계")
fig3.update_traces(
    line_color=WARM,
    fillcolor="rgba(228, 87, 46, 0.30)",
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>합계: %{y:,}명<extra></extra>",
)

# 가장 컸던 3일을 점으로 찍고, 날짜를 글자로 적기
fig3.add_scatter(
    x=peak3["날짜"],
    y=peak3["일관객"],
    mode="markers+text",
    text=peak3["날짜"].dt.strftime("%Y-%m-%d"),
    textposition=["top center", "top right", "top left"],  # 글자가 겹치지 않게 위치를 나눔
    marker=dict(size=11, color="#7B3F61", line=dict(width=2, color="white")),
    showlegend=False,
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>합계: %{y:,}명<extra></extra>",
)
# 글자가 그래프 밖으로 잘리지 않게 위쪽 여백을 조금 늘림
fig3.update_yaxes(range=[0, daily["일관객"].max() * 1.18])
fig3.update_layout(xaxis_title="날짜", yaxis_title="10위권 일관객 합계(명)")
st.plotly_chart(fig3, use_container_width=True)
show_insight("graph3")

# ─────────────────────────────────────────────
# 구역 4 : (다음 그래프를 여기에 추가)
# ─────────────────────────────────────────────
# st.divider()
# st.header("구역 4. ...")

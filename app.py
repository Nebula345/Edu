import streamlit as st
import pandas as pd
import html

st.set_page_config(
    page_title="독서던전",
    page_icon="🧟",
    layout="centered"
)

# =========================
# CSV 자동 인코딩 처리
# =========================

try:
    choices = pd.read_csv(
        "choice_data.csv",
        encoding="utf-8-sig"
    )
except:
    choices = pd.read_csv(
        "choice_data.csv",
        encoding="cp949"
    )

try:
    books = pd.read_csv(
        "book_data.csv",
        encoding="utf-8-sig"
    )
except:
    books = pd.read_csv(
        "book_data.csv",
        encoding="cp949"
    )

# =========================
# 세션 상태
# =========================

if "page" not in st.session_state:
    st.session_state.page = 0

if "name" not in st.session_state:
    st.session_state.name = ""

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "grade" not in st.session_state:
    st.session_state.grade = 1

question_ids = list(
    choices["question_id"].unique()
)

# =========================
# CSS
# =========================

st.markdown("""
<style>

.stApp {
    background-color: #050505;
}

h1, h2, h3, p, div, label, span {
    color: white !important;
}

.story-box {
    background-color: #111111;
    color: white;
    border: 2px solid #333333;
    border-radius: 16px;
    padding: 22px;
    margin: 18px 0;
    line-height: 1.8;
    font-size: 18px;
}

div.stButton > button {
    width: 100%;
    border-radius: 15px;
    padding: 0.8rem;
    font-size: 18px;
    background-color: #1f1f1f;
    color: white !important;
    border: 2px solid #555;
    font-weight: bold;
}

div.stButton > button:hover {
    background-color: #333333;
    color: #00ff88 !important;
    border: 2px solid #00ff88;
}

[data-testid="stAlert"] {
    background-color: #111111 !important;
    color: white !important;
    border: 1px solid #444 !important;
}

input {
    background-color: #111111 !important;
    color: white !important;
    border: 1px solid #555 !important;
}

.stRadio label {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# 카드 함수
# =========================

def story_card(title, body):

    body = html.escape(
        str(body)
    ).replace("\n", "<br>")

    st.markdown(
        f"""
        <div class="story-box">

        <h2>{title}</h2>

        <p>{body}</p>

        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# 시작 화면
# =========================

if st.session_state.page == 0:

    st.image(
        "start.png",
        width="stretch"
    )

    st.audio("zombie.mp3")

    story_card(
        "📡 긴급 통신",
        """통신 장치가 희미하게 깜빡인다.

스마트폰 바이러스가 퍼진 이후,
사람들이 좀비로 변하고 세상이 점점 무너지고 있어.

살아남기 위해서는
너에게 맞는 독서백신으로 세상을 지킬 수 있어."""
    )

    if st.button("🛰️ 게임 시작"):

        st.session_state.page = 1

        st.rerun()

# =========================
# 이름 입력
# =========================

elif st.session_state.page == 1:

    story_card(
        "📡 생존자 인증",
        "생존자 이름을 입력해."
    )

    name = st.text_input(
        "생존자 이름을 입력해"
    )

    if st.button("통신 연결"):

        if name.strip() == "":

            st.warning("이름을 입력해.")

        else:

            st.session_state.name = (
                name.strip()
            )

            st.session_state.page = 2

            st.rerun()

# =========================
# 오프닝
# =========================

opening = [

    "지금 상황이 심각해.",

    "스마트폰 바이러스가 퍼지고 있어.",

    "사람들이 생각 없는 좀비처럼 변하고 있어.",

    "유일한 해결책은 독서 백신뿐이야.",

    "세상을 꼭 지켜줘... 뚜뚜뚜"
]

opening_start = 2

opening_end = (
    opening_start + len(opening) - 1
)

if (
    opening_start
    <= st.session_state.page
    <= opening_end
):

    st.image(
        "signal.png",
        width="stretch"
    )

    idx = (
        st.session_state.page
        - opening_start
    )

    if idx == 0:

        text = (
            f"{st.session_state.name}, "
            f"{opening[idx]}"
        )

    else:

        text = opening[idx]

    story_card(
        "🛰️ 긴급 통신",
        text
    )

    if st.button("다음 ▶"):

        st.session_state.page += 1

        st.rerun()

# =========================
# 질문 이미지
# =========================

question_images = {

    "Q1": "forest.png",
    "Q2": "street.png",
    "Q3": "library.png",
    "Q4": "lab.png",
    "Q5": "escape.png"
}

question_start = opening_end + 1

question_end = (
    question_start
    + len(question_ids)
    - 1
)

if (
    question_start
    <= st.session_state.page
    <= question_end
):

    idx = (
        st.session_state.page
        - question_start
    )

    qid = question_ids[idx]

    q = choices[
        choices["question_id"] == qid
    ]

    st.image(
        question_images.get(
            qid,
            "forest.png"
        ),
        width="stretch"
    )

    stage = q["stage"].iloc[0]

    question_text = q[
        "question_text"
    ].iloc[0]

    story_card(
        f"📍 {stage}",
        question_text
    )

    option = st.radio(
        "어떻게 행동할래?",
        q["choice_text"].tolist(),
        key=qid
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("◀ 이전"):

            st.session_state.page -= 1

            st.rerun()

    with col2:

        if st.button("선택 ▶"):

            selected = q[
                q["choice_text"] == option
            ]

            st.session_state.answers[qid] = (
                selected["trait"].values[0]
            )

            st.session_state.page += 1

            st.rerun()

# =========================
# 학년 입력
# =========================

grade_page = question_end + 1

if st.session_state.page == grade_page:

    st.image(
        "vaccine.png",
        width="stretch"
    )

    story_card(
        "💉 독서백신 분석",
        "마지막으로 학년 정보를 입력해."
    )

    grade = st.number_input(
        "학년 입력",
        min_value=1,
        max_value=6,
        step=1
    )

    if st.button("분석 시작"):

        st.session_state.grade = grade

        st.session_state.page += 1

        st.rerun()

# =========================
# 결과 화면
# =========================

if (
    st.session_state.page
    == grade_page + 1
):

    st.audio("ending.mp3")

    trait_score = {

        "행동형": 0,
        "분석형": 0,
        "공감형": 0,
        "상상형": 0
    }

    for trait in (
        st.session_state.answers.values()
    ):

        if trait in trait_score:

            trait_score[trait] += 1

    max_score = max(
        trait_score.values()
    )

    top_traits = [

        trait
        for trait, score
        in trait_score.items()

        if score == max_score
    ]

    story_card(
        "🎉 생존 성공",
        "너는 끝까지 살아남았어."
    )

    for trait, score in (
        trait_score.items()
    ):

        st.write(
            f"{trait}: {score}점"
        )

    ending_map = {

        "행동형":
        "망설이지 않고 움직이며 살아남았어.",

        "분석형":
        "상황을 분석하며 가장 안전한 길을 찾아냈어.",

        "공감형":
        "다른 사람들을 도우며 끝까지 버텼어.",

        "상상형":
        "아무도 떠올리지 못한 방법으로 탈출했어."
    }

    st.markdown("## 🏆 엔딩")

    for t in top_traits:

        st.write(
            f"• {ending_map[t]}"
        )

    recommended = books[
        (
            books["trait"].isin(
                top_traits
            )
        )
        &
        (
            books["min_grade"]
            <= st.session_state.grade
        )
        &
        (
            books["max_grade"]
           >= st.session_state.grade
        )
    ]

    st.markdown("## 📚 독서백신 지급")

    for _, row in (
        recommended.iterrows()
    ):

        story_card(
            f"📖 {row['title']}",
            f"""✍ 저자: {row['author']}

🏢 출판사: {row['publisher']}

💬 추천 이유:
{row['reason']}"""
        )

    if st.button(
        "🔄 처음부터 다시 하기"
    ):

        st.session_state.page = 0

        st.session_state.answers = {}

        st.rerun()
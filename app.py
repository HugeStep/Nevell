import streamlit as st
import google.generativeai as genai

# 넓은 화면 사용
st.set_page_config(layout="wide")

# Gemini API 키 설정 (코드에 직접 쓰지 않고 secrets.toml에서 불러옴)
try:
    genai.configure(api_key=st.secrets["gemini_api_key"])
except Exception as e:
    st.error("Gemini API 키를 불러오는 중 오류가 발생했습니다. (secrets.toml 파일을 확인해 주세요.)")
    st.stop()

# 전체 배경색 및 스타일
st.markdown("""
    <style>
    body { background-color: #FEF1DD; }
    .box {
        border: 2px solid #CCE7FF;
        border-radius: 18px;
        padding: 18px 18px 18px 18px;
        margin-bottom: 18px;
        background: #fff;
    }
    .best-products-outer {
        border: 2.5px solid #7BA7D9;
        border-radius: 32px;
        background: #EAF6FF;
        padding: 28px 28px 18px 28px;
        margin-bottom: 18px;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .best-title {
        color: #3887C2;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 18px;
        text-align: left;
    }
    .best-row {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        width: 100%;
    }
    .best-card {
        background: none;
        border: none;
        box-shadow: none;
        border-radius: 18px;
        padding: 0 10px;
        text-align: center;
        flex: 1;
    }
    .product-img {
        width: 100%;
        height: 100px;
        object-fit: cover;
        background: #fff;
        border-radius: 12px;
        margin-bottom: 8px;
    }
    .product-label {
        text-align: center;
        color: #7BA7D9;
        font-size: 14px;
        margin-bottom: 4px;
    }
    .section-title {
        color: #7BA7D9;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 12px;
        text-align: left;
    }
    .skin-section-title {
        color: #7BA7D9;
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 10px;
        text-align: center;
    }
    .skin-product-box {
        background: #F8FBFF;
        border: 1.5px solid #CCE7FF;
        border-radius: 6px;
        padding: 8px;
        margin-bottom: 10px;
        text-align: center;
    }
    .vline {
        border-left: 2px solid #CCE7FF;
        height: 100%;
        margin: 0 10px;
    }
    .header-right {
        text-align: right;
        font-size: 15px;
        color: #7BA7D9;
    }
    .menu-bar { display: flex; gap: 12px; justify-content: flex-end; align-items: center; }
    .menu-bar select, .menu-bar button {
        font-size: 16px; padding: 6px 18px; border-radius: 8px; border: 1px solid #ccc; background: #fff; margin: 0 2px;
    }
    .menu-bar .login-btn { color: #464FEB; font-weight: bold; border: 1.5px solid #464FEB; }
    .menu-bar .signup-btn { color: #5E5841; font-weight: bold; border: 1.5px solid #B0C4DE; }
    </style>
""", unsafe_allow_html=True)

# 상단 헤더 - Nevell 로고 중앙 정렬
st.markdown("<div style='text-align:center;'><span style='font-size:70px; color:#5E5841; font-weight:bold;'>Nevell</span></div>", unsafe_allow_html=True)
# Nevell 아래에 작은 글씨 설명 추가
st.markdown("<div style='text-align:center; margin-top:-18px;'><span style='font-size:18px; color:#5E5841;'>사용자 적합 화장품 추천 AI 서비스</span></div>", unsafe_allow_html=True)

# --- 언어/로그인/회원가입 메뉴를 오른쪽 상단에 가로로 배치 (Streamlit 기본 방식 복원) ---
menu_col1, menu_col2 = st.columns([8, 2])
with menu_col2:
    col_lang, col_login, col_signup = st.columns([1,1,1])
    with col_lang:
        lang = st.selectbox("", ["한국어", "English"], label_visibility="collapsed")
    with col_login:
        login_clicked = st.button("로그인")
    with col_signup:
        signup_clicked = st.button("회원가입")

# 로그인/회원가입 모달 창 구현 (Streamlit은 진짜 모달은 없으나, expander+session_state로 유사하게 구현)
if "show_login" not in st.session_state:
    st.session_state["show_login"] = False
if "show_signup" not in st.session_state:
    st.session_state["show_signup"] = False

if login_clicked:
    st.session_state["show_login"] = True
if signup_clicked:
    st.session_state["show_signup"] = True

if st.session_state["show_login"]:
    with st.expander("로그인", expanded=True):
        st.markdown("<h4>로그인</h4>", unsafe_allow_html=True)
        st.text_input("아이디", key="login_id")
        st.text_input("비밀번호", type="password", key="login_pw")
        if st.button("로그인 완료", key="login_submit"):
            st.success("로그인 성공! (예시)")
            st.session_state["show_login"] = False
        if st.button("닫기", key="login_close"):
            st.session_state["show_login"] = False

if st.session_state["show_signup"]:
    with st.expander("회원가입", expanded=True):
        st.markdown("<h4>회원가입</h4>", unsafe_allow_html=True)
        st.text_input("아이디", key="signup_id")
        st.text_input("비밀번호", type="password", key="signup_pw")
        st.text_input("이메일", key="signup_email")
        st.text_input("이름", key="signup_name")
        if st.button("회원가입 완료", key="signup_submit"):
            st.success("회원가입 성공! (예시)")
            st.session_state["show_signup"] = False
        if st.button("닫기", key="signup_close"):
            st.session_state["show_signup"] = False

st.markdown("<hr style='margin-top:0;margin-bottom:18px;border:1px solid #CCE7FF;'>", unsafe_allow_html=True)

# 본문 3분할 (좌:3, 중앙:0.2, 우:2)
main_col1, main_col2, main_col3 = st.columns([3, 0.2, 2])

# --- 좌측: 추천 제품 영역 ---
with main_col1:
    st.markdown("<div class='section-title' style='color:#464FEB; font-size:40px; text-align:left;'>BEST 인기 제품</div>", unsafe_allow_html=True)

    # 코드에서 리스트만 수정하면 반영되도록
    best_product_imgs = [
        "https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/550/10/0000/0021/A00000021390707ko.png?l=ko",
        "https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/550/10/0000/0020/A00000020122640ko.jpg?l=ko",
        "https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/550/10/0000/0015/A00000015525323ko.jpg?l=ko",
        "https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/550/10/0000/0019/A00000019278709ko.jpg?l=ko"
    ]
    best_product_names = [
        "에스네이처 아쿠아 스쿠알란 수분크림 60ml",
        "구달 청귤 비타C 잡티케어 세럼 50ml",
        "아누아 어성초 수딩 토너 350ml",
        "에스네이처 아쿠아 소이 요거 아이크림 25g"
    ]

    best_cols = st.columns(4)
    for i, col in enumerate(best_cols):
        with col:
            st.image(best_product_imgs[i], use_container_width=True)
            st.markdown(f"<div style='text-align:center; color:#3887C2; font-weight:bold;'>{best_product_names[i]}</div>", unsafe_allow_html=True)

    # 피부 타입별 추천 박스
    st.markdown("<div class='box'>", unsafe_allow_html=True)

    # 각 피부타입별 추천 제품 이미지/이름 리스트 (코드에서만 수정)
    best_skin_imgs = [
        [  # 건성
            "https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/550/10/0000/0016/A00000016261010ko.jpg?l=ko",
            "https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/550/10/0000/0018/A00000018665513ko.jpg?l=ko",
            "https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/550/10/0000/0020/A00000020376510ko.jpg?l=ko"
        ],
        [  # 중성
            "https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/550/10/0000/0021/A00000021751125ko.png?l=ko",
            "https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/550/10/0000/0021/A00000021270313ko.png?l=ko",
            "https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/550/10/0000/0020/A00000020122640ko.jpg?l=ko"
        ],
        [  # 지성
            "https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/550/10/0000/0020/A00000020682702ko.jpg?l=ko",
            "https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/550/10/0000/0021/A00000021419509ko.jpg?l=ko",
            "https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/550/10/0000/0021/A00000021743109ko.jpg?l=ko"
        ]
    ]
    best_skin_names = [
        ["건성추천1", "건성추천2", "건성추천3"],
        ["중성추천1", "중성추천2", "중성추천3"],
        ["지성추천1", "지성추천2", "지성추천3"]
    ]

    skin_cols = st.columns([1,0.05,1,0.05,1])
    skin_types = ["건성 피부 추천", "중성 피부 추천", "지성 피부 추천"]
    for idx, skin in enumerate(skin_types):
        with skin_cols[idx*2]:
            st.markdown(f"<div class='skin-section-title'>{skin}</div>", unsafe_allow_html=True)
            for j in range(3):
                st.image(best_skin_imgs[idx][j], use_container_width=True)
                st.markdown(f"<div style='text-align:center; color:#888;'>{best_skin_names[idx][j]}</div>", unsafe_allow_html=True)
        if idx < 2:
            with skin_cols[idx*2+1]:
                st.markdown("<div class='vline'>&nbsp;</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 중앙: 구분선 역할 (비워둠) ---
with main_col2:
    st.markdown("&nbsp;", unsafe_allow_html=True)

# --- 우측: 사용자 정보 입력 + 챗봇 ---
with main_col3:
    # 사용자 정보 입력 폼
    st.markdown("<div class='box'><div class='section-title' style='text-align:center;'>사용자 정보 입력</div>", unsafe_allow_html=True)
    if "show_form" not in st.session_state:
        st.session_state["show_form"] = True
    if st.button("사용자 정보 입력 폼 열기/닫기"):
        st.session_state["show_form"] = not st.session_state["show_form"]
    if st.session_state["show_form"]:
        gender = st.radio("성별", ("남", "여"))
        age = st.number_input("나이", min_value=0, max_value=100, value=20, step=1)
        skin_condition = st.text_input("피부 상태 (예: 민감성, 트러블 등)")
        skin_type = st.selectbox("피부 타입", ("건성", "중성", "지성"))
        if st.button("입력 완료"):
            st.session_state["user_info"] = {"gender": gender, "age": age, "skin_condition": skin_condition, "skin_type": skin_type}
            st.success("사용자 정보가 저장되었습니다.")
            # 사용자 정보 기반 자동 챗봇 질문
            user_info_str = f"성별: {gender}, 나이: {age}, 피부 상태: {skin_condition}, 피부 타입: {skin_type}"
            auto_prompt = f"{user_info_str}\n\n위 사용자에게 맞춤형 화장품을 추천해줘. 추천 이유도 간단히 설명해줘."
            if "chat_history" not in st.session_state:
                st.session_state["chat_history"] = []
            st.session_state["chat_history"].append({"role": "user", "content": auto_prompt})
            with st.spinner("AI 추천을 생성 중입니다..."):
                try:
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(auto_prompt)
                    answer = response.text if hasattr(response, 'text') else str(response)
                except Exception as e:
                    answer = "Gemini API 호출 중 오류가 발생했습니다. (오류 메시지: " + str(e) + ")"
            st.session_state["chat_history"].append({"role": "assistant", "content": answer})
    st.markdown("</div>", unsafe_allow_html=True)

    # 챗봇 UI 및 대화 관리
    st.markdown("<div class='box'><div class='section-title' style='text-align:center;'>맞춤형 화장품 추천 챗봇</div>", unsafe_allow_html=True)
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "user_info" in st.session_state:
        user_info = st.session_state["user_info"]
        user_info_str = f"성별: {user_info['gender']}, 나이: {user_info['age']}, 피부 상태: {user_info['skin_condition']}, 피부 타입: {user_info['skin_type']}"
    else:
        user_info = None
        user_info_str = "(사용자 정보가 입력되지 않았습니다.)"

    # 이전 대화 표시
    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 챗봇 입력
    prompt = st.chat_input("궁금한 점을 입력해 주세요.")
    if prompt:
        st.session_state["chat_history"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.spinner("추천을 생성 중입니다..."):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                context = f"사용자 정보: {user_info_str}\n대화 이력: {[m['content'] for m in st.session_state['chat_history'] if m['role']=='user']}"
                full_prompt = f"{context}\n\n{prompt}\n\n위 사용자에게 맞춤형 화장품을 추천해줘. 추천 이유도 간단히 설명해줘."
                response = model.generate_content(full_prompt)
                answer = response.text if hasattr(response, 'text') else str(response)
            except Exception as e:
                answer = "Gemini API 호출 중 오류가 발생했습니다. (오류 메시지: " + str(e) + ")"
        st.session_state["chat_history"].append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)
    st.markdown("</div>", unsafe_allow_html=True)

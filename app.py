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
    .stApp {
        background-color: #F7F8FF;
    }
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
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 12px;
        text-align: center;
    }
    .skin-section-title {
        color: #7BA7D9;
        font-size: 22px;
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

# 다국어 사전 정의
TEXT = {
    "ko": {
        "nevell": "Nevell",
        "desc": "사용자 적합 화장품 추천 AI 서비스",
        "best": "BEST 인기 제품",
        "skin_types": ["건성 피부 추천", "중성 피부 추천", "지성 피부 추천"],
        "user_info": "사용자 정보 입력",
        "user_form_toggle": "사용자 정보 입력 폼 열기/닫기",
        "gender": "성별",
        "male": "남",
        "female": "여",
        "age": "나이",
        "skin_condition": "피부 상태 (예: 민감성, 트러블 등)",
        "skin_type": "피부 타입",
        "input_done": "입력 완료",
        "chatbot": "맞춤형 화장품 추천 챗봇",
        "chat_input": "궁금한 점을 입력해 주세요.",
        "login": "로그인",
        "signup": "회원가입",
        "login_title": "로그인",
        "signup_title": "회원가입",
        "login_id": "아이디",
        "login_pw": "비밀번호",
        "signup_email": "이메일",
        "signup_name": "이름",
        "login_done": "로그인 완료",
        "signup_done": "회원가입 완료",
        "close": "닫기",
        "login_success": "로그인 성공!",
        "signup_success": "회원가입 성공!",
        "user_saved": "사용자 정보가 저장되었습니다.",
        "ai_recommend": "AI 추천을 생성 중입니다...",
        "chatbot_recommend": "추천을 생성 중입니다..."
    },
    "en": {
        "nevell": "Nevell",
        "desc": "Personalized Cosmetics Recommendation AI Service",
        "best": "BEST Popular Products",
        "skin_types": ["Dry Skin Recommendation", "Normal Skin Recommendation", "Oily Skin Recommendation"],
        "user_info": "User Information Input",
        "user_form_toggle": "Open/Close User Info Form",
        "gender": "Gender",
        "male": "Male",
        "female": "Female",
        "age": "Age",
        "skin_condition": "Skin Condition (e.g. Sensitive, Trouble, etc.)",
        "skin_type": "Skin Type",
        "input_done": "Submit",
        "chatbot": "Personalized Cosmetics Chatbot",
        "chat_input": "Please enter your question.",
        "login": "Login",
        "signup": "Sign Up",
        "login_title": "Login",
        "signup_title": "Sign Up",
        "login_id": "ID",
        "login_pw": "Password",
        "signup_email": "Email",
        "signup_name": "Name",
        "login_done": "Login",
        "signup_done": "Sign Up",
        "close": "Close",
        "login_success": "Login Success! (Sample)",
        "signup_success": "Sign Up Success! (Sample)",
        "user_saved": "User information saved.",
        "ai_recommend": "Generating AI recommendation...",
        "chatbot_recommend": "Generating recommendation..."
    }
}

# 1. Nevell 로고/설명 중앙
st.markdown(f"<div style='text-align:center;'><span style='font-size:70px; color:#5E5841; font-weight:bold;'>Nevell</span></div>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center; margin-top:-18px; margin-bottom:0px;'><span style='font-size:18px; color:#5E5841;'>사용자 적합 화장품 추천 AI 서비스</span></div>", unsafe_allow_html=True)

# 2. 로고/설명 바로 아래에 메뉴 오른쪽 정렬 (여기서 lang, login_clicked, signup_clicked, T 정의)
menu_col1, menu_col2 = st.columns([8, 2])
with menu_col2:
    col_lang, col_login, col_signup = st.columns([1,1,1])
    with col_lang:
        lang = st.selectbox("", ["한국어", "English"], label_visibility="collapsed")
    lang_key = "ko" if lang == "한국어" else "en"
    T = TEXT[lang_key]
    with col_login:
        login_clicked = st.button(T["login"])
    with col_signup:
        signup_clicked = st.button(T["signup"])

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
    with st.expander(T["login"], expanded=True):
        st.markdown(f"<h4>{T['login_title']}</h4>", unsafe_allow_html=True)
        st.text_input(T["login_id"], key="login_id")
        st.text_input(T["login_pw"], type="password", key="login_pw")
        if st.button(T["login_done"], key="login_submit"):
            st.success(T["login_success"])
            st.session_state["show_login"] = False
        if st.button(T["close"], key="login_close"):
            st.session_state["show_login"] = False

if st.session_state["show_signup"]:
    with st.expander(T["signup"], expanded=True):
        st.markdown(f"<h4>{T['signup_title']}</h4>", unsafe_allow_html=True)
        st.text_input(T["login_id"], key="signup_id")
        st.text_input(T["login_pw"], type="password", key="signup_pw")
        st.text_input(T["signup_email"], key="signup_email")
        st.text_input(T["signup_name"], key="signup_name")
        if st.button(T["signup_done"], key="signup_submit"):
            st.success(T["signup_success"])
            st.session_state["show_signup"] = False
        if st.button(T["close"], key="signup_close"):
            st.session_state["show_signup"] = False

st.markdown("<hr style='margin-top:0;margin-bottom:18px;border:1px solid #CCE7FF;'>", unsafe_allow_html=True)

# 본문 3분할 (좌:3, 중앙:0.2, 우:2)
main_col1, main_col2, main_col3 = st.columns([3, 0.2, 2])

# --- 좌측: 추천 제품 영역 ---
with main_col1:
    st.markdown(f"<div class='section-title' style='color:#464FEB; font-size:40px; text-align:left;'>{T['best']}</div>", unsafe_allow_html=True)

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
        ["Chamomilla Sinensis Ampoule", "The Lab by blanc doux Oligo Hyaluronic Acid Boosting Ampoule", "Round Lab Mugwort Calming Line (3종)"],
        ["WHIPED Cleanser", "Round Lab Green Tomato Vita Cleanser + Calming Cream", "S.NATURE Aqua Soy Yogurt Super Moisture Ampoule"],
        ["AESTURA Derma UV365 Barrier Sun Cream (SPF 50+)", "Arencia Fresh Herb Soothing Gel", "Arencia Green Tea & Rice Cream Cleanser"]
    ]

    skin_cols = st.columns([1,0.05,1,0.05,1])
    skin_types = T["skin_types"]
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
    st.markdown(f"<div class='box'><div class='section-title' style='text-align:center;'>{T['user_info']}</div>", unsafe_allow_html=True)
    if "show_form" not in st.session_state:
        st.session_state["show_form"] = True
    if st.button(T["user_form_toggle"]):
        st.session_state["show_form"] = not st.session_state["show_form"]
    if st.session_state["show_form"]:
        gender = st.radio(T["gender"], (T["male"], T["female"]))
        age = st.number_input(T["age"], min_value=0, max_value=100, value=20, step=1)
        skin_condition = st.text_input(T["skin_condition"])
        skin_type = st.selectbox(T["skin_type"], (T["skin_types"][0].split()[0], T["skin_types"][1].split()[0], T["skin_types"][2].split()[0]))
        if st.button(T["input_done"]):
            st.session_state["user_info"] = {"gender": gender, "age": age, "skin_condition": skin_condition, "skin_type": skin_type}
            st.success(T["user_saved"])
            # 사용자 정보 기반 자동 챗봇 질문
            user_info_str = f"{T['gender']}: {gender}, {T['age']}: {age}, {T['skin_condition']}: {skin_condition}, {T['skin_type']}: {skin_type}"
            auto_prompt = f"{user_info_str}\n\n위 사용자에게 맞춤형 화장품을 추천해줘. 추천 이유도 간단히 설명해줘."
            if "chat_history" not in st.session_state:
                st.session_state["chat_history"] = []
            st.session_state["chat_history"].append({"role": "user", "content": auto_prompt})
            with st.spinner(T["ai_recommend"]):
                try:
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(auto_prompt)
                    answer = response.text if hasattr(response, 'text') else str(response)
                except Exception as e:
                    answer = "Gemini API 호출 중 오류가 발생했습니다. (오류 메시지: " + str(e) + ")"
            st.session_state["chat_history"].append({"role": "assistant", "content": answer})
    st.markdown("</div>", unsafe_allow_html=True)

    # 챗봇 UI 및 대화 관리
    st.markdown(f"<div class='box'><div class='section-title' style='text-align:center;'>{T['chatbot']}</div>", unsafe_allow_html=True)
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "user_info" in st.session_state:
        user_info = st.session_state["user_info"]
        user_info_str = f"{T['gender']}: {user_info['gender']}, {T['age']}: {user_info['age']}, {T['skin_condition']}: {user_info['skin_condition']}, {T['skin_type']}: {user_info['skin_type']}"
    else:
        user_info = None
        user_info_str = f"({T['user_info']}가 입력되지 않았습니다.)"

    # 이전 대화 표시
    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 챗봇 입력
    prompt = st.chat_input(T["chat_input"])
    if prompt:
        st.session_state["chat_history"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.spinner(T["chatbot_recommend"]):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                context = f"{T['user_info']}: {user_info_str}\n대화 이력: {[m['content'] for m in st.session_state['chat_history'] if m['role']=='user']}"
                full_prompt = f"{context}\n\n{prompt}\n\n위 사용자에게 맞춤형 화장품을 추천해줘. 추천 이유도 간단히 설명해줘."
                response = model.generate_content(full_prompt)
                answer = response.text if hasattr(response, 'text') else str(response)
            except Exception as e:
                answer = "Gemini API 호출 중 오류가 발생했습니다. (오류 메시지: " + str(e) + ")"
        st.session_state["chat_history"].append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)
    st.markdown("</div>", unsafe_allow_html=True)

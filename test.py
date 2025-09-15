import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv 
import os 


# .env 파일 로드 
load_dotenv() 


# OpenAI API Key (환경 변수에서 불러오기)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 세션 상태 초기화
if 'memos' not in st.session_state:
    st.session_state.memos = []

st.title('나만의 직업 추천기')
st.sidebar.subheader('나를 표현하는 활동 기록')

# 입력창
t = st.sidebar.text_input('흥미/관심사', key='title')
c = st.sidebar.text_area('성격/스타일', key='content')

# 저장 함수
def save_clear():
    if st.session_state.title and st.session_state.content:
        st.session_state.memos.append({
            'title': st.session_state.title,
            'content': st.session_state.content
        })
        st.success('메모가 저장되었습니다.')
        st.session_state.title = ''
        st.session_state.content = ''
    else:
        st.warning('제목과 내용을 모두 입력하세요.')

st.sidebar.button('저장', on_click=save_clear, key='save')

# 기존 메모 보여주기
st.subheader("내가 기록한 활동")
if st.session_state.memos:
    for memo in st.session_state.memos:
        st.markdown(f"### {memo['title']}")
        st.write(memo['content'])
        st.markdown('---')
else:
    st.info("아직 저장된 메모가 없습니다. 사이드바에서 활동을 입력해 보세요.")

if st.button("직업 추천받기"):
    if not st.session_state.memos:
        st.warning("먼저 메모를 입력하고 저장해 주세요.")
    else:
        with st.spinner("직업을 분석하고 추천 중입니다..."):
            profile_text = "\n".join([f"- {m['title']}: {m['content']}" for m in st.session_state.memos])

            prompt = f"""
            다음은 사용자가 좋아하는 활동과 과목입니다:
            {profile_text}

            위 정보를 바탕으로 사용자가 잘 맞을만한 직업을 3가지 추천해 주세요.
            각 직업마다:
            1) 직업명
            2) 잘 맞는 이유 (2~3문장)
            3) 필요한 핵심 기술이나 능력
            을 간단하게 설명해 주세요.
            """

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "너는 진로와 직업을 안내하는 커리어 코치다."},
                        {"role": "user", "content": prompt}
                    ],
                   
                )
                answer = response.choices[0].message.content
                st.subheader("추천 직업 결과")
                st.write(answer)
            except Exception as e:
                st.error(f"API 호출 중 오류 발생: {e}")


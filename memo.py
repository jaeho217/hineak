import streamlit as st

if 'memos' not in st.session_state:
    st.session_state.memos = []

st.title('MyMemo')
st.sidebar.subheader('to do list')
t = st.sidebar.text_input('할 일을 입력하세요', key='title')
c = st.sidebar.text_area('상세 내용', key='content')

def save_clear():
    if st.session_state.title and st.session_state.content:
        st.session_state.memos.append({'title':st.session_state.title, 
															        'content':st.session_state.content})
        st.toast('✅ 메모가 저장되었습니다!')
        st.session_state.title = ''
        st.session_state.content = ''
    else:        
        st.toast('❗ 제목과 내용을 모두 입력하세요.')


st.sidebar.button('저장', on_click=save_clear, key='save') 
    
for memo in st.session_state.memos:
    st.markdown(f'# {memo["title"]} ')
    st.write(memo["content"])
    st.markdown('---')
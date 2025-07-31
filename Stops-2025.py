
import streamlit as st
import pandas as pd
import pytz
from datetime import datetime, timedelta
import json
import os
from github import Github
from io import StringIO
st.set_page_config(
    layout="wide",
    page_title='STG-2024',
    page_icon='🪙')

egypt_tz = pytz.timezone('Africa/Cairo')
df_Material = pd.read_excel('C2155 Stops.xlsx')


if 'df' not in st.session_state:
    st.session_state.df = pd.read_excel('C2155 Stops.xlsx')
    

page = st.sidebar.radio('Select page', ['STG-2024'])

if page == 'STG-2024':
        def main():
            st.markdown("""
            <style>
                .stProgress > div > div > div {
                    background-color: #FFD700;
                    border-radius: 50%;
                }
            </style>
            """, unsafe_allow_html=True)
            
            with st.spinner("Data loaded successfully!"):
                import time
                time.sleep(1)
            
            col1, col2 = st.columns([2, 0.75])
            with col1:
                st.markdown("""
                    <h2 style='text-align: center; font-size: 40px; color: red;'>
                        Find your parts
                    </h2>
                """, unsafe_allow_html=True)
            
            with col2:
                search_keyword = st.session_state.get('search_keyword', '')
                search_keyword = st.text_input("Enter keyword to search:", search_keyword)
                search_button = st.button("Search")
                search_option = 'All Columns'
            
            def search_in_dataframe(df_Material, keyword, option):
                if option == 'All Columns':
                    result = df_Material[df_Material.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
                else:
                    result = df_Material[df_Material[option].astype(str).str.contains(keyword, case=False)]
                return result
            
            if st.session_state.get('refreshed', False):
                st.session_state.search_keyword = ''
                st.session_state.refreshed = False
            
            if search_button and search_keyword:
                st.session_state.search_keyword = search_keyword
                search_results = search_in_dataframe(st.session_state.df, search_keyword, search_option)
                st.write(f"Search results for '{search_keyword}'in{search_option}:")
                st.dataframe(search_results, width=1000, height=200)
            st.session_state.refreshed = True 
            
            st.write(df_Material)
            df = pd.read_excel("C2155 Stops.xlsx")

            df = pd.read_excel("C2155 Stops.xlsx")

            st.subheader("قائمة الأعطال")
            
            # نستخدم حاوية لعرض تفاصيل العطل عند الضغط
            placeholder = st.empty()
            
            for index, row in df.iterrows():
                cols = st.columns([2, 2, 1])  # 3 أعمدة
            
                cols[0].write(row["رقم العطل"])
                cols[1].write(row["الوصف"] if "الوصف" in row else "بدون وصف")
            
                if cols[2].button("👁️", key=f"view_{index}"):
                    with placeholder.container():
                        st.markdown("---")
                        st.markdown(f"### 🔧 تفاصيل العطل رقم {row['رقم العطل']}")
                        st.write(f"📄 **الوصف:** {row['الوصف'] if 'الوصف' in row else 'لا يوجد'}")
                        if "رابط_الصورة" in row:
                            st.image(row["رابط_الصورة"], caption="الصورة التوضيحية")
        if __name__ == '__main__':
            main()
            
            

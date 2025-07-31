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
    


    page = st.sidebar.radio('Select page', ['STG-2024', 'View Logs'])
    
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
            
            tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
                'Reel Label (Small)', 'Reel Label (Large)',
                'Ink Reels for Label', 'Red Tape', 'Adhasive Tape', 'Cartridges', 'MultiPharma Cartridge'
            ])
            
            with tab1:
                Small = df_Material[df_Material['Item Name'] == 'Reel Label (Small)'].sort_values(by='Item Name')
                st.dataframe(Small, width=2000)
                col4, col5, col6 = st.columns([2,1,2])
                with col4:
                    display_tab('Reel Label (Small)', 20)
               
            with tab2:
                Large = df_Material[df_Material['Item Name'] == 'Reel Label (Large)'].sort_values(by='Item Name')
                st.dataframe(Large, width=2000)
                col4, col5, col6 = st.columns([2,1,2])
                with col4:
                    display_tab('Reel Label (Large)', 60)
            with tab3:
                Ink = df_Material[df_Material['Item Name'] == 'Ink Reels for Label'].sort_values(by='Item Name')
                st.dataframe(Ink, width=2000)
                col4, col5, col6 = st.columns([2,1,2])
                with col4:
                    display_tab('Ink Reels for Label', 20)
            with tab4:
                Tape = df_Material[df_Material['Item Name'] == 'Red Tape'].sort_values(by='Item Name')
                st.dataframe(Tape, width=2000)
                col4, col5, col6 = st.columns([2,1,2])
                with col4:
                    display_tab('Red Tape', 5)
            with tab5:
                Adhesive = df_Material[df_Material['Item Name'] == 'Adhasive Tape'].sort_values(by='Item Name')
                st.dataframe(Adhesive, width=2000)
                col4, col5, col6 = st.columns([2,2,2])
                with col4:
                    display_tab('Adhasive Tape', 100)
            with tab6:
                Cartridges = df_Material[df_Material['Item Name'] == 'Cartridges'].sort_values(by='Item Name')
                st.dataframe(Cartridges, width=2000)
                col4, col5, col6 = st.columns([2,1,2])
                with col4:
                    display_tab('Cartridges', 50)
            with tab7:
                MultiPharma = df_Material[df_Material['Item Name'] == 'MultiPharma Cartridge'].sort_values(by='Item Name')
                st.dataframe(MultiPharma, width=2000)
                col4, col5, col6 = st.columns([2,1,2])
                with col4:
                    display_tab('MultiPharma Cartridge', 5)

            st.button("Update page")
            csv = df_Material.to_csv(index=False)
            st.download_button(label="Download updated sheet", data=csv, file_name='matril.csv', mime='text/csv')
    
        if __name__ == '__main__':
            main()
    elif page == 'View Logs':
        st.header('User Activity Logs')
        st.dataframe(logs_df, width=1000, height=400)
        csv = logs_df.to_csv(index=False)
        st.download_button(label="Download Logs as CSV", data=csv, file_name='logs.csv', mime='text/csv')
            #if st.button("Clear Logs"):
                #clear_logs()

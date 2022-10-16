
from io import StringIO
from datetime import datetime    
import re
#import sqlite3
import datetime as dt
from pathlib import Path
import streamlit as st
import numpy as np
import pandas as pd
from numpy import random



def main():

    st.markdown(
            f"""
    <style>
        .reportview-container .main .block-container{{
            max-width: {'1900'}px;
            padding-top: {10}rem;
            padding-right: {2}rem;
            padding-left: {2}rem;
            padding-bottom: {10}rem;
        }}
        
    </style>
    """,
            unsafe_allow_html=True,
        )
     
    st.markdown(html_temp.format('#94A6A1','#18261B'),unsafe_allow_html=True)

    st.markdown('<br>',unsafe_allow_html=True);
  
    uploaded_file = st.sidebar.file_uploader("Az FB profile html beolvasása")
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        string_data = stringio.read()
        lista =re.findall('buddy_id(.+?)picture', string_data) 
        for i in range(len(lista)):
            lista[i] = re.findall('name\"\:"(.+?)\"\,', lista[i])
        df = pd.DataFrame(lista, columns={'name'})
        dict_hu = {'u00c1': 'Á','u00e1': 'á','u00f3': 'ó','u00e9': 'é','u0151': 'ő','u00f6': 'ö','u00ed': 'í','u00c9': 'É','u00fa': 'ú','u00fc': 'ü'}
        for key in dict_hu.keys():
            df['name'] = df['name'].str.replace(key, dict_hu[key])
            df['name'] = df['name'].str.replace('\\', '')
        df['rn']=df.index+1
        now = datetime.now()
        df['date']=now.strftime('%Y.%m.%d')
        df.columns =['name', 'rn','date']
        #df.to_sql('fb_buddy', conn, if_exists='append', index=False)

        st.table(df)
        


if __name__ == '__main__':
    main()
   # footer()

    
    
    
    
    
    
    
    
    
    
    

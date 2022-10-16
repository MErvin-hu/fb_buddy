
from io import StringIO
from datetime import datetime    
import re
import sqlite3
import datetime as dt
from pathlib import Path
import streamlit as st
import numpy as np
import pandas as pd
from numpy import random


from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb

st.set_page_config(page_title='FB buddy sorrend',page_icon=':male-student:')

def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 105px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="black",
        text_align="center",
        height="auto",
        opacity=1
    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(2)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def footer():
    myargs = [
        "Made in ",
        image('https://avatars3.githubusercontent.com/u/45109972?s=400&v=4',
              width=px(25), height=px(25)),
        " with ❤️", # by ",
        #link("https://", "D-Viz"),
        br(),
        link("https://buymeacoffee.com/ervin.murvai", image('https://i.imgur.com/thJhzOO.png')),
    ]
    layout(*myargs)



html_temp = """
<div style="background-color:{};padding:10px;border-radius:10px">
<h1 style="color:{};text-align:center;">FB buddy sorrend</h1>
</div>
"""
title_temp ="""
<div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
<h4 style="color:white;text-align:center;">{}</h1>
<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
<h6>Author:{}</h6>
<br/>
<br/> 
<p style="text-align:justify">{}</p>
</div>
"""
article_temp ="""
<div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
<h4 style="color:white;text-align:center;">{}</h1>
<h6>Author:{}</h6> 
<h6>Post Date: {}</h6>
<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;width: 50px;height: 50px;border-radius: 50%;" >
<br/>
<br/>
<p style="text-align:justify">{}</p>
</div>
"""
head_message_temp ="""
<div style="background-color:#464e5f;padding:10px;border-radius:5px;margin:10px;">
<h4 style="color:white;text-align:center;">{}</h1>
<img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;">
<h6>Author:{}</h6> 
<h6>Post Date: {}</h6> 
</div>
"""
full_message_temp ="""
<div style="background-color:#3B5659;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
<p style="text-align:justify;color:black;padding:10px">{}</p>
</div>
"""

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after {
                content:''; 
                visibility: visible;
                display: block;
                position: relative;
                #background-color: red;
                padding: 5px;
            top: 2px;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


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

    
    
    
    
    
    
    
    
    
    
    
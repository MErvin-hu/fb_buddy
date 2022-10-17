import pandas as pd
import plotly.express as px
import plotly as plt
import streamlit as st
import os
import requests
import numpy as np
import pydeck as pdk


st.set_page_config(page_title=None, page_icon=None, layout='centered', initial_sidebar_state='collapsed')


st.markdown(
    """
<style>
.sidebar .sidebar-content {
    background-image: linear-gradient(#3666A8,#1b2a40);
    color: white;
}
</style>
""",
    unsafe_allow_html=True,
)

html_temp = """
<div style="background-color:{};padding:0px;border-radius:10px">
<h1 style="color:{};text-align:center;">A szallas.hu adatai alapján készült kimutatás 2020.</h1>
</div>
"""


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
    
full_message_temp ="""
<div style="text-align:center;background-color:#3666A8;overflow-x: auto; padding:px;border-radius:10px;margin:0px; width:800px; height: 110px">
{}
</div>
"""    
#<p style="text-align:center;color:black;padding:0px">{}</p>	

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

local_css("style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

	
@st.cache(allow_output_mutation=True)
def get_data():
    #return pd.read_excel('c:\Sajat\Python_sajat_prog\szallas_streamlit\szallas_hu_2020_reservations_me.xlsx','Reservations')
    return pd.read_csv('https://docs.google.com/spreadsheets/d/1R8aTgvZVi6_cYvAE2a5tNvSxHQIMVfCA/gviz/tq?gid=1650570333&tq=select%20*&tqx=out:csv')


df_base = get_data()#
df_base.dropna() 

df_ter = df_base.groupby(['lat','lng','City'])['vendegejszaka'].sum().reset_index()

df_base["BookingMo"] = df_base["BookingMonth"]
df_base["ArrivalMo"] = df_base["ArrivalMonth"]

df_base["BookingMo"].replace({
                         1:"Jan",
                          2:'Feb',
                          3:'Márc',
                          4:'Árp',
                          5:'Máj',6:'Jún',7:'Júl',8:'Aug',
                          9:'Szept',10:'Okt',11:'Nov',12:'Dec'
                         }, inplace=True)
                         
df_base["ArrivalMo"].replace({
                         1:"Jan",
                          2:'Feb',
                          3:'Márc',
                          4:'Árp',
                          5:'Máj',6:'Jún',7:'Júl',8:'Aug',
                          9:'Szept',10:'Okt',11:'Nov',12:'Dec'
                         }, inplace=True)                         
 
honapok = ['Jan', 'Feb', 'Márc', 'Ápr', 'Máj', 'Jún',
          'Júl', 'Aug', 'Szept', 'Okt', 'Nov', 'Dec']    





def main():

    st.markdown(html_temp.format('#3666A8','#1b2a40'),unsafe_allow_html=True)
    
   # st.header("2020. szallas.hu adatai alapján készült kimutatás")

    
    
    st.sidebar.write("Beállítások")
    display_code = st.sidebar.radio("",("Vendégéjszakák", "Foglalások"),0)    
    
    bar_chkb = st.sidebar.checkbox("Időbeli változás", True, key=1)
    
    foglalasutazasdelta_chkb = st.sidebar.checkbox("Foglalás és indulás közötti összefüggés", True, key=1)
    
    treemap_chkb = st.sidebar.checkbox("Régió-település-átlagos vendégszám ", True, key=1)
    
    buborek_chkb = st.sidebar.checkbox("Szállás típus-vendégek száma-régiónként az idő függvényébe ", True, key=1)
    
    adattbl_chkb = st.sidebar.checkbox("Adattábla", True, key=1)

    df_base_agg2 = df_base.groupby(['ArrivalMonth','ArrivalMo','AccomodationType'],sort=True).size().reset_index(name='foglalasok')
    sumfoglalasok = df_base_agg2['foglalasok'].sum()
    
    df_base_agg1 = df_base.groupby(['ArrivalMonth','ArrivalMo','AccomodationType'],sort=True)['vendegejszaka'].sum().reset_index()
    sumvendegejszaka = df_base_agg1['vendegejszaka'].sum()
    
    sum_vendegejszaka = f"<h2>Összes <font color='#f2cc0c'>vendégéjszakák</font> száma a szallas.hu-n: <br><b><font color='#f2cc0c'>{sumvendegejszaka}</font></h2></b>" 
    sum_foglalasok = f"<h2>Összes <font color='#f8710a'>foglalások</font> száma a szallas.hu-n: <br><b><font color='#f8710a'>{sumfoglalasok}</font></h2></b>" 
    #sum_vendegejszaka = f"Összes vendégéjszakák száma: **{sumvendegejszaka:}**" #to_string(df_base_agg1['vendegejszaka'].sum())
    
    #st.markdown(full_message_temp.format(sum_vendegejszaka + "<br>KSH 2020.I-III.negyedévben az össz vendégéjszakák száma országosan: <b>11962636</b>"),unsafe_allow_html=True)

    col1, col2 = st.beta_columns(2)

#col1.header("Animáció")
#col1.plotly_chart(fig, use_column_width=True, width=90) 
#col2.header("Tree")
#col2.plotly_chart(fig_fa, use_column_width=True) 


###########################################
#   Oszlopdiagram Vendégéjszaka-Hónap
###########################################
    #df_base_agg1.sort_values('ArrivalMonth', ascending=False)
    
    if bar_chkb == 1:
        if display_code == "Vendégéjszakák":
            col1.markdown(full_message_temp.format(sum_vendegejszaka),unsafe_allow_html=True)
            fig1 = px.bar(df_base_agg1, x="ArrivalMo"
            , color="AccomodationType",
                y='vendegejszaka',
                title="Vendégéjszakák havi alakulása",
                barmode='relative',
                height=600,
                color_discrete_map={'apartment': '#00255C', 'guest_house': '#4483E1', 'hotel': '#0159DB' , 'pension': '#1C355C' } , #0043A8
                labels={
                        "ArrivalMo": "Hónap",
                        "vendegejszaka": "Vendégéjszakák száma",
                        "AccomodationType": "Szállás típusa"
                    },
                category_orders=dict(group=[['Jan', 'Feb', 'Márc', 'Ápr', 'Máj', 'Jún',
                'Júl', 'Aug', 'Szept', 'Okt', 'Nov', 'Dec']])
                )
            fig1.update_layout({'template':'plotly_dark'})
            fig1.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                        'paper_bgcolor': 'rgba(0, 0, 0, 0)'
                                    })            
            col1.plotly_chart(fig1)  
    
        elif display_code == "Foglalások":
            col1.markdown(full_message_temp.format(sum_foglalasok),unsafe_allow_html=True)
            fig1 = px.bar(df_base_agg2, x="ArrivalMo"
            , color="AccomodationType",
                y='foglalasok',
                title="Foglalások havi alakulása",
                barmode='relative',
                height=600,
                color_discrete_map={'apartment': '#00255C', 'guest_house': '#4483E1', 'hotel': '#0159DB' , 'pension': '#1C355C' } , #0043A8
                labels={
                        "ArrivalMo": "Hónap",
                        "foglalasok": "Foglalások száma",
                        "AccomodationType": "Szállás típusa"
                    },
                category_orders=dict(group=[['Jan', 'Feb', 'Márc', 'Ápr', 'Máj', 'Jún',
                'Júl', 'Aug', 'Szept', 'Okt', 'Nov', 'Dec']])
                )
            fig1.update_layout({'template':'plotly_dark'})
            fig1.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                   })            
            col1.plotly_chart(fig1)      




###########################################
#   Térkép oszlop
###########################################

    df_base_map_foglalas=df_base.groupby(['lng', 'lat','City'])['vendegejszaka'].count().reset_index()
    df_base_map_foglalas.rename(columns = {'vendegejszaka':'foglalas'}, inplace = True) 
    df_base_map_vendegejszaka=df_base.groupby(['lng', 'lat','City'])['vendegejszaka'].sum().reset_index()

    df_base_map_foglalas["vejszaka"] = df_base_map_foglalas.merge(
        df_base_map_vendegejszaka, left_on="City", right_on="City"
    )["vendegejszaka"]
    

    #st.write(df_base_map_foglalas)
   
    if display_code == "Vendégéjszakák":
        valtozo = 'vejszaka'
        terkep1a = pdk.Deck(tooltip = {"html": "Település: {City}<br> Vendégéjszaka: {vejszaka}"}, )
       
    elif display_code == "Foglalások":
        valtozo = 'foglalas'
        terkep1a = pdk.Deck(tooltip = {"html": "Település: {City}<br> Foglalás: {foglalas}"}, )
       
    
    hex_layer = pdk.Layer(
        "ColumnLayer",
        data = df_base_map_foglalas,#df_base_map_vendegejszaka,#[['lng', 'lat', 'vendegejszaka']],
        get_position=['lng', 'lat'],
        auto_highlight=True,
        get_elevation=valtozo,#"vendegejszaka",
        elevation_scale=5,
        pickable=True,
        elevation_range=[0, 3000],
        get_color="[242, 204, 12]",#67, 130, 166]",  #67,130,166    40, foglalas / 5000 * 255, 40, 150
        extruded=True,                 
        coverage=3)

    terkep1 = pdk.ViewState(longitude=19.1, latitude=47.0, zoom=6.7, min_zoom=5, max_zoom=15, pitch=40.5, bearing=5.36, height=600, width=900)
    
    if display_code == "Vendégéjszakák":
        terkep1a = pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v10",#streets-v11",#dark-v10",#light-v9",
            layers=[hex_layer],
            initial_view_state=terkep1,
            tooltip = {"html": "Település: {City}<br> Vendégéjszaka: {vejszaka}"}, 
            #{ "text": "{City}"},
            #"html": "Település: {City}<br> Foglalás: {vendegejszaka}"}, 
            )
    elif display_code == "Foglalások":
        terkep1a = pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v10",#light-v9",
            layers=[hex_layer],
            initial_view_state=terkep1,
            tooltip = {"html": "Település: {City}<br> Foglalás: {foglalas}"}, 
            #{ "text": "{City}"},
            #"html": "Település: {City}<br> Foglalás: {vendegejszaka}"}, 
            )

   
    col2.pydeck_chart(terkep1a)



###########################################
#   Animált buborék diagram
###########################################
    
    if buborek_chkb == 1:
        #df_base_agg2 = df_base.groupby(['Region','City','AccomodationType','ArrivalMonth','GuestCount'])['vendegejszaka'].sum().reset_index()
        df_base_agg2=df_base.groupby(['Region','AccomodationType','ArrivalMonth','ArrivalMo','GuestCount'])['vendegejszaka'].sum().reset_index()
        buborek_graph =px.scatter(df_base_agg2, x="Region", y="GuestCount", animation_frame="ArrivalMo",# animation_group="City",
            size="vendegejszaka", color="AccomodationType", #hover_name="City",
                                size_max=105,
                                labels={
                        "ArrivalMo": "Hónap",
                        "vendegejszaka": "Vendégéjszakák száma",
                        "AccomodationType": "Szállás típusa",
                        "GuestCount": "Vendégek száma/foglalás",
                        "Region":"Régió"
                    },
            #log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90]
        template='plotly_dark').update_layout( )
        buborek_graph.update_layout(height=500, width=900)    
        buborek_graph.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                    'paper_bgcolor': 'rgba(0, 0, 0, 0)'
                                   })                
        #st.plotly_chart(buborek_graph)     
        col1.plotly_chart(buborek_graph)
    
    
###########################################
#   Interaktív táblázat
###########################################    
    if adattbl_chkb == 1:
        option = col2.multiselect('Válassz települést',sorted(df_base_map_foglalas['City'].unique()), default=['Budapest'])
    #"Select option", options=sorted(df_base_map_foglalas['City'].unique()))
      
        tablazat1 = df_base_map_foglalas.loc[df_base_map_foglalas['City'].isin(option)]
        tablazat2 = tablazat1.reset_index()
        tablazat2.rename(columns = {'City':'Település', 'foglalas':'Foglalások száma', 'vejszaka':'Vendégéjszakák száma'}, inplace = True) 
    
        col2.write(tablazat2[['Település','Foglalások száma','Vendégéjszakák száma']].sort_values(by=['Település']))

###########################################
#   Treemaps
###########################################        
    if treemap_chkb == 1:
        fig_tmap = px.treemap(df_base, path=[px.Constant('Magyarország'), 'Region', 'City'], values='GuestCount',
                    color='GuestCount',# hover_data=['GuestCount'],
                            )
        fig_tmap.update_layout(template='plotly_dark').update_layout( )
        fig_tmap.update_layout(height=700, width=1000)    
        fig_tmap.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                        'paper_bgcolor': 'rgba(0, 0, 0, 0)'
                                    })                
        col2.plotly_chart(fig_tmap)

###########################################
#   Box
###########################################        
   # fig_violin = px.violin(df_base, y="DaysToGo", x="AccomodationType", color="LengthOfStay", box=True, points="all", hover_data=df_base.columns)    
    if foglalasutazasdelta_chkb==1:
        fig_box = px.box(df_base, x="AccomodationType", y="DaysToGo", color="LengthOfStay", notched=True)
        fig_box.update_layout(template='plotly_dark').update_layout( )
        fig_box.update_layout(height=700, width=1000)    
        fig_box.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                        'paper_bgcolor': 'rgba(0, 0, 0, 0)'
                                    })                
        col1.plotly_chart(fig_box)

##############################################################

    
##########################################
#    Menü
##########################################




#if st.sidebar.checkbox('adattábla'):
#    st.subheader('Raw data')
#    st.write(df_base)


if __name__ == '__main__':
	main()
    

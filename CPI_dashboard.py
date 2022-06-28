

import streamlit as st
import pandas as pd
import numpy as np
import datetime
from PIL import Image
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
#import win32com.client as win32
#import os

import streamlit.components.v1 as components
from dateutil import relativedelta
st.set_page_config(layout="wide")

data=pd.read_excel('CPI raw rebased series 2021.xlsx', sheet_name='Sheet1')
portal=pd.read_excel('Portal_Data_0306.xlsx', sheet_name='1 Table')
#st.dataframe(data)
#st.dataframe(portal)
#st.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:40px;border-radius:0%;">CPI</p>', unsafe_allow_html=True)

#remove extra spaces from end of a string
for i in range(len(portal)):
    portal['Country'][i]=portal['Country'][i].rstrip()
#Data date
mydate = datetime.datetime.now()
cpi_photo=Image.open('Capture.PNG')
#Country

country = 'Bahrain'
#missing dataframe
missing_bool=portal[portal['Country']==country].isnull().any().to_frame().reset_index()
last_data_month=portal[portal['Country']==country].columns[-1]
col1,col2,col3,col4=st.columns(4)
with col1:
    st.image(cpi_photo, width=500)
with col3:
    #Month 
    month_radio=st.radio('Do you want to specify the month?', ['Yes', 'No'], index=1 )
    if month_radio == 'No':
        if missing_bool[missing_bool[0]==True].empty:
                #st.markdown(f'<p style="text-align:left;font-style: italic;color:#0d0d0c;font-family:Arial;font-size:15px;border-radius:0%;"> No missing CPI data</p>', unsafe_allow_html=True)
                datetime_object = datetime.datetime.strptime(last_data_month, '%Y-%m')
                month= datetime_object.strftime("%B")
                #last data
                latest_month_nb=datetime_object.strftime("%m")
                year=datetime_object.strftime("%Y")            
                latest_date_data=year+'-'+latest_month_nb
                #missing data
                missing_date=datetime_object+ relativedelta.relativedelta(months=1)
                missing_month=missing_date.strftime("%B")
                missing_month_nb=missing_date.strftime("%m")
                missing_year=missing_date.strftime("%Y")
                missing_date_data=missing_year+'-'+missing_month_nb
            
                st.write("The specified month is", missing_month,", ", missing_year)
                displayed=missing_month+" "+ missing_year
        else:
                missing_month=missing_bool['index'].loc[missing_bool[0]==True].iloc[0]
                datetime_object = datetime.datetime.strptime(missing_month, '%Y-%m')
                month= datetime_object.strftime("%B")
                missing_year=datetime_object.strftime("%Y")
                #last data
                last_date=datetime_object+ relativedelta.relativedelta(months=-1)
                latest_month_nb=last_date.strftime("%m")
                year=last_date.strftime("%Y")            
                latest_date_data=year+'-'+latest_month_nb
                missing_date_data=missing_month
                displayed=month+" "+ missing_year
                st.markdown(f'<p style="text-align:left;font-style: italic;color:#0d0d0c;font-family:Arial;font-size:15px;border-radius:0%;">Needed Data Month: '+ str(month) + ' '+str(missing_year)+'</p>', unsafe_allow_html=True)
    else: #convert to number
        #month, year, space1, space2, space3=st.columns(5)
        month=st.selectbox("Month", ("January", "February", "March", "April", "May", "June", "July", "August", "October", "November", "December"))
        #year=st.selectbox("Year",("2010", "2011","2012","2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"), index=12)
        year=str(st.number_input('Year', min_value=2010, step=1, value=2020))
        st.write("The specified month is", month,", ", year)
        missing_data=month+' '+year
        missing_date_data=datetime.datetime.strptime(missing_data, '%B %Y').strftime('%Y-%m')
        latest_date_data=missing_bool['index'][missing_bool[0]==False][-1:].values[0]
        displayed=month+" "+ year

    #st.write(missing_month)
    #st.write(missing_date_data)
    #st.write(latest_date_data)
    #st.write(portal[latest_date_data][(portal['CPI groups']=='General CPI') & (portal['Country']=='Egypt')].values[0])

    
    #Unlock button
    m = st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #fc9a6d;
            font-family:Arial;
            text-align:center;
            color: black;
            height: 2em;
            width: 15em;
            border-radius:10px;
            border:1px solid #f0f0e4;
            font-size:12px;
            font-weight: bold;
            margin:0px;
            display: block;
        }

        div.stButton > button:hover {
	        background:linear-gradient(to bottom, #fc9a6d 5%, #ff5a5a 100%);
	        background-color:#fc9a6d;
        }

        div.stButton > button:active {
	        position:relative;
	        top:3px;
        }

        </style>""", unsafe_allow_html=True)   
    model_button=st.button(" Unlock Base Year 🔓")
    if "model_button" not in st.session_state:
        st.session_state.model_button=False

    if model_button or st.session_state.model_button:
        st.session_state.model_button=True
        #Base Year
        base_year_new=st.number_input('New Base Year', min_value=2010, step=1, value=2020)
        base_year_new_str=str(base_year_new)
        #col1_base,col2_base=st.columns([2,10])
        base_year=st.markdown(f'<p style="text-align:left;color:#0d0d0c;font-family:Arial Black;font-size:18px;border-radius:0%;">Base Year: '+ base_year_new_str + '</p>', unsafe_allow_html=True)

    else:
        #Base Year
        base_year=data['Year'][data['Country']==country]
        #col1_base,col2_base=st.columns([2,10])
        base_year=st.markdown(f'<p style="text-align:left;color:#0d0d0c;font-family:Arial Black;font-size:18px;border-radius:0%;">Base Year: '+ str(base_year.values[0]) + '</p>', unsafe_allow_html=True)

datetime_object_latest = datetime.datetime.strptime(latest_date_data, '%Y-%m')

full_month_name = datetime_object_latest.strftime("%B")
year_latest=datetime_object_latest.strftime("%Y")
latest_alpha=full_month_name+' '+year_latest

#CPI Data 
food_weight=data.iloc[:, 0][data["Country"]==country].values[0]
alcohol_weight=data.iloc[:, 1][data["Country"]==country].values[0]
cloths_weight=data.iloc[:, 2][data["Country"]==country].values[0]
house_weight=data.iloc[:, 3][data["Country"]==country].values[0]
furnish_weight=data.iloc[:, 4][data["Country"]==country].values[0]
health_weight=data.iloc[:, 5][data["Country"]==country].values[0]
trans_weight=data.iloc[:, 6][data["Country"]==country].values[0]
com_weight=data.iloc[:, 7][data["Country"]==country].values[0]
leis_weight=data.iloc[:, 8][data["Country"]==country].values[0]
edu_weight=data.iloc[:, 9][data["Country"]==country].values[0]
rest_weight=data.iloc[:, 10][data["Country"]==country].values[0]
mis_weight=data.iloc[:, 11][data["Country"]==country].values[0]
total_weight=food_weight+alcohol_weight+cloths_weight+house_weight+furnish_weight+health_weight+trans_weight+com_weight+leis_weight+edu_weight+rest_weight+mis_weight

food_cpi_last = portal[latest_date_data][(portal['CPI groups']=='Food and non-alcoholic beverages') & (portal['Country']==country)].values[0]
alcohol_cpi_last = portal[latest_date_data][(portal['CPI groups']=='Alcoholic beverages, tobacco and narcotics') & (portal['Country']==country)].values[0]
cloth_cpi_last = portal[latest_date_data][(portal['CPI groups']=='Clothing and footwear') & (portal['Country']==country)].values[0]
house_cpi_last = portal[latest_date_data][(portal['CPI groups']=='Housing, water, electricity, gas and other fuels') & (portal['Country']==country)].values[0]
furnish_cpi_last = portal[latest_date_data][(portal['CPI groups']=='Furnishings, household equipment and routine household maintenance') & (portal['Country']==country)].values[0]
health_cpi_last = portal[latest_date_data][(portal['CPI groups']=='Health') & (portal['Country']==country)].values[0]
trans_cpi_last = portal[latest_date_data][(portal['CPI groups']=='Transport') & (portal['Country']==country)].values[0]
comm_cpi_last = portal[latest_date_data][(portal['CPI groups']=='Information and Communication') & (portal['Country']==country)].values[0]
leis_cpi_last = portal[latest_date_data][(portal['CPI groups']=='Recreation, sport and culture') & (portal['Country']==country)].values[0]
edu_cpi_last = portal[latest_date_data][(portal['CPI groups']=='Education') & (portal['Country']==country)].values[0]
rest_cpi_last = portal[latest_date_data][(portal['CPI groups']=='Restaurants and accommodation services') & (portal['Country']==country)].values[0]
mis_cpi_last = portal[latest_date_data][(portal['CPI groups']=='Miscellaneous goods and services') & (portal['Country']==country)].values[0]
gen_cpi_last = portal[latest_date_data][(portal['CPI groups']=='General CPI') & (portal['Country']==country)].values[0]
with col4:
    #col_gen1, col_gen2,col_gen3, col_gen4=st.columns(4)
    #General
    #Miscellaneous goods and services
    gen_exp=st.expander('General CPI', expanded=True)
    #weight
    gen_exp.markdown(f'<i style="text-align:center;color:#0d0d0c;font-family:Arial;font-size:15px;border-radius:0%;">Weight: '+ str(round(total_weight,2)) + '</i>', unsafe_allow_html=True)
    #gen_exp.markdown(f'<p style="text-align:center;color:#0d0d0c;font-family:Arial;font-size:15px;border-radius:0%;">'+ str(round(total_weight,2)) + '</p>', unsafe_allow_html=True)
    #last available
    gen_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Last Available Data</p>', unsafe_allow_html=True)
    gen_exp.markdown(f'<span style="font-family:Arial;font-size:13px;">'+ str(latest_alpha)+'<br></span> <span style="margin:auto; display:table;font-family:Arial;font-size:20px;">'+ str(gen_cpi_last)+'</span>', unsafe_allow_html=True)
    #needed data
    gen_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Needed Index</p>', unsafe_allow_html=True)
    gen_cpi = gen_exp.text_input(displayed+'             ')

col1,col2,col3,col4=st.columns(4)
#food and non alcoholic beverages
food_exp=col1.expander('Food & Non-Alcoholic Beverages', expanded=False)
#food_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Weight</p>', unsafe_allow_html=True)
#weight
if "model_button" not in st.session_state:
    st.session_state.model_button=False

if model_button or st.session_state.model_button:
    st.session_state.model_button=True
    new_food_weight=food_exp.text_input('Weight '+str(base_year_new))
else:
    food_exp.markdown(f'<i style="text-align:center;color:#0d0d0c;font-family:Arial;font-size:15px;border-radius:0%;">Weight: '+ str(round(food_weight,2)) + '</i>', unsafe_allow_html=True)
#last available
food_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Last Available Data</p>', unsafe_allow_html=True)
food_exp.markdown(f'<span style="font-family:Arial;font-size:13px;">'+ str(latest_alpha)+'<br></span> <span style="margin:auto; display:table;font-family:Arial;font-size:20px;">'+ str(food_cpi_last)+ '</span>', unsafe_allow_html=True)
#needed data
food_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Needed Index</p>', unsafe_allow_html=True)
food_cpi = food_exp.text_input(displayed)

#Alcoholic Beverages, Tobacco and Narcotics
alcohol_exp=col2.expander('Alcoholic Beverages & Tobacco', expanded=False)
#alcohol_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Weight</p>', unsafe_allow_html=True)
#weight
if "model_button" not in st.session_state:
    st.session_state.model_button=False

if model_button or st.session_state.model_button:
    st.session_state.model_button=True
    new_alcohol_weight=alcohol_exp.text_input('Weight '+str(base_year_new)+' ')
else:
    alcohol_exp.markdown(f'<i style="text-align:center;color:#0d0d0c;font-family:Arial;font-size:15px;border-radius:0%;">Weight: '+ str(round(alcohol_weight,2)) + '</i>', unsafe_allow_html=True)
#last available
alcohol_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Last Available Data</p>', unsafe_allow_html=True)
alcohol_exp.markdown(f'<span style="font-family:Arial;font-size:13px;">'+ str(latest_alpha)+'<br></span> <span style="margin:auto; display:table;font-family:Arial;font-size:20px;">'+ str(alcohol_cpi_last)+ '</span>', unsafe_allow_html=True)
#needed data
alcohol_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Needed Index</p>', unsafe_allow_html=True)
alcohol_cpi = alcohol_exp.text_input(displayed+' ')

#Clothing and Footwear
cloth_exp=col3.expander('Clothing & Footwear', expanded=False)
#weight
#cloth_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Weight</p>', unsafe_allow_html=True)
if "model_button" not in st.session_state:
    st.session_state.model_button=False

if model_button or st.session_state.model_button:
    st.session_state.model_button=True
    new_cloth_weight=cloth_exp.text_input('Weight '+str(base_year_new)+'  ')
else:
    cloth_exp.markdown(f'<i style="text-align:center;color:#0d0d0c;font-family:Arial;font-size:15px;border-radius:0%;">Weight: '+ str(round(cloths_weight,2)) + '</i>', unsafe_allow_html=True)
#last available
cloth_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Last Available Data</p>', unsafe_allow_html=True)
cloth_exp.markdown(f'<span style="font-family:Arial;font-size:13px;">'+ str(latest_alpha)+'<br></span> <span style="margin:auto; display:table;font-family:Arial;font-size:20px;">'+ str(cloth_cpi_last)+ '</span>', unsafe_allow_html=True)
#needed data
cloth_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Needed Index</p>', unsafe_allow_html=True)
cloth_cpi = cloth_exp.text_input(displayed+'  ')

#Housing, Water, Electricity, Gas and Other Fuels
house_exp=col4.expander('Housing, Water, Electricity, & Other Fuels', expanded=False)
#weight
#house_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Weight</p>', unsafe_allow_html=True)
if "model_button" not in st.session_state:
    st.session_state.model_button=False

if model_button or st.session_state.model_button:
    st.session_state.model_button=True
    new_house_weight=house_exp.text_input('Weight '+str(base_year_new)+'   ')
else:
    house_exp.markdown(f'<i style="text-align:center;color:#0d0d0c;font-family:Arial;font-size:15px;border-radius:0%;">Weight: '+ str(round(house_weight,2)) + '</i>', unsafe_allow_html=True)
#last available
house_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Last Available Data</p>', unsafe_allow_html=True)
house_exp.markdown(f'<span style="font-family:Arial;font-size:13px;">'+ str(latest_alpha)+'<br></span> <span style="margin:auto; display:table;font-family:Arial;font-size:20px;">'+ str(house_cpi_last)+ '</span>', unsafe_allow_html=True)
#needed data
house_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Needed Index</p>', unsafe_allow_html=True)
house_cpi = house_exp.text_input(displayed+'    ')

#Furnishings, Household Equipment and Routine Household Maintenance
furnish_exp=col1.expander('Furnishings, Equipment & Maintenance', expanded=False)
#weight
#furnish_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Weight</p>', unsafe_allow_html=True)
if "model_button" not in st.session_state:
    st.session_state.model_button=False

if model_button or st.session_state.model_button:
    st.session_state.model_button=True
    new_furnish_weight=furnish_exp.text_input('Weight '+str(base_year_new)+'    ')
else:
    furnish_exp.markdown(f'<i style="text-align:center;color:#0d0d0c;font-family:Arial;font-size:15px;border-radius:0%;">Weight: '+ str(round(furnish_weight,2)) + '</i>', unsafe_allow_html=True)
#last available
furnish_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Last Available Data</p>', unsafe_allow_html=True)
furnish_exp.markdown(f'<span style="font-family:Arial;font-size:13px;">'+ str(latest_alpha)+'<br></span> <span style="margin:auto; display:table;font-family:Arial;font-size:20px;">'+ str(furnish_cpi_last)+ '</span>', unsafe_allow_html=True)
#needed data
furnish_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Needed Index</p>', unsafe_allow_html=True)
furnish_cpi = furnish_exp.text_input(displayed+'     ')


#Health
health_exp=col2.expander('Health', expanded=False)
#weight
#health_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Weight</p>', unsafe_allow_html=True)
if "model_button" not in st.session_state:
    st.session_state.model_button=False

if model_button or st.session_state.model_button:
    st.session_state.model_button=True
    new_health_weight=health_exp.text_input('Weight '+str(base_year_new)+'     ')
else:
    health_exp.markdown(f'<i style="text-align:center;color:#0d0d0c;font-family:Arial;font-size:15px;border-radius:0%;">Weight: '+ str(round(health_weight,2)) + '</i>', unsafe_allow_html=True)
#last available
health_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Last Available Data</p>', unsafe_allow_html=True)
health_exp.markdown(f'<span style="font-family:Arial;font-size:13px;">'+ str(latest_alpha)+'<br></span> <span style="margin:auto; display:table;font-family:Arial;font-size:20px;">'+ str(health_cpi_last)+ '</span>', unsafe_allow_html=True)
#needed data
health_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Needed Index</p>', unsafe_allow_html=True)
health_cpi = health_exp.text_input(displayed+'      ')

#Transport
trans_exp=col3.expander('Transport', expanded=False)
#weight
#trans_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Weight</p>', unsafe_allow_html=True)
if "model_button" not in st.session_state:
    st.session_state.model_button=False

if model_button or st.session_state.model_button:
    st.session_state.model_button=True
    new_trans_weight=trans_exp.text_input('Weight '+str(base_year_new)+'      ')
else:
    trans_exp.markdown(f'<i style="text-align:center;color:#0d0d0c;font-family:Arial;font-size:15px;border-radius:0%;">Weight: '+ str(round(trans_weight,2)) + '</i>', unsafe_allow_html=True)
#last available
trans_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Last Available Data</p>', unsafe_allow_html=True)
trans_exp.markdown(f'<span style="font-family:Arial;font-size:13px;">'+ str(latest_alpha)+'<br></span> <span style="margin:auto; display:table;font-family:Arial;font-size:20px;">'+ str(trans_cpi_last)+ '</span>', unsafe_allow_html=True)
#needed data
trans_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Needed Index</p>', unsafe_allow_html=True)
trans_cpi = trans_exp.text_input(displayed+'       ')

#Information and Communication
comm_exp=col4.expander('Information & Communication', expanded=False)
#weight
#comm_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Weight</p>', unsafe_allow_html=True)
if "model_button" not in st.session_state:
    st.session_state.model_button=False

if model_button or st.session_state.model_button:
    st.session_state.model_button=True
    new_comm_weight=comm_exp.text_input('Weight '+str(base_year_new)+'       ')
else:
    comm_exp.markdown(f'<i style="text-align:center;color:#0d0d0c;font-family:Arial;font-size:15px;border-radius:0%;">Weight: '+ str(round(com_weight,2)) + '</i>', unsafe_allow_html=True)
#last available
comm_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Last Available Data</p>', unsafe_allow_html=True)
comm_exp.markdown(f'<span style="font-family:Arial;font-size:13px;">'+ str(latest_alpha)+'<br></span> <span style="margin:auto; display:table;font-family:Arial;font-size:20px;">'+ str(comm_cpi_last)+ '</span>', unsafe_allow_html=True)
#needed data
comm_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Needed Index</p>', unsafe_allow_html=True)
comm_cpi = comm_exp.text_input(displayed+'        ')

#Recreation, sport and culture
leis_exp=col1.expander('Recreation, Sport & Culture', expanded=False)
#weight
#leis_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Weight</p>', unsafe_allow_html=True)
if "model_button" not in st.session_state:
    st.session_state.model_button=False

if model_button or st.session_state.model_button:
    st.session_state.model_button=True
    new_leis_weight=leis_exp.text_input('Weight '+str(base_year_new)+'        ')
else:
    leis_exp.markdown(f'<i style="text-align:center;color:#0d0d0c;font-family:Arial;font-size:15px;border-radius:0%;">Weight: '+ str(round(leis_weight,2)) + '</i>', unsafe_allow_html=True)
#last available
leis_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Last Available Data</p>', unsafe_allow_html=True)
leis_exp.markdown(f'<span style="font-family:Arial;font-size:13px;">'+ str(latest_alpha)+'<br></span> <span style="margin:auto; display:table;font-family:Arial;font-size:20px;">'+ str(leis_cpi_last)+ '</span>', unsafe_allow_html=True)
#needed data
leis_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Needed Index</p>', unsafe_allow_html=True)
leis_cpi = leis_exp.text_input(displayed+'         ')

#Education
edu_exp=col2.expander('Education', expanded=False)
#weight
#edu_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Weight</p>', unsafe_allow_html=True)
if "model_button" not in st.session_state:
    st.session_state.model_button=False

if model_button or st.session_state.model_button:
    st.session_state.model_button=True
    new_edu_weight=edu_exp.text_input('Weight '+str(base_year_new)+'         ')
else:
    edu_exp.markdown(f'<i style="text-align:center;color:#0d0d0c;font-family:Arial;font-size:15px;border-radius:0%;">Weight: '+ str(round(edu_weight,2)) + '</i>', unsafe_allow_html=True)
#last available
edu_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Last Available Data</p>', unsafe_allow_html=True)
edu_exp.markdown(f'<span style="font-family:Arial;font-size:13px;">'+ str(latest_alpha)+'<br></span> <span style="margin:auto; display:table;font-family:Arial;font-size:20px;">'+ str(edu_cpi_last)+ '</span>', unsafe_allow_html=True)
#needed data
edu_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Needed Index</p>', unsafe_allow_html=True)
edu_cpi = edu_exp.text_input(displayed+'          ')

#Restaurants and accommodation services
rest_exp=col3.expander('Restaurants & Accommodation Services', expanded=False)
#weight
#rest_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Weight</p>', unsafe_allow_html=True)
if "model_button" not in st.session_state:
    st.session_state.model_button=False

if model_button or st.session_state.model_button:
    st.session_state.model_button=True
    new_rest_weight=rest_exp.text_input('Weight '+str(base_year_new)+'          ')
else:
    rest_exp.markdown(f'<i style="text-align:center;color:#0d0d0c;font-family:Arial;font-size:15px;border-radius:0%;">Weight: '+ str(round(rest_weight,2)) + '</i>', unsafe_allow_html=True)
#last available
rest_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Last Available Data</p>', unsafe_allow_html=True)
rest_exp.markdown(f'<span style="font-family:Arial;font-size:13px;">'+ str(latest_alpha)+'<br></span> <span style="margin:auto; display:table;font-family:Arial;font-size:20px;">'+ str(rest_cpi_last)+ '</span>', unsafe_allow_html=True)
#needed data
rest_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Needed Index</p>', unsafe_allow_html=True)
rest_cpi = rest_exp.text_input(displayed+'           ')

#Miscellaneous goods and services
mis_exp=col4.expander('Miscellaneous Goods & Services', expanded=False)
#weight
#mis_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Weight</p>', unsafe_allow_html=True)
if "model_button" not in st.session_state:
    st.session_state.model_button=False

if model_button or st.session_state.model_button:
    st.session_state.model_button=True
    new_mis_weight=mis_exp.text_input('Weight '+str(base_year_new)+'           ')
else:
    mis_exp.markdown(f'<i style="text-align:center;color:#0d0d0c;font-family:Arial;font-size:15px;border-radius:0%;">Weight: '+ str(round(mis_weight,2)) + '</i>', unsafe_allow_html=True)
#last available
mis_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Last Available Data</p>', unsafe_allow_html=True)
mis_exp.markdown(f'<span style="font-family:Arial;font-size:13px;">'+ str(latest_alpha)+'<br></span> <span style="margin:auto; display:table;font-family:Arial;font-size:20px;">'+ str(mis_cpi_last)+ '</span>', unsafe_allow_html=True)
#needed data
mis_exp.markdown(f'<p style="text-align:center; background-color:#f5f5ed;color:#0d0d0c;font-family:Arial Black;font-size:15px;border-radius:0%;">Needed Index</p>', unsafe_allow_html=True)
mis_cpi = mis_exp.text_input(displayed+'            ')

st.markdown('<p></p>', unsafe_allow_html=True)

col1, col2,col3, col4,col5,col6,col7=st.columns(7)
#contact_form = """
#<form action="https://formsubmit.co/cpi_online@outlook.com" method="POST">
#     <input type="hidden" name="_captcha" value="false">
#     <button type="submit">Submit & Send</button>
#</form>
#"""

#submit=col3.markdown(contact_form, unsafe_allow_html=True)

## Use Local CSS File
#def local_css(file_name):
#    with open(file_name) as f:
#        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


#local_css("C:/Users/10197378/OneDrive/Capstone/streamlit/Buttons/style/style.css")

submit=col4.button("Submit and Send")
#st.write(type(gen_cpi))
#gen_cpi=float(gen_cpi)
#st.write(type(gen_cpi))
#st.write(missing_date_data)
#st.write(type(missing_date_data))

if submit:
     
        st.markdown('<h3 style="text-align:center;color:#0d0d0c;font-family:Arial Black;font-size:35px;border-radius:0%;">Thank you! Your CPI data was sent.</h3>', unsafe_allow_html=True)
        try:
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='General CPI')]=float(gen_cpi)
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='Food and non-alcoholic beverages')]=float(food_cpi)
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='Alcoholic beverages, tobacco and narcotics')]=float(alcohol_cpi)
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='Clothing and footwear')]=float(cloth_cpi)
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='Housing, water, electricity, gas and other fuels')]=float(house_cpi)
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='Furnishings, household equipment and routine household maintenance')]=float(furnish_cpi)
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='Health')]=float(health_cpi)
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='Transport')]=float(trans_cpi)
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='Information and Communication')]=float(comm_cpi)
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='Recreation, sport and culture')]=float(leis_cpi)
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='Education')]=float(edu_cpi)
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='Restaurants and accommodation services')]=float(rest_cpi)
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='Miscellaneous goods and services')]=float(mis_cpi)
        except:
            portal[missing_date_data] = np.nan
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='General CPI')]=float(gen_cpi)
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='Food and non-alcoholic beverages')]=float(food_cpi)
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='Alcoholic beverages, tobacco and narcotics')]=float(alcohol_cpi)
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='Clothing and footwear')]=float(cloth_cpi)
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='Housing, water, electricity, gas and other fuels')]=float(house_cpi)
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='Furnishings, household equipment and routine household maintenance')]=float(furnish_cpi)
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='Health')]=float(health_cpi)
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='Transport')]=float(trans_cpi)
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='Information and Communication')]=float(comm_cpi)
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='Recreation, sport and culture')]=float(leis_cpi)
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='Education')]=float(edu_cpi)
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='Restaurants and accommodation services')]=float(rest_cpi)
            portal[missing_date_data][(portal['Country']==country)&(portal['CPI groups']=='Miscellaneous goods and services')]=float(mis_cpi)
        portal.to_excel('Portal_Data_0306.xlsx', sheet_name='1 Table')
        try:
            data['Year'][(data['Country']==country)]=float(base_year_new_str)
            data['Food and non-alcoholic beverages'][(data['Country']==country)]=float(new_food_weight)
            data['Alcoholic beverages, tobacco and narcotics'][(data['Country']==country)]=float(new_alcohol_weight)
            data['Clothing and footwear'][(data['Country']==country)]=float(new_cloth_weight)
            data['Housing, water, electricity, gas and other fuels'][(data['Country']==country)]=float(new_house_weight)
            data['Furnishings, household equipment and routine household maintenance'][(data['Country']==country)]=float(new_furnish_weight)
            data['Health'][(data['Country']==country)]=float(new_health_weight)
            data['Transport'][(data['Country']==country)]=float(new_trans_weight)
            data['Information and Communication'][(data['Country']==country)]=float(new_comm_weight)
            data['Recreation, sport and culture'][(data['Country']==country)]=float(new_leis_weight)
            data['Education'][(data['Country']==country)]=float(new_edu_weight)
            data['Restaurants and accommodation services'][(data['Country']==country)]=float(new_rest_weight)
            data['Miscellaneous goods and services'][(data['Country']==country)]=float(new_mis_weight)
            data.to_excel('CPI raw rebased series 2021.xlsx', sheet_name='Sheet1')
        except:
            pass





        data_sent = {'Country':country,
            missing_date_data: [food_cpi,alcohol_cpi, cloth_cpi,house_cpi,furnish_cpi,health_cpi,trans_cpi,comm_cpi,leis_cpi,edu_cpi,rest_cpi,mis_cpi,gen_cpi], 
                'CPI groups': ['Food and non-alcoholic beverages','Alcoholic beverages, tobacco and narcotics','Clothing and footwear','Housing, water, electricity, gas and other fuels',
                               'Furnishings, household equipment and routine household maintenance','Health','Transport','Information and Communication','Recreation, sport and culture',
                               'Education','Restaurants and accommodation services','Miscellaneous goods and services','General CPI']}  
  

        df = pd.DataFrame(data_sent)
        if "model_button" not in st.session_state:
            st.session_state.model_button=False

        if model_button or st.session_state.model_button:
            st.session_state.model_button=True
            df['New Base Year']=base_year_new
        
            df['New Weight']=[new_food_weight,new_alcohol_weight,new_cloth_weight,new_house_weight,new_furnish_weight,new_health_weight,new_trans_weight,new_comm_weight,new_leis_weight,
                              new_edu_weight,new_rest_weight,new_mis_weight,'100']
        st.session_state.model_button=False
        df.to_excel('CPI_online.xlsx', sheet_name='Sheet1')
	#send email
        fromaddr = 'koteichghina@gmail.com'
        toaddr = ['ghina.koteich@un.org']

        msg = MIMEMultipart()

        msg['From'] = fromaddr
        msg['To'] = ", ".join(toaddr)
        msg['Subject'] = "NEW Bahrain CPI Data"

        body = "Kindly, find attached the recently submitted CPI Data by Bahrain NSO."

        msg.attach(MIMEText(body, 'plain'))
        filename = "CPI_online.xlsx"
        attachment = open("CPI_online.xlsx","rb")

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        msg.attach(part)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, 'vuzlwmedxabnnzyz') #Type Password
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()

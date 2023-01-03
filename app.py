import streamlit as st
import re
import pandas as pd
from ipynb.fs.full.get_variables import get_all_variables
from ipynb.fs.full.others import *
from ipynb.fs.full.regex import *
from ipynb.fs.full.output_df import list_to_df
import PyPDF2



#MAIN
st.title("Get the data from the [SHARE study](https://share-eric.eu) you want in 3 easy steps")




#SIDEBAR
st.sidebar.markdown("## The app")
st.sidebar.markdown("In this app, you have the possibility to choose the variables from the [SHARE study](https://share-eric.eu) you are interested in at a given wave. From these, you can then retrieve a csv file containing these variables and the merge identifier (called 'mergeid' in SHARE).")

st.sidebar.markdown("## About us")
st.sidebar.markdown("French statistics students from the Bordeaux School of Economics.")
st.sidebar.markdown("Contact: blabla@gmail.com")




#MAIN
data_load_state = st.text("Loading data... (wait until the end)")

#Step 1: choose a wave
years = ["2004", "2006/7", "2008/9", "2011", "2013", "2015", "2017", "2019/20"]
waves = years[0]
st.markdown("### Step 1: select a wave")
waves = ["wave "+str(i)+"  (published in "+year+")" for i,year in zip(range(1,9), years)]

wave = st.selectbox("Choose the wave you want to get the data from", waves)
wave_selected = re.search(r'\d+', wave)
suffix = wave_selected.group()
st.write(f"You have selected the {th(int(suffix))} wave.")

#Step 2: choose the variables
st.markdown("### Step 2: select variables")
variables = st.multiselect(f"Select variables from the choosen wave (max is 10)",
                           get_all_variables(int(wave_selected.group())),
                           max_selections=10)
list_var = list(variables)
st.markdown("##### *You have selected the following variables:*")
path = "/Users/josephbarbier/Desktop/PROJETpython/questionnaire/wave1questionnaire.pdf"
documentation = extract_text_from_pdf(pdf_file=path)
for var in list_var:
    clean_name = extract_description(var.upper(), text_to_scrap=documentation)
    st.write(var + ": "+change_case(clean_name))

data_load_state.text("Data loaded!")





#Step 3: retrieve your data!
st.markdown("### Step 3: get the data")
data = list_to_df(wave=int(suffix), variables=list_var)
st.dataframe(data.head())
st.download_button(label="Get the data",
                   data=data.to_csv().encode('utf-8'),
                   file_name = "my_share_data.csv")










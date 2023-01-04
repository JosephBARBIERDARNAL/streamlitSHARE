import streamlit as st
import re
import pandas as pd
from ipynb.fs.full.get_variables import get_all_variables
from ipynb.fs.full.others import *
from ipynb.fs.full.regex import *
from ipynb.fs.full.output_df import list_to_df
import PyPDF2


st.title("Get the data from the [SHARE study](https://share-eric.eu) you want in 3 easy steps")






#SIDEBAR

#the app description
st.sidebar.markdown("## The app")
st.sidebar.markdown("In this app, you have the possibility to choose the variables from the [SHARE study](https://share-eric.eu) you are interested in at a given wave. From these, you can then retrieve a csv file containing these variables and the merge identifier (called 'mergeid' in SHARE).")

#source code
st.sidebar.markdown("## Source code")
st.sidebar.markdown("You can fin the source code at this [Github](https://github.com/JosephBARBIERDARNAL)")


#about us description
st.sidebar.markdown("## About us")
st.sidebar.markdown("French statistics students from the Bordeaux School of Economics.")
st.sidebar.markdown("Contact: blabla@gmail.com")







#MAIN

data_load_state = st.text("LOADING...")


#STEP 1: CHOOSE A WAVE

#create wave full names
years = ["2004", "2006/7", "2008/9", "2011", "2013", "2015", "2017", "2019/20"]
waves = years[0]
st.markdown("### Step 1: select a wave")
waves = ["wave "+str(i)+"  (published in "+year+")" for i,year in zip(range(1,9), years)]

#scrolling bar
wave = st.selectbox("Choose the wave you want to get the data from", waves)

#output the wave choosen
selected_wave = re.search(r'\d+', wave)
suffix = selected_wave.group()
st.write(f"You have selected the {th(int(suffix))} wave.")
if int(suffix) not in [i for i in range(1,9)]:
    print("There is a problem")

    
    
    

#STEP 2 : CHOOSE THE VARIABLES

#get variables from the selected wave and scrolling bar
st.markdown("### Step 2: select variables")
variables = st.multiselect(f"Select variables from the choosen wave (max is 10)",
                           get_all_variables(int(selected_wave.group())),
                           max_selections=10)

#output the choosen variables
#to do this, we get the "cleaned" name of the variables (thanks to regex) in order to
#allow the user to check which variables have been chosen. 
list_var = list(variables)
st.markdown("##### *You have selected the following variables:*")

#path where to find the documentation of each wave
path = f"/Users/josephbarbier/Desktop/PROJETpython/questionnaire/wave{suffix}questionnaire.pdf"

#if the wave choosen is in the wave 1 or 2, use this code
if int(suffix) in [1, 2]:
    documentation = remove_selected(extract_text_from_pdf(pdf_file=path))
    for var in list_var:
        clean_name = get_description_12(var.upper(), text_to_scrap=documentation)
        st.write(var + ": "+change_case(clean_name, int(suffix)))

#if the wave choosen is in the wave 4, 5 ,6, 7 or 8, use thise code
if int(suffix) in [4,5,6,7,8]:
    documentation = extract_text_from_pdf(pdf_file=path)
    for var in list_var:
        clean_name = get_description_45678(var.upper(), text_to_scrap=documentation)
        st.write(var + ": "+change_case(clean_name, int(suffix)))

#if the wave choosen is in the wave 3, use this code
if int(suffix) == 3:
    documentation = extract_text_from_pdf(pdf_file=path)
    for var in list_var:
        clean_name = get_description_3(var.upper(), text_to_scrap=documentation)
        st.write(var + ": "+change_case(clean_name, int(suffix)))


        
        
#STEP 3: RETRIEVE YOUR DATA!

st.markdown("### Step 3: get the data")

#add the mergeid and the country, and transform the list into a df
list_var.extend(["mergeid","country"])
data = list_to_df(wave=int(suffix), variables=list_var)
if len(list_var) > 2:
    st.dataframe(data.head())

#print NA percentage of each variable
for var in data:
    tot_na = data[var].isna().sum()
    na_percent = round(tot_na/len(data)*100,2)
    st.write(f"Percentage of NAs from the variable {data[var].name}: {na_percent}%\n")


    


#return the df cleaned
df_to_return = data.to_csv().encode('utf-8')
#df_to_return = df_to_return.dropna(axis=1, how='all')
st.download_button(label="Dowload the dataset",
                   data=df_to_return,
                   file_name = "my_share_data.csv")


data_load_state.text("Data loaded!")







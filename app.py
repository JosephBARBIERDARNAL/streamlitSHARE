import streamlit as st
import re
import os
import numpy as np
import pandas as pd
from ipynb.fs.full.get_variables import get_all_variables
from ipynb.fs.full.others import *
from ipynb.fs.full.regex import *
from ipynb.fs.full.output_df import list_to_df
import PyPDF2







#START

st.title("Data exploration of the [SHARE study](https://share-eric.eu)")


st.text("")
st.text("")
st.text("") 






#get file directory
st.markdown("## Working directory")
st.markdown("Enter your working directory")
full_path = st.text_input("example: /Users/josephbarbier/Desktop/PROJETpython/", '/Users/josephbarbier/Desktop/PROJETpython/')
st.write("Current directory:", full_path)
st.text("")
st.markdown("***If you obtain the following error, your working directory is probably wrong. Verify that you did not change any file or folder name before using the app.***")
st.code("FileNotFoundError: [Errno 2] No such file or directory:")


st.text("")
st.text("")
st.text("")








#SIDEBAR

#the app description
st.sidebar.markdown("## The app")
st.sidebar.markdown("In this app, you have the possibility to choose the variables from the [SHARE study](https://share-eric.eu) you are interested in at a given wave. From these, you can then retrieve a csv file containing these variables and the merge identifier (called 'mergeid' in SHARE).")
st.sidebar.markdown("")

#source code
st.sidebar.markdown("## Source code")
st.sidebar.markdown("You can find the source code on this [Github repository](https://github.com/JosephBARBIERDARNAL/streamlitSHARE)")


#about us description
st.sidebar.markdown("## About us")
st.sidebar.markdown("French statistics students from the Bordeaux School of Economics.")
st.sidebar.markdown("Contact: blabla@gmail.com")







#MAIN


#STEP 1: CHOOSE A WAVE


#create wave full names
years = ["2004", "2006/7", "2008/9", "2011", "2013", "2015", "2017", "2019/20"]
waves = years[0]
st.markdown("## Select a wave")
st.markdown("**The SHARE database is separated into 8 different waves of questionnaires spread over time. Choose the period or wave you are interested in *before proceeding* to the next step.**")
waves = ["wave "+str(i)+"  (published in "+year+")" for i,year in zip(range(1,9), years)]

#scrolling bar
wave = st.selectbox("Choose the wave you want to get the data from", waves)

#output the wave choosen
selected_wave = re.search(r'\d+', wave)
wave_chosen = int(selected_wave.group())
st.write(f"You have selected the {th(wave_chosen)} wave.")
if wave_chosen not in [i for i in range(1,9)]:
    print("There is a problem")

    
st.text("")
st.text("")
st.text("")    
    
    
    
    
    


#STEP 2 : CHOOSE THE VARIABLES


#get variables from the selected wave and scrolling bar
st.markdown("## Select variables")
variables = st.multiselect(f"Select variables from the choosen wave (max is 10)",
                           get_all_variables(path=full_path, wave=wave_chosen),
                           max_selections=10)

#output the choosen variables
#to do this, we get the "cleaned" name of the variables (thanks to regex) in order to
#allow the user to check which variables have been chosen. 
list_var = list(variables)
st.markdown("##### *You have selected the following variables:*")

#path where to find the documentation of each wave
path = f"{full_path}/questionnaire/wave{str(wave_chosen)}questionnaire.pdf"
docu = extract_text_from_pdf(pdf_file=path)

#use different function to get the description of the variables chosen depending on the wave
clean_names = []
for i,var in zip(range(len(list_var)), list_var):
    if wave_chosen in [1, 2]:
        docu = remove_selected(docu)
        clean_names.append(get_description_12(var.upper(), text_to_scrap=docu))
    if wave_chosen in [4,5,6,7,8]:
        clean_names.append(get_description_45678(var.upper(), text_to_scrap=docu))
    if wave_chosen == 3:
        clean_names.append(get_description_3(var.upper(), text_to_scrap=docu))
    
    #print the variables chosen and their full name
    st.write(var + ": "+change_case(clean_names[i], wave_chosen))


    
st.text("")
st.text("")
st.text("")        








#STEP 3: RETRIEVE YOUR DATA!



st.markdown("## Quick overview of the data")

#add the mergeid and the country, and transform the list into a df
list_var.extend(["mergeid","country"])
clean_names.extend(["mergeid","country"])
data = list_to_df(wave=wave_chosen, variables=list_var, path=full_path)
row, col = data.shape

#print shape of the df
st.markdown("***Shape of the current dataset***")
st.write(f"Sample size: {row}. Number of cols: {col}")
#st.write(f"Number of cols: {col}")



#print some informations about the variables chosen
if len(list_var) > 2:
    
    #print head of the df
    st.dataframe(data.head())
    
    st.markdown("***Percentage of NAs of each variable:***")
    for i,var in zip(range(len(list_var)), list_var):
        tot_na = data[var].isna().sum()
        na_percent = round(tot_na/len(data)*100,2)
        clean_name = change_case(clean_names[i], wave_chosen)
        st.write(f"{data[var].name} ({clean_name}): {na_percent}%")

        
        
st.text("")
st.text("")
st.text("")        







#STEP 4: ANALYSIS
st.markdown("## Analysis")       

    
#clean each variable and print its descriptive statistics
for var in list_var[:-2]:
    data[var] = qual_to_quant(data, var)
    st.write(var, data[var].dtype)
    stat(data, var)        
        
   
        
        
        
        
st.text("")
st.text("")
st.text("") 
st.text("")
st.text("")
st.text("") 
st.text("")
st.text("")
st.text("") 
        
#return the df cleaned
df_to_return = data.to_csv().encode('utf-8')
st.download_button(label="Dowload the dataset",
                   data=df_to_return,
                   file_name = "my_share_data.csv")





st.markdown("***Selectionnez le graphique ***")





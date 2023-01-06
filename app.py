#import basic packages
import streamlit as st
import re
import os
import numpy as np
import pandas as pd
import PyPDF2
import matplotlib.pyplot as plt

#import our functions
from ipynb.fs.full.get_variables import get_all_variables
from ipynb.fs.full.cleaning import *
from ipynb.fs.full.regex import *
from ipynb.fs.full.output_df import *
from ipynb.fs.full.graph import graph
from ipynb.fs.full.modelling import *

#import function for the modelling part
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.preprocessing import OneHotEncoder
from scipy import stats




#START

st.title("Data exploration of the [SHARE study](https://share-eric.eu)")


st.text("")
st.text("")
st.text("") 






#get file directory
st.markdown("## Working directory")
st.markdown("#### Enter your working directory")
cwd = os.path.dirname(os.path.realpath(__file__))
st.write("Current directory:", cwd)
use_cwd = st.checkbox('Use current working directory')
if use_cwd:
    full_path = cwd + "/"
else:
    full_path = st.text_input("Other (example: /Users/josephbarbier/Desktop/PROJETpython/)")
st.write("Directory chosen:", full_path)
st.text("")
st.markdown("***If you obtain the following error, your working directory is probably wrong. Verify that you did not change any file or folder name before using the app.***")
st.code("FileNotFoundError: [Errno 2] No such file or directory")


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
st.sidebar.markdown("Contact: joseph.barbierdarnal@gmail.com")







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
path = f"{full_path}wave{str(wave_chosen)}questionnaire.pdf"
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

#clean variable and save the dataset for the end
for var in list_var:
    data[var] = qual_to_quant(data, var)
df_to_return = data.to_csv().encode('utf-8') #see at the end

#save shape    
row, col = data.shape

#print shape of the df
st.write(f"Sample size n = {row} \n Number of cols p = {col}")

#print head of the df
st.dataframe(data.head(7))



st.text("")
st.text("")




st.markdown("***Each modality percentage is calculated ignoring NAs in order to make 100% in total***")
st.markdown("***Outliers from quantitative variables have been transform to NA (not the case for the download button below)***")

#SHOW BASIC INFORMATION OF EACH VARIABLE

var_to_describe = list_var[:-2] #remove mergeid and country

#Init 2 columns
col1, col2 = st.columns(2, gap="small") 
col1.header("Statistics")
col2.header("Distribution")

x = 0
for var in var_to_describe:
    
    display = st.checkbox(var)
    
    if display:
        #count the NA percentage
        tot_na = data[var].isna().sum()
        na_percent = round(tot_na/len(data)*100,2)
        
        with col1:
            
            #make some space
            st.text("")
            st.text("")
            st.text("")
            
            #test if its the first iteration
            if x != 0:
                #make some space
                st.text("")
                st.text("")
                st.text("")
                st.text("")
                st.text("")
                st.text("")
                st.text("")
                st.text("")
                st.text("")
                st.text("")
                st.text("")
                st.text("")
                st.text("")
            x += 1
            
            #print NA percentage
            st.write(var, " has ", na_percent, "% of missing values. ")
        
            #compute stats
            if data[var].isna().sum() == len(data):
                clean_and_stat(data, var, full_na=True)
            else:
                clean_and_stat(data, var)
            
        with col2:
            if data[var].isna().sum() == len(data):
                st.text("")
                st.text("")
                st.text("")
                st.text("")
                st.write("Plot impossible (reason: only has missing values)")
                st.text("")
                st.text("")
                st.text("")
                st.text("")
            else:
                st.text("")
                st.text("")
                graph(data, var)
                st.text("")
    

        
st.text("")
st.text("")
st.text("")        







  



#MODELLING

#some comments
st.markdown("## Modelling")
st.markdown("- **Since SHARE data contains lots of missing values, we can't use the model we want for the analysis. There are 2 main solutions: NAs imputation or use modelling tools that allow the presence of missing values. We choose the second solution. According to the [scikit-learn documentation](https://scikit-learn.org/stable/modules/impute.html#estimators-that-handle-nan-values), there are several estimators that matches our criteria.**")
st.markdown("- **When the user wants to predict a quantitative variable, then the estimator *Histogram-based Gradient Boosting Regression Tree* will be used. For qualitative variables, the estimator will be *Histogram-based Gradient Boosting Classification Tree*.**")
st.markdown("- **Other important informations: all observations containing NAs in the variable that wille be predicted are dropped and all qualitative variables are encoded using one hot encoder.**")

#choose the parameters to be included in the analysis
predicted = st.selectbox("Choose the variable that will be predicted", list_var[:-2])
predictors = st.multiselect("Choose the predictors", list_var[:-2], default=list_var[1])
   
#if the user wants to predict a quantitative variable
if data[predicted].dtype in ["int64", "float64"]:
    modelling_quant(data, predicted, predictors)

#if the user wants to predict a qualitative variable
else:
    modelling_qual(data, predicted, predictors)
        
        
        
st.text("")
st.text("")
st.text("") 







#DOWNLOAD DATASET
st.markdown("## Get the dataset")
st.markdown("***By clicking on the button below, you can download the selected data in csv format.***")       
st.download_button(label="Dowload the dataset",
                   data=df_to_return,
                   file_name = "my_share_data.csv")











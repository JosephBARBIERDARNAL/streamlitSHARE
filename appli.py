#import basic packages
import streamlit as st
import re
import os
import time
import numpy as np
import pandas as pd
import PyPDF2
import matplotlib.pyplot as plt

#import our functions
from ipynb.fs.full.remove_mc2 import *
from ipynb.fs.full.variable_name import *
from ipynb.fs.full.cleaning2 import *
from ipynb.fs.full.regex2 import *
from ipynb.fs.full.univariate import *
from ipynb.fs.full.modelling2 import *
from ipynb.fs.full.imputation import *
from ipynb.fs.full.outliers import *

#import function for the modelling part
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import IterativeImputer
from sklearn.linear_model import BayesianRidge
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from scipy import stats









#DONE
#TITLE

st.title("Data exploration of the [SHARE study](https://share-eric.eu)")

st.text("")
st.text("")
st.text("") 











#DONE
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










#DONE
#GET WORKING DIRECTORY

st.markdown("## Working directory")
st.markdown("#### Enter your working directory")

#find current directory
cwd = os.path.dirname(os.path.realpath(__file__))
st.write("Current directory:", cwd)

#give the possibility to use the current working directory
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


















#DONE
#CHOOSE A WAVE

#create a list of the full wave names with their publication year
years = ["2004", "2006/7", "2008/9", "2011", "2013", "2015", "2017", "2019/20"]
waves = ["wave "+str(i)+"  (published in "+year+")" for i,year in zip(range(1,9), years)]

#information about waves
st.markdown("## Select a wave")
st.markdown("**The SHARE database is separated into 8 different waves of questionnaires spread over time. Each wave contains *more or less* the same variables, which allows analysis of longitudinal data. However, you only have here the possibility to select one single wave. You can still download mutliple datasets from different waves and merge them in your own since the csv file returned contains the mergeid feature.**")

#scrolling bar
wave = st.selectbox("Choose the wave you want to get the data from", waves)

#output the wave choosen
selected_wave = re.search(r'\d+', wave) #select the first digit of "wave"
wave_chosen = int(selected_wave.group()) #convert it to an integer
st.write(f"You have selected the {th(wave_chosen)} wave.") #output the wave chosen

st.text("")
st.text("")
st.text("")    
    
    
    
    
    
    
    
    

    
    
#DONE
#SELECTION OF THE VARIABLES

#information about variables
st.markdown("## Select variables")
st.markdown("***It is recommended that variables with the following structure: 2 letters, 3 numbers, and 1 underscore (e.g., br001_, ex005_, dn018_, or ph013_) be chosen because they are the best documented and have the fewest missing values. In addition, the fact that we use regular expressions (regex) to find the corresponding name makes these variables easier to interpret for a user not familiar with SHARE data. If you want a specific variable, use the [documentation](https://share-eric.eu/data/data-documentation).***")
st.markdown("***Also, variables beginning with 'ch' refer to the children of the respondents, not to the individual. Because some people have many children, there are a significant number of variables beginning with 'ch' regardless of their interest. The associated results, however, remain corresponding.***")

#scrolling bar with multiple choices
variables = st.multiselect(f"Select variables from the choosen wave (max is 10)",
                           get_all_variables(path=full_path, wave=wave_chosen),
                           max_selections=10)

#output the choosen variables
list_var = list(variables)
st.markdown("##### *You have selected the following variables:*")

#path where to find the documentation of each wave
path = f"{full_path}wave{str(wave_chosen)}questionnaire copy.pdf"
docu = extract_text_from_pdf(pdf_file=path)

#add a loader
with st.spinner("Loading variables..."):

    #use different function to get the description of the variables chosen depending on the wave
    clean_names = []
    for i,var in zip(range(len(list_var)), list_var):
        if wave_chosen in [1, 2]:
            docu = remove_selected(docu)
            clean_names.append(get_description_12(var.upper(), text_to_scrap=docu))
        if wave_chosen in [4,5,6,7,8]:
            clean_names.append(get_description_45678(var.upper(), text_to_scrap=docu))
        if wave_chosen in [3]:
            clean_names.append(get_description_3(var.upper(), text_to_scrap=docu))
        
        #print the variables chosen and their full name
        #add an exception with this variable since it has no documentation
        if var == "dn042_":
            st.write(var + ": "+"Gender")
            time.sleep(0.1)
        else:
            st.write(var + ": "+change_case(clean_names[i], wave_chosen))
            time.sleep(0.1)

#loader end if the user has chosen variables
if len(list_var)>0:
    st.success("Variables loaded!")    

st.text("")
st.text("")
st.text("")        











#DONE
#OVERVIEW OF THE DATA CHOSEN

#title
st.markdown("## Quick overview of the data")

#add the mergeid and the country
list_var.extend(["mergeid","country"])
clean_names.extend(["mergeid","country"])

#transform the list into a df
data = list_to_df(wave=wave_chosen, variables=list_var, path=full_path)

#save shape 
row, col = data.shape

#print shape of the df
st.write(f"Sample size n = {row}")
st.write(f"Number of cols p = {col}")

#clean variables and convert their type
for var in list_var:
    data[var] = qual_to_quant(data, var)

#save the dataset for the end if the user has selected variables
if len(list_var) > 2:
    df_to_return = data.to_csv().encode('utf-8') #see at the end

#print head of the df
st.dataframe(data.head(7))

st.text("")
st.text("")
st.text("")














#OUTLIERS

#information about the section
st.markdown("## Outliers")
st.markdown("- This section aim is to manage outliers from the selected variables.")
st.markdown("- We propose several methods: z-score, Median absolute deviation...")

manage_outliers = st.checkbox("Keep the current dataset")
st.text("")
st.text("")

if manage_outliers:
    st.write("All observations conserved")
else:
    detect_methods = ["Z-score", "Median absolute deviation"]
    method_selected = st.selectbox("Detection method", detect_methods)
    
    #choose between keeping (in Nan) or removing outliers
    st.text("")
    st.write("What to do with outliers?")
    keep_nan = st.checkbox("Keep outliers (Nan) (if not, remove them from the dataset)")
    
    #title
    st.text("")
    st.text("")
    st.markdown("#### Threshold to be used for outlier detection")
    
    #Method 1
    #manage outliers using z-scores
    if method_selected == "Z-score":
        
        #threshold used
        z = st.slider(label="The higher the value, the least restrictive for outliers",
                      min_value=0.1,
                      max_value=float(10),
                      value=float(4),
                      step=0.1)
        
        #remove (or transform to Nan) outliers and change data
        data, tot_outliers = outliers_zscore(data, list_var, z, keep_nan=keep_nan)
        
    #Method 2
    #manage outliers using m-scores
    elif method_selected == "Median absolute deviation":
        
        #threshold used
        m = st.slider(label="The higher the value, the least restrictive for outliers",
                      min_value=0.1,
                      max_value=float(10),
                      value=float(4),
                      step=0.1)
        
        #remove (or transform to Nan) outliers and change data
        data, tot_outliers = outliers_mscore(data, list_var, m, keep_nan=keep_nan)
    
    #loader end if the user has chosen variables
    if len(list_var)>2:
        st.write(f"Number of outliers detected: {tot_outliers}")
        st.success("Outliers managed!")
        
st.text("")
st.text("")
st.text("")















#IMPUTATION

#section title
st.markdown("## Imputation")

#print the percentage of missing values 
nan = count_na(data, list_var)
st.dataframe(nan, width=200)

#check if the user wants to imput nan or not
manage_nan = st.checkbox("Don't imput missing values")

#front
st.markdown("- This section aim is to imput (replace) missing values")
st.markdown("- We propose several methods: Mean, Median, Multivariate imputation...")

st.text("")
st.text("")

#add a loader
with st.spinner("Loading..."):

    if manage_nan:
        st.write("Current dataset conserved")
    else:
        
        #select the imputation method wanted
        imputation_methods = ["Univariate imputation (mean, median or mode)",
                              "Multivariate imputation",
                              "KNN imputation"]
        imputation_method = st.selectbox("Imputation method to use", imputation_methods)
        
        #imput value using univariate methods
        if imputation_method=="Univariate imputation (mean, median or mode)":
            
            #imputation method for quantitative variable
            imput_methods_quant = ["mean", "median", "most_frequent"]
            strategy_quant = st.selectbox("Imputation method for quantitative variables", imput_methods_quant)
            
            #imputation method for qualitative variable
            imput_methods_qual = ["most_frequent"]
            strategy_qual = st.selectbox("Imputation method for qualitative variables", imput_methods_qual)
            
            for var in list_var[:-2]:
                
                time.sleep(0.1)
                data_imputed = data
                
                #test the variable type
                if data_imputed[var].dtype in ["int64", "float64"]:
                    data_imputed[var] = simple_imputation(data_imputed, var, strategy_quant)
                    st.write(f"{var} has been imputed!")
                    
                else:
                    data_imputed[var] = simple_imputation(data_imputed, var, strategy_qual)
                    st.write(f"{var} has been imputed!")
        
        #imputation method using multivariate methods
        elif imputation_method=="Multivariate imputation":
            
            #define a (more or less) exhaustive estimator list
            #bayesian and random forest are supposed to be the best ones
            estimators = [BayesianRidge(),
                          RandomForestRegressor(n_estimators=4,
                                                max_depth=10,
                                                bootstrap=True,
                                                max_samples=0.5,
                                                n_jobs=2),
                          Ridge(alpha=1e3),
                          KNeighborsRegressor(n_neighbors=15)]
            estimator = st.selectbox("Choose an estimator", estimators)
            
            #define the imputation order
            imputation_orders = ["Ascending", "Descending", "Roman", "Arabic", "Random"]
            imputation_order = st.selectbox("Imputation order", imputation_orders)
            imputation_order = imputation_order.lower()
            
            #remove mergeid and country from the data to imput
            data_to_imput = data[list_var[:-2]]
            
            #imput using user inputs
            data_imputed = iterate_imputer(data_to_imput,
                                   estimator=estimator,
                                   imputation_order=imputation_order)
            
            #add mergeid and country features
            data_imputed = pd.concat(data_imputed, data[list_var[-2:]])
        
        elif imputation_method=="KNN imputation":
            ###add here the KNN imputation method
            pass
            
                    
#loader end if the user has chosen variables
if len(list_var)>2:
    
    #make room
    st.text("")
    st.text("")
    
    #verify the current number of Nan in the dataset
    total_nan = 0
    for var in list_var:
        total_nan += data[var].isna().sum()
    st.write(f"Current number of Nan: {total_nan}")
    
    #success of imputing the whole dataset
    if total_nan == 0:
        st.success("Dataset fully imputed!")

st.dataframe(data_imputed.head(12))

st.text("")
st.text("")
st.text("")














#DONE
#UNIVARIATE ANALYSIS 

#front
st.markdown("## Univariate analysis")
st.markdown("Select a variable between the ones you chose")

#save the chosen variable
var_chosen = st.selectbox("Choose a variable", list_var[:-2])

#identitfy the variable "clean name" and save it for the graph
index = list_var[:-2].index(var_chosen)
clean_name = clean_names[index]
clean_name = change_case(clean_name, wave_chosen)

#plot distribution
graph(data, var_chosen, clean_name)

#print the main descriptive statistics
st.text("")
st.markdown("#### Descriptives statistics")
univariate_stats(data, var_chosen)

st.text("")
st.text("")
st.text("")




  



    
    
    


#MODELLING

#some comments
st.markdown("## Modelling")
st.markdown("- **Since SHARE data contains lots of missing values, we can't use the model we want for the analysis. There are 2 main solutions: NAs imputation or use modelling tools that allow the presence of missing values. We choose the second solution. According to the [scikit-learn documentation](https://scikit-learn.org/stable/modules/impute.html#estimators-that-handle-nan-values), there are several estimators that matches our criteria.**")
st.markdown("- **When the user wants to predict a quantitative variable, then the estimator *Histogram-based Gradient Boosting Regression Tree* will be used. For qualitative variables, the estimator will be *Histogram-based Gradient Boosting Classification Tree*.**")
st.markdown("- **Other important informations: all observations containing NAs in the variable that wille be predicted are dropped and all qualitative variables are encoded using one hot encoder.**")



try:
    #choose the parameters to be included in the analysis
    predicted = st.selectbox("Choose the variable that will be predicted", list_var[:-2])
    predictors = st.multiselect("Choose the predictors", list_var[:-2])

    #if the user wants to predict a quantitative variable
    if data[predicted].dtype in ["int64", "float64"]:
        modelling_quant(data, predicted, predictors)

    #if the user wants to predict a qualitative variable
    else:
        modelling_qual(data, predicted, predictors)
except Exception as e:
    pass #avoid displaying errors in the application 
        
        
st.text("")
st.text("")
st.text("") 







#DOWNLOAD DATASET

st.markdown("## Get the dataset")
st.markdown("***By clicking on the button below, you can download the selected data in csv format.***")       

try:
    st.download_button(label="Dowload the dataset",
                       data=df_to_return,
                       file_name = "my_share_data.csv")
except NameError:
    st.write("Choose variable before using the download button")
    st.download_button(label="Dowload the dataset",
                       data=data.to_csv().encode('utf-8'),
                       file_name = "my_share_data.csv", disabled=True)
    
    











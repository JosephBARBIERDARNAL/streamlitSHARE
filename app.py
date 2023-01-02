#packages and functions importation
import streamlit as st
#from ipynb.fs.full.get_variables import get_all_variables


#test
import pandas as pd
import os
def get_all_variables():
    
    PATH = "/Users/josephbarbier/Desktop/PROJETpython/rawdata"
    vars = set()
    
    for index, dirs, files in os.walk(PATH):
        for file in files:
            if file.endswith(".dta"):
                df = pd.read_stata(
                    os.path.join(index, file),
                    chunksize=1,
                    convert_categoricals=False,
                ).read(3)
                vars.update(df.columns.tolist())
            
    return vars

  
  
  
st.title("Get the data from the [SHARE study](https://share-eric.eu) you want in 3 easy steps")



#SIDEBAR
st.sidebar.markdown("## Menu")
st.sidebar.markdown("In this interface, you have the possibility to choose the variables you are interested in at a given wave. From these, you can then retrieve a .csv file containing these variables and the merge identifier (called 'mergeid').")

st.sidebar.markdown("## About us")
st.sidebar.markdown("French data science students from the Bordeaux School of Economics")


#MAIN
data_load_state = st.text("Loading data... (wait until the end)")

#Step 1: choose a wave
years = ["2004", "2006/7", "2008/9", "2011", "2013", "2015", "2017", "2019/20"]
st.markdown("### Step 1: select a wave")
choices_name = ["wave "+str(i)+"  (published in "+year+")" for i,year in zip(range(1,9), years)]
wave = st.selectbox("Choose the wave you want to get data from", choices_name)
st.write('You selected the', wave)

#Step 2: choose the variables
st.markdown("### Step 2: select variables")
variables = st.multiselect(f"Select variables from the choosen wave (max is 10)",
                           get_all_variables(),
                           max_selections=10)
to_print = list(variables)
st.write("You have selected the following variables:")
for var in to_print:
    st.write(var)

data_load_state.text("Data loaded!")


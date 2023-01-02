import streamlit as st
from ipynb.fs.full.get_variables import get_all_variables

st.title('Get the data from the SHARE study')

#SIDEBAR
st.sidebar.markdown("## Menu")



#MAIN
data_load_state = st.text('Loading data...')

#choose a wave
wave = st.selectbox("Choose a wave to get data from", [i for i in range(1,9)])
st.write('You selected the', wave, 'th wave')

#choose the variables wanted
variables = st.multiselect(f"Select variables from wave {wave} (max is 10)",
                           get_all_variables(),
                           max_selections=10)
st.write('You selected the following variables:', variables[1])

data_load_state.text(None)


import streamlit as st
import pandas as pd
import numpy as np

st.title('Hello, World!')
st.write('Good to see you!', 'Lets get started, or not, your choice.\n'
            ' We will load 1000 rows from Uber dataset for pickups and drop-offs in New York City.')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Let people know data is being loaded
data_load_state = st.text('Loading...')
# Start by loading 1000 rows
data = load_data(1000)
# Notify people that the data was successfully loaded
data_load_state.text("Loading done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('No. pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

st.subheader('Map of all pickups')
st.map(data)

hour_to_filter = st.slider('Hour',0,23,17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader('Map of pickups at %s:00' % hour_to_filter)
st.map(filtered_data)
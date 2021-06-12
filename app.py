import streamlit as st

import numpy as np
import pandas as pd

import requests

st.markdown('''# MEET an ALIEN in the US! 
## Choose your State and season you're interested in''')

#''' Choosing your State'''

@st.cache
def get_select_box_data():
    print('get_select_box_data called')

    df = pd.DataFrame({
    'State': ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
                  'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
                  'Illinois', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland',
                  'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
                  'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
                  'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
                  'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
                  'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia',
                  'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'],
    'state_abbreviation': ['al', 'ak', 'az', 'ar', 'ca', 'co',
                           'ct', 'de', 'fl', 'ga', 'hi', ' id',
                           'il', 'ia', 'ks', 'ky', 'la', 'me', 'md',
                           'ma', 'mi', 'mn', 'ms', 'mo',
                           'mt', 'ne', 'nh', 'nh', 'nj',
                           'nm', 'ny', 'nc', 'nd', 'oh',
                           'ok', 'or', 'pa', 'rh', 'sc',
                           'sd', 'tn', 'tx', 'ut', 'vt', 'va',
                           'wa', 'wv', 'wi', 'wy']
})
    return df

df = get_select_box_data()

option = st.selectbox('Select a State', df['State'])

for index, row in df.iterrows():
    if row['State'] == option:
        state_brev = df.iloc[index, 1]

filtered_df = df[df['State'] == option]

#st.write(filtered_df)

#''' Choosing your Season''''

season = st.radio('Select a Season', ('winter', 'spring', 'summer', 'autumn'))

st.write(season)


#url = 'https://...../predict'

params = dict(
    state = state_brev,
    season = season
)

response = requests.get(url, params=params)

prediction = response.json()

pred = prediction['prediction']

pred

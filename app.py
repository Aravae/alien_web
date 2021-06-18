import requests
import folium
from folium.plugins import HeatMap
import numpy as np
import pandas as pd
import streamlit as st
from math import floor
from streamlit_folium import folium_static

PREDICTION_URL = 'https://alienfuturepredict-ytkptzsdgq-ew.a.run.app/predict'
BUCKET_NAME = 'ufo_sightings'
BUCKET_TRAIN_DATA_PATH = 'data/scrubbed.csv'
Testing = 'test'

st.set_page_config(
    page_title="Meet an Alien",
    page_icon="👽",
    layout="centered",  # wide
    initial_sidebar_state="auto")  # collapsed

header = st.beta_container()
user_input = st.beta_container()
report_maps = st.beta_container()

CSS = """
h1 {
    color: #39FF14;
}
body {
    background-image: url(https://avatars1.githubusercontent.com/u/9978111?v=4);
    background-size: cover;
}
.sightings-prediction {
    text-align: center;
}

.sightings-prediction h1 {
    margin-top: 0px;
    padding-top: 0px;
}
"""

st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)


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


@st.cache(suppress_st_warning=True)
def get_reports_df():
    df = pd.read_csv(f"gs://{BUCKET_NAME}/{BUCKET_TRAIN_DATA_PATH}")
    df = df.rename(columns={'longitude ': 'longitude'})
    df = df.apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna()

    center_location = 29.8830556, -97.9411111
    m = folium.Map(location=center_location, control_scale=True, zoom_start=3)

    for lat, lng in zip(df['latitude'], df['longitude']):
        print(lat, lng)
        folium.CircleMarker(locationn=(lat, lng)).add_to(m)

    folium_static(m)


with header:
    st.title("Meet an Alien")
    st.markdown("""

    Welcome to MaA. This web application displays current UFO sighting reports and predicts future reports so you can have your cameras ready and stop taking those blurry pictures and videos.
    
    **Note:** To make a prediction, select a State and we will predict the number of sightings you can expect for the next season (Spring, summer, etc.)
    
    """)

with report_maps:
    get_reports_df()



with user_input:
    st.sidebar.header('Sightings prediction')

    states_df = get_select_box_data()

    option = st.sidebar.selectbox('Select a State', states_df['State'])

    if st.sidebar.button('Predict sightings'):
        state = states_df.loc[states_df['State'] == option, 'state_abbreviation'].iloc[0]

        params = dict(state=state, season='winter')
        response = requests.get(PREDICTION_URL, params=params)

        prediction = response.json()

        sightings = floor(prediction['prediction'])
        if sightings == 1:
            word = 'sighting'
        else:
            word = 'sightings'

        HTML = f"""
        <div class="sightings-prediction">
            <p>Next season you can expect</p>
            <h1><strong>{sightings}</strong> {word}</h1>
            <p>in {option}</p>
        </div>
        """
        st.sidebar.write(HTML, unsafe_allow_html=True)

import folium
import requests
import pandas as pd
import streamlit as st
from math import floor
from streamlit_folium import folium_static

PREDICTION_URL = 'https://alienfuturepredict-ytkptzsdgq-ew.a.run.app/predict'
BUCKET_NAME = 'ufo_sightings'
BUCKET_TRAIN_DATA_PATH = 'data/scrubbed.csv'
BUCKET_ACTUAL_TARGET = 'data/final_df_2020_summer.csv'

st.set_page_config(
    page_title="Meet an Alien",
    page_icon="👽",
    layout="centered",  # wide
    initial_sidebar_state="auto")  # collapsed

header = st.beta_container()
user_input = st.beta_container()
report_maps = st.beta_container()
performance = st.beta_container()

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

    df = df.head(2000)

    df = df.loc[df['country'] == 'us']

    df = df.rename(columns={'longitude ': 'longitude'})
    df = df[['latitude', 'longitude']].apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna()

    return df


@st.cache
def get_actual_target(chosen_state=None):
    if chosen_state:
        df = pd.read_csv(f"gs://{BUCKET_NAME}/{BUCKET_ACTUAL_TARGET}")
        state_data = df.loc[df['state'] == chosen_state]

        return state_data['sightings_days']


with header:
    st.title("Meet an Alien")
    st.markdown("""

    Welcome to MaA. This web application displays current UFO sighting reports and predicts future reports so you can have your cameras ready and stop taking those blurry pictures and videos.
    
    **Note:** To make a prediction, select a State and we will predict the number of sightings you can expect for the next season (Spring, summer, etc.)
    
    """)

with user_input:
    st.sidebar.header('Sightings prediction')

    states_df = get_select_box_data()

    option = st.sidebar.selectbox('Select a State', states_df['State'])

    if st.sidebar.button('Predict sightings'):
        state = states_df.loc[states_df['State'] == option, 'state_abbreviation'].iloc[0]

        params = dict(state=state, season='summer')
        response = requests.get(PREDICTION_URL, params=params)

        prediction = response.json()

        sightings = floor(prediction['prediction']) if prediction['prediction'] > 1 else 0
        if sightings == 1:
            word = 'sighting'
        else:
            word = 'sightings'

        HTML = f"""
        <div class="sightings-prediction">
            <p>Next Autumn you can expect</p>
            <h1><strong>{sightings}</strong> {word}</h1>
            <p>in {option}</p>
        </div>
        """
        st.sidebar.write(HTML, unsafe_allow_html=True)

        actual = get_actual_target(state)


with report_maps:
    st.title('Reports of UFO sightings in the past 10 years')
    coords = get_reports_df()

    center_location = 29.8830556, -97.9411111
    m = folium.Map(location=center_location, control_scale=True, zoom_start=3)

    for lat, lng in zip(coords['latitude'], coords['longitude']):
        folium.CircleMarker(location=(lat, lng), radius=2, color='green').add_to(m)

    folium_static(m)


@st.cache
def get_histo():
    df = pd.DataFrame(
        [actual, sightings],
        columns=['a']
    )

    return np.histogram(
        df.a, bins=2)[0]


hist_values = get_histo()

st.bar_chart(hist_values)

import pickle
import streamlit as st
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


# Function to safely fetch movie data (poster fetching removed)
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('https://', adapter)

        response = session.get(url, timeout=5)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        st.warning("Connection to TMDB timed out. Please try again later.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f" Error fetching movie details: {e}")
        return None


# Recommendation logic (only names)
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []

    for i in distances[1:6]:
        movie_name = movies.iloc[i[0]].title
        recommended_movie_names.append(movie_name)

    return recommended_movie_names


# Streamlit UI
st.header('Movie Recommender System')

movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names = recommend(selected_movie)

    st.subheader("Recommended Movies:")
    for name in recommended_movie_names:
        st.write(f"- {name}")

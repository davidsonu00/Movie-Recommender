import streamlit as st
import pandas as pd
import pickle, bz2
import os

# -------------------------------
# Load compressed data
# -------------------------------
with bz2.BZ2File("movies.pbz2", "rb") as f:
    movies = pickle.load(f)

with bz2.BZ2File("similarity.pbz2", "rb") as f:
    similarity = pickle.load(f)

# -------------------------------
# Load poster CSV
# -------------------------------
posters_df = pd.read_csv("movie_posters.csv")

FALLBACK_POSTER = "sorry_poster.png"  # keep this in repo

def fetch_poster(movie_title):
    result = posters_df[posters_df['title'].str.lower() == movie_title.lower()]
    if not result.empty and pd.notna(result.iloc[0]['poster']):
        return result.iloc[0]['poster']
    elif os.path.exists(FALLBACK_POSTER):
        return FALLBACK_POSTER
    else:
        return "https://via.placeholder.com/300x450.png?text=Poster+Not+Available"

# -------------------------------
# Recommendation function
# -------------------------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),
                       reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in distances:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_movies_posters.append(fetch_poster(movie_title))

    return recommended_movies, recommended_movies_posters

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")
st.title("🎬 Movie Recommender System 🍿")

option = st.selectbox("Select a movie:", movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(option)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            st.markdown(f"**{names[i]}**")

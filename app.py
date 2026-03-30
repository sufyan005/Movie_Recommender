import streamlit as st
import pickle
import pandas as pd
import scipy.sparse
import requests
import concurrent.futures
import os
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

# 0. API Key Setup
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

# 1. Config & Data Loading
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

@st.cache_resource
def load_data():
    movies = pd.read_parquet("movies.parquet")
    indices      = pickle.load(open("indices.pkl",      "rb"))
    tfidf_matrix = pickle.load(open("tfidf_matrix.pkl", "rb"))
    return movies, indices, tfidf_matrix

movies, indices, tfidf_matrix = load_data()

# 2. poster fetching with caching
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except Exception:
        pass
    return "https://placehold.co/500x750?text=No+Poster+Available"

def recommend(title, n=10):
    key = title.lower()
    if key not in indices:
        return None
    idx = indices[key]
    sim_scores = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()
    top_idx = sim_scores.argsort()[::-1][1:n+1]
    return top_idx

# 3. UI Elements
st.title("🎬 Movie Recommender")

selected = st.selectbox("Choose a movie", sorted(movies["title"].values))
n_recs   = st.slider("Number of recommendations", 5, 20, 10, step=5)

if st.button("Recommend"):
    with st.spinner("Finding similar movies..."):
        results = recommend(selected, n=n_recs)

        if results is None:
            st.error("Movie not found in database.")
        else:
            # --- Header for Selected Movie ---
            key = selected.lower()
            selected_idx = indices[key]
            if hasattr(selected_idx, "__iter__"):
                selected_idx = selected_idx[0]
            
            selected_id = movies.iloc[selected_idx]['movie_id']
            
            col_h1, col_h2 = st.columns([1, 5])
            with col_h1:
                st.image(fetch_poster(selected_id), width=150)
            with col_h2:
                st.subheader(f"Because you liked *{selected}*")
                st.write(f"Showing {n_recs} similar titles:")

            st.divider()

            # --- Parallel Poster Fetch ---
            movie_data_list = [movies.iloc[int(idx)] for idx in results]

            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                poster_urls = list(
                    executor.map(lambda x: fetch_poster(x['movie_id']), movie_data_list)
                )

            # --- Display Grid ---
            num_cols = 5
            # Create rows manually for cleaner alignment
            for i in range(0, len(movie_data_list), num_cols):
                cols = st.columns(num_cols)
                for j in range(num_cols):
                    if i + j < len(movie_data_list):
                        movie_data = movie_data_list[i + j]
                        with cols[j]:
                            st.image(poster_urls[i + j], use_container_width=True)
                            st.caption(f"**{movie_data['title']}**")

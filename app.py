import os
import pickle
import requests
import streamlit as st

# -------------------- Helper Functions --------------------

def fetch_poster(movie_id):
    """
    Fetch poster URL for a given TMDB movie ID.
    Falls back to placeholder if none or on error.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer YOUR_TMDB_BEARER_TOKEN"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except requests.RequestException:
        pass
    # fallback placeholder
    return "https://via.placeholder.com/500x750?text=No+Poster"


def recommend(movie_title, movies_df, similarity_matrix):
    """
    Given a movie title, return top-5 recommended titles and poster URLs.
    """
    idx = movies_df[movies_df['title'] == movie_title].index[0]
    distances = sorted(
        enumerate(similarity_matrix[idx]),
        key=lambda x: x[1],
        reverse=True
    )
    names, posters = [], []
    for i, _ in distances[1:6]:  # skip the first (same movie)
        m_id = movies_df.iloc[i]['movie_id']
        names.append(movies_df.iloc[i]['title'])
        posters.append(fetch_poster(m_id))
    return names, posters


# -------------------- Data Loading --------------------

@st.cache_data
def load_data():
    """
    Load movie list and similarity matrix from disk once.
    """
    base = os.path.dirname(os.path.abspath(__file__))
    movies_path = os.path.join(base, 'artifacts', 'movie_list.pkl')
    sim_path    = os.path.join(base, 'artifacts', 'similarity.pkl')
    movies_df   = pickle.load(open(movies_path, 'rb'))
    similarity  = pickle.load(open(sim_path, 'rb'))
    return movies_df, similarity

movies, similarity = load_data()

# -------------------- Streamlit UI --------------------

st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommendation System")

# Selection widget
movie_list = movies['title'].tolist()
selected = st.selectbox("Choose a movie:", movie_list)

# Initialize recommendations on first load
if 'rec_names' not in st.session_state:
    st.session_state.rec_names, st.session_state.rec_posters = recommend(selected, movies, similarity)

# Button to refresh recommendations
if st.button('Show recommendation'):
    st.session_state.rec_names, st.session_state.rec_posters = recommend(selected, movies, similarity)

# Render recommendations in columns
cols = st.columns(5)
for idx, col in enumerate(cols):
    with col:
        st.caption(st.session_state.rec_names[idx])
        st.image(st.session_state.rec_posters[idx], use_column_width=True)

# Footer
st.markdown("---")
st.write("*Powered by TMDB & Streamlit*")

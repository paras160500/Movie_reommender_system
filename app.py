import streamlit as st 
import pickle
import pandas as pd 
import requests
from sklearn.metrics.pairwise import cosine_similarity

similarity = pickle.load(open("similarity.pkl" , "rb"))



def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/"+str(movie_id)+"?api_key=b22bba233223e976917f1cab6a1e01b8&language=en-US"
    # print(url , movie_id)
    data = requests.get(url)
    data = data.json()
    # print("---------")
    # print(data['poster_path'])
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

movies_list = pickle.load(open('movies.pkl' , 'rb'))


st.title("Movie Recommender System")
selected_movie_name = st.selectbox('Select your Pictures' , movies_list['title'])

def recommended(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    m_list = sorted(list(enumerate(distances)) , reverse=True , key=lambda x : x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in m_list:
        movie_id = movies_list.iloc[i[0]].id
        recommended_movies.append(movies_list.iloc[i[0]].title)
        #recommended_movies_poster.append(fetch_poster(movie_id))
        #Fetch Poster From API
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies , recommended_movies_poster


if st.button("Recommend"):

    recommended_movie_names, recommended_movie_posters = recommended(selected_movie_name)

    # Page styling: dark background with subtle default border and neon on hover
    st.markdown("""
        <style>
        body {
            background-color: #000;
            color: #fff;
        }

        .movie-card {
            position: relative;
            background-color: #111;
            border-radius: 12px;
            padding: 10px;
            text-align: center;
            border: 1px solid;
            border-image: linear-gradient(90deg, rgba(255,255,255,0.05), rgba(255,255,255,0.1), rgba(255,255,255,0.05)) 1;
            animation: subtleBorder 4s ease-in-out infinite;
            transition: transform 0.3s ease-in-out;
        }

        .movie-card:hover {
            transform: scale(1.05);
            animation: neonBorder 2s linear infinite;
            border-image: linear-gradient(90deg, #00ffff, #ff00ff, #ffff00, #00ff00) 1;
        }

        .movie-title {
            font-size: 16px;
            color: #fff;
            margin-top: 10px;
            font-weight: 600;
            font-family: 'Segoe UI', sans-serif;
        }

        .movie-poster {
            width: 100%;
            border-radius: 8px;
            box-shadow: 0 0 6px rgba(255, 255, 255, 0.05);
        }

        @keyframes subtleBorder {
            0% { border-image: linear-gradient(90deg, rgba(255,255,255,0.05), rgba(255,255,255,0.1), rgba(255,255,255,0.05)) 1; }
            50% { border-image: linear-gradient(90deg, rgba(255,255,255,0.1), rgba(255,255,255,0.2), rgba(255,255,255,0.1)) 1; }
            100% { border-image: linear-gradient(90deg, rgba(255,255,255,0.05), rgba(255,255,255,0.1), rgba(255,255,255,0.05)) 1; }
        }

        @keyframes neonBorder {
            0% { border-image: linear-gradient(90deg, #00ffff, #ff00ff, #ffff00, #00ff00) 1; }
            25% { border-image: linear-gradient(90deg, #ff00ff, #ffff00, #00ff00, #00ffff) 1; }
            50% { border-image: linear-gradient(90deg, #ffff00, #00ff00, #00ffff, #ff00ff) 1; }
            75% { border-image: linear-gradient(90deg, #00ff00, #00ffff, #ff00ff, #ffff00) 1; }
            100% { border-image: linear-gradient(90deg, #00ffff, #ff00ff, #ffff00, #00ff00) 1; }
        }
        </style>
    """, unsafe_allow_html=True)

    # Create 5 columns
    cols = st.columns(5)

    # Render each movie card
    for idx, col in enumerate(cols):
        with col:
            st.markdown(f"""
                <div class="movie-card">
                    <img src="{recommended_movie_posters[idx]}" class="movie-poster"/>
                    <div class="movie-title">{recommended_movie_names[idx]}</div>
                </div>
            """, unsafe_allow_html=True)

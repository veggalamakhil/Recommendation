import streamlit as st
import pickle
import requests
import streamlit.components.v1 as components

default_image_url = "https://via.placeholder.com/500x750?text=No+Image"

def fetch_poster(movie_id):
    try:
        url = "https://api.themoviedb.org/3/movie/{}?api_key=00be465eb5784103a6fa6c7da55e63dc&language=en-US".format(movie_id)
        data = requests.get(url, timeout=5)
        data.raise_for_status()
        data = data.json()
        poster_path = data.get('poster_path', '')
        if not poster_path:
            return default_image_url
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except Exception as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        return default_image_url


movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list=movies['title'].values

st.header("Movie Recommender System")

try:
    imageUrls = [
        fetch_poster(1632),
        fetch_poster(299536),
        fetch_poster(17455),
        fetch_poster(2830),
        fetch_poster(429422),
        fetch_poster(9722),
        fetch_poster(13972),
        fetch_poster(240),
        fetch_poster(155),
        fetch_poster(598),
        fetch_poster(914),
        fetch_poster(255709),
        fetch_poster(572154)
    ]
except:
    imageUrls = [default_image_url] * 13


selectvalue=st.selectbox("Select movie from dropdown", movies_list)

def recommend(movie):
    index=movies[movies['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    recommend_movie=[]
    recommend_poster=[]
    for i in distance[1:6]:
        movies_id=movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
    return recommend_movie, recommend_poster



if st.button("Show Recommend"):
    movie_name, movie_poster = recommend(selectvalue)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])

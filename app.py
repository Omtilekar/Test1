import pickle
import requests
import pandas as pd
import streamlit as st

# st.markdown(
#     """
#     <style>
#     .selected_movie_name select {
#         font-size: 500px; /* Adjust the font size as needed */
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center;'>Movies Recommender System</h1>", unsafe_allow_html=True)

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=d50bcc1e4d87cd26fd6df713f7f3a97b&language=en-US'.format(movie_id))
    data=response.json()


    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []

    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        #fetch poster from api
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster

movies_dict=pickle.load(open('movies_dict.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))
movies=pd.DataFrame(movies_dict)
#st.title("Movie Recommender System")


selected_movie_name = st.selectbox(
    'Search Movie here',
    movies['title'])

if st.button('Recommend'):
   recommended_movies, recommended_movies_poster=recommend(selected_movie_name)
   col1, col2, col3 ,col4 ,col5= st.columns(5)

   with col1:
       st.text(recommended_movies[0])
       st.image(recommended_movies_poster[0])

   with col2:
       st.text(recommended_movies[1])
       st.image(recommended_movies_poster[1])
   with col3:
       st.text(recommended_movies[2])
       st.image(recommended_movies_poster[2])
   with col4:
       st.text(recommended_movies[3])
       st.image(recommended_movies_poster[3])
   with col5:
       st.text(recommended_movies[4])
       st.image(recommended_movies_poster[4])

   st.markdown("<h1 style='text-align: center;'>Thank You For Visiting!</h1>", unsafe_allow_html=True)

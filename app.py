from flask import Flask, render_template, request, redirect, url_for
import csv
import random

from Recommender import Recommender

import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)

@app.route('/')
def home():
    # Generate a random list of movies to display
    movies = get_random_movies()
    return render_template('home.html', movies=movies)

@app.route('/dropdown')
def dropdown():
    rows = []
    with open('movies1.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            rows.append(row)
    return render_template('index.html', rows=rows)

@app.route('/selected_row', methods=['POST'])
def selected_row():
    selected_row = request.form.get('dropdown')
    # do something with the selected_row variable
    display(selected_row)
    return redirect(url_for('recommendations', selected_row=selected_row))

@app.route('/lucky')
def feelingLucky():
    movies = []
    with open('movies1.csv', 'r') as file:
        for line in file:
            movie = line.strip()
            movies.append(movie)
    random_movie = random.choice(movies)
    return render_template('lucky.html', movies=random_movie)

@app.route('/recommendations')
def recommendations():
    selected_row = request.args.get('selected_row')
    # get the recommended movies based on the selected_row
    # recommended_movies = get_recommended_movies(selected_row)
    recommended_movies = display(selected_row)
    # return render_template('result.html', selected_row=selected_row)
    return render_template('result.html', selected_row=selected_row, recommended_movies=recommended_movies)

@app.route('/about')
def about():
    return render_template('about.html')

def get_random_movies():
    # get a random list of movies to display on the home page
    movies = []
    with open('movies1.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader) # skip header row
        for row in reader:
            movies.append(row[0])
    return random.sample(movies, 4) # return 5 random movies


def display(selected_row):
    recommender = Recommender()
    recommended_movies = recommender.recommend_on_movie(selected_row)
    return recommended_movies

if __name__ == '__main__':
    app.run(debug=True)

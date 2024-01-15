from flask import Flask, jsonify, request
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from flask_marshmallow import Marshmallow

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'movies.db')

db = SQLAlchemy(app)
ma = Marshmallow(app)

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created successfully')

@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped successfully')

@app.route('/hello')
def hello():
    return jsonify(message='Hello, there')

@app.route('/movies', methods=['GET'])
def movies():
    movies_list = Movies.query.all()
    result = movies_schema.dump(movies_list)
    return jsonify(result)

@app.route('/movie_details/<int:id>', methods=['GET'])
def movie_details(id: int):
    movie = Movies.query.filter_by(id=id).first()
    if movie:
        result = movie_schema.dump(movie)
        return jsonify(result)
    else:
        return jsonify(message='That movies does not exist.'), 404

@app.route('/add_movie', methods=['POST'])
def add_movie():
    movie_name = request.form['movie_name']
    test = Movies.query.filter_by(movie_name=movie_name).first()
    if test:
        return jsonify(message='Movie already exists'), 409
    else:
        movie_genre = request.form['movie_genre']
        lead_actor = request.form['lead_actor']
        lead_actress = request.form['lead_actress']
        rating = float(request.form['rating'])

        new_movie = Movies(movie_name=movie_name,
                           movie_genre=movie_genre,
                           lead_actor=lead_actor,
                           lead_actress=lead_actress,
                           rating=rating)
        db.session.add(new_movie)
        db.session.commit()
        return jsonify(message='Movie inserted successfully'), 201

@app.route('/update_movie', methods=['POST'])
def update_movie():
    id = int(request.form['id'])
    movie = Movies.query.filter_by(id=id).first()
    if movie:
        movie.movie_name = request.form['movie_name']
        movie.movie_genre = request.form['movie_genre']
        movie.lead_actor = request.form['lead_actor']
        movie.lead_actress = request.form['lead_actress']
        movie.rating = float(request.form['rating'])
        db.session.commit()
        return jsonify(message='Updated successfully')
    else:
        return jsonify(message='That movie that does not exist.')

@app.route('/remove_movie/<int:id>', methods=['DELETE'])
def remove_movie(id: int):
    movie = Movies.query.filter_by(id=id).first()
    if movie:
        db.session.delete(movie)
        db.session.commit()
        return jsonify(message='Deleted successfully'), 202
    else:
        return jsonify(message='That movie does not exist.'), 404
    
@app.route('/top_rated_movies', methods=['GET'])
def top_rated_movies():
    movies_list = Movies.query.order_by(Movies.rating.desc()).all()
    result = movies_schema.dump(movies_list)
    return jsonify(result)

@app.route('/movies_by_actor/<string:lead_actor>', methods=['GET'])
def movies_by(lead_actor: str):
    movies_list = Movies.query.filter_by(lead_actor=lead_actor).all()
    result = movies_schema.dump(movies_list)
    return jsonify(result)

@app.route('/movies_by_genre/<string:movie_genre>', methods=['GET'])
def movies_by_genre(movie_genre: str):
    movies_list = Movies.query.filter_by(movie_genre=movie_genre).all()
    result = movies_schema.dump(movies_list)
    return jsonify(result)

# Defining movies class
class Movies(db.Model):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    movie_name = Column(String)
    movie_genre = Column(String)
    lead_actor = Column(String)
    lead_actress = Column(String)
    rating = Column(Float)

class MovieSchema(ma.Schema):
    class Meta:
        fields = ('id', 
                  'movie_name', 
                  'movie_genre', 
                  'lead_actor', 
                  'lead_actress', 
                  'rating')
        
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
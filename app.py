#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from datetime import datetime
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app,db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    genres = db.Column(db.String(120))
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(500))
    seeking_talent = db.Column(db.String(120))
    seeking_description = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    show = db.relationship('Show',backref='Venue',lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    address = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(500))
    seeking_venue = db.Column(db.String(120))
    seeking_description = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    show = db.relationship('Show',backref='Artist',lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
   __tablename__ = 'Show'
   id = db.Column(db.Integer, primary_key=True)
   venue_id = db.Column(db.Integer,db.ForeignKey('Venue.id'),nullable=False)
   artist_id = db.Column(db.Integer,db.ForeignKey('Artist.id'),nullable=False)
   start_time = db.Column(db.DateTime,nullable=False,default = datetime.utcnow)



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  database_data =[]
  for loc in db.session.query(Venue.city,Venue.state).distinct():
    d = {"city":loc[0], "state": loc[1],"venues":[]}
    for y in Venue.query.filter_by(city=loc[0],state=loc[1]):
        upcoming_shows = Show.query.filter_by(venue_id = y.id).filter(Show.start_time > datetime.now()).count()
        venue_details = { "id": y.id , "name": y.name , "num_upcoming_shows":upcoming_shows}
        d["venues"].append(venue_details)
    database_data.append(d)
  
  print(database_data)
        
  
  return render_template('pages/venues.html', areas=database_data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }

  search_item = request.form.get('search_term')
  filtered_venue= Venue.query.filter(Venue.name.ilike(search_item))
  c = filtered_venue.count()

  database_response={"count":c ,"data":[]}

  for y in filtered_venue:
      upcoming_shows = Show.query.filter_by(venue_id= y.id).filter(Show.start_time > datetime.now()).count()
      venue_data = {"id":y.id, "name": y.name, "num_upcoming_shows":upcoming_shows}
      database_response['data'].append(venue_data)
  return render_template('pages/search_venues.html', results=database_response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  a = Venue.query.filter_by(id=venue_id)[0]
  print(a.name)
  d_genres = a.genres.split(' ')
  seeking_talent = True if a.seeking_talent =='Yes' else False
  database_response = {
  "id": a.id , 
  "name":a.name , 
  "genres":d_genres , 
  "city":a.city ,
  "state": a.state ,
  "phone": a.phone,
  "website":a.website_link, 
  "facebook":a.facebook_link, 
  "seeking_venue" : seeking_talent ,
  "seeking_description": a.seeking_description, 
  "image_link": a.image_link , 
  "past_shows":[],
  "upcoming_shows":[],
  "past_shows_count":0,
  "upcoming_shows_count":0
  }
  upcoming_shows = Show.query.filter_by(venue_id= a.id).filter(Show.start_time > datetime.now())
  database_response["upcoming_shows_count"]= upcoming_shows.count()
  past_shows = Show.query.filter_by(venue_id= a.id).filter(Show.start_time < datetime.now())
  database_response["past_shows_count"]=past_shows.count()

  for up_shows in upcoming_shows:
    artist_details = Artist.query.filter_by(id=up_shows.artist_id)[0]
    show_details = {"artist_id": artist_details.id , "artist_name": artist_details.name , "artist_image_link": artist_details.image_link,
    "start_time": str(up_shows.start_time)}
    database_response['upcoming_shows'].append(show_details)
  
  for p_shows in past_shows:
    artist_details = Artist.query.filter_by(id=p_shows.venue_id)[0]
    show_details = {"artist_id": artist_details.id , "artist_name": artist_details.name , "artist_image_link": artist_details.image_link,
    "start_time": str(p_shows.start_time)}
    database_response['past_shows'].append(show_details)

  return render_template('pages/show_venue.html', venue=database_response)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  name = request.form.get('name')
  state = request.form.get('state')
  city = request.form.get('city')
  address = request.form.get('address')
  phone = request.form.get('phone')
  genres = ' '.join(request.form.getlist('genres'))
  website = request.form.get('website_link')
  image = request.form.get('image_link')
  seeking_talent = request.form.get('seeking_talent')
  seeking_description =request.form.get('seeking_description')
  facebook = request.form.get('facebook_link')
  venue = Venue(name=name,state= state , city=city, address= address, phone=phone, genres=genres,image_link = image, 
  website_link = website, seeking_talent = seeking_talent,seeking_description = seeking_description, facebook_link = facebook)
  db.session.add(venue)
  db.session.commit()
  

  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database


  database_data =[]
  for artist in Artist.query.all():
      a = {"id": artist.id, "name":artist.name}
      database_data.append(a)
  
  print(database_data)


  return render_template('pages/artists.html', artists=database_data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search_item = request.form.get('search_term')
  print(search_item)
  filtered_artist= Artist.query.filter(Artist.name.ilike(search_item))
  c = filtered_artist.count()
  print(c)
  database_response={"count":c ,"data":[]}

  for y in filtered_artist:
      upcoming_shows = Show.query.filter_by(artist_id= y.id).filter(Show.start_time > datetime.now()).count()
      artist_data = {"id":y.id, "name": y.name, "num_upcoming_shows":upcoming_shows}
      database_response['data'].append(artist_data)
  

  return render_template('pages/search_artists.html', results=database_response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  a = Artist.query.filter_by(id=artist_id)[0]
  print(a.name)
  d_genres = a.genres.split(' ')
  seeking_venue = True if a.seeking_venue =='Yes' else False
  database_response = {
  "id": a.id , 
  "name":a.name , 
  "genres":d_genres , 
  "city":a.city ,
  "state": a.state ,
  "phone": a.phone,
  "website":a.website_link, 
  "facebook":a.facebook_link, 
  "seeking_venue" : seeking_venue ,
  "seeking_description": a.seeking_description, 
  "image_link": a.image_link , 
  "past_shows":[],
  "upcoming_shows":[],
  "past_shows_count":0,
  "upcoming_shows_count":0
  }
  upcoming_shows = Show.query.filter_by(artist_id= a.id).filter(Show.start_time > datetime.now())
  database_response["upcoming_shows_count"]= upcoming_shows.count()
  past_shows = Show.query.filter_by(artist_id= a.id).filter(Show.start_time < datetime.now())
  database_response["past_shows_count"]=past_shows.count()

  for up_shows in upcoming_shows:
    venue_details = Venue.query.filter_by(id=up_shows.venue_id)[0]
    show_details = {"venue_id": venue_details.id , "venue_name": venue_details.name , "venue_image_link": venue_details.image_link,
    "start_time": str(up_shows.start_time)}
    database_response['upcoming_shows'].append(show_details)
  
  for p_shows in past_shows:
    venue_details = Venue.query.filter_by(id=p_shows.venue_id)[0]
    show_details = {"venue_id": venue_details.id , "venue_name": venue_details.name , "venue_image_link": venue_details.image_link,
    "start_time": str(p_shows.start_time)}
    database_response['past_shows'].append(show_details)

  
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=database_response)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  name = request.form.get('name')
  state = request.form.get('state')
  city = request.form.get('city')
  address = request.form.get('address')
  phone = request.form.get('phone')
  genres = ' '.join(request.form.getlist('genres'))
  website = request.form.get('website_link')
  image = request.form.get('image_link')
  seeking_venue = request.form.get('seeking_venue')
  seeking_description =request.form.get('seeking_description')
  facebook = request.form.get('facebook_link')
  artist = Artist(name=name,state= state , city=city, address= address, phone=phone, genres=genres,image_link = image, 
  website_link = website, seeking_venue = seeking_venue,seeking_description = seeking_description, facebook_link = facebook)
  db.session.add(artist)
  db.session.commit()
  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  

  database_response=[]
  for show in Show.query.all():
       venue = Venue.query.filter_by(id = show.venue_id)[0]
       artist = Artist.query.filter_by(id = show.artist_id)[0]
       data = {
    "venue_id": venue.id,
    "venue_name": venue.name,
    "artist_id": artist.id,
    "artist_name": artist.name,
    "artist_image_link": artist.image_link,
    "start_time": str(show.start_time)
  }
       database_response.append(data)
  return render_template('pages/shows.html', shows=database_response)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  artist_id = request.form.get('artist_id')
  venue_id = request.form.get('venue_id')
  start_time = request.form.get('start_time')
  show = Show(artist_id = artist_id , venue_id = venue_id, start_time = start_time)
  db.session.add(show)
  db.session.commit()
  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

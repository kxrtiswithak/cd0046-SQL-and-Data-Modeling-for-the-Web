from config import *

#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import sys
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
# db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = -1
  if isinstance(value, str):
    date = dateutil.parser.parse(value)
  else:
    date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

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
  areas = Venue.query.distinct(Venue.city, Venue.state).all()
  venues = Venue.query.all()
  
  return render_template('pages/venues.html', areas=areas, venues=venues)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term')
  response = Venue.query.filter(
    Venue.name.ilike('%' + search_term + '%')).all()
  
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
  shows = db.session.query(
    Show.venue_id,
    Artist.image_link,
    Artist.id,
    Artist.name,
    Show.start_time,
    Venue.name,
    Venue.image_link,
    ).join(Venue).join(Artist).filter(Show.venue_id == venue_id)
  upcoming_shows = shows.filter(Show.start_time >= datetime.now()).all()
  past_shows = shows.filter(Show.start_time < datetime.now()).all()

  return render_template('pages/show_venue.html', venue=venue, upcoming_shows=upcoming_shows, past_shows=past_shows)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)
  venue_name = request.form.get('name')
  error = False
  error_text = 'Error occured: Venue \'' + venue_name + '\' could not be listed.'

  try:
    venue = Venue()
    form.populate_obj(venue)
    db.session.add(venue)
    db.session.commit()
    flash('Venue \'' + venue_name + '\' was successfully listed!')
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
    flash(error_text)
  finally:
    db.session.close()

  return redirect(url_for('index'))

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  venue = Venue.query.get(venue_id)
  error_text = 'Error occured: Venue \'' + venue.name + '\' could not be deleted.'

  if venue is None:
    redirect(url_for('not_found_error', error='Venue not found'))

  try:
    db.session.delete(venue)
    db.session.commit()
    flash('Venue \'' + venue.name + '\' was successfully deleted!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash(error_text)
  finally:
    db.session.close()
  
  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artists = Artist.query.all()
  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term')
  response = Artist.query.filter(
    Artist.name.ilike('%' + search_term + '%')).all()
  
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  shows = db.session.query(
    Show.artist_id,
    Show.venue_id,
    Show.start_time,
    Venue.name,
    Venue.image_link,
  ).join(Venue).filter(Show.artist_id == artist_id)
  # shows = Show.query.join(Artist, Artist.id == Show.artist_id).join(Venue, Venue.id == Show.venue_id).filter(Artist.id == artist_id)
  upcoming_shows = shows.filter(Show.start_time >= datetime.now()).all()
  past_shows = shows.filter(Show.start_time < datetime.now()).all()

  return render_template('pages/show_artist.html', artist=artist, upcoming_shows=upcoming_shows, past_shows=past_shows)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  form = ArtistForm(obj=artist)
  
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  artist = Artist.query.get(artist_id)
  form = ArtistForm(request.form,obj=artist)
  artist_name = request.form.get('name')
  error_text = 'Error occured: Artist \'' + artist_name + '\' could not be edited.'

  try:
    form.populate_obj(artist)
    db.session.add(artist)
    db.session.commit()
    flash('Artist \'' + artist_name + '\' was successfully edited!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash(error_text)
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)
  
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(request.form,obj=venue)

  try:
    form.populate_obj(venue)
    db.session.add(venue)
    db.session.commit()
    flash('Venue \'' + venue.name + '\' was successfully edited!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('Error occured: Venue \'' + request.form.get('name') + '\' could not be edited.')
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)
  artist_name = request.form.get('name')
  error_text = 'Error occured: Artist \'' + artist_name + '\' could not be listed.'

  try:
    artist = Artist()
    form.populate_obj(artist)
    db.session.add(artist)
    db.session.commit()
    flash('Artist \'' + artist_name + '\' was successfully listed!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash(error_text)
  finally:
    db.session.close()

  return redirect(url_for('index'))

@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  artist = Artist.query.get(artist_id)
  error_text = 'Error occured: Artist \'' + artist.name + '\' could not be deleted.'

  if artist is None:
    redirect(url_for('not_found_error', error='Artist not found'))

  try:
    db.session.delete(artist)
    db.session.commit()
    flash('Artist \'' + artist.name + '\' was successfully deleted!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash(error_text)
  finally:
    db.session.close()
  
  return redirect(url_for('index'))


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows = db.session.query(
    Show.venue_id,
    Venue.name,
    Show.artist_id,
    Show.start_time,
    Artist.name,
    Artist.image_link
  ).join(Venue).join(Artist).all()
  return render_template('pages/shows.html', shows=shows)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm(request.form)

  try:
    show = Show()
    form.populate_obj(show)
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('Error occured: Failed to create show.')
  finally:
    db.session.close()

  return redirect(url_for('index'))

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

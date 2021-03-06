#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
import pytz
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import (
    Venue,
    Artist,
    Show,
    app,
    db
)


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
    locations = set(Venue.query.with_entities(Venue.city, Venue.state).all())
    print(locations)
    data = []
    for location in locations:
        elem = {
            "city": location[0],
            "state": location[1],
            "venues": []
        }
        venues = Venue.query.filter_by(city=location[0], state=location[1])
        for venue in venues:
            v = {}
            v['id'] = venue.id
            v['name'] = venue.name
            elem['venues'].append(v)

        data.append(elem)

    return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term=request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.ilike(
        '%{}%'.format(search_term))).all()
    data = []
    for venue in venues:
        data.append({
        'id': venue.id,
        'name': venue.name,
        "num_upcoming_shows": Show.query.filter_by(venue_id=venue.id).count()
        })
    response={
    "count": len(venues),
    "data": data
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    venue = Venue.query.get(venue_id)
    shows = Show.query.join(Venue, (Show.venue_id == venue.id))
    now = pytz.utc.localize(datetime.utcnow())
    past_shows = []
    upcoming_shows = []
    for show in shows:
        print(type(show.start_time))
        if show.start_time < now:
            past_shows.append({
            'artist_id': show.artist_id,
            'artist_name': Artist.query.filter(Artist.id == show.artist_id).with_entities(Artist.name).one_or_none()[0],
            "start_time": format_datetime(str(show.start_time))
            })
        else:
            upcoming_shows.append({
            'artist_id': show.artist_id,
            'artist_name': Artist.query.filter(Artist.id == show.artist_id).with_entities(Artist.name).one_or_none()[0],
            "start_time": format_datetime(str(show.start_time))
            })
    data={
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "facebook_link": venue.facebook_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }
    return render_template('pages/show_venue.html', venue=data)

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
    try:
        form = VenueForm(request.form)
        venue = Venue(
            name = form.name.data,
            city = form.city.data,
            state = form.state.data,
            address = form.address.data,
            phone = form.phone.data,
            image_link = form.image_link.data,
            facebook_link = form.facebook_link.data,
            genres = form.genres.data,
            website = form.website.data,
            seeking_talent = True if form.seeking_talent.data == 'True' else False,
            seeking_description = form.seeking_description.data
        )
        db.session.add(venue)
        db.session.commit()
        print(venue)

        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
        db.session.rollback()
        # TODO: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()
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
    data=[]
    artists_all = Artist.query.all()
    for artist in artists_all:
        a = {}
        a['id'] = artist.id
        a['name'] = artist.name
        data.append(a)
    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term=request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.ilike(
        '%{}%'.format(search_term))).all()
    data = []
    for venue in artists:
        data.append({
        'id': venue.id,
        'name': venue.name,
        "num_upcoming_shows": Show.query.filter_by(venue_id=venue.id).count()
        })
    response={
    "count": len(artists),
    "data": data
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    artist = Artist.query.get(artist_id)
    shows = Show.query.join(Artist, (Show.artist_id == artist.id))
    now = pytz.utc.localize(datetime.utcnow())
    past_shows = []
    upcoming_shows = []
    for show in shows:
        if show.start_time < now:
            past_shows.append({
            'venue_id': show.venue_id,
            'venue_name': Venue.query.filter(Venue.id == show.venue_id).with_entities(Venue.name).one_or_none()[0],
            "start_time": format_datetime(str(show.start_time))
            })
        else:
            upcoming_shows.append({
            'venue_id': show.venue_id,
            'venue_name': Venue.query.filter(Venue.id == show.venue_id).with_entities(Venue.name).one_or_none()[0],
            "start_time": format_datetime(str(show.start_time))
            })
    data={
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    
    # TODO: populate form with fields from artist with ID <artist_id>
    form.name.data = artist.name
    form.city.data = artist.city 
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.image_link.data = artist.image_link
    form.facebook_link.data = artist.facebook_link
    form.genres.data = artist.genres
    form.website.data = artist.website
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    form = ArtistForm(request.form)
    try:
        artist = Artist.query.get(artist_id)
        artist.name = form.name.data 
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.image_link = form.image_link.data
        artist.facebook_link = form.facebook_link.data
        artist.genres = form.genres.data
        artist.website = form.website.data
        artist.seeking_venue = True if form.seeking_venue.data == 'True' else False
        artist.seeking_description = form.seeking_description.data

        db.session.commit()
        flash(f"Artist {artist.name} was successfully updated")
    except Exception as e:
        print(e)
        db.session.rollback()
        flash(f"Artist {artist.name} updating is failed")
    finally:
        db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue=Venue.query.get(venue_id)
    # TODO: populate form with values from venue with ID <venue_id>
    form.name.data = venue.name
    form.city.data = venue.city
    form.address.data = venue.address
    form.state.data = venue.state
    form.phone.data = venue.phone
    form.image_link.data = venue.image_link
    form.facebook_link.data = venue.facebook_link
    form.genres.data = venue.genres
    form.website.data = venue.website
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    form = VenueForm(request.form)
    try:
        venue = Venue.query.get(venue_id)
        venue.name = form.name.data 
        venue.city = form.city.data
        venue.address = form.address.data
        venue.state = form.state.data
        venue.phone = form.phone.data
        venue.image_link = form.image_link.data
        venue.facebook_link = form.facebook_link.data
        venue.genres = form.genres.data
        venue.website = form.website.data
        venue.seeking_talent = True if form.seeking_talent.data == 'True' else False
        venue.seeking_description = form.seeking_description.data

        db.session.commit()
        flash(f"Venue {venue.name} was successfully updated")
    except Exception as e:
        print(e)
        db.session.rollback()
        flash(f"Venue {venue.name} updating is failed")
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
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    try:
        form = ArtistForm(request.form)
        artist = Artist(
            name = form.name.data,
            city = form.city.data,
            state = form.state.data,
            phone = form.phone.data,
            image_link = form.image_link.data,
            facebook_link = form.facebook_link.data,
            genres = form.genres.data,
            website = form.website.data,
            seeking_venue = True if form.seeking_venue.data == 'True' else False,
            seeking_description = form.seeking_description.data
        )
        db.session.add(artist)
        db.session.commit()
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
        db.session.rollback()
        # TODO: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    shows = Show.query.all()
    data = []
    for show in shows:
        s = {
            "venue_id": show.venue_id,
            "venue_name": Venue.query.filter(Venue.id == show.venue_id).with_entities(Venue.name)[0][0],
            "artist_id": show.artist_id,
            "artist_name":Artist.query.filter(Artist.id == show.artist_id).with_entities(Artist.name)[0][0],
            "start_time": format_datetime(str(show.start_time))
        }
        data.append(s)
    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
    try:
        form = ShowForm(request.form)
        show = Show(
            start_time = form.start_time.data,
            venue_id = form.venue_id.data,
            artist_id = form.artist_id.data)

        db.session.add(show)
        db.session.commit()
        # on successful db insert, flash success
        flash('Show was successfully listed!')
    except Exception as e:
        db.session.rollback()
        # TODO: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()

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
    app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

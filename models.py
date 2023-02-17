from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    genres = db.Column(db.ARRAY(db.String(20)))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))

    shows = db.relationship('Show', backref='venue', lazy=True)

    def __repr__(self):
        return f'<Venue - id: {self.id}, ' \
            f'name: {self.name}, ' \
            f'genres: {self.genres}, ' \
            f'address: {self.address}, ' \
            f'city: {self.city}, ' \
            f'state: {self.state}, ' \
            f'phone: {self.phone}, ' \
            f'website: {self.website_link}, ' \
            f'facebook_link: {self.facebook_link}, ' \
            f'seeking_talent: {self.seeking_talent}, ' \
            f'seeking_description: {self.seeking_description}, ' \
            f'image_link: {self.image_link}>'


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    genres = db.Column(db.ARRAY(db.String(20)))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String(500))

    shows = db.relationship('Show', backref='artist', lazy=True)

    def __repr__(self):
        return f'<Artist - id: {self.id}, ' \
            f'name: {self.name}, genres: {self.genres}, ' \
            f'city: {self.city}, ' \
            f'state: {self.state}, ' \
            f'phone: {self.phone}, ' \
            f'website: {self.website_link}, ' \
            f'facebook_link: {self.facebook_link}, ' \
            f'seeking_venue: {self.seeking_venue}, ' \
            f'seeking_description: {self.seeking_description}, ' \
            f'image_link: {self.image_link}>'


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'),
                         nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'),
                          nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Show - id: {self.id}, ' \
            f'venue_id: {self.venue_id}, ' \
            f'artist_id: {self.artist_id}, ' \
            f' start_time: {self.start_time}> '

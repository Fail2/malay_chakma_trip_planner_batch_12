from app import db

trip_traveler = db.Table('trip_traveler',
db.Column('trip_id', db.Integer, db.ForeignKey('trips.id'), primary_key=True),
db.Column('traveler_id', db.Integer, db.ForeignKey('travelers.id'), primary_key=True)
)

class Trip(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float, nullable=False, default=0.0)
    max_travelers = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(db.String(20), nullable=False, default='planned')

    expenses = db.relationship('Expense', backref='trip', lazy='select', cascade="all, delete-orphan")
    travelers = db.relationship('Traveler', secondary=trip_traveler, backref = db.backref('trips', lazy='dynamic'))

    def __repr__(self):
        return f"<Trip to {self.destination}>"

class Expense(db.Model):
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)

    def __repr__(self):
        return f"<Expense ${self.amount} for {self.title}>"

class Traveler(db.Model):
    __tablename__ = 'travelers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f"<Traverller {self.name}>"
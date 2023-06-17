from flask import Flask, request
import flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/hospital'
db = flask_sqlalchemy.SQLAlchemy(app)

with app.app_context():
    db.create_all()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    vaccine = db.Column(db.String(100), nullable=False)
    taken_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Event: {self.description,self.vaccine,self.taken_at}"
    
    def __init__(self, description):
        self.description = description

def format_event(event):
    return {
        "description": event.description,
        "id": event.id,
        "vaccine": event.vaccine,
        "taken_at": event.taken_at
    }

@app.route('/')
def hello():
    return 'Hello'

# Creating an event object
@app.route('/event', methods=['POST'])
def create_event():
    description = request.json['description']
    event = Event(description)
    db.session.add(event)
    db.session.commit()
    return format_event(event)

# Get all events
@app.route('/event', methods=["GET"])
def get_events():
    events = Event.query.order_by(Event.id.asc()).all()
    event_list = []
    for event in events:
        event_list.append(format_event(event))
    return {'events': event_list}

# Get single event
@app.route('/event/<id>', methods=['GET'])
def get_event(id):
    event = Event.query.filter_by(id=id).one()
    formatted_event = format_event(event)
    return {'formatted_event': formatted_event}

# Delete an event
@app.route('/event/<id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.filter_by(id=id).one()
    db.session.delete(event)
    db.session.commit()
    return f'Event (id:{id}) deleted!'

# Edit an Event
@app.route('/event/<id>', methods=['PUT'])
def update_event(id):
    event = Event.query.filter_by(id=id)
    description = request.json['description']
    event.update(dict(description=description, taken_at=datetime.utcnow()))
    db.session.commit()
    return {'event': format_event(event.one())}

if __name__ == '__main__':
    app.run(debug=True)

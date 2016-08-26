from radradrad import app, db, Venue

db.create_all()
Venue.create_all()

app.run()
from radradrad import app, db, Venue

db.create_all()
Venue.create_all()
app.config['DEBUG']=True
app.run(debug=True, host='0.0.0.0')

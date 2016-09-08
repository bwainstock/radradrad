from radradrad import app, db, Venue

if __name__ == '__main__':
    db.create_all()
    Venue.create_all()

    app.run()

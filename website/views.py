from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Institution, Exhibit, Artist
from . import db
import json
from sqlalchemy.sql import func
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/', methods = ['GET', 'POST'])
@login_required
def home():
    # inst = Institution(name = 'jakies', city = 'napisy')
    # db.session.add(inst)
    # db.session.commit()

    return render_template("home.html", user = current_user, institutions = Institution.query.all())


# @views.route('/delete-note', methods = ['POST'])
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()

#     return jsonify({})


def clean_string(string):
    return ''.join(c for c in string if c not in '\\\"\'')


@views.route('/search', methods = ['GET', 'POST'])
def search():
    if request.method == 'POST':        
        artist = request.form.get('artist')
        exhibit = request.form.get('exhibit')
        
        if not artist and not exhibit:
            flash('At least one field must be not empty.', category = 'error')
        else:
            artist = clean_string(artist)
            exhibit = clean_string(exhibit)

            if artist and exhibit:
                return redirect(url_for('views.results', artist = artist, exhibit = exhibit))
            elif artist:
                return redirect(url_for('views.results', artist = artist))
            elif exhibit:
                return redirect(url_for('views.results', exhibit = exhibit))
            else:
                flash('You used invalid characters. Please try again.', category = 'error')

        
    return render_template("search.html", user = current_user)


@views.route('/results', methods = ['GET'])
def results():
    artist = request.args.get('artist')
    exhibit = request.args.get('exhibit')

    if artist and exhibit:
        artists = Artist.query.filter(Artist.name.contains(artist)).all()
        ids = set()
        for row in artists:
            ids.add(row.id)
        exhibits = Exhibit.query.filter(Exhibit.author.in_(ids)).all()
        if exhibits:
            return render_template("results.html", user = current_user, exhibits = exhibits)
    elif artist:
        artists = Artist.query.filter(Artist.name.contains(artist)).all()
        if artists:
            return render_template("results.html", user = current_user, artists = artists)
    elif exhibit:
        exhibits = Exhibit.query.filter(Exhibit.title.contains(exhibit)).all()
        if exhibits:
            return render_template("results.html", user = current_user, exhibits = exhibits)

    return render_template("results.html", user = current_user)

@views.route('/artist', methods = ['GET'])
def artist():
    # nar = Artist(name = '明治元気だ', birth_date = -200, death_date = None)
    # db.session.add(nar)
    # db.session.commit()

    ex = Exhibit(author = 3, localization = 2, title = 'サスケは元気ですか', type = 'something', x_size = 2, y_size = 2, z_size = 1, state = 1)
    db.session.add(ex)
    db.session.commit()
    
    id = request.args.get('id')
    artist = Artist.query.filter(Artist.id == id).first()
    
    birth = ""
    if artist.birth_date < 0:
        birth = str((-1) * artist.birth_date) + " BC"
    else:
        birth = str(artist.birth_date)

    if artist:
        exhibits = Exhibit.query.filter(Exhibit.author == id).all()
        if exhibits:
            return render_template("artist.html", user = current_user, artist = artist, birth = birth, exhibits = exhibits)
        else:
            print("ERROR. No exhibits found!")
            return render_template("artist.html", user = current_user, artist = artist, birth = birth)
    return render_template("artist.html", user = current_user)

@views.route('/exhibit', methods = ['GET'])
def exhibit():
    id = request.args.get('id')
    exhibit = Exhibit.query.filter(Exhibit.id == id).first()
    if exhibit:
        return render_template("exhibit.html", user = current_user, exhibit = exhibit)
    return render_template("exhibit.html", user = current_user)

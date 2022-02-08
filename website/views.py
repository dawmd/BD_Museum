from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Institution, Exhibit
from . import db
import json

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

    if exhibit:
        results = Exhibit.query.filter(Exhibit.title.contains(exhibit))
        print(results.count())

    return render_template("results.html", user = current_user)#, artists = results)

    if not artist and not exhibit:
        return render_template("results.html", user = current_user, artists = results)

    return render_template("results.html", user = current_user)
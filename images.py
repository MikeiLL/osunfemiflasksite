from flask import Blueprint, jsonify, request, render_template, redirect, flash, make_response
from database import query, dict_query
from flask_login import current_user

images = Blueprint('images', __name__)

@images.before_request
def restrict_bp_to_students():
    if not (current_user and hasattr(current_user, 'user_level') and current_user.user_level >= 1):
        return redirect("/")

@images.route('/thumbs/<id>')
def get_thumbnail(id):
    binary_png = query("SELECT thumbnail FROM library_content WHERE id=%s", (id,))[0]
    if binary_png:
        response = make_response(bytes(binary_png[0]))
        response.headers['Content-Type'] = 'image/png'
    else:
        return render_template("400_generic.html", user=current_user, e="Whoops the file you were looking for doesn't seem to exist."), 404
    return response

from flask import Blueprint, jsonify, request, render_template, redirect, flash, make_response
from flask_login import LoginManager, current_user, login_user
import stripe
import os
import logging
import psycopg2
import psycopg2.extras
from datetime import datetime
from dotenv import load_dotenv
from database import query, dict_query

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

admin = Blueprint('admin', __name__)

@admin.context_processor
def inject_date():
    return dict(year=datetime.now().year)

@admin.before_request
def restrict_bp_to_admins():
    if not (current_user and hasattr(current_user, 'user_level') and current_user.user_level > 1):
        return redirect("/")

# This allows us to easily manage Stripe related env vairables
stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "webhook_secret": os.environ["STRIPE_WEBHOOK_SECRET"]
}
domain_url = os.environ["DOMAIN_URL"]
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: <https://dashboard.stripe.com/apikeys>
stripe.api_key = stripe_keys["secret_key"]

@admin.route("/")
def index():
    return render_template("admin_index.html", user=current_user)

@admin.route("/library")
def library():
    library_content = dict_query("""SELECT id, title, description, filename, minimum_grade, active
                                 FROM library_content
                                 ORDER BY filename""")
    return render_template("library_admin.html", user=current_user, library_content=library_content)


# see https://flask.palletsprojects.com/en/stable/patterns/fileuploads/
@admin.route("/library", methods=["POST"])
def new_library_document():
    # check if the post request has the file part
    if 'document' not in request.files:
        flash('No file part for PDF')
        return redirect(request.url, 303)
    if 'thumbnail' not in request.files:
        flash('No file part for thumbnail')
        return redirect(request.url, 303)
    doc = request.files['document']
    thumb = request.files['thumbnail']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if doc.filename == '':
        flash('No selected file')
        return redirect(request.url, 303)
    id = query("""
            INSERT INTO library_content
                (title, description, filename, filecontent, thumbnail, active, minimum_grade)
            VALUES (%s, %s, %s, %s, %s, true, %s) returning id
        """, (
            request.form["title"],
            request.form["description"],
            doc.filename,
            doc.read(),
            thumb.read(),
            request.form["minimum_grade"],
        ))[0][0]
    flash('Succesfully uploaded %s' % request.form["title"])
    return redirect(request.url, 303)

@admin.route("/users")
def user_listing():
    users = dict_query("SELECT * FROM users ORDER BY user_level")
    max_grade = query("SELECT MAX(level) FROM grade_levels")[0][0]
    return render_template("user_admin.html", user=current_user, users=users, max_grade=max_grade)

@admin.route("/users", methods=["post"])
def user_update():
    fields, params = [], []
    for field in ["fullname", "ifaorishaname", "email", "user_level", "grade_level"]:
        if field in request.form:
            fields.append(field + " = %s")
            params.append(request.form[field])
    params.append(request.form["userid"])
    dict_query("UPDATE users SET " + ", ".join(fields) + " WHERE id = %s", params)
    return redirect("/admin/users"), 303

@admin.route("/users", methods=["delete"])
def user_delete():
    data = request.json
    user_id = data['user_id']
    query("DELETE FROM users WHERE id = %s", (user_id,))
    return jsonify({"message": "user deleted " + user_id})

@admin.route("/docs", methods=["delete"])
def document_delete():
    data = request.json
    document_id = data['document_id']
    query("DELETE FROM library_content WHERE id = %s", (document_id,))
    return jsonify({"message": "document deleted " + document_id})

@admin.route('/docs/<id>')
def get_pdf(id):
    binary_pdf = query("SELECT filecontent FROM library_content WHERE id = %s", (id,))[0]
    if binary_pdf:
        response = make_response(bytes(binary_pdf[0]))
        response.headers['Content-Type'] = 'application/pdf'
        #response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'yourfilename' (for download)
    else:
        return render_template("400_generic.html", user=current_user, e="Whoops the file you were looking for doesn't seem to exist."), 404
    return response

from flask import Blueprint, jsonify, request, render_template, redirect, flash, make_response
from database import query, dict_query

images = Blueprint('images', __name__)

THUMBNAILS = None

print("############MODULE LOADED##########")

@images.route('/thumbs/<id>')
def get_thumbnail(id):
    """ print(id, type(id), id != '5')
    if id != '5':
        return "not yet"
    print("################################################################STILL GOING HERE....")
     """
    global THUMBNAILS
    if not THUMBNAILS:
        allthumbs = query("SELECT id, thumbnail FROM library_content WHERE active")
        print(allthumbs)
        THUMBNAILS = {t[0]: bytes(t[1]) for t in allthumbs}
        print(THUMBNAILS)
    return make_response(THUMBNAILS[int(id)])
    if binary_png:
        response = make_response(bytes(binary_png[0]))
        response.headers['Content-Type'] = 'image/png'
        #response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'yourfilename' (for download)
    else:
        return render_template("400_generic.html", user=current_user, e="Whoops the file you were looking for doesn't seem to exist."), 404
    return response

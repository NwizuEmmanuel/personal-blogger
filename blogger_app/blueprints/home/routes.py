from . import home_bp
from flask import render_template
from fetch_blog import fetch_blogs

@home_bp.route('/')
def home_page():
    return render_template('home/index.html', blogs=fetch_blogs())
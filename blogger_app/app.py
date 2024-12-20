from flask import Flask, request, redirect, url_for, session
from blueprints.admin import admin_bp
from blueprints.home import home_bp
from blueprints.blog import blog_bp

app = Flask(__name__)
app.secret_key = 'secret_key'

endpoints = ['blogger', 'new_blog']

@app.before_request
def before_request():
    if request.endpoint in endpoints:
        if not session.get("is_login") or not 'is_login' in session:
            return redirect(url_for('admin_login_page'))

app.register_blueprint(blog_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(home_bp)

if __name__ == "__main__":
    app.run(debug=True)
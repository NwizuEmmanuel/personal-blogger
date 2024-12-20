from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'secret_key'

def check_user_authentication():
    if not session.get("is_login") or not 'is_login' in session:
        return redirect(url_for('admin_login_page'))

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/admin', methods=['POST','GET'])
def admin_login_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == 'admin@mail.com' and password == 'admin':
            session['is_login'] = True
            return redirect(url_for('blogger'))
    if session.get("is_login"):
        return redirect(url_for('blogger'))
    return render_template('admin_login.html')

@app.route("/blogger")
def blogger():
    if session.get('is_login'):
        return render_template("blogger.html")
    return redirect(url_for('admin_login_page'))

@app.route("/new_blog", methods=['POST','GET'])
def new_blog():
    check_user_authentication()
    if request.method == 'POST':
        title = request.form['title']
        publish_date = request.form['publish_date']
        article_content = request.form['content']
        data = {
            'title': title,
            'publish_date': publish_date,
            'article_content': article_content
        }
        filename = "blog_db/" + title + ".json"
        with open(filename, 'a') as file:
            json.dump(data, file, indent=4)
        return redirect(url_for('blogger'))
    return render_template('new_blog.html')

@app.route("/logout")
def logout():
    session.pop('is_login', None)
    return redirect(url_for('admin_login_page'))

if __name__ == "__main__":
    app.run(debug=True)
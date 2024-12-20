from . import blog_bp
from flask import session, render_template, redirect, url_for, request, flash
import os
import json
from fetch_blog import fetch_blogs

@blog_bp.route("/")
def blogger():
    if session.get('is_login'):
        return render_template("blog/blogger.html", blogs=fetch_blogs())
    return redirect(url_for('admin_login_page'))

@blog_bp.route("/<blog_title>")
def read_blog(blog_title):
    filename = f"blog_db/{blog_title}.json"
    with open(filename, 'r') as file:
        data = json.load(file)
    title = data['title']
    pub_date = data['publish_date']
    content = data['article_content']
    context = {
        'title': title,
        'pub_date': pub_date,
        'content': content
    }
    return render_template('blog/blog_article.html', **context)

@blog_bp.route("/new_blog", methods=['POST','GET'])
def new_blog():
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
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        return redirect(url_for('blogger'))
    return render_template('blog/new_blog.html')

@blog_bp.route('/edit', defaults={'blog': None}, methods=['GET', 'POST'])
@blog_bp.route("/edit/<blog>", methods=['POST', 'GET'])
def edit_blog(blog):
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
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        flash("Blog updated", 'success')
        return redirect(url_for('blogger'))

    filename = f"blog_db/{blog}.json"
    if not os.path.exists(filename):
        flash("Error. Blog not found", 'error')
        return redirect(url_for('blogger'))
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    context = {
    'title': data['title'],
    'pub_date': data['publish_date'],
    'content': data['article_content'],
    }
    return render_template('blog/edit_blog.html', **context)
    

@blog_bp.route("/delete/<blog>")
def delete_blog(blog):
    filename = f"blog_db/{blog}.json"
    if os.path.exists(filename):
        os.remove(filename)
        flash("Blog deleted.", 'success')
    else:
        flash("Error blog not found.", "error")
    return redirect(url_for('blogger'))

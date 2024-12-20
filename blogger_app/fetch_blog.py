import os

def fetch_blogs():
    blogs = []
    directory = "blog_db/"
    files = os.listdir(directory)
    for file in files:
        filename, ext = file.split('.')
        blogs.append(filename)
    return blogs

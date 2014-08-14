#!/usr/bin/env python2

import datetime
import operator
import os
import shutil
import sys

from urlparse import urljoin

from flask.ext.assets import Environment, Bundle
from flask_flatpages import FlatPages
from flask_frozen import Freezer
from flask import Flask, render_template, request
from htmlmin import minify
from werkzeug.contrib.atom import AtomFeed

DEBUG = True

BASE_URL = "http://www.bendoan.me"
SITE_NAME = "Bendoan.me"
RSS_NUM_POSTS = 15

FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = ".md"

FREEZER_BASE_URL = BASE_URL
FREEZER_DESTINATION = "deploy"

WEB_ASSETS_PATH = FREEZER_DESTINATION + os.sep +'static' + os.sep + '.webassets-cache'
HTACCESS_PATH = FREEZER_DESTINATION + os.sep + ".htaccess"

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)
assets = Environment(app)
assets.url_expire = False

css = Bundle('css/base.css', 'css/layout.css', 'css/skeleton.css',
            'css/style.css', filters="cssmin", output='css/gen/packed.css')
assets.register('css_all', css)


@app.route("/")
def index():
    return minify(render_template('portfolio.html'))

@app.route("/blog/")
def blog():
    # ISO formatted dates can be sorted as plain strings
    p = sorted(pages, key=lambda p: p['date'], reverse=True)
    return minify(render_template('blog.html', pages=p))

@app.route('/blog/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return minify(render_template('page.html', page=page))

@app.route("/blog/tag/<tag>/")
def tag(tag):
    tagged = filter(lambda p: tag in p.meta.get('tags',[]), pages)
    tagged = sorted(tagged, key=lambda p: p['date'], reverse=True)
    return minify(render_template('tag.html', pages=tagged, tag=tag))

@app.route('/blog/posts.atom')
def feed():
    feed = AtomFeed("Recent Posts", feed_url=request.url, url=request.url_root)
    posts = sorted(pages, key=lambda p: p['date'], reverse=True)[:RSS_NUM_POSTS]
    for p in posts:
        feed.add(p.meta['title'], unicode(p.html),
                content_type='html',
                author=p.meta['author'],
                url=urljoin(urljoin(request.url_root, "blog/arch"), p.path),
                updated=p.meta['date'],
                published=p.meta['date'])
    return feed.get_response()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
        shutil.copy2(".htaccess", HTACCESS_PATH)
        shutil.rmtree(WEB_ASSETS_PATH, ignore_errors=True)#deletes metadata from static
    elif len(sys.argv) > 1 and sys.argv[1] == "test":
        freezer.run(debug=True, port=8000)
    else:
        app.run(port=8000)

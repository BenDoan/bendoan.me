#!/usr/bin/env python2

import sys
import os
import shutil

from flask import Flask, render_template, request
from flask.ext.assets import Environment, Bundle
from flask_flatpages import FlatPages
from flask_frozen import Freezer
from htmlmin import minify


DEBUG = True

BASE_URL = "http://www.bendoan.me"
SITE_NAME = "Bendoan.me"

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
    return minify(render_template('portfolio.html', pages=pages))

@app.route("/blog/")
def blog():
    return minify(render_template('blog.html', pages=pages))

@app.route('/blog/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return minify(render_template('page.html', page=page))

@app.route("/blog/tag/<string:tag>/")
def tag(tag):
    tagged = [p for p in pages if tag in p.meta.get('tags', [])]
    return minify(render_template('tag.html', pages=tagged, tag=tag))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
        shutil.copy2(".htaccess", HTACCESS_PATH)
        shutil.rmtree(WEB_ASSETS_PATH, ignore_errors=True)
    elif len(sys.argv) > 1 and sys.argv[1] == "test":
        freezer.run(debug=True, port=8000)
    else:
        app.run(port=8000)

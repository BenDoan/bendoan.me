title: Colophon
date: 2014-05-01
tags: [python, programming]
author: Ben Doan

> Colophon: a statement at the end of a book, typically with a printer's emblem, giving information about its authorship and printing. -

This site was previously using a python static site generator called [Pelican](http://blog.getpelican.com/).  It let me setup a modular theme with jinja2 for my portfolio, but it wasn't flexible enough when I wanted to extend the site and add a blog.  During my remake I end up using [Flask](http://flask.pocoo.org/) and [Frozen-Flask](https://pythonhosted.org/Frozen-Flask/) which are at the opposite end of the flexibility spectrum.  Frozen flask lets you build a static site with a normal web framework like Flask, with full control over routing and resource management.

In addition to Flask I'm using a module called [Flask FlatPages](http://pythonhosted.org/Flask-FlatPages/) which handles the loading of posts from markdown files.  The module is a bit heavy for what I'm using for, so I have plans to just replicate its functionality separately.



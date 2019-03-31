from flask import render_template,redirect,url_for
from . import home

@home.app_errorhandler(404)
def page_not_found(error):
    return render_template('home/404.html'),404
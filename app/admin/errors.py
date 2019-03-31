from flask import render_template
from . import admin

@admin.app_errorhandler(404)
def page_not_found(error):
    return render_template('home/404.html'),404
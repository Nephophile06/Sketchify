from flask import Flask, Blueprint, render_template

default_route = Blueprint("default_route", __name__)

@default_route.route("/")
def home_page():
    return render_template('homepage.html')

@default_route.route("/categories")
def categories():
    return render_template("categories.html")
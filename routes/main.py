from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template("index.html")

@main_bp.route('/re102-calculator')
def re102_calculator():
    return render_template("re102_calculator.html")

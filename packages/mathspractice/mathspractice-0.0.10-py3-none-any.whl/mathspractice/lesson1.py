import math
import random
import time

from flask import Blueprint, render_template, request, flash, session

from .stats import Statistics

bp = Blueprint('lesson1', __name__)

@bp.route('/')
def index():
    statistics = Statistics()
    return render_template(
        'lesson1/index.html',
        statistics=statistics,
    )


@bp.route('/addition', methods=['GET', 'POST'])
def addition():
    when = time.time()
    statistics = Statistics()
    stats = statistics.get_stats('lesson1', 'addition')
    if request.method == 'POST':
        try:
            if not request.form.get('answer'):
                raise ValueError('Sorry. You needed to provide an answer. Please try again.')
            first = int(request.form.get('first'))
            second = int(request.form.get('second'))
            answer = int(request.form.get('answer'))
            now = float(request.form.get('now'))
            elapsed = when - now
            real_answer = first + second
            stats['seconds'] += elapsed
            if answer == real_answer:
                flash(f"Correct. Well done! {first} + {second} = {answer}", category='correct')
                stats['correct'] += 1
            else:
                flash(f"Incorrect. I'm sorry but {first} + {second} is not {answer}. It is {real_answer}", category='incorrect')
                stats['incorrect'] += 1
            statistics.save()
        except Exception as e:
            flash(str(e), category='error')
    max_value = int(math.pow(10, 1 + stats['correct'] // 30))
    first = random.randint(1, max_value-1)
    second = random.randint(1, max_value-1)
    now = int(time.time())
    return render_template(
        'lesson1/addition.html',
        first=first, second=second, now=now, statistics=statistics
    )


@bp.route('/subtraction', methods=['GET', 'POST'])
def subtraction():
    when = time.time()
    statistics = Statistics()
    stats = statistics.get_stats('lesson1', 'subtraction')
    if request.method == 'POST':
        try:
            if not request.form.get('answer'):
                raise ValueError('Sorry. You needed to provide an answer. Please try again.')
            first = int(request.form.get('first'))
            second = int(request.form.get('second'))
            answer = int(request.form.get('answer'))
            now = float(request.form.get('now'))
            elapsed = when - now
            real_answer = first - second
            stats['seconds'] += elapsed
            if answer == real_answer:
                stats['correct'] += 1
                flash(f"Correct. Well done! {first} - {second} = {answer}", category='correct')
            else:
                stats['incorrect'] += 1
                flash(f"Incorrect. I'm sorry but {first} - {second} is not {answer}. It is {real_answer}", category='incorrect')
            statistics.save()
        except Exception as e:
            flash(str(e), category='error')
    max_value = int(math.pow(10, 1 + stats['correct'] // 30))
    first = random.randint(1, max_value-1)
    second = random.randint(1, max_value-1)
    now = int(time.time())
    return render_template(
        'lesson1/subtraction.html',
        first=first, second=second, now=now, statistics=statistics
    )

import math
import random
import time

from flask import Blueprint, render_template, request, flash, session

from .stats import Statistics

bp = Blueprint('lesson2', __name__)

@bp.route('/')
def index():
    statistics = Statistics()
    return render_template(
        'lesson2/index.html',
        statistics=statistics,
    )


@bp.route('/multiply', methods=['GET', 'POST'])
def multiply():
    when = time.time()
    statistics = Statistics()
    stats = statistics.get_stats('lesson2', 'multiply')
    if request.method == 'POST':
        try:
            if not request.form.get('answer'):
                raise ValueError('Sorry. You needed to provide an answer. Please try again.')
            first = int(request.form.get('first'))
            second = int(request.form.get('second'))
            answer = int(request.form.get('answer'))
            now = float(request.form.get('now'))
            elapsed = when - now
            real_answer = first * second
            stats['seconds'] += elapsed
            if answer == real_answer:
                flash(f"Correct. Well done! {first} x {second} = {answer}", category='correct')
                stats['correct'] += 1
            else:
                flash(f"Incorrect. I'm sorry but {first} x {second} is not {answer}. It is {real_answer}", category='incorrect')
                stats['incorrect'] += 1
            statistics.save()
        except Exception as e:
            flash(str(e), category='error')
    max_value = int(math.pow(10, 1 + stats['correct'] // 30))
    first = random.randint(1, max_value-1)
    second = random.randint(1, max_value-1)
    now = int(time.time())
    return render_template(
        'lesson2/multiply.html',
        first=first, second=second, now=now, statistics=statistics
    )

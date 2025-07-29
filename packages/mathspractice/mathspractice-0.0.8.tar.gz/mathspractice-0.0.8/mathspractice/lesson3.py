import math
import random
import time

from flask import Blueprint, render_template, request, flash, session

from .stats import Statistics

bp = Blueprint('lesson3', __name__)

@bp.route('/')
def index():
    statistics = Statistics()
    return render_template(
        'lesson3/index.html',
        statistics=statistics,
    )


@bp.route('/division', methods=['GET', 'POST'])
def division():
    when = time.time()
    statistics = Statistics()
    stats = statistics.get_stats('lesson3', 'division')
    if request.method == 'POST':
        try:
            if not request.form.get('answer'):
                raise ValueError('Sorry. You needed to provide an answer. Please try again.')
            if not request.form.get('remainder'):
                raise ValueError('Sorry. You needed to provide a remainder. Please try again.')
            first = int(request.form.get('first'))
            second = int(request.form.get('second'))
            answer = int(request.form.get('answer'))
            remainder = int(request.form.get('remainder'))
            now = float(request.form.get('now'))
            elapsed = when - now
            real_calculation = first / second
            real_answer = int(real_calculation)
            real_remainder = first - (second * real_answer)
            stats['seconds'] += elapsed
            if answer == real_answer and remainder == real_remainder:
                flash(
                    f"Correct. "
                    f"Well done! "
                    f"{first} ÷ {second} = {answer} remainder {remainder}",
                    category='correct')
                stats['correct'] += 1
            else:
                flash(
                    f"Incorrect. "
                    f"I'm sorry but {first} ÷ {second} is not {answer} remainder {remainder}. "
                    f"It is {real_answer} remainder {real_remainder}",
                    category='incorrect')
                stats['incorrect'] += 1
            statistics.save()
        except Exception as e:
            flash(str(e), category='error')
    max_value = int(math.pow(10, 1 + stats['correct'] // 30))
    first = random.randint(1, max_value-1)
    second = random.randint(1, max_value-1)
    now = int(time.time())
    return render_template(
        'lesson3/division.html',
        first=first, second=second, now=now, statistics=statistics
    )

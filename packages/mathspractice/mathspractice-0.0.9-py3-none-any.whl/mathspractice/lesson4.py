import math
import random
import time
from typing import Tuple

from flask import Blueprint, render_template, request, flash

from .stats import Statistics

bp = Blueprint('lesson4', __name__)

@bp.route('/')
def index():
    statistics = Statistics()
    return render_template(
        'lesson4/index.html',
        statistics=statistics,
    )


def factorise(n: int) -> list[int]:
    factors = []
    for pp in range(2, int(math.sqrt(n)) + 1):
        while n % pp == 0:
            factors.append(pp)
            n //= pp
    factors.append(n)
    return factors


def reduce(numerator: int, denominator: int) -> Tuple[int, int]:
    n_factors = factorise(numerator)
    d_factors = factorise(denominator)
    for f in list(n_factors):
        if f in d_factors:
            n_factors.remove(f)
            d_factors.remove(f)
    return int(math.prod(n_factors)), int(math.prod(d_factors))


@bp.route('/reduction', methods=['GET', 'POST'])
def reduction():
    when = time.time()
    statistics = Statistics()
    stats = statistics.get_stats('lesson4', 'reduction')
    if request.method == 'POST':
        try:
            if not request.form.get('numerator') or not request.form.get('denominator'):
                raise ValueError('Sorry. You needed to provide a numerator and denominator. Please try again.')
            first = int(request.form.get('first'))
            second = int(request.form.get('second'))
            numerator = int(request.form.get('numerator'))
            denominator = int(request.form.get('denominator'))
            now = float(request.form.get('now'))
            elapsed = when - now
            real_numerator, real_denominator = reduce(first, second)
            stats['seconds'] += elapsed
            if numerator == real_numerator and denominator == real_denominator:
                flash(f"Correct. Well done! {first} / {second} = {numerator} / {denominator}", category='correct')
                stats['correct'] += 1
            else:
                flash(f"Incorrect. I'm sorry but {first} / {second} is not reduced to {numerator} / {denominator}. It is {real_numerator} / {real_denominator}", category='incorrect')
                stats['incorrect'] += 1
            statistics.save()
        except Exception as e:
            flash(str(e), category='error')
    max_value = int(math.pow(10, 2 + stats['correct'] // 30))
    first = random.randint(2, max_value-1)
    second = random.randint(2, max_value-1)
    now = int(time.time())
    return render_template(
        'lesson4/reduction.html',
        first=first, second=second, now=now, statistics=statistics
    )

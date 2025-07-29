import math
import random
import time
from decimal import Decimal, ROUND_FLOOR
from typing import Tuple

from flask import Blueprint, render_template, request, flash

from .stats import Statistics

bp = Blueprint('lesson10', __name__)

@bp.route('/')
def index():
    statistics = Statistics()
    return render_template(
        'lesson10/index.html',
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


@bp.route('/percent/to/fractions', methods=['GET', 'POST'])
def percent_to_fractions():
    when = time.time()
    statistics = Statistics()
    stats = statistics.get_stats('lesson10', 'percent_to_fractions')
    if request.method == 'POST':
        try:
            if not request.form.get('numerator') or not request.form.get('denominator'):
                raise ValueError('Sorry. You needed to provide a numerator and denominator. Please try again.')
            first = Decimal(request.form.get('first'))
            second = 100
            numerator = int(request.form.get('numerator'))
            denominator = int(request.form.get('denominator'))
            now = float(request.form.get('now'))
            elapsed = when - now
            real_numerator, real_denominator = reduce(int(first * 10), second * 10)
            stats['seconds'] += elapsed
            if numerator == real_numerator and denominator == real_denominator:
                flash(f"Correct. Well done! {first} % = {numerator} / {denominator}", category='correct')
                stats['correct'] += 1
            else:
                flash(f"Incorrect. I'm sorry but {first} % is not reduced to {numerator} / {denominator}. It is {real_numerator} / {real_denominator}", category='incorrect')
                stats['incorrect'] += 1
            statistics.save()
        except Exception as e:
            flash(str(e), category='error')
    max_value = int(math.pow(10, 2 + stats['correct'] // 20))
    first = random.randint(2, max_value-1) / 10
    now = int(time.time())
    return render_template(
        'lesson10/percent_to_fractions.html',
        first=first, now=now, statistics=statistics
    )

@bp.route('/percent/to/decimals', methods=['GET', 'POST'])
def percent_to_decimals():
    when = time.time()
    statistics = Statistics()
    stats = statistics.get_stats('lesson10', 'percent_to_decimals')
    if request.method == 'POST':
        try:
            if not request.form.get('numerator'):
                raise ValueError('Sorry. You needed to provide an answer. Please try again.')
            first = Decimal(request.form.get('first'))
            numerator = Decimal(request.form.get('numerator'))
            now = float(request.form.get('now'))
            elapsed = when - now
            real_numerator = first / 100
            stats['seconds'] += elapsed
            if numerator == real_numerator :
                flash(f"Correct. Well done! {first} % = {numerator} ", category='correct')
                stats['correct'] += 1
            else:
                flash(f"Incorrect. I'm sorry but {first} % is not {numerator}. It is {real_numerator}", category='incorrect')
                stats['incorrect'] += 1
            statistics.save()
        except Exception as e:
            flash(str(e), category='error')
    max_value = int(math.pow(10, 2 + stats['correct'] // 15))
    first = random.randint(2, max_value-1) / 10
    now = int(time.time())
    return render_template(
        'lesson10/percent_to_decimals.html',
        first=first, now=now, statistics=statistics
    )

@bp.route('/fraction/to/decimals', methods=['GET', 'POST'])
def fraction_to_decimals():
    when = time.time()
    statistics = Statistics()
    stats = statistics.get_stats('lesson10', 'fraction_to_decimals')
    if request.method == 'POST':
        try:
            if not request.form.get('numerator'):
                raise ValueError('Sorry. You needed to provide an answer. Please try again.')
            first = Decimal(request.form.get('first'))
            second = Decimal(request.form.get('second'))
            numerator = Decimal(request.form.get('numerator'))
            now = float(request.form.get('now'))
            elapsed = when - now
            real_numerator = first / second
            stats['seconds'] += elapsed
            if numerator == real_numerator :
                flash(f"Correct. Well done! {first} / {second} = {numerator} ", category='correct')
                stats['correct'] += 1
            else:
                flash(f"Incorrect. I'm sorry but {first} / {second} is not {numerator}. It is {real_numerator}", category='incorrect')
                stats['incorrect'] += 1
            statistics.save()
        except Exception as e:
            flash(str(e), category='error')
    max_value = int(math.pow(10, 1 + stats['correct'] // 15))
    while True:
        first = random.randint(2, max_value-1)
        second = random.randint(2, max_value-1)
        answer = str(Decimal(first) / Decimal(second))
        if '.' not in answer:
            continue
        decimals = answer.split('.')[1]
        while len(decimals) > 0 and decimals[-1] == '0':
            decimals = decimals[:-1]
        if 0 < len(decimals) <= 4:
            break
    now = int(time.time())
    return render_template(
        'lesson10/fraction_to_decimals.html',
        first=first, second=second, now=now, statistics=statistics
    )

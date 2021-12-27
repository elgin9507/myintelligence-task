import operator
from functools import reduce, wraps

from flask import abort, request
from peewee import Select
from flask_restful import marshal
from .parsers import paginate_parser


def paginate(results, url, start, limit):
    start = int(start)
    limit = int(limit)
    count = results.count()
    if count < start or start < 0 or limit < 0:
        abort(404)
    # make response
    obj = {}
    obj["start"] = start
    obj["limit"] = limit
    obj["count"] = count
    # make URLs
    # make previous url
    if start == 0:
        obj["previous"] = None
    else:
        start_copy = max(0, start - limit)
        obj["previous"] = url + "?start=%d&limit=%d" % (start_copy, limit)
    # make next url
    if start + limit > count:
        obj["next"] = None
    else:
        start_copy = start + limit
        obj["next"] = url + "?start=%d&limit=%d" % (start_copy, limit)
    # finally extract result according to bounds
    obj["results"] = results[(start) : (start + limit)]
    return obj


def get_or_404(model, **kwargs):
    clauses = []

    for field, value in kwargs.items():
        clauses.append((getattr(model, field) == value))

    instance = model.select().where(reduce(operator.and_, clauses)).first()

    if instance is None:
        abort(404)

    return instance


def paginated_response(marshal_fields):
    def paginate_decorator(view_func):
        @wraps(view_func)
        def _wrapped(*args, **kwargs):
            parser = paginate_parser
            url_params = parser.parse_args()
            start, limit = operator.itemgetter("start", "limit")(url_params)

            resp = view_func(*args, **kwargs)

            paginated = paginate(resp, request.url_rule.rule, start, limit)
            paginated["results"] = marshal(paginated["results"], marshal_fields)

            return paginated

        return _wrapped

    return paginate_decorator

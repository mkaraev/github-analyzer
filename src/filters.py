from datetime import datetime, timezone
import functools

from src.parser import string_to_datetime


def apply_filters(filters):
    def decorator(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            applier = filter_applier_fabric(filters)
            result = f(*args, **kwargs)
            return applier(result)

        return inner

    return decorator


def filter_applier_fabric(filters):
    def inner(items):
        filter_ = combine_filters(filters)
        return list(filter(filter_, items))

    return inner


def combine_filters(filters):
    def filter_(item):
        return all([f(item) for f in filters])

    return filter_


def old_filter_fabric(days):
    def filter_(item):
        created_at = string_to_datetime(item["created_at"])
        days_passed = datetime.now(timezone.utc) - created_at
        return days_passed.days > days

    return filter_


def range_filter_fabric(since, until):
    def filter_(item):
        created_at = string_to_datetime(item["created_at"])

        if since and since > created_at:
            return False
        if until and until < created_at:
            return False
        return True

    return filter_

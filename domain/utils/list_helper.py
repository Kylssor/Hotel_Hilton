def first_or_none(iterable):
    if iterable:
        return next(iter(iterable), None)
    
    return None
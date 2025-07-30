def flatten(l: list):
    for el in l:
        if isinstance(el, list):
            yield from flatten(el)
        else:
            yield el

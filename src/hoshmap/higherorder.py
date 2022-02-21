from hoshmap import Let


def map(f, field, in_out, asdict=False):
    """Apply 'f' to every element in 'field'

     Assume the element goes as the first arg of 'f'.
     It should not apper inside 'in_out'.

     If field is a dict, f should receive and return key-value tuples.
     """
    let = Let(f, in_out)
    input, outstr = let.input, let.outstr
    if let.parsed:
        it = iter(input.items())
        next(it)
        instr = " ".join(f"{k}:{v}" for k, v in it)
    else:
        instr = let.instr
    instr = f"{field}:collection{(' ' + instr) if instr else ''}"

    def fun(collection, **kwargs):
        if isinstance(collection, dict):
            return dict(f(kv, **kwargs) for kv in collection.items())
        elif asdict:
            return dict(f(v, **kwargs) for v in collection)
        else:
            return [f(v, **kwargs) for v in collection]
    return fun, f"{instr}→{outstr}"

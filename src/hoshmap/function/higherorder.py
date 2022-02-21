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
        if isinstance(collection, dict) or asdict:
            if not asdict:
                collection = collection.items()
            dic = {}
            for kv in collection:
                kv_ret = f(kv, **kwargs)
                if kv_ret is not ...:
                    k, v = kv_ret
                    dic[k] = v
            return dic
        else:
            lst = []
            for item in collection:
                ret = f(item, **kwargs)
                if ret is not ...:
                    lst.append(ret)
            return lst

    return fun, f"{instr}→{outstr}"


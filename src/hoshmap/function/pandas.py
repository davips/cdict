def series2df(key__measures):
    import pandas as pd
    k, measures = key__measures
    allseries = list(measures.values())
    try:
        table = pd.concat(allseries, axis=1)
        result = k, table
    except ValueError as e:
        if str(e) == "All objects passed were None":
            result = ...
        else:
            raise Exception(str(e))
    return result

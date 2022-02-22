def series2df(k, measures):
    import pandas as pd

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

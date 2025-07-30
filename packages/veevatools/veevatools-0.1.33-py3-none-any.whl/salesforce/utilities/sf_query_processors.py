from collections import OrderedDict
import pandas as pd


def recursive_walk(od_field: OrderedDict):
    """
    Recursively flattens each row the results of simple salesforce.
    Only works for bottom up queries.
    :param od_field: results returned by simple salesforce (multiple objects)
    :return: returns a flattened list of dictionaries
    """
    d = {}
    for k in od_field.keys():
        if isinstance(od_field[k], OrderedDict) & (k != 'attributes'):
            if 'attributes' in od_field[k].keys():
                ret_df = recursive_walk(od_field[k])
                d = {**d, **ret_df}
            else:
                obj = od_field['attributes']['type'].replace(" ", ".")
                d[f'{obj}.{k}'] = ",\n".join([   f'{k}: {v}' for k, v in od_field[k].items() if v is not None])
        else:
            if k != 'attributes':
                obj = od_field['attributes']['type'].replace(" ", ".")
                d[f'{obj}.{k}'] = od_field[k]
    return d

def transform_sf_result_set_rec(query_results: OrderedDict):
    """
    Recursively flattens the results of simple salesforce. It needs flattening when  selecting
    multiple objects.
    :param query_results:
    :return:
    """
    data = []
    for res in query_results:
        d = recursive_walk(res)
        data.append(d)
    data = pd.DataFrame(data)
    return data

def deep_merge_dictionaries(source, destination):
    """
    run me with nosetests --with-doctest file.py

    >>> a = { 'first' : { 'all_rows' : { 'pass' : 'dog', 'number' : '1' } } }
    >>> b = { 'first' : { 'all_rows' : { 'fail' : 'cat', 'number' : '5' } } }
    >>> deep_merge_dictionaries(b, a) == { 'first' : { 'all_rows' : { 'pass' : 'dog', 'fail' : 'cat', 'number' : '5' } } }
    True
    """
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            deep_merge_dictionaries(value, node)
        else:
            destination[key] = value

    return destination
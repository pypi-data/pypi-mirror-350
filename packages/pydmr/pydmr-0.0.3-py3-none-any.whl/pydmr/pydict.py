try:
    import pandas as pd
    import_error = False
except:
    import_error = True


def dict_to_flat(dmr, format):
    # TODO extend to format=pandas

    dmr_flat = {}

    if not 'data' in dmr:
        raise ValueError("data key is required in dmr dictionary")

    data = dmr['data']
    if format=='table':
        if not isinstance(data, list):
            raise ValueError("dmr['data'] must be a list")
        data = {dat[0]: dat[1:] for dat in data}
    elif not isinstance(data, dict):
        raise ValueError("dmr['data'] must be a dictionary")
    dmr_flat['data'] = data


    if 'columns' in dmr:
        dmr_flat['columns'] = dmr['columns']


    if 'rois' in dmr:
        rois = dmr['rois']
        if format=='flat':
            if not isinstance(rois, dict):
                raise ValueError("dmr['rois'] must be a dictionary")
        elif format=='nest':
            if not isinstance(rois, dict):
                raise ValueError("dmr['rois'] must be a dictionary")
            rois = _nested_dict_to_multi_index(rois)
        elif format=='table':
            if not isinstance(rois, list):
                raise ValueError("dmr['rois'] must be a list")
            rois = {tuple(roi[:3]): roi[4] for roi in rois}
        dmr_flat['rois'] = rois


    if 'pars' in dmr:
        pars = dmr['pars']
        if format=='flat':
            if not isinstance(pars, dict):
                raise ValueError("dmr['pars'] must be a dictionary")
        elif format=='nest':
            if not isinstance(pars, dict):
                raise ValueError("dmr['pars'] must be a dictionary")
            pars = _nested_dict_to_multi_index(pars)
        elif format=='table':
            if not isinstance(pars, list):
                raise ValueError("dmr['pars'] must be a list")
            pars = {tuple(par[:3]): par[4] for par in pars}
        dmr_flat['pars'] = pars


    if 'sdev' in dmr:
        sdev = dmr['sdev']
        if format=='flat':
            if not isinstance(sdev, dict):
                raise ValueError("dmr['sdev'] must be a dictionary")
        elif format=='nest':
            if not isinstance(sdev, dict):
                raise ValueError("dmr['sdev'] must be a dictionary")
            sdev = _nested_dict_to_multi_index(sdev)
        elif format=='table':
            if not isinstance(sdev, list):
                raise ValueError("dmr['sdev'] must be a list")
            sdev = {tuple(sd[:3]): sd[4] for sd in sdev}
        dmr_flat['sdev'] = sdev

    return dmr_flat


def dict_reformat(dmr, format):

    if format=='pandas':
        if import_error:
            raise ImportError(
                "This feature requires an installation of pandas. "
                "or installation of pydmr with pandas option "
                "as pip install pydmr[pandas]."
            )

    if format == 'table':
        dmr['data'] = [[k] + v for k,v in dmr['data'].items()]
    elif format == 'pandas':
        cols = ['description', 'unit', 'type']
        if 'columns' in dmr:
            cols += dmr['columns']
        dmr['data'] = pd.DataFrame.from_dict(dmr['data'], orient='index', columns=cols)
    if 'pars' in dmr:
        if format == 'nest':
            dmr['pars'] = _multi_index_to_nested_dict(dmr['pars'])
        elif format == 'table':
            dmr['pars'] = [list(k) + [v] for k,v in dmr['pars'].items()]
        elif format == 'pandas':
            cols = ['subject', 'study', 'parameter', 'value']
            vals = [list(k) + [v] for k,v in dmr['pars'].items()]
            dmr['pars'] = pd.DataFrame(vals, columns=cols)
    if 'rois' in dmr: 
        if format == 'nest':
            dmr['rois'] = _multi_index_to_nested_dict(dmr['rois'])
        elif format == 'table':
            dmr['rois'] = [list(k) + [v] for k,v in dmr['rois'].items()]
        elif format == 'pandas':
            vals = [list(k) + list(v) for k,v in dmr['rois'].items()]
            dmr['rois'] = pd.DataFrame(vals).T
    if 'sdev' in dmr:
        if format == 'nest':
            dmr['sdev'] = _multi_index_to_nested_dict(dmr['sdev'])
        elif format == 'table':
            dmr['sdev'] = [list(k) + [v] for k, v in dmr['sdev'].items()]
        elif format == 'pandas':
            cols = ['subject', 'study', 'parameter', 'value']
            vals = [list(k) + [v] for k,v in dmr['sdev'].items()]
            dmr['sdev'] = pd.DataFrame(vals, columns=cols)
    return dmr


def dict_drop(data:dict, subject, study, parameter):

    if parameter is not None:
        if isinstance(parameter, str):
            parameter = [parameter]
        data['data'] = {k:v for k,v in data['data'].items() if k not in parameter}
        if 'pars' in data:
            data['pars'] = {k:v for k,v in data['pars'].items() if k[2] not in parameter}
        if 'sdev' in data:
            data['sdev'] = {k:v for k,v in data['sdev'].items() if k[2] not in parameter}

    if subject is not None:
        if isinstance(subject, str):
            subject = [subject]
        if 'pars' in data:
            data['pars'] = {k:v for k,v in data['pars'].items() if k[0] not in subject}
        if 'sdev' in data:
            data['sdev'] = {k:v for k,v in data['sdev'].items() if k[0] not in subject}

    if study is not None:
        if isinstance(study, str):
            study = [study]
        if 'pars' in data:
            data['pars'] = {k:v for k,v in data['pars'].items() if k[1] not in study}
        if 'sdev' in data:
            data['sdev'] = {k:v for k,v in data['sdev'].items() if k[1] not in study}

    return data


def dict_keep(data:dict, subject, study, parameter):

    if parameter is not None:
        if isinstance(parameter, str):
            parameter = [parameter]
        data['data'] = {k:v for k,v in data['data'].items() if k in parameter}
        if 'pars' in data:
            data['pars'] = {k:v for k,v in data['pars'].items() if k[2] in parameter}
        if 'sdev' in data:
            data['sdev'] = {k:v for k,v in data['sdev'].items() if k[2] in parameter}

    if subject is not None:
        if isinstance(subject, str):
            subject = [subject]
        if 'pars' in data:
            data['pars'] = {k:v for k,v in data['pars'].items() if k[0] in subject}
        if 'sdev' in data:
            data['sdev'] = {k:v for k,v in data['sdev'].items() if k[0] in subject}

    if study is not None:
        if isinstance(study, str):
            study = [study]
        if 'pars' in data:
            data['pars'] = {k:v for k,v in data['pars'].items() if k[1] in study}
        if 'sdev' in data:
            data['sdev'] = {k:v for k,v in data['sdev'].items() if k[1] in study}

    return data


def _multi_index_to_nested_dict(multi_index_dict):
    """
    Converts a dictionary with tuple keys (multi-index) into a nested dictionary.
    
    Parameters:
        multi_index_dict (dict): A dictionary where keys are tuples of indices.

    Returns:
        dict: A nested dictionary where each level corresponds to an index in the tuple.
    """
    nested_dict = {}

    for key_tuple, value in multi_index_dict.items():
        current_level = nested_dict  # Start at the root level
        for key in key_tuple[:-1]:  # Iterate through all but the last key
            current_level = current_level.setdefault(key, {})  # Go deeper/create dict
        current_level[key_tuple[-1]] = value  # Assign the final value

    return nested_dict


def _nested_dict_to_multi_index(nested_dict, parent_keys=()):
    """
    Converts a nested dictionary into a dictionary with tuple keys (multi-index).

    Parameters:
        nested_dict (dict): A nested dictionary.
        parent_keys (tuple): Used for recursion to keep track of the current key path.

    Returns:
        dict: A dictionary where keys are tuples representing the hierarchy.
    """
    flat_dict = {}

    for key, value in nested_dict.items():
        new_keys = parent_keys + (key,)  # Append the current key to the path

        if isinstance(value, dict):  # If the value is a dict, recurse
            flat_dict.update(_nested_dict_to_multi_index(value, new_keys))
        else:  # If it's a final value, store it with the multi-index key
            flat_dict[new_keys] = value

    return flat_dict




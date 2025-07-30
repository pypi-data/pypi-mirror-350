import os
import shutil
import zipfile
import csv
from io import TextIOWrapper

import numpy as np


from pydmr.pydict import (
    dict_keep, 
    dict_reformat, 
    _nested_dict_to_multi_index,
    dict_to_flat,
)



def write(path:str, dmr:dict, format='flat'):
    """Write data to disk in .dmr format.

    Args:
        path (str): path to .dmr file. If the extension .dmr is not 
          included, it is added automatically.
        dmr (dict): A dictionary with one required key 'data' 
          and optional keys 'rois', 'pars', 'sdev', 'columns'. 
          dmr['data'] is a dictionary with one item for each 
          parameter; the key is the parameter and the value is a list 
          of containing description, unit and python data type. 
          dmr['rois'] is a dictionary with one item per ROI; each 
          ROI is a dictionary on itself which has keys 
          (subject, study, parameter) and a list or array as value.
          dmr['pars'] is a dictionary with parameters 
          such as sequence parameters or subject characteristics. 
          dmr['sdev'] is a dictionary with standard deviations 
          of parameters listed in pars.csv. This can include only a 
          subset of parameters but all parameters in sdev.csv must 
          also be in pars.csv. Defaults to None.
          dmr['columns'] is a list of headers for optional 
          columns in the data dictionary. Required if the data 
          dictionary contains extra columns above the required three 
          (description, unit, type). 
        format (str, optional): Formatting of the arguments. 
          The default ('flat') is a dictionary with a 
          multi-index, meaning values (rois, pars, sdev) are 
          flat dictionaries with a multi-index consisting of 
          (subject, study, parameter). If format='nest', these values 
          are nested dictionaries with 3 levels. If 
          format='table', the values are a list of lists. 
          Defaults to 'flat'.
        
 
    Raises:
        ValueError: if the data are not dmr-compliant formatted.
        ImportError: if an optional package is not installed
    """

    #
    # Check dmr compliance
    #

    dmr = dict_to_flat(dmr, format)

    data = dmr['data']
    for key, values in data.items():
        if not isinstance(values, list):
            raise ValueError(
                f"Each dmr['data'] value must be a list"
            )     
        length = 3
        if 'columns' in dmr:
            length += len(dmr['columns'])    
        if len(values) < length:
            raise ValueError(
                f"Each dmr['data'] value must have at least {length} elements. "
                f"The required 'description', 'unit', 'type' and the "
                f"optional columns {columns}."
            )
        
    if 'rois' in dmr:
        rois = dmr['rois']
        for roi in rois.keys():
            if len(roi) != 3:
                raise ValueError("Each rois key must be a 3-element tuple")
            if roi[-1] not in list(data.keys()):
                raise ValueError(
                    f"rois parameter {roi[-1]} not in dmr['data']. "
                    "Please add it to the dictionary."
                )
        for key, values in rois.items():
            if key[-1] not in data:
                raise ValueError(
                    f"rois parameter {key[-1]} not in data. "
                    "Please add it to the dictionary."
                )
            data_type = np.dtype(data[key[-1]][2])
            write_values = np.asarray(values).astype(data_type) 
            if not np.array_equal(write_values, values):
                raise ValueError(
                    f"rois parameter {key[-1]} has wrong data type. "
                    "Please correct the data in rois.csv "
                    "or correct the data type in data.csv"
                )
            
    if 'pars' in dmr:
        pars = dmr['pars']
        for par in pars.keys():
            if len(par) != 3:
                raise ValueError("Each pars key must be a 3-element tuple")
            if par[-1] not in list(data.keys()):
                raise ValueError(
                    f"pars parameter {par[-1]} not in dmr['data']. "
                    "Please add it to the dictionary."
                )
        for key, value in pars.items():
            if key[-1] not in data:
                raise ValueError(
                    f"pars parameter {key[-1]} not in data. "
                    "Please add it to the dictionary."
                )
            data_type = data[key[-1]][2]
            if data_type == 'str':
                if not isinstance(value, (str, np.str_, np.unicode_)):
                    raise ValueError(
                        f"pars parameter {key[-1]} must be a string. "
                        "Please correct the data in pars.csv "
                        "or correct the data type in data.csv"
                    )
            elif data_type == 'float':
                if not isinstance(value, (float, np.floating, int)):
                    raise ValueError(
                        f"pars parameter {key[-1]} must be a float. "
                        "Please correct the data in pars.csv "
                        "or correct the data type in data.csv"
                    )
            elif data_type == 'bool':
                if not isinstance(value, (bool, np.bool_)):
                    raise ValueError(
                        f"pars parameter {key[-1]} must be a boolean. "
                        "Please correct the data in pars.csv "
                        "or correct the data type in data.csv"
                    )
            elif data_type == 'int':
                if not isinstance(value, (int, np.integer)):
                    raise ValueError(
                        f"pars parameter {key[-1]} must be an integer. "
                        "Please correct the data in pars.csv "
                        "or correct the data type in data.csv"
                    )
            elif data_type == 'complex':
                if not isinstance(value, (complex, np.complexfloating)):
                    raise ValueError(
                        f"pars parameter {key[-1]} must be a complex number. "
                        "Please correct the data in pars.csv"
                        "or correct the data type in data.csv"
                    )
    
    if 'sdev' in dmr:
        if 'pars' not in dmr:
            raise ValueError(
                "dmr['sdev'] should only be provided if dmr['pars'] are also "
                "provided."
            )
        sdev = dmr['sdev']

        if not (sdev.keys() <= pars.keys()):
            raise ValueError(
                'keys in the sdev dictionary must also be in pars.'
            )
        for key, value in sdev.items():
            try:
                float(value)
            except:
                raise ValueError("sdev values must be float.")
            

    # make folder
    if path[-4:] == ".dmr":
        path = path[:-4]
    elif path[-8:] == ".dmr.zip":
        path = path[:-8]

    if not os.path.exists(path):
        os.makedirs(path)


    #
    # Write data dictionary
    #

    # Build rows
    header = ['parameter', 'description', 'unit', 'type']
    if 'columns' in dmr:
        header += dmr['columns']
    rows = [header]
    for key, values in data.items():
        row = [key] + values
        rows.append(row)

    # Write rows to dict.csv
    file = os.path.join(path, "data.csv")
    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    #
    # Write ROI curves
    #

    if 'rois' in dmr:
        
        # Find the longest array length
        max_len = max(len(arr) for arr in rois.values())

        # Prepare CSV data (convert dictionary to column format)
        columns = []

        # First 3 rows: keys (tuple elements)
        for key, values in rois.items():
            data_type = np.dtype(data[key[-1]][2])
            write_values = np.asarray(values).astype(data_type)
            if data_type=='bool':
                write_values = write_values.astype(str)
                write_values[write_values=='True'] = '1'
                write_values[write_values=='False'] = '0'
            col = list(key) + list(write_values) + [""] * (max_len - len(values))  # Pad shorter columns
            columns.append(col)

        # Transpose to get row-wise structure
        rows = list(map(list, zip(*columns)))

        # Write to CSV
        file = os.path.join(path, "rois.csv")
        with open(file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    #
    # Write parameters
    # 

    if 'pars' in dmr:
        rows = [
            ['subject', 'study', 'parameter', 'value'],
        ]
        for key, value in pars.items():
            data_type = data[key[-1]][2]
            if data_type == 'str':
                write_value = value
            elif data_type == 'float':
                write_value = value
            elif data_type == 'bool':
                write_value = '1' if value else '0'
            elif data_type == 'int':
                write_value = value
            elif data_type == 'complex':
                write_value = value
            row = list(key) + [write_value]
            rows.append(row)
        file = os.path.join(path, "pars.csv")
        with open(file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    if 'sdev' in dmr:
        rows = [
            ['subject', 'study', 'parameter', 'value'],
        ]
        for key, value in sdev.items():
            row = list(key) + [value]
            rows.append(row)
        file = os.path.join(path, "sdev.csv")
        with open(file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    # Zip and delete original
    shutil.make_archive(path + ".dmr", "zip", path)
    shutil.rmtree(path)



def read(path:str, format='flat', subject=None, study=None, parameter=None):
    """Read .dmr data from disk.

    Args:
        path (str): Path to .dmr file where the data are 
        saved. The extensions do not need to be included.
        format (str, optional): Formatting of the returned results. 
          The default ('flat') returns a dictionary with a 
          multi-index, meaning values (rois, pars, sdev) are returned 
          as flat dictionaries with a multi-index consisting of 
          (subject, study, parameter). If format='nest', these values 
          are returned as nested dictionaries with 3 levels. If 
          format='table', the values are returned as a list of lists.
          If format is 'pandas' the results are pandas dataframes.  
          Defaults to 'flat'.
        subject (str or list, optional): subject or list of subjects 
          to return. If not provided, all subjects are returned. 
          Defaults to None.
        study (str or list, optional): subject or list of subjects 
          to return. If not provided, all studies are returned. 
          Defaults to None.
        parameter (str or list, optional): parameter or list of 
          parameters to return. If not provided, all parameters are returned. 
          Defaults to None.

    Raises:
        ValueError: If the data on disk are not correctly formatted.

    Returns:
        dict: A dictionary with one item for each of the csv files 
          in the dmr file - keys are either 'data', 'rois', 'pars', 
          'sdev'. The optional key 'columns' is returned as well if
          the data dictionary has optional columns, in which case it 
          lists the names of those extra columns.
    """
    
    if path[-8:] == ".dmr.zip":
        read_path = path
    
    # If the filename is provided with the .dmr extension alone, add the .zip
    elif path[-4:] == ".dmr":
        read_path = path + ".zip"

    # If filename is provided without extensions, add them both
    else:
        read_path = path + ".dmr.zip"


    with zipfile.ZipFile(read_path, "r") as z:
        
        # Check files
        csv_files = [f for f in z.namelist() if f.endswith(".csv")]  
        if 'data.csv' not in csv_files:
            raise ValueError("A .dmr file must contain a data.csv file.")    
        
        
        # Read data dictionary
        data = {}
        with z.open('data.csv') as file:
            text = TextIOWrapper(file, encoding="utf-8")
            reader = csv.reader(text)
            dict_list = list(reader)
            data_headers = dict_list[0]
            for d in dict_list[1:]: 
                if len(d) != len(data_headers):
                    raise ValueError(
                        f"Each data_dict row must have {len(data_headers)} "
                        f"elements {data_headers}. "
                        f"Correct the data dictionary in data.csv"
                    )
                if d[3] not in ['str', 'float', 'bool', 'int', 'complex']:
                    raise ValueError(
                        f"data type {d[3]} is not allowed. Correct "
                        f"the data dictionary in data.csv"
                    )
                data[d[0]] = d[1:]


        if 'pars.csv' in csv_files: 
            pars = {}
            with z.open('pars.csv') as file:
                text = TextIOWrapper(file, encoding="utf-8")
                reader = csv.reader(text)
                pars_list = list(reader)
                pars_list = pars_list[1:] # do not return headers
                for p in pars_list:
                    if len(p) != 4:
                        raise ValueError(
                            f"Error in pars row {p}. "
                            f"Each row must have 4 elements: "
                            f"subject, study, parameter, value. "
                            f"Correct the data in pars.csv"
                        )
                    if p[2] not in data:
                        raise ValueError(
                            f"parameter {p[2]} is not listed in the "
                            f"data dictionary in data.csv"
                        )
                    data_type = data[p[2]][2]
                    if data_type=='str':
                        value = p[3]
                    elif data_type=='float':
                        value = float(p[3])
                    elif data_type=='bool':
                        if p[3]=='1':
                            value = True
                        elif p[3]=='0':
                            value = False
                        else:
                            raise ValueError(
                                f"Boolean value {p[3]} is not allowed. "
                                "Possible values are 1 or 0. "
                                "Correct the data in pars.csv"
                            )
                    elif data_type=='int':
                        value = int(p[3])
                    elif data_type=='complex':
                        value = complex(p[3])
                    pars[tuple(p[:3])] = value

        if 'rois.csv' in csv_files: 
            rois = {}
            with z.open('rois.csv') as file:
                text = TextIOWrapper(file, encoding="utf-8")
                reader = csv.reader(text)
                rois_list = list(reader)
                if len(rois_list)!=0:
                    # Extract headers (first 3 rows)
                    # Transpose first 3 rows to get column-wise headers
                    headers = list(zip(*rois_list[:3]))  
                    # Extract data (from row 3 onward) and convert to NumPy arrays
                    rois = {}
                    for header, col in zip(headers, zip(*rois_list[3:])):
                        if header[2] not in data:
                            raise ValueError(
                                f"roi parameter {header[2]} is not listed in the "
                                f"data dictionary in data.csv. Please update the dictionary."
                            )
                        values = np.array([val for val in col if val])
                        data_type = data[header[2]][2]
                        if data_type == 'bool':
                            rois[header] = values.astype(int).astype(bool)
                        else:
                            rois[header] = values.astype(np.dtype(data_type))

        if 'sdev.csv' in csv_files: 
            if 'pars.csv' not in csv_files:
                raise ValueError(
                    "A file sdev.csv is included in the .dmr file "
                    "without a corresponding pars.csv file. "
                    "Please remove the sdev.csv file or add a "
                    "pars.csv file."
                )
            sdev = {}
            with z.open('sdev.csv') as file:
                text = TextIOWrapper(file, encoding="utf-8")
                reader = csv.reader(text)
                sdev_list = list(reader)
                sdev_list = sdev_list[1:] # do not return headers
                for p in sdev_list:
                    if len(p) != 4:
                        raise ValueError(
                            f"Each sdev row must have 4 elements: "
                            f"subject, study, parameter, sdev. "
                            f"Correct the data in sdev.csv"
                        )
                    if tuple(p[:3]) not in pars:
                        raise ValueError(
                            f"parameter {tuple(p[:3])} has a sdev but "
                            f"no corresponding value in pars.csv."
                        ) 
                    sdev[tuple(p[:3])] = float(p[3])

        # Create dictionary
        dmr = {'data': data}
        if len(data_headers) > 4:
            dmr['columns'] = data_headers[4:]
        if 'pars.csv' in csv_files:
            dmr['pars'] = pars
        if 'rois.csv' in csv_files:
            dmr['rois'] = rois
        if 'sdev.csv' in csv_files:
            dmr['sdev'] = sdev

        # Extract requested fields
        dmr = dict_keep(dmr, subject, study, parameter)

        # Convert to required return format
        dmr = dict_reformat(dmr, format)

    return dmr






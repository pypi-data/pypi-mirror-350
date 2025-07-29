
from __future__ import annotations

import numpy as np
import numbers


def generate_dict_structure(dictionary):
    """
    
    this function create a full dictionnary containing all the structure of an dictionnary in order to save it to an hdf5

    Parameters
    ----------
    
    instance : python dictionary
        a custom dictionary.

    Returns
    -------
    
    list or dict :
        A list or dictionary matching the structure of the python object.
    
    """
    key_data={}
    key_list = list()
    
    for attr,value in dictionary.items():
        
        try:
            if isinstance(value,dict):
                
                subkey_data=generate_dict_structure(value)
                if len(subkey_data)>0:
                    key_data.update({attr:subkey_data})
            
            elif isinstance(value, (list, tuple, np.ndarray, numbers.Number, str)):
                key_list.append(attr)
            
            elif type(value) == "method":
                key_list.append(attr)
            
            else:
                
                subkey_data = generate_object_structure(value)
                if len(subkey_data) > 0:
                    key_data.update({attr: subkey_data})

        except:
            pass
    
    for attr, value in key_data.items():
        key_list.append({attr: value})
    
    return key_list



def generate_object_structure(instance):
    """
    
    this function create a full dictionnary containing all the structure of an object in order to save it to an hdf5

    Parameters
    ----------
    
    instance : object
        a custom python object.

    Returns
    -------
    
    list or dict :
        A list or dictionary matching the structure of the python object.
    
    """
    key_data = {}
    key_list = list()
    return_list = False
    
    for attr in dir(instance):
        
        if not attr.startswith("_") and not attr in ["from_handle", "copy"]:
            
            try:
                value = getattr(instance, attr)
                
                if isinstance(value, (np.ndarray, list, tuple)):

                    if isinstance(value, list):
                        value = np.array(value)

                    if value.dtype == "object" or value.dtype.char == "U":
                        value = value.astype("S")

                    key_list.append(attr)
                    return_list = True
                
                elif isinstance(value, dict):
                    
                    depp_key_data=generate_dict_structure(value)
                    if len(depp_key_data) > 0:
                        key_data.update({attr: depp_key_data})

                elif isinstance(value, numbers.Number):
                    key_list.append(attr)
                    return_list = True

                elif isinstance(value, str):
                    key_list.append(attr)
                    return_list = True

                elif type(value) == "method":
                    key_list.append(attr)
                    return_list = True

                else:
                    
                    depp_key_data = generate_object_structure(value)

                    if len(depp_key_data) > 0:
                        key_data.update({attr: depp_key_data})

            except:
                # raise ValueError("unable to parse attr", attr)
                # print("unable to parse attr", attr, "skip it...")
                pass

    # print(key_data)
    if return_list:
        for attr, value in key_data.items():
            key_list.append({attr: value})

        return key_list

    else:
        return key_data


def read_object_as_dict(instance, recursion_counter=0):
    """
    
    create a dictionary from a custom python object

    Parameters
    ----------
    
    instance : object
        an custom python object

    Return
    ------
    
    key_data: dict
        an dictionary containing all keys and atributes of the object
    
    """
    key_data = {}
    # key_list = list()
    # return_list = False
    recursion_counter = 0
    for attr in dir(instance):
        #print(attr)
        if not attr.startswith("_") and not attr in ["from_handle", "copy"]:
            try:
                value = getattr(instance, attr)
                
                if isinstance(value, (np.ndarray, list, tuple)):
                    
                    if isinstance(value, list):
                        value = np.array(value).astype('U')

                    if value.dtype == "object" or value.dtype.char == "U":
                        value = value.astype("U")
                    
                    key_data.update({attr: value})
                
                elif isinstance(value, dict):
                    key_data.update({attr: value})
                
                elif isinstance(value, numbers.Number):
                    key_data.update({attr: value})

                elif isinstance(value, str):
                    key_data.update({attr: value})

                elif type(value) == "method":
                    next(attr)

                else:
                    
                    depp_key_data = read_object_as_dict(
                        value, recursion_counter=recursion_counter)
                    
                    recursion_counter = recursion_counter+1
                    
                    if len(depp_key_data) > 0:
                        key_data.update({attr: depp_key_data})

                    if recursion_counter > 100:
                        print("recursion counter exxeed the limit of 100... return")
                        return
            except:
                pass

    return key_data

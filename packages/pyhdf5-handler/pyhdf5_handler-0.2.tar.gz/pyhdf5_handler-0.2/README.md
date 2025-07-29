# pyhdf5_handler

# Descritpion

Pyhdf5_handler is a simple python library to quickly read and write hdf5 file storage. This library has been developped by Hydris hydrologie (https://www.hydris-hydrologie.fr/).  
Read and write to hdf5 support main python type:  
- dictionnary  
- list  
- tuple  
- numeric value (int, float)  
- string  
- timestamp (datetime, pandas and numpy)  
- numpy array  
- Structured numpy array  
 
Basically, data are stored in the hdf5 as dataset using numpy array. Thus all input data are stored in a numpy array. If the hdf5 format does not support the type of data, data will be automatically converted to a supported type (byte for string). An attribute, containing the type of the original data, is also created. When reading the hdf5 database, data stored in the dataset are converted back to its original type. If the attribute is not found (for an hdf5 file which has been written by an other librairie), the data will be returned as stored in the hdf5: string and timestamp will be converted to byte sequence but can be decoded using str.decode().

This librairy also provide a way to access "simultaneously" (with different program or threads) to an hdf5 file for reading or writing. 

# Installation

Pyhdf5_handler can be installed using pip:  

```bash
pip install pyhdf5_handler  
```

You can also download the source from https://codeberg.org/maximejay/pyhdf5_handler.  

```bash
git clone https://codeberg.org/maximejay/pyhdf5_handler.git  
pip install ./pyhdf5_handler  
```

# API documentation  

The API documentation can be downloaded at https://codeberg.org/maximejay/pyhdf5_handler/archive/main:html/pyhdf5_handler.zip. This documentation is auto-generated using pdoc (https://pdoc.dev/docs/pdoc.html).  

```bash
pdoc pyhdf5_handler/ -o ./html  
```

# Quick start  

## Create or open an hdf5 database:  

```python
import pyhdf5_handler  
hdf5 = pyhdf5_handler.open_hdf5("./test.hdf5", read_only=False, replace=False)  
```

## Create a new group (like a folder) in this database:  

```python
hdf5 = pyhdf5_handler.add_hdf5_sub_group(hdf5, subgroup="my_group")  
hdf5["my_group"]  
<HDF5 group "/my_group" (0 members)>  
```

## Storing any data in the hdf5 database:  

### Storing basic type such as integer, float, string or None  

```python
pyhdf5_handler.hdf5_dataset_creator(hdf5,"str","str")
pyhdf5_handler.hdf5_dataset_creator(hdf5,"numbers",1.0)
pyhdf5_handler.hdf5_dataset_creator(hdf5,"none",None)  
```

### Storing Timestamp  

Timestamp object will be stored as string with ts.strftime("%Y-%m-%d %H:%M") encoded as utf8.

```python
import numpy as np
import pandas as pd

pyhdf5_handler.hdf5_dataset_creator(hdf5,"timestamp_numpy",np.datetime64('2019-09-22T17:38:30'))
pyhdf5_handler.hdf5_dataset_creator(hdf5,"timestamp_datetime",datetime.datetime.fromisoformat('2019-09-22T17:38:30'))
pyhdf5_handler.hdf5_dataset_creator(hdf5,"timestamp_pandas",pd.Timestamp('2019-09-22T17:38:30'))
```

### Storing list or tuple

```python
import numpy as np
import pandas as pd

pyhdf5_handler.hdf5_dataset_creator(hdf5,"list_num",[1.0,2.0])
pyhdf5_handler.hdf5_dataset_creator(hdf5,"list_str",["a","b"])
pyhdf5_handler.hdf5_dataset_creator(hdf5,"list_mixte",[1.0,"a"])
pyhdf5_handler.hdf5_dataset_creator(hdf5,"list_date_numpy",[np.datetime64('2019-09-22 17:38:30'),np.datetime64('2019-09-22 18:38:30')])
pyhdf5_handler.hdf5_dataset_creator(hdf5,"list_date_datetime",[datetime.datetime.fromisoformat('2019-09-22 17:38:30'),datetime.datetime.fromisoformat('2019-09-22T18:38:30')])
pyhdf5_handler.hdf5_dataset_creator(hdf5,"list_date_pandas",[pd.Timestamp('2019-09-22 17:38:30'),pd.Timestamp('2019-09-22 17:38:30')])
pyhdf5_handler.hdf5_dataset_creator(hdf5,"list_date_range_pandas",pd.date_range(start='1/1/2018', end='1/08/2018'))
```
Remark: List of timestamp will be stored in an numpy array first. When you will read back the data, you will retreive the numpy array but not the orignal list. Thus the data will be string, not timestamp. You will need to convert it yourself. 

### Storing dictionnary

```python
dictionary={"dict":{
               "int":1,
               "float":2.0,
               "none":None,
               "timestamp":pd.Timestamp('2019-09-22 17:38:30'),
               "list":[1,2,3,4],
               "array": np.array([1,2,3,4]),
               "date_range": pd.date_range(start='1/1/2018', end='1/08/2018'),
               "list_mixte":[1.0,np.datetime64('2019-09-22 17:38:30')],
           }
       }

pyhdf5_handler.src.hdf5_handler.dump_dict_to_hdf5(hdf5, dictionary)
```

### handle structured ndarray

Structured ndarray are numpy array which store different type of data. Pyhdf5_handler will treat these numpy data specifically:

```python
import numpy as np
data = [('Alice', 25, 55.0), ('Bob', 32, 60.5)]
dtypes = [('name', 'U10'), ('age', 'i4'), ('weight', 'f4')]
people = np.array(data, dtype=dtypes)

pyhdf5_handler.hdf5_dataset_creator(hdf5,"structured_array",people)
```

## Viewing the content of the hdf5 database

### Using the function hdf5_view

This function provide many option to list groups, attributes and dataset in the hdf5 with recursive search (refer to the api documentation).  

```python
pyhdf5_handler.hdf5_view(hdf5)
```

### Using hdf5_ls

This function will list only dataset on the current group (like h5ls in bash).  
 
```python
pyhdf5_handler.hdf5_ls(hdf5)
```

## Reading the content of the hdf5

The content of an hdf5 object can be imported as a dictionary.

```python
data=pyhdf5_handler.read_hdf5_as_dict(hdf5)
```
If you want to read a specific item you can use hdf5_read_dataset and specify the output dtype:  

```python
pyhdf5_handler.hdf5_read_dataset(hdf5["list_mixte"])
pyhdf5_handler.hdf5_read_dataset(hdf5["str"],str(type("str")))
pyhdf5_handler.hdf5_read_dataset(hdf5["str"],hdf5.attrs["str"])
```

If you don't mind of the output dtype and you prefer to read the content like it is use:

```python
hdf5["list_mixte"][:]
```

## Closing the hdf5 file

Do not forget to close the hdf5 !

```python
hdf5.close()
```

If you get in trouble with your hdf5 file because you forgot to close it, you can try to close all hdf5 file:

```python
pyhdf5_handler.close_all_hdf5_file()
```

## Quickly viewing or reading hdf5file  

Most functions above have have their equivalent function working with the file directly. No need to open and close it manually. pyhdf5_handler will do it for you.

```python
pyhdf5_handler.hdf5file_ls("./test.hdf5")
pyhdf5_handler.hdf5file_ls("./test.hdf5",location="structured_array")

data=pyhdf5_handler.read_hdf5file_as_dict("./test.hdf5")
```

##Getting attributes and dataset

The following functions will read attributes and dataset in the hdf5 database.  

```python
pyhdf5_handler.get_hdf5file_item(path_to_hdf5="./test.hdf5", location="./", item="structured_array", search_attrs=False)
pyhdf5_handler.get_hdf5file_item(path_to_hdf5="./test.hdf5", location="./", item="list_mixte", search_attrs=False)

pyhdf5_handler.get_hdf5file_attribute(path_to_hdf5="./test.hdf5", location="./", attribute="list_num", wait_time=0)
pyhdf5_handler.get_hdf5file_attribute(path_to_hdf5="./test.hdf5", location="./structured_array/ndarray_ds", attribute="name", wait_time=0)
``` 
## Searching attributes and dataset

You can also recursively search attributes and dataset in an hdf5 dataset:  

```python
res=pyhdf5_handler.search_in_hdf5file("./test.hdf5", key="date_range", location="./")
res=pyhdf5_handler.search_in_hdf5file("./test.hdf5", key="structured_array", location="./")
```

## Parallel file access

Hdf5 does not allowed parallel access to file, i.o a programm can't read some data in the hdf5 while another programm is writing in the same hdf5. To workaround this problem, we provide the function parameter wait_time. This parameter used by most of the functions in this librairy. Wait_time is delay in seconds in which pyhdf5_handler will try to access to the file. Default is 0. When this time is elapsed, the function will not open the hdf5 and nothing will be read or written.  
Suppose an external progam, noted external_prog, is writting data in the hdf5 test. This writting will last few seconds, let'say around 10s. You can use the folowing option to read the data:

```python
data=pyhdf5_handler.read_hdf5file_as_dict("./test.hdf5", wait_time=60)
```

In that case pyhdf5_handler will try to access to the hdf5 file during 60 seconds maximum. After 10s, external_prog will have finish its jobs and your script will process normally.
 
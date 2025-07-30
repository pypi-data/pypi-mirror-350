##########
ka_uts_aod
##########

Overview
********

.. start short_desc

**Utilities to manage Arrays of Dictionaries**

.. end short_desc

Installation
************

.. start installation

Package ``ka_uts_aod`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: shell

	$ python -m pip install ka_uts_aod

To install with ``conda``:

.. code-block:: shell

	$ conda install -c conda-forge ka_uts_aod

.. end installation

Package logging 
***************

(c.f.: **Appendix**: `Package Logging`)

Package files
*************

Classification
==============

The Package ``ka_uts_aod`` consist of the following file types (c.f.: **Appendix**):

#. **Special files:** (c.f.: **Appendix:** *Special python package files*)

#. **Dunder modules:** (c.f.: **Appendix:** *Special python package modules*)

#. **Modules**

   a. *aod.py*
   #. *aodpath.py*

Modules
*******

Module: aod.py
==============

The Module ``aod.py`` contains only the static class ``AoD``.

Class: AoD
----------

The Class ``AoD`` contains the following methods:

AoD Methods
^^^^^^^^^^^

  .. AoD-Methods-label:
  .. table:: *AoD Methods*

   +------------------------------------+----------------------------------------------+
   |Name                                |Short description                             |
   +====================================+==============================================+
   |add                                 |Add object to array of dictionaries.          |
   +------------------------------------+----------------------------------------------+
   |apply_function                      |Apply function to array of dictionaries       |
   +------------------------------------+----------------------------------------------+
   |csv_dictwriterows                   |Write array of dictionaries to csv file       |
   |                                    |with function dictwriterows.                  |
   +------------------------------------+----------------------------------------------+
   |dic_found_with_empty_value          |Return True or raise an exception if the arr. |
   |                                    |of dicts. contains a dict. with empty value   |
   |                                    |and the execption switch is True.             |
   +------------------------------------+----------------------------------------------+
   |extend_if_not_empty                 |Extend array of dicts. with non empty dict.   |
   +------------------------------------+----------------------------------------------+
   |join_aod                            |Join elements of array of dicts.              |
   +------------------------------------+----------------------------------------------+
   |merge_dic                           |Merge elements of array of dicts.             |
   +------------------------------------+----------------------------------------------+
   |nvl                                 |Replace empty array of dicts.                 |
   +------------------------------------+----------------------------------------------+
   |pd_to_csv                           |Write array of dicts. to csv file with pandas.|
   +------------------------------------+----------------------------------------------+
   |pl_to_csv                           |Write array of dicts. to csv file with polars.|
   +------------------------------------+----------------------------------------------+
   |put                                 |Write transformed array of dicts. to a csv    |
   |                                    |file with a selected I/O function.            |
   +------------------------------------+----------------------------------------------+
   |sh_doaod_split_by_value_is_not_empty|Converted array of dicts. to array of arrays  |
   |                                    |dict. by using conditional split              |
   +------------------------------------+----------------------------------------------+
   |sh_dod                              |Convert array of dicts. to dict. of dicts.    |
   +------------------------------------+----------------------------------------------+
   |sh_key_value_found                  |Show True if an element exists in the array of|
   |                                    |dicts. which contains the key, value pair     |
   +------------------------------------+----------------------------------------------+
   |sh_unique                           |Deduplicate arr.  of dicts.                   |
   +------------------------------------+----------------------------------------------+
   |split_by_value_is_not_empty         |Split arr. of dicts. by the condition "the    |
   |                                    |given key value is not empty".                |
   +------------------------------------+----------------------------------------------+
   |to_aoa                              |Convert array of dictionaries to array of     |
   |                                    |arrays controlled by key- and value-switch.   |
   +------------------------------------+----------------------------------------------+
   |to_aoa of_keys_values               |Convert arr. of dicts. to arr. of arrays usin |
   |                                    |keys of any dict. and values of all dict.     |
   +------------------------------------+----------------------------------------------+
   |to_aoa of_values                    |Convert arr. of dicts. to arr. of arrays      |
   |                                    |using values of all dict.                     |
   +------------------------------------+----------------------------------------------+
   |to_aoa of_key_values                |Convert array of dicts. to array using dict.  |
   |                                    |values with given key.                        |
   +------------------------------------+----------------------------------------------+
   |to_doaod_by_key                     |Convert array of dics. to dict. of arrays of  |
   |                                    |dicts. using a key.                           |
   +------------------------------------+----------------------------------------------+
   |to_dic_by_key                       |Convert array of dicts. to dict. of dicts     |
   |                                    |using a key                                   |
   +------------------------------------+----------------------------------------------+
   |to_dic_by_lc_keys                   |Convert array of dicts. to dict. of arrays    |
   |                                    |using 2 lowercase keys.                       |
   +------------------------------------+----------------------------------------------+
   |to_unique_by_key                    |Convert array of dicts. to array of dicts by  |
   +------------------------------------+----------------------------------------------+
   |sh_unique                           |by selecting dictionaries with ke.            |
   +------------------------------------+----------------------------------------------+
   |write_xlsx_wb                       |Write array of dicts. to xlsx workbook.       |
   +------------------------------------+----------------------------------------------+

AoD Method: add
^^^^^^^^^^^^^^^

Description
"""""""""""

Add object to array of dictionaries.

#. If the objects is a dictionary:

   * the object is appended to the array of dictionaries
  
#. If the objects is an array of dictionaries:

   * the object extends the array of dictionaries

Parameter
"""""""""

  .. AoD-Method-add-Parameter-label:
  .. table:: *AoD-Method-add-Parameter*

   +----+-----+-------+---------------------+
   |Name|Type |Default|Description          |
   +====+=====+=======+=====================+
   |aod |TyAoD|       |Array of dictionaries|
   +----+-----+-------+---------------------+
   |obj |TyAny|       |Object               |
   +----+-----+-------+---------------------+

Return Value
""""""""""""

  .. AoD-Method-add-Return-Value-label:
  .. table:: *AoD Method-add: Return Value*

   +----+----+---------------------+
   |Name|Type|Description          |
   +====+====+=====================+
   |    |None|                     |
   +----+----+---------------------+

AoD Method: apply_function
^^^^^^^^^^^^^^^^^^^^^^^^^^

Description
"""""""""""

Create a new array of dictionaries by applying the function to each element
of the array of dictionaries.

Parameter
"""""""""

  .. AoD-Method-apply_function-Parameter-label:
  .. table:: *AoD Method apply_function: Parameter*

   +------+-------+---------------------+
   |Name  |Type   |Description          |
   +======+=======+=====================+
   |aod   |TyAoD  |Array of dictionaries|
   +------+-------+---------------------+
   |fnc   |TN_Call|Object               |
   +------+-------+---------------------+
   |kwargs|TN_Dic |Keyword arguments    |
   +------+-------+---------------------+

Return Value
""""""""""""

  .. AoD-Method-apply_function-Return-Value-label:
  .. table:: *AoD Method apply_function: Return Value*

   +-------+-----+-------------------------+
   |Name   |Type |Description              |
   +=======+=====+=========================+
   |aod_new|TyAoD|new array of dictionaries|
   +-------+-----+-------------------------+

AoD Method: csv_dictwriterows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^          

Description
"""""""""""

Write given array of dictionaries (1.argument) to a csv file with the given path
name (2.argument) using the function "dictwriter" of the builtin path module "csv"

Parameter
"""""""""

  .. AoD-Method-csv_dictwriterows-Parameter-label:
  .. table:: *AoD Method csv_dictwriterows: Parameter*

   +----+------+---------------------+
   |Name|Type  |Description          |
   +====+======+=====================+
   |aod |TyAoD |Array of dictionaries|
   +----+------+---------------------+
   |path|TyPath|Path                 |
   +----+------+---------------------+
   
Return Value
""""""""""""

  .. AoD-Method-csv_dictwriterows-Return-Value-label:
  .. table:: *AoD Method csv_dictwriterows: Return Value*


   +----+------+---------------------+
   |Name|Type  |Description          |
   +====+======+=====================+
   |    |None  |                     |
   +----+------+---------------------+
   
AoD Method: dic_found_with_empty_value
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^       
   
Description
"""""""""""

#. Set the switch sw_found to True if a dictionary with an empty value for the key is found
   in the given array of dictionaries (1.argument). 

#. If the Argument "sw_raise" is True and the switch "sw_found" is True, then an Exception is raised,
   otherwise the value of "sw_found" is returned.                  

Parameter
"""""""""

  .. AoD-Method-csv_dic_found_with_empty_value-Parameter-label:
  .. table:: *AoD Method csv_dictwriterows: Parameter*

   +--------+------+-------+---------------------+
   |Name    |Type  |Default|Description          |
   +========+======+=======+=====================+
   |aod     |TyAoD |       |array of dictionaries|
   +--------+------+-------+---------------------+
   |key     |TyStr |       |Key                  |
   +--------+------+-------+---------------------+
   |sw_raise|TyBool|False  |                     |
   +--------+------+-------+---------------------+

Return Value
""""""""""""

  .. AoD-Method-dic_found_with_empty_value-Return-Value-label:
  .. table:: *AoD Method csv_dictwriterows: Return Value*

   +--------+------+----------------------------+
   |Name    |Type  |Description                 |
   +========+======+============================+
   |sw_found|TyBool|key is found in a dictionary|
   +--------+------+----------------------------+
   
AoD Method: extend_if_not_empty
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
Description
"""""""""""

#. Apply the given function (4.argument) to the value of the given dictionary (2.argument) for
   the key (3.argument).

#. The result is used to extend the given array of dictionaries (1.argument).

Parameter
"""""""""

  .. AoD-Method-extend_if_not_empty-Parameter-label:
  .. table:: *AoD Method extend_if_not_empty: Parameter*

   +--------+------+-------+---------------------+
   |Name    |Type  |Default|Description          |
   +========+======+=======+=====================+
   |aod     |TyAoD |       |Array of dictionaries|
   +--------+------+-------+---------------------+
   |dic     |TyDic |       |Dictionary           |
   +--------+------+-------+---------------------+
   |key     |TN_Any|       |Key                  |
   +--------+------+-------+---------------------+
   |function|TyCall|       |Function             |
   +--------+------+-------+---------------------+
   
Return Value
""""""""""""

  .. AoD-Method-extend_if_not_empty-Return-Value-label:
  .. table:: *AoD Method extend_if_not_empty: Return Value*

   +-------+-----+-------------------------+
   |Name   |Type |Description              |
   +=======+=====+=========================+
   |aod_new|TyAoD|New array of dictionaries|
   +-------+-----+-------------------------+
   
AoD Method: join_aod
^^^^^^^^^^^^^^^^^^^^
  
Description
"""""""""""

join 2 arrays of dictionaries

Parameter
"""""""""

  .. AoD-Method-join_aod-Parameter-label:
  .. table:: *AoD Method join_aod: Parameter*

   +----+-----+-------+----------------------------+
   |Name|Type |Default|Description                 |
   +====+=====+=======+============================+
   |aod0|TyAoD|       |First array of dictionaries |
   +----+-----+-------+----------------------------+
   |aod1|TyAoD|       |Second array of dictionaries|
   +----+-----+-------+----------------------------+
   
Return Value
""""""""""""

  .. AoD-Method-join_aod-Return-Value-label:
  .. table:: *AoD Method join_aod: Return Value*

   +-------+-----+-------------------------+
   |Name   |Type |Description              |
   +=======+=====+=========================+
   |aod_new|TyAoD|New array of dictionaries|
   +-------+-----+-------------------------+
   
AoD Method: merge_dic
^^^^^^^^^^^^^^^^^^^^^
   
Description
"""""""""""

Merge array of dictionaries (1.argument) with the dictionary (2.argument).

#. Each element of the new array of dictionaries is created by merging an element
   of the given array of dictionaries with the given dictionary.
   
Parameter
"""""""""

  .. AoD-Method-merge_dic-Parameter-label:
  .. table:: *AoD Method merge_dic: Parameter*

   +----+------+-------+---------------------+
   |Name|Type  |Default|Description          |
   +====+======+=======+=====================+
   |aod |TN_AoD|       |Array of dictionaries|
   +----+------+-------+---------------------+
   |dic |TN_Dic|       |Dictionary           |
   +----+------+-------+---------------------+
   
Return Value
""""""""""""

  .. AoD-Method-merge_dic-Return-Value-label:
  .. table:: *AoD Method merge_dic: Return Value*

   +-------+-----+-------------------------+
   |Name   |Type |Description              |
   +=======+=====+=========================+
   |aod_new|TyAoD|New array of dictionaries|
   +-------+-----+-------------------------+
   
AoD Method: nvl
^^^^^^^^^^^^^^^
   
Description
"""""""""""

Replace a none value of the first argument with the emty array. 

Parameter
"""""""""

  .. AoD-Method-nvl-Parameter-label:
  .. table:: *AoD Method nvl: Parameter*

   +----+------+-------+---------------------+
   |Name|Type  |Default|Description          |
   +====+======+=======+=====================+
   |aod |TN_AoD|       |Array of dictionaries|
   +----+------+-------+---------------------+
   
Return Value
""""""""""""

  .. AoD-Method-nvl-Return-Value-label:
  .. table:: *AoD Method nvl: Return Value*

   +-------+-----+-------------------------+
   |Name   |Type |Description              |
   +=======+=====+=========================+
   |aod_new|TyArr|New array of dictionaries|
   +-------+-----+-------------------------+
   
AoD Method: pd_to_csv
^^^^^^^^^^^^^^^^^^^^^
   
Description
"""""""""""

#. Convert the given array of dictionaries (1.argument) to a panda dataframe using the panda function "from_dict".

#. Write the result to a csv file with the given path name (2.argument using the panda function "to_csv".

Parameter
"""""""""

  .. AoD-Method-pd_to_csv-Parameter-label:
  .. table:: *AoD Method pd_to_csv: Parameter*

   +------+------+-------+---------------------+
   |Name  |Type  |Default|Description          |
   +======+======+=======+=====================+
   |aod   |TyAoD |       |Array of dictionaries|
   +------+------+-------+---------------------+
   |path  |TyPath|       |Csv file psth        |
   +------+------+-------+---------------------+
   |fnc_pd|TyCall|       |Panda function       |
   +------+------+-------+---------------------+
   
AoD Method: pl_to_csv
^^^^^^^^^^^^^^^^^^^^^
   
Description
"""""""""""

#. Convert the given array of dictionaries (1.argument) to a panda dataframe with the panda function "from_dict". 

#. Convert the result to a polars dataframe using the polars function "to_pandas".
  
#. Apply the given function (3. argument) to the polars dataframe.
  
#. Write the result to a csv file with the given name (2.argument) using the polars function "to_csv".

Parameter
"""""""""

  .. AoD-Method-pl_to_csv-Parameter-label:
  .. table:: *AoD Method pl_to_csv: Parameter*

   +------+------+-------+---------------------+
   |Name  |Type  |Default|Description          |
   +======+======+=======+=====================+
   |aod   |TyAoD |       |Array of dictionaries|
   +------+------+-------+---------------------+
   |path  |TyPath|       |Csv file path        |
   +------+------+-------+---------------------+
   |fnc_pd|TyCall|       |Polars function      |
   +------+------+-------+---------------------+
   
Return Value
""""""""""""

  .. AoD-Method-pl_to_csv-Return-Value-label:
  .. table:: *AoD Method pl_to_csv: Return Value*

   +----+----+---------------------+
   |Name|Type|Description          |
   +====+====+=====================+
   |    |None|                     |
   +----+----+---------------------+
   
AoD Method: put
^^^^^^^^^^^^^^^
   
Description
"""""""""""

#. Transform array of dictionaries (1.argument) with a transformer function (3.argument)

#. If the I/O function is defined for the given dataframe type (4.argument).

   #. write result to a csv file with the given path name (2.argument).

Parameter
"""""""""

  .. AoD-Method-put-Parameter-label:
  .. table:: *AoD Method put: Parameter*

   +-------+------+-------+---------------------+
   |Name   |Type  |Default|Description          |
   +=======+======+=======+=====================+
   |aod    |TyAoD |       |Array of dictionaries|
   +-------+------+-------+---------------------+
   |path   |TyPath|       |Csv file path        |
   +-------+------+-------+---------------------+
   |fnc_aod|TyAoD |       |AoD function         |
   +-------+------+-------+---------------------+
   |df_type|TyStr |       |Dataframe type       |
   +-------+------+-------+---------------------+
   
Return Value
""""""""""""

  .. AoD-Method-put-Return-Value-label:
  .. table:: *AoD Method put: Return Value*

   +----+----+--------------------+
   |Name|Type|Description         |
   +====+====+====================+
   |    |None|                    |
   +----+----+--------------------+
   
AoD Method: sh_doaod_split_by_value_is_not_empty
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
Description
"""""""""""

#. Create 2-dimensional dict. of array of dictionaries from given array of dict. (1.argument)
and key (2.argument) to split the array of dictionaries into 2 array of dictionaries by
the two conditions

   #. "the key is contained in the dictionary and the value empty".

   #. "the key is contained in the dictionary and the value is not empty".

#. The first array of dictionaries is created by the condition and is assigned to 
   the new dictionary of array of dictionaries using the given key (3.argument).

#. The second array of dictionaries is created by the negation of the condition 
   and is assigned to the new dictionary of array of dictionaries using the given
   key (4.argument).

Parameter
"""""""""

  .. AoD-Method-sh_doaod_split_by_value_is_not_empty-Parameter-label:
  .. table:: *AoD Method sh_doaod_split_by_value_is_not_empty: Parameter*

   +-----+-----+-------+--------------------------------------+
   |Name |Type |Default|Description                           |
   +=====+=====+=======+======================================+
   |aod  |TyAoD|       |Array of dictionaries                 |
   +-----+-----+-------+--------------------------------------+
   |key  |Any  |       |Key                                   |
   +-----+-----+-------+--------------------------------------+
   |key_n|Any  |       |key of the array of dictionaries      |
   |     |     |       |wich satisfies the condition.         |
   +-----+-----+-------+--------------------------------------+
   |key_y|Any  |       |key of the array of dictionaries which|
   |     |     |       |does not satisfies the condition.     |
   +-----+-----+-------+--------------------------------------+
   
  .. AoD-Method-sh_doaod_split_by_value_is_not_empty-Return-Value-label:
  .. table:: *AoD Method sh_doaod_split_by_value_is_not_empty: Return Value*

   +-----+-------+-----------------------------------+
   |Name |Type   |Description                        |
   +=====+=======+===================================+
   |doaod|TyDoAoD|Dictionary of array of dictionaries|
   +-----+-------+-----------------------------------+
   
AoD Method: sh_dod
^^^^^^^^^^^^^^^^^^
   
Description
"""""""""""

Create dictionary of dicionaries from the array of dictionaries (1.argument) and the key (2.argument).       

Parameter
"""""""""

  .. AoD-Method-sh_dod-Parameter-label:
  .. table:: *AoD Method sh_dod: Parameter*

   +----+-----+-------+---------------------+
   |Name|Type |Default|Description          |
   +====+=====+=======+=====================+
   |aod |TyAoD|       |Array of dictionaries|
   +----+-----+-------+---------------------+
   |key |Any  |       |Key                  |
   +----+-----+-------+---------------------+
   
Return Value
""""""""""""

  .. AoD-Method-sh_dod-Return-Value-label:
  .. table:: *AoD Method sh_dod: Return Value*

   +----+-----+--------------------------+
   |Name|Type |Description               |
   +====+=====+==========================+
   |dod |TyDoD|Dictionary of dictionaries|
   +----+-----+--------------------------+
   
AoD Method: sh_unique
^^^^^^^^^^^^^^^^^^^^^

Description
"""""""""""

Deduplicate array of dictionaries (1.argument).
   
Parameter
"""""""""

  .. AoD-Method-sh_unique-Parameter-label:
  .. table:: *AoD Method sh_unique: Parameter*

   +----+-----+-------+---------------------+
   |Name|Type |Default|Description          |
   +====+=====+=======+=====================+
   |aod |TyAoD|       |Array of dictionaries|
   +----+-----+-------+---------------------+
   |key |Any  |       |Key                  |
   +----+-----+-------+---------------------+
   
Return Value
""""""""""""

  .. AoD-Method-sh_unique-Return-Value-label:
  .. table:: *AoD Method sh_unique: Return Value*

   +-------+-----+-------------------------+
   |Name   |Type |Description              |
   +=======+=====+=========================+
   |aod_new|TyAoD|New array of dictionaties|
   +-------+-----+-------------------------+
   
AoD Method: split_by_value_is_not_empty
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^      
   
Description
"""""""""""

Split the given array of dictionary into 2 arrays of dictionary by the condition 
"the key is contained in the dictionary and the value is not empty"

Parameter
"""""""""

  .. AoD-Method-split_by_value_is_not_empty-Parameter-label:
  .. table:: *AoD Method split_by_value_is_not_empty: Parameter*

   +----+-----+-------+---------------------+
   |Name|Type |Default|Description          |
   +====+=====+=======+=====================+
   |aod |TyAoD|       |array of dictionaries|
   +----+-----+-------+---------------------+
   |key |Any. |       |Key                  |
   +----+-----+-------+---------------------+
   
Return Value
""""""""""""

  .. AoD-Method-split_by_value_is_not_empty-Return-Value-label:
  .. table:: *AoD Method split_by_value_is_not_empty: Return Value*

   +--------------+--------+---------------------------------+
   |Name          |Type    |Description                      |
   +==============+========+=================================+
   |(aod_n, aod_y)|Ty2ToAoD|Tuple of 2 arrays of dictionaries|
   +--------------+--------+---------------------------------+
   
AoD Method: sw_key_value_found
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
Description
"""""""""""

Set the condition to True if:

* the key is contained in a dictionary of the array of dictionaries and

* the key value is not empty"

Parameter
"""""""""

  .. AoD-Method-sw_key_value_found-Parameter-label:
  .. table:: *AoD Method sw_key_value_found: Parameter*

   +----+-----+-------+---------------------+
   |Name|Type |Default|Description          |
   +====+=====+=======+=====================+
   |aod |TyAoD|       |Array of dictionaries|
   +----+-----+-------+---------------------+
   |key |Any  |       |Key                  |
   +----+-----+-------+---------------------+
   
Return Value
""""""""""""

  .. AoD-Method-sw_key_value_found-Return-Value-label:
  .. table:: *AoD Method sw_key_value_found: Return Value*

   +----+------+-------+--------------------------------+
   |Name|Type  |Default|Description                     |
   +====+======+=======+================================+
   |sw  |TyBool|       |key is contained in a dictionary|
   |    |      |       |of the array of dictionaries    |
   +----+------+-------+--------------------------------+
   
AoD Method: to_aoa
^^^^^^^^^^^^^^^^^^
   
Description
"""""""""""

Create array of arrays from given array of dictionaries (1.argument).

#. If switch sw_keys (2.argument) is True:

   Create the first element of the array of arrays as the list of dict. keys of the
   first elements of the array of dictionaries.

#. If the switch sw_values (3. argument) is True:

   Create the other elemens of the array of dictionries as list of dict. values of the
   elements of the array of dictionaries.

Parameter
"""""""""

  .. AoD-Method-to_aoa-Parameter-label:
  .. table:: *AoD Method to_aoa: Parameter*

   +---------+------+-------+---------------------+
   |Name     |Type  |Default|Description          |
   +=========+======+=======+=====================+
   |aod      |TyAoD |       |array of dictionaries|
   +---------+------+-------+---------------------+
   |sw_keys  |TyBool|       |keys switch          |
   +---------+------+-------+---------------------+
   |sw_values|TyBool|       |values switch        |
   +---------+------+-------+---------------------+
   
Return Value
""""""""""""

  .. AoD-Method-to_aoa-Return-Value-label:
  .. table:: *AoD Method to_aoa: Return Value*

   +----+-----+---------------+
   |Name|Type |Description    |
   +====+=====+===============+
   |aoa |TyAoA|array of arrays|
   +----+-----+---------------+
   
AoD Method: to_aoa of_key_values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
Description
"""""""""""

Convert the given array of dictionary (1.argument) into an array of arrays.
#. Create first element of the new array of arrays as the keys-list of the first dictionary.
#. Create other elements as the values-lists of the dictionaries of the array of dictionaries.

Parameter
"""""""""

  .. AoD-Method-to_aoa of_key_values-Parameter-label:
  .. table:: *AoD Method to_aoa of_key_values: Parameter*

   +----+-----+--------+---------------------+
   |Name|Type |Default |Description          |
   +====+=====+========+=====================+
   |aod |TyAoD|        |Array of dictionaries|
   +----+-----+--------+---------------------+
   
Return Value
""""""""""""

  .. AoD-Method-to_aoa of_key_values-Return-Value-label:
  .. table:: *AoD Method to_aoa of_key_values: Return Value*

   +----+-----+---------------+
   |Name|Type |Description    |
   +====+=====+===============+
   |aoa |TyAoA|Array of arrays|
   +----+-----+---------------+
   
AoD Method: to_aoa_of_values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  
Description
"""""""""""

Convert the given array of dictionaries (1.argument) into an array of arrays.
The elements of the new array of arrays are the values-lists of the dictionaries
of the array of dictionaries.

Parameter
"""""""""

  .. AoD-Method-to_aoa_of_values-Parameter-label:
  .. table:: *AoD Method to_aoa_of_values: Parameter*

   +----+-----+--------+---------------------+
   |Name|Type |Default |Description          |
   +====+=====+========+=====================+
   |aod |TyAoD|        |Array of dictionaries|
   +----+-----+--------+---------------------+
   
Return Value
""""""""""""

  .. AoD-Method-to_aoa_of_values-Return-Value-label:
  .. table:: *AoD Method to_aoa_of_values: Return Value*

   +----+-----+--------+---------------+
   |Name|Type |Default |Description    |
   +====+=====+========+===============+
   |aoa |TyAoA|        |Array of arrays|
   +----+-----+--------+---------------+
   
AoD Method: to_arr of_key_values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
Description
"""""""""""

Convert the given array of dictionaries (1.argument) to an array. The elements of the new
array are the selected values of each dictionary of the array of dictionaries with the 
given key (2.argument).

Parameter
"""""""""

  .. AoD-Method-to_arr of_key_values-Parameter-label:
  .. table:: *AoD Method to_arr of_key_values: Parameter*

   +----+-----+--------+---------------------+
   |Name|Type |Default |Description          |
   +====+=====+========+=====================+
   |aod |TyAoD|        |Array of dictionaries|
   +----+-----+--------+---------------------+
   |key |Any  |        |Key                  |
   +----+-----+--------+---------------------+
   
Return Value
""""""""""""

  .. AoD-Method-to_arr of_key_values-Return-Value-label:
  .. table:: *AoD Method to_arr of_key_values: Return Value*

   +----+-----+-----------+
   |Name|Type |Description|
   +====+=====+===========+
   |arr |TyAoD|New array  |
   +----+-----+-----------+
   
AoD Method: to_doaod_by_key
^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
Parameter
"""""""""

  .. AoD-Method-to_doaod_by_key-Parameter-label:
  .. table:: *AoD Method to_doaod_by_key: Parameter*

   +----+-----+-------+---------------------+
   |Name|Type |Default|Description          |
   +====+=====+=======+=====================+
   |aod |TyAoD|       |Array of dictionaries|
   +----+-----+-------+---------------------+
   |key |Any  |       |Key                  |
   +----+-----+-------+---------------------+
   
Return Value
""""""""""""

  .. AoD-Method-to_doaod_by_key-Return-Value-label:
  .. table:: *AoD Method to_doaod_by_key: Return Value*

   +-----+-----+-----------------------------------+
   |Name |Type |Description                        |
   +=====+=====+===================================+
   |doaod|TyAoD|Dictionary of array of dictionaries|
   +-----+-----+-----------------------------------+
   
AoD Method: to_dod_by_key
^^^^^^^^^^^^^^^^^^^^^^^^^
   
Parameter
"""""""""

  .. AoD-Method-to_dod_by_key-Parameter-label:
  .. table:: *AoD Method to_dod_by_key: Parameter*

   +----+-----+-------+-------------+
   |Name|Type |Default|Description  |
   +====+=====+=======+=============+
   |aod |TyAoD|       |             |
   +----+-----+-------+-------------+
   |key |Any  |       |             |
   +----+-----+-------+-------------+
   
Return Value
""""""""""""

  .. AoD-Method-to_dod_by_key-Return-Value-label:
  .. table:: *AoD Method to_dod_by_key: Return Value*

   +----+-----+-------------+
   |Name|Type |Description  |
   +====+=====+=============+
   |dic |TyDic|             |
   +----+-----+-------------+
   
   
AoD Method: to_doa_by_lc_keys
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
Parameter
"""""""""

  .. AoD-Method-to_doa_by_lc_keys-Parameter-label:
  .. table:: *AoD Method to_doa_by_lc_keys: Parameter*

   +----+-----+-------+-------------+
   |Name|Type |Default|Description  |
   +====+=====+=======+=============+
   |aod |TyAoD|       |             |
   +----+-----+-------+-------------+
   |key |Any  |       |             |
   +----+-----+-------+-------------+
   
Return Value
""""""""""""

  .. AoD-Method-to_doa_by_lc_keys-Return-Value-label:
  .. table:: *AoD Method to_doa_by_lc_keys: Return Value*

   +----+-----+-------------+
   |Name|Type |Description  |
   +====+=====+=============+
   |doa |TyDoA|             |
   +----+-----+-------------+
   
AoD method: to_unique_by_key
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
Parameter
"""""""""

  .. AoD-Method-to_unique_by_key-Parameter-label:
  .. table:: *AoD Method to_unique_by_key: Parameter*

   +----+-----+-------+-------------+
   |Name|Type |Default|Description  |
   +====+=====+=======+=============+
   |aod |TyAoD|       |             |
   +----+-----+-------+-------------+
   |key |Any  |       |             |
   +----+-----+-------+-------------+
   
Return Value
""""""""""""

  .. AoD-Method-to_unique_by_key-Return-Value-label:
  .. table:: *AoD Method csv_dictwriterows: Return Value*

   +-------+-----+-------+-------------+
   |Name   |Type |Default|Description  |
   +=======+=====+=======+=============+
   |aod_new|TyAoD|       |             |
   +-------+-----+-------+-------------+
   
AoD method: write_xlsx_wb
^^^^^^^^^^^^^^^^^^^^^^^^^
   
Parameter
"""""""""

  .. AoD-Method-write_xlsx_wb-Parameter-label:
  .. table:: *AoD Method write_xlsx_wb: Parameter*

   +----+-----+-------+---------------------+
   |Name|Type |Default|Description          |
   +====+=====+=======+=====================+
   |aod |TyAoD|       |array of dictionaries|
   +----+-----+-------+---------------------+
   
Return Value
""""""""""""

  .. AoD-Method-write_xlsx_wb-Return-Value-label:
  .. table:: *AoD Method write_xlsx_wb: Return Value*

   +----+-----+-----------+
   |Name|Type |Description|
   +====+=====+===========+
   |    |None |           |
   +----+-----+-----------+
   
Module: aodpath.py
==================

The Module ``aodpath.py`` contains only the static class ``AoDPath``;

Class: AoDPath
--------------

AoDPath Methods
^^^^^^^^^^^^^^^

  .. AoDPath-methods-label:
  .. table:: *AoPath methods*

   +---------+----------------------------------------------+
   |Name     |short Description                             |
   +=========+==============================================+
   |sh_aopath|Show array of paths for array of dictionaries.|
   +---------+----------------------------------------------+

AoDPath Method: sh_a_path
^^^^^^^^^^^^^^^^^^^^^^^^^

Convert Array of Path-Disctionaries to Array of Paths.

Parameter
"""""""""

  .. AoD-Method-sh_aopath-Parameter-label:
  .. table:: *AoD Method sh_aopath: Parameter*

   +----+-----+-------+---------------------------+
   |Name|Type |Default|Description                |
   +====+=====+=======+===========================+
   |aod |TyAoD|       |Array of Path-Dictionaries.|
   +----+-----+-------+---------------------------+
   
Return Value
""""""""""""

  .. AoD-Method-sh_aopath-Return-Value-label:
  .. table:: *AoD Method sh_aopath: Return Value*

   +----+--------+--------------+
   |Name|Type    |Description   |
   +====+========+==============+
   |    |TyAoPath|Array of paths|
   +----+--------+--------------+
   
Appendix
********

Package Logging
===============

Description
-----------

The Standard or user specifig logging is carried out by the log.py module of the logging
package ka_uts_log using the configuration files **ka_std_log.yml** or **ka_usr_log.yml**
in the configuration directory **cfg** of the logging package **ka_uts_log**.
The Logging configuration of the logging package could be overriden by yaml files with
the same names in the configuration directory **cfg** of the application packages.

Log message types
-----------------

Logging defines log file path names for the following log message types: .

#. *debug*
#. *info*
#. *warning*
#. *error*
#. *critical*

Application parameter for logging
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  .. Application-parameter-used-in-log-naming-label:
  .. table:: *Application parameter used in log naming*

   +-----------------+---------------------------+----------+------------+
   |Name             |Decription                 |Values    |Example     |
   +=================+===========================+==========+============+
   |dir_dat          |Application data directory |          |/otev/data  |
   +-----------------+---------------------------+----------+------------+
   |tenant           |Application tenant name    |          |UMH         |
   +-----------------+---------------------------+----------+------------+
   |package          |Application package name   |          |otev_xls_srr|
   +-----------------+---------------------------+----------+------------+
   |cmd              |Application command        |          |evupreg     |
   +-----------------+---------------------------+----------+------------+
   |pid              |Process ID                 |          |æevupreg    |
   +-----------------+---------------------------+----------+------------+
   |log_ts_type      |Timestamp type used in     |ts,       |ts          |
   |                 |logging files|ts, dt       |dt        |            |
   +-----------------+---------------------------+----------+------------+
   |log_sw_single_dir|Enable single log directory|True,     |True        |
   |                 |or multiple log directories|False     |            |
   +-----------------+---------------------------+----------+------------+

Log type and Log directories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Single or multiple Application log directories can be used for each message type:

  .. Log-types-and-Log-directories-label:
  .. table:: *Log types and directoriesg*

   +--------------+---------------+
   |Log type      |Log directory  |
   +--------+-----+--------+------+
   |long    |short|multiple|single|
   +========+=====+========+======+
   |debug   |dbqs |dbqs    |logs  |
   +--------+-----+--------+------+
   |info    |infs |infs    |logs  |
   +--------+-----+--------+------+
   |warning |wrns |wrns    |logs  |
   +--------+-----+--------+------+
   |error   |errs |errs    |logs  |
   +--------+-----+--------+------+
   |critical|crts |crts    |logs  |
   +--------+-----+--------+------+

Log files naming
^^^^^^^^^^^^^^^^

Naming Conventions
""""""""""""""""""

  .. Naming-conventions-for-logging-file-paths-label:
  .. table:: *Naming conventions for logging file paths*

   +--------+-------------------------------------------------------+-------------------------+
   |Type    |Directory                                              |File                     |
   +========+=======================================================+=========================+
   |debug   |/<dir_dat>/<tenant>/RUN/<package>/<cmd>/<Log directory>|<Log type>_<ts>_<pid>.log|
   +--------+-------------------------------------------------------+-------------------------+
   |info    |/<dir_dat>/<tenant>/RUN/<package>/<cmd>/<Log directory>|<Log type>_<ts>_<pid>.log|
   +--------+-------------------------------------------------------+-------------------------+
   |warning |/<dir_dat>/<tenant>/RUN/<package>/<cmd>/<Log directory>|<Log type>_<ts>_<pid>.log|
   +--------+-------------------------------------------------------+-------------------------+
   |error   |/<dir_dat>/<tenant>/RUN/<package>/<cmd>/<Log directory>|<Log type>_<ts>_<pid>.log|
   +--------+-------------------------------------------------------+-------------------------+
   |critical|/<dir_dat>/<tenant>/RUN/<package>/<cmd>/<Log directory>|<Log type>_<ts>_<pid>.log|
   +--------+-------------------------------------------------------+-------------------------+

Naming Examples
"""""""""""""""

  .. Naming-examples-for-logging-file-paths-label:
  .. table:: *Naming examples for logging file paths*

   +--------+--------------------------------------------+------------------------+
   |Type    |Directory                                   |File                    |
   +========+============================================+========================+
   |debug   |/data/otev/umh/RUN/otev_xls_srr/evupreg/logs|debs_1737118199_9470.log|
   +--------+--------------------------------------------+------------------------+
   |info    |/data/otev/umh/RUN/otev_xls_srr/evupreg/logs|infs_1737118199_9470.log|
   +--------+--------------------------------------------+------------------------+
   |warning |/data/otev/umh/RUN/otev_xls_srr/evupreg/logs|wrns_1737118199_9470.log|
   +--------+--------------------------------------------+------------------------+
   |error   |/data/otev/umh/RUN/otev_xls_srr/evupreg/logs|errs_1737118199_9470.log|
   +--------+--------------------------------------------+------------------------+
   |critical|/data/otev/umh/RUN/otev_xls_srr/evupreg/logs|crts_1737118199_9470.log|
   +--------+--------------------------------------------+------------------------+

Python Terminology
==================

Python packages
---------------

  .. Python packages-label:
  .. table:: *Python packages*

   +-----------+-----------------------------------------------------------------+
   |Name       |Definition                                                       |
   +===========+==========+======================================================+
   |Python     |Python packages are directories that contains the special module |
   |package    |``__init__.py`` and other modules, packages files or directories.|
   +-----------+-----------------------------------------------------------------+
   |Python     |Python sub-packages are python packages which are contained in   |
   |sub-package|another pyhon package.                                           |
   +-----------+-----------------------------------------------------------------+

Python package Sub-directories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  .. Python package-Sub-directories-label:
  .. table:: *Python packages Sub-directories*

   +----------------------+-------------------------------+
   |Name                  |Definition                     |
   +======================+==========+====================+
   |Python package        |Sub-directories are directories|
   |sub-directory         |contained in python packages.  |
   +----------------------+-------------------------------+
   |Special Python package|Python package sub-directories |
   |sub-directory         |with a special meaning.        |
   +----------------------+-------------------------------+

Special python package Sub-directories
""""""""""""""""""""""""""""""""""""""

  .. Special-python-package-Sub-directories-label:
  .. table:: *Special python Sub-directories*

   +-------+------------------------------------------+
   |Name   |Description                               |
   +=======+==========================================+
   |bin    |Directory for package scripts.            |
   +-------+------------------------------------------+
   |cfg    |Directory for package configuration files.|
   +-------+------------------------------------------+
   |data   |Directory for package data files.         |
   +-------+------------------------------------------+
   |service|Directory for systemd service scripts.    |
   +-------+------------------------------------------+

Python package files
^^^^^^^^^^^^^^^^^^^^

  .. Python-package-files-label:
  .. table:: *Python package files*

   +--------------+---------------------------------------------------------+
   |Name          |Definition                                               |
   +==============+==========+==============================================+
   |Python        |Files within a python package.                           |
   |package files |                                                         |
   +--------------+---------------------------------------------------------+
   |Special python|Package files which are not modules and used as python   |
   |package files |and used as python marker files like ``__init__.py``.    |
   +--------------+---------------------------------------------------------+
   |Python package|Files with suffix ``.py``; they could be empty or contain|
   |module        |python code; other modules can be imported into a module.|
   +--------------+---------------------------------------------------------+
   |Special python|Modules like ``__init__.py`` or ``main.py`` with special |
   |package module|names and functionality.                                 |
   +--------------+---------------------------------------------------------+

Special python package files
""""""""""""""""""""""""""""

  .. Special-python-package-files-label:
  .. table:: *Special python package files*

   +--------+--------+---------------------------------------------------------------+
   |Name    |Type    |Description                                                    |
   +========+========+===============================================================+
   |py.typed|Type    |The ``py.typed`` file is a marker file used in Python packages |
   |        |checking|to indicate that the package supports type checking. This is a |
   |        |marker  |part of the PEP 561 standard, which provides a standardized way|
   |        |file    |to package and distribute type information in Python.          |
   +--------+--------+---------------------------------------------------------------+

Special python package modules
""""""""""""""""""""""""""""""

  .. Special-Python-package-modules-label:
  .. table:: *Special Python package modules*

   +--------------+-----------+-----------------------------------------------------------------+
   |Name          |Type       |Description                                                      |
   +==============+===========+=================================================================+
   |__init__.py   |Package    |The dunder (double underscore) module ``__init__.py`` is used to |
   |              |directory  |execute initialisation code or mark the directory it contains as |
   |              |marker     |a package. The Module enforces explicit imports and thus clear   |
   |              |file       |namespace use and call them with the dot notation.               |
   +--------------+-----------+-----------------------------------------------------------------+
   |__main__.py   |entry point|The dunder module ``__main__.py`` serves as an entry point for   |
   |              |for the    |the package. The module is executed when the package is called by|
   |              |package    |the interpreter with the command **python -m <package name>**.   |
   +--------------+-----------+-----------------------------------------------------------------+
   |__version__.py|Version    |The dunder module ``__version__.py`` consist of assignment       |
   |              |file       |statements used in Versioning.                                   |
   +--------------+-----------+-----------------------------------------------------------------+

Python elements
---------------

  .. Python elements-label:
  .. table:: *Python elements*

   +---------------------+--------------------------------------------------------+
   |Name                 |Description                                             |
   +=====================+========================================================+
   |Python method        |Python functions defined in python modules.             |
   +---------------------+--------------------------------------------------------+
   |Special python method|Python functions with special names and functionalities.|
   +---------------------+--------------------------------------------------------+
   |Python class         |Classes defined in python modules.                      |
   +---------------------+--------------------------------------------------------+
   |Python class method  |Python methods defined in python classes                |
   +---------------------+--------------------------------------------------------+

Special python methods
^^^^^^^^^^^^^^^^^^^^^^

  .. Special-python-methods-label:
  .. table:: *Special python methods*

   +--------+------------+----------------------------------------------------------+
   |Name    |Type        |Description                                               |
   +========+============+==========================================================+
   |__init__|class object|The special method ``__init__`` is called when an instance|
   |        |constructor |(object) of a class is created; instance attributes can be|
   |        |method      |defined and initalized in the method.                     |
   +--------+------------+----------------------------------------------------------+

Table of Contents
=================

.. contents:: **Table of Content**

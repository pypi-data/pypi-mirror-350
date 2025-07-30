##########
ka_uts_dic
##########

********
Overview
********

.. start short_desc

**Utilities to manage Dictionaries**

.. end short_desc

************
Installation
************

.. start installation

Package ``ka_uts_dic`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: shell

	$ python -m pip install ka_uts_dic

To install with ``conda``:

.. code-block:: shell

	$ conda install -c conda-forge ka_uts_dic

.. end installation

***************
Package logging 
***************

(c.f.: **Appendix**: `Package Logging`)

*************
Package files
*************

Classification
==============

The Package ``ka_uts_uts`` consist of the following file types (c.f.: **Appendix**):

#. **Special files:** (c.f.: **Appendix:** *Special python package files*)

#. **Dunder modules:** (c.f.: **Appendix:** *Special python package modules*)

#. **Modules**

   #. **Modules for Management of Dictionary**

      a. **dic.py**

   #. **Modules for Management of Dictionary of arrays**

      a. **doaod.py**
      #. **doa.py**

   #. **Modules for Management of Dictionary of callables**

      a. **doc.py**

   #. **Modules for Management of Dictionary of dataframes**
   
      a. **dopddf.py**
      #. **dopldf.py**

   #. **Modules for Management of Dictionary of dictionaries**
   
      a. **dodoa.py**
      #. **dodoa.py**
      #. **dodod.py**
      #. **dodows.py**
      #. **dod.py**

   #. **Modules for Management of Dictionary of objects**
   
      a. **doo.py**
   
************************************
Modules for Management of Dictionary
************************************

  .. Dictionary-Modules-label:
  .. table:: *Dictionary-Modules*

   +------+------------------------+
   |Name  |Description             |
   +======+========================+
   |dic.py|Management of Dictionary|
   +------+------------------------+

Module: dic
============

Classes of Module: dic
----------------------

The Module ``dic.py`` contains the followinga static classes:

   +----+------------------------+
   |Name|Description             |
   +====+========================+
   |Dic |Management of Dictionary|
   +----+------------------------+

Class: Dic of Module: dic
-------------------------

The static Class ``Dic`` is used to manage Dictionaries;
The Methods of Class ``Dic`` could be classified into the following method types:

#. *Miscellenous Methods*
#. *Set Methods*
#. *Get / Show Methods*
#. *Split Methods*
#. *Yield Methods*

Miscellenous Methods of Class: Dic
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  .. Dic-Miscellenous-Methods-label:
  .. table:: *Dic: Miscellenous Methods*

   +------------------------+----------------------------------------------------------+
   |Name                    |Description                                               |
   +========================+==========================================================+
   |add_counter_to_values   |Apply the function "add_counter_with key" to the last key |
   |                        |of the key list and the Dictionary localized by that key. |
   +------------------------+----------------------------------------------------------+
   |add_counter_to_value    |Initialize the unintialized counter with 1 and add it to  |
   |                        |the Dictionary value of the key.                          |
   +------------------------+----------------------------------------------------------+
   |append_to_values        |Apply the function "append with key" to the last key of   |
   |                        |the key list amd the Dictionary localized by that key.    |
   +------------------------+----------------------------------------------------------+
   |append_to_value         |Initialize the unintialized counter with 1 and add it to  |
   |                        |the Dictionary value of the key.                          |
   +------------------------+----------------------------------------------------------+
   |change_keys_by_keyfilter|Change the keys of the Dictionary by the values of the    |
   |                        |keyfilter Dictionary with the same keys.                  |
   +------------------------+----------------------------------------------------------+
   |copy                    |Copy the value for keys from source to target dictionary. |
   +------------------------+----------------------------------------------------------+
   |extend_values           |Appply the function "extend_by_key" to the last key of the|
   |                        |key list and the dictionary localized by that key.        |
   +------------------------+----------------------------------------------------------+
   |extend_value            |Add the item with the key as element to the dictionary if |
   |                        |the key is undefined in the dictionary. Extend the element|
   |                        |value with the value if both supports the extend function.|
   +------------------------+----------------------------------------------------------+
   |increment_values        |Appply the function "increment_by_key" to the last key of |
   |                        |the key list and the Dictionary localized by that key.    |
   +------------------------+----------------------------------------------------------+
   |increment_value         |Increment the value of the key if it is defined in the    |
   |                        |Dictionary, otherwise assign the item to the key          |
   +------------------------+----------------------------------------------------------+
   |is_not                  |Return False if the key is defined in the Dictionary and  |
   |                        |the key value if not empty, othewise returm True.         |
   +------------------------+----------------------------------------------------------+
   |locate                  |Return the value of the key reached by looping thru the   |
   |                        |nested Dictionary with the keys from the key list until   |
   |                        |the value is None or the last key is reached.             |
   +------------------------+----------------------------------------------------------+
   |locate_last_value       |Apply the locate function for the key list which contains |
   |                        |all items except the last one.                            |
   +------------------------+----------------------------------------------------------+
   |lstrip_keys             |Remove the first string found in the Dictionary keys.     |
   +------------------------+----------------------------------------------------------+
   |merge                   |Merge two Dictionaries.                                   |
   +------------------------+----------------------------------------------------------+
   |new                     |create a new dictionary from keys and values.             |
   +------------------------+----------------------------------------------------------+
   |normalize_value         |Replace every Dictionary value by the first list element  |
   |                        |of the value if it is a list with only one element.       |
   +------------------------+----------------------------------------------------------+
   |nvl                     |Return the Dictionary if it is not None otherwise return  |
   |                        |the empty Dictionary "{}".                                |
   +------------------------+----------------------------------------------------------+
   |rename_key_using_kwargs |Rename old Dictionary key with new one get from kwargs.   |
   +------------------------+----------------------------------------------------------+
   |replace_string_in_keys  |Replace old string contained in keys with new one.        |
   +------------------------+----------------------------------------------------------+
   |rename_key              |Rename old Dictionary key with new one.                   |
   +------------------------+----------------------------------------------------------+
   |round_values            |Round values selected by keys,                            |
   +------------------------+----------------------------------------------------------+
   |to_aod                  |Convert dictionary to array of dictionaries.              |
   +------------------------+----------------------------------------------------------+

Get/Show Methods of class: Dic
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  .. Dic-Get-Show-Methods-label:
  .. table:: *Dic: Get/Show Methods*

   +-------------------+-------------------------------------------------------------------+
   |Name               |Description                                                        |
   +===================+===================================================================+
   |get                |Type-dependent extended flattening of array elements               |
   +-------------------+-------------------------------------------------------------------+
   |get_yn_value       |Type-dependent extended flattening of array elements               |
   +-------------------+-------------------------------------------------------------------+
   |sh_dic             |Type-dependent extended flattening of array elements               |
   +-------------------+-------------------------------------------------------------------+
   |sh_d_filter        |Type-dependent extended flattening of array elements               |
   +-------------------+-------------------------------------------------------------------+
   |sh_d_index_d_values|Type-dependent extended flattening of array elements               |
   +-------------------+-------------------------------------------------------------------+
   |sh_d_vals_d_cols   |Type-dependent extended flattening of array elements               |
   +-------------------+-------------------------------------------------------------------+
   |sh_prefixed        |Type-dependent extended flattening of array elements               |
   +-------------------+-------------------------------------------------------------------+
   |sh_keys            |Type-dependent extended flattening of array elements               |
   +-------------------+-------------------------------------------------------------------+
   |show_sorted_keys   |Type-dependent extended flattening of array elements               |
   +-------------------+-------------------------------------------------------------------+
   |sh_value           |Show value of dictionary element selected by keys                  |
   +-------------------+-------------------------------------------------------------------+
   |sh_values          |Convert the dictionary into an array by using a key filter.        |
   |                   |The array elements are the values of all dictionary elements       |
   |                   |where the key is the given single key or where the key is contained|
   |                   |in the key list.                                                   |
   +-------------------+-------------------------------------------------------------------+
   |sh_value2keys      |Convert the dictionary to a new dictionary by using the values as  |
   |                   |new keys and all keys mapped to the same value as new value.       |
   +-------------------+-------------------------------------------------------------------+

Set Methods of class: Dic
^^^^^^^^^^^^^^^^^^^^^^^^^

  .. Set-Methods-of_class-Dic-label:
  .. table:: *Set Methods of class Dic*

   +-----------------------------------------+---------------------------------------------------------------------+
   |Name                                     |Description                                                          |
   +=========================================+=====================================================================+
   |set_kv_not_none                          |Set the given Dictionary key to the given value if both are not None.|
   +-----------------------------------------+---------------------------------------------------------------------+
   |set_by_keys                              |Locate the values in a nested dictionary for the suceeding keys of a |
   |                                         |key array and replace the last value with the given value            |
   +-----------------------------------------+---------------------------------------------------------------------+
   |set_by_key_pair                          |Replace value of source key by value of target key.                  |
   +-----------------------------------------+---------------------------------------------------------------------+
   |set_if_none                              |Locate the values in a nested dictionary for the suceeding keys of a |
   |                                         |key array and assign the given value to the last key if that key does|
   |                                         |not exist in the dictionary.                                         |
   +-----------------------------------------+---------------------------------------------------------------------+
   |set_by_div                               |Replace the source key value by the division of the values of two    |
   |                                         |target keys if the they are of type float and the divisor is not 0   |
   |                                         |otherwise assign None.                                               |
   +-----------------------------------------+---------------------------------------------------------------------+
   |set_first_tgt_with_src_using_d_src2tgt   |Replace value of first dictionary target key found in the source to  |
   |                                         |target dictionary by the source value found in the dictionary.       |
   +-----------------------------------------+---------------------------------------------------------------------+
   |set_first_tgt_with_src_using_d_tgt2src   |Replace value of first dictionary target key found in the target to  |
   |                                         |source dictionary by the source value found in the dictionary.       |
   +-----------------------------------------+---------------------------------------------------------------------+
   |set_format_value                         |Replace the dictionary values by the formatted values using the      |
   |                                         |format string.                                                       |
   +-----------------------------------------+---------------------------------------------------------------------+
   |set_multiply_with_factor                 |Replace the dictionary values by the original value multiplied with  |
   |                                         |the factor.                                                          |
   +-----------------------------------------+---------------------------------------------------------------------+
   |set_tgt_with_src                         |Replace source dictionary values by target dictionary values.        |
   +-----------------------------------------+---------------------------------------------------------------------+
   |set_tgt_with_src_using_doaod_tgt2src     |Loop through the target to source dictionaries of the values of the  |
   |                                         |dictionary of the arrays of target to source dictionaries until the  |
   |                                         |return value of the function                                         |
   |                                         |"set_nonempty_tgt_with_src_using_d_tgt2src" is defined.              |
   +-----------------------------------------+---------------------------------------------------------------------+
   |set_nonempty_tgt_with_src_using_d_tgt2src|Exceute the function "set_tgt_with_src_using_d_tgt2src" if all       |
   |                                         |dictionary values for the keys provided by the values of the target  |
   |                                         |to source dictionary are defined.                                    |
   +-----------------------------------------+---------------------------------------------------------------------+
   |set_first_tgt_with_src_using_d_tgt2src   |Replace value of first dictionary target key found in the target to  |
   |                                         |source dictionary by the source value found in the dictionary if     |
   +-----------------------------------------+---------------------------------------------------------------------+
   |set_tgt_with_src_using_d_src2tgt         |                                                                     |
   +-----------------------------------------+---------------------------------------------------------------------+
   |set_tgt_with_src_using_d_tgt2src         |                                                                     |
   +-----------------------------------------+---------------------------------------------------------------------+

Dic: Split Methods
^^^^^^^^^^^^^^^^^^

  .. Dic-Split-Methods-label:
  .. table:: *Dic Split Methods*

   +----------------------+----------------------------------------------------------------------------+
   |Name                  |Description                                                                 |
   +======================+============================================================================+
   |split_by_value_endwith|Split the dictionary into a tuple of dictionaries using the the condition   |
   |                      |"the element value ends with the given value".                              |
   |                      |The first tuple element is the dictionary of all dictionary                 |
   |                      |elements whose value ends with the given value; the second one is           |
   |                      |the dictionary of the other elements.                                       |
   +----------------------+----------------------------------------------------------------------------+
   |split_by_value        |Split the dictionary into a tuple of dictionaries using the given value. The|
   |                      |first tuple element is the dictionary of all elements whose value is equal  |
   |                      |to the given value; the second one is the dictionary of the other elements. |
   +----------------------+----------------------------------------------------------------------------+
   |split_by_value_is_int |Split the dictionary into a tuple of dictionaries using the condition       |
   |                      |"the element value is of type integer". The first tuple element is the      |
   |                      |dictionary of all elements whose value is of type integer; the second one is| 
   |                      |the dictionary of the other elements.                                       |
   +----------------------+----------------------------------------------------------------------------+

Dic: Yield Methods
^^^^^^^^^^^^^^^^^^

  .. Dic-Yield-Methods-label:
  .. table:: *Dic: Yield Methods*

   +---------------------------+----------------------------------------------------------------------------+
   |Name                       |Description                                                                 |
   +===========================+============================================================================+
   |yield_values_with_keyfilter|Yield the values of all elements which are selected by the given key filter.|
   +---------------------------+----------------------------------------------------------------------------+

****************************************************
Modules for Management of Dictionary of Dictionaries
****************************************************

  .. Modules-for-Management-of-Dictionary-of-Dictionaries-label:
  .. table:: *Modules for Management of Dictionary of Dictionaries*

   +------+-------------------------------------------------------+
   |Name  |Description                                            |
   +======+=======================================================+
   |dod.py|Management of Dictionary of Dictionaries.              |
   +------+-------------------------------------------------------+
   |d2v.py|Management of 2-dimensional Dictionary of Dictionaries.|
   |      |A 2 dimensional Dictionary of Dictionaries contains    |
   |      |dictionaries of Dictionaries as values.                |
   +------+-------------------------------------------------------+
   |d3v.py|Management of 3-dimensional Dictionary of Dictionaries.|
   |      |A 3 dimensional Dictionary of Dictionaries contains    |
   |      |Dictionaries of Dictionaries of Dictionaries as values.|
   +------+-------------------------------------------------------+

**********************************************
Modules for Management of Dictionary of Arrays
**********************************************

  .. Modules-for-Dictionaryies-of-Arrays-label:
  .. table:: *Modules for Dictionaries of Arrays*

   +--------+---------------------------------------------------+
   |Name    |Description                                        |
   +========+===================================================+
   |doaod.py|Management of Dictionary of Arrays of Dictionaries.|
   +--------+---------------------------------------------------+
   |doa.py  |Management of Dictionary of Arrays.                |
   +--------+---------------------------------------------------+

Module: doaod.py
================

doaod.py Classes
----------------

The Module ``doaod.py`` contains the static class ``DoAoD``:

Class: DoAoD
------------

The static Class ``DoAoD`` is used to manage ``Dictionary of Arrays of Dictionaries``;
it contains the subsequent methods.

DoAoD Methods
^^^^^^^^^^^^^^^

  .. DoAoD-Methods-label:
  .. table:: *DoAoD Methods*

   +------------------+-------------------------------------------------------+
   |Name              |Description                                            |
   +==================+=======================================================+
   |dic_value_is_empty|Check if all keys of the given Dictionary of Arrays of |
   |                  |Dictionaries are found in any Dictionary of the Array  |
   |                  |of Dictionaries and the value for the key is not empty.|
   +------------------+-------------------------------------------------------+
   |sh_aod_unique     |Convert Dictionary of Array of Dictionaries to unique  |
   |                  |Array of Dictionaries.                                 |
   +------------------+-------------------------------------------------------+
   |sh_aod            |Convert Dictionary of Array of Dictionaries to Array   |
   |                  |of Dictionaries.                                       |
   +------------------+-------------------------------------------------------+
   |sh_unique         |Convert Dictionary of Array of Dictionaries to         |
   |                  |Dictionaries of unique Array of Dictionaries.          |
   +------------------+-------------------------------------------------------+
   |union_by_keys     |Convert filtered Dictionary of Arrays of Dictionaries  |
   |                  |by keys to an Array of distinct Dictionaries           |
   +------------------+-------------------------------------------------------+
   |union             |Convert Dictionary of Arrays of Dictionaries to an     |
   |                  |Array of distinct Dictionaries                         |
   +------------------+-------------------------------------------------------+

Module: doa.py
==============

doa.py Classes
---------------

The Module ``doa.py`` contains the static classes ``DoA``:

Class: DoA
----------

The static Class ``DoA`` is used to manage Arrays used for the flattening of dictionaries;
it contains the subsequent methods.

DoA: Methods
^^^^^^^^^^^^

  .. DoA-Methods-label:
  .. table:: *DoA Methods*

   +-------------+------------------------------------------------------+
   |Name         |Description                                           |
   +=============+======================================================+
   |apply        |                                                      |
   +-------------+------------------------------------------------------+
   |append       |                                                      |
   +-------------+------------------------------------------------------+
   |append_by_key|                                                      |
   +-------------+------------------------------------------------------+
   |append_unique|                                                      |
   +-------------+------------------------------------------------------+
   |extend       |                                                      |
   +-------------+------------------------------------------------------+
   |set          |                                                      |
   +-------------+------------------------------------------------------+
   |sh_d_pddf    |                                                      |
   +-------------+------------------------------------------------------+
   |sh_union     |                                                      |
   +-------------+------------------------------------------------------+

******************************************+++++++*******
Modules for the Management of Dictionary of Dictionaries
******************************************+++++++*******

  .. Modules-for-the-Management-of-Dictionary-of-Dictionaries-label:
  .. table:: *Modules for the Management of Dictionary of Dictionaries*

   +--------+---------------------------------------------------------+
   |Name    |Description                                              |
   +========+=========================================================+
   |dodoa.py|Management of Dictionary of Dictionaries of Arrays.      |
   +--------+---------------------------------------------------------+
   |dodod.py|Management of Dictionary of Dictionaries of Dictionaries.|
   +--------+---------------------------------------------------------+
   |dod.py  |Management of Dictionary of Dictionaries.                |
   +--------+---------------------------------------------------------+

Module: doc.py
==============

The Module ``fnc.py`` contains the static class ``Fnc`` with I/O Control methods for log files;

doc.py Class Fnc
----------------

The static Class ``Fnc`` contains the subsequent methods

Fnc: Methods
^^^^^^^^^^^^

  .. Fnc-Methods-label:
  .. table:: *Fnc Methods*

   +--------+------+---------------------------------------------+
   |Name    |Type  |Description                                  |
   +========+======+=============================================+
   |ex      |class |Show and execute the function as the value of|
   |        |      |of the function-dictionary for the given key.|
   +--------+------+---------------------------------------------+
   |identity|static|Identity function for any objects            |       
   +--------+------+---------------------------------------------+
   |sh      |static|Show(get) the function as the value of the   |       
   |        |      |function-dictionary for the given key.       |       
   +--------+------+---------------------------------------------+

Fnc Method: ex
^^^^^^^^^^^^^^

Parameter
"""""""""

  .. Fnc-Method-ex-Parameter-label:
  .. table:: *Fnc Method ex: Parameter*

   +-----------+--------+------------------------------+
   |Name       |Type    |Description                   |
   +===========+========+==============================+
   |cls        |class   |current class                 |
   +-----------+--------+------------------------------+
   |doc        |TnDoC   |Dictionary of Callables       |
   +-----------+--------+------------------------------+
   |key        |TnDoc   |key                           |
   +-----------+--------+------------------------------+
   |args_kwargs|TnArrDoc|arguments or keyword arguments|
   +-----------+--------+------------------------------+

Return Value
""""""""""""

  .. Fnc-Method-ex-Return-Value-label:
  .. table:: *Fnc Method ex: Return Value*

   +----+----------+------------------------------------------+
   |Name|Type      |Description                               |
   +====+==========+==========================================+
   |    |TyCallable|Value of Function for argument args_kwargs|
   +----+----------+------------------------------------------+

Fnc Method: identity
^^^^^^^^^^^^^^^^^^^^

Parameter
"""""""""

  .. Fnc Method-identity-Parameter-label:
  .. table:: *Fnc Method identity: Parameter*

   +----+-----+-----------+
   |Name|Type |Description|
   +====+=====+===========+
   |obj |TyAny|object     |
   +----+-----+-----------+

Return Value
""""""""""""

  .. Fnc Method-identity-Return-Value-label:
  .. table:: *Fnc Method identity: Parameter*

   +----+-----+-----------+
   |Name|Type |Description|
   +====+=====+===========+
   |obj |TyAny|object     |
   +----+-----+-----------+

Fnc Method: sh
^^^^^^^^^^^^^^

Parameter
"""""""""

  .. Fnc-Method-sh-Parameter-label:
  .. table:: *Fnc Method sh: Parameter*

   +----+-----+------------------------------+
   |Name|Type |Description                   |
   +====+=====+==============================+
   |cls |class|current class                 |
   +----+-----+------------------------------+
   |doc |TnDoC|Dictionary of Callables       |
   +----+-----+------------------------------+
   |key |TnDoc|key                           |
   +----+-----+------------------------------+

Return Value
""""""""""""

  .. Fnc-Method-sh-Return-Value-label:
  .. table:: *Fnc Method sh: REturn Value*

   +----+----------+-----------+
   |Name|Type      |Description|
   +====+==========+===========+
   |fnc |TyCallable|Function   |
   +----+----------+-----------+

Module: pacmod.py
=================

The Utility module pacmod.py contains a single static class ``PacMod``.

pacmod.py Class: PacMmd
-----------------------

PacMod Methods
^^^^^^^^^^^^^^

  .. PacMod-Methods-label:
  .. table:: *PacMod Methods*

   +-----------------+-------------------------------------------------+
   |Name             |Description                                      |
   +=================+=================================================+
   |sh_d_pacmod      |create and show (return) pacmod dictionary       |
   +-----------------+-------------------------------------------------+
   |sh_path_cfg_yaml |show pacmod file path of the yaml file           |
   |                 |<pacmod module>.yaml in the data directory of the|
   |                 |current module of the current package            |
   +-----------------+-------------------------------------------------+
   |sh_path_keys_yaml|show pacmod file path type for the yaml file     |
   |                 |keys.yml in the data directory of the current    |
   |                 |module of the current pacḱage                    |
   +-----------------+-------------------------------------------------+
   |sh_pacmod_type   |show pacmod type directory path                  |
   +-----------------+-------------------------------------------------+
   |sh_file_path     |show pacmod file path                            |
   +-----------------+-------------------------------------------------+
   |sh_pattern       |show pacmod file path pattern                    |
   +-----------------+-------------------------------------------------+
   |sh_path_cfg_log  |show file path of log configuration file         |
   +-----------------+-------------------------------------------------+
   |sh_d_pacmod      |show pacmod dictionary                           |
   +-----------------+-------------------------------------------------+

PacMod Method: sh_d_pacmod
^^^^^^^^^^^^^^^^^^^^^^^^^^

Parameter
"""""""""

  .. Parameter-of-module-sh_d_pacmod-label:
  .. table:: *Parameter of method sh_d_pacmod*

   +--------+-----+-----------------+
   |Name    |Type |Description      |
   +========+=====+=================+
   |root_cls|class|root class       |
   +--------+-----+-----------------+
   |tenant  |Any  |                 |
   +--------+-----+-----------------+
        
Method: sh_path_cfg_yaml
^^^^^^^^^^^^^^^^^^^^^^^^

Parameter
"""""""""

  .. Parameter-of-module-sh_path_cfg_yaml-of-class-Pacmod-label:
  .. table:: *Parameter of method sh_path_cfg_yaml*

   +------+-----+-----------------+
   |Name  |Type |Description      |
   +======+=====+=================+
   |pacmod|TyDic|                 |
   +------+-----+-----------------+
        
Method: sh_path_cfg_yaml
^^^^^^^^^^^^^^^^^^^^^^^^

Parameter
"""""""""

   +------+-----+-----------------+
   |Name  |Type |Description      |
   +======+=====+=================+
   |pacmod|TyDic|                 |
   +------+-----+-----------------+
   |type\_|Tystr|                 |
   +------+-----+-----------------+

Method: sh_path_cfg_yaml
^^^^^^^^^^^^^^^^^^^^^^^^

Parameter
"""""""""

  .. Parameter-of-module-sh_path_cfg_yaml-label:
  .. table:: *Parameter of method sh_path_cfg_yaml*

   +------+-----+-----------------+
   |Name  |Type |Description      |
   +======+=====+=================+
   |pacmod|TyDic|                 |
   +------+-----+-----------------+
   |type\_|str  |                 |
   +------+-----+-----------------+
        
Method: sh_path_cfg_yaml
^^^^^^^^^^^^^^^^^^^^^^^^

Parameter
"""""""""

  .. Parameter-of-module-sh_path_cfg_yaml-label:
  .. table:: *Parameter of method sh_path_cfg_yaml*

   +---------+-----+-----------------+
   |Name     |Type |Description      |
   +=========+=====+=================+
   |cls      |class|current class    |
   +---------+-----+-----------------+
   |pacmod   |TyDic|                 |
   +---------+-----+-----------------+
   |type\_   |TyStr|                 |
   +---------+-----+-----------------+
   |suffix   |TyStr|                 |
   +---------+-----+-----------------+
   |pid      |TyStr|                 |
   +---------+-----+-----------------+
   |ts       |TyAny|                 |
   +---------+-----+-----------------+
   |\**kwargs|TyAny|keyword arguments|
   +---------+-----+-----------------+
        
Method: sh_path_cfg_yaml
^^^^^^^^^^^^^^^^^^^^^^^^

Parameter
"""""""""

  .. Parameter-of-method-sh_path_cfg_yaml-label:
  .. table:: *Parameter of method sh_path_cfg_yaml*

   +---------+-----+-----------------+
   |Name     |Type |Description      |
   +=========+=====+=================+
   |pacmod   |TyDic|                 |
   +---------+-----+-----------------+
   +---------+-----+-----------------+
   |type\_   |TyStr|                 |
   +---------+-----+-----------------+
   |suffix   |TyStr|                 |
   +---------+-----+-----------------+
   |\**kwargs|TyAny|keyword arguments|
   +---------+-----+-----------------+
        
Method: sh_path_cfg_yaml
^^^^^^^^^^^^^^^^^^^^^^^^

Parameter
"""""""""

  .. Parameter-of-method-sh_path_cfg_yaml-label:
  .. table:: *Parameter of method sh_path_cfg_yaml*

   +--------+-----+-----------------+
   |Name    |Type |Description      |
   +========+=====+=================+
   |pacmod  |TnDic|                 |     
   +--------+-----+-----------------+
   +--------+-----+-----------------+
   |filename|TyStr|                 |
   +--------+-----+-----------------+
        
Method: sh_d_pacmod
^^^^^^^^^^^^^^^^^^^

Parameter
"""""""""

  .. Parameter-of-method-sh_d_pacmod-label:
  .. table:: *Parameter of method sh_d_pacmod*

   +---------+-----+-----------------+
   |Name     |Type |Description      |
   +=========+=====+=================+
   |cls      |class|current class    |
   +---------+-----+-----------------+
   |\**kwargs|TyAny|keyword arguments|
   +---------+-----+-----------------+

Module: dodoa.py
================

Classes
-------

The Module ``dodoa.py`` contains the static class ``DoDoA``:

Class: DoDoA
------------

The static Class ``DoDoA`` is used to manage Dictionary of Dictionaries of Arrays;
it contains the subsequent methods.

Methods
^^^^^^^

  .. Methods-of-class-DoDoA-label:
  .. table:: *Methods of class DoDoA*

   +-------------+------------------------------------------------------+
   |Name         |Description                                           |
   +=============+======================================================+
   |append       |                                                      |
   +-------------+------------------------------------------------------+
   |sh_union     |                                                      |
   +-------------+------------------------------------------------------+

Module: dodod.py
================

Classes
-------

The Module ``dodod.py`` contains the static Class ``DoDoD``:

Class: DoDoD
------------

The static Class ``DoDoD`` is used to manage Dictionary of Dictionaries of Dictionaries;
it contains the subsequent methods.

Methods
^^^^^^^

  .. Methods-of-class-DoDoD-label:
  .. table:: *Methods of class DoDoD*

   +------------+------------------------------------------------------+
   |Name        |Description                                           |
   +============+======================================================+
   |set         |                                                      |
   +------------+------------------------------------------------------+
   |yield_values|                                                      |
   +------------+------------------------------------------------------+

Module: dod.py
==============

Classes
-------

The Module ``dod.py`` contains the static Class ``DoD``:


Class: DoD
----------

The static Class ``DoD`` is used to manage ``Dictionary of Dictionaries``;
it contains the subsequent methods.

Methods
^^^^^^^

  .. Methods-of_class-DoD-label:
  .. table:: *DoD Methods*

   +---------------+-------------------------------------------------------+
   |Name           |Description                                            |
   +===============+=======================================================+
   |nvl            |Return the Dictionary of Dictionaries if it is not None|
   |               |otherwise return the empty Dictionary "{}".            |
   +---------------+-------------------------------------------------------+
   |replace_keys   |Recurse through the Dictionary while building a new one|
   |               |with new keys and old values; the old keys are         |
   |               |translated to new ones by the keys Dictionary.         |
   +---------------+-------------------------------------------------------+
   |yield_values   |                                                       |
   +---------------+-------------------------------------------------------+

Module: dodows.py
=================

Classes
-------

The Module ``dodows.py`` contains the static Class ``DoDoWs``:

Class: DoDoWs
-------------

The static Class ``DoDoWs`` is used to manage ``Dictionary of Dictionaries of Worksheets``;
it contains the subsequent methods.

Methods
^^^^^^^

  .. Methods-of-class-DoDoWs-label:
  .. table:: *Methods of class DoDoWs*

   +--------------+------------------------------------------------------------------+
   |Name          |Description                                                       |
   +==============+==================================================================+
   |write_workbook|Write a workbook using a Dictionary of Dictionaries of worksheets.|
   +--------------+------------------------------------------------------------------+

***********************************************
Modules for Management of Dictionariy of Ojects
***********************************************

The Module Type ``Modules for Nabagement of Dictionary of Objects`` contains the following Modules:

  .. Management-Modules-for-Dictionaries-of-Ojects-label:
  .. table:: *Management Modules for Dictionaries of Ojects*

   +------+------------------------------------+
   |Name  |Description                         |
   +======+====================================+
   |doo.py|Management of Dictionary of Objects.|
   +------+------------------------------------+

Module: doo.py
==============

The Module ``doo.py`` contains the static Classes ``DoO``.

Class: DoO
----------

The static Class ``DoO`` is used to manage ``Dictionary of Objects``; it contains the subsequent methods.

Methods
^^^^^^^

  .. Methods-of-class-DoO-label:
  .. table:: *Methods of class DoO*

   +------------+---------------------------------------------------------------+
   |Name        |Description                                                    |
   +============+===============================================================+
   |replace_keys|Replace the keys of the given Dictionary by the values found in|
   |            |the given keys Dictionary if the values are not Dictionaries;  |
   |            |otherwise the function is called with these values.            |
   +------------+---------------------------------------------------------------+

**************************************
Modules for Dictionaries of Dataframes
**************************************

Modules
=======

The Module Type ``Modules for Dictionaries of Dataframes`` contains the following Modules:

  .. Management Modules for Dictionary of Dataframes-label:
  .. table:: *Management Modules for Dictionary of Dataframes*

   +---------+----------------------------------------------+
   |Name     |Description                                   |
   +=========+==============================================+
   |dopddf.py|Management of Dictionary of Panda Dataframes. |
   +---------+----------------------------------------------+
   |dopldf.py|Management of Dictionary of Polars Dataframes.|
   +---------+----------------------------------------------+

Module: dopddf.py
=================

The Module ``dopddf.py`` contains only the static Class ``DoPdDf``.


Class: DoPdDf
-------------

The static Class ``DoPdDf`` is used to manage ``Dictionaries of Panda Dataframes``;
it contains the subsequent methods.

Methods
^^^^^^^

  .. Methods-of-class-DoPdDf-label:
  .. table:: *Methodsc of class DoPdDf*

   +----------------------+-----------------------------------------------------+
   |Name                  |Description                                          |
   +======================+=====================================================+
   |set_ix_drop_key_filter|Apply Function set_ix_drop_col_filter to all Panda   |
   |                      |Dataframe values of given Dictionary.                |
   +----------------------+-----------------------------------------------------+
   |to_doaod              |Replace NaN values of Panda Dataframe values of given|
   |                      |Dictionary and convert them to Array of Dictionaries.|
   +----------------------+-----------------------------------------------------+

Module: dopldf.py
==================

The Module ``dopldf.py`` contains only the static Class ``DoPlDf``:


Class: DoPlDf
-------------

The static Class ``DoPlDf`` is used to manage ``Dictionary of Polars Dataframes``;
it contains the subsequent Methods.

Methods
^^^^^^^

  .. Methods-of-class-DoPlDf-label:
  .. table:: *Methods of class DoPlDf*

   +--------+------------------------------------------------------+
   |Name    |Description                                           |
   +========+======================================================+
   |to_doaod|Replace NaN values of Polars Dataframe values of given|
   |        |Dictionary and convert them to Array of Dictionaries. |
   +--------+------------------------------------------------------+

########
Appendix
########

***************
Package Logging
***************

Description
===========

The Standard or user specifig logging is carried out by the log.py module of the logging
package **ka_uts_log** using the standard- or user-configuration files in the logging
package configuration directory:

* **<logging package directory>/cfg/ka_std_log.yml**,
* **<logging package directory>/cfg/ka_usr_log.yml**.

The Logging configuration of the logging package could be overriden by yaml files with the
same names in the application package- or application data-configuration directories:

* **<application package directory>/cfg**
* **<application data directory>/cfg**.

Log message types
=================

Logging defines log file path names for the following log message types: .

#. *debug*
#. *info*
#. *warning*
#. *error*
#. *critical*

Log types and Log directories
-----------------------------

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

Application parameter for logging
---------------------------------

  .. Application-parameter-used-in-log-naming-label:
  .. table:: *Application parameter used in log naming*

   +-----------------+---------------------------+------+------------+
   |Name             |Decription                 |Values|Example     |
   +=================+===========================+======+============+
   |dir_dat          |Application data directory |      |/otev/data  |
   +-----------------+---------------------------+------+------------+
   |tenant           |Application tenant name    |      |UMH         |
   +-----------------+---------------------------+------+------------+
   |package          |Application package name   |      |otev_xls_srr|
   +-----------------+---------------------------+------+------------+
   |cmd              |Application command        |      |evupreg     |
   +-----------------+---------------------------+------+------------+
   |pid              |Process ID                 |      |681025      |
   +-----------------+---------------------------+------+------------+
   |log_ts_type      |Timestamp type used in     |ts,   |ts          |
   |                 |logging files|ts, dt       |dt'   |            |
   +-----------------+---------------------------+------+------------+
   |log_sw_single_dir|Enable single log directory|True, |True        |
   |                 |or multiple log directories|False |            |
   +-----------------+---------------------------+------+------------+

Log files naming
----------------

Naming Conventions
^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^

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

******************
Python Terminology
******************

Python Packages
===============

Overview
--------

  .. Python Packages-Overview-label:
  .. table:: *Python Packages Overview*

   +---------------------+-----------------------------------------------------------------+
   |Name                 |Definition                                                       |
   +=====================+=================================================================+
   |Python package       |Python packages are directories that contains the special module |
   |                     |``__init__.py`` and other modules, packages files or directories.|
   +---------------------+-----------------------------------------------------------------+
   |Python sub-package   |Python sub-packages are python packages which are contained in   |
   |                     |another pyhon package.                                           |
   +---------------------+-----------------------------------------------------------------+
   |Python package       |directory contained in a python package.                         |
   |sub-directory        |                                                                 |
   +---------------------+-----------------------------------------------------------------+
   |Python package       |Python package sub-directories with a special meaning like data  |
   |special sub-directory|or cfg                                                           |
   +---------------------+-----------------------------------------------------------------+


Examples
--------

  .. Python-Package-sub-directory-Examples-label:
  .. table:: *Python Package sub-directory-Examples*

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
====================

Overview
--------

  .. Python-package-files-overview-label:
  .. table:: *Python package overview files*

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

Examples
--------

  .. Python-package-files-examples-label:
  .. table:: *Python package examples files*

   +--------------+-----------+-----------------------------------------------------------------+
   |Name          |Type       |Description                                                      |
   +==============+===========+=================================================================+
   |py.typed      |Type       |The ``py.typed`` file is a marker file used in Python packages to|
   |              |checking   |indicate that the package supports type checking. This is a part |
   |              |marker     |of the PEP 561 standard, which provides a standardized way to    |
   |              |file       |package and distribute type information in Python.               |
   +--------------+-----------+-----------------------------------------------------------------+
   |__init__.py   |Package    |The dunder (double underscore) module ``__init__.py`` is used to |
   |              |directory  |execute initialisation code or mark the directory it contains as |
   |              |marker     |a package. The Module enforces explicit imports and thus clear   |
   |              |file       |namespace use and call them with the dot notation.               |
   +--------------+-----------+-----------------------------------------------------------------+
   |__main__.py   |entry point|The dunder module ``__main__.py`` serves as an entry point for   |
   |              |for the    |the package. The module is executed when the package is called   |
   |              |package    |by the interpreter with the command **python -m <package name>**.|
   +--------------+-----------+-----------------------------------------------------------------+
   |__version__.py|Version    |The dunder module ``__version__.py`` consist of assignment       |
   |              |file       |statements used in Versioning.                                   |
   +--------------+-----------+-----------------------------------------------------------------+

Python methods
==============

Overview
--------

  .. Python-methods-overview-label:
  .. table:: *Python methods overview*

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

Examples
--------

  .. Python-methods-examples-label:
  .. table:: *Python methods examples*

   +--------+------------+----------------------------------------------------------+
   |Name    |Type        |Description                                               |
   +========+============+==========================================================+
   |__init__|class object|The special method ``__init__`` is called when an instance|
   |        |constructor |(object) of a class is created; instance attributes can be|
   |        |method      |defined and initalized in the method.                     |
   +--------+------------+----------------------------------------------------------+

#################
Table of Contents
#################

.. contents:: **Table of Content**

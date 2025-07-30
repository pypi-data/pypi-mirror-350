###########
ka_uts_path
###########

********
Overview
********

.. start short_desc

**Path Utilities**

.. end short_desc

************
Installation
************

.. start installation

Package ``ka_uts_path`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: shell

	$ python -m pip install ka_uts_path

To install with ``conda``:

.. code-block:: shell

	$ conda install -c conda-forge ka_uts_path

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

The Package ``ka_uts_path`` consist of the following file types (c.f.: **Appendix**):

#. **Special files:** (c.f.: **Appendix:** *Special python package files*)

#. **Dunder modules:** (c.f.: **Appendix:** *Special python package modules*)

#. **Modules**

   #. **Modules for Management of Array of Paths**

      #. **aododopath.py**
      #. **aopath.py**

   #. **Modules for Management of Dictionary of Paths**

      a. **dodopath.py**
      #. **dopath.py**

   #. **Modules for Management of Paths**

      a. **file.py**
      #. **path.py**

   #. **Modules for Management of Path names**

      #. **pathnm.py**

******************************************
Modules for Management of Array of Paths**
******************************************

The Module Type ``Modules for Management of Array of Paths`` contains the following Modules:

  .. Array-of-Paths-Management-Modules-label:
  .. table:: *Array of Paths Management Rodules*

   +-------------+-------------------------------------------------------------+
   |Name         |Description                                                  |
   +=============+=============================================================+
   |aododopath.py|Management of Array of Dictionaries of Dictionaries of Paths.|
   +-------------+-------------------------------------------------------------+
   |aopath.py    |Management of Array of Paths.                                |
   +-------------+-------------------------------------------------------------+

Module: aopath.py
==================

The Module ``aopath.py`` contains the static Classes ``AoPath``.

Class: AoPath
-------------

The static Class ``AoPath`` is used to manage ``Array of Paths``; it contains the subsequent methods.

Methods
^^^^^^^

  .. AoPath-Methods-label:
  .. table:: *AoPath Methods*

   +------------------------------------+----------------------------------------------------+
   |Name                                |Description                                         |
   +====================================+====================================================+
   |join                                |Join array of paths using the os separator          |
   +------------------------------------+----------------------------------------------------+
   |mkdirs                              |Make directories                                    |
   +------------------------------------+----------------------------------------------------+
   |show functions                                                                           |
   +------------------------------------+----------------------------------------------------+
   |sh_a_path                           |Show array of paths for path template.              |
   +------------------------------------+----------------------------------------------------+
   |sh_a_path_by_tpl                    |Convert array of path template keys and kwargs      |
   |                                    |Rto array of paths.                                 |
   +------------------------------------+----------------------------------------------------+
   |sh_aopath_by_gl-ob                  |                                                    |
   +------------------------------------+----------------------------------------------------+
   |sh_aopath_by_pac                    |                                                    |
   +------------------------------------+----------------------------------------------------+
   |sh_aopath_mtime_gt                  |                                                    |
   +------------------------------------+----------------------------------------------------+
   |sh_path_by_tpl_first_exist          |                                                    |
   +------------------------------------+----------------------------------------------------+
   |yield functions                                                                          |
   +------------------------------------+----------------------------------------------------+
   |yield_path_kwargs_over_path         |                                                    |
   +------------------------------------+----------------------------------------------------+
   |yield_path_kwargs_over_dir_path     |                                                    |
   +------------------------------------+----------------------------------------------------+
   |yield_path_item_kwargs_over_path_arr|                                                    |
   +------------------------------------+----------------------------------------------------+

AoPath Method: join
^^^^^^^^^^^^^^^^^^^
   
#. Convert array of paths (1.argument) by striping the leading or trailing os separator.

#. join the converted array of paths.

Parameter
"""""""""

  .. Parameter-of-AoPath-Method-join-label:
  .. table:: *Parameter of: AoPath Method: join*

   +------+--------+-------+--------------+
   |Name  |Type    |Default|Description   |
   +======+========+=======+==============+
   |aopath|TyAoPath|       |array of paths|
   +------+--------+-------+--------------+
   
Return Value
""""""""""""

  .. Return-Value-of-AoPath-Method-join-label:
  .. table:: *Return Value of: AoPath Method: join*

   +----+------+-----------+
   |Name|Type  |Description|
   +====+======+===========+
   |path|TyPath|Path       |
   +----+------+-----------+
   
AoPath Method: sh_a_path
^^^^^^^^^^^^^^^^^^^^^^^^

Convert path template to array of paths using glob function of module glob.py.

Parameter
"""""""""

  .. Parameter-of-AoPath-Method-sh_a_path-label:
  .. table:: *Parameter of: AoPath Method: sh_a_path*

   +----+------+-------+-----------+
   |Name|Type  |Default|Description|
   +====+======+=======+===========+
   |path|TyPath|       |Path       |
   +----+------+-------+-----------+
   
Return Value
""""""""""""

  .. Return-Value-of-AoPath-Method-sh_a_path-label:
  .. table:: *Return Value of: AoPath Method: sh_a_path*

   +------+--------+--------------+
   |Name  |Type    |Description   |
   +======+========+==============+
   |a_path|TyAoPath|Array of paths|
   +------+--------+--------------+
   
AoPath Method: sh_a_path_by_tmpl
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
#. Select array of path templates from keyword arguments (1.arguments) using the parameter

   * array of path template keys (1.argument);

#. join the array of path templates with the os separator

#. convert the created final path template to an array of paths.

Parameter
"""""""""

  .. Parameter-of-AoPath-Method-sh_a_path_by_tmpl-label:
  .. table:: *Parameter of: AoPath Method: sh_a_path_by_tmpl*

   +---------------+--------+-------+---------------------------+
   |Name           |Type    |Default|Description                |
   +===============+========+=======+===========================+
   |a_path_tmpl_key|TyAoPath|       |array of path template keys|
   +---------------+--------+-------+---------------------------+
   |kwargs         |TyDic   |       |keyword arguments          |
   +---------------+--------+-------+---------------------------+
   
Return Value
""""""""""""

  .. Return-Value-of-AoPath-Method-sh_a_path_by_tmpl-label:
  .. table:: *Return Value of: AoPath Method: sh_a_path_by_tmpl*

   +------+--------+-------+-----------+
   |Name  |Type    |Default|Description|
   +======+========+=======+===========+
   |a_path|TyAoPath|       |Path       |
   +------+--------+-------+-----------+
   
AoPath Method: yield_path_kwargs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
#. Create array of paths by executing the function sh_a_path_by_tmpl with the parameter:

   * array of path template keys (2.argument).
    
#. Loop over array of paths to yield:

   #. yield path, kwargs (3. argument)

Parameter
"""""""""

  .. Parameter-of-AoPath-Method-yield_path_kwargs-label:
  .. table:: *Parameter of: AoPath Method: yield_path_kwargs*

   +---------------+--------+-------+---------------------------+
   |Name           |Type    |Default|Description                |
   +===============+========+=======+===========================+
   |cls            |Tyclass |       |current class              |
   +---------------+--------+-------+---------------------------+
   |a_path_tmpl_key|TyAoPath|       |array of path template keys|
   +---------------+--------+-------+---------------------------+
   |kwargs         |TyDic   |       |keyword arguments          |
   +---------------+--------+-------+---------------------------+

Return Value
""""""""""""

  .. Return-Value-of-AoPath-Method-yield_path_kwargs-label:
  .. table:: *Return Value of: AoPath Method: yield_path_kwargs*

   +--------------+--------+-----------+
   |Name          |Type    |Description|
   +==============+========+===========+
   |(path, kwargs)|TyAoPath|Path       |
   +--------------+--------+-----------+
   
AoPath Method: yield_path_kwargs_new
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
Synopsis
""""""""

sh_a_path_by_tmpl(a_path_tmpl_key, kwargs)


Description
"""""""""""

#. Create array of directories by executing the function sh_a_path_by_tmpl with the arguments:

   * array of directory template keys (2.argument).

#. Loop over array of directories to:

   #. create kwargs_new by executing ths given function sh_kwargs_new (4. argument) with the arguments:

      * directory, given kwargs (5. argument) 

   #. create array of paths by executing the function sh_a_oath_by_tmpl with the arguments:

      * given array of path template keys (3. argument), kwargs_new

#. Loop over array of paths within the outer loop to:

   #. yield path, kwargs_new

Parameter
"""""""""

  .. Parameter-of-AoPath-Method-yield_path_kwargs_new-label:
  .. table:: *Parameter of: AoPath Method: yield_path_kwargs_new*

   +---------------+--------+-------+-----------------------------------+
   |Name           |Type    |Default|Description                        |
   +===============+========+=======+===================================+
   |cls            |Tyclass |       |Current class                      |
   +---------------+--------+-------+-----------------------------------+
   |a_dir_tmpl_key |TyAoPath|       |Array of path template keys        |
   +---------------+--------+-------+-----------------------------------+
   |a_path_tmpl_key|TyAoPath|       |Array of path template keys        |
   +---------------+--------+-------+-----------------------------------+
   |sh_kwargs_new  |TyAoPath|       |Show new keyword arguments function|
   +---------------+--------+-------+-----------------------------------+
   |kwargs         |TyDic   |       |Keyword arguments                  |
   +---------------+--------+-------+-----------------------------------+
   
Return Value
""""""""""""

  .. Return-Value-of-AoPath-Method-yield_path_kwargs_new-label:
  .. table:: *Return Value of: AoPath Method: yield_path_kwargs_new*

   +------------------+--------+---------------------------+
   |Name              |Type    |Description                |
   +==================+========+===========================+
   |(path, kwargs_new)|TyAoPath|Path, new keyword arguments|
   +------------------+--------+---------------------------+
   
AoPath Method: yield_path_item_kwargs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
#. Create array of paths by executing the function sh_a_path_by_tmpl with the arguments:

   * array of path template keys (2.argument).

#. Create array of items by selecting the value in the directory kwargs (4. argument) for
   the kwargs key (3. argument)

#. Loop over array of path and array of items to:

   #. yield path, item, kwargs (4. argument)

Parameter
"""""""""

  .. Parameter-of-AoPath-Method-yield_path_item_kwargs-label:
  .. table:: *Parameter of: AoPath Method: yield_path_item_kwargs*

   +---------------+--------+-------+---------------------------+
   |Name           |Type    |Default|Description                |
   +===============+========+=======+===========================+
   |cls            |Tyclass |       |current class              |
   +---------------+--------+-------+---------------------------+
   |a_path_tmpl_key|TyAoPath|       |array of path template keys|
   +---------------+--------+-------+---------------------------+
   |a_arr_key      |TyAoPath|       |array of path template keys|
   +---------------+--------+-------+---------------------------+
   |kwargs         |TyDic   |       |keyword arguments          |
   +---------------+--------+-------+---------------------------+
   
Return Value
""""""""""""

  .. Return Value-of-AoPath-Method-yield_path_item_kwargs-label:
  .. table:: *Return Value of: AoPath Method: yield_path_item_kwargs*

   +--------------------+--------+-----------------------------+
   |Name                |Type    |Description                  |
   +====================+========+=============================+
   |(path, item, kwargs)|TyAoPath|Path, Item, keyword arguments|
   +--------------------+--------+-----------------------------+
   
Method: AoPath.yield_path_item_kwargs_new
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   
#. Create array of directories by executing the function sh_a_path_by_tmpl with the parameter:

   * a_dir_tmpl_key (2.argument).

#. Create  array of items by selecting the value in the directory kwargs (4. argument) for
   the key arr_key (3. argument)

#. Loop over the array of directories to:

   #. create kwargs_new by executing ths function sh_kwargs_new (4. argument) with the arguments:

      * directory, given kwargs (5. argument) 

   #. create array of paths by executing the function sh_a_oath_by_tmpl with the arguments:

      * given array of path template keys (3. argument), kwargs_new

   #. Loop over array of path and array of items within the outer loop to:

      #. yield path, item, kwargs_new

Parameter
"""""""""

  .. Parameter-of-AoPath-Method-yield_path_item_kwargs_new-label:
  .. table:: *Parameter of: AoPath Method: yield_path_item_kwargs_new*

   +---------------+--------+-------+-----------------------------------+
   |Name           |Type    |Default|Description                        |
   +===============+========+=======+===================================+
   |cls            |Tyclass |       |current class                      |
   +---------------+--------+-------+-----------------------------------+
   |a_dir_tmpl_key |TyAoPath|       |array of path template keys        |
   +---------------+--------+-------+-----------------------------------+
   |a_path_tmpl_key|TyAoPath|       |array of path template keys        |
   +---------------+--------+-------+-----------------------------------+
   |sh_kwargs_new  |TyAoPath|       |show new keyword arguments function|
   +---------------+--------+-------+-----------------------------------+
   |kwargs         |TyDic   |       |keyword arguments                  |
   +---------------+--------+-------+-----------------------------------+
   
Return Value
""""""""""""

  .. Return-Value-of-AoPath-Method-yield_path_item_kwargs_new-label:
  .. table:: *Return Value of: AoPath Method: yield_path_item_kwargs_new*

   +------------------------+--------+---------------------------------+
   |Name                    |Type    |Description                      |
   +========================+========+=================================+
   |(path, item, kwargs_new)|TyAoPath|Path, Item, new keyword arguments|
   +------------------------+--------+---------------------------------+

*********************************************
Modules for Management of Dictionary of Paths
*********************************************

The Module Type ``Modules for Management of Dictionary of Paths`` contains the following Modules:

  .. Dictionaries-of-Paths-Management-Modules-label:
  .. table:: *Dictionaries of Paths Management Modules*

   +-----------+--------------------------------------------------+
   |Name       |Description                                       |
   +===========+==================================================+
   |dodopath.py|Management of Dictionary of Dictionaries of Paths.|
   +-----------+--------------------------------------------------+
   |dopath.py  |Management of Dictionary of Paths.                |
   +-----------+--------------------------------------------------+

Module: dodopath.py
===================

The Module ``dodoath.py`` contains the static Classes ``DoDoPath``.

Class: DoDoPath
---------------

The static Class ``DoDoPath`` is used to manage ``Dictionary of Dictionaries of Paths``; it contains the subsequent methods.

Methods
^^^^^^^

  .. DoDoPath-Methods-label:
  .. table:: *DoDoPath Methods*

   +-------+-----------+
   |Name   |Description|
   +=======+===========+
   |sh_path|Show Path. |
   +-------+-----------+

Module: dopath.py
==========-======

The Module ``doath.py`` contains the static Classes ``DoPath``.

Class: DoDoPath
---------------

The static Class ``DoPath`` is used to manage ``Dictionary of Paths``; it contains the subsequent methods.

Methods
^^^^^^^

  .. DoDoPath-Methods-label:
  .. table:: *DoDoPath Methods*

   +-------+-----------+
   |Name   |Description|
   +=======+===========+
   |sh_path|Show Path. |
   +-------+-----------+

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

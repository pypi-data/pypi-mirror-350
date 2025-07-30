##########
ka_uts_log
##########

********
Overview
********

.. start short_desc

**Log Management**

.. end short_desc

************
Installation
************

.. start installation

The package ``ka_uts_log`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: shell

	$ python -m pip install ka_uts_log

To install with ``conda``:

.. code-block:: shell

	$ conda install -c conda-forge ka_uts_log

.. end installation

***************
Package logging
***************

c.f.: **Appendix: Package Logging**

*************
Package files
*************

Classification
==============

The Package ``ka_uts_log`` consist of the following file types (c.f.: **Appendix**):

#. **Special files:** (c.f.: **Appendix:** *Special python package files*)

#. **Dunder modules:** (c.f.: **Appendix:** *Special python package modules*)

#. **Modules**

   #. *log.py*

#. **Special Sub-directories:** (c.f.: **Appendix:** *Special python package Sub-directories*)

   #. **cfg**

      a. *__init__.py*
      #. *log.std.yml*
      #. *log.usr.yml*

Special Sub-directory: cfg
==========================

Overview
--------

  .. Special-Sub-directory-cfg-Files-label:
  .. table:: *Special Sub directory cfg: Files*

   +-----------+-----------------------------------------+
   |Name       |Description                              |
   +===========+=========================================+
   |log.std.yml|Yaml definition file for standard logging|
   +-----------+-----------------------------------------+
   |log.usr.yml|Yaml definition file for user logging    |
   +-----------+-----------------------------------------+

Modules
=======

The Package ``ka_uts_log`` contains the following modules.

  .. ka_uts_log-Modules-label:
  .. table:: *ka_uts_log Modules*

   +------+-------------------------+
   |Name  |Decription               |
   +======+=========================+
   |log.py|Logging management module|
   +------+-------------------------+

Module: log.py of Package: ka_uts_log
=====================================

The Module ``log`` contains the following static classes.

Classes of Module: log
----------------------

  .. Classes-of-Module-log-label:
  .. table:: *Classes of Modul log*

   +------+--------------------------------------------+
   |Name  |Description                                 |
   +======+============================================+
   |LogEq |Management of Log Equate message, generated |
   |      |from a key-, value-pair.                    |
   +------+--------------------------------------------+
   |LogDic|Management of Log Equate messages, generated|
   |      |from the key-, value-pairs of a dictionary. |
   +------+--------------------------------------------+
   |Log   |Management of Log messages                  |
   +------+--------------------------------------------+

Class: Log of Modul: log.py
---------------------------

The static Class ``Log`` contains the subsequent display- and management-methods.

Display Methods of Class: Log
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  .. Log-Display-Methods-label:
  .. table:: *Log Display Methods*

   +--------+---------------------------------------------+
   |Name    |Description                                  |
   +========+=============================================+
   |debug   |Log debug message to debug destination.      |
   +--------+---------------------------------------------+
   |info    |Log info message to info destination.        |
   +--------+---------------------------------------------+
   |warning |Log warnning message to warning destination. |
   +--------+---------------------------------------------+
   |error   |Log error message to error destination.      |
   +--------+---------------------------------------------+
   |critcial|Log critical message to critical destination.|
   +--------+---------------------------------------------+

Management Methods of Class: Log
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  .. Log-Managment-Methods-label:
  .. table:: *Log Management Methods*

   +---------------+------------------------------------+
   |Name           |Description                         |
   +===============+====================================+
   |init           |initialise current class.           |
   +---------------+------------------------------------+
   |sh_calendar_ts |Show timestamp or datetime.         |
   +---------------+------------------------------------+
   |sh_dir_run     |Show run directory.                 |
   +---------------+------------------------------------+
   |sh_d_dir_run   |Show dictionary of run directories. |
   +---------------+------------------------------------+
   |sh_d_log_cfg   |Show log configuration directory.   |
   +---------------+------------------------------------+
   |sh_path_log_cfg|Show path of log configuration file.|
   +---------------+------------------------------------+
   |sh             |initialise and show current class.  |
   +---------------+------------------------------------+

Management Method: init of Class: Log
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
Parameter
"""""""""

  .. Log-method-init-Parameter-label:
  .. table:: *Log method init: Parameter*

   +---------+-----+-----------------+
   |Name     |Type |Description      |
   +=========+=====+=================+
   |cls      |class|current class    |
   +---------+-----+-----------------+
   |\**kwargs|TyAny|keyword arguments|
   +---------+-----+-----------------+


Class: LogEq of Modul: Log
--------------------------

The static Class ``LogEq`` of Module log.py contains the subsequent methods

Methods of Class LogEq
^^^^^^^^^^^^^^^^^^^^^^

  .. LogEq Methods-label:
  .. table:: *LogEq Methods*

   +--------+---------------------------------------------------------------------------+
   |Name    |Description                                                                |
   +========+===========================================================================+
   |debug   |Log generated equate message "<key> = <value>" to the debug destination.   |
   +--------+---------------------------------------------------------------------------+
   |info    |Log generated equate message "<key> = <value>" to the info destination.    |
   +--------+---------------------------------------------------------------------------+
   |warning |Log generated equate message "<key> = <value>" to the warning destination. |
   +--------+---------------------------------------------------------------------------+
   |error   |Log generated equate message "<key> = <value>" to the error destination.   |
   +--------+---------------------------------------------------------------------------+
   |critcial|Log generated equate message "<key> = <value>" to the critical destination.|
   +--------+---------------------------------------------------------------------------+

All Methods of Class: LogEq use the following Parameters:

Methods Parameter of Class: LogEq
"""""""""""""""""""""""""""""""""

  .. LogEq- Methods-parameter-label:
  .. table:: *LogEq Methods parameter*

   +-----+-----+-------------+
   |Name |Type |Description  |
   +=====+=====+=============+
   |cls  |class|current class|
   +-----+-----+-------------+
   |key  |TyAny|Key          |
   +-----+-----+-------------+
   |value|TyAny|Value        |
   +-----+-----+-------------+

Class: LogDic of Modul: log.py
------------------------------

The static Class ``LogDic`` of Module log.py contains the subsequent methods

Methods of Class: LogDic
^^^^^^^^^^^^^^^^^^^^^^^^

  .. LogDic-Methods-label:
  .. table:: *LogDic Methods*

   +--------+-------------------------------------------------------------------------------------+
   |Name    |Description                                                                          |
   +========+=====================================================================================+
   |debug   |Log generated equate messages for all dictionary entries to the debug destination.   |
   +--------+-------------------------------------------------------------------------------------+
   |info    |Log generated equate messages for all dictionary entries to the info destination.    |
   +--------+-------------------------------------------------------------------------------------+
   |warning |Log generated equate messages for all dictionary entries to the warning destination. |
   +--------+-------------------------------------------------------------------------------------+
   |error   |Log generated equate messages for all dictionary entries to the error destination.   |
   +--------+-------------------------------------------------------------------------------------+
   |critical|Log generated equate messages for all dictionary entries to the critical destination.|
   +--------+-------------------------------------------------------------------------------------+

All Methods of Class LogDic use the following Parameters:

Method Parameters of Class: LogDic
""""""""""""""""""""""""""""""""""

  .. LogDic-Methods-Parameter-label:
  .. table:: *LogDic Methods Parameter*

   +----+-----+-------------+
   |Name|Type |Description  |
   +====+=====+=============+
   |cls |class|current class|
   +----+-----+-------------+
   |dic |TyDic|Dictionary   |
   +----+-----+-------------+

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

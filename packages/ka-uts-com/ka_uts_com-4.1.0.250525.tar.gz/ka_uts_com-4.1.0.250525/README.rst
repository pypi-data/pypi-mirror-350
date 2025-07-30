##########
ka_uts_com
##########

********
Overview
********

.. start short_desc

**Communication and CLI Utilities**

.. end short_desc

************
Installation
************

.. start installation

The package ``ka_uts_com`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: shell

	$ python -m pip install ka_uts_com

To install with ``conda``:

.. code-block:: shell

	$ conda install -c conda-forge ka_uts_com

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

The Package ``ka_uts_com`` consist of the following file types (c.f.: **Appendix**):

#. **Special files:** (c.f.: **Appendix:** *Special python package files*)

#. **Dunder modules:** (c.f.: **Appendix:** *Special python package modules*)

#. **Modules**

   #. **Decorator Modules**

      a. *dec.py*

   #. **Communication Modules**

      a. *com.py*

   #. **Timer Modules**

      #. *timer.py*

   #. **Base Modules**

      a. *app.py*
      #. *cfg.py*
      #. *exit.py*

****************
Decorator Module
****************

Overview
========

  .. Decorator Module-label:
  .. table:: *Decorator Module*

   +------+----------------+
   |Name  |Decription      |
   +======+================+
   |dec.py|Decorator module|
   +------+----------------+

Decorator module: dec.py
========================

Decorator functions of modul: dec
---------------------------------

The Decorator Module ``dec.py`` contains the follwing decorator functions.

  .. Decorator-functions-of-module-dec-label:
  .. table:: *Decorator functions of module dec*

   +------------+-----------------+
   |Name        |Description      |
   +============+=================+
   |timer       |Timer            |
   +------------+-----------------+
   |handle_error|Handle exceptions|
   +------------+-----------------+

Decorator functions: timer of modul: dec
----------------------------------------
        
Parameter
^^^^^^^^^

  .. Parameter-of-decorator-function-timer-label:
  .. table:: *Parameter of decorator function timer*

   +----+----------+-----------+
   |Name|Type      |Description|
   +====+==========+===========+
   |fnc |TyCallable|function   |
   +----+----------+-----------+

********************
Communication Module
********************

Overview
========

  .. Communication Module-label:
  .. table:: *Communication Module*

   +------+-----------------------------+
   |Name  |Decription                   |
   +======+=============================+
   |com.py|Communication handling module|
   +------+-----------------------------+

Communication module: com.py
============================

The Communication Module ``com.py`` contains the single static class ``Com``.

com.py Class: Com
-----------------

The static Class ``Com`` contains the subsequent variables and methods.

Com: Variables
^^^^^^^^^^^^^^

  .. Com-Variables-label:
  .. table:: *Com: Variables*

   +------------+-----------+-------+---------------------------------------+
   |Name        |Type       |Default|Description                            |
   +============+===========+=======+=======================================+
   |cmd         |TyStr      |None   |Command                                |
   +------------+-----------+-------+---------------------------------------+
   |d_com_pacmod|TyDic      |{}     |Communication package module dictionary|
   +------------+-----------+-------+---------------------------------------+
   |d_app_pacmod|TyDic      |{}     |Application package module dictionary  |
   +------------+-----------+-------+---------------------------------------+
   |sw_init     |TyBool     |None   |Initialisation switch                  |
   +------------+-----------+-------+---------------------------------------+
   |tenant      |TyStr      |None   |Tenant name                            |
   +------------+-----------+-------+---------------------------------------+
   |**Timestamp fields**                                                    |
   +------------+-----------+-------+---------------------------------------+
   |ts          |TnTimeStamp|None   |Timestamp                              |
   +------------+-----------+-------+---------------------------------------+
   |d_timer     |TyDic      |False  |Timer dictionary                       |
   +------------+-----------+-------+---------------------------------------+
   |**Links to other Classes**                                              |
   +------------+-----------+-------+---------------------------------------+
   |App         |TyAny      |None   |Application class                      |
   +------------+-----------+-------+---------------------------------------+
   |cfg         |TyDic      |None   |Configuration dictionary               |
   +------------+-----------+-------+---------------------------------------+
   |Log         |TyLogger   |None   |Log class                              |
   +------------+-----------+-------+---------------------------------------+
   |Exit        |TyAny      |None   |Exit class                             |
   +------------+-----------+-------+---------------------------------------+

Methods of class: Com
^^^^^^^^^^^^^^^^^^^^^

  .. Com-Methods-label:
  .. table:: *Com Methods*

   +---------+-------------------------------------------------------+
   |Name     |Description                                            |
   +=========+=======================================================+
   |init     |Initialise static variables if they are not initialized|
   +---------+-------------------------------------------------------+
   |sh_kwargs|Show keyword arguments                                 |
   +---------+-------------------------------------------------------+

Com Method: init
^^^^^^^^^^^^^^^^
        
Parameter
"""""""""

  ..Com-Method-init-Parameter-label:
  .. table:: *Com Method init: Parameter*

   +---------+-----+-----------------+
   |Name     |Type |Description      |
   +=========+=====+=================+
   |cls      |class|current class    |
   +---------+-----+-----------------+
   |\**kwargs|TyAny|keyword arguments|
   +---------+-----+-----------------+

Com Method: sh_kwargs
^^^^^^^^^^^^^^^^^^^^^
        
Parameter
"""""""""

  .. Com-Method-sh_kwargs-Parameter-label:
  .. table:: *Com Method sh_kwargs: Parameter*

   +--------+-----+--------------------+
   |Name    |Type |Description         |
   +========+=====+====================+
   |cls     |class|current class       |
   +--------+-----+--------------------+
   |root_cls|class|root lass           |
   +--------+-----+--------------------+
   |d_parms |TyDic|parameter dictionary|
   +--------+-----+--------------------+
   |\*args  |list |arguments array     |
   +--------+-----+--------------------+

************
Timer Module
************

Overview
========

  .. Timer Modules-label:
  .. table:: *Timer Modules*

   +--------+-----------------------------+
   |Name    |Decription                   |
   +========+=============================+
   |timer.py|Timer management module      |
   +--------+-----------------------------+

Timer module: timer.py
======================

timer.py: Classes
-----------------

The Module ``timer.py`` contains the following classes


  .. timer.py-Classes-label:
  .. table:: *timer.py classes*

   +---------+------+---------------+
   |Name     |Type  |Description    |
   +=========+======+===============+
   |Timestamp|static|Timestamp class|
   +---------+------+---------------+
   |Timer    |static|Timer class    |
   +---------+------+---------------+

timer.py Class: Timer
---------------------

Timer: Methods
^^^^^^^^^^^^^^

  .. Timer-Methods-label:
  .. table:: *Timer Methods*

   +----------+------------------------------------+
   |Name      |Description                         |
   +==========+====================================+
   |sh_task_id|Show task id                        |
   +----------+------------------------------------+
   |start     |Start Timer                         |
   +----------+------------------------------------+
   |end       |End Timer and Log Timer info message|
   +----------+------------------------------------+

Timer Method: sh_task_id
^^^^^^^^^^^^^^^^^^^^^^^^
        
Show task id, which is created by the concatination of the following items if they are defined:
#. package,
#. module,
#. class_name,
#. parms
The items package and module are get from the package-module directory;
The item class_name is the class_id if its a string, otherwise the attribute
__qualname__ is used.
        
Parameter
"""""""""

  .. Parameter-of-Timer-Method-sh_task_id-label:
  .. table:: *Parameter of: Timer Method sh_task_id*

   +--------+-----+-----------------+
   |Name    |Type |Description      |
   +========+=====+=================+
   |d_pacmod|TyDic|pacmod dictionary|
   +--------+-----+-----------------+
   |class_id|TyAny|Class Id         |
   +--------+-----+-----------------+
   |parms   |TnAny|Parameters       |
   +--------+-----+-----------------+
   |sep     |TyStr|Separator        |
   +--------+-----+-----------------+

Return Value
""""""""""""

  .. Timer-Method-sh_task_id-Return-Value-label:
  .. table:: *Timer Method sh_task_id: Return Value*

   +----+-----+-----------+
   |Name|Type |Description|
   +====+=====+===========+
   |    |TyStr|Task Id    |
   +----+-----+-----------+

Timer Method: start
^^^^^^^^^^^^^^^^^^^
        
Parameter
"""""""""

  .. Parameter-of-Timer-Method-start-Parameter-label:
  .. table:: *Timer Method start: Parameter*

   +--------+-----+-------------+
   |Name    |Type |Description  |
   +========+=====+=============+
   |cls     |class|current class|
   +--------+-----+-------------+
   |class_id|TyAny|Class Id     |
   +--------+-----+-------------+
   |parms   |TnAny|Parameter    |
   +--------+-----+-------------+
   |sep     |TyStr|Separator    |
   +--------+-----+-------------+

Timer Method: end
^^^^^^^^^^^^^^^^^
        
Parameter
"""""""""

  .. Parameter-of-Timer-Method-end-label:
  .. table:: *Parameter of: Timer Method end*

   +--------+-----+-------------+
   |Name    |Type |Description  |
   +========+=====+=============+
   |cls     |class|current class|
   +--------+-----+-------------+
   |class_id|TyAny|Class Id     |
   +--------+-----+-------------+
   |parms   |TnAny|Parameter    |
   +--------+-----+-------------+
   |sep     |TyStr|Separator    |
   +--------+-----+-------------+

************
Base Modules
************

Overview
========

  .. Base Modules-label:
  .. table:: *Base Modules*

   +---------+----------------------------+
   |Name     |Decription                  |
   +=========+============================+
   |app\_.py |Application setup module    |
   +---------+----------------------------+
   |cfg\_.py |Configuration setup module  |
   +---------+----------------------------+
   |exit\_.py|Exit Manafement setup module|
   +---------+----------------------------+

Base module: app\_.py
=====================

The Module ``app\_.py`` contains a single static class ``App_``.

Class: App\_
------------

The static class ``App_`` contains the subsequent static variables and methods

App\_: Static Variables
^^^^^^^^^^^^^^^^^^^^^^^

  .. Appl\_ Static-Variables-label:
  .. table:: *Appl\_ tatic Variables*

   +---------------+-------+-------+---------------------+
   |Name           |Type   |Default|Description          |
   +===============+=======+=======+=====================+
   |sw_init        |TyBool |False  |initialisation switch|
   +---------------+-------+-------+---------------------+
   |httpmod        |TyDic  |None   |http modus           |
   +---------------+-------+-------+---------------------+
   |sw_replace_keys|TnBool |False  |replace keys switch  |
   +---------------+-------+-------+---------------------+
   |keys           |TnArr  |None   |Keys array           |
   +---------------+-------+-------+---------------------+
   |reqs           |TyDic  |None   |Requests dictionary  |
   +---------------+-------+-------+---------------------+
   |app            |TyDic  |None   |Appliction dictionary|
   +---------------+-------+-------+---------------------+

App\_: Methods
^^^^^^^^^^^^^^

  .. App\_-Methods-label:
  .. table:: *App\_ Methods*

   +----+------+------------------------------------+
   |Name|Type  |Description                         |
   +====+======+====================================+
   |init|class |initialise static variables of class|
   |    |      |if they are not allready initialized|
   +----+------+------------------------------------+
   |sh  |class |show (return) class                 |
   +----+------+------------------------------------+

App\_ Method: init
^^^^^^^^^^^^^^^^^^
        
Parameter
"""""""""

  .. Parameter-of-App\_-Method-init-label:
  .. table:: *Parameter of: App\_ Method init*

   +---------+-----+-----------------+
   |Name     |Type |Description      |
   +=========+=====+=================+
   |cls      |class|Current class    |
   +---------+-----+-----------------+
   |\**kwargs|TyAny|Keyword arguments|
   +---------+-----+-----------------+

App\_ Method: sh
^^^^^^^^^^^^^^^^
        
  .. App\_-Method-sh-label:
  .. table:: *App\_ Method: sh*

   +---------+-----+-----------------+
   |Name     |Type |Description      |
   +=========+=====+=================+
   |cls      |class|Current class    |
   +---------+-----+-----------------+
   |\**kwargs|TyAny|Keyword arguments|
   +---------+-----+-----------------+

Return Value
""""""""""""

  .. App\_-Method-sh-Return-Value-label:
  .. table:: *App\_ Method sh: Return Value*

   +----+--------+-----------+
   |Name|Type    |Description|
   +====+========+===========+
   |log |TyLogger|Logger     |
   +----+--------+-----------+

Base module: cfg\_.py
=====================

The Base module cfg\_.py contains a single static class ``Cfg_``.

cfg\_.py Class Cfg\_
---------------------

The static class ``Cfg_`` contains the subsequent static variables and methods

Cfg\_Static Variables
^^^^^^^^^^^^^^^^^^^^^

  .. Cfg\_-Static-Variables-label:
  .. table:: *Cfg\_ Static Variables*

   +----+-----+-------+--------------------+
   |Name|Type |Default|Description         |
   +====+=====+=======+====================+
   |cfg |TyDic|None   |Configuration object|
   +----+-----+-------+--------------------+

Cfg\_ Methods
^^^^^^^^^^^^^

  .. Cfg\_-Methods-label:
  .. table:: *Cfg\_ Methods*

   +----+------+-----------------------------------+
   |Name|Type  |Description                        |
   +====+======+===================================+
   |sh  |class |read pacmod yaml file into class   |
   |    |      |variable cls.dic and return cls.cfg|
   +----+------+-----------------------------------+

Cfg\_ Method: sh
^^^^^^^^^^^^^^^^
        
Parameter
"""""""""

  .. Cfg\_-Method-sh-Parameter-label:
  .. table:: *Cfg\_ Method sh: Parameter*

   +--------+--------+-----------------+
   |Name    |Type    |Description      |
   +========+========+=================+
   |cls     |class   |Current class    |
   +--------+--------+-----------------+
   |log     |TyLogger|Logger           |
   +--------+--------+-----------------+
   |d_pacmod|TyDic   |pacmod dictionary|
   +--------+--------+-----------------+

Return Value
""""""""""""

  .. Cfg\_-Method-sh-Return-Value-label:
  .. table:: *Cfg\_ Method sh: Return Value*

   +-------+-----+-----------+
   |Name   |Type |Description|
   +=======+=====+===========+
   |cls.cfg|TyDic|           |
   +-------+-----+-----------+

Base Modul: exit\_.py
=====================

The Base module exit\_.py contains a single static class ``Ext_``.

exit\_.py class: Exit\_
-----------------------

The static Class ``Exit_`` of Module exit\_.py contains the subsequent static variables and methods.

Exit\_: Variables
^^^^^^^^^^^^^^^^^

  .. Exit\_-Variables-label:
  .. table:: *Exit\_ Variables*

   +--------------+------+-------+---------------------+
   |Name          |Type  |Default|Description          |
   +==============+======+=======+=====================+
   |sw_init       |TyBool|False  |initialisation switch|
   +--------------+------+-------+---------------------+
   |sw_critical   |TyBool|False  |critical switch      |
   +--------------+------+-------+---------------------+
   |sw_stop       |TyBool|False  |stop switch          |
   +--------------+------+-------+---------------------+
   |sw_interactive|TyBool|False  |interactive switch   |
   +--------------+------+-------+---------------------+

Exit\_: Methods
^^^^^^^^^^^^^^^

  .. Exit\_-Methods-label:
  .. table:: *Exit\_ Methods*

   +----+------+------------------------------------+
   |Name|Method|Description                         |
   +====+======+====================================+
   |init|class |initialise static variables of class|
   |    |      |if they are not allready initialized|
   +----+------+------------------------------------+
   |sh  |class |show (return) class                 |
   +----+------+------------------------------------+

Exit\_: Method: init
^^^^^^^^^^^^^^^^^^^^
        
Parameter
"""""""""

  .. Exit\_-Method-init-Parameter:
  .. table:: *Exit\_ Method init: Parameter*

   +---------+-----+-----------------+
   |Name     |Type |Description      |
   +=========+=====+=================+
   |cls      |class|Current class    |
   +---------+-----+-----------------+
   |\**kwargs|TyAny|Keyword arguments|
   +---------+-----+-----------------+

Exit\_: Method: sh
^^^^^^^^^^^^^^^^^^
        
Parameter
"""""""""

  .. Exit\_-Method-sh-Parameter:
  .. table:: *Exit\_ Method sh: Parameter*

   +---------+-----+-----------------+
   |Name     |Type |Description      |
   +=========+=====+=================+
   |cls      |class|Current class    |
   +---------+-----+-----------------+
   |\**kwargs|TyAny|Keyword arguments|
   +---------+-----+-----------------+

Return Value
""""""""""""

  .. Exit\_-Method-sh-Return-Value:
  .. table:: *Exit\_ Method sh: Return Value*

   +----+-----+-------------+
   |Name|Type |Description  |
   +====+=====+=============+
   |cls |class|Current class|
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

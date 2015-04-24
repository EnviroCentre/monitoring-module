Introduction
============

The HEC-DSS Monitoring Module includes a set of jython scripts that can be used 
to rapidly set up "tools" to execute various automated tasks in HEC-DSSVue. 


Workflow
--------

The following workflow is assumed:

 1. A `yaml` configuration file defines the tool's input parameters. The 
    configuration file is saved alongside the HEC-DSS `.dss` file.

 2. The :class:`toolbox.Tool` is sub-classed to define the tool. The method
    :meth:`toolbox.Tool.main` includes the task logic (e.g. importing data,  
    creating plots, etc.).

 3. The tool is run using the :meth:`toolbox.Tool.run` method.

Example toolbox
---------------

Example of a HEC-DSS script using the :class:`toolbox.Tool`:

.. code-block:: python

    # name=Example tool
    # displayinmenu=true
    # displaytouser=true
    # displayinselector=true

    import toolbox
    from some_module import do_something

    CONFIG_FILE = 'input.yml'  # Relative to DSS-file

    class ExampleTool(toolbox.Tool):
        requiredParams = ['folder', 'files', 'site', ...]
        refreshCatalogue = 1  # Update catalogue when completed

        def main(self):
            do_something(self.config, self.dssFilePath)
            self.message = "Test tool successfully completed."

    tool = ExampleTool(CONFIG_FILE)
    tool.run()


The above code should be saved in a file like this
:file:`%APPDATA%/Roaming/HEC/HEC-DSSVue/scripts/example_tool.py` for it to show
up in the HEC-DSSVue :menuselection:`Script` menu and toolbar.

The corresponding configuration file :file:`input.yml` could look like this.

.. code-block:: yaml

    folder: C:\some\folder
    files:
     - file 1.txt
     - file 2.txt

    site: Site name
    ...


"Fixing" the HEC-DSSVue configuration
-------------------------------------

All scripts are executed within the HEC-DSSVue application (Java-based) using an
embedded Python interpreter, Jython 2.2. This version of Jython was released in
2007 and does not have the same functionality as recent releases of Python 2.7 
and 3.x. 

.. note::
   
   The most recent yaml parsers available for Python do not work with Jython 
   2.2. An archived version of a `legacy yaml parser 
   <http://pyyaml.org/wiki/PyYAMLLegacy>`_ has therefore been included in the 
   HEC-DSS Monitoring Module. This parser does unfortunately not support the 
   full yaml spec!

Python search path
~~~~~~~~~~~~~~~~~~

HEC-DSSVue scripts are saved in the 
:file:`%APPDATA%/Roaming/HEC/HEC-DSSVue/scripts` folder. Scripts in this folder
can be run directly from HEC-DSSVue window.

The scripts folder is not available on the Python search path by default and 
this prevents any imports to Python modules in the same folder. The only way to 
fix this is by modifying the ``vmparam -Dpython.path`` variable in the file
:file:`%programfiles(x86)%/HEC/HEC-DSSVue/HEC-DSSVue.config` like this::

  vmparam -Dpython.path=jar\sys\jythonLib.jar\lib;jar\sys\jythonUtils.jar;$APPDATA\HEC\HEC-DSSVue\scripts

Jython configuration
~~~~~~~~~~~~~~~~~~~~

On Windows operating systems released since 2009, Jython 2.2 throws an error as
it assumes the operating system being Linux. To fix this, add the file
:file:`%HOME%/.jython` with the following content::

  python.os=nt

Debugging in HEC-DSSVue
~~~~~~~~~~~~~~~~~~~~~~~

To make debugging scripts in HEC-DSSVue easier, the Java console window can be
shown when starting HEC-DSSVue by setting ``showConsole true`` in the 
:file:`HEC-DSSVue.config` file. Java and Jython errors will be displayed in this
window.

Alternatively the console output can be inspected from the HEC-DSSVue menu
:menuselection:`Advanced --> Console Output...`.

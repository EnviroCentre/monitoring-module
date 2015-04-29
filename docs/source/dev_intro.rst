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

    class ExampleTool(toolbox.Tool):
        requiredParams = ['folder', 'files', 'site', ...]
        refreshCatalogue = 1  # Update catalogue when completed

        def main(self):
            do_something(self.config, self.dssFilePath)
            self.message = "Test tool successfully completed."

    tool = ExampleTool()
    tool.run()


The above code should be saved in a file like this
:file:`%APPDATA%/Roaming/HEC/HEC-DSSVue/scripts/example_tool.py` for it to show
up in the HEC-DSSVue :menuselection:`Script` menu and toolbar.

The corresponding configuration file, for example :file:`input.yml`, could look
like this.

.. code-block:: yaml

    folder: C:\some\folder
    files:
     - file 1.txt
     - file 2.txt

    site: Site name
    ...


The user is prompted to select the configuration file when running the tool. 
Alternatively, the tool can be created like this::

    tool = ExampleTool(configFileName, fullPathToDssFile)

This would be suitable for unattended execution of the tool.


"Fixing" the HEC-DSSVue configuration
-------------------------------------

HEC-DSSVue scripts are saved in the 
:file:`%APPDATA%/Roaming/HEC/HEC-DSSVue/scripts` folder. Scripts in this folder
can be run directly from HEC-DSSVue window.

All scripts are executed within the HEC-DSSVue application (Java-based) using an
embedded Python interpreter, Jython 2.2 (a very old version). Install the 
`Jython upgrade for HEC-DSSVue 
<https://github.com/EnviroCentre/jython-upgrade>`_ to upgrade to the most recent
stable version of Jython. This will also modify the Python search path to 
include the scripts folder.


Debugging in HEC-DSSVue
-----------------------

To make debugging scripts in HEC-DSSVue easier, the Java console window can be
shown when starting HEC-DSSVue by setting ``showConsole true`` in the 
:file:`%programfiles(x86)%/HEC/HEC-DSSVue/HEC-DSSVue.config` file. Java and 
Jython errors will be displayed in this window.

Alternatively the console output can be inspected from the HEC-DSSVue menu
:menuselection:`Advanced --> Console Output...`.

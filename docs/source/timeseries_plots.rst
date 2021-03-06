Creating timeseries plots (locations combined)
==============================================

A series of timeseries plots can be exported using the `Monitoring Module` for 
a range of locations and parameters. One graph is created for each parameter
showing all locations combined.


Getting everything in place
---------------------------

In this example, the following project file structure is used:: 

    C:\
        Project\
            Output\
                (empty)
            Monitoring data.dss
            plots.yml

The :file:`Monitoring data.dss` file includes some data for site `Example site`
(A-part), locations `L1` and `L2` (B-part) for a range of parameters at a 
15-minute interval and version `OBS` (F-part).


The configuration file
----------------------

The configuration file :file:`plots.yml` can be created as a simple text
file with the following content:

.. code-block:: yaml

    site: Example site
    locations:
    - LOCATION 1
    - LOCATION 2
    interval: 15MIN
    version: OBS

    output_folder: Output

    period:
      start: 01JAN2000 00:00
      end:   01JAN2001 00:00

    params:
      DO:
        scale: log
      DO%:
        scale: log
      EC:
        scale: log
      PH:
      TEMP:
      TURB:
        scale: log
      ORP:
    

.. tip::

   The configuration file is structured according to the `YAML format 
   <http://yaml.org>`_. Indentation is important to define the configuration 
   correctly. The example is best copied exactly as provided!


The configuration file lists the locations and parameters to plot as well as 
the folder to export the images into. 

 - The ``output_folder`` is relative to the location of the 'yml' config file.
 - The horizontal axis is limited to the period defined by the ``start`` and
   ``end`` settings. These must be formatted as date/times as in the example.
 - The vertical axis can be set to a logarithmic scale by setting the 
   parameter's ``scale`` configuration to `log`. If the parameter values are 
   zero or less, the axis is always linear and a warning message is displayed.

Creating the plots
------------------

When the configuration has been set up, the plots can be generated as follows:

 1. Open the :file:`Monitoring data.dss` file in HEC-DSSVue.
 2. Select menu item :menuselection:`Scripts --> Monitoring plots` or 
    alternatively click on :menuselection:`Monitoring plots` on the toolbar.
 3. Choose the configuration file :file:`plots.yml` in the file selection 
    window. 

The plots are briefly shown on the screen as they are created and then exported
into the ``output_folder`` as `JPG`-files.

Adding threshold lines
----------------------

One or multiple horizontal lines can be added to the graphs by including a
section like this in the configuration file:
    
.. code-block:: yaml

    thresholds:
      DO:
        all: 
          10: upper threshold
          8.5: lower threshold
      TURB:
        all: 
          1000: trigger value

Where ``all`` refers to all locations.

Optional settings
-----------------

The following settings are optional and the defaults can be overriden if 
required:

.. code-block:: yaml

    width: 1200
    height: 800

    line:
      markers: yes
      width: 2
      colours:
      - [166, 206, 227]
      - [ 31, 120, 180]
      - [178, 223, 138]
      - [ 51, 160,  44]
      - [251, 154, 153]
      - [227,  26,  28]
      - [253, 191, 111]
      - [255, 127,   0]
      - [202, 178, 214]
      - [106,  61, 154]

Explanation:

 - The ``width`` and ``height`` settings define the dimensions of the plot
   window in pixels. The actual exported image is slightly smaller than this.
 - A set of colours for individual curves on the graph (one for each location)
   is set by the ``line``, ``colours`` settings which is a list of RGB colour
   values. If there are more locations than in the colours list, the colours at
   the beginning of the list are used twice.
 - Line symbol markers can be switched off by setting ``markers`` to ``no``.

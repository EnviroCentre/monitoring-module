Creating timeseries plots
=========================

A series of timeseries plots can be exported using the `Monitoring Module` for 
a range of locations and parameters. One graph is created for each parameter
showing all locations.


Plotting example
----------------

Getting everything in place
~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~~~

The configuration file :file:`plots.yml` can be created as a simple text
file with the following content:

.. code-block:: yaml

    site: Example site
    locations:
     - L1
     - L2
    interval: 15MIN
    version: OBS

    output_folder: Output

    period:
      start: 01JAN2000 00:00
      end:   31DEC2000 24:00

    params:
      DO:
        scale: log
      DO%:
        scale: log
      EC:
        scale: log
      PH:
        scale: lin
      TEMP:
        scale: lin
      TURB:
        scale: log
      ORP:
        scale: lin

    width: 1200
    height: 800

    line:
      width: 1.25
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

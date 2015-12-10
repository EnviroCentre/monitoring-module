Creating timeseries plots with thresholds
=========================================

A series of timeseries plots with one or more threshold lines can be exported 
using the `Monitoring Module` for a range of locations and parameters. One graph
is created per parameter, per location.


Getting everything in place
---------------------------

In this example, the following project file structure is used:: 

    C:\
        Project\
            Output\
                (empty)
            Monitoring data.dss
            threshold_plots.yml

The :file:`Monitoring data.dss` file includes some data for site `Example site`
(A-part), locations `L1` and `L2` (B-part) for a range of parameters at a 
15-minute interval and version `OBS` (F-part).


The configuration file
----------------------

The configuration file :file:`threshold_plots.yml` can be created as a simple 
text file with the following content:

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

    thresholds:
      DO:
        LOCATION 1: 
          10: threshold
        LOCATION 2: 
          12: upper threshold
          8.5: lower threshold
      TURB:
        LOCATION 1: 
          1000: trigger value
        LOCATION 2: 
          1000: trigger value

    params:
      DO:
      DO%:
      EC:
        scale: log
      PH:
      TEMP:
      TURB:
        scale: log
      ORP:
    
The configuration file lists the locations and parameters to plot as well as 
the folder to export the images into. 

Multiple thresholds can be specified per parameter, per location using the 
``thresholds`` section like this: :samp:`{numeric value}: {line label}`


Creating the plots
------------------

When the configuration has been set up, the plots can be generated as follows:

 1. Open the :file:`Monitoring data.dss` file in HEC-DSSVue.
 2. Select menu item :menuselection:`Scripts --> Monitoring threshold plots` or 
    alternatively click on :menuselection:`Monitoring threshold plots` on the 
    toolbar.
 3. Choose the configuration file :file:`threshold_plots.yml` in the file
    selection window. 

The plots are briefly shown on the screen as they are created and then exported
into the ``output_folder`` as `JPG`-files.


Baseline statistics thresholds
------------------------------

Instead of specifying the value for a threshold line, the `Monitoring Module` 
can also plot horizontal lines based on summary statistics of the baseline 
period. Supported statistics are:

 - mean
 - any number of standard deviations above or below the mean

Statistic thresholds are specified like this: 
:samp:`{statistic}: {line label}` where :samp:`{statistic}` is one of ``mean``, 
:samp:`+{n}sd` or :samp:`-{n}sd`.

Or with an example within the config file (for example :file:`threshold_plots.yml`):

.. code-block:: yaml

    thresholds:
      DO:
        LOCATION 1: 
          mean: baseline average
          +2sd: +2 std. dev.
        LOCATION 2: 
          mean: baseline average
          +2sd: +2 std. dev.
          -2sd: -2 std. dev.

If a parameter is plotted on a log scale (as specified in the ``params`` 
section), the statistics are computed on a log scale. The baseline dataset is 
log-transformed before calculating the mean and standard deviation.

The baseline period itself is specified like this:

.. code-block:: yaml

    baseline:
      all:
        start: 01MAR2014 00:00
        end:   01JUL2014 00:00 
      LOCATION 2:
        start: 01MAR2014 00:00
        end:   01SEP2014 00:00

The ``all`` section specifies the baseline period for all locations within the
site and other locations can be overridden as shown if there are differences
between the locations.

The end of the baseline period is shown on the plot by a vertical line.


Optional settings
-----------------

The following settings are optional and the defaults can be overriden if 
required:

.. code-block:: yaml
    
    width: 1200
    height: 300

    line:
      markers: yes
      width: 2
      colour: [166, 206, 227]

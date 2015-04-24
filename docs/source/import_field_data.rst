Importing "field" data
======================

The Monitoring Module can be used to import water quality data collected in the
field with a handheld meter. The measured parameters are exported from the meter
to a `csv`-file with the measurement **locations** forming the columns 
(**across**) and the **parameters** in rows (**down**).

Multiple `csv`-files can be imported at once.

.. note::

   The Monitoring Module's field data importing tool has been tested to work
   with the following meters:

    - Hanna Instruments® multi-parameter meter type HI 9828

   Other meters and `csv` input file formats may be supported by tweaking the 
   tool's configuration parameters.


Data import example
-------------------

Getting everything in place
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this example, the file to be imported :file:`2015-01 Site measurements.csv`
is saved in a project file structure as follows:: 

    C:\
        Project\
            Import data\
                2015-01 Site measurements.csv
            Monitoring data.dss
            field_import.yml

The configuration file
~~~~~~~~~~~~~~~~~~~~~~

The configuration file :file:`field_import.yml` can be created as a simple text
file with the following content:

.. code-block:: yaml

    folder: C:\Project\Import data
    files:
     - 2015-01 Site measurements.csv

    site: Example site
    version: RAW

    columns:
      date: 1
      time: 2
      location: 21

    params:
      TEMP:
        column: 3
        unit: degC
      PH:
        column: 4
        unit: "-"
      DO%:
        column: 7
        unit: %
      DO:
        column: 8
        unit: mg/l
      EC:
        column: 9
        unit: µS/cm


.. tip::

   The configuration file is structured according to the `YAML format 
   <http://yaml.org>`_. Indentation is important to define the configuration 
   correctly. The example is best copied exactly as provided!


The configuration file describes the files to be imported as well as information
about which `csv`-file columns to be imported. Measured parameter columns can be 
modified as required by editing the ``params`` section of the configuration 
file.

Parameter values in the import file starting with `<` are interpreted as being 
below the meter's limit of detection (LOD). Such measurements are imported as 
50% of the LOD to allow numeric evaluations and plotting in line with current 
best practice.


.. warning::
   
   The date column is assumed to be formatted as ``yyyy/mm/dd``! 

   If the time column is omitted all times are set to 12:00:00 hrs.


Running the import
~~~~~~~~~~~~~~~~~~

When the configuration has been set up, the data can be imported as follows:

 1. Open the :file:`Monitoring data.dss` file in HEC-DSSVue.
 2. Select menu item :menuselection:`Scripts --> Import field data` or 
    alternatively click on :menuselection:`Import field data` on the toolbar. 

When successfully completed, a message is displayed how many records have been 
imported and the catalogue is refreshed.

Data post-processing
~~~~~~~~~~~~~~~~~~~~

In this example, data were imported using `RAW` for the data version (F-part). 
This allows review of data and corrections and manipulations using the
HEC-DSSVue built-in functionality. Quality assured data can then be saved using
a different version, for example `OBS`.

Importing logger data
=====================

The `Monitoring Module` can be used to import continuous logger data. The 
timeseries data are first exported into a `csv`-file with one row per interval
(timestep) and one or multiple columns for the recorded parameters. 

Each `csv`-file represents a single monitoring location. Multiple `csv`-files
can be imported at once.

.. note::

   The Monitoring Module's logger data importing tool has been tested to work
   with the following loggers:

    - In-Situ® Troll 9000 Pro XP

   Other loggers and `csv` input file formats may be supported by tweaking the 
   tool's configuration parameters.


Getting everything in place
---------------------------

In this example, the file to be imported :file:`2015-01 Logger results.csv`
is saved in a project file structure as follows:: 

    C:\
        Project\
            Import data\
                2015-01 Logger results.csv
            Monitoring data.dss
            logger_import.yml

The configuration file
----------------------

The configuration file :file:`logger_import.yml` can be created as a simple text
file with the following content:

.. code-block:: yaml

    folder: C:\Project\Import data
    files:
      2015-01 Logger results.csv: Location A

    site: Site name
    version: RAW

    date_format: "%d/%m/%Y"

    mapping:
      Temperature: TEMP
      Turbidity: TURB
      pH: PH
      Rugged DO Sat: DO%
      Rugged DO: DO
      Conductivity: EC

    params:
      TEMP:
        unit: degC
      TURB:
        unit: FNU
      PH:
        unit: "-"
      DO%:
        unit: "%"
      DO:
        unit: mg/l
      EC:
        unit: µS/cm


The configuration file describes the files to be imported as well as information
about which `csv`-file parameter columns to be imported. The ``mapping`` section
of the configuration file indicates which column headings map onto the 
parameters to be saved into the database. Special symbols (non-ASCII characters)
should be omitted from the ``mapping`` section.

.. important::

   Unlike the other import tools, the ``files`` section lists the file names 
   without a dash ``-``. Instead, the files are listed as a series of `key`: 
   `value` pairs like this::
   
       files:
         file name 1.csv: location name A
         file name 2.csv: location name B

Parameter values in the import file starting with `<` are interpreted as being 
below the meter's limit of detection (LOD). Such measurements are imported as 
50% of the LOD to allow numeric evaluations and plotting in line with current 
best practice.


Running the import
------------------

When the configuration has been set up, the data can be imported as follows:

 1. Open the :file:`Monitoring data.dss` file in HEC-DSSVue.
 2. Select menu item :menuselection:`Scripts --> Import logger data` or 
    alternatively click on :menuselection:`Import logger data` on the toolbar.
 3. Choose the configuration file :file:`logger_import.yml` in the file s
    election window. 


When successfully completed, a message is displayed how many records have been 
imported and the catalogue is refreshed.

Data post-processing
--------------------

In this example, data were imported using `RAW` for the data version (F-part). 
This allows review of data and corrections and manipulations using the
HEC-DSSVue built-in functionality. Quality assured data can then be saved using
a different version, for example `OBS`.

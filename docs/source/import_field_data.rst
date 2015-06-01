Importing "field" data
======================

The `Monitoring Module` can be used to import water quality data collected in
the field with a handheld meter. The measured parameters are exported from the 
meter to a `csv`-file with the **parameters** forming the columns (**across**)
and the **locations** in rows (**down**).

Multiple `csv`-files can be imported at once.

.. note::

   The Monitoring Module's field data importing tool has been tested to work
   with the following meters:

    - Hanna Instruments® multi-parameter meter type HI 9828

   Other meters and `csv` input file formats may be supported by tweaking the 
   tool's configuration parameters.


Getting everything in place
---------------------------

In this example, the file to be imported :file:`2015-01 Site measurements.csv`
is saved in a project file structure as follows:: 

    C:\
        Project\
            Import data\
                2015-01 Site measurements.csv
            Monitoring data.dss
            field_import.yml

The configuration file
----------------------

The configuration file :file:`field_import.yml` can be created as a simple text
file with the following content:

.. code-block:: yaml

    folder: C:\Project\Import data
    files:
     - 2015-01 Site measurements.csv

    site: Example site
    version: RAW

    columns:
      date: 
        title: Date
        format: "%Y/%m/%d"
      time: 
        title: Time
      location: 
        title: Location

    mapping:
      C: TEMP
      pH: PH
      DO %: DO%
      DO mg/l: DO
      S/cm: EC

    params:
      TEMP:
        unit: degC
      PH:
        unit: "-"
      DO%:
        unit: "%"
      DO:
        unit: mg/l
      EC:
        unit: µS/cm


.. tip::

   The configuration file is structured according to the `YAML format 
   <http://yaml.org>`_. Indentation is important to define the configuration 
   correctly. The example is best copied exactly as provided!


The configuration file describes the files to be imported as well as information
about which `csv`-file columns to be imported. The ``mapping`` section of the 
configuration file indicates which column headings map onto the parameters to be
saved into the database. Special symbols (non-ASCII characters) should be 
omitted from the ``mapping`` section.

The following tags can be used to specify the date format:

=== ============== === ===================== === ==============
Day                Month                     Year
------------------ ------------------------- ------------------
Tag Example        Tag Example               Tag Example
=== ============== === ===================== === ==============
%d  01, 02, .., 31 %b  Jan, Feb, ..          %y  00, 01, .., 99
|                  %B  January, February, .. %Y  1970, 2013, ..
|                  %m  01, 02, .., 12        |
=== ============== === ===================== === ==============

The `time` column is optional. If not specified, all times are set to 
12:00:00 hrs. The time format is always assumed to be ``%H:%M:%S``.

Parameter values in the import file starting with `<` are interpreted as being 
below the meter's limit of detection (LOD). Such measurements are imported as 
50% of the LOD to allow numeric evaluations and plotting in line with current 
best practice.


Running the import
------------------

When the configuration has been set up, the data can be imported as follows:

 1. Open the :file:`Monitoring data.dss` file in HEC-DSSVue.
 2. Select menu item :menuselection:`Scripts --> Import field data` or 
    alternatively click on :menuselection:`Import field data` on the toolbar.
 3. Choose the configuration file :file:`field_import.yml` in the file selection 
    window. 


When successfully completed, a message is displayed how many records have been 
imported and the catalogue is refreshed.

Data post-processing
--------------------

In this example, data were imported using `RAW` for the data version (F-part). 
This allows review of data and corrections and manipulations using the
HEC-DSSVue built-in functionality. Quality assured data can then be saved using
a different version, for example `OBS`.

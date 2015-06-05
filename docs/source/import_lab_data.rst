Importing lab data
==================

The `Monitoring Module` can be used to import laboratory analytical results. The
results are imported from a `csv`-file with the measurement **locations** 
forming the columns (**across**) and the **parameters** in rows (**down**).

Multiple `csv`-files can be imported at once.

.. note::

   The Monitoring Module's lab data importing tool has been tested to work
   with results provided by the following laboratories:

    - Chemtest

   Other `csv` input file formats may be supported by tweaking the tool's
   configuration parameters.


Getting everything in place
---------------------------

In this example, the file to be imported :file:`2015-01 Lab results.csv` is 
saved in a project file structure as follows:: 

    C:\
        Project\
            Import data\
                2015-01 Lab results.csv
            Monitoring data.dss
            lab_import.yml

The configuration file
----------------------

The configuration file :file:`lab_import.yml` can be created as a simple text
file with the following content:

.. code-block:: yaml

    folder: C:\Path\To\Folder
    files:
     - File 1.csv
     - File 2.csv

    site: Site name
    version: RAW

    rows:
      location:
        title: "Client Sample ID.:"
      date:
        title: "Date Sampled:"
        format: "%d-%b-%y"

    columns:
      parameter:
        title: Determinand
      unit:
        title: Units

    mapping:
      pH: PH
      Suspended Solids At 105C: SS
      Colour: COLOUR
      Biochemical Oxygen Demand Low Level: BOD
      Biochemical Oxygen Demand: BOD
      Chemical Oxygen Demand: COD
      Chloride: CHLORIDE
      Nitrate: NITRATE
      Sulphate: SULPHATE
      Calcium: CALCIUM
      Sodium: SODIUM
      Aluminium (Dissolved): ALUMINIUM
      Manganese (Dissolved): MANGANESE
      Zinc (Dissolved): ZINC
      Iron (Dissolved): IRON
      Dissolved Organic Carbon: DOC
      Total Petroleum Hydrocarbons: TPH

    params:
      PH:
        unit: "-"
      SS:
        unit: mg/l
      COLOUR:
        unit: Pt/Co
      BOD:
        unit: mg/l
      COD:
        unit: mg/l
      DOC:
        unit: mg/l
      CHLORIDE:
        unit: mg/l
      NITRATE:
        unit: mg/l
      SULPHATE:
        unit: mg/l
      CALCIUM:
        unit: mg/l
      SODIUM:
        unit: mg/l
      ALUMINIUM:
        unit: μg/l
      MANGANESE:
        unit: μg/l
      ZINC:
        unit: μg/l
      IRON:
        unit: μg/l
      TPH:
        unit: μg/l


.. tip::

   The configuration file is structured according to the `YAML format 
   <http://yaml.org>`_. Indentation is important to define the configuration 
   correctly. The example is best copied exactly as provided!


The configuration file describes the files to be imported as well as information
about which `csv`-file rows (parameters) to be imported. Analysed parameters can 
be modified as required by editing the ``mapping`` and ``params`` sections of 
the configuration file.

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

Parameter values in the import file starting with `<` are interpreted as being 
below the meter's limit of detection (LOD). Such measurements are imported as 
50% of the LOD to allow numeric evaluations and plotting in line with current 
best practice.


.. warning::
   
   The date column is assumed to be formatted as ``dd-mmm-yy``! 

   Times are set to 12:00:00 hrs.


Running the import
------------------

When the configuration has been set up, the data can be imported as follows:

 1. Open the :file:`Monitoring data.dss` file in HEC-DSSVue.
 2. Select menu item :menuselection:`Scripts --> Import lab data` or 
    alternatively click on :menuselection:`Import lab data` on the toolbar. 

When successfully completed, a message is displayed how many records have been 
imported and the catalogue is refreshed.

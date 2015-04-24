Introduction
============

The `Monitoring Module` is a set of HEC-DSSVue scripts for managing 
environmental monitoring data. The following scripts are included:

 1. Importing water quality data measured using a hand-held meter (see 
    :doc:`import_field_data`).
 2. Importing laboratory water quality analytical results ("lab data").
 3. Creating timeseries plots of water quality data.

HEC-DSS stores data using A- to F-parts. The `Monitoring Module` uses these as 
follows:

 - A-part: Site name
 - B-part: Monitoring point within the site
 - C-part: Parameter, e.g. pH, temperature
 - D-part: Time period
 - E-part: Monitoring interval, e.g. every 15 minutes or irregular
 - F-part: Version, e.g. `raw` or `obs`

The F-part can be used as part of a data quality control workflow. For example, 
imported data can be imported as `raw` and after checking and manipulation (as
required) be saved as `obs`.

.. note::

   In HEC-DSS, all parts are stored in uppercase letters, e.g. `pH` is saved as
   `PH` etc. This cannot be changed.

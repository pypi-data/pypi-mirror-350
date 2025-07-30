MIDAS Default Data Simulator
============================

The *dlpdata* module, provided by the *midas-dlpdata* package, provides a simulator for the default load profiles provided by the BDEW set.

Installation
------------

This package will usually installed automatically together with `midas-mosaik`. It is available on pypi, so you can install it manually with

.. code-block:: bash

    pip install midas-dlpdata

The Data
--------

The data set is taken from the `BDEW` (Bundesverband der Energie- und Wasserwirtschaft e.V.).
It provides eleven default load profiles; seven for trade (G), one for houshold (H) and three for agriculture (L). 
Each profile is grouped into summer, winter and transition and each season is grouped into weekday, saturday and sunday. 
A time resolution of a quarter of an hour was chosen.  

.. _`BDEW`:https://www.bdew.de/energie/standardlastprofile-strom/ 

======================= ============ ======== ===========
Season                    start      end       days
======================= ============ ======== ===========
Winter                     01.11      20.03     140 (141)

Summer                     15.05      14.09     123

Spring (transition)        21.03.     14.05      55

Autum (transition)         15.09.     31.10.     47
======================= ============ ======== ===========


The annaul values of the profiles are calculated starting with the 01.11 as an monday.

========= ========== ===========  ========= 
Profile    MWh/a      peak W      avg kWh    
========= ========== ===========  ========= 
G0         1.154      240.4         0.131    

G1         1.084      489.9         0.123    

G2         1.148      251.2         0.131    

G3         1.145      154.5         0.13

G4         1.155      230.5         0.131

G5         1.178      255.9         0.134

G6         1.154      298.7         0.131

H0         1.152      213.7         0.131

L0         1.137      240.4         0.13

L1         1.137      305.2         0.13

L2         1.137      213.8         0.13
========= ========== ===========  ========= 


For more information about the specific facilities behind the profiles, take a look at `BDEW`.

The daily schedules of the seasons are shown below. 
The green graph represents the weekday load, the blue graph is the saturday load and the yellow one stands for the sunday load.

.. image:: dlp_season.png
    :width: 800

Usage
-----

The intended use-case for the time simulator is to be used inside of MIDAS.
However, it only depends on the `midas-util` package and be used in any mosaik simulation scenario.

Inside of MIDAS
~~~~~~~~~~~~~~~

To use the store inside of MIDAS, simply add `dlpdata` to your modules

.. code-block:: yaml

    my_scenario:
      modules:
        - dlpdata
        # - ...

and provide a *scope* and a *gridfile*: 

.. code-block:: yaml
    
    my_scenario:
      # ...
      dlp_data_params:
        my_scenario:
          load_scaling: 1.5
          interpolate: True
          randomize_data: True
          randomize_cos_phi: True
          mapping:
          15: [[G4, 262.8]]
          17: [[H0, 1038.06]]
 

The numbers 15 and 17 stand for the bus number which depends on the used *gridfile*.   

Any Mosaik Scenario
~~~~~~~~~~~~~~~~~~~

If you don't use MIDAS, you can add the `dlpdata` manually to your `mosaik scenario`_ file. 
First, the entry in the `sim_config`: 

.. _`mosaik scenario`: https://mosaik.readthedocs.io/en/latest/tutorials/demo1.html

.. code-block:: python

    sim_config = {
        "DLPSimulator": {"python": "midas.modules.dlpdata.simulator:DLPSimulator"},
        # ...
    }

Next, you need to start the simulator (assuming a `step_size` of 900):

.. code-block:: python 

    dlpdata_sim = world.start(
        "DLPSimulator", 
        step_size=900,
        start_date="2020-01-01 00:00:00+0100",
        data_path="/path/to/folder/where/dataset/is/located/",
        filename="DefaultLoadProfiles.hdf5",  # this is default
    )

Then the models can be started:

.. code-block:: python

    houshold = dlpdata_sim.H0(scaling=1.0)
    trade = dlpdata_sim.G4(scaling=0.8)

Finally, the models need to be connected to other entities:

.. code-block:: python

    world.connect(trade, other_entity, "p_mw", "q_mvar")

The Keys of the DLP Data Simulator
-----------------------------------------

This section gives a short description for all of the keys of the *dlpdata* module. 
Keys that are part of every upgrade module will only be mentioned if the actual behavior might be unexpected.
First, the keys supported by the base data simulator.

step_size
  The step size does not only affect the frequency of the simulator's step calls but also the access to the data set.
  The time resolution of the data set is 15 minutes (= 900 seconds).
  When a lower *step_size* is used, e.g., 450, then the models will return the same values in every two consecutive steps.
  With a higher *step_size*, e.g., 1800, every second value will be skipped.

interpolate
  In cases where the time resolution of the data set is larger than the *step_size*, this key can be used to activate interpolation.
  It is of type bool and defaults to `false`.
  The interpolation is linear and allows to use even a *step_size* of 1.

randomize_data
  This key can be used to activate randomization of the data.
  It is of type bool and defaults to `false`.
  If activated, a normal-distributed noise will be added to the output values.
  The strength of the noise can be controlled with *noise_factor*.
  The randomization is applied after interpolation. 
  If the data set contains *P* and *Q* values, noise is calculated individually for both of them.

noise_factor
  This key can be used to control the strength of the noise, when *randomize_data* is used.
  It is of type float and the default value is `0.2`, i.e., the noise is drawn with mean of zero (always) and standard deviation of 0.2 times the standard deviation of the data set for *P* or *Q*, respectively.

randomize_cos_phi
  If the data set does not have values for *Q* (which is the case for the Smart Nord data set), the *Q* value will be calculated based on the value of the *cos_phi* key.
  The *randomize_cos_phi* key allows to randomize the cos_phi value before that calculation.
  It is of type bool and defaults to `false`.

On the module level, the *dlpdata* may also have following key:

load_scaling
  This key can be used to scale all load models simultaneously.
  It does not replace individual scaling, instead it is just another factor which is included in the multiplication.
  It is of type float and the default value is `1.0`.

The following keys are only available on the scope level:

filename
  The value of this key holds the filename of the data set file, starting from the location specified by *data_path*.
  The value is of type string, the default value is `DefaultLoadProfiles.hdf5`, and, usually, there is no need to change this value.

mapping
  This key allows to configure the models this simulator should create.
  The mapping depends on the grid in-use and requires information about the available load nodes and the buses they should be connected to.
  For example, a mapping for a grid with two facilitys at buses 2 and 4, the mapping could look like 

  .. code-block:: yaml

      mapping:
        2: [[H0, 1.0]]
        4: [[G4, 1.2]]

  This will be interpreted as: create a H0 (houshold) and a G4 trade model and a scaling of 1.0 and 1.2.
  Connect those models to the load node at bus 2 and 4.
  The models will also automatically connect to the database if any is used.



Inputs of the DLP Data Simulator
---------------------------------------

Since this module is a data provider, it has not many inputs:

cos_phi
  Set the cos phi for the next step. 
  This input is only relevant if the data set has no *Q* values and if *randomize_cos_phi* is set to `false`.

local_time
  (Not yet implemented) If *local_time* is provided, e.g., by the *timesim*, then this time will be used to determine the current value from the data set.
  This input is of type string in the UTC ISO 8601 date format.

Outputs of the DLP Data Simulator
----------------------------------------

The models of this module have three outputs:

p_mw
  Active power output in MW.

q_mvar
  Reactive power output in MVAr.

cos_phi
  The actual cos phi used in the previous step.

Example
-------

The following example is taken from the Bremerhaven MV scenario file.

.. code-block:: yaml

      dlpdata_params:
          bremerhaven:
            load_scaling: 0.75
            mapping:
              15: [[G4, 262.8]] # Weddewarden Industrielast
              17: [[H0, 1038.06]] # Weddewarden Households
              19: [[G4, 17103.9]] # Lehe Industrielast
              20: [[H0, 14454.0]] # Lehe Households - 0
              24: [[G4, 15067.2]] # Geestemünde Industrielast
              25: [[H0, 15111]] # Geestemünde Households - 0
              28: [[H0, 13271.4]] # Lehe Households - 1
              30: [[H0, 14454]] # Lehe Households - 2
              32: [[G1, 175.2]] # Erdgas Kronos Titan GmbH
              33: [[H0, 18615]] # Geestemünde Households - 1
              35: [[H0, 13140]] # Lehe Households - 3
              37: [[H0, 13140]] # Lehe Households - 4
              40: [[H0, 16206]] # Leherheide Households - 0
              44: [[G3, 4108.44]] # Klinikum Bremerhaven 
              45: [[H0, 4568.34]] # Schifferdorferdamm Households
              47: [[G4, 1165.08]] # Schifferdorferdamm Industrielast
              48: [[G4, 2365.2]] # Eisarena, Stadthalle
              49: [[G4, 5676.48]] # Mitte Industrielast
              50: [[H0, 11169]] # Mitte Households - 0
              52: [[G4, 7450.38]] # Leherheide Industrielast
              53: [[H0, 11388]] # Wulsdorf Households - 0
              56: [[G4, 1362.18]] # Surheide Industrielast
              57: [[H0, 5343.6]] # Surheide Households
              59: [[G3, 1226.4]] # AMEOS Klinikum Am Bürgerpark
              60: [[G4, 1554.9]] # Innenstadt
              61: [[G3, 1182.6]] # Zoo
              62: [[G3, 1033.68]] # AMEOS Klinikum Mitte
              63: [[H0, 11169]] # Mitte Households - 1
              65: [[H0, 9636]] # Leherheide Households - 1
              67: [[H0, 8760]] # Wulsdorf Households - 1
              69: [[G4, 87.6]] # Fischereihafen Industrielast
              70: [[G4, 5150.88]] # Wulsdorf Industrielast
              71: [[H0, 12702]] # Geestemünde Households - 2
              73: [[G4, 2334.54]] # Bremerhaven Süd
              74: [[G3, 1095]] # Fischereihafen - 4
              75: [[G3, 1095]] # Fischereihafen - 3
              76: [[G3, 1095]] # Fischereihafen - 2
              77: [[G3, 1095]] # Fischereihafen - 1
              78: [[G3, 1095]] # Fischereihafen - 0
              80: [[H0, 341.64]] # Fischereihafen - Households

MIDAS Commercial Data Simulator
===============================

The *comdata* module, provided by the *midas-comdata* package, provides a simulator for a commercial building reference data set.

Installation
------------

This package will usually installed automatically together with `midas-mosaik`. It is available on pypi, so you can install it manually with

.. code-block:: bash

    pip install midas-comdata

The Data
--------

The data set is taken from the project `Open Energy Data Initiative`_.
It provides 15 time series for commercial facilitys, as it's shown in the following table.  

.. _`Open Energy Data Initiative`: https://data.openei.org/about

========================== ========== ============ ========
Facility                   peak kW     MWh/a       avg kW   
========================== ========== ============ ========
Full Service Restaurant      0.137       601.044    0.069
Hospital                     2.805      18106.771   2.067
Large Hotel                  0.876       4574.578   0.522  
Large Office                 3.482      12137.960   1.386
Medium Office                0.588       1445.567   0.165
Midrise Apartment            0.133        454.896   0.052
Out Patient                  0.630       2643.197   0.302 
Primary School               0.713       1705.623   0.195 
Quick Service Restaurant     0.077        357.569   0.041 
Secondary School             2.529       6396.515   0.730
Small Hotel                  0.270       1147.850   0.131
Small Office                 0.039        122.119   0.014
Standalone Retail            0.219        615.892   0.070
Strip Mall                   0.197        541.853   0.062
Super Market                 0.568       2343.541   0.268
Warehouse                    0.186        481.342   0.055
========================== ========== ============ ========

The aggregated load of each lands is visualized in this figure:

.. image:: facilitys.png
    :width: 800

Usage
-----

The intended use-case for the time simulator is to be used inside of MIDAS.
However, it only depends on the `midas-util` package and be used in any mosaik simulation scenario.

Inside of MIDAS
~~~~~~~~~~~~~~~

To use the store inside of MIDAS, simply add `comdata` to your modules

.. code-block:: yaml

    my_scenario:
      modules:
        - comdata
        # - ...

and provide a *scope* and a *gridfile*: 

.. code-block:: yaml
    
    my_scenario:
      # ...
      comdata_params:
        my_grid_scope:
          interpolate: True
          randomize_data: True
          randomize_cos_phi: True
          mapping:
            22: [[Hospital, 0.002]] # industrial subgrid
            35: [[StripMall, 0.015]]
 

The number 22, 35 stands for the bus number, which depends on the used *gridfile*.   

Any Mosaik Scenario
~~~~~~~~~~~~~~~~~~~

If you don't use MIDAS, you can add the `comdata` manually to your `mosaik scenario`_ file. 
First, the entry in the `sim_config`: 

.. _`mosaik scenario`: https://mosaik.readthedocs.io/en/latest/tutorials/demo1.html

.. code-block:: python

    sim_config = {
        "CommercialDataSimulator": {"python": "midas.modules.comdata.simulator:CommercialDataSimulator"},
        # ...
    }

Next, you need to start the simulator (assuming a `step_size` of 900):

.. code-block:: python
    
    comdata_sim = world.start(
        "CommercialData", 
        step_size=900,
        start_date="2020-01-01 00:00:00+0100",
        data_path="/path/to/folder/where/dataset/is/located/",
        filename="CommercialsRefTMY3.hdf5",  # this is default
    )

Then the models can be started:

.. code-block:: python

    hospital = comdata_sim.Hospital(scaling=1.0)
    full_serv_restaurant = comdata_sim.FullServiceRestaurant(scaling=0.8)

Finally, the modells need to be connected to other entities:

.. code-block:: python

    world.connect(hospital, other_entity, "p_mw", "q_mvar")

The Keys of the Commercial Data Simulator
-----------------------------------------

This section gives a short description for all of the keys of the *comdata* module. 
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

On the module level, the *comdata* may also have following key:

load_scaling
  This key can be used to scale all load models simultaneously.
  It does not replace individual scaling, instead it is just another factor which is included in the multiplication.
  It is of type float and the default value is `1.0`.

The following keys are only available on the scope level:

filename
  The value of this key holds the filename of the data set file, starting from the location specified by *data_path*.
  The value is of type string, the default value is `CommercialsRefTMY3.hdf5`, and, usually, there is no need to change this value.

mapping
  This key allows to configure the models this simulator should create.
  The mapping depends on the grid in-use and requires information about the available load nodes and the buses they should be connected to.
  For example, a mapping for a grid with two facilitys at buses 2 and 4, the mapping could look like 

  .. code-block:: yaml

      mapping:
        2: [[SuperMarket, 1.0]]
        4: [[SmallOffice, 1.2]]

  This will be interpreted as: create a SuperMarket and a SmallOffice model and a scaling of 1.0 and 1.2.
  Connect those models to the load node at bus 2 and 4cd.
  The models will also automatically connect to the database if any is used.



Inputs of the Commercial Data Simulator
---------------------------------------

Since this module is a data provider, it has not many inputs:

cos_phi
  Set the cos phi for the next step. 
  This input is only relevant if the data set has no *Q* values and if *randomize_cos_phi* is set to `false`.

local_time
  (Not yet implemented) If *local_time* is provided, e.g., by the *timesim*, then this time will be used to determine the current value from the data set.
  This input is of type string in the UTC ISO 8601 date format.

Outputs of the Commercial Data Simulator
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

The following example is taken from the default `midaslv` scenario file.

.. code-block:: yaml

   comdata_params:
    midaslv:
      interpolate: True
      randomize_data: True
      randomize_cos_phi: True
      mapping:
        22: [[Hospital, 0.002]] # industrial subgrid
        35: [[StripMall, 0.015]]
        36: [[Warehouse, 0.015]]
        37: [[SmallHotel, 0.0072]]
        40: [[StandaloneRetail, 0.015]]
        41: [[QuickServiceRestaurant, 0.0075]]
        42: [[MidriseApartment, 0.012]]
        43: [[SmallOffice, 0.021]]

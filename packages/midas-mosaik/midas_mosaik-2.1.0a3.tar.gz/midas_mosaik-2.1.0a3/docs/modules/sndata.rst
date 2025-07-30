MIDAS Smart Nord Data Module
============================

The *sndata* module, provided by the *midas-sndata* package, provides a simulator for the Smart Nord Data set.

Installation
------------

This package will usually installed automatically together with `midas-mosaik`. It is available on pypi, so you can install it manually with

.. code-block:: bash

    pip install midas-sndata

The Data
--------

The data set is a synthetic data set developed in the research project `Smart Nord`_.
The data set consists of 941 individual time series, each of them representing one household.
Those time series are further grouped into 8 *low-voltage lands* of different sizes.
The following table gives an overview over the number of households per land as well as a few statistics of the aggregated power consumption.

.. _`Smart Nord`: http://www.smartnord.de

==== ======= ========= ===== ====== =======
Land #Houses House IDs MWh/a avg kW peak kW
==== ======= ========= ===== ====== =======
0       41     0 -  40  130   14.8   39.9
1      139    41 - 179  661   75.5  516.6
2       67   180 - 246  323   36.9  148.2
3       57   247 - 303  223   25.5   70.9
4      169   304 - 472  741   84.6  277.9
5      299   473 - 771 1377  157.2  413.7
6       66   772 - 837  309   35.3   97.5
7      103   838 - 940  421   48.1  146.4
==== ======= ========= ===== ====== =======

The aggregated load of each lands is visualized in this figure:

.. image:: smart_nord_lands.png
    :width: 800

Usage
-----

The intended use-case for the time simulator is to be used inside of MIDAS.
However, it only depends on the `midas-util` package and be used in any mosaik simulation scenario.

Inside of MIDAS
~~~~~~~~~~~~~~~

To use the store inside of MIDAS, simply add `powergrid` to your modules

.. code-block:: yaml

    my_scenario:
      modules:
        - sndata
        # - ...

and provide a *scope* and a *gridfile*: 

.. code-block:: yaml
    
    my_scenario:
      # ...
      sndata_params:
        my_grid_scope:
          household_mapping: {}
          land_mapping: {}

One of those mappings should be filled with actual values but since this depends on the grid, the general format will be described in the Keys section and an example is given at the end of this page.

Any Mosaik Scenario
~~~~~~~~~~~~~~~~~~~

If you don't use MIDAS, you can add the `sndata` manually to your mosaik scenario file. 
First, the entry in the `sim_config`:

.. code-block:: python

    sim_config = {
        "SmartNordData": {"python": "midas.modules.sndata.simulator:SmartNordDataSimulator"},
        # ...
    }

Next, you need to start the simulator (assuming a `step_size` of 900):

.. code-block:: python
    
    sndata_sim = world.start(
        "SmartNordData", 
        step_size=900,
        start_date="2020-01-01 00:00:00+0100",
        data_path="/path/to/folder/where/dataset/is/located/",
        filename="SmartNordProfiles.hdf5",  # this is default
    )

Then the models can be started:

.. code-block:: python
    
    land1 = sndata_sim.Land(eidx=0, scaling=1.0)
    land2 = sndata_sim.Land(eidx=7, scaling=0.8)
    house1 = sndata_sim.Household(eidx=0, scaling=1.1)
    house2 = sndata_sim.Household(eidx=940, scaling=2.0)

Finally, the modells need to be connected to other entities:

.. code-block:: python

    world.connect(land1, other_entity, "p_mw", "q_mvar")

The Keys of the Smart Nord Data Simulator
-----------------------------------------

This section gives a short description for all of the keys of the *sndata* module. 
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

On the module level, the *sndata_params* may also have following key:

load_scaling
  This key can be used to scale all load models simultaneously.
  It does not replace individual scaling, instead it is just another factor which is included in the multiplication.
  It is of type float and the default value is `1.0`.

The following keys are only available on the scope level:

filename
  The value of this key holds the filename of the data set file, starting from the location specified by *data_path*.
  The value is of type string, the default value is `SmartNordProfiles.hdf5`, and, usually, there is no need to change this value.

household_mapping
  This key allows to configure the models this simulator should create.
  The mapping depends on the grid in-use and requires information about the available load nodes and the buses they should be connected to.
  For example, a mapping for a grid with loads at buses 2 and 4, the mapping could look like 

  .. code-block:: yaml

      household_mapping:
        2: [[0, 1.0], [940, 1.0]]
        4: [[42, 1.2]]

  This will be interpreted as: create two household models based on time series with index 0 and 940 and a scaling of 1.0 each.
  Connect those models to the load node at bus 2.
  Additionally, create one household model based on time series with index 42 and scaling 1.2 and connect it to the load at bus 4.
  The models will also automatically connect to the database if any is used.

land_mapping
  This key works similar to the *household_mapping* key but instead of households, lands are created.

Inputs of the Smart Nord Data Simulator
---------------------------------------

Since this module is a data provider, it has not many inputs:

cos_phi
  Set the cos phi for the next step. 
  This input is only relevant if the data set has no *Q* values and if *randomize_cos_phi* is set to `false`.

local_time
  (Not yet implemented) If *local_time* is provided, e.g., by the *timesim*, then this time will be used to determine the current value from the data set.
  This input is of type string in the UTC ISO 8601 date format.

Outputs of the Smart Nord Data Simulator
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

The following example is taken from the default `midasmv` scenario file.

.. code-block:: yaml

  midasmv_sn:
    parent:
    modules: [store, powergrid, sndata]
    step_size: 15*60
    start_date: 2020-01-01 00:00:00+0100
    end: 1*24*60*60
    store_params:
      filename: midasmv_sn.hdf5
    powergrid_params:
      midasmv:
        gridfile: midasmv
    sndata_params:
      midasmv:
        land_mapping:
          1: [[0, 1.0], [2, 1.0], [3, 2.0], [6, 2.0], [7, 1.0]]
          3: [[2, 1.0], [3, 1.0], [6, 1.0], [7, 1.0]]
          4: [[0, 2.0], [3, 2.0], [7, 1.0]]
          5: [[3, 2.0], [7, 1.0]]
          6: [[0, 2.0], [3, 1.0]]
          7: [[0, 2.0], [2, 1.0], [3, 2.0], [7, 1.0]]
          8: [[0, 1.0], [3, 1.0], [6, 1.0]]
          9: [[2, 1.0], [3, 1.0], [6, 2.0], [7, 1.0]]
          10: [[0, 2.0], [2, 1.0], [3, 1.0], [6, 2.0], [7, 1.0]]
          11: [[0, 1.0], [2, 1.0], [3, 1.0], [6, 2.0], [7, 1.0]]

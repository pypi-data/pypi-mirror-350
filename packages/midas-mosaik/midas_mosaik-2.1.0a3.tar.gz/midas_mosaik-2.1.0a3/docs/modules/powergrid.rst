MIDAS Powergrid Module
======================

The *powergrid* module, provided by the `midas-powergrid` package, contains a simulator for pandapower networks, which will be called *grids* in the context of MIDAS.

Installation
------------

This package will usually installed automatically together with `midas-mosaik`. It is available on pypi, so you can install it manually with

.. code-block:: bash

    pip install midas-powergrids


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
        - powergrid
        # - ...

and provide a *scope* and a *gridfile*: 

.. code-block:: yaml
    
    my_scenario:
      # ...
      powergrid_params:
        my_grid_scope:
          gridfile: midasmv

Other, data-providing simulators with the same scope will output their data to this grid.
Possible values for *gridfile* will be described in the *Keys* section below.

Any Mosaik Scenario
~~~~~~~~~~~~~~~~~~~

If you don't use MIDAS, you can add the `powergrid` manually to your mosaik scenario file. 
First, the entry in the `sim_config`:

.. code-block:: python

    sim_config = {
        "Powergrid": {"python": "midas.modules.powergrid.simulator:PandapowerSimulator"},
        # ...
    }

Next, you need to start the simulator (assuming a `step_size` of 900):

.. code-block:: python
    
    grid_sim = world.start("Powergrid", step_size=900)

Finally, the model needs to be started:

.. code-block:: python
    
    grid = grid_sim.Grid(gridfile="midasmv")

To connect the output of the grids' buses to another model, you have to get the list of bus models from the powergrids' children like

.. code-block:: python
    
    bus_models = [e for e in grid.children if "bus" in e.eid]

and then connect those models either individually or in a loop, e.g.,

.. code-block:: python
    
    for bus in bus_models:
        world.connect(bus, other_entity, "vm_pu", "va_degree", "p_mw", "q_mvar")

The inputs are generally handled in the same way.
Have a look at `grid.children` to get the required entity eids.

The Keys of the Powergrid Simulator
-----------------------------------

This section gives a short description for all of the keys of the *powergrid* module. 
Keys that are part of every upgrade module will only be mentioned if the actual behavior might be unexpected.

step_size
  This key is mainly ignored by the grid model itself, since the model has no time-based internal state.

plotting
  This key allows to enable grid plotting for certain grids.
  The value is of type bool and defaults to `false`.

plot_path
  This key specifies where the plotted grid images will be stored. 
  The value is of type string and the default value is `plots`, which will create a directory called *plots* in the *_outputs* directory defined in *midas-runtime-conf.yaml*.

save_grid_json
  The value of this key is of type bool. 
  If set to true, the grid model will serialize the pandapower grid to json and send it to the database.
  Since the resulting string is rather long, this option is set to `false` by default. 

use_constraints
  This key allows to enable the experimental feature of grid constraints.
  The value is of type bool and defaults to `false`.

constraints
  If *use_constraints* is set to `true`, this key allows to define the constraints to be used.
  Once the feature is more evaluated, it will get its own section. 
  The `constrainted_grids.yml` scenario file in the MIDAS source code contains examples for different grids.

All above keys can be overwritten (or solely defined) within a certain scope.
However, available on scope level only are the following keys:

gridfile
  This keys defines the grid topology to be loaded.
  The type of the value is string but there are different semantics to that string.
  First, there are a few pandapower grid topologies that can be directly accessed with aliases.
  Those are `cigre_hv`, `cigre_mv` and `cigre_lv` for the corresponding grids.
  Second, a few more aliases are `midasmv`, `midaslv`, and `bhv`, which load certain custom grids defined inside of MIDAS (*bhv* is the Bremerhaven Grid developed by a students' project group at the University of Oldenburg).
  Next, any Simbench code can be entered to load the corresponding grid (to get the data set of that grid, you have to modify the *midas-runtime-conf.yaml*, see the *sbdata* module for more information).
  Finally, a python import string to a function can be entered that returns a pandapower grid. 
  This allows to define custom grids even outside of MIDAS.
  The last segment of the import string needs to be the function to be called.
  Parameters to that function can be passed with the *grid_params* key.
  Additionally, grids can be loaded from `.json` or `.xlsx` files can be loaded.
  The full (absolute or relative) path to those files needs to be entered.

grid_params
  This key allows to pass additional parameters to grids that are neither .json nor .xlsx nor Simbench grids.
  The value is of type dictionary and the values will be passed without further checking.
  The default value is an empty dictionary.

Inputs of the Powergrid Simulator
---------------------------------

The exact number of inputs depends on the grid topology that is used. 
The grid has a number of children models, representing different components of the grid.

The most important attributes of loads, sgens, and storages (not available in every grid) are:

p_mw
  Active power in Mega Watt of the grid node. 
  The behavior depends on the role (load, sgen, or storage) and multiple inputs to the same node will be summed up.
  The value is of type float.

q_mvar 
  Reactive power in Mega Volt-Ampere reactive of the grid node.
  The behavior depends on the role (load, sgen, or storage) and multiple inputs to the same node will be summed up.
  The value is of type float.

Transformators have an input as well:

tap_pos
  The currently active tap position.
  The value is of type integer and defaults to 0.
  The *tap_pos* can be between *tap_min* and *tap_max*, defined in the grid itself.
  Currently, there is no MIDAS simulator that makes use of this input.

Finally, there are the switches which have an input:

closed
  Controls the current state of the switch. 
  The default setting is closed, i.e., *closed* is set to `true`.
  Currently, there is no MIDAS simulator that makes use of this input.


Outputs of the Powergrid Simulator
----------------------------------

The grid itself has two outputs:

health
  The average voltage magnitude per unit of all the buses in the grid.
  The value is of type float.

grid_json
  A string containing the json-serialized grid.

The bus nodes of the grid have four outputs:

vm_pu
  The voltage magnitude per unit in relation to the slack node in the grid.
  The value is of type float.

va_degree
  The angle between voltage and current.
  The value is of type float.

p_mw
  The active power that arives at the bus.
  The value is of type float.

q_mvar
  The reactive power that arives at the bus.   
  The value is of type float.

Lines and transformators have (among others) the following output:

loading_percent
  The load utilization relative to the rated power. 
  The value is of type float.

Additionally, the nodes that are listed in the inputs section, will send there current input to the database if one is used.


PalaestrAI Sensors of the Powergrid Simulator
---------------------------------------------

If the *with_arl* is set either on the scenario levle or on the module level, sensor objects for the following outputs will be created.
However, space definitions needed to be generalized and may not represent the actual space of the attribute.

* loading_percent (Trafo, Line) = Box(0, 1, (1,), np.float32)
* vm_pu (Bus) = Box(0.8, 1.2, (1,), np.float32)
* va_degree (Bus) = Box(-1, 1, (1,), np.float32)
* p_mw (Load, Sgen, Storage, Ext_grid) = Box(0, 1, (1,), np.float32)
* q_mvar (Load, Sgen, Storage, Ext_grid) = Box(-1, 1, (1,), np.float32)
* health (Grid) = Box(0, 1.2, (1,), np.float32)
* grid_json (Grid) = Box(0, 1, (1,), np.float32)  

The last one (grid_json) is actually a string and not intented to be used as common sensor.

PalaestrAI Actuators of the Powergrid Simulator
-----------------------------------------------

With the *with_arl* flag, the following actuators will be created.
The spaces have the same limitations as with the sensors.

* tap_pos (Trafo): Box(-10, 10, (1,), np.int32)
* p_mw (Load, Sgen): Box(0, 0.5, (1,), np.float32)
* q_mvar (Load, Sgen): Box(0, 0.5, (1,), np.float32)

Example Scenario Configuration
------------------------------

The following scenario runs the same grid twice but one instance will use the (yet experimental) grid constraints.

.. code-block:: yaml

    two_grid_example:
      name: two_grid_example
      parent: ~
      modules: [store, powergrid, sndata, comdata]
      step_size: 1*60
      start_date: 2020-06-01 10:00:00+0100
      end: 1*5*60*60
      store_params:
        filename: two_grid_example.hdf5
        overwrite: true
      powergrid_params:
        midasmv:
          gridfile: midasmv
        midas_constr:
          gridfile: midasmv
          use_constraints: true
          constraints:
            - [load, 0.02]
            - [line, 100]
      sndata_params:
        midasmv:
          interpolate: True
          load_scaling: 1.5
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
        midas_constr:
          interpolate: True
          load_scaling: 1.5
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
      comdata_params:
        midasmv:
          interpolate: True
          load_scaling: 1.5
          mapping:
            13: [[SuperMarket, 3.0]]
            14: [[SmallHotel, 2.0]]
        midas_constr:
          interpolate: True
          load_scaling: 1.5
          mapping:
            13: [[SuperMarket, 3.0]]
            14: [[SmallHotel, 2.0]]

The first plot shows the result from the grid without constraints.

.. image:: two_grid_example-Powergrid__0_0-buses_vmpu.png
    :width: 800


The second plot shows the results from the grid with constraints. 
An oscillating behavior can be seen at the end, after some of the constraints where activated.

.. image:: two_grid_example-Powergrid__1_0-buses_vmpu.png
    :width: 800

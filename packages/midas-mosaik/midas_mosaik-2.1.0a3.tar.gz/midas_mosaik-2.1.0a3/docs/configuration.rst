Scenario Configuration
======================

This part aims to provide a comprehensive overview of all the functions the configurator and the scenario yaml file can provide.
The individual modules will be excluded for now and will receive a separate part.

Lifecycle
---------

What happens after calling *midasctl run*?
Well, the functions *configure* and *download* will be called to make sure that everything is configured and downloaded.
After that, the *Configurator* of midas will be executed.
The Configurator will perform a number of checks, e.g., can all default configs and custom configs be loaded and is the provided *scenario_name* contained in one of them?
The Configurator will then create a list of all the configurations required for *scenario_name*. 
Those will be determined by evaluating the *parent* key of a scenario configuration.
Once all configurations are collected, the final configuration will be created by updating the configurations in reverse order.

Given that everything went well, a new *Scenario* object will be created and the final params will be passed to it.
The Scenario will provide default values for all the keys that are not part of any module.
After that, the `modules` key will be evaluated.
The Configurator will apply modules in a fixed order, defined in the *midas-runtime-conf.yml* file (you should not change them unless you know what you're doing).
Once all the module upgrades were applied, the same is done for custom modules.
Finally, if the scenario configuration was successful, the simulation is started. 
At this point, everything else is handled by mosaik and not by *midas* anymore.

The Keys to the Scenario
------------------------

This section will give a short explanation for every key possible that is not part of one of the modules.
On the toplevel of a scenario file, the *scenario_name* needs to be provided as key. 
It is important that the *scenario_name* is unique over all of your scenario files, including the default scenarios as well as those defined in your *midas_scenarios* folder.
Midas uses dictionaries to store the configurations with the *scenario_name* being the key. 
Once a duplicate is detected, midas will stop with an error.


The following keys can be provided on the next lower hierarchical level to the scenario name.

parent
  This key defines a scenario by its' *scenario_name* that should provide default configuration for the current scenario.
  The current scenario file can overwrite any of the keys in the parent scenario, but note that some values will be extended instead of being replaced.
  The value is of type string.

modules
  This key is used to define the modules to be loaded. 
  The value is of type list. Each element of the list is of type string and represents a module.
  The order of the module names does not matter, the Configurator will get the correct order from a different place.
  If only the parameters of a module are provided but not the entry in *modules*, the module will not be loaded.

custom_modules
  This key works similar to the *modules* key. 
  However, this one is used to define modules that are not part of the midas ecosystem.
  Therefore, the order matters in this case.
  The value itself is of type list but the list entries are lists as well.
  Those sub-lists contain the name of the module as first entry and the full python import path to the module.
  An upgrade module should be a subclass of `midas.scenario.upgrade_module:UpgradeModule`.

data_path
  This key defines the absolute path to the *midas_data* folder and will usually be derived from the runtime config and set automatically.
  However, it can be set manually to use a different configuration for a specific scenario.

start_date
  An UTC ISO 8601 time string to indicate the starting point of the simulation. 
  Modules don't have to use and track the current time but if they do, they should use this value to start.
  The default value is `2020-01-01 00:00:00+0100`.

end
  The number of simulation steps mosaik should orchestrate. 
  Per convention, one step equals one second.
  However, steps where nothing happens will simply be skipped.
  Although the value is of type integer, it is recommended to define *end* as multiplication string for more readability.
  The Configurator will then calculate the correct value.
  The default value is `1*24*60*60`, which equals 86,400 seconds or one day of simulated time.

step_size
  This key provides the step size in seconds as default value.
  Modules can use this value to synchronize their steps but they don't have to.
  Like *end*, the value is of type integer, but can be provided as multiplication string.
  The default value is `15*60` = 900 = 15 minutes.

no_db
  This key can be used to globally disable connections to the database module.
  However, globally only means that modules will get their default value from this flag.
  They can individually decide to use or to not use the database.
  The value is of type bool and the default value is `false`.

no_rng
  This key can be used to disable the use of random numbers. 
  Modules supporting this flag should disable all possible functions that make use of random numbers.
  Modules can indicidually decice to overwrite this value.
  The value is of type bool and the default value is `false`.

seed
  This key can be used to provide a master seed. 
  If it is not set, a random seed will be created. 
  Random seeds for all modules will be created based on this seed unless a module locally overwrites the seed.
  The *seed* key will be ignored when the *random_state* key is present.
  The value if of type integer and the default value is `None` (which uses a randomly chosen random seed).

random_state
  This key can be used to pass a numpy random state object that was pickled to the file system.
  The value must contain the full path to the random state object.
  The value is of type string and is usually not used except in the auto-generated yaml configs if a seed was used in the original scenario.

cmd
  Mosaik knows three different ways to interact with simulators: start them in-process via python, as external process via command line, or connect to them with sockets.
  Which type is supported depends on the different modules. 
  The core modules of MIDAS will support in-process and as external process.
  Like before, this value is used as default for modules, which can use a different definition locally.
  The value is of type string and the default value is `python`. 

with_arl
  This key controls compatibility to `palaestrAI`, the reference implementation of *Adversarial Resilience Learning*.
  The value is of type bool and defaults to `false`.
  If enabled, the `create_sensors` and `create_actuators` methods of the upgrade modules will be called.

with_ict
  This key controls compatibility to ICT-based modules.
  Modules can query this flag and decide to skip some of their connections to other modules in favor of letting the ICT-based module handle this connection.
  More details will follow in the future.
  The value is of type bool and defaults to `false`.
  *Currently, there is no (working) implementation of ICT available*

with_timesim
  This key is similar to the *no_db* key. 
  If enabled and a time simulator is used, modules can get the local time from the time simulator instead of using their own time tracking.
  Depending on the time simulator in use, this allows weird and unrealistic time jumps.
  The value is of type bool and defaults to `false`.

cos_phi
  This key provides a default value for the cosinus of the phase angle for all modules. 
  The value is of type float and the default value is `0.9`.

forecast_horizon_hours
  This key allows to define the time frame for forecasts.
  Modules that support forecasts can use this value to decide how large the forecast should be.
  The value is of type float and the default value is `0.25`, which equals 15 minutes. 

flexibility_horizon_hours
  This key is similar to *forecast_horizon_hours* but is intended to be used by flexibility-based modules.
  Flexibilities are defined as a set of schedules for a certain time frame in the future, e.g., different power generation values of a controllable generator.
  The value is of type float and defaults to the value set in *forecast_horizon_hours* (i.e., `0.25` without any changes).

flexibility_horizon_start_hours
  In contrast to forecasts, flexibilities can be calculated beginning at a point of time somewhere in the future (e.g., 3 hours ahead of time).
  With this key, a default value of hours can be defined so that modules can synchronize themselves.
  The value is of type float and defaults to `0` indicating that the future is now!

mosaik_params
  This key can be used to pass information to mosaik.
  The value is of type dictionary and is not set by default.

Keys of the Upgrade Module 
--------------------------

Some of the keys above will be directly passed to the modules, i.e., if they are not defined on the module level, they will have the value from the scenario level.
This includes following attributes:

* cmd
* step_size
* no_db
* no_rng
* with_timesim
* with_arl


There are also a few keys that every module has, which are not part of the base scenario configuration.
The will be briefly described in the following.

sim_name
  This key can be used to set a different simulator name.
  The simulator name is used to create the entry in mosaik's *sim_config* and mosaik will start the simulator with that name, e.g., if a simulator is called `MyCoolSim`, then mosaik will start it as `MyCoolSim-0`.
  Each module has an individual default value for the *sim_name* and, normally, there should be no reason to change it.
  The value is of type string.

import_str
  This key defines where to import the simulator from in case that the simulator is started in-process (`cmd: python`).
  The value of *import_str* will be placed in mosaik's *sim_config* as well.
  Each module has an individual default value for *import_str* and the value is of type string.
  This value also defines how the simulator is started as external process (`cmd: cmd`).
  Unlike *sim_name*, there are various reasons to change the value of *import_str*, e.g., if you have a custom implementation of a certain simulator, you can simply place the import string here and the custom implementation will be loaded instead.
  However, this requires that the custom implementation supports all functionality of the base simulators' mosaik interface.


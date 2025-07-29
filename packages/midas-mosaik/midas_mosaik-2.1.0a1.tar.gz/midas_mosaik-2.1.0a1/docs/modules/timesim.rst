MIDAS Timesim Module
====================

The *timesim* module, provided by the `midas-timesim` package, contains a simulator that tracks time and is able to manipulate it within the simulation.


Installation
------------

This package will usually installed automatically together with `midas-mosaik`. It is available on pypi, so you can install it manually with

.. code-block:: bash

    pip install midas-timesim


Usage
-----

The intended use-case for the time simulator is to be used inside of MIDAS.
However, it only depends on the `midas-util` package and be used in any mosaik simulation scenario.

Inside of MIDAS
~~~~~~~~~~~~~~~

To use the store inside of MIDAS, simply add `timesim` to your modules:

.. code-block:: yaml

    my_scenario:
      modules:
        - timesim
        # - ...

This is sufficient for the timesim to run. 
However, additional configuration is possible with:

.. code-block:: yaml
    
    my_scenario:
      # ...
      timesim_params:
        start_date: 2020-01-01 01:00:00+0100

All of the core simulators that have support time inputs will then automatically connect to the *timesim* simulator. 
The scope *timesim* will be created automatically but no other scopes are supported.

Any Mosaik Scenario
~~~~~~~~~~~~~~~~~~~

If you don't use MIDAS, you can add the `timesim` manually to your mosaik scenario file. First, the entry in the `sim_config`:

.. code-block:: python

    sim_config = {
        "TimeSimulator": {"python": "midas.modules.timesim.simulator:TimeSimulator"},
        # ...
    }


Next, you need to start the simulator (assuming a `step_size` of 900):

.. code-block:: python
    
    timesim_sim = world.start("TimeSimulator", step_size=900)


Finally, the model needs to be started:

.. code-block:: python
    
    timesim = timesim_sim.Timegenerator()


Afterwards, you can define `world.connect(timesim, other_entity, attrs)` as you like.

The Keys of the Time Simulator
------------------------------

This section gives a short description for all of the keys of the *timesim* module. 
Keys that are part of every upgrade module will only be mentioned if the actual behavior might be unexpected.

start_date
  This key allows to set the start date for the time tracking of the simulator. 
  Usually, this defaults to the *start_date* from the scenario configuration.
  However, different values can be set, so that the time simulator is, e.g., one hour or one day off to the simulators using the default scenario time.
  This affects all outputs of the time simulator.
  The value is of type string and the value should be an UTC ISO 8601 time string.

time_schedule
  This key allows to define complete different time values.
  It is of type list, which each entry being of type string (like *start_date*).
  If *time_schedule* contains at least one value, *start_date* is completely ignored.
  Instead, the time simulator will iterate over this list and setting the internal time to the value of the current list element.
  Once the the simulator reaches the end of the list, it will start again from the beginning.

Outputs of the Time Simulator
-----------------------------

The time simulator has a number of outputs but, usually, only *local_time* is used.

local_time
  The current local time calculated by the time simulator as UTC ISO 8601 time string.
  That time is either the *start_date* plus the time that has passed since or the current value from the *time_schedule* if used.
  The *local_time* is timezone-aware.

utc_time
  The time simulator always calculates the UTC time from the local time.
  It has the same format and follows the same rules like *local_time*.

sin_time_day
  This value represents the current hour of the day as value on a sinus curve.
  The value is of type float.

sin_time_week
  This value represents the current day of the week as value on a sinus curve.
  The value is of type float.

sin_time_year
  This value represents the current day of the year as value on a sinus curve.
  The value is of type float.

cos_time_day
  This value represents the current hour of the day as value on a cosinus curve.
  The value is of type float.

cos_time_week
  This value represents the current day of the week as value on a cosinus curve.
  The value is of type float.

cos_time_year
  This value represents the current day of the year as value on a cosinus curve.
  The value is of type float.

PalaestrAI Sensors of the Time Simulator
----------------------------------------

If the *with_arl* key is set either on the scenario level or on the module level, sensor objects for following outputs (including space definitions) will be created:

* sin_time_day = Box(0, 1, (1,), np.float32)
* sin_time_week = Box(0, 1, (1,), np.float32)
* sin_time_year = Box(0, 1, (1,), np.float32)
* cos_time_day = Box(0, 1, (1,), np.float32)
* cos_time_week = Box(0, 1, (1,), np.float32)
* cos_time_year = Box(0, 1, (1,), np.float32)

Example Scenario Configuration
------------------------------

The following example scenario demonstrates the application of the *time_schedule*
It runs the time simulator together with the store and two simulators of the weather modules:

.. code-block:: yaml

  time_weather:
    modules: [store, timesim, weather]
    start_date: 2020-01-01 00:00:00+0100
    end: 4*60*60
    step_size: 60*60
    store_params:
      filename: time_weather.hdf5
    timesim_params:
      time_schedule: 
        - 2021-06-08 16:00:00+0200
        - 2014-12-06 23:00:00+0100
        - 2019-08-11 04:00:00+0200
        - 2013-02-05 09:00:00+0100
        - 2015-11-11 11:00:00+0100
    weather_params:
      bremen1:
        weather_mapping:
          WeatherCurrent: [{}]
      bremen2:
        with_timesim: true
        weather_mapping:
          WeatherCurrent: [{}]

Since this is part of the default scenarios, it can be run with:

.. code-block:: bash

    midasctl run time_weather

The resulting air temperatures of both weather simulators are shown in the following figure.

.. image:: time_weather.png
    :width: 800

MIDAS Store Module
==================

The *store* module, provided by the `midas-store` package, contains a simple database simulator.
It is simple in that regard that only a simple *Hierarchical Document Format* (HDF) database will be used to store the data.
Furthermore, *pandas* and *pytables* are used to allow pandas dataframes to be saved directly to the HDF file.
This makes it convenient to use inside of python code or a Jupyter notebook but on the otherside it gets more complicated to read the HDF file with a common HDF viewer application.

Installation
------------

This package will usually installed automatically together with `midas-mosaik`. It is available on pypi, so you can install it manually with

.. code-block:: bash

    pip install midas-store


Usage
-----

The intended use-case for the store is to be used inside of MIDAS.
However, it only depends on the `midas-util` package and be used in any mosaik simulation scenario.

Inside of MIDAS
~~~~~~~~~~~~~~~

To use the store inside of MIDAS, simply add `store` to your modules

.. code-block:: yaml

    my_scenario:
      modules:
        - store
        # - ...

and configure it with:

.. code-block:: yaml
    
    my_scenario:
      # ...
      store_params:
        filename: my_db.hdf5

All of the core simulators that have something to store will then automatically connect to the *store* simulator.
However, the store does not support scopes.
Implicitly, the scope *database* will be created and used.  

Any Mosaik Scenario
~~~~~~~~~~~~~~~~~~~

If you don't use MIDAS, you can add the `store` manually to your mosaik scenario file. First, the entry in the `sim_config`:

.. code-block:: python

    sim_config = {
        "MidasHdf": {"python": "midas.modules.store.simulator:MidasHdf5"},
        # ...
    }


Next, you need to start the simulator (assuming a `step_size` of 900):

.. code-block:: python
    
    store_sim = world.start("MidasHdf", step_size=900)


Finally, the model needs to be started:

.. code-block:: python
    
    store = store_sim.Database(filename="path/to/my_db.hdf5", buffer_size=0, keep_old_files=False)


Afterwards, you can define `world.connect(other_entity, store, attrs)` as you like.

The Keys of the Store
---------------------

This section gives a short description for all of the keys of the *store* module. 
Keys that are part of every upgrade module will only be mentioned if the actual behavior might be unexpected.

step_size
  While the *step_size* works as expected, the implications might not be directly clear.
  When *step_size* is set to 1, the store will step in every step.
  In each step, mosaik passes all the outputs from all simulators connected to the store as inputs.
  When other simulators did not perform a step between two store steps, the store will receive the same data from those simulators until they stepped again.
  Therefore, it does not make sense to step the store every second.
  On the other side, if the step size of the store is larger than those of the simulators, only the latest step results will be passed to the store.
  A good rule-of-thumb would be to set the step size to be the same as the simulator with smallest step size that passes relevant data to the store.
  Since the default step size of MIDAS is 900, this step size works as well for the store.

filename
  This key defines the name of the database file.
  A database file with that name will be created inside of the *_outputs* directory defined in the *midas-runtime-conf.yml*.
  The value is of type string

overwrite
  This key controls the behavior of the store when the filename is already present in the *_outputs* directory.
  The value is of type bool.
  If it set to *true*, the existing file will be move to *existing_db.hdf5.old* and the store will use the filename defined by the corresponding key.
  If will not check if *existing_db.hdf5.old* already exists and will overwrite that file.
  Otherwise, the store will try to find a new filename by adding an increment, e.g., *existing_db_2.hdf5*.
  The default value is *false*.

buffer_size
  This key can be used to control how the store will save the data into the database.
  The value if of type integer and defaults to 0, i.e., the store will collect all data from the simulation and will save everything to disk once the simulation is finished.
  In very large and long-running simulations, that behavior might be undesirable and the *buffer_size* can be used to change this.
  A *buffer_size* of, e.g., 1000 will force the store to save the collected data every 1000 steps to the disk. 
  In that regard, the 1000 actually means 1000 calls of the stores' *step* function, not simulation steps.
  The store uses threads to perform that action, so you should not notice any performance issues.
  However, it is recommended to not set the *buffer_size* too low.

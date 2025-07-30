Installation
============

This guide describes how to install *midas* on :ref:`linux`, :ref:`os-x`, and :ref:`windows`. 

.. _linux:

Linux
-----

This guide is based on *Arch Linux 6.11, 64 bit*, but this should for work for
other distributions as well.

The *midas-mosaik* package requires `Python`__ >= 3.8.
We recommend to use a `virtualenv`__ to avoid messing up your system environment.
Use your distributions' package manager to install pip and virtualenv.
Make sure which python version is linked to the `python` command (in some distros this may still be python2).
To be sure, specify the python interpreter when creating the env:

.. code-block:: bash

  $ python3 -m venv ~/.virtualenvs/midas
  $ source ~/.virtualenvs/midas/bin/activate

Now you can install *midas-mosaik* from the pypi package repository

.. code-block:: bash

  (midas) $ pip install midas-mosaik
    
or from the source code.

.. code-block:: bash

  (midas) $ pip install git+https://gitlab.com/midas-mosaik/midas.git

Finally, you can test your installation by typing:

.. code-block:: bash

  (midas) $ midasctl --help 

into the console, which should print information about the command line tool of *midas*.

__ https://www.python.org/
__ https://virtualenv.readthedocs.org

.. _os-x:

OS-X
----

Since I don't have a Mac, I cannot give concrete instructions.
Assuming that you already know how to use Python on your machine, you should be able to follow the instructions for Linux most of the time.

.. _windows:

Windows
-------

Installing under can sometimes be a hassle.
The following steps where tested on Windows 11, 64 bit and Python 3.9.12.

Install Python
~~~~~~~~~~~~~~

This section describes how to install Python and virtualenv. 
If you have already a working installation, you can skip this section.

First, you need to download and install Python on your System. 
Visit https://www.python.org/downloads/release/python-3912/ to select and download the latest 3.9 release version of python.
Make sure to use the 64bit version (unless your system is 32bit only).

Once the installer is downloaded, double-click to start the setup.
During the installation, make sure to mark the options "Add Python to PATH" and "Install for all users" (although the last one might be personal preference).
As soon as the installation finishes, it may be required to log out and log in from your system or restart the whole system.
However, this was not necessary in my case.
You can test your installation via Windows Terminal or use the PowerShell if Windows Terminal is not available.
Once the Powershell opens, type:

.. code-block:: bash

  PS > py --version

If your installation was successful, the command prints out the installed version of Python (e.g.: "Python 3.9.12")

To use virtualenvs inside of Powershell, you need to allow the execution of scripts.
This can be achieved by typing the following command into the Powershell.

.. code-block:: bash

  PS > Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Afterwards, you should install virtualenv with

.. code-block:: bash

  PS > py -m pip install --user virtualenv


Create Virtual Environment and Install MIDAS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create and activate a virtual environment, open Windows Terminal and type:

.. code-block:: bash
    
  PS > py -m venv PyVenvs\\midas
  PS > .\\PyVenvs\\midas\\Scripts\\activate

This creates a virtual environment in your current folder and activates it.
You should now be able to install *midas-mosaik* directly from pypi:

.. code-block:: bash
    
  (midas) PS > pip install midas-mosaik==1.0.0rc2

Finally, to test your installation, type

.. code-block:: bash

  (midas) PS > midasctl configure -a
  (midas) PS > midasctl download
  (midas) PS > midasctl run midasmv

Most likely, you will receive a warning after the *download* command and each time you run the *run* command.
MIDAS downloads the data sets in a temporary location inside the *midas_data* folder before the actual databases are created. 
Aftwards, MIDAS tries to delete that temporary folder but on Windows this is not allowed for some reasons.
To get rid of the warning, open the folder at %USER%\\AppData\\Local\\OFFIS\\midas\\midas_data and delete the *tmp* folder.

If the installation or one of the *midasctl* commands fail, one of the following workarounds may help you.


Use a Different Python Environment
##################################

You could also try to use a different packaging system, e.g., *conda* (https://docs.conda.io/en/latest/).
If you're using *PyCharm*, you could try to use PyCharms' packacking tool as well.

Windows Subsystem for Linux
###########################

As another you can you the Subsystem for Linux (https://docs.microsoft.com/en-us/windows/wsl/install) and follow the installation instructions for Linux.
WSL integrates well, e.g., in the source code editor Visual Studio Code (there is a plugin that hides nearly all the Linux for you).
But this solution should work for PyCharm as well.
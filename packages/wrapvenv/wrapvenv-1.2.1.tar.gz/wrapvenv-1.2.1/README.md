# 1. One line description

Yet another python virtual environments manager


# 2. A more detailed description

Some python scripts require a set of python packages to be preinstalled in your
PC.

Using your Linux distro package manager to install missing packages does not
always work:

  - Not all python packages are available in all Linux distro package managers.
  - Some python scripts require a very specific version of one or more of those
    packages, which will probably be different from the ones your Linux distro
    package manager offers.

This script is meant to help you with that: instead of directly running a
script, you call "wrapvenv" with two arguments: 

  1. The path to a file containing all the needed python packages (and their
     versions)
  2. The name of the script to run

...it will then automatically create a virtual environment, install all the
needed python packages inside of it and finally run the script.

Example:

    $ wrapvenv --reqs frozen_requirements.txt my_script.py
                      ^^^^^^^^^^^^^^^^^^^^^^^ ^^^^^^^^^^^^
                      |                       `--> Script you want to run
                      `-----> List of needed python packages and versions

"wrapvenv" will also save the resulting virtual environment into a local cache
(in "~/.cache/wrapvenv") so that the next time you run a script using those same
requirements, the virtual environment will not have to be regenerated.


# 3. Installation

You don't want to use this repository directly. Instead you should install the
latest released version by running this command:

    $ python -m pip install wrapvenv

Once that is done, you should be able to run "wrapvenv" using any of these two
(equivalent) ways:

    $ python -m wrapvenv --help
    $ wrapvenv --help


# 4. Information for users

# 4.1. Scripts developers

When you are working on a script that you know will need a very specific set of
dependencies (in the form of python packages), do this:

  1. Create a text file with the list of python packages your script needs.
     Example:

         matplotlib
         PyQt6

  2. Use wrapvenv with "--freeze" to create a virtual environment with all the
     packages listed in the file frozen at the latest available version at that
     moment. This step will also create a new text file with the frozen list of
     packages and versions which will look something like this:

         contourpy==1.3.1
         cycler==0.12.1
         fonttools==4.55.3
         kiwisolver==1.4.8
         matplotlib==3.10.0
         numpy==2.2.1
         packaging==24.2
         pillow==11.0.0
         pyparsing==3.2.0
         PyQt6==6.8.0
         PyQt6-Qt6==6.8.1
         PyQt6_sip==13.9.1
         python-dateutil==2.9.0.post0
         six==1.17.0

  3. Develop your script in that virtual environment.
  4. When distributing your script, include the frozen list of packages in the
     distribution.

For more details, run this:

    $ python -m wrapvenv --help

# 4.2. Scripts users

Call wrapvenv providing the name of the script to run and the list of frozen
packages provided by the script developer (see section 4.1).

For more details, run this:

    $ python -m wrapvenv --help


# 5. Information for hackers

## 5.1. Development environment

Clone this repo, add its path to PYTHONPATH:

    $ git clone <this repo URL>
    $ export PYTHONPATH=`pwd`/wrapvenv

...and run it as any other python module:

    $ python -m wrapvenv --help

In order to crontribute to this project, please run this command and make sure
there are not errors before sending your patch:

    $ ruff check .

## 5.2. Distribution

The source code in this repository is meant to be distributed as a python
package that can be "pip install"ed.

Once you are ready to make a release:

  1. Increase the "version" number in file "pyproject.toml"
  2. Run the next command:

         $ ./release.sh

  3. Publish the contents of the "dist" folder to a remote package repository
     such as PyPi (see
     [here](https://packaging.python.org/en/latest/tutorials/packaging-projects/)).
     Example:

         $ python -m twine upload dist/*

  4. Tell your users that a new version is available and that they can install
     it by running this command:

         $ python -m pip install wrapvenv

     Once installed, they should be able to run it in any of these two
     (equivalent) ways:

         $ python -m wrapvenv --help
         $ wrapvenv --help


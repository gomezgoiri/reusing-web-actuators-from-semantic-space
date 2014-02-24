Reusing Web-enabled Actuators from Semantic Space-based Perspective
===================================================================

This project implements a basic scenario in three different ways to show:

 1. How to change the smart environment using [RESTdesc](http://restdesc.org).
 1. How to change the smart environment using a semantic shared space.
 1. How to make the second implementation interoperate with the first one.

Therefore, the goal of the third implementation is to exemplify how to seamlessly reuse an HTTP API from a space-aided consumer.
In other words, the consumer still writes _tasks_ into the space, which automatically consumes any needed HTTP API on its behalf.
To check that the interoperation is feasible, we completely reuse first scenario's provider and second scenario's consumer.
We only extend the space implementation.


Installation
------------

After cloning this project, to complete its installation you will need to:

 1. Install the requirements specified by _requirements.txt_ in your python environment.

        pip install -r requirements.txt

   * You might experience [an error installing _matplotlib_ and _numpy_ at the same time](http://stackoverflow.com/questions/19119042/pip-dependency-resolution-fails-when-install-both-numpy-and-matplotlib). If so, run the following command before re-executing the previous one.

            pip install pip install numpy==1.7.1
        
 2. Update the _eulerjar_ variable in _scripts/config.sh_ with your local _[EYE](http://eulersharp.sourceforge.net/) jar_ location.
    
    If you don't have _EYE_, you can [download it here](http://sourceforge.net/projects/eulersharp/files/eulersharp/).


Basic usage
-----------

To run each of the scenario's implementations, go to the _scripts_ folder and run the desired script:

    bash run_scenario_only_rest.sh
    bash run_scenario_only_space.sh
    bash run_scenario_mixed.sh


Directories
-----------

Feel free to check the code and give me any interesting feedback you want ;-)

 * _actuation_ is the main module which contains the code for the implementations.
  * _api_ defines the APIs of the nodes used in the scenario.
  * _impl_ contains the implementations of the APIs.
  * _proofs_ contains all the classes which intermediate with [EYE](http://eulersharp.sourceforge.net/).
   This module is an updated version of the one developed for [this project](https://github.com/gomezgoiri/actuationInSpaceThroughRESTdesc).
  * _scenarios_ includes the basic entry points which define the scenarios at high level.
  * _utils_ contains utility functions and classes.
 * _files_ has the resource descriptions, semantic files and queries.
  * _rest_ contains the files used in the first implementation.
  * _space_ contains the files used in the second implementation.
  * _mix_ contains the files which are specific to the third implementation.
 * _otsopy_ has OtsoPy's data access layer.
 * _scripts_ has the scripts which run the scenarios.
  * _config.sh_ is the file with the environment variables the user has to customize.
 * _tests_ some unit tests.


License
-------

Check the [COPYING file](https://github.com/gomezgoiri/actuationOnTripleSpace/blob/master/COPYING).

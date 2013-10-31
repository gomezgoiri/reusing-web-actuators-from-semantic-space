Actuation using Triple Spaces
=============================

This project implements a very basic scenario in three different ways to show:

 1. How to change the smart environment using [RESTdesc](http://restdesc.org)
 1. How to change the smart environment using a semantic shared space
 1. Basic interoperation between the previous implementations


Specifically, for the interoperation scenario, we wanted to exemplify how to seamlessly reuse an HTTP API from a space-aided consumer.
In other words, the consumer still writes _tasks_ into the space, which automatically consumes any needed HTTP API on its behalf.
To check that the interoperation is possible, we completely reuse first scenario's provider and second scenario's consumer.
We only extended the space implementation.


Installation
------------

You will need to install the requirements specified by _requirements.txt_ in you python environment.

    pip install -r requirements.txt


Basic usage
-----------

To run each of the scenario's implementations, go to the _scripts_ folder and run the desired script:

    bash run_scenario_only_rest.sh
    bash run_scenario_only_space.sh
    bash run_scenario_mixed.sh


Directories
-----------

I encourage you to check the code and give me any interesting feedback you want ;-)

 * _actuation_ is the main module which contains the code for the implementations
  * _api_ defines the APIs of the nodes used in the scenario
  * _impl_ contains the implementations of the APIs
  * _proofs_ contains all the classes which intermediate with [EYE](http://eulersharp.sourceforge.net/)
   * ( this module is an updated version of the one developed for [this project](https://github.com/gomezgoiri/actuationInSpaceThroughRESTdesc) )
  * _scenarios_ includes the basic entry points which define the scenarios at high level
  * _utils_ contains utility functions and classes
 * _files_ has the resource descriptions, semantic files and queries
  * _rest_ contains the files used in the first implementation
  * _space_ contains the files used in the second implementation
  * _mix_ contains the files which are specific to the third implementation
 * _otsopy_ has OtsoPy's data access layer
 * _scripts_ has the scripts which run the scenarios
  * _config.sh_ is the file with the environment variables the user has to customize
 * _tests_ some unit tests


License
-------

Check [COPYING.txt](https://github.com/gomezgoiri/actuationOnTripleSpace/blob/master/COPYING.txt).

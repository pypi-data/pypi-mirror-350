Gap processing
=============

We can loosely define a gap as a period of time when we should have trigger files but do not.
To be precise the following conditions must met:

+ The detector is in a proper state as defined by  the configuration file. Most groups
  use "low noise" (``DMT-GRD_ISC_LOCK_NOMINAL``). The environmental monitors do not
  require any particular state
+ The appropriate frame file(s) are available and discoverable using datafind.
+ There are no trigger files covering the time period. NB: Omicron may create
  trigger files with no triggers if the channel was sufficiently quiet.

The ``omicron-gaps`` program uses the above conditions to analyze a time period to
construct a condor DAG to fill any gaps found that are of significant length.
It is a very dynamic process with multiple stages. ``omicron-gaps`` creates the skeleton
which is fleshed out by each stage setting up the commands for the next. The overview
looks like:

* Omicron gaps creates and launches the skeleton DAG for each group specified
  on the command line.

  * The ``FIND`` job runs a single instance of ``omicron-find-gaps`` that examines DQ segments,
    frame file availability using datafind API, and the existence of trigger files using
    gwtriggerfind.  It then creates multiple bash scripts for the next stage. The
    number of scripts is a command line option.
  * As a child of the ``FIND`` job the ``FILL`` job uses the ``queue script matching``
    feature of htCondor to launch one job for each script created by the ``FIND`` job.
    Each script contains one or more calls to the ``omicron-process`` (pyomicron) program
    to create but not submit a DAG to process one gap interval.
  * A ``POST SCRIPT`` to the FILL job calls the program ``omicron-subdag-create`` to set up
    the final stage of the main DAG. This takes the DAGs created by ``omicron-process``
    and creates parent-child relationships to limit the number of parallel jobs accessing
    the same frame files.

The `omicron-gaps` program
++++++++++++++++++++++++++

.. command-output:: omicron-gaps --help


The ``omicron-find-gaps`` program
+++++++++++++++++++++++++++++++++

.. command-output:: omicron-find-gaps --help

The ``omicron-subdag-create`` program
+++++++++++++++++++++++++++++++++++++

.. command-output:: omicron-subdag-create --help

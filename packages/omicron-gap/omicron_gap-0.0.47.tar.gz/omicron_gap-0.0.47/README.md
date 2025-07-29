# Omicron gap related utilities

This package is a collection of utilities to compliment LIGO's detector 
characterization group Omicron trigger generator task. Our goal is to
visualize the times when we should have triggers and any gaps.

There are also programs to submit htCondor jobs to fill in 
those gaps.

* __omicron-batch-merge-dir__ - to reduce the number of files, this program 
  safely merges contiguous trigger files in a metric day
* __omicron-channel-check__ - examines each channel in our configuration file 
  to confirm it is available in current frame files.
* **omicron-compare-dirs** - Confirm that 2 directories have trigger files that cover 
  the same time period and have the same number of triggers. Works with merge programs
* **omicron-find-gaps** - Check DQ segments, frame availability and trigger file
  ecistance to determine which segments if any need to be reprocessed
* **omicron-gaps** 
* **omicron-gap-analysis**
* **omicron-merge-days**
* **omicron-metric-day-merge**
* **omicron-plot-gaps**
* **omicron-segfile-print**
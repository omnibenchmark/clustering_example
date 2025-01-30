#!/bin/bash

sudo singularity build sklearn.sif sklearn_singularity.def

sudo singularity build clustbench.sif clustbench_singularity.def

sudo singularity build r.sif r_singularity.def

sudo singularity build fcps.sif fcps_singularity.def

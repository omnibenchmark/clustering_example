#!/bin/sh
singularity build sklearn.sif sklearn_singularity.def
singularity build clustbench.sif clustbench_singularity.def
singularity build r.sif r_singularity.def
singularity build fcps.sif fcps_singularity.def

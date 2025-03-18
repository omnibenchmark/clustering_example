MAX_THREADS ?= 30
# by default, we want to run all snakemake rules even if there are failures
OB_CMD=ob run benchmark -k --local
prepare_apptainer_env:
	cd envs && ./build_singularity.sh
run_with_apptainer_backend:
	 ${OB_CMD} -b Clustering_singularity.yml --threads ${MAX_THREADS}
	 mv out out_apptainer
run_with_conda_backend:
	 ${OB_CMD} -b Clustering_conda.yml --threads ${MAX_THREADS}
	 mv out out_conda

MAX_CORES ?= 50

# without continue on error (-k)
OB_CMD=ob run benchmark --local --cores ${MAX_CORES} --yes

# prepare_apptainer_env:
# 	cd envs && bash build_singularity.sh

all: run_with_default_conda run_with_unpinned_oras run_with_default_envs # knit_report

run_with_default_conda:
	${OB_CMD} -b Clustering_conda.yml
	cp Clustering_conda.yml out
	mv out out_conda_$(shell date +'%Y%m%d_%H%M')

run_with_unpinned_oras:
	${OB_CMD} -b Clustering_oras.yml
	cp Clustering_oras.yml out
	mv out out_singularity_$(shell date +'%Y%m%d_%H%M')

run_with_default_envs:
	${OB_CMD} -b Clustering_envmodules.yml
	cp Clustering_envmodules.yml out
	mv out out_envmodules_$(shell date +'%Y%m%d_%H%M')

# ## derived from Mark's plots to process multiple benchmark runs at once
# knit_report: 
# 	## todo incorporate this report to this repo, downloading from a temporary branch `mark` is a bad idea
# 	## also control the environment this is run with
# 	wget -nc https://raw.githubusercontent.com/imallona/clustering_report/refs/heads/mark/07_metrics_across_backends.Rmd
# 	R -e 'rmarkdown::render("07_metrics_across_backends.Rmd", params = list(performance_bn = "performance-results.rds", metrics_bn = "metrics-results.rds", clustering_dir =  "."))'
# 	wget -nc https://github.com/imallona/clustering_report/blob/mark/08_performances_across_backends.Rmd
# 	R -e 'rmarkdown::render("08_performances_across_backends.Rmd", params = list(performance_bn = "performance-results.rds", metrics_bn = "metrics-results.rds", clustering_dir =  "."))'

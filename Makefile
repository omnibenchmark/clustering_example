MAX_CORES ?= 50
SEED ?= 2
RUN ?= 1
OB_FLAGS ?=          # e.g. OB_FLAGS="--filter slice.obfilter.yaml" for two datasets

# --dirty: ob wants it for modules at local paths, here the pinned submodules
# under modules/.
# One output tree per backend, seed and run, named as reports/across_backends.Rmd
# expects: out_<backend>_seed_<seed>_run_<run>
define run_plan
	sed -e 's/seed: [0-9]\+/seed: $(SEED)/' $(SANDBOX_SED) $(1) > .plan_seed_$(SEED).yml
	ob run .plan_seed_$(SEED).yml --dirty --cores $(MAX_CORES) --out-dir out_$(2)_seed_$(SEED)_run_$(RUN) $(OB_FLAGS) $(3)
	ob collect performance -o out_$(2)_seed_$(SEED)_run_$(RUN)
	rm .plan_seed_$(SEED).yml
endef

all: run_conda run_docker run_envmodules across_backends

run_conda:
	$(call run_plan,Clustering_conda.yml,conda)

# Containers see only the out dir: bind the plan directory too (report
# template). Not read-only: ":ro" reaches apptainer mangled. ob should bind it
# itself (omnibenchmark BUGS.md).
DOCKER_BINDS = $(CURDIR)

# SANDBOX=1, for hosts without /dev/fuse: build the images here and run them
# from envs/<name>.sif directories instead of pulling from the registry.
SANDBOX_SED = $(if $(filter 1,$(SANDBOX)),-e 's|docker://.*/\(.*\):.*|envs/\1.sif|')

run_docker:
	$(if $(filter 1,$(SANDBOX)),$(MAKE) -C envs sandbox)
	$(call run_plan,Clustering_docker.yml,docker,-- --singularity-args "--bind $(DOCKER_BINDS)")

run_envmodules:
	$(call run_plan,Clustering_envmodules.yml,envmodules)

# Compares every out_<backend>_seed_<seed>_run_<run> tree in this directory.
# Needs R with rmarkdown, dplyr, ggplot2 and jsonlite (envs/quarto.yml has them).
across_backends:
	Rscript -e 'rmarkdown::render("reports/across_backends.Rmd", params = list(runs_dir = normalizePath(".")), output_dir = ".")'

.PHONY: all run_conda run_docker run_envmodules across_backends

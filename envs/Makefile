# Build the container images of Clustering_docker.yml locally. Nothing is
# pushed anywhere.
#
#   make -C envs              # docker images, then apptainer images from them
#   make -C envs SANDBOX=1    # hosts without /dev/fuse: apptainer directories
#
# Snakemake (< 10) runs containers through apptainer only, so each Docker
# image is converted from the local Docker daemon into envs/<name>.sif.

TAG ?= 2.0.0
SANDBOX ?= 0
IMAGES = clustbench fcps quarto

all: $(IMAGES:%=%.sif)

%.sif: docker/%.Dockerfile $(wildcard docker/requirements-%.txt)
	docker build -t clustering_example/$*:$(TAG) -f $< docker
	rm -rf $@
	apptainer build $(if $(filter 1,$(SANDBOX)),--sandbox) $@ docker-daemon:clustering_example/$*:$(TAG)

clean:
	rm -rf $(IMAGES:%=%.sif)

.PHONY: all clean

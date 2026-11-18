# Container images of Clustering_docker.yml: one per method, plus clustbench
# (data, metrics) and quarto (report).
#
#   make -C envs              # docker build
#   make -C envs push         # build and push to $(REGISTRY); CI does this
#                             # (.github/workflows/images.yml)
#   make -C envs sandbox      # hosts without /dev/fuse, which cannot run the
#                             # images apptainer pulls: envs/<name>.sif directories

REGISTRY ?= ghcr.io/omnibenchmark/clustering_example
TAG ?= 2.0.0
IMAGES = clustbench fastcluster sklearn agglomerative genieclust fcps quarto

build: $(IMAGES:%=build-%)
push: $(IMAGES:%=push-%)
sandbox: $(IMAGES:%=%.sif)

# docker/<name>.Dockerfile if there is one, else python.Dockerfile with
# requirements-<name>.txt. The source label links the package to the repository.
build-%:
	docker build -t $(REGISTRY)/$*:$(TAG) --build-arg NAME=$* \
	  --label org.opencontainers.image.source=$(REGISTRY:ghcr.io/%=https://github.com/%) \
	  -f $(or $(wildcard docker/$*.Dockerfile),docker/python.Dockerfile) docker

push-%: build-%
	docker push $(REGISTRY)/$*:$(TAG)

%.sif: $(wildcard docker/*)
	$(MAKE) build-$*
	rm -rf $@
	apptainer build --sandbox $@ docker-daemon:$(REGISTRY)/$*:$(TAG)

clean:
	rm -rf $(IMAGES:%=%.sif)

.PHONY: build push sandbox clean

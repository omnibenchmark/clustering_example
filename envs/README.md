We distribute `Clustering.yml` runs with different backends.

- `Clustering_conda.yml`. Conda semi-reproducible (no pinning, pip)
- `Clustering_oras.yml`. Singularity non- to semi-reproducible, prebuilt remote images.
- `Clustering_envmodules.yml`. Easybuilt with default optimization.


## Conda

### Files

- `clustbench.yml`
- `fcps.yml`

### How to build

No need to `ob software conda pin / prepare`; let `ob run benchmark -b Clustering_conda.yml --local` do it.

## Apptainer semi-reproducible and local

### Files

- `clustbench_singularity.def`
- `fcps_singularity.def`

### How to build

- `build_singularity.sh`

### How to push to renku's gitlab registry

```
apptainer push --docker-username janedoe --docker-password glpat-uzh fcps.sif oras://registry.renkulab.io/izaskun.mallona/clustering_example/name:tag
```

## Aptainer semi-reproducible and remote

No need to prepare/build anything; let `ob run benchmark -b Clustering_oras.yml --local` do it using pre-built images from https://gitlab.renkulab.io/izaskun.mallona/clustering_example/container_registry.

## Apptainer (reproducible) with easybuild

This is pending work

## envmodules - reproducible builds with easybuild

### Files

- `clustbench.eb`
- `fcps.eb`

### How to build and warnings

1. Mind https://github.com/easybuilders/easybuild-easyconfigs/commit/e29210626f076e3a207f1abf3759ea124e28f8b2
2. Mind `clustbench` is only installable from https://github.com/gagolews/genieclust/archive/refs/tags/v1.1.6.tar.gz and not from pypi's tgz (!), download it locally and ideally update the easyconfig to automate this
3. `python3-wget` from pypi doesn't look very well maintaned
4. `eb fcps.eb --robot --ignore-checksums`
5. `eb clustbench.eb --robot --ignore-checksums`

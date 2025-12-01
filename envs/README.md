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

Using EESSI, python 3.12, and the foss/2024a toolchain.


```bash
source /cvmfs/software.eessi.io/versions/2025.06/init/lmod/bash
module load EESSI-extend/2025.06-easybuild
eb --robot clustbench.eb
```

Using EESSI and python 3.11, and the foss/2023a toolchain

```bash
source /cvmfs/software.eessi.io/versions/2023.06/init/lmod/bash
module load EESSI-extend/2023.06-easybuild
eb --robot fcps.eb
```

### Files

- `clustbench.eb`
- `fcps.eb`

### How to build and warnings

4. `eb fcps.eb --robot`
5. `eb clustbench.eb --robot`

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

### Files

- `clustbench.eb`
- `fcps.eb`

### Full workflow, with some tuning to select where stuff are built

Install CVMFS and mount EESSI: follow https://www.eessi.io/docs/getting_access/native_installation/ .

Extend EESSI with the extra packages needed to run clustbench via Easybuild. [Docs](https://www.eessi.io/docs/using_eessi/building_on_eessi/).

```bash

echo "Install cvmfs and mount EESSI; no instructions given here"

echo "Load latest EESSI"
source /cvmfs/software.eessi.io/versions/2025.06/init/lmod/bash
module load EESSI-extend/2025.06-easybuild


echo "Configure eb"
export EASYBUILD_PREFIX=path_to_your_installations_update_here
#export EASYBUILD_PREFIX=/data/imallona/.local/easybuild   ## RAID-6 in my case
export EASYBUILD_INSTALLPATH=$EASYBUILD_PREFIX/software
export EASYBUILD_BUILDPATH=$EASYBUILD_PREFIX/build
# export EASYBUILD_BUILDPATH=/opt/cache/imallona/build     ## SSD in my case
export EASYBUILD_REPOSITORYPATH=$EASYBUILD_PREFIX/ebfiles_repo
export EASYBUILD_SOURCEPATH=$EASYBUILD_PREFIX/sources
export EASYBUILD_PACKAGEPATH=$EASYBUILD_PREFIX/packages

echo "Configure temp path"
mkdir -p $HOME/tmp
export TMPDIR=$HOME/tmp

eb --robot fcps.eb --job-cores=10
eb --robot clustbench.eb --job-cores=10
```

Running a benchmark:

```bash
source /cvmfs/software.eessi.io/versions/2025.06/init/lmod/bash ## if not loaded
module load EESSI-extend/2025.06-easybuild                      ## if not loaded
export MODULEPATH="$EASYBUILD_PREFIX"/software/modules/all:"$MODULEPATH"
module use $MODULEPATH

ob run benchmark -b Clustering_envmodules.yml  --local-storage --cores 30
```

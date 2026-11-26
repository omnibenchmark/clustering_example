We distribute `Clustering.yml` runs with different backends.

- `Clustering_conda.yml`. Conda semi-reproducible (no pinning, pip)
- `Clustering_docker.yml`. Docker images built locally from `docker/*.Dockerfile`, pinned like the conda environments.
- `Clustering_envmodules.yml`. Easybuilt with default optimization. Can be built extending EESSI.


# Conda

## Files

- `clustbench.yml`
- `fcps.yml`

## How to build

No need to `ob software conda pin / prepare`; let `ob run benchmark -b Clustering_conda.yml --local` do it.

# Docker, built locally

## Files

- `docker/clustbench.Dockerfile`, `docker/requirements-clustbench.txt`: the
  `clustbench.yml` pins on `python:3.12.6-slim-bookworm`.
- `docker/fcps.Dockerfile`: `r-base:4.3.3` with CRAN read from a dated snapshot
  (2025-03-01), which has the versions `fcps.yml` pins.
- `Makefile`

## How to build

```
make -C envs             # docker build, then an apptainer image per Docker image
make -C envs SANDBOX=1   # hosts without /dev/fuse
```

Nothing is pushed. Snakemake before 10.0 runs containers through apptainer
only, so `Clustering_docker.yml` names `envs/<name>.sif`, converted from the
local Docker daemon. Without `/dev/fuse` apptainer cannot mount a `.sif`;
`SANDBOX=1` builds a directory under the same name instead.

# envmodules - reproducible builds with easybuild

## Compiling everything

It will take time (even days).

```bash
eb --robot envs/fcps.eb --job-cores=10
eb --robot envs/clustbench.eb --job-cores=10
```

## EESSI

Exteding EESSI 2025.06. cernvmfs has to be installed and EESSI configured.

### Full workflow to extend EESSI

Install CVMFS and mount EESSI: follow https://www.eessi.io/docs/getting_access/native_installation/ .

Extend EESSI with the extra packages needed to run clustbench via Easybuild. [Docs](https://www.eessi.io/docs/using_eessi/building_on_eessi/).

These snippets are verbose and somewhat tailored to our omnibenchmark machine.

```bash

echo "Install cvmfs and mount EESSI; no instructions given here"

echo "Load latest EESSI"
source /cvmfs/software.eessi.io/versions/2025.06/init/lmod/bash
module load EESSI-extend/2025.06-easybuild

echo "Configure eb"
export EASYBUILD_PREFIX=/path/to/install  # e.g., /data/mark/eessi/versions/2025.06/software/linux/x86_64/amd/zen2/
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

eb --robot envs/fcps.eb --job-cores=10
eb --robot envs/clustbench.eb --job-cores=10
```

Running a benchmark assuming the modules were installed within the `MODULE_BASEPATH`/software/modules/all path (perhaps `MODULE_BASEPATH` equals `$EASYBUILD_PREFIX`):

```bash
MODULE_BASEPATH='path/to/sw' # e.g., /data/mark/eessi/versions/2025.06/software/linux/x86_64/amd/zen2

source /cvmfs/software.eessi.io/versions/2025.06/init/lmod/bash ## if not loaded
module load EESSI-extend/2025.06-easybuild                      ## if not loaded
export MODULEPATH="$MODULE_BASEPATH"/software/modules/all:"$MODULEPATH"
module use $MODULEPATH
echo $MODULEPATH

# the resulting $MODULEPATH should contain both the MODULE_BASEPATH and EESSI's injections
# /data/mark/eessi/versions/2025.06/software/linux/x86_64/amd/zen2/software/modules/all:/home/mark/eessi/versions/2025.06/software/linux/x86_64/amd/zen2/modules/all:/cvmfs/software.eessi.io/host_injections/2025.06/software/linux/x86_64/amd/zen2/modules/all:/cvmfs/software.eessi.io/versions/2025.06/software/linux/x86_64/amd/zen2/modules/all:/cvmfs/software.eessi.io/init/modules

ob run Clustering_envmodules.yml --cores 10
```

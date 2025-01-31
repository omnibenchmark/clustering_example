We distribute `Clustering.yml` runs with different backends. Planned are:
- conda semi-reproducible (no pinning, pip)
- singularity semi-reproducible
- easybuild with several optimization strategies (ongoing)

## Conda

### Files

- `clustbench.yml`
- `fcps.yml`
- `r.yml`
- `sklearn.yml`

### How to build

No need to `ob software conda pin / prepare`; just let `ob run benchmark -b Clustering.yml --local` do it.

## Apptainer dirty

### Files

- `clustbench_singularity.def`
- `fcps_singularity.def`
- `r_singularity.def`
- `sklearn_singularity.def`

### How to build

- `build_singularity.sh`
- todo push to some ORAS-compatible registry

## Apptainer with easybuild

Lorem ipsum.

## Easybuild

### Files

- `clustbench.eb`
- `fcps.eb`

### How to build

1. Mind https://github.com/easybuilders/easybuild-easyconfigs/commit/e29210626f076e3a207f1abf3759ea124e28f8b2
2. Mind `clustbench` is only installable from https://github.com/gagolews/genieclust/archive/refs/tags/v1.1.6.tar.gz and not from pypi's tgz (!), download it locally and ideally update the easyconfig to automate this
3. `python3-wget` from pypi doesn't look very well maintaned
4. `eb fcps.eb --robot --ignore-checksums`
5. `eb clustbench.eb --robot --ignore-checksums`

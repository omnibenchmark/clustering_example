# R 4.3.2, as in ../fcps.yml. rocker/r-ver is Ubuntu (jammy), not Debian:
# no Debian repository keeps a pinned old R (CRAN's bookworm repo carries only
# the latest, and r-base tracks testing/sid, which no longer installs on top
# of its 2024 images).
#
# CRAN is read from a dated snapshot, so every package, dependencies included,
# is the version that was current that day: 2025-03-01 has the versions
# ../fcps.yml pins (FCPS 1.3.4, cluster 2.1.8, mclust 6.1.1, energy 1.7-12,
# dbscan 1.2.2, argparse 2.2.5, DataVisualizations 1.3.3, protoclust 1.6.4,
# cclust 0.6-26). The __linux__/jammy path serves prebuilt binaries.
FROM rocker/r-ver:4.3.2

ARG CRAN_SNAPSHOT=https://packagemanager.posit.co/cran/__linux__/jammy/2025-03-01

# python3: R's argparse runs its parser in Python. libgsl27: energy -> gsl.
# The base image pins its Ubuntu release; apt package versions are not pinned.
# hadolint ignore=DL3008
RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 libgsl27 \
 && rm -rf /var/lib/apt/lists/*

RUN Rscript -e "options(repos = c(CRAN = '${CRAN_SNAPSHOT}'), Ncpus = parallel::detectCores()); \
      pkgs <- c('FCPS', 'cluster', 'mclust', 'energy', 'dbscan', 'argparse', \
                'DataVisualizations', 'protoclust', 'cclust', 'R.utils'); \
      install.packages(pkgs); \
      missing <- setdiff(pkgs, rownames(installed.packages())); \
      if (length(missing)) stop('not installed: ', paste(missing, collapse = ', '))"

# The `report` stage: omni-quarto-report (render.py, Python) renders
# reports/report.Rmd with quarto. Versions as in ../quarto.yml resolved for
# the conda run: R 4.3.2, quarto 1.11.9, and a CRAN snapshot (2025-05-01) with
# rmarkdown 2.29, knitr 1.50, ggplot2 3.5.2, dplyr 1.1.4, tidyr 1.3.1 and
# jsonlite 2.0.0. Ubuntu-based for the same reason as fcps.Dockerfile.
FROM rocker/r-ver:4.3.2

ARG CRAN_SNAPSHOT=https://packagemanager.posit.co/cran/__linux__/jammy/2025-05-01
ARG QUARTO_VERSION=1.11.9

# hadolint ignore=DL3008
RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 \
 && rm -rf /var/lib/apt/lists/* \
 && /rocker_scripts/install_quarto.sh "${QUARTO_VERSION}"

RUN Rscript -e "options(repos = c(CRAN = '${CRAN_SNAPSHOT}'), Ncpus = parallel::detectCores()); \
      pkgs <- c('rmarkdown', 'knitr', 'jsonlite', 'ggplot2', 'dplyr', 'tidyr'); \
      install.packages(pkgs); \
      missing <- setdiff(pkgs, rownames(installed.packages())); \
      if (length(missing)) stop('not installed: ', paste(missing, collapse = ', '))"

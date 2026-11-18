A clustering example for omnibenchmark

# How to run

1. Install omnibenchmark using [our tutorial](https://docs.omnibenchmark.org/latest/howto/#install-omnibenchmark)
2. Clone the benchmark plan / this repository with `git clone --recurse-submodules git@github.com:omnibenchmark/clustering_example.git`. The modules are git submodules under `modules/`, each pinned to a commit (`git submodule status`); in an existing clone, `git submodule update --init`
3. Move to the cloned repository `cd clustering_example`
4. Run locally, somewhat in parallel `ob run CLUSTERING.YAML --dirty --cores 6` (`--dirty` because the plans name the modules by local path). Choose `Clustering.yml` plan based on whether running it with conda, easybuild, apptainer, etc. [More details about the available backends](https://github.com/omnibenchmark/clustering_example/blob/main/envs/README.md).

The plans are written for omnibenchmark api 0.8.0.

## A quick check on two datasets

`slice.obfilter.yaml` keeps two small datasets (`fcps/atom`, `fcps/chainlink`) and
every method and metric:

    ob run Clustering_conda.yml --dirty --filter slice.obfilter.yaml --cores 6

## Reports

- `metrics` (every plan) gathers the clusterings of a dataset and writes one
  `summary.tsv` for it: every metric of the plan's `metrics` list, with the
  dataset, method and parameters of each score.
- `report` (conda plan) renders `reports/report.Rmd` over those tables into
  `out/report/report.html`.
- `reports/across_backends.Rmd` compares several runs (backends, seeds, repeats).
- `tools/verify_zenodo.py OUT` checks the scores of a run against the runs
  archived with the paper (https://doi.org/10.5281/zenodo.18598405). The
  archive used seeds 20, 54 and 85: `make run_conda SEED=20`.
  It is not part of a run: `make run_conda run_docker run_envmodules across_backends`.

# Disclaimer

This does not work in arm64.

# Clustbench attribution

by Marek Gagolewski, modified by Izaskun Mallona (some edits to the plan(s) by Ben Carrillo, Mark Robinson)

# Data disclaimer

Some datasets are commented out to speed up calculations.

From [Are cluster validity measures (in) valid?](https://www.sciencedirect.com/science/article/pii/S0020025521010082):

> The original benchmark battery consists of 79 data instances, however 16 datasets are accompanied by labels that yield ; they were omitted for their computation would be too lengthy (namely: mnist/digits, mnist/fashion, other/chameleon_t7_10k, other/chameleon_t8_8k, sipu/a1, sipu/a2, sipu/a3, sipu/birch1, sipu/birch2, sipu/d31, sipu/s1, sipu/s2, sipu/s3, sipu/s4, sipu/worms_2, sipu/worms_64). Also uci/glass has been removed as one of its 25-near-neighbour graph’s connected components was too small for the NN-based methods to succeed. This leaves us with 62 datasets in total.

A yaml such as [0a88c91](https://github.com/omnibenchmark/clustering_example/blob/0a88c910bbda62d1b593f4215a682770227f39ff/Clustering.yaml) with 30 cores should run half of the stuff in ~4 h and reach 97% completion in ~8h.

# Summary

- Data. Example datasets (not a comprehensive list, it's >60 of them):
  - https://github.com/imallona/clustbench_data 
        parameters:
          - generator: "{module.id}" # 9
            dataset_name: ["atom", "chainlink", "engytime", "hepta", "lsun", "target", "tetra", "twodiamonds", "wingnut"]
          - generator: "{module.id}" # 10 datasets
            dataset_name: ["dense", "fuzzyx", "line", "parabolic", "ring", "ring_noisy", "ring_outliers", "zigzag", "zigzag_noisy", "zigzag_outliers"]
          - generator: "{module.id}" # 6 datasets
            dataset_name: ["chameleon_t4_8k", "chameleon_t5_8k", "hdbscan", "iris", "iris5", "square"]
          - generator: "{module.id}" # 8 datasets
            dataset_name: ["aggregation", "compound", "flame", "jain", "pathbased", "r15", "spiral", "unbalance"]
          - generator: "{module.id}" # 7 datasets
            dataset_name: ["ecoli", "ionosphere", "sonar", "statlog", "wdbc", "wine", "yeast"]
          - generator: "{module.id}" # 22 datasets
            dataset_name: ["circles", "cross", "graph", "isolation", "labirynth", "mk1", "mk2", "mk3", "mk4", "olympic", "smile", "stripes", "trajectories", "trapped_lovers", "twosplashes", "windows", "x1", "x2", "x3", "z1", "z2", "z3"]
- Method families/providers (they include several methods each)
  - https://github.com/imallona/clustbench_fastcluster
        parameters:
          - linkage: ["complete", "ward", "average", "weighted", "median", "centroid"]
  - https://github.com/imallona/clustbench_sklearn 
        parameters:
          - method: ["birch", "kmeans", "gm"]
          # "spectral" ## too slow
  - https://github.com/imallona/clustbench_agglomerative
        parameters:
          - linkage: ["average", "complete", "ward"]
  - https://github.com/imallona/clustbench_genieclust
        parameters:
          - method: "genie"
            gini_threshold: 0.5
          - method: ["gic", "ica"]
  - https://github.com/imallona/clustbench_fcps
        parameters:
          - method: ["FCPS_Minimax", "FCPS_MinEnergy", "FCPS_HDBSCAN_2", "FCPS_HDBSCAN_4", "FCPS_HDBSCAN_8", "FCPS_Diana", "FCPS_Fanny", "FCPS_Hardcl", "FCPS_Softcl", "FCPS_Clara", "FCPS_PAM"]
            seed: 2
          # - "FCPS_AdaptiveDensityPeak" # not in Conda
- Metric providers (several metrics)
  - https://github.com/imallona/clustbench_metrics
        parameters:
          - metric: ["normalized_clustering_accuracy", "adjusted_fm_score", "adjusted_rand_score"]
          # - "adjusted_mi_score"
          # - "adjusted_rand_score"
          # - "fm_score"
          # - "mi_score"
          # - "normalized_clustering_accuracy"
          # - "normalized_mi_score"
          # - "normalized_pivoted_accuracy"
          # - "pair_sets_index"
          # - "rand_score"
  - https://github.com/imallona/clustering_report
- Daniel modules (independent from clustbench)
  - https://github.com/omnibenchmark-example/iris.git
  - https://github.com/omnibenchmark-example/penguins.git
  - https://github.com/omnibenchmark-example/kmeans.git
  - https://github.com/omnibenchmark-example/ward.git
  - https://github.com/omnibenchmark-example/ari.git
  - https://github.com/omnibenchmark-example/accuracy.git
  
  
# Software backends

In `envs`: conda, Docker (built locally), easybuild (lmod modules)

# Warnings

Note that we try to run clusterings specifying the true number of clusters +- 2. But sometimes the true number is k=3. Then we do `k=2, k=2, k=3, k=5, k=6` filling with k=2s as needed, and recomputing the same values multiple times (so runtimes are comparable across datasets, regardless of their true number of clusters).

Also, we have modules by Daniel Incicau that are not fully incorporated into Gagolewski's flow.

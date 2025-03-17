A clustering example for omnibenchmark

# How to run

1. Install omnibenchmark using [our tutorial](https://omnibenchmark.org/tutorial/)
2. Clone the benchmark definition / this repository with `git clone https://github.com/omnibenchmark/clustering_example`
3. Move into the cloned folder: `cd clustering_example`
4. Run locally, somewhat in parallel `ob run benchmark -b CLUSTERING.YAML  --local --threads 6`. Choose `Clustering.yml` specification based on whether running it with conda, easybuild, apptainer, etc. [More details about the available backends](https://github.com/omnibenchmark/clustering_example/blob/main/envs/README.md).

# Clustbench attribution

by Marek Gagolewski, modified by Izaskun Mallona

# Data disclaimer

Some datasets are commented out to speed up calculations.

From [Are cluster validity measures (in) valid?](https://www.sciencedirect.com/science/article/pii/S0020025521010082):

> The original benchmark battery consists of 79 data instances, however 16 datasets are accompanied by labels that yield ; they were omitted for their computation would be too lengthy (namely: mnist/digits, mnist/fashion, other/chameleon_t7_10k, other/chameleon_t8_8k, sipu/a1, sipu/a2, sipu/a3, sipu/birch1, sipu/birch2, sipu/d31, sipu/s1, sipu/s2, sipu/s3, sipu/s4, sipu/worms_2, sipu/worms_64). Also uci/glass has been removed as one of its 25-near-neighbour graph’s connected components was too small for the NN-based methods to succeed. This leaves us with 62 datasets in total, see Table 1.

A yaml such as [0a88c91](https://github.com/omnibenchmark/clustering_example/blob/0a88c910bbda62d1b593f4215a682770227f39ff/Clustering.yaml) with 30 cores should run half of the stuff in ~4 h and reach 97% completion in ~8h.

# Summary

- Data. Example datasets (not a comprehensive list, it's >79 of them):
  - https://github.com/imallona/clustbench_data 
    - args: ["--dataset_generator", "mnist", "--dataset_name", "fashion"]
    - args: ["--dataset_generator", "other", "--dataset_name", "iris"]
    - args: ["--dataset_generator", "mnist", "--dataset_name", "digits"]
    - args: ["--dataset_generator", "wut", "--dataset_name", "circles"]
- Method families/providers (they include several methods each)
  - https://github.com/imallona/clustbench_fastcluster
    - args: ["--linkage", "complete"]
    - args: ["--linkage", "ward"]
    - args: ["--linkage", "average"]
    - args: ["--linkage", "weighted"]
    - args: ["--linkage", "median"]
    - args: ["--linkage", "centroid"]
  - https://github.com/imallona/clustbench_sklearn 
    - args: ["--method", "birch"]
    - args: ["--method", "kmeans"]
    - args: ["--method", "spectral"] ## too slow
    - args: ["--method", "gm"]
  - https://github.com/imallona/clustbench_agglomerative
    - args: ["--linkage", "average"]
    - args: ["--linkage", "complete"]
    - args: ["--linkage", "ward"]
  - https://github.com/imallona/clustbench_genieclust
    - args: ["--method", "genie", "--gini_threshold", 0.5]
    - args: ["--method", "gic"]
    - args: ["--method", "ica"]
  - https://github.com/imallona/clustbench_fcps
    - args: ["--method", "FCPS_Minimax"]
    - args: ["--method", "FCPS_MinEnergy"]
    - args: ["--method", "FCPS_HDBSCAN_2"]
    - args: ["--method", "FCPS_HDBSCAN_4"]
    - args: ["--method", "FCPS_HDBSCAN_8"]
    - args: ["--method", "FCPS_Diana"]
    - args: ["--method", "FCPS_Fanny"]
    - args: ["--method", "FCPS_Hardcl"]
    - args: ["--method", "FCPS_Softcl"]
    - args: ["--method", "FCPS_Clara"]
    - args: ["--method", "FCPS_PAM"]
- Metric providers (several metrics)
  - https://github.com/imallona/clustbench_metrics
    - args: ["--metric", "normalized_clustering_accuracy"]
    - args: ["--metric", "adjusted_fm_score"]
    - args: ["--metric", "adjusted_mi_score"]
    - args: ["--metric", "adjusted_rand_score"]
    - args: ["--metric", "fm_score"]
    - args: ["--metric", "mi_score"]
    - args: ["--metric", "normalized_clustering_accuracy"]
    - args: ["--metric", "normalized_mi_score"]
    - args: ["--metric", "normalized_pivoted_accuracy"]
    - args: ["--metric", "pair_sets_index"]
    - args: ["--metric", "rand_score"]
- Metric collector
  - https://github.com/imallona/clustering_report
- Daniel modules (independent from clustbench)
  - https://github.com/omnibenchmark-example/iris.git
  - https://github.com/omnibenchmark-example/penguins.git
  - https://github.com/omnibenchmark-example/kmeans.git
  - https://github.com/omnibenchmark-example/ward.git
  - https://github.com/omnibenchmark-example/ari.git
  - https://github.com/omnibenchmark-example/accuracy.git
  
  
# Software backends

In `envs`: conda, apptainer, easybuild (lmod modules)

# Warnings

Mind we try to run clusterings specifying the true number of clusters +- 2. But sometimes the true number is k=3. Then we do `k=2, k=2, k=3, k=5, k=6` filling with k=2s as needed, and recomputing the same values multiple times (so runtimes are comparable across datasets, regardless of their true number of clusters).

Also, we have modules by Daniel not fully incorporated into Gagolewski's flow.

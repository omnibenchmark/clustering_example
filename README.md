A clustering example for omnibenchmark

# How to run

1. Install omnibenchmark with conda capabilities using [our tutorial](https://omnibenchmark.org/tutorial/)
2. Clone the benchmark definition / this repository with `git clone --branch gagolewski git@github.com:omnibenchmark/clustering_example.git`
3. Move to the cloned repository `cd clustering_example`
4. Run locally, somewhat in parallel `ob run benchmark -b Clustering.yaml  --local --threads 6` (do not use lots of threads, this version uses conda and filesystem latency can be a problem)

# Clustbench attribution

by Marek Gagolewski, modified by Izaskun Mallona

# Summary

- Data
  - https://github.com/imallona/clustbench_data 
    - args: ["--dataset_generator", "mnist", "--dataset_name", "fashion"]
    - args: ["--dataset_generator", "other", "--dataset_name", "iris"]
    - args: ["--dataset_generator", "mnist", "--dataset_name", "digits"]
    - args: ["--dataset_generator", "wut", "--dataset_name", "circles"]
    - args: ["--dataset_generator", "wut", "--dataset_name", "cross"]
    - args: ["--dataset_generator", "wut", "--dataset_name", "graph"]
    - args: ["--dataset_generator", "wut", "--dataset_name", "isolation"]
    - args: ["--dataset_generator", "wut", "--dataset_name", "labirynth"]
    - args: ["--dataset_generator", "wut", "--dataset_name", "mk1"]
    - args: ["--dataset_generator", "wut", "--dataset_name", "mk2"]
    - args: ["--dataset_generator", "wut", "--dataset_name", "mk3"]
    - args: ["--dataset_generator", "wut", "--dataset_name", "mk4"]
    - args: ["--dataset_generator", "wut", "--dataset_name", "olympic"]
    - args: ["--dataset_generator", "wut", "--dataset_name", "smile"]
    - args: ["--dataset_generator", "wut", "--dataset_name", "stripes"]
    - args: ["--dataset_generator", "wut", "--dataset_name", "trajectories"]
    - args: ["--dataset_generator", "wut", "--dataset_name", "trapped_lovers"]
    - args: ["--dataset_generator", "wut", "--dataset_name", "twosplashes"]
    - args: ["--dataset_generator", "wut", "--dataset_name", "windows"]
    - args: ["--dataset_generator", "wut", "--dataset_name", "x1"]
    - args: ["--dataset_generator", "wut", "--dataset_name", "x2"]
    - args: ["--dataset_generator", "wut", "--dataset_name", "x3"]
    - args: ["--dataset_generator", "wut", "--dataset_name", "z1"]
    - args: ["--dataset_generator", "wut", "--dataset_name", "z2"]
    - args: ["--dataset_generator", "wut", "--dataset_name", "z3"]
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

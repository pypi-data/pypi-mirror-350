# QUARK-plugin-pvc


### Provided Modules:

| Module                              | Upstream Interface          | Downstream Interface        |
|-------------------------------------| --------------------------- | --------------------------- |
| pvc_graph_provider                  | None                        | quark.interface_types.graph |
| pvc_qubo_mapping                    | quark.interface_types.graph | quark.interface_types.qubo  |
| greedy_classical_pvc_solver         | quark.interface_types.graph | None                        |
| reverse_greedy_classical_pvc_solver | quark.interface_types.graph | None                        |
| random_classical_pvc_solver         | quark.interface_types.graph | None                        |

<!-- ### Reference Graph

If you want to run a benchmark with the reference graph used in [Finzgar et al.](https://arxiv.org/pdf/2202.03028)
you must create it using the following command:

TODO -->

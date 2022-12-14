from qiskit.converters import circuit_to_dag
import networkx as nx
import pandas as pd
import time

def is_gate_predicate(gate_name):
    return lambda i: i.operation.name == gate_name

def summarize_circuit(circuit):
    # length of critical path
    print(f"Depth: {circuit.depth()}")
    # number of qubits plus clbits in circui
    print(f"Width: {circuit.width()}")
    # gates involving 2+ qubits
    print(f"Non-local gate count: {circuit.num_nonlocal_gates()}")

    # gates along the critical path
    graph = circuit_to_dag(circuit)
    longest_path = graph.longest_path()
    for node in longest_path:
        print(node.op.name)

    # execution time

    # aggregated error

def fetch_calibration_data(provider):
    for backend in provider.backends():
        backend_name = backend.name()
        # t = datetime(day=15, month=4, year=2020, hour=10)
        props = backend.properties()
        config = backend.configuration()

        cols = ["T1 (us)",
                "T2 (us)",
                "frequency (GHz)",
                "anharmonicity (GHz)",
                "readout_error ()",
                "prob_meas0_prep1 ()",
                "prob_meas1_prep0 ()",
                "readout_length (ns)"]

        n_qubits = config.n_qubits

        if props is not None:
            p_dict = props.to_dict()
            df = pd.DataFrame(columns=cols, index=list(range(n_qubits)))

            for i, qubit in enumerate(p_dict["qubits"]):
                for prop in qubit:
                    name = prop["name"]
                    unit = prop["unit"]
                    value = prop["value"]
                    label = f"{name} ({unit})"

                    df.loc[i, label] = value

            df.to_csv(f"{backend_name}_props.csv")

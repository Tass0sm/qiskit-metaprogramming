from qiskit import QuantumCircuit
import qiskit
import ast

loop_expressions = [ast.For, ast.comprehension]
def is_loop(e):
    return any(map(lambda c: isinstance(e, c), loop_expressions))


with open("./circuit1.py", "r") as f:
    circuit_program = f.read()

prog_ast = ast.parse(circuit_program)
# print(ast.dump(prog_ast, indent=4))



# assumption 1: first expression declares the circuit and QuantumCircuit is in scope.
circuit_declaration = prog_ast.body[0]
# assumption 2: the rest of the program builds the circuit
circuit_body = prog_ast.body[1:]



# declare the circuit so that we can run statements on it later
exec(ast.unparse(circuit_declaration))

for expr in circuit_body:
    if is_loop(expr):
        iter = eval(ast.unparse(expr.iter))
        r = list(iter)

        print("Found a Loop")
        print(f"Loop repeats over the following range: {r}")
        print("Loop gates include:")
        for i, loop_expr in enumerate(expr.body):
            r = eval(ast.unparse(loop_expr))
            print (f"{i+1}.")
            
            if isinstance(r, qiskit.circuit.instructionset.InstructionSet):
                print(f"instructions = {r.instructions}")
                print(f"classical args = {r.cargs}")
                print(f"quantum args = {r.qargs}\n")



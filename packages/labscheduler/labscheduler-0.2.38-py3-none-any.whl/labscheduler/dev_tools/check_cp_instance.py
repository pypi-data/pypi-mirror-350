from google.protobuf import text_format
from ortools.sat.python.cp_model import CpModel, CpSolver

model = CpModel()
with open("infeasible.txt") as reader:
    text_format.Parse(reader.read(), model.Proto())
solver = CpSolver()
status = solver.Solve(model)
print(solver.status_name(status))  # noqa: T201

import gurobipy as gp
from gurobipy import GRB
import numpy as np

m = None

def main():
    global m

    orbit_size = 12
    times = 3
    size = orbit_size * times
    b0 = 10  # Battery at t=0
    max_batt = 100  # Max Battery Value

    # dt = 0.9  # Discretization time quanta
    # r = 0.2 * 2 * dt   # Charge-Discharge Rate

    dt = 1  # Discretization time quanta
    r = 1   # Charge-Discharge Rate
    transition_steps = 4

    # 1 if charge-acquisition edge
    _edge_detector = np.zeros((size - 1, size))
    for i in range(size - 1):
        _edge_detector[i, i] = 1
        _edge_detector[i, i + 1] = 1

    m = gp.Model("CIARC Scheduler")

    a = m.addVars(size, vtype=GRB.BINARY, name="acquisition")
    c = m.addVars(size, vtype=GRB.BINARY, name="charge")
    b = m.addVars(size, vtype=GRB.CONTINUOUS, name="battery", lb=0, ub=max_batt)

    # Full Coverage Constraint
    mod = m.addVars(orbit_size, vtype=GRB.BINARY, name="mod")
    for orbit_val in range(orbit_size):
        m.addGenConstrOr(mod[orbit_val], [a[orbit_size*i+orbit_val] for i in range(times)], f"orconstr_{orbit_val}")

    coverage = m.addVars(orbit_size, vtype=GRB.BINARY, name="coverage")
    for orbit_val in range(orbit_size):
        m.addGenConstrIndicator(mod[orbit_val], True, coverage[orbit_val] == 1, name=f"cover_{orbit_val}")
        m.addGenConstrIndicator(mod[orbit_val], False, coverage[orbit_val] == 0, name=f"cover_{orbit_val}")

    m.addConstr(gp.quicksum(coverage[orbit_val] for orbit_val in range(orbit_size)) == orbit_size, name="full_coverage")

    # Transition Time Constraint
    edges_c_a = m.addVars(size-1, vtype=GRB.BINARY, name="edges_c_a")
    edges_a_c = m.addVars(size-1, vtype=GRB.BINARY, name="edges_a_c")
    edges = m.addVars(size-1, vtype=GRB.BINARY, name="edges")
    
    for i in range(size - 1):
        m.addGenConstrAnd(
            edges_c_a[i], [c[i], a[i+1]],
            name=f"edges_c_a{i}"
        )

        m.addGenConstrAnd(
            edges_a_c[i], [a[i], c[i+1]],
            name=f"edges_a_c{i}"
        )

        m.addGenConstrOr(
            edges[i], [edges_a_c[i], edges_c_a[i]],
            name=f"edges_a_c{i}"
        )

    t = m.addVars(size, vtype=GRB.BINARY, name="transitioning")
    for i in range(size-1):

        m.addConstrs(
            ((edges[i] == 1) >> (a[i+j] == 0) for j in range(1, transition_steps+1) if i+j<size),
            name=f"transition_time_acquisition_{i+1}"
        )
        m.addConstrs(
            ((edges[i] == 1) >> (c[i+j] == 0) for j in range(1, transition_steps+1) if i+j<size),
            name=f"transition_time_charge_{i+1}"
        )

        # m.addConstrs(
        #     ((edges[i] == 0) >> (t[i+j] == 0) for j in range(1, transition_steps+1) if i+j<size),
        #     name=f"transition_{i+1}"
        # )

        m.addConstrs(
            ((edges[i] == 1) >> (t[i+j] == 1) for j in range(1, transition_steps+1) if i+j<size),
            name=f"transition_{i+1}"
        )


    m.addConstr(
        t[size-1] == 0,
        name=f"transition_{size-1}"
    )


    # Idle State Defragmentation
    authorized_transitions = m.addVars(size, vtype=GRB.BINARY, name="authorized_transitions")
    for i in range(size):
        m.addGenConstrOr(authorized_transitions[i], [t[i], c[i], a[i]], name="authorized_transitions_init")

    for i in range(size-1):
        m.addConstr(authorized_transitions[i] >= authorized_transitions[i+1])
    

    # Battery Constraints
    m.addConstr(
        b[0] == b0,
        name = "battery_status_0"
    )

    for i in range(1, size):
        m.addConstr(
            b[i] == b[j := i-1] + r * (c[j] - a[j]),
            name = f"battery_status_{i}"
        )

        m.addConstr(
            b[i] >= 1,
            name = "battery_charge_constraint"
        )
    
    # States Mutual Exclusion Constraint
    for i in range(size):
        m.addConstr(
            (c[i] + a[i]) <= 1,
            name = "mut_ex"
        )
    
    m.setObjective(t.sum() + edges.sum(), GRB.MINIMIZE)
    m.optimize()


    for v in m.getVars():
        if "edge_detector" in v.VarName: continue
        print(f"{v.VarName} {v.X:g}")

    print(f"Obj: {m.ObjVal:g}")



if __name__ == "__main__":
    try:
        main()

    except gp.GurobiError as e:
        print(f"Error code {e.errno}: {e}")

    except AttributeError:
        print("Encountered an attribute error")
        # m.computeIIS()

        # for c in m.getConstrs():
        #     if c.IISConstr: print(f'\t{c.constrname}: {m.getRow(c)} {c.Sense} {c.RHS}')
        

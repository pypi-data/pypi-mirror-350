import numpy as np
from scipy.optimize import linprog, milp, Bounds, LinearConstraint

def parse_dscp(dscp):
    dscp_map = {
        'default': 0, 'cs0': 0, 'cs1': 8, 'af11': 10, 'af12': 12, 'af13': 14, 'cs2': 16, 'af21': 18, 'af22': 20,
        'af23': 22, 'cs3': 24, 'af31': 26, 'af32': 28, 'af33': 30, 'cs4': 32, 'af41': 34, 'af42': 36, 'af43': 38,
        'cs5': 40, 'va': 44, 'ef': 46, 'cs6': 48, 'cs7': 56
    }
    try:
        return int(dscp)
    except:
        return dscp_map.get(dscp.strip().lower(), None)

def reverse_dscp(dscp):
    dscp_reverse_map = {
        0: 'default', 8: 'cs1', 10: 'af11', 12: 'af12', 14: 'af13', 16: 'cs2', 18: 'af21', 20: 'af22', 22: 'af23',
        24: 'cs3', 26: 'af31', 28: 'af32', 30: 'af33', 32: 'cs4', 34: 'af41', 36: 'af42', 38: 'af43', 40: 'cs5',
        44: 'va', 46: 'ef', 48: 'cs6', 56: 'cs7'
    }
    return dscp_reverse_map.get(dscp, f"dscp {dscp}")

def aggregate_flows(N, M, a, dscp_values, K=64):
    kf = np.array(dscp_values)
    ranges = []
    step = 64 // N
    remainder = 64 % N
    start = 0
    for i in range(N):
        end = start + step + (1 if i < remainder else 0)
        ranges.append(range(start, end))
        start = end
    kq = [np.mean(r) for r in ranges]
    Aeq = np.zeros((M, M * N))
    for i in range(M):
        Aeq[i, i * N:(i + 1) * N] = 1
    beq = np.ones(M)
    hx = np.array([(kf[i] - kq[j])**2 for i in range(M) for j in range(N)])
    for i in range(M):
        for j in range(N):
            hx[i * N + j] = (kf[i] - kq[j])**2 + 1
    integrality = np.ones(M * N)
    bounds = Bounds(np.zeros(M * N), np.ones(M * N))
    constraint_eq = LinearConstraint(Aeq, beq, beq)
    res = milp(c=hx, integrality=integrality, bounds=bounds, constraints=[constraint_eq])
    if not res.success:
        raise ValueError("MILP не вдалося знайти рішення. Перевірте вхідні дані.")
    x = res.x
    x2 = np.zeros((N, M))
    for i in range(M):
        x2[:, i] = x[i*N:(i+1)*N]
    return x2, kq

def find_min_Dmin(N, M, a, x2, kq, K, B, Dmin, max_Dmin):
    found = False
    while Dmin <= max_Dmin:
        try:
            D_range = np.arange(Dmin, 151, 5)
            poo = []
            for D in D_range:
                h = 1 + np.array(kq) / (K * D)
                aa = np.zeros(N)
                for i in range(N):
                    for j in range(M):
                        aa[i] += a[j] * x2[i, j]
                A = np.hstack([-np.eye(N), (h * aa).reshape(-1, 1)])
                b = np.zeros(N)
                Aeq_lp = np.hstack([np.ones(N), 0])
                beq_lp = np.array([B])
                f_lp = np.hstack([np.zeros(N), -1])
                lb = np.zeros(N + 1)
                ub = np.hstack([np.full(N, B), np.inf])
                res_lp = linprog(f_lp, A_ub=A, b_ub=b, A_eq=[Aeq_lp], b_eq=beq_lp,
                                 bounds=list(zip(lb, ub)), method='highs')
                if res_lp.status != 0:
                    raise ValueError("LP не вдалося знайти рішення. Перевірте вхідні дані.")
                x3 = res_lp.x
                po = []
                for j in range(N):
                    if x3[j] != 0:
                        po.append(aa[j] / x3[j])
                    else:
                        po.append(0)
                poo.append(po)
            found = True
            break
        except ValueError:
            Dmin += 1
    if not found:
        raise ValueError("Не вдалося знайти мінімальне Dmin, яке забезпечує коректну роботу.")
    return Dmin

def calculate_bandwidths(N, M, a, x2, kq, K, B, Dmin):
    D_range = np.arange(Dmin, 151, 5)
    poo = []
    x3 = None
    for D in D_range:
        h = 1 + np.array(kq) / (K * D)
        aa = np.zeros(N)
        for i in range(N):
            for j in range(M):
                aa[i] += a[j] * x2[i, j]
        A = np.hstack([-np.eye(N), (h * aa).reshape(-1, 1)])
        b = np.zeros(N)
        Aeq_lp = np.hstack([np.ones(N), 0])
        beq_lp = np.array([B])
        f_lp = np.hstack([np.zeros(N), -1])
        lb = np.zeros(N + 1)
        ub = np.hstack([np.full(N, B), np.inf])
        res_lp = linprog(f_lp, A_ub=A, b_ub=b, A_eq=[Aeq_lp], b_eq=beq_lp,
                         bounds=list(zip(lb, ub)), method='highs')
        if res_lp.status != 0:
            raise ValueError("LP не вдалося знайти рішення. Перевірте вхідні дані.")
        x3 = res_lp.x
        po = []
        for j in range(N):
            if x3[j] != 0:
                po.append(aa[j] / x3[j])
            else:
                po.append(0)
        poo.append(po)
    return np.array(poo), x3, D_range

def generate_cisco_commands(N, M, x2, dscp_values, x3):
    dscp_reverse_map = {
        0: 'default', 8: 'cs1', 10: 'af11', 12: 'af12', 14: 'af13', 16: 'cs2', 18: 'af21', 20: 'af22', 22: 'af23',
        24: 'cs3', 26: 'af31', 28: 'af32', 30: 'af33', 32: 'cs4', 34: 'af41', 36: 'af42', 38: 'af43', 40: 'cs5',
        44: 'va', 46: 'ef', 48: 'cs6', 56: 'cs7'
    }
    queue_dscp_map = {j: [] for j in range(N)}
    for i in range(M):
        for j in range(N):
            if x2[j, i] == 1:
                queue_dscp_map[j].append(dscp_values[i])
    bandwidths = x3.astype(float)[:N]
    bandwidths_kbps = bandwidths * 1000
    formatted_bandwidths = [int(round(bw)) for bw in bandwidths_kbps]
    commands = []
    for j in range(N):
        if formatted_bandwidths[j] > 0:
            class_name = f"q{j+1}"
            if queue_dscp_map[j]:
                commands.append(f"class-map match-any {class_name}")
                for dscp in set(queue_dscp_map[j]):
                    dscp_name = dscp_reverse_map.get(dscp, f"dscp {dscp}")
                    commands.append(f"match dscp {dscp_name}")
                commands.append(f"exit")
    commands.append(f"policy-map pyauto")
    for j in range(N):
        if formatted_bandwidths[j] > 0:
            class_name = f"q{j+1}"
            bw = max(1, int(formatted_bandwidths[j]))
            commands.append(f"class {class_name}")
            commands.append(f"bandwidth {bw}")
            commands.append(f"exit")
    commands.append(f"")
    commands += [
        "int f0/1",
        "service-policy output pyauto",
        "exit",
        "exit",
        "wr"
    ]
    return commands
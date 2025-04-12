import math
import heapq

# Graful este reprezentat printr-un dicționar unde fiecare nod are ca valoare alt dicționar
# ce conține vecinii și costul pentru arc.
graph = {
    1:  {2: 2, 3: 4},
    2:  {1: 2, 4: 6, 5: 3},
    3:  {1: 4, 6: 5},
    4:  {2: 6, 7: 4},
    5:  {2: 3, 8: 2, 12: 1},
    6:  {3: 5, 9: 3},
    7:  {4: 4, 10: 6},
    8:  {5: 2, 11: 3, 12: 2},
    9:  {6: 3, 13: 5},
    10: {7: 6, 14: 4},
    11: {8: 3, 15: 4},
    12: {5: 1, 8: 2, 16: 3},
    13: {9: 5, 17: 2},
    14: {10: 4, 18: 3},
    15: {11: 4, 19: 2},
    16: {12: 3, 20: 5},
    17: {13: 2, 21: 4},
    18: {14: 3, 22: 4},
    19: {15: 2, 23: 3},
    20: {16: 5, 24: 2},
    21: {17: 4},
    22: {18: 4},
    23: {19: 3},
    24: {20: 2}
}

# Pentru euristică folosim coordonate (x,y) pentru fiecare nod.
# Aceste coordonate sunt alese astfel încât să permită calculul unei distanțe aproximative față de nodurile scop.
coords = {
    1:  (0, 0),
    2:  (1, 2),
    3:  (2, 0),
    4:  (3, 2),
    5:  (1, 1),
    6:  (2, 3),
    7:  (4, 2),
    8:  (2, 2),
    9:  (3, 3),
    10: (5, 2),
    11: (3, 1),
    12: (2, 1),
    13: (2, 0.5),
    14: (4, 1),
    15: (3, 0),
    16: (1, 0),
    17: (0.5, 2),
    18: (4, 0),
    19: (5, 1),
    20: (1, -1),
    21: (0, 2),
    22: (4, 3),
    23: (5, 3),
    24: (1, -2)
}

def euclidean_distance(p1, p2):
    """Calculează distanța euclidiană între două puncte."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def heuristic(n, goals):
    """
    Pentru un nod n, euristica este minimul dintre distanțele euclidiene
    de la n la fiecare nod scop.
    """
    return min(euclidean_distance(coords[n], coords[goal]) for goal in goals)

def a_star_search(graph, start, goals, steps):
    """
    Implementarea A* cu simulare de pași:
      - graph: structura grafului
      - start: nodul de pornire
      - goals: listă de noduri scop
      - steps: numărul de pași de expansiune în A*

    La fiecare pas se înregistrează nodul selectat și valoarea sa f.
    Dacă se atinge un nod scop, căutarea se oprește.

    Returnează o listă de tuple (nod, f) pentru nodurile expandate,
    precum și un flag care indică dacă s-a atins un nod scop.
    """
    # Vom folosi o coadă de prioritate pentru open_list
    # Fiecare element este un tuple: (f, g, nod, cale)
    open_list = []
    # Inițializarea lui g: costul de la start până la fiecare nod
    g_scores = {node: float('inf') for node in graph}
    g_scores[start] = 0

    start_f = g_scores[start] + heuristic(start, goals)
    heapq.heappush(open_list, (start_f, 0, start, [start]))

    # Pentru a ține evidența nodurilor deja expandate
    closed_set = set()

    # Lista care stochează nodurile expandate, împreună cu valoarea lor f
    expanded_nodes = []

    current_step = 0

    while open_list and current_step < steps:
        # Extragem nodul cu f minim
        f, g_val, current, path = heapq.heappop(open_list)
        expanded_nodes.append((current, f))

        # Dacă am ajuns într-un nod scop, oprim căutarea
        if current in goals:
            return expanded_nodes, True

        closed_set.add(current)
        current_step += 1

        for neighbor, cost in graph[current].items():
            if neighbor in closed_set:
                continue
            tentative_g = g_val + cost
            # Dacă găsim un drum mai bun spre vecin:
            if tentative_g < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g
                f_neighbor = tentative_g + heuristic(neighbor, goals)
                heapq.heappush(open_list, (f_neighbor, tentative_g, neighbor, path + [neighbor]))
    return expanded_nodes, False

# Pentru completitudine se poate adăuga și o versiune a IDA*.
# Aceasta folosește recursivitatea și mărește treptat limita.
def ida_star_search(graph, start, goals, steps):
    """
    Implementare simplificată a algoritmului IDA*, cu oprire după un număr maxim de pași.
    Observație: IDA* se bazează pe backtracking recursiv și nu se aliniază
    la un „număr de pași” la fel ca A*. Aici folosim o limită de expansiuni.

    Returnează o listă a nodurilor expandate (în ordinea expansiunii împreună cu f)
    și un flag care indică dacă s-a atins un nod scop.
    """
    expanded_nodes = []
    num_expansions = 0

    def search(path, g, bound):
        nonlocal num_expansions
        current = path[-1]
        f = g + heuristic(current, goals)
        if f > bound:
            return f
        if current in goals:
            expanded_nodes.append((current, f))
            return current  # semnalăm că s-a atins nod scop
        expanded_nodes.append((current, f))
        num_expansions += 1
        if num_expansions >= steps:
            return None  # s-a atins limita de pași
        min_threshold = float('inf')
        for neighbor, cost in graph[current].items():
            if neighbor in path:  # evităm ciclurile
                continue
            result = search(path + [neighbor], g + cost, bound)
            if result == current or isinstance(result, int):
                return result
            if result is not None and result < min_threshold:
                min_threshold = result
        return min_threshold

    bound = heuristic(start, goals)
    while True:
        result = search([start], 0, bound)
        if isinstance(result, int):  # s-a găsit un nod scop
            return expanded_nodes, True
        if result == float('inf'):
            return expanded_nodes, False
        bound = result
        if num_expansions >= steps:
            break
    return expanded_nodes, False

# Blocul principal de rulare
if __name__ == '__main__':
    # Setări inițiale, de exemplu:
    start_node = 12
    goal_nodes = [1, 20]

    # Citim numărul de pași și tipul de algoritm de la utilizator
    try:
        n_steps = int(input("Introduceți numărul de pași: "))
    except ValueError:
        print("Introduceți un număr întreg pentru pași.")
        exit(1)

    algorithm = input("Algoritmul (A* sau IDA*): ").strip().lower()

    if algorithm == "a*":
        expansions, reached = a_star_search(graph, start_node, goal_nodes, n_steps)
    elif algorithm == "ida*":
        expansions, reached = ida_star_search(graph, start_node, goal_nodes, n_steps)
    else:
        print("Algoritm necunoscut. Utilizați 'A*' sau 'IDA*'.")
        exit(1)

    # Afișăm rezultatele:
    if reached:
        # Dacă s-a atins un nod scop, afișăm doar acel nod și valoarea f corespunzătoare
        node, f_val = expansions[-1]
        print(f"Scop atins: {node} (f = {f_val:.2f})")
    else:
        print("Nodurile expandate după", n_steps, "pași:")
        for node, f_val in expansions:
            print(f"{node}: {f_val:.2f}")

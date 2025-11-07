from collections import defaultdict
import networkx as nx
import numpy as np

# Lista susedstva kao string
adj_list_text = """
0:1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 17, 19, 21, 31
1:0, 2, 3, 7, 13, 17, 19, 21, 30
2:0, 1, 3, 7, 8, 9, 13, 27, 28, 32
3:0, 1, 2, 7, 12, 13
4:0, 6, 10
5:0, 6, 10, 16
6:0, 4, 5, 16
7:0, 1, 2, 3
8:0, 2, 30, 32, 33
9:2, 33
10:0, 4, 5
11:0
12:0, 3
13:0, 1, 2, 3, 33
14:32, 33
15:32, 33
16:5, 6
17:0, 1
18:32, 33
19:0, 1, 33
20:32, 33
21:0, 1
22:32, 33
23:25, 27, 29, 32, 33
24:25, 27, 31
25:23, 24, 31
26:29, 33
27:2, 23, 24, 33
28:2, 31, 33
29:23, 26, 32, 33
30:1, 8, 32, 33
31:0, 24, 25, 28, 32, 33
32:2, 8, 14, 15, 18, 20, 22, 23, 29, 30, 31, 33
33:8, 9, 13, 14, 15, 18, 19, 20, 22, 23, 26, 27, 28, 29, 30, 31, 32
"""

# Pretvaranje u dict
graph = defaultdict(list)
for line in adj_list_text.strip().split('\n'):
    node, neighbors = line.split(":")
    graph[int(node)] = list(map(int, neighbors.strip().split(',')))

# Kreiraj NetworkX graf
G = nx.Graph(graph)
v, t = 23, 19

# 1. Zbir stepena
stepen_v = len(graph[v])
stepen_t = len(graph[t])
zbir_stepena = stepen_v + stepen_t

# 2. Najkraci put
najkraci_put = nx.shortest_path(G, source=v, target=t)

# 3. Susedi v koji nisu susedi t
razlika_suseda = sorted(set(graph[v]) - set(graph[t]))

# 4. Susedi v ili t sa stepenom ispod proseka
prosek = sum(len(g) for g in graph.values()) / len(graph)
ispod_proseka = sorted([
    node for node in set(graph[v]) | set(graph[t])
    if len(graph[node]) < prosek
])

# 5. Broj grana u indukovanom podgrafu
indukovani_cvorovi = set(graph[v]) | set(graph[t]) | {v, t}
podgraf = G.subgraph(indukovani_cvorovi)
broj_grana = podgraf.number_of_edges()

# 6. cvorovi na udaljenosti do 2 od oba
def u_dva_koraka(node):
    prvi = set(graph[node])
    drugi = set()
    for sused in prvi:
        drugi.update(graph[sused])
    return prvi | drugi | {node}

dva_v = u_dva_koraka(v)
dva_t = u_dva_koraka(t)
zajednicki = sorted(dva_v & dva_t)

# 7. Zbir ekscentriciteta
zbir_eks = nx.eccentricity(G, v) + nx.eccentricity(G, t)

# 8. Broj komponenti nakon uklanjanja v, t i suseda
uklonjeni = {v, t} | set(graph[v]) | set(graph[t])
G_reduced = G.copy()
G_reduced.remove_nodes_from(uklonjeni)
broj_komponenti = nx.number_connected_components(G_reduced)

# 9. Broj putanja duzine 3 od v do t
def putanje_d3(g, start, end):
   count = 0
   def dfs(node, d, path):
       nonlocal count
       if d == 3:
           if node == end:
               count += 1
           return
       for neighbor in g[node]:
            if d < 3 or neighbor == end:
                dfs(neighbor, d+1, path + [neighbor])
            dfs(start, 0, [start])
            return count

putanja3 = putanje_d3(graph, v, t) #

# Pretpostavljamo da je G vec kreiran iz tvoje liste susedstva

v = 13
t = 16
duzina = 3
count = 0

for path in nx.all_simple_paths(G, source=v, target=t, cutoff=duzina):
    if len(path) - 1 == duzina:
        print("Put:", path)
        count += 1

print("Ukupno puteva duzine 3:", count)






# 10. Putanje duzine 10 od v do t (matrica susedstva)
A = nx.to_numpy_array(G, dtype=int)
putanja10 = int(np.linalg.matrix_power(A, 10)[v][t])

# Ispis svih rezultata
print("1. Zbir stepena v i t:", zbir_stepena)
print("2. Najkraci put od v do t:", '-'.join(map(str, najkraci_put)))
print("3. Susedi v koji nisu susedi t:", ','.join(map(str, razlika_suseda)) if razlika_suseda else "/")
print("4. Susedi v ili t sa stepenom < proseka:", ','.join(map(str, ispod_proseka)) if ispod_proseka else "/")
print("5. Broj grana u indukovanom podgrafu:", broj_grana)
print("6. cvorovi udaljeni do 2 od oba:", ','.join(map(str, zajednicki)) if zajednicki else "/")
print("7. Zbir ekscentriciteta v i t:", zbir_eks)
print("8. Komponenti nakon uklanjanja:", broj_komponenti)
#print("9. Broj putanja duzine 3 od v do t:", putanja3)
print("10. Broj putanja duzine 10 od v do t:", putanja10)
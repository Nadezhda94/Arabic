import codecs
import re
import networkx as nx
import pydot

grammar_file = "grammar.txt"
data = []
with codecs.open(grammar_file, "r", "utf-8") as f:
	for line in f:
		if len(line) > 0:
			stripped_line = line.strip("\r\n")
			if (len(stripped_line) > 0):
				splited_line = re.split("[0-9]+\.\s*|\s*->\s*|\s+", stripped_line)
				if len(splited_line) > 0:
					data.append(splited_line)

nka = nx.MultiDiGraph()
finish_num = 0
print data[0]
labels = set()
for rule in data:
    if (len(rule) != 3 ):
        print(type(rule[0]))
        """
        nka.add_node("FIN" + str(finish_num), style = "filled", fillcolor = "grey")
        nka.add_edge(rule[0], "FIN" + str(finish_num), key = rule[1], label = rule[1])
        """
        nka.add_node("FIN", style = "filled", fillcolor = "grey")
        nka.add_edge(rule[0], "FIN", key = rule[1], label = rule[1])
        finish_num += 1
    else:
        nka.add_edge(rule[0], rule[2], key = rule[1], label = rule[1])
    labels.add(rule[1])


queue = []

dka = nx.MultiDiGraph()
start_node = "S"
queue.append((set([start_node]), 0))
node_num = 1


nodes = {}

def get_node(nodes_list):
    for key in nodes.keys():
        if (nodes_list == nodes[key]):
            return key
    return None

i = 0
start = 0
final_nodes = set()
while (len(queue) > 0):
    print("step: ")
    print(i)
    
    start_nodes = queue.pop()
    start = start_nodes[1]
    start_nodes = start_nodes[0]
    print start_nodes
    keys = {}
    for node in start_nodes:
     
        for edge in nka.edges(node, keys = True):
            if (keys.get(edge[-1]) == None):
                keys[edge[-1]] = set([edge[1]])
            else:
                keys[edge[-1]].add(edge[1])
    print "keys: ", keys
    for key in keys.keys():
        end_node = get_node(keys[key])
        if (end_node == None):
            nodes[node_num] = set(keys[key])
            end_node = node_num
            queue.append((keys[key], node_num))
            node_num += 1
        if "FIN" in keys[key]:
            final_nodes.add(int(end_node))
            dka.add_node(end_node, style = "filled", fillcolor = "grey")
        print "edge: ", start, end_node,key
        dka.add_edge(start, end_node, label = key, key = key)
    i += 1

print final_nodes
print "labels: ", labels

def get_keys_nodes(predecessors):
    keys = {}
    for edge in predecessors:
        if (keys.get(edge[-1]) == None):
            keys[edge[-1]] = set([edge[1]])
        else:
            keys[edge[-1]].add(edge[1])
    return keys

A = nx.to_pydot(dka)
A.write_png("grDKA.png")

n = node_num
"""
dka.add_node(n, style = "filled", fillcolor = "red")
for i in range(n + 1):
    for label in labels:
    
        first_predecessors = dka.edges(i, keys = True)
        first_keys = dict(get_keys_nodes(first_predecessors))
        if first_keys.get(label) == None:
            dka.add_edge(i, n, label = label, key = label)
"""
            



reverse_dka = dka.reverse()




def build_table():
    queue = []
    marked = [[False for i in range(n + 1)] for j in range(n + 1)]
    print "first_marked"
    for i in range(n + 1):
        for j in range(n + 1):
            if not marked[i][j] and (i in final_nodes) != (j in final_nodes):
                #print i, j
                marked[i][j] = True
                marked[j][i] = True
                queue.append((i, j))
    print "end_marked"

    while (len(queue) > 0):
        top_pair = queue.pop()
        print "pair: ", top_pair
        first_predecessors = reverse_dka.edges(top_pair[0], keys = True)
        second_predecessors = reverse_dka.edges(top_pair[1], keys = True)
        first_keys = dict(get_keys_nodes(first_predecessors))
        print "first_keys: ", first_predecessors, first_keys

        second_keys = dict(get_keys_nodes(second_predecessors))
        print "second_keys: ", second_keys
        for label in labels:
            label_pred_first = first_keys.get(label)
            label_pred_second = second_keys.get(label)
            if label_pred_first != None and label_pred_second != None:
                for i in label_pred_first:
                    for j in label_pred_second:
                        if not marked[i][j]:
                            marked[i][j] = True
                            marked[j][i] = True
                            queue.append((i, j))
    return marked

        

def minimize_dka():
    marked = build_table()
    with codecs.open("marked.txt", "w", "utf-8") as f:
        res = ""
        for row in marked:
            for col in row:
                res += str(col) + "  "
            res += "\n"
        f.write(res)
    print marked
    components_count = 0
    components = [-1 for i in range(n + 1)]
    for i in range(n + 1):
        if (not marked[n][i]):
            components[i] = 0
            print i
    for i in range(0, n):
        
        if (components[i] == -1):
            print "row: ", i
            components_count += 1
            components[i] = components_count
            
            for j in range(i + 1, n):
                if (not marked[i][j]):
                    print "col ", j
                    components[j] = components_count
    print "components_count: ", components_count

    for i in range(n):
        print i, components[i] 

  

#minimize_dka()

"""
nka.add_edge("S", "NOUN", label = "cp")
nka.add_edge("S", "NOUN", label = "cn")
nka.add_edge("S", "NOUN", label = "v")
"""


def draw_pydot(nka):
    B = nx.to_pydot(nka)
    B.write_png("gr.png")
draw_pydot(nka)

print("Nodes of graph: ")
print(dka.nodes())
print("Edges of graph: ")
print(len(dka.edges()))
print ("from final nodes: ")
a = set()
for node in final_nodes:
    a.update(reverse_dka.out_edges(node))
print len(a)
print "unique_edges: ", len(labels)
print labels

"""
pos = nx.spring_layout(nka)
nx.write_dot(nka,'nka.png')
"""
"""
nx.draw_networkx_nodes(nka, pos)
nx.draw_networkx_edges(nka, pos)

nx.draw_networkx_labels(nka, pos, font_size=20, font_family='sans-serif')
nx.draw_networkx_edge_labels(nka, pos, 
    {
        ("S", "NOUN"):"cp", ("S", "NOUN"):"cn"
   	},
    label_pos=0.3
)
"""

#plt.savefig("nka.png")


"""
cities = {0:"Toronto",1:"London",2:"Berlin",3:"New York"}

H=nx.relabel_nodes(G,cities)
 
print("Nodes of graph: ")
print(H.nodes())
print("Edges of graph: ")
print(H.edges())
pos=nx.spring_layout(H)
nx.draw_networkx_nodes(H, pos)
nx.draw_networkx_edges(H,pos)
nx.draw_networkx_labels(H,pos,font_size=20,font_family='sans-serif')
nx.draw_networkx_edge_labels(G,pos, 
    {
        ("Toronto"
        	,"London"):"x", ("London","Berlin"):"y", ("Berlin","New York"):"w"
    },
    label_pos=0.3
)
plt.savefig("path_graph_cities1.png")
"""


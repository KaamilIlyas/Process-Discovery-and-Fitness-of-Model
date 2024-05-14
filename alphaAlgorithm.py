import pandas as pd
from graphviz import Digraph
import networkx as nx
import matplotlib.pyplot as plt

#Part A

#STEP 1

#reading the file using pd.read_csv
event_log = pd.read_csv('E:/Procmin/AnonymizedEventData.csv')

#grouping events in the event_log dataFrame based on 'TicketNum' column and then 
#for each group extracting the 'Status' column and converting it into a list of events
traces = event_log.groupby('TicketNum')['Status'].apply(list).tolist()
L = [tuple(trace) for trace in traces]  #takes a list of traces and convert each trace into a tuple
print("Multi-set of traces (L):")
print(L)

print ("-------------------------------------------")
print ("-------------------------------------------")
print ("-------------------------------------------")

#STEP 2

#contains all the unique statuses extracted from the list of traces L
TL = set(status for trace in L for status in trace)
print("Set TL:")
print(TL)

print ("-------------------------------------------")
print ("-------------------------------------------")
print ("-------------------------------------------")

#STEP 3

#iterating each trace in L and retrieving the first element using trace[0]
start_events = [trace[0] for trace in L]
end_events = [trace[-1] for trace in L] 

#set is used to remove duplicates, max function is used to find elements that occur most frequently
TI = max(set(start_events), key=start_events.count)
TO = max(set(end_events), key=end_events.count)

print("Start event (TI):", TI)
print("End event (TO):", TO)

print ("-------------------------------------------")
print ("-------------------------------------------")
print ("-------------------------------------------")

#STEP 4

PL = set()  #initialized empty set
for trace in L:
    for i in range(1, len(trace)):   #iterates over all pairs of consecutive events
        predecessor = (trace[i-1], trace[i])   #trace[i-1] represent predecessor event & trace[i] successor event
        PL.add(predecessor)   #adding predecessor tuple to the set

print("Set PL:")
for predecessor in PL:
    print(predecessor)

print ("-------------------------------------------")
print ("-------------------------------------------")
print ("-------------------------------------------")

#STEP 5

FL = set()
for trace in L:
    for i in range(len(trace) - 1):  #expression is used to ensure that we do not go out of bounds 
        follow = (trace[i], trace[i+1])
        FL.add(follow)

print("Set FL:")
for follow in FL:
    print(follow)

print ("-------------------------------------------")
print ("-------------------------------------------")
print ("-------------------------------------------")

#STEP 6

resultant_process = Digraph()
resultant_process.attr(rankdir='LR')
resultant_process.attr('node', shape='rectangle')
resultant_process.node(TI)
for relation in PL:
   resultant_process.edge(relation[0], relation[1])
resultant_process.node(TO)

print("Resultant Process:")
print(resultant_process.source)

print ("-------------------------------------------")
print ("-------------------------------------------")
print ("-------------------------------------------")

process = {
    'L': trace,
    'TL': TL,
    'TI': TI,
    'TO': TO,
    'PL': PL,
    'FL': FL
}
#print("\nResultant process:")
#print(process)


#visualizing process

resultant_process = nx.DiGraph()
resultant_process.add_edges_from(FL)

plt.figure(figsize=(8, 6))
pos = nx.spring_layout(resultant_process)
nx.draw(resultant_process, pos, with_labels=True, node_color='lightblue', edge_color='gray', arrows=True)
plt.title("Resultant Process")
plt.savefig("resultant_process.png")
plt.show()


#PART B

fitness_results = []

for trace in L:
    current_node = trace[0]
    executed_trace = [current_node]

    for event in trace[1:]:
        if (current_node, event) in FL:
            current_node = event
            executed_trace.append(current_node)

    if executed_trace == list(trace):
        fitness_results.append((trace, True))  #trace successfully executed on the process
    else:
        fitness_results.append((trace, False))  #trace did not be executed on the process


print("Fitness Results:")
for trace, is_executable in fitness_results:
    print(f"Trace: {trace}, Executable: {is_executable}")



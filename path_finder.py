#start_node - stores starting point
#goal_node - stores destination point
#type_of_algorithm - A*, UCS, BFS, DFS
#traffic_lines_number - Specifies the number of Intersections
#sunday_traffic_lines_number - Specifies the number of Sunday Intersections
#path - A dictionary to store parent node of a node. Required for traversing the root from start state to goal state
#visited - A dictionary that contains all visited nodes
#Queue, Stack, Priority Queue - Data Structures as required for the algorithm

import Queue
import sys
def defineSundayTraffic(sunday_traffic_intersection, sunday_traffic_travel_time):
    if sunday_traffic_intersection not in sunday_traffic_information:
        sunday_traffic_information[sunday_traffic_intersection] = sunday_traffic_travel_time
    return sunday_traffic_information

def readInputFile():
    input_file = open("C:\PyCharm Python programs\N.txt", "r")
    line_number = 0

    for each_line in input_file:
        if line_number < 4:
            if line_number == 0:
                type_of_algorithm = str(each_line.rstrip('\n'))
                type_of_algorithm = type_of_algorithm.upper()
                #print type_of_algorithm
                #print type_of_algorithm
            elif line_number == 1:
                start_node = each_line.rstrip('\n')
                #print start_node
            elif line_number == 2:
                goal_node = each_line.rstrip('\n')
                #print goal_node
            else:
                traffic_lines_number = int(each_line.rstrip('\n'))
                #traffic_lines_number
            line_number += 1
        elif line_number >= 4 and line_number < (4 + traffic_lines_number):
            current_line = each_line.rstrip('\n').split(' ')
            parent_node = current_line[0]
            child_node = current_line[1]
            travel_time = int(current_line[2])
            #print parent_node, child_node, travel_time
            graph, graph_travel_time = createFinalGraph(parent_node, child_node, travel_time)
            line_number += 1
        else:
            #print temporary_graph
            if line_number == (4 + traffic_lines_number):
                sunday_traffic_lines_number = int(each_line.rstrip('\n'))
                #print sunday_traffic_lines_number
            else:

                sunday_traffic = each_line.rstrip('\n').split(' ')
                sunday_traffic_intersection = sunday_traffic[0]
                sunday_traffic_travel_time = int(sunday_traffic[1])
                #temporary_sunday_traffic_intersection.append(sunday_traffic_intersection)
                sunday_traffic_information = defineSundayTraffic(sunday_traffic_intersection, sunday_traffic_travel_time)
                #print sunday_traffic
            line_number += 1

    return start_node, goal_node, type_of_algorithm

def createFinalGraph(parent_node, child_node, travel_time):
    if parent_node not in graph:
        graph[parent_node] = []
        graph_travel_time[parent_node] = []
    if child_node not in graph:
        graph[child_node] = []
        graph_travel_time[child_node] = []
    if child_node not in graph[parent_node]:
        graph[parent_node].append(child_node)
        graph_travel_time[parent_node].append(travel_time)

    return graph, graph_travel_time

def breadthFirstSearch(graph, start_node, goal_node):
    visited = {}
    queue = [start_node]
    path = {}
    path[start_node] = start_node
    while queue:
        #print queue
        node = queue.pop(0)
        #print node
        if node not in visited:
            visited[node] = []
        visited[node] = 1
        for child_node in graph[node]:
            # print child_node
            if child_node not in visited:
                if not path.has_key(child_node):  # child_node not in path:
                    # path[child_node] = []
                    path[child_node] = node
                if child_node == goal_node:
                    return node, path
                if child_node not in queue:
                    queue.append(child_node)
                    # print "Queue ", queue

def depthFirstSearch(graph, start_node, goal_node):
    #print "DFS"
    visited = dict()
    visited[start_node] = True
    path = dict()
    path[start_node] = start_node
    stack = [start_node]
    i = 0
    while stack:
        current_node = stack.pop(0)
        #print current_node
        visited[current_node] = True
        if current_node == goal_node:
            return current_node, path
        i += 1
        for child_node in reversed(graph[current_node]):
            if child_node not in visited and child_node not in stack:
                path[child_node] = current_node
                stack.insert(0, child_node)

def uniformCostSearch(graph, start_node, goal_node):
    count = 0
    priority_queue = Queue.PriorityQueue()
    open_list = dict()
    closed_list = dict()
    priority_queue.put((0, count, start_node))
    temporary_priority_queue = Queue.PriorityQueue()
    open_list[start_node] = 0
    path = dict()
    path[start_node] = start_node
    while priority_queue:
        #print priority_queue.queue
        cummulative_travel_time_till_that_node, dummy, current_node = priority_queue.get()
        print current_node
        if current_node == goal_node:
            return current_node, path
        index = 0
        for child_node in graph[current_node]:
            count += 1
            total_travel_time = cummulative_travel_time_till_that_node + graph_travel_time[current_node][index]
            index += 1
            if child_node not in open_list and child_node not in closed_list:
                open_list[child_node] = total_travel_time
                priority_queue.put((total_travel_time, count, child_node))
                path[child_node] = current_node
            elif child_node in open_list:
                c = open_list[child_node]
                if total_travel_time < c:
                    open_list[child_node] = total_travel_time
                    for i in range(0, priority_queue.qsize()):
                        cost, dummy, node = priority_queue.get()
                        #print cost, node
                        if node != child_node:
                            temporary_priority_queue.put((cost, dummy, node))
                        else:
                            temporary_priority_queue.put((total_travel_time, count, node))
                            path[child_node] = current_node
                    priority_queue = temporary_priority_queue
                    temporary_priority_queue = Queue.PriorityQueue()
            elif child_node in closed_list:
                c = closed_list[child_node]
                if total_travel_time < c:
                    priority_queue.put((total_travel_time, count, child_node))
                    del closed_list[child_node]
                    for i in range(0, priority_queue.qsize()):
                        cost, dummy, node = priority_queue.get()
                        if node != child_node:
                            temporary_priority_queue.put((cost, dummy, node))
                        else:
                            temporary_priority_queue.put((total_travel_time, count, node))
                            path[child_node] = current_node
                    priority_queue = temporary_priority_queue
                    temporary_priority_queue = Queue.PriorityQueue()

        closed_list[current_node] = cummulative_travel_time_till_that_node
        if open_list.has_key(current_node):
            #print "here"
            del open_list[current_node]

def printPathBFSAndDFS(parent_of_goal_node, path):
    #print path
    path_from_parent_to_child = [goal_node];  # To store the path from start to goal
    while True:
        if parent_of_goal_node == start_node:
            break
        for nodes in path.keys():
            if nodes == parent_of_goal_node:
                if nodes != goal_node:
                    path_from_parent_to_child.insert(0, parent_of_goal_node)  # Since it iterates from bottom to top; Therefore insert nodes at the start
                parent_of_goal_node = path[nodes]
    path_from_parent_to_child.insert(0, start_node)
    count = 0
    result = ""
    result += ''.join(str(start_node) + " %d" % count + "\n")
    count += 1
    for r in path_from_parent_to_child:
        if r != start_node:
            result += ''.join(str(r) + " %d" % count + "\n")
            count += 1

    return result

def printPathUCSAndAStar(parent_of_goal_node, path):
    path_from_parent_to_child = [];  # To store the path from start to goal
    while True:
        if parent_of_goal_node == start_node:
            break
        for nodes in path.keys():
            if nodes == parent_of_goal_node:
                path_from_parent_to_child.insert(0, parent_of_goal_node)  # Since it iterates from bottom to top; Therefore insert nodes at the start
                parent_of_goal_node = path[nodes]

    path_from_parent_to_child.insert(0, start_node)
    count = 0
    result = ""
    result += ''.join(str(start_node) + " %d" % count + "\n")
    for r in path_from_parent_to_child:
        if r == start_node:
            parent_node = r

        else:
            for child_node in graph[parent_node]:
                if child_node == r:

                    index = graph[parent_node].index(child_node)
                    count += graph_travel_time[parent_node][index]
                    parent_node = child_node
        if r != start_node:
            result += ''.join(str(r) + " %d" % count + "\n")
    return result

def AStarSearch(graph, start_node, goal_node):
    priority_queue = Queue.PriorityQueue()
    count = 0
    open_list = dict()
    closed_list = dict()
    temporary_priority_queue = Queue.PriorityQueue()
    priority_queue.put((sunday_traffic_information[start_node],count, start_node))
    open_list[start_node] = sunday_traffic_information[start_node]
    path = dict()
    path[start_node] = start_node
    while priority_queue:
        cummulative_travel_time_till_that_node, dummy, current_node = priority_queue.get()
        #print current_node
        if current_node == goal_node:
            #print open_list, closed_list

            return current_node, path
        index = 0
        for child_node in graph[current_node]:
            count += 1
            #print open_list
            #print priority_queue.queue
            total_travel_time = cummulative_travel_time_till_that_node + graph_travel_time[current_node][index] + sunday_traffic_information[child_node] - sunday_traffic_information[current_node]
            #print total_travel_time, child_node
            index += 1
            if child_node not in open_list and child_node not in closed_list:
                open_list[child_node] = total_travel_time
                priority_queue.put((total_travel_time, count, child_node))
                #print priority_queue.queue
                path[child_node] = current_node

            elif child_node in open_list:
                #print "Hey"
                c = open_list[child_node]
                if total_travel_time < c:
                    #print total_travel_time, c, child_node, open_list[child_node]
                    open_list[child_node] = total_travel_time
                    #print open_list[child_node]
                    success = 0
                    for i in range(0, priority_queue.qsize()):
                        cost, dummy, node = priority_queue.get()
                        #print cost, node
                        if node != child_node:
                            temporary_priority_queue.put((cost, dummy, node))
                        else:
                            success = 1
                            temporary_priority_queue.put((total_travel_time, count, node))
                            path[child_node] = current_node

                    priority_queue = temporary_priority_queue
                    temporary_priority_queue = Queue.PriorityQueue()
            elif child_node in closed_list:
                c = closed_list[child_node]
                if total_travel_time < c:
                    priority_queue.put((total_travel_time, count, child_node))
                    open_list[child_node] = total_travel_time
                    del closed_list[child_node]
                    #print  priority_queue.queue
                    for i in range(0, priority_queue.qsize()):
                        cost, dummy, node = priority_queue.get()
                        #print cost, node
                        if node != child_node:
                            temporary_priority_queue.put((cost, dummy, node))
                        else:
                            temporary_priority_queue.put((total_travel_time, count, node))
                            path[child_node] = current_node
                    priority_queue = temporary_priority_queue
                    temporary_priority_queue = Queue.PriorityQueue()
        closed_list[current_node] = cummulative_travel_time_till_that_node
        if open_list.has_key(current_node):
            #print "here"
            del open_list[current_node]

graph_travel_time = dict()
sunday_traffic_information = dict()
graph = dict()
temporary_graph = dict()
temporary_sunday_traffic_intersection = []
start_node, goal_node, type_of_algorithm = readInputFile()
#print sunday_traffic_information
#print temporary_graph
#print graph
if start_node == goal_node:
    result = ""
    result += ''.join(start_node + " %d" % 0)

    #print result
else:
    if type_of_algorithm == 'BFS':

        parent_of_goal_node, path = breadthFirstSearch(graph, start_node, goal_node)
        #print path
        result = printPathBFSAndDFS(parent_of_goal_node, path)

    elif type_of_algorithm == 'DFS':

        parent_of_goal_node, path = depthFirstSearch(graph, start_node, goal_node)
        result = printPathBFSAndDFS(parent_of_goal_node, path)


    elif type_of_algorithm == 'UCS':

        parent_of_goal_node, path = uniformCostSearch(graph, start_node, goal_node)
        result = printPathUCSAndAStar(parent_of_goal_node, path)



    else:

        parent_of_goal_node, path = AStarSearch(graph, start_node, goal_node)
        result = printPathUCSAndAStar(parent_of_goal_node, path)


        #print parent_of_goal_node, path
output_file = open("C:\PyCharm Python programs\Noutput.txt", "w+")
    # sys.stdout = output_file
    #output_file.seek(0)
output_file.write(result)
    #print result
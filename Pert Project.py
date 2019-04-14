import logging

class Activity:
    "It's an activity doing what activities do, activate."

    @property
    def logger(self):
        name = '.'.join([__name__, self.__class__.__name__])
        return logging.getLogger(name)

    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.logger.debug('Activity initialized')

    def __str__(self):
        self.logger.debug('Activity str method activated')
        return str(self.name) + ", Duration: " + str(self.duration)


class Project:

    @property
    def logger(self):
        name = '.'.join([__name__, self.__class__.__name__])
        return logging.getLogger(name)

    def __init__(self, project_dict=None):
        """ initializes a graph object
            If no dictionary or None is given, an empty dictionary will be used
        """
        if project_dict == None:
            self.__project_dict = {}
            self.logger.debug('Project without dict initialized')
        else:
            self.__project_dict = project_dict
            self.logger.debug('Project initialized with dict initialized')

    def __generate_edges(self):
        """ A static method generating the edges of the
            graph "graph". Edges are represented as sets
            with one (a loop back to the vertex) or two
            vertices
        """
        edges = []
        for vertex in self.__project_dict:
            for neighbour in self.__project_dict[vertex]:
                if {neighbour.name, vertex.name} not in edges:
                    edges.append({vertex.name, neighbour.name})
        self.logger.debug('Edges generated')
        return edges

    def __str__(self):
        res = "Activities: "
        for k in self.__project_dict:
            res += str(k) + " "
        res += "\nEdges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        self.logger.debug('Project str method activated')
        return res

    def add_activity(self, Activity):
        """ add activity from the project """
        self.__project_dict[Activity] = []
        self.logger.debug('Project add activity method activated')

    def remove_activity(self, Activity):
        """ remove activity from the project """
        for a in self.__project_dict:
            if Activity in self.__project_dict[a]:
                self.__project_dict[a].remove(Activity)
        if Activity in self.__project_dict:
            del self.__project_dict[Activity]
        self.logger.debug('Project remove activity method activated')

    def vertices(self):
        """ returns the vertices of a graph """
        self.logger.debug('Project vertices method activated')
        return list(self.__project_dict.keys())

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list;
            between two vertices can be multiple edges!
        """
        edge = set(edge)
        vertex1 = edge.pop()
        if edge:
            # not a loop
            vertex2 = edge.pop()
        else:
            # a loop
            vertex2 = vertex1
        if vertex1 in self.__project_dict:
            self.__project_dict[vertex1].append(vertex2)
        else:
            self.__project_dict[vertex1] = [vertex2]
        self.logger.debug('Project add edge method activated')

    def cycle_exists(self):
        """Scaning for cyclic activities in the project"""
        project = self.__project_dict
        color = {u: "white" for u in project}  # - All nodes are initially white
        found_cycle = [False]  # - Define found_cycle as a list so we can change
        # its value per reference, see:
        # http://stackoverflow.com/questions/11222440/python-variable-reference-assignment
        for u in project:  # - Visit all nodes.
            if color[u] == "white":
                self.dfs_visit(u, color, found_cycle)
            if found_cycle[0]:
                break
        return found_cycle[0]

    def dfs_visit(self, u, color, found_cycle):
        project = self.__project_dict
        if found_cycle[0]:  # - Stop dfs if cycle is found.
            return
        color[u] = "gray"  # - Gray nodes are in the current path
        for v in project[u]:  # - Check neighbors, where G[u] is the adjacency list of u.
            if color[v] == "gray":  # - Case where a loop in the current path is present.
                found_cycle[0] = True
                return
            if color[v] == "white":  # - Call dfs_visit recursively.
                self.dfs_visit(v, color, found_cycle)
        color[u] = "black"

    def find_isolated_vertices(self):
        """returns a list of isolated vertices."""
        project = self.__project_dict
        isolated = []
        for vertex in project:
            if not project[vertex]:
                isolated.append(vertex)
        self.logger.debug('Project find isoalted vertices method activated')
        return isolated

    def print_isolated_vertices(self):
        """ printing isolated activities """

        isolated = self.find_isolated_vertices()
        for i in isolated:
            print(i.name)
        self.logger.debug('Project print isolated vertices method activated')

    def find_all_paths(self, start_vertex, end_vertex, path=[]):
        """ find all paths from start_vertex to end_vertex in project """
        graph = self.__project_dict
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return [path]
        if start_vertex not in graph:
            return []
        paths = []
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_paths = self.find_all_paths(vertex,
                                                     end_vertex,
                                                     path)
                for p in extended_paths:
                    paths.append(p)
        self.logger.debug('Project find all paths method activated')
        return paths

    def print_all_paths(self, start_vertex, end_vertex):
        """ printing all the activity path """
        tempList = self.find_all_paths(start_vertex, end_vertex)
        for i in tempList:
            for b in i:
                print(b.name + " ", end='')
            print("\n")
        self.logger.debug('Project print all paths method activated')

    def print_critical_path(self, start_Vertex, end_vertex):
        """ printing the critical path """
        resList = []
        tempList = project.find_all_paths(start_Vertex, end_vertex)
        for i in tempList:
            res = 0
            for b in i:
                # print(b.name + " ", end='')
                res += b.duration
            # print(res)
            # print("\n")
            resList.append(res)

        project.duration = max(resList)
        for b in tempList[resList.index(max(resList))]:
            print(b.name + " ", end='')
        print("\n")
        for b in tempList[resList.index(max(resList))]:
            print(b)
        print("Critical path duration: " + str(max(resList)))

        self.logger.debug('Project print critical path method activated')

    def print_slack_time(self, start_vertex, end_vertex):
        """ printing the slack time """
        resList = []
        tempList = project.find_all_paths(start_vertex, end_vertex)
        for i in tempList:
            res = 0
            for b in i:
                # print(b.name + " ", end='')
                res += b.duration
            print(res)
            # print("\n")
            resList.append(res)

        slackTimeList = []

        for i in resList:
            slackTimeList.append(max(resList) - i)

        slackTimeList.remove(0)
        slackTimeList.sort()
        slackTimeList.reverse()
        print(slackTimeList)

        self.logger.debug('Project print slack time method activated')


if __name__ == "__main__":
    # Configuring logger
    logging.basicConfig(level=logging.DEBUG,
                        filename='logger.log', filemode='w',
                        format='%(name)s %(levelname)s %(message)s')

    a = Activity("A", 5)
    b = Activity("B", 3)
    c = Activity("C", 4)
    d = Activity("D", 2)
    e = Activity("E", 6)
    f = Activity("F", 8)

    g = {a: [d, b],
         b: [c],
         c: [b, c, d, e],
         d: [a, c],
         e: [c],
         f: []
         }

    # Initialize project
    project = Project(g)
    print(project)

    print("\nAdd activity K:")
    k = Activity("K", 40)
    project.add_activity(k)
    print(project)

    print("\nRemoving activity K:")
    project.remove_activity(k)
    print(project)

    print("\nReveals a cyclic activities in the project: ")
    print(project.cycle_exists())

    print("\nIsolated activities in project: ")
    project.print_isolated_vertices()

    print("\nAll paths for listed vertices:")
    project.print_all_paths(a, e)

    print("\nCritical path:")
    project.print_critical_path(a, e)

    print("\nPrinting Slack time of the activities:")
    project.print_slack_time(a, e)

    print("\n")
    print(project)

# This is the FindCyclicReferences

from MapReduce import MapReduce
from collections import defaultdict



class FindCyclicReferences(MapReduce):
    def Map(self, parts):
        papers = {}
        edges = [tuple(part) for part in parts]
        
        for edge in edges:
            if int(edge[0]) > int(edge[1]):
                edge = (int(edge[1]), int(edge[0]))

                if edge in papers.keys():
                    papers[edge] += 1
                else:
                    papers[edge] = 1
            else:
                edge = (int(edge[0]), int(edge[1]))
                if edge in papers.keys():
                    papers[edge] += 1
                else:
                    papers[edge] = 1
            papers1 = {str(key):val for key, val in papers.items()}

        return papers1

    def Reduce(self, presults):
        p = defaultdict(int)
        for papers in presults:
            for key, val in papers.items():
                p[key] += val
                
        final_papers = {key:1 for key, val in p.items() if val >= 2}
                
        return final_papers


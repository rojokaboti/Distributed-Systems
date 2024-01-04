# This the FindCitations file

from MapReduce import MapReduce


class FindCitations(MapReduce):
    def Map(self, parts):
        papers = {}
        for edge in parts:
            papers[str(edge[1])] = 0


        for paper in papers.keys():
            citations = 0
            citers = [i[1] for i in parts if i[1] == paper]
            citations = len(citers)
            papers[paper] = citations

        papers = {key:val for key, val in papers.items() if val != 0}

        return papers

    def Reduce(self, presults):
        final_papers = {}
        for papers in presults:
            for key,value in papers.items():
                if key not in final_papers.keys():
                    final_papers[key] = value
                else:
                    final_papers[key] += value
        return final_papers



        

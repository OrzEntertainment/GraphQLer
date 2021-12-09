"""
TODO: Sequence generation
James
"""


from typing import List

from utils.requester import render_seq


class Orchestrator:
    

    # constructor
    def __init__(self, graph=None, maxLen=None, bugSequences=None):
        self.graph = graph
        self.maxLen = maxLen
        self.bugSequences = []
    # main orchestrate function
    def orchestrate(self) -> List[request]:
        for node in self.graph.nodes():
            if self.graph.out_degrees(node) == 0:
                dfs(self, [], node, self.maxLen)
        """
        TODO: main method to run
        """

    def dfs(self, sequence, node, n) -> None:
        if(len(sequence) > n):
            return
        
        [validSeq, bugSeq] = render_seq(sequence)

        for bSeq in bugSeq:
            self.bugSequences.append(bSeq)

        for seq in validSeq:
            for node in self.graph:
                if self.graph.out_degree(node) == 0:
                    deletedEdges = self.graph.in_edges(nbunch=node)
                    seq.append(node)
                    self.graph.remove(node)
                    self.dfs(self, seq, node)
                    seq.remove(node)
                    self.graph.add_edges_from(deletedEdges)
        
        
        

    

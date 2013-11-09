# -*- coding: utf-8 -*-
'''
 Copyright (C) 2013 onwards University of Deusto
  
 All rights reserved.
 
 This software is licensed as described in the file COPYING, which
 you should have received as part of this distribution.
 
 This software consists of contributions made by many individuals, 
 listed below:
 
 @author: Aitor Gómez Goiri <aitor.gomez@deusto.es>
'''

from optparse import OptionParser
from rdflib import Graph
import networkx as nx
import matplotlib.pyplot as plt
from actuation.utils.skolemize import skolemize_lemmas
from actuation.proofs.parser import LemmasParser


class PlanFactory(object):
    """
    This class is a factory for Plan.
        
    In some way, it can be seen as an entry point to the whole proofs module
    because it encapsulates all the needed substeps to generate a _graph.
    """
    
    def __init__(self, output_folder, reasoner):
        self.output_folder = output_folder
        self.reasoner = reasoner
    
    def _create_plan(self, query_goal_path, rule_paths):
        output_file_path = self.reasoner.query_proofs( rule_paths,
                                                 query_goal_path,
                                                 self.output_folder + "plan.n3" ) # Write the plan into a file
        return output_file_path
    
    def create(self, query_goal_path, all_knowledge):
        """
        This method creates a _graph with the steps needed to achieve a goal.
        """
        plan_filepath = self._create_plan( query_goal_path, all_knowledge )
        skolemized_plan_filepath = self.output_folder + "partially_skolemized_plan.n3"
        skolemize_lemmas( plan_filepath, skolemized_plan_filepath)
        
        rdf_graph = Graph()
        rdf_graph.parse(skolemized_plan_filepath, format="n3")
        parser = LemmasParser(rdf_graph)
        lemmas = parser.parse()
        
        #lemma_graph.to_image( output_file = self.output_folder + "lemma_precedences.png" )
        #lemma_graph.to_gml( output_file = self.output_folder + "lemma_precedences.gml" )
        return Plan( lemmas )


# TODO rethink/reorder URI or str, when and where?
# To be used with "lemma_precedences.txt"
class Plan(object): # rename to "Plan"
    
    def __init__(self, lemmas_info):
        """
        @param lemma_info
            A 'Lemmas' object with the summary of a result file's content.
        """
        self._lemmas_info = lemmas_info
        self._graph = self._create_nx_graph() 
    
    def _is_repeated(self, added_children_uris, new_child_node_info):
        for added_child_uri in added_children_uris:
            added_child_info = self._lemmas_info.get_lemma( str(added_child_uri) ) # It exists, otherwise wouldn't be in added_children_uris
            if new_child_node_info.equivalent_rest_calls( added_child_info ):
                return True
        return False
    
    def _should_be_filtered(self, added_children, child_node):
        # avoid adding lemmas which are not REST calls
        # avoid adding 2 children lemmas who have the same REST calls
        if self._lemmas_info is not None:
            
            child_node_info = self._lemmas_info.get_lemma( child_node )
            if child_node_info is None:
                raise Exception("ERROR. Lemma %s appears in the precedence graph but its information has not been parsed: %s." % (child_node, self._lemmas_info) )
            
            if child_node_info.is_rest_call():
                return self._is_repeated( added_children, child_node_info )
        return False
    
    def _create_nx_graph(self):
        """Adds a Lemmas object with the summary of a result file's content."""
        #_graph = nx.Graph()
        graph = nx.DiGraph()
        for name, lemma in self._lemmas_info.get_parent_lemmas():
            added_children = []
            for child_n in lemma.evidence_lemmas:
                child_node = str(child_n)
                if not self._should_be_filtered( added_children, child_node ):
                    added_children.append( child_node )
                    
                    graph.add_node( name ) # it's OK if it exists from the previous iteration
                    graph.add_node( child_node )
                    # lemma1 because lemma2, means that lemma2 -> lemma1
                    graph.add_edge( child_node, name )
        
        self._append_source_and_target( graph )
        return graph
    
    def _append_source_and_target(self, graph):
        """ It creates a starting point and an ending point and links them with leaves."""
        graph.add_node( "source" )
        graph.add_node( "target" )
        
        for leave in (n for n,d in graph.out_degree_iter() if d==0):
            if leave is not "source" and leave is not "target":
                graph.add_edge( leave, "target" )
            
        for root in (n for n,d in graph.in_degree_iter() if d==0):
            if root is not "source" and root is not "target":  
                graph.add_edge( "source", root )
    
    def to_gml(self, output_file):
        # from http://networkx.github.io/documentation/latest/examples/drawing/edge_colormap.html
        nx.write_gml(self._graph, output_file)
        #nx.write_edgelist(self._graph, output_file)
    
    def to_image(self, output_file):
        # from http://networkx.github.io/documentation/latest/examples/drawing/edge_colormap.html
        #pos = nx.spectral_layout(self._graph)
        pos = nx.circular_layout(self._graph)
        #pos = nx.spring_layout(self._graph)
        colors = '#6aaed6' #range(len(self._graph.edges()))
        nx.draw( self._graph, pos, node_size=0, alpha=0.4, edge_color=colors,
                 node_color='#A0CBE2', edge_cmap=plt.cm.Blues, width=2) #, node_color='#A0CBE2' , with_labels=False)
        plt.savefig(output_file)

    def get_shortest_path(self):
        list_with_lemmas = []
        for node_name in nx.shortest_path(self._graph, source="source", target="target"):
            if node_name not in ("source", "target"):
                list_with_lemmas.append( self._lemmas_info.get_lemma( node_name ) )
        return list_with_lemmas
    
    def get_all_paths(self):
        return nx.all_simple_paths(self._graph, source="source", target="target")
    
    def remove_edge(self, node1, node2):
        self._graph.remove_edge( node1, node2 )



if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--rest_input", dest="input", default="/tmp/tmpIRRiLo/partially_skolemized_plan.n3",
                      help="File to process")
    parser.add_option("-o", "--output", dest="output", default="/tmp",
                      help="Output folder where the processed results will be written.")
    (options, args) = parser.parse_args()
    
    rdf_graph = Graph()
    rdf_graph.parse(options.input, format="n3")
    parser = LemmasParser(rdf_graph)
    lemmas = parser.parse()
    rg = Plan( lemmas )
    
    rg.to_image( output_file = options.output + "/lemma_precedences.png" )
    rg.to_gml( output_file = options.output + "/lemma_precedences.gml" )
    
    #rg._get_shortest_path( goal = (URIRef("file:///home/tulvur/Downloads/test/image_ex/myphoto.jpg"), dbpedia_namespace["thumbnail"], None))
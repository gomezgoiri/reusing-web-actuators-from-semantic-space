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
from actuation.proofs import Namespaces
from actuation.proofs.preprocess import Preprocessor
from actuation.proofs.parsers.lemmas import LemmasParser



# TODO rethink/reorder URI or str, when and where?
# To be used with "lemma_precedences.txt"
class LemmaPrecedencesGraph(object):
    
    def __init__(self, file_path, lemmas_info):
        """
        @param file_path
            Path to the 'precedences' preprocessed file.
        @param lemma_info
            A 'Lemmas' object with the summary of a result file's content.
        """
        self.rdf_graph = Graph()
        self.rdf_graph.parse(file_path, format="n3")
        self._create_nx_graph( lemmas_info )
        
        # TODO remove from the methods params
        self._lemmas_info = lemmas_info
    
    def _is_repeated(self, added_children_uris, new_child_node_info, lemma_info):
        for added_child_uri in added_children_uris:
            added_child_info = lemma_info.get_lemma( str(added_child_uri) ) # It exists, otherwise wouldn't be in added_children_uris
            if new_child_node_info.equivalent_rest_calls( added_child_info ):
                return True
        return False
    
    def _should_be_filtered(self, added_children, child_node, lemmas_info):
        # avoid adding lemmas which are not REST calls
        # avoid adding 2 children lemmas who have the same REST calls
        if lemmas_info is not None:
            child_node_info = lemmas_info.get_lemma( child_node )
            if child_node_info is None:
                raise Exception("ERROR. Lemma %s appears in the precedence graph but its information has not been parsed: %s." % (child_node, lemmas_info) )
            
            if child_node_info.is_rest_call():
                return self._is_repeated( added_children, child_node_info, lemmas_info )
        return False
    
    def _create_nx_graph(self, lemmas_info):
        """Adds a Lemmas object with the summary of a result file's content."""
        #graph = nx.Graph()
        graph = nx.DiGraph()
        
        unique_parent_nodes = set( list( self.rdf_graph.subjects( Namespaces.REASON.because, None ) ) )
        for parent_node in unique_parent_nodes:
            if lemmas_info is not None:  # There may not be a lemmas_info to filter anything
                                        # Legacy case which mainly exists for testing purposes
                if lemmas_info.get_lemma( parent_node ) is None:
                    raise Exception("ERROR. Lemma %s appears in the precedence graph but its information has not been parsed (%s)." % (parent_node, lemmas_info) )
            
            added_children = []
            for child_node_uri in self.rdf_graph.objects( parent_node, Namespaces.REASON.because ):
                child_node = str(child_node_uri)
                
                if not self._should_be_filtered( added_children, child_node, lemmas_info ):
                    added_children.append( child_node )
                    
                    graph.add_node( parent_node ) # it's OK if it exists from the previous iteration
                    graph.add_node( child_node )
                    # lemma1 because lemma2, means that lemma2 -> lemma1
                    graph.add_edge( child_node, parent_node )
        
        self._append_source_and_target( graph )
        self.graph = graph # or maybe simply return?
    
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
        nx.write_gml(self.graph, output_file)
        #nx.write_edgelist(self.graph, output_file)
    
    def to_image(self, output_file):
        # from http://networkx.github.io/documentation/latest/examples/drawing/edge_colormap.html
        #pos = nx.spectral_layout(self.graph)
        pos = nx.circular_layout(self.graph)
        #pos = nx.spring_layout(self.graph)
        colors = '#6aaed6' #range(len(self.graph.edges()))
        nx.draw( self.graph,
                 pos, node_size=0, alpha=0.4, edge_color=colors, node_color='#A0CBE2', edge_cmap=plt.cm.Blues, width=2) #, node_color='#A0CBE2' , with_labels=False)
        plt.savefig(output_file)

    def get_shortest_path(self):
        list_with_lemmas = []
        for node_name in nx.shortest_path(self.graph, source="source", target="target"):
            if node_name not in ("source", "target"):
                list_with_lemmas.append( self._lemmas_info.get_lemma( node_name ) )
        return list_with_lemmas
    
    def get_all_paths(self):
        return nx.all_simple_paths(self.graph, source="source", target="target")
    
    def remove_edge(self, node1, node2):
        self.graph.remove_edge( node1, node2 )



if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input", default="../../../files/precedences.txt",
                      help="File to process")
    parser.add_option("-f", "--lemma_info", dest="filter_path", default=None, #"/tmp",
                      help="""Delete repeated REST calls.
                              Avoid REST call repetitions using the information from the provided folder.
                              Note that the folder should contain a 'bindings.txt' and 'services.txt' files.
                              """
                           )
    parser.add_option("-o", "--output", dest="output", default="/tmp",
                      help="Output folder where the image will be written.")
    (options, args) = parser.parse_args()
    
    
    rg = None
    if options.filter_path is not None:
        lemmas = LemmasParser.parse_file( options.filter_path + "/" + Preprocessor.get_output_filename("services"),
                                          options.filter_path + "/" + Preprocessor.get_output_filename("bindings") )
        rg = LemmaPrecedencesGraph( options.input, lemmas )
    else:
        rg = LemmaPrecedencesGraph( options.input )
    
    rg.to_image( output_file = options.output + "/lemma_precedences.png" )
    rg.to_gml( output_file = options.output + "/lemma_precedences.gml" )
    
    #rg._get_shortest_path( goal = (URIRef("file:///home/tulvur/Downloads/test/image_ex/myphoto.jpg"), dbpedia_namespace["thumbnail"], None))
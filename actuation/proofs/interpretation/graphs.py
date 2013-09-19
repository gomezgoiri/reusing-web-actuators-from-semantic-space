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
from rdflib import Graph, Namespace
import networkx as nx
import matplotlib.pyplot as plt
from actuation.proofs.extract_info import UsefulInformationExtractor
from actuation.proofs.interpretation.lemma_parser import LemmaParser

r_ns = Namespace("http://www.w3.org/2000/10/swap/reason#")

# TODO rethink/reorder URI or str, when and where?
# To be used with "lemma_precedences.txt"
class LemmaPrecedencesGraph(object):
    
    def __init__(self, file_path):
        self.rdf_graph = Graph()
        self.rdf_graph.parse(file_path, format="n3")
        self.lemma_info = None
    
    def add_lemmas_info(self, lemmas_info):
        self.lemma_info = lemmas_info
    
    def get_lemma_info(self, node):
        if node in self.lemma_info:
            return self.lemma_info[node]
        return None
    
    def _is_rest_call(self, new_child_node):
        return new_child_node in self.lemma_info and self.lemma_info[new_child_node].rest is not None
    
    def _is_repeated(self, added_children_uris, new_child_node):                
        node_li = self.lemma_info[ new_child_node ]
        for added_child_uri in added_children_uris: # not sure if "in" should work without redefining the hash_code
            
            added_child = str(added_child_uri)
            if added_child in self.lemma_info:
                added_li = self.lemma_info[ added_child ]
                if node_li.equivalent_rest_calls( added_li ):
                    return True
        return False
    
    def _should_be_filtered(self, added_children, child_node):
        # avoid adding lemmas which are not REST calls
        # avoid adding 2 children lemmas who have the same REST calls
        if self.lemma_info is not None:
            if self._is_rest_call(child_node):
                return self._is_repeated( added_children, child_node )
        return False
    
    def create_nx_graph(self):
        #graph = nx.Graph()
        graph = nx.DiGraph()
        
        unique_parent_nodes = set( list( self.rdf_graph.subjects( r_ns.because, None ) ) )
        for parent_node in unique_parent_nodes:
            added_children = []
            for child_node_uri in self.rdf_graph.objects( parent_node, r_ns.because ):
                child_node = str(child_node_uri)
                if not self._should_be_filtered( added_children, child_node ):
                    added_children.append( child_node )
                    
                    graph.add_node( parent_node )
                    graph.add_node( child_node )
                    # lemma1 because lemma2, means that lemma2 -> lemma1
                    graph.add_edge( child_node, parent_node )
        
        # create starting point and ending point and link it with leaves
        graph.add_node( "source" )
        graph.add_node( "target" )
        
        for leave in (n for n,d in graph.out_degree_iter() if d==0):
            if leave is not "source" and leave is not "target":
                graph.add_edge( leave, "target" )
            
        for root in (n for n,d in graph.in_degree_iter() if d==0):
            if root is not "source" and root is not "target":  
                graph.add_edge( "source", root )
        
        self.graph = graph
    
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
        return nx.shortest_path(self.graph, source="source", target="target")
    
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
    
    
    rg = LemmaPrecedencesGraph( options.input )
    
    if options.filter_path is not None:
        lp = LemmaParser( options.filter_path + "/" + UsefulInformationExtractor.get_output_filename("services"),
                              options.filter_path + "/" + UsefulInformationExtractor.get_output_filename("bindings") )
        rg.add_lemmas_info( lp.lemmas )
    
    rg.create_nx_graph()
    rg.to_image( output_file = options.output + "/lemma_precedences.png" )
    rg.to_gml( output_file = options.output + "/lemma_precedences.gml" )
    
    #rg._get_shortest_path( goal = (URIRef("file:///home/tulvur/Downloads/test/image_ex/myphoto.jpg"), dbpedia_namespace["thumbnail"], None))
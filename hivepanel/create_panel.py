'''
created  10/06/2014

by sperez

makes hive panel from user input
'''

import sys
import os
import argparse
import shutil
import string
from ntpath import basename, dirname
from uttilities_panel import *
from file_skeletons import parameters_file, html_file

PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),'methodfiles')

NODE_MEASURES = [degree,
                nx.clustering,
                nx.betweenness_centrality, 
                nx.closeness_centrality,
                component_membership,
                ]

EDGE_MEASURES = [nx.edge_betweenness_centrality]

NUM_AXES = 3

def get_all_attributes(G):
    '''iters through nodes and edges to get their attributes'''
    nodeKeys = []
    edgeKeys = []
    
    for n in G.nodes():
        nodeKeys.extend(G.node[n].keys())
    nodeKeys = set(nodeKeys)

    for s,t in G.edges():
        edgeKeys.extend(G[s][t].keys())
    edgeKeys = set(edgeKeys)

    return list(nodeKeys), list(edgeKeys)

def make_js_files(G):
    '''make a network in js format'''
    nodeAttributes = G.graph['nodeAttributes'] #names of attributes
    edgeAttributes = G.graph['edgeAttributes']
    graphName = G.graph['title']

    newnodeFile = os.path.join(G.graph['folder'],"{0}_nodes.js".format(graphName))
    newedgeFile = os.path.join(G.graph['folder'],"{0}_edges.js".format(graphName))

    f = open(newnodeFile, 'w')
    f.write('var SVGTitle = "{0} Hive Panel"\n'.format(graphName.replace('_',' ')))
    f.write('var nodes = [\n')
    nodes = G.nodes()
    for node in nodes:
        line = '    {name: "' + str(node) +'"'
        for attribute in nodeAttributes:
            line  += ', '+attribute+': "' + str(G.node[node][attribute]) + '"'
        line += '},\n'
        f.write(line)
    f.write('];')
    f.close()

    f = open(newedgeFile,'w')
    f.write('var links = [\n')
    for (s,t) in G.edges():
        line = '  {source: nodes['+str(nodes.index(s))+'], target: nodes['+str(nodes.index(t))+']'
        for attribute in edgeAttributes:
            line  += ', '+attribute+': "' + str(G.edge[s][t][attribute]) + '"'
        line += '},\n'
        f.write(line)
    f.write('];')
    f.close()
    return None

def make_panel_parameters_file(G):
    fileName = os.path.join(G.graph['folder'],"{0}_parameters.js".format(G.graph['title']))
    f = open(fileName, 'w')
    asgtraits = [G.graph['nodeAttributes'][0],G.graph['nodeAttributes'][2]]
    postraits = [G.graph['nodeAttributes'][1],G.graph['nodeAttributes'][3]]
    newfile = parameters_file.format(G.graph['axes'],
                    str(G.graph['double']).lower(),
                    '"'    +   '","'.join(asgtraits)  +   '"',
                    '"'    +   '","'.join(postraits)  +   '"',
                    '"' +   '":"linear","'.join(asgtraits)    +  '":"linear"',
                    '"' +   '":"linear","'.join(postraits)    +  '":"linear"',
                    )
    f.write(newfile)
    f.close()
    return None

def make_html_file(G):
    fileName = os.path.join(G.graph['folder'],"{0}_panel.html".format(G.graph['title']))
    f = open(fileName, 'w')
    newfile = html_file.format(G.graph['title'])
    f.write(newfile)
    f.close()
    return None

def make_panel_methods(G):
    destination = G.graph['folder']
    fileName = "panel_methods.js"
    shutil.copy(os.path.join(PATH,fileName),destination)
    fileName = "panel_style.css"
    shutil.copy(os.path.join(PATH,fileName),destination)
    fileName = "d3.v3.min.js"
    shutil.copy(os.path.join(PATH,fileName),destination)
    fileName = "d3.hive.v0.min.js"
    shutil.copy(os.path.join(PATH,fileName),destination)
    fileName = "remove_icon.svg"
    shutil.copy(os.path.join(PATH,fileName),destination)
    return None

def make_panel(G):
    make_js_files(G)
    make_panel_parameters_file(G)
    make_html_file(G)
    make_panel_methods(G)
    return None

def main(*argv):
    '''handles user input and creates a panel'''
    parser = argparse.ArgumentParser(description='This scripts takes networks and created the necessary file to make an interactive Hive panel')
    parser.add_argument('-input', help='Location of network file')
    parser.add_argument('-format', help='Input format of network')
    parser.add_argument('-nodes', help='Location of node network file')
    parser.add_argument('-edges', help='Location of edge network file')
    parser.add_argument('-title', help='Title/Name of graph')
    parser.add_argument('-folder', help='Output folder')
    parser.add_argument('-axes', help='Number of axes',default=NUM_AXES)
    parser.add_argument('-double', help='Makes hive plots with doubled axes', action = 'store_true')
    args = parser.parse_args()

    #Get graph in networkx format
    if args.format=='graphml':
        print_message("Reading .graphml as a networkx graph.")
        G = import_graphml(args.input)
        title = basename(args.input).split('.')[0]
        folder = dirname(args.input)
    elif args.format=='txt':
        print_message("Reading .txt as a networkx graph.")
        G = import_graph(args.nodes, args.edges)
        title = basename(args.nodes).split('.')[0]
        folder = dirname(args.nodes)
    else:
        print_message("Please specify the format of your network: .gexf, .graphml, or a 2 .txt files with node and edge attribute.")
        parser.print_help()
        sys.exit()


    if args.title:
        title = args.title

    if args.folder:
        folder = args.folder

    #store all the plotting info in the graph as attributes
    G.graph['axes']=args.axes
    G.graph['double']=args.double
    G.graph['folder']=folder
    G.graph['title']=title
    G.graph['nodeAttributes'],G.graph['edgeAttributes']=get_all_attributes(G)
    for m in NODE_MEASURES:
        G.graph['nodeAttributes'].append(m.__name__)
        measures = m(G)
        nx.set_node_attributes(G,m.__name__,measures)

    for m in EDGE_MEASURES:
        G.graph['edgeAttributes'].append(m.__name__)
        measures = m(G)
        nx.set_edge_attributes(G,m.__name__,measures)

    print "PARAMETERS OF NETWORK:"
    print "     Network name:", G.graph['title']
    print "     Node attributes:\n\t\t", '\n\t\t'.join(G.graph['nodeAttributes'])
    print "     Edge attributes:\n\t\t", '\n\t\t'.join(G.graph['edgeAttributes'])
    print "     Output folder", G.graph['folder']

    print_message('Making panel.')
    make_panel(G,)



if __name__ == "__main__":
    main(*sys.argv[1:])







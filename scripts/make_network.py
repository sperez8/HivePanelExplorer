'''
created  10/06/2014

by sperez

makes hive panel from user input
'''

import sys
import os
import argparse
import networkx as nx
import numpy as np
import string
from gexf import read_gexf
from ntpath import basename

NODE_MEASURES = [nx.betweenness_centrality, 
                nx.degree_centrality,
                nx.closeness_centrality]

EDGE_MEASURES = [nx.edge_betweenness_centrality]


def import_gexf(gexfFile):
    #parse graphml file
    G = read_gexf(gexfFile)
    return G

def import_graphml(graphmlFile):
    #parse graphml file
    G = nx.read_graphml(graphmlFile)
    return G

def import_graph(nodeFile, edgeFile, filterEdges = True):
    '''make a networkx graph from a csv or tsv'''
    
    nodes, nodeAttributes = get_nodes(nodeFile)
    sources, targets, edgeAttributes = get_edges(edgeFile)
    
    G = make_graph(sources, targets, nodes, filterEdges)
    for i,n in enumerate(nodes):
        for p,v in nodeAttributes.iteritems():
            G.node[n][p] = v[i]

    for i,e in enumerate(zip(sources, targets)):
        s,t = e[0],e[1]
        if filterEdges:
            if s not in nodes or t not in nodes:
                continue
        for p,v in edgeAttributes.iteritems():
            G[s][t][p] = v[i]
    return G

def measure_all(G):
    '''measure all interesting global network measures'''
    measure = {}
    
    return measures

def convert_gexf(gexfFile):
    G = import_gexf(gexfFile)
    fileName = gexfFile.split('.gexf')[0]
    convert_graph(G,fileName)
    return None

def convert_graphml(graphmlFile):
    G = import_graphml(graphmlFile)
    fileName = graphmlFile.split('.graphml')[0]
    convert_graph(G,fileName)
    return None

def convert_graph(G,fileName):
    sources, targets, edgeAttributes = zip(*G.edges(data=True))
    nodeFile = fileName+'_nodes.csv'
    edgeFile = fileName+'_edges.csv'
    nf = open(nodeFile,'w')
    keys = []
    for node, nodeAttributes in G.nodes(data=True):
        new_keys = nodeAttributes.keys()
        if new_keys != keys:
            keys.extend(new_keys)
    
    keys = set(keys)
    
    #write header
    if keys:
        nf.write('Node'+','+','.join(keys))
    else:
        nf.write('Node')        
    
    for node, nodeAttributes in G.nodes(data=True):
        row = []
        row.append(node)
        for k in keys:
            if k in nodeAttributes.keys():
                row.append(str(nodeAttributes[k]).replace(',', ';'))
            else:
                row.append('None')
        nf.write('\n' + ','.join([str(r) for r in row]))
    
    nf.close()
    
    ef = open(edgeFile,'w')
    keys = []
    for source,target, edgeAttributes in G.edges(data=True):
        new_keys = edgeAttributes.keys()
        if new_keys != keys:
            keys.extend(new_keys)
    
    keys = set(keys)
    
    if keys:
        ef.write('source' + ',' + 'target' + ',' +','.join(keys))
    else: 
        ef.write('source' + ',' + 'target')

    for source, target, edgeAttributes in G.edges(data=True):
        row = []
        row.append(source)
        row.append(target)
        for k in keys:
            if k in edgeAttributes.keys():
                row.append(str(edgeAttributes[k]))
            else:
                row.append('None')
        ef.write('\n' + ','.join([str(r) for r in row]))
    
    print "writing nodefile", nodeFile
    print "writing edgefile", edgeFile
    return None


def make_graph(sources, targets, nodes, filterEdges= True):
    '''Makes a graph using the networkx package Graph instance'''
    G = nx.Graph()
    G.add_edges_from(zipper(sources,targets))
    if filterEdges:
        for n in G.nodes():
            if n not in nodes:
                G.remove_node(n)
    return G


def get_nodes(inputFile,removeNA=None):
    '''gets nodes and their attribute from csv file'''
    
    delimiter = get_delimiter(inputFile)

    data = np.genfromtxt(inputFile, delimiter=delimiter, dtype='str', filling_values = 'None')
    
    #get attribute and format as strings
    attribute = data[0,1:]
    attribute = format_attribute(attribute)
    
    if removeNA:
        colName = nx.betweenness_centrality.__name__.replace('_',' ').capitalize()
        col = np.where(data[0,:]==colName)[0][0]
        #remove first row with column names
        data = data[1:,]
        data = data[np.where(data[:,col]!=removeNA)]
    else:
        #remove first row with column names
        data = data[1:,]

    #get all the node data
    nodes = list(data[:,0])
    
    #take note of number of nodes
    totalNodes = len(nodes)
    
    #transform node attribute into the numerical types if possible
    nodeAttributes = {}

    for i, column in enumerate(data[:,1:].T):
        values = convert_type(list(column))
        nodeAttributes[attribute[i]] = values
    nodeAttributes = nodeAttributes

    return nodes, nodeAttributes


def get_edges(inputFile):
    '''gets edges and their attribute from csv file'''
    
    delimiter = get_delimiter(inputFile)
    data = np.genfromtxt(inputFile, delimiter=delimiter, dtype='str', filling_values = 'None')
    
    #get attribute and format as strings
    attribute = data[0,2:]
    attribute = format_attribute(attribute)
    
    #remove first row with column names
    data = data[1:,]
    
    #get all the edge data
    sources = list(data[:,0])        
    targets = list(data[:,1])
    
    #take note of number of edges:
    totalEdges = len(sources)

    #transform edge attribute into the numerical types if possible
    edgeAttributes = {}

    for i, column in enumerate(data[:,2:].T):
        values = convert_type(list(column))
        edgeAttributes[attribute[i]] = values
    edgeAttributes = edgeAttributes
    
    #store the name of the edge attribute
    edgePropertyList = edgeAttributes.keys()

    return sources, targets, edgeAttributes

def convert_type(data):
    def num(s):
        '''convert list of strings to corresponding int or float type'''
        try:
            return int(d)
        except ValueError:
            return float(d)
    
    try:
        convertedData = [num(d) for d in data]
        return convertedData
    except ValueError:
        return data

def get_delimiter(inputFile):
    '''detect if input file is a tab or comma delimited file
        and return delimiter.'''
    
    ext = os.path.splitext(os.path.basename(inputFile))[1]
    
    if 'tab' in ext or 'tsv' in ext:
        return '\t'
    elif 'csv' in ext:
        return ','
    elif 'txt' in ext:
        #detects delimiter by counting the number of tabs and commas in the first line
        f = open(inputFile, 'r')
        first = f.read()
        if first.count(',') > first.count('\t'):
            return ','
        elif first.count(',') < first.count('\t'):
            return '\t'
        else:
            print "Couldn't detect a valid file extension: ", inputFile
            return ','
    else:
        print "Couldn't detect a valid file extension: ", inputFile
        return ','


def format_attribute(attribute, debug = False):
    '''takes a list of attribute names and removes all punctuation and numbers'''
    
    numbers = {1:'one', 2:'two', 3:'three', 4:'four', 5:'five', 6:'six', 7:'seven', 8:'eight', 9:'nine', 10:'ten'}
    
    def convert_word(word):
        '''remove punctuation and numbers from a word'''
        w = word
        word = ''.join(word.split()) #removes all whitespace (tabs, newlines, spaces...)
        for c in string.punctuation + string.digits:
            word = word.replace(c,'')
        if w != word:
            if debug:
                print "The attribute \'{0}\' contains spaces, punctuation or digits and has been renamed '{1}'".format(w,word)
        return word
         
    newAttributes = []
    i = 1
    for prop in attribute:
        newProp = convert_word(prop)
        if not newProp:
            #if attribute isn't named, we give it one
            newAttributes.append('unNamedProperty' + numbers[i] + '')
            i += 1
        elif newProp in newAttributes:
            newAttributes.append(newProp + 'second')
        else:
            newAttributes.append(newProp)
            
    return newAttributes

def zipper(*args):
    '''a revamped version of zip() method that checks that lists
    to be zipped are the same length'''
    for i,item in enumerate(args):
        if len(item) != len(args[0]):
            raise ValueError('The lists to be zipped aren\'t the same length.')
    
    return zip(*args)

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
    nodeAttributes = G['nodeAttributes'] #names of attributes
    edgeAttributes = G['edgeAttributes']


    newnodeFile = os.path.join(newnetpath,"{0}_nodes.js".format(graphName))
    newedgeFile = os.path.join(newnetpath,"{0}_edges.js".format(graphName))

    f = open(newnodeFile, 'w')
    f.write('var SVGTitle = "{0} Hive Panel"\n'.format(graphName))
    f.write('var nodes = [\n')
    for node in G.nodes():
        line = '    {name: \'' + str(node) +'\''
        for p,v in nodeAttributes.iteritems():
            line  += ', '+p+': \'' + str(v[i]) + '\''
        line += '},\n'
        f.write(line)
    f.write('];')
    f.close()

    f = open(newedgeFile,'w')
    f.write('var links = [\n')
    for i,(s,t) in enumerate(zip(sources, targets)):
        line = '  {source: nodes['+str(nodes.index(s))+'], target: nodes['+str(nodes.index(t))+']'
        for p,v in edgeAttributes.iteritems():
            line  += ', '+p+': \'' + str(v[i]) + '\''
        line += '},\n'
        f.write(line)
    f.write('];')
    f.close()
    return None

def make_panel(G):
    return None




def main(*argv):
    '''handles user input and creates a panel'''
    parser = argparse.ArgumentParser(description='This scripts takes networks and created the necessary file to make an interactive Hive panel')
    parser.add_argument('-input', help='Location of network file')
    parser.add_argument('-format', help='Input format of network')
    parser.add_argument('-nodes', help='Location of node network file')
    parser.add_argument('-edges', help='Location of edge network file')
    parser.add_argument('-title', help='Title/Name of graph')
    args = parser.parse_args()

    #Get graph in networkx format
    if args.format=='graphml':
        print "Reading .graphml as a networkx graph."
        G = import_graphml(args.input)
        title = basename(args.input).split('.')[0]
    elif args.format=='gexf':
        #need a specific version of networkx for read_gexf to work
        # import pkg_resources
        # pkg_resources.require("networkx==1.7")
        # print "Reading .gefx as a networkx graph."
        # G = import_gexf(args.input)
        print "Gexf files currently not supported."
        sys.exit()

    elif args.format=='txt':
        print "Reading .txt as a networkx graph."
        G = import_graph(args.nodes, args.edges)
        title = basename(args.nodes).split('.')[0]
    else:
        print "Please specify the format of your network: .gexf, .graphml, or a 2 .txt files with node and edge attribute."
        parser.print_help()
        sys.exit()


    if args.title:
        title = args.title

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


    print 'Making panel.'
    make_panel(G)



if __name__ == "__main__":
    main(*sys.argv[1:])

# file = "C:\\Users\\Sarah\\Dropbox\\1-Hive panels\\Diseasome\\diseasome.gexf"
# f = open(file,'r')
# print f.readlines()
# convert_gexf(file)






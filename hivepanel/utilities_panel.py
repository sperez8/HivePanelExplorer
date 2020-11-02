'''
created  10/06/2014

by sperez

functions used by create_panel
'''
from __future__ import print_function

import sys
import os
import numpy as np
import string

# Loading local copy of networkx package
sys.path.insert(0, os.path.abspath(".."))
import networkx as nx


def degree(G):
    return G.degree()


def component_membership(G):
    nodeComponents = {}
    # get connected components sorted by size
    ccs = sorted(nx.connected_components(G), key=len, reverse=True)
    for i, cc in enumerate(ccs):
        for node in cc:
            nodeComponents[node] = i
    return nodeComponents


def import_graphml(graphmlFile):
    # parse graphml file
    G = nx.read_graphml(graphmlFile)
    return G.to_undirected(reciprocal=False)


def import_graph(nodeFile, edgeFile, include_lonely_nodes, filterEdges=True):
    '''make a networkx graph from a csv or tsv'''

    nodes, nodeAttributes = get_nodes(nodeFile)
    sources, targets, edgeAttributes = get_edges(edgeFile)

    G = make_graph(sources, targets, nodes, include_lonely_nodes, filterEdges)
    allNodes = G.nodes()
    for i, n in enumerate(nodes):
        for p in nodeAttributes.keys():
            v = nodeAttributes[p]
            if not include_lonely_nodes and n not in allNodes:
                continue
            G.node[n][p] = v[i]

    for i, e in enumerate(zip(sources, targets)):
        s, t = e[0], e[1]
        if filterEdges:
            if s not in nodes or t not in nodes:
                continue
        for p in edgeAttributes.keys():
            v = edgeAttributes[p]
            G[s][t][p] = v[i]
    return G


def convert_graphml(graphmlFile):
    G = import_graphml(graphmlFile)
    fileName = graphmlFile.split('.graphml')[0]
    convert_graph(G, fileName)
    return None


def convert_graph(G, fileName):
    sources, targets, edgeAttributes = zip(*G.edges(data=True))
    nodeFile = fileName + '_nodes.csv'
    edgeFile = fileName + '_edges.csv'
    nf = open(nodeFile, 'w')
    keys = []
    for node, nodeAttributes in G.nodes(data=True):
        new_keys = nodeAttributes.keys()
        if new_keys != keys:
            keys.extend(new_keys)

    keys = set(keys)

    # write header
    if keys:
        nf.write('Node' + ',' + ','.join(keys))
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

    ef = open(edgeFile, 'w')
    keys = []
    for source, target, edgeAttributes in G.edges(data=True):
        new_keys = edgeAttributes.keys()
        if new_keys != keys:
            keys.extend(new_keys)

    keys = set(keys)

    if keys:
        ef.write('source' + ',' + 'target' + ',' + ','.join(keys))
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

    print_message("writing nodefile", nodeFile)
    print_message("writing edgefile", edgeFile)
    return None


def make_graph(sources, targets, nodes, include_lonely_nodes, filterEdges=True):
    '''Makes a graph using the networkx package Graph instance'''
    G = nx.Graph()
    if include_lonely_nodes:
        G.add_nodes_from(nodes)  # add all nodes, even ones without edges...
    G.add_edges_from(zipper(sources, targets))
    if filterEdges:
        for n in G.nodes():
            if n not in nodes:
                print("I am here")
                G.remove_node(n)

    return G


def load_file(inputFile):
    # try loading as a tab delimited file, otherwise a comma delimited file.
    try:
        data = np.genfromtxt(inputFile, delimiter='\t', dtype='str', filling_values='None')
        attribute = data[0, 1:]  # this will fail if file is comma
    except IndexError:
        try:
            data = np.genfromtxt(inputFile, delimiter=',', dtype='str', filling_values='None')
            attribute = data[0, 1:]
        except IndexError:
            print_message("ERROR: Please use a tab delimited or comma delimited text file")
            sys.exit()
    return data


def get_nodes(inputFile, removeNA=None):
    '''gets nodes and their attribute from csv file'''

    data = load_file(inputFile)
    attribute = data[0, 1:]

    # get attribute and format as strings
    attribute = format_attribute(attribute)

    if removeNA:
        colName = nx.betweenness_centrality.__name__.replace('_', ' ').capitalize()
        col = np.where(data[0, :] == colName)[0][0]
        # remove first row with column names
        data = data[1:, ]
        data = data[np.where(data[:, col] != removeNA)]
    else:
        # remove first row with column names
        data = data[1:, ]

    # get all the node data
    nodes = list(data[:, 0])

    # take note of number of nodes
    totalNodes = len(nodes)

    # transform node attribute into the numerical types if possible
    nodeAttributes = {}

    for i, column in enumerate(data[:, 1:].T):
        values = convert_type(list(column))
        nodeAttributes[attribute[i]] = values
    nodeAttributes = nodeAttributes

    return nodes, nodeAttributes


def get_edges(inputFile):
    '''gets edges and their attribute from csv file'''

    data = load_file(inputFile)

    # get attribute and format as strings
    attribute = data[0, 2:]
    attribute = format_attribute(attribute)

    # remove first row with column names
    data = data[1:, ]

    # get all the edge data
    sources = list(data[:, 0])
    targets = list(data[:, 1])

    # take note of number of edges:
    totalEdges = len(sources)

    # transform edge attribute into the numerical types if possible
    edgeAttributes = {}

    for i, column in enumerate(data[:, 2:].T):
        values = convert_type(list(column))
        edgeAttributes[attribute[i]] = values
    edgeAttributes = edgeAttributes

    # store the name of the edge attribute
    edgePropertyList = edgeAttributes.keys()

    return sources, targets, edgeAttributes


def convert_type(data):
    def num(d):
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


def format_attribute(attribute, debug=False):
    '''takes a list of attribute names and removes all punctuation and numbers'''

    numbers = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine',
               10: 'ten'}

    def convert_word(word):
        '''remove punctuation and numbers from a word'''
        w = word
        word = '_'.join(word.split())  # removes all whitespace (tabs, newlines, spaces...)
        for c in string.punctuation.replace('_', '') + string.digits:
            word = word.replace(c, '')
        if w != word:
            if debug:
                print_message(
                    "The attribute \'{0}\' contains spaces, punctuation or digits and has been renamed '{1}'".format(w,
                                                                                                                     word))
        return word

    newAttributes = []
    i = 1
    for prop in attribute:
        newProp = convert_word(prop)
        if not newProp:
            # if attribute isn't named, we give it one
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
    for i, item in enumerate(args):
        if len(item) != len(args[0]):
            raise ValueError('The lists to be zipped aren\'t the same length.')

    return zip(*args)


def print_message(*args):
    '''Formats terminal messages for user'''
    print("\n*\n ", ' '.join(args), "\n")
    return None

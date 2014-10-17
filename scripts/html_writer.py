'''
created  03/06/2014

by sperez

Takes user input and calls Hive module to produce the JavaScript files
needed to make a hive plot in D3 using Mike Bolstock's D3 hive module
'''
#library imports
import os
import sys
import math

#hive plot specific imports
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

from htmlDoc import htmlDoc, htmlDocPanel
import string

TEMP_FOLDER = _root_dir + '/tmp/'
NEUTRAL_COLOR = "#5C5C5C"

EDGE_WIDTH = 1.3
EDGE_OPACITY = 0.8
NODE_OPACITY = 0.6

LARGE_NODE_NUMBER = 100
LARGE_EDGE_NUMBER = 500

def write_nodes(file, hive):
    '''outputs node info to a text file
        in a javascript variable format'''
    
    f = open(file, 'w')

    f.write('var nodes = [\n')
    
    for i,n in enumerate(hive.nodes):
        if n[-2:] == '.1' or n[-2:] == '.2':
            name = n[:-2]
        else: name = n
        line  = '  {axis: ' + str(hive.axisAssignment[n]-1) + ', pos: ' + str(hive.nodePositions[n])
        line += ', name: \'' + str(name) +'\''
        for property,values in hive.nodeProperties.iteritems():
            if i < len(values):
                index = i
            else:
                index = i - len(values) #for doubled axes
            line  += ', '+str(property) + ': \'' + str(values[index]) +'\''
        line += '},\n'
        f.write(line)
    f.write('];')
    
def write_nodes_panel(file, hives, rules):
    '''outputs node info to a text file
        in a javascript variable format'''
    
    f = open(file, 'w')

    f.write('var nodes = [\n')
    
    nodes = hives[rules[0]].nodes
    for i,n in enumerate(nodes):
        if n[-2:] == '.1' or n[-2:] == '.2':
            name = n[:-2]
        else: 
            name = n
        
        line = '    {name: \'' + str(name) +'\''
        
        rulesAdded = []
        for (a,p) in rules:
            hive = hives[(a,p)]
            asgRule = a + '_axis' #to distinguish from position values of the same rule
            posRule = p + '_pos' #to distinguish from assignment values of the same rule
            if asgRule not in rulesAdded:
                line  += ', '+asgRule+': ' + str(hive.axisAssignment[n]-1)
                rulesAdded.append(asgRule)
            if posRule not in rulesAdded:
                line  += ', '+posRule+': ' + str(hive.nodePositions[n])
                rulesAdded.append(posRule)
        for property,values in hive.nodeProperties.iteritems():
            if i < len(values):
                index = i
            else:
                index = i - len(values) #for doubled axes
            line  += ', '+str(property) + ': \'' + str(values[index]) +'\''
        line += '},\n'
        f.write(line)
    f.write('];')
    
def write_edges(file, hive):
    '''outputs node info to a text file
        in a javascript variable format'''
    properties = hive.edgePropertyList
    
    f = open(file, 'w')
    f.write('var links = [\n')
    for i, (s, t) in enumerate(hive.edges):        
        line = '  {source: nodes['+str(hive.nodes.index(s))+'], target: nodes['+str(hive.nodes.index(t))+'], type: ' + str(hive.edgeStyling[(s,t)])
        for j, value in enumerate(hive.edgeProperties[i]):
                line  += ', '+str(properties[j]) + ': \'' + str(value) +'\''
        line += '},\n'
        f.write(line)
    f.write('];')


def make_html(title, hive, hive_size, folder = TEMP_FOLDER, rules = None):
    '''takes a hive instance and write the
    following files:
        nodes.js - contains nodes, position and coloring
        edges.js - contains edges and their type
        hiveplot.html - contains the html and D3 script to make the hive plot!
    '''
    newtitle = reformat_title(title)
    outputfile = os.path.join(folder, newtitle + ".html")
    print '    Making the hive plot \'{0}\''.format(outputfile)
    
    nodeFileName = title + '_nodes.js' 
    edgeFileName = title + '_edges.js'
    nodeFile = os.path.join(folder, nodeFileName)
    edgeFile = os.path.join(folder, edgeFileName)
    
    write_nodes(nodeFile, hive)
    write_edges(edgeFile, hive)
    
    #Preparing all variables to insert into htmlDoc
    colorNeutral = NEUTRAL_COLOR
    
    title = string.capitalize(title)
    numAxis = hive.numAxes
    if hive.doubleAxes:
        numAxis *= 2
    angles = hive.angles
    nodeColor = hive.nodeColor
    edgeColor = hive.edgePalette
    
    nodeReveal = '"<br><br><b>Name: " + d.name +"</b>"'
    for p in hive.nodeProperties.keys():
        nodeReveal += '+\',\'+"    ' + string.capitalize(p) + ': " + d.' + p
    
    linkReveal = '"<br><br><b>Source: " + d.source.name + ", Target: " + d.target.name +"</b>"'
    for p in hive.edgePropertyList:
        linkReveal += '+\',\'+\"    ' + string.capitalize(p) + ': \" + d.' + p
    
    assignmentRule = string.capitalize(rules['assignment']) + ': (' + ', '.join(hive.valuesAssignment) + ')'
    positionsRule = string.capitalize(rules['position']) + ': (' + ', '.join(hive.valuesPosition) + ')'
    if hive.valuesEdges:
        colorRule = string.capitalize(rules['edges']) + ': (' + ', '.join(hive.valuesEdges) + ')'
    else:
        colorRule = 'None'
    
    edgeWidth = EDGE_WIDTH
    edgeOpacity = EDGE_OPACITY
    nodeOpacity = NODE_OPACITY
    
    #adjust and reduce the opacity of nodes and edges given how many there are
    if hive.totalNodes/LARGE_NODE_NUMBER > 0:
        nodeOpacity *= pow(0.8,hive.totalNodes/LARGE_NODE_NUMBER/2)
    if hive.totalEdges/LARGE_EDGE_NUMBER > 0:
        edgeWidth *= pow(0.8, hive.totalEdges/LARGE_EDGE_NUMBER/2)
        edgeOpacity *= pow(0.8, hive.totalEdges/LARGE_EDGE_NUMBER/3)
    
  
    #writing the html
    with open(outputfile, 'w') as f:           
        document = htmlDoc.format(nodeFileName, edgeFileName, title,
                       colorNeutral, numAxis, angles, nodeColor, 
                       edgeColor, nodeReveal, linkReveal,
                       assignmentRule, positionsRule, colorRule,
                       edgeWidth, edgeOpacity, nodeOpacity, 
                       hive_size[0], hive_size[1]
                       )    
        f.write(document)
    f.close()
    
    return outputfile


def make_panel_html(title, hives, panelSize, rules, folder = TEMP_FOLDER):
    '''takes a hive instance and write the
    following files:
        panel_nodes.js - contains nodes, position and coloring
        panel_edges.js - contains edges and their type
        hivepanelplot.html - contains the html and D3 script to make the panel of hive plots!
    '''
    newtitle = reformat_title(title)
    outputfile = os.path.join(folder, newtitle + ".html")
    print '    Making the hive panel \'{0}\''.format(outputfile)
    
    #pick a random hive, well the first one
    hive = hives[rules[0]]
    
    nodeFileName = title + '_nodes.js' 
    edgeFileName = title + '_edges.js'
    nodeFile = os.path.join(folder, nodeFileName)
    edgeFile = os.path.join(folder, edgeFileName)
    
    write_nodes_panel(nodeFile, hives, rules)
    write_edges(edgeFile, hive)
    
    #Preparing all variables to insert into htmlDoc
    colorNeutral = NEUTRAL_COLOR
    
    title = string.capitalize(title)
        
    numAxis = hive.numAxes
    if hive.doubleAxes:
        numAxis *= 2
    angles = hive.angles
    nodeColor = hive.nodeColor
    edgeColor = hive.edgePalette
    
    nodeReveal = '"<br><br><b>Name: " + d.name +"</b>"'
    for p in hive.nodeProperties.keys():
        nodeReveal += '+\',\'+"    ' + string.capitalize(p) + ': " + d.' + p
    
    linkReveal = '"<br><br><b>Source: " + d.source.name + ", Target: " + d.target.name +"</b>"'
    for p in hive.edgePropertyList:
        linkReveal += '+\',\'+\"    ' + string.capitalize(p) + ': \" + d.' + p
    
    assignmentRule = ''
    positionsRule = ''
    asg = []
    pos = []
    for (a,p) in rules:
        hive = hives[(a,p)]
        if a not in asg:
            assignmentRule += string.capitalize(a) + ': (' + ', '.join(hive.valuesAssignment) + '),     '
            asg.append(a)
        if p not in pos:
            positionsRule += string.capitalize(p) + ': (' + ', '.join(hive.valuesPosition) + '),     '
            pos.append(p)
    rowRules = '[\"'+'\",\"'.join(asg)+'\"]'
    columnRules = '[\"'+'\",\"'.join(pos)+'\"]'
    
    if hive.valuesEdges:
        colorRule = string.capitalize(rules['edges']) + ': (' + ', '.join(hive.valuesEdges) + ')'
    else:
        colorRule = 'None'
    
    edgeWidth = EDGE_WIDTH
    edgeOpacity = EDGE_OPACITY
    nodeOpacity = NODE_OPACITY
    
    #adjust and reduce the opacity of nodes and edges given how many there are
    if hive.totalNodes/LARGE_NODE_NUMBER > 0:
        nodeOpacity *= pow(0.8,hive.totalNodes/LARGE_NODE_NUMBER/2)
    if hive.totalEdges/LARGE_EDGE_NUMBER > 0:
        edgeWidth *= pow(0.8, hive.totalEdges/LARGE_EDGE_NUMBER/2)
        edgeOpacity *= pow(0.8, hive.totalEdges/LARGE_EDGE_NUMBER/3)
    
    panel_size = (1000,550)
  
    #writing the html
    with open(outputfile, 'w') as f:           
        document = htmlDocPanel.format(nodeFileName, edgeFileName, title,
                                       colorNeutral, numAxis, angles,
                                       nodeColor, edgeColor, nodeReveal, 
                                       linkReveal,assignmentRule, positionsRule,
                                       colorRule, edgeWidth, edgeOpacity,
                                       nodeOpacity, panel_size[0], panel_size[1], 
                                       rowRules, columnRules, panelSize[0])    
        f.write(document)
    f.close()
    
    return outputfile

def reformat_title(title):
    '''remove punctuation from the title'''
    newtitle = title
    for p in "#$%&\'*+/:;<=>?@[\\]^`{|}~:":
        newtitle = newtitle.replace(p,'')
    if newtitle != title:
        print "The title \'{0}\' contained punctuation which have been removed".format(title)
    return newtitle

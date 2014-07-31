'''
created  03/06/2014

by sperez

Takes user input and calls Hive module to produce the JavaScript files
needed to make a hive plot in D3 using Mike Bolstock's D3 hive module
'''
#library imports
import os
import sys

#hive plot specific imports
_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

from data import html_items
import string

TEMP_FOLDER = _root_dir + '/tmp/'
NEUTRAL_COLOR = "#5C5C5C"



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


def make_html(title, hive, folder = TEMP_FOLDER, rules = None):
    '''takes a hive instance and write the
    following files:
        nodes.js - contains nodes, position and coloring
        edges.js - contains edges and their type
        hiveplot.html - contains the html and D3 script to make the hive plot!
    '''
    htmlItems = html_items.htmlContainer
    keyOrder = html_items.keyOrder
    
    outputfile = os.path.join(folder, title + ".html")
    print '    Making the hive plot \'{0}\''.format(outputfile)
    nodeFileName = title + '_nodes.js' 
    edgeFileName = title + '_edges.js'
    nodeFile = os.path.join(folder, nodeFileName)
    edgeFile = os.path.join(folder, edgeFileName)
    
    write_nodes(nodeFile, hive)
    write_edges(edgeFile, hive)
    
    with open(outputfile, 'w') as f:
        for key in keyOrder:
            text = htmlItems[key]
            #wrap text given user input
            if key == 'nodefile':
                f.write('<script src="' + nodeFileName  +  '"></script>')
            elif key == 'edgefile':
                f.write('<script src="' + edgeFileName +  '"></script>')
            elif key == 'start js parameters':
                f.write('<script> \n//All the user defined parameters')
            elif key == 'titleheader':
                f.write('var SVGTitle = \'' + 'Hive plot : ' + string.capitalize(title) + '\'')
            elif key == 'rules':
                if rules:
                    f.write('d3.select("body").select("#rules").append("p")\n\t.html(')
                    f.write('\"<br><br>Node assignment property: '+ string.capitalize(rules['assignment']) + ': (' + ', '.join(hive.valuesAssignment) + ')')
                    f.write(' <br><br>Node positioning property: '+ string.capitalize(rules['position']) + ': (' + ', '.join(hive.valuesPosition) + ')')
                    f.write(' <br><br>Edge coloring property: '+ string.capitalize(rules['edges']) + ': (' + ', '.join(hive.valuesEdges) + ')')
                    f.write('\")')
                    f.write('\n\t.style("color", "' + NEUTRAL_COLOR + '")')
            elif key == 'angles':
                f.write('var angle = ['+ ','.join([str(a) for a in hive.angles]) +']')
            elif key == 'color':
                #f.write('var modulecolor = ' + '[\'' + color + '\']') #doesn't work yet
                f.write('var nodecolor = ' + '\'' + hive.nodeColor + '\'')
            elif key == 'edge_color':
                if isinstance(hive.edgePalette,str):
                    f.write('var edge_color = [\'' + hive.edgePalette +'\']')
                else: 
                    f.write('var edge_color = [\'' + '\',\''.join([str(c) for c in hive.edgePalette]) +'\']')
            elif key == 'numAxes':
                if hive.doubleAxes:
                    f.write('var num_axis = ' + str(hive.numAxes*2))
                else:
                    f.write('var num_axis = ' + str(hive.numAxes))
            elif key == 'revealNode':
                    f.write('var revealNode = function(d,color){\n')
                    f.write('    d3.select("body").select("#reveal").append("p")\n\t\t.html(')
                    f.write('"<br><br><b>Name: " + d.name +"</b>"')
                    for p in hive.nodeProperties.keys():
                        f.write('+\',\'+"    ' + string.capitalize(p) + ': " + d.' + p) 
                    f.write(')')
                    f.write('\n\t\t.style("color", color)')
                    f.write('\n\t};')
            elif key == 'revealLink':
                    f.write('var revealLink = function(d,color){\n')
                    f.write('    d3.select("body").select("#reveal").append("p")\n\t\t.html(')
                    f.write('"<br><br><b>Source: " + d.source.name + ", Target: " + d.target.name +"</b>"')
                    for p in hive.edgePropertyList:
                        f.write('+\',\'+\"    ' + string.capitalize(p) + ': \" + d.' + p) 
                    f.write(')')
                    f.write('\n\t\t.style("color", color)')
                    f.write('\n\t};')
            elif key == 'end js parameters':
                f.write('</script>')
            else:
                f.write(text)
            f.write('\n')
        
    f.close()
    
    return outputfile

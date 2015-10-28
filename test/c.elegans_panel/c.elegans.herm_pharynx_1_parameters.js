  // ****************************************** //


 //         USER DEFINED PARAMETERS            //


// ****************************************** //

var SVGTitle = 'C. elegans connectome' + ' panel'

var numAxes = 3
    doubleAxes = true

var nodeColor = 'grey'
    edgeColor = ['darkgrey']
    linkwidth = 1.2
    oplink = 0.3
    opnode = 0.2
    opnode_more = 0.6

var nodesize = 5
    nodestroke = 0.2
    nodestrokecolor = "grey"

var linkfill = "none"
    bkgcolor = "white"

var hoverOverTime = 900

var columntraits = ["cell_type","clustering","degree"];
    rowtraits = ["Somatic_position", "degree", "betweenness"];

var columnTraitScales = {"cell_type":"linear", "degree":"even", "clustering":"log"}
var rowTraitScales = {"Somatic_position":"linear","degree": "log","betweenness":"linear"}
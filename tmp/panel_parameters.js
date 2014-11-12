
  // ****************************************** //


 //         USER DEFINED PARAMETERS            //


// ****************************************** //

var SVGTitle = 'Friends Forever' + ' Hive Panel'

var num_axis = 3

var angle = d3.range(0.0001,2*Math.PI,2.0*Math.PI/num_axis)

var angles = d3.scale.ordinal()
    .domain(d3.range(num_axis))
    .range(angle);

var nodeColor = 'darkgrey'
    edgeColor = ['darkgrey']
    linkwidth = 1.3
    oplink = 0.8
    opnode = 0.8

var nodesize = 5
    nodestroke = 0.4
    nodestrokecolor = "grey"

var linkfill = "none"
    bkgcolor = "white"

var hoverOverTime = 900


var columntraits = ["Gender", "degree"];
    rowtraits = ["Gender", "Height"];
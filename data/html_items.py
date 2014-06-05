'''
created 06/05/2014

by sperez

contains all the pieces of the html and d3 functions to plot the hive
'''

from collections import OrderedDict

htmlContainer= OrderedDict()

htmlContainer['intro'] = """<!comment This is a hive plot developed using HivePlotter.>

<!DOCTYPE html>
<meta charset="utf-8">
<body>
<script src="http://d3js.org/d3.v3.min.js"></script>
<script src="http://d3js.org/d3.hive.v0.min.js"></script>
<script src="
"""
htmlContainer['nodefile'] = 'nodes.js' #will be specified by user                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
htmlContainer['filewrapper'] ='"></script> \n<script src="'
htmlContainer['linkfile'] = 'links.js' #will be specified by user
htmlContainer['titleheader'] = '"></script> \n<script> \nvar SVGTitle = \''
htmlContainer['title'] = 'hive plot 1' #will be modifed by user
htmlContainer['d3functions'] = """\'

var show_indicator = true

var nodesize = 5
    nodestroke = 0.4
    nodestrokecolor = "grey"
    ind1 = "#E3CD9D" //beige
    ind2 = "#EBAB21" //orange
    indmin = "#543A02" //brown
    
var width = 600
    height = 500
    innerRadius = 40,
    outerRadius = 240;

var linkfill = "none"
    linkwidth = 0.8
    oplink = 0.8
    opnode = 0.8
    bkgcolor = "white"
    //modulecolor = ["#bdbdbd","#80cdc1","#35978f","#01665e","#003c30"]
    //folowing colors are in order of dark to light
    modulecolor = ["#bdbdbd","#003c30","#01665e","#35978f","#80cdc1"]
    num_axis = 6    //want 6 axis
    
var angle = [-0.35, 0.35, 1.75, 2.44, 3.84, 4.54], // for 6 axis
    radius = d3.scale.linear().range([innerRadius, outerRadius]);

var angles = d3.scale.ordinal()
    .domain(d3.range(num_axis))
    .range(angle);

var colors = d3.scale.linear()
    .domain(d3.range(0,modulecolor.length,1.0))
    .range(modulecolor);

var svg = d3.select("body").append("svg")
    .attr("class", SVGTitle)
    .attr("width", width)
    .attr("height", height)
    .style("background-color", bkgcolor)
  .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

svg.selectAll(".axis")
    .data(angle)
  .enter().append("line")
    .attr("class", "axis")
    .attr("transform", function(d) { return "rotate(" + degrees(angles(d)) + ")"; })
    .attr("x1", radius.range()[0])
    .attr("x2", radius.range()[1])
    .attr("stroke-width",0.7)
    .attr("stroke", "black");

svg.selectAll(".link")
    .data(links)
  .enter().append("path")
    .attr("class", "link")
    .attr("d", d3.hive.link()
    .angle(function(d) { return angles(d.axis); })
    .radius(function(d) { return radius(d.pos); }))
    .style("fill", linkfill)
    .style("stroke-opacity", oplink)
    .style("stroke", function(d) { return colors(d.source.mod); })
    .style("stroke-width", linkwidth);
  
svg.selectAll(".node")
    .data(nodes)
  .enter().append("circle")
    .attr("class", "node")
    .attr("transform", function(d) { return "rotate(" + degrees(angles(d.axis)) + ")"; })
    .attr("cx", function(d) { return radius(d.pos); })
    .attr("r", nodesize)
    .attr("stroke-width", nodestroke)
    .attr("stroke", nodestrokecolor)
    .style("fill-opacity", function(d) {
        if (show_indicator){
            if (d.ind == 0){
                return opnode*0.3}
            else {return opnode}
            }
        else{return opnode}
        })
     .style("fill", function(d) { 
         if (show_indicator){
            if (d.ind == 1){
                return ind1}
            else if (d.ind == 2){
                return ind2}
            else if (d.ind == 3){
                return indmin}
            else {return colors(d.mod)}
            }
        else {return colors(d.mod)}
        })

function degrees(radians) {
  return radians / Math.PI * 180 - 90;
}

</script>"""

#more to be added

for i,j in htmlContainer.iteritems():
    print j
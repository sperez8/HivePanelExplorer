'''
created 06/05/2014

by sperez

contains all the pieces of the html and d3 functions to plot the hive
'''

htmlContainer= {}

keyOrder = ['intro', 'nodefile', 'edgefile',
            'start js parameters','titleheader', 'rules',
            'numAxes', 'angles','color', 'edge_color', 'revealNode', 'revealLink',
            'end js parameters', 'd3functions']

htmlContainer['intro'] = """<!comment This is a hive plot developed using HivePlotter.>
<!DOCTYPE html>
<meta charset="utf-8">
<body>
<script src="http://d3js.org/d3.v3.min.js"></script>
<script src="http://d3js.org/d3.hive.v0.min.js"></script>
<div id="container" style="width:900px">
<div id="title" style="height:70px;width:550px;float:left;"></div>
<div id="hive" style="height:550px;width:550px;float:left;"></div>
<div id="rules" style="height:120px;width:300px;float:left;border-bottom:2px solid #5C5C5C"></div>
<div id="reveal" style="height:60px;width:300px;float:left;"></div></div>
"""

htmlContainer['nodefile'] = 'nodes.js' #will be specified by user
htmlContainer['edgefile'] = 'links.js' #will be specified by user

htmlContainer['start js parameters'] = '' #will be specified by user
htmlContainer['titleheader'] = '' #will be specified by user
htmlContainer['rules'] = '' #will be specified by user
htmlContainer['numAxes'] = '' #will be specified by user
htmlContainer['angles'] = '' #will be specified by user
htmlContainer['color'] = '' #will be specified by user
htmlContainer['edge_color'] = '' #will be specified by user
htmlContainer['revealNode'] = '' #will be specified by user
htmlContainer['revealLink'] = '' #will be specified by user
htmlContainer['end js parameters'] = '' #will be specified by user


htmlContainer['d3functions'] = """
<script>
d3.select("body").select("#title")
    .append("h2").html('<center>'+SVGTitle+'</center>')
    .style("color", "#5C5C5C")
    
var removeReveal = function(d){
    d3.select("body").select("#reveal").selectAll("p")
        .transition()
        .duration(hoverOverTime)
        .style("opacity", 0)
        .remove();
    };
    
var nodesize = 4
    nodestroke = 0.4
    nodestrokecolor = "grey"
    
var width = document.getElementById("hive").offsetWidth
    height = document.getElementById("hive").offsetHeight
    innerRadius = 40,
    outerRadius = 240;

var linkfill = "none"
    linkwidth = 1.3
    oplink = 0.9
    opnode = 0.6
    bkgcolor = "white"

var hoverOverTime = 900

var radius = d3.scale.linear().range([innerRadius, outerRadius]);

var angles = d3.scale.ordinal()
    .domain(d3.range(num_axis))
    .range(angle);

var link_color = d3.scale.linear()
    .domain(d3.range(0,edge_color.length,1.0))
    .range(edge_color);

var svg = d3.select("body").select("#container").select("#hive").append("svg")
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
    .style("stroke", function(d) {
        if (edge_color.length == 1){
            return edge_color}
        else {return link_color(d.type)}
        })
    .style("stroke-width", linkwidth)
    .on("mouseover", function(d){
            revealLink(d, d3.select(this).style("stroke"));
            d3.select(this)
                .style("stroke-opacity", 1)
                .style("stroke-width", linkwidth*2)})
    .on("mouseout", function(d){
            removeReveal();
            d3.select(this)
                .transition()
                .duration(800)
                .style("stroke-opacity", oplink)
                .style("stroke-width", linkwidth)});
  
svg.selectAll(".node")
    .data(nodes)
  .enter().append("circle")
    .attr("class", "node")
    .attr("transform", function(d) { return "rotate(" + degrees(angles(d.axis)) + ")"; })
    .attr("cx", function(d) { return radius(d.pos); })
    .attr("r", nodesize)
    .attr("stroke-width", nodestroke)
    .attr("stroke", nodestrokecolor)
    .style("fill-opacity", opnode)
    .style("fill", nodecolor)
    .on("mouseover", function(d){
            d3.select(this)
                .style("fill-opacity", 1)
                .attr("stroke-width", nodestroke*3)
                .attr("stroke", 'black')
                .attr("r", nodesize*1.5) 
               revealNode(d, d3.select(this).style("fill"));
            d3.selectAll(".node")
                .transition()
                .duration(hoverOverTime*0.2)
                .style("fill-opacity", function(n){
                    if (n.name == d.name){
                        return 1}
                    else {
                        return opnode}
                })
                .style("stroke-width", function(n){
                    if (n.name == d.name){
                        return nodestroke*3}
                    else {
                        return nodestroke}
                })
                .attr("stroke", function(n){
                    if (n.name == d.name){
                        return 'black'}
                    else {
                        return nodestrokecolor}
                })
                .attr("r", function(n){
                    if (n.name == d.name){
                        return nodesize*1.5}
                    else {
                        return nodesize}
                })
            d3.selectAll(".link")
                .transition()
                .delay(hoverOverTime*0.1)
                .duration(hoverOverTime*0.2)
                .style("stroke-opacity", function(l){
                    if (l.source.name == d.name || l.target.name == d.name){
                        return 1}
                    else {
                        return oplink}
                })
                .style("stroke-width", function(l){
                    if (l.source.name == d.name || l.target.name == d.name){
                        return linkwidth*2.5}
                    else {
                        return linkwidth}
                })
            })
    .on("mouseout", function(d){
            d3.select(this)
                .transition()
                .duration(hoverOverTime)
                .style("fill-opacity", opnode)
                .attr("stroke-width", nodestroke)
                .attr("stroke", nodestrokecolor)
                .attr("r", nodesize);
            removeReveal();
            d3.selectAll(".link")
                .transition()
                .duration(hoverOverTime)
                .style("stroke-opacity", oplink)
                .style("stroke-width", linkwidth)
            d3.selectAll(".node")
                .transition()
                .duration(hoverOverTime)
                .attr("r", nodesize)
                .attr("stroke-width", nodestroke)
                .attr("stroke", nodestrokecolor)
                .style("fill-opacity", opnode)
            });

function degrees(radians) {
  return radians / Math.PI * 180 - 90;
}
</script>
</body>
</html>
"""

#more to be added

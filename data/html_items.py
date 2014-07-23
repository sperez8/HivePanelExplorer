'''
created 06/05/2014

by sperez

contains all the pieces of the html and d3 functions to plot the hive
'''

htmlContainer= {}

keyOrder = ['intro', 'nodefile', 'edgefile',
            'start js parameters','titleheader',
            'numAxes', 'angles','color', 'edge_color', 
            'end js parameters', 'd3functions']

htmlContainer['intro'] = """<!comment This is a hive plot developed using HivePlotter.>
<!DOCTYPE html>
<meta charset="utf-8">
<body>
<script src="http://d3js.org/d3.v3.min.js"></script>
<script src="http://d3js.org/d3.hive.v0.min.js"></script>
<div id="hive" style="height:500px;width:600px;float:left;"></div>
"""

htmlContainer['nodefile'] = 'nodes.js' #will be specified by user
htmlContainer['edgefile'] = 'links.js' #will be specified by user

htmlContainer['start js parameters'] = '' #will be specified by user
htmlContainer['titleheader'] = '' #will be specified by user
htmlContainer['numAxes'] = '' #will be specified by user
htmlContainer['angles'] = '' #will be specified by user
htmlContainer['color'] = '' #will be specified by user
htmlContainer['edge_color'] = '' #will be specified by user
htmlContainer['end js parameters'] = '' #will be specified by user


htmlContainer['d3functions'] = """
<script>

var nodesize = 4
    nodestroke = 0.4
    nodestrokecolor = "grey"
    
var width = 600
    height = 500
    innerRadius = 40,
    outerRadius = 240;

var linkfill = "none"
    linkwidth = 1.2
    oplink = 0.9
    opnode = 0.6
    bkgcolor = "white"
    
var radius = d3.scale.linear().range([innerRadius, outerRadius]);

var angles = d3.scale.ordinal()
    .domain(d3.range(num_axis))
    .range(angle);

var link_color = d3.scale.linear()
    .domain(d3.range(0,edge_color.length,1.0))
    .range(edge_color);

var printName = function(pos){
        d3.select("body").select("p").text(pos)
    };

var svg = d3.select("body").select("div").append("svg")
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
            d3.select(this)
                .style("stroke-opacity", 1)
                .style("stroke-width", linkwidth*2)})
    .on("mouseout", function(d){
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
//             var cxPos = parseFloat(d3.select(this).attr("x"))        
//             var transPos = parseFloat(d3.select(this).attr("transform"))
//             svg.append("text")
//                 .attr("id", "tooltip")
//                 .attr("cx", cxPos)
//                 .attr("transform", transPos)
//                 .attr("r", nodesize)
//                 .text(d.pos);
            })
    .on("mouseout", function(d){
            d3.select(this)
                .transition()
                .duration(800)
                .style("fill-opacity", opnode)
                .attr("stroke-width", nodestroke)
                .attr("stroke", nodestrokecolor)
                .attr("r", nodesize);
            })
    .on("click", function(d){
        printName(d.pos);
    })
       .append("title").text(function(d){
            return "Position: " + d.pos;
    });

function degrees(radians) {
  return radians / Math.PI * 180 - 90;
}
</script>

<p id="print area" style="background-color:#EEEEEE;height:500px;width:300px;float:left;"></p>
</body>
</html>
"""

#more to be added

'''
created 06/05/2014

by sperez

contains all the pieces of the html and d3 functions to plot the hive
'''

htmlDoc = """<!comment This is a hive plot developed using HivePlotter.>
<!DOCTYPE html>
<meta charset="utf-8">
<body>
<script src="http://d3js.org/d3.v3.min.js"></script>
<script src="http://d3js.org/d3.hive.v0.min.js"></script>
<div id="container" style="width:{16}px">
<div id="title" style="height:70px;width:550px;float:left;"></div>
<div id="rules" style="height:200px;width:450px;float:right;border-bottom:2px solid #5C5C5C"></div>
<div id="hive" style="height:{17}px;width:{17}px;float:left;"></div>
<div id="reveal" style="height:60px;width:450px;float:left;"></div></div>

<script src="{0}"></script>
<script src="{1}"></script>
<script>
//All the user defined parameters

var SVGTitle = 'Hive plot : ' + '{2}'

var colorNeutral = '{3}'

var num_axis = {4}

var angle = {5}

var nodeColor = '{6}'
    edgeColor = {7}
    linkwidth = {13}
    oplink = {14}
    opnode = {15}

var revealNode = function(d,color){{
    d3.select("body").select("#reveal").append("p")
        .html({8})
        .style("color", color)
    }};
var revealLink = function(d,color){{
    d3.select("body").select("#reveal").append("p")
        .html({9})
        .style("color", color)
    }};

d3.select("body").select("#rules")
    .append("p")
    .html('<br><br>Node assignment property: ' + '{10}' + '<br><br>Node positioning property: ' + '{11}' + '<br><br>Edge coloring property: ' + '{12}') 
    .style("color", colorNeutral)

d3.select("body").select("#title")
    .append("h2").html('<center>'+SVGTitle+'</center>')
    .style("color", colorNeutral)
    
var removeReveal = function(d){{
    d3.select("body").select("#reveal").selectAll("p")
        .transition()
        .duration(hoverOverTime)
        .style("opacity", 0)
        .remove();
    }};
    
var nodesize = 4
    nodestroke = 0.4
    nodestrokecolor = "grey"
    
var width = document.getElementById("hive").offsetWidth
    height = document.getElementById("hive").offsetHeight
    innerRadius = 40,
    outerRadius = width*0.4;

var linkfill = "none"
    bkgcolor = "white"

var hoverOverTime = 900

var radius = d3.scale.linear().range([innerRadius, outerRadius]);

var angles = d3.scale.ordinal()
    .domain(d3.range(num_axis))
    .range(angle);

var link_color = d3.scale.linear()
    .domain(d3.range(0,edgeColor.length,1.0))
    .range(edgeColor);

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
    .attr("transform", function(d) {{ return "rotate(" + degrees(angles(d)) + ")"; }})
    .attr("x1", radius.range()[0])
    .attr("x2", radius.range()[1])
    .attr("stroke-width",0.7)
    .attr("stroke", "black");

svg.selectAll(".link")
    .data(links)
  .enter().append("path")
    .attr("class", "link")
    .attr("d", d3.hive.link()
    .angle(function(d) {{ return angles(d.axis); }})
    .radius(function(d) {{ return radius(d.pos); }}))
    .style("fill", linkfill)
    .style("stroke-opacity", oplink)
    .style("stroke", function(d) {{
        if (edgeColor.length == 1){{
            return edgeColor}}
        else {{return link_color(d.type)}}
        }})
    .style("stroke-width", linkwidth)
    .on("mouseover", function(d){{
            revealLink(d, d3.select(this).style("stroke"));
            d3.select(this)
                .style("stroke-opacity", 1)
                .style("stroke-width", linkwidth*2)}})
    .on("mouseout", function(d){{
            removeReveal();
            d3.select(this)
                .transition()
                .duration(800)
                .style("stroke-opacity", oplink)
                .style("stroke-width", linkwidth)}});
  
svg.selectAll(".node")
    .data(nodes)
  .enter().append("circle")
    .attr("class", "node")
    .attr("transform", function(d) {{ return "rotate(" + degrees(angles(d.axis)) + ")"; }})
    .attr("cx", function(d) {{ return radius(d.pos); }})
    .attr("r", nodesize)
    .attr("stroke-width", nodestroke)
    .attr("stroke", nodestrokecolor)
    .style("fill-opacity", opnode)
    .style("fill", nodeColor)
    .on("mouseover", function(d){{
            d3.select(this)
                .style("fill-opacity", 1)
                .attr("stroke-width", nodestroke*3)
                .attr("stroke", 'black')
                .attr("r", nodesize*1.5) 
               revealNode(d, d3.select(this).style("fill"));
            d3.selectAll(".node")
                .transition()
                .duration(hoverOverTime*0.2)
                .style("fill-opacity", function(n){{
                    if (n.name == d.name){{
                        return 1}}
                    else {{
                        return opnode}}
                }})
                .style("stroke-width", function(n){{
                    if (n.name == d.name){{
                        return nodestroke*3}}
                    else {{
                        return nodestroke}}
                }})
                .attr("stroke", function(n){{
                    if (n.name == d.name){{
                        return 'black'}}
                    else {{
                        return nodestrokecolor}}
                }})
                .attr("r", function(n){{
                    if (n.name == d.name){{
                        return nodesize*1.5}}
                    else {{
                        return nodesize}}
                }})
            d3.selectAll(".link")
                .transition()
                .delay(hoverOverTime*0.1)
                .duration(hoverOverTime*0.2)
                .style("stroke-opacity", function(l){{
                    if (l.source.name == d.name || l.target.name == d.name){{
                        return 1}}
                    else {{
                        return oplink}}
                }})
                .style("stroke-width", function(l){{
                    if (l.source.name == d.name || l.target.name == d.name){{
                        return linkwidth*2.5}}
                    else {{
                        return linkwidth}}
                }})
            }})
    .on("mouseout", function(d){{
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
            }});

function degrees(radians) {{
  return radians / Math.PI * 180 - 90;
}}
</script>
</body>
</html>
"""

#the panel


htmlDocPanel = """<!comment This is a hive panel developed using HivePlotter.>
<!DOCTYPE html>
<meta charset="utf-8">
<body>
<script src="http://d3js.org/d3.v3.min.js"></script>
<script src="http://d3js.org/d3.hive.v0.min.js"></script>
<div id="container" style="width:100%;min-width:{16}">
<div id="title" style="height:70px;width:550px;float:left;"></div>
<div id="panel" style="height:{17}px;width:{17}px;float:left;"></div>
<div id="rules" style="height:200px;width:450px;float:right;border-bottom:2px solid #5C5C5C"></div>
<div id="reveal" style="height:60px;width:450px;float:left;"></div></div>

<script src="{0}"></script>
<script src="{1}"></script>
<script>
//All the user defined parameters

var SVGTitle = 'Hive Panel : ' + '{2}'

var colorNeutral = '{3}'

var num_axis = {4}

var angle = {5}

var nodeColor = '{6}'
    edgeColor = {7}
    linkwidth = {13}
    oplink = {14}
    opnode = {15}

var revealNode = function(d,color){{
    d3.select("body").select("#reveal").append("p")
        .html({8})
        .style("color", color)
    }};
var revealLink = function(d,color){{
    d3.select("body").select("#reveal").append("p")
        .html({9})
        .style("color", color)
    }};

d3.select("body").select("#rules")
    .append("p")
    .html('<br><br>Node assignment property: ' + '{10}' + '<br><br>Node positioning property: ' + '{11}' + '<br><br>Edge coloring property: ' + '{12}') 
    .style("color", colorNeutral)

d3.select("body").select("#title")
    .append("h2").html('<center>'+SVGTitle+'</center>')
    .style("color", colorNeutral)
    
var removeReveal = function(d){{
    d3.select("body").select("#reveal").selectAll("p")
        .transition()
        .duration(hoverOverTime)
        .style("opacity", 0)
        .remove();
    }};
    
var nodesize = 4
    nodestroke = 0.4
    nodestrokecolor = "grey"
    
var width = document.getElementById("panel").offsetWidth
    height = document.getElementById("panel").offsetHeight

var linkfill = "none"
    bkgcolor = "white"

var hoverOverTime = 900

var angles = d3.scale.ordinal()
    .domain(d3.range(num_axis))
    .range(angle);

var link_color = d3.scale.linear()
    .domain(d3.range(0,edgeColor.length,1.0))
    .range(edgeColor);
    
//Where the panel fun begins
padding = 130;
panels = {20}
size = width/panels

var svg = d3.select("body").select("#container").select("#panel").append("svg")
    .attr("class", SVGTitle)
    .attr("width", width)
    .attr("height", width)
    .style("background-color", bkgcolor)
  .append("g")
    .attr("transform", "translate(" + padding + "," + padding + ")");
 
var rowtraits = {18};
var columntraits = {19};

function cross(a, b){{
    var c = [], n = a.length, m = b.length, i, j;
    for (i = -1; ++i < n;) for (j = -1; ++j < m;) c.push({{x: a[i]+'_axis', i: i, y: b[j] + '_pos', j: j}});
    return c;
}};

var cell = svg.selectAll(".cell")
  .data(cross(rowtraits,columntraits))
.enter().append("g")
  .attr("class", "cell")
  .attr("transform", function(d) {{ return "translate(" + (panels - d.i - 1) * size + "," + d.j * size + ")"; }})
  .each(plot);
  
function plot(p){{
    var cell = d3.select(this);

    var innerRadius = size*0.05
    var outerRadius = size*0.45
    var radius = d3.scale.linear().range([innerRadius, outerRadius]);

    cell.selectAll(".axis")
        .data(angle)
      .enter().append("line")
        .attr("class", "axis")
        .attr("transform", function(d) {{ return "rotate(" + degrees(angles(d)) + ")"; }})
        .attr("x1", radius.range()[0])
        .attr("x2", radius.range()[1])
        .attr("stroke-width",0.7)
        .attr("stroke", "black");

    cell.selectAll(".link")
        .data(links)
      .enter().append("path")
        .attr("class", "link")
        .attr("d", d3.hive.link()
        .angle(function(d) {{ return angles(d[p.x]); }})
        .radius(function(d) {{ return radius(d[p.y]); }}))
        .attr("show", function (d) {{
            if (d.source[p.x] == d.target[p.x]) {{return false}}
            else {{return true}}
        }})
        .style("fill", linkfill)
        .style("stroke-opacity", oplink)
        .style("stroke", function(d) {{
            if (edgeColor.length == 1){{
                return edgeColor}}
            else {{return link_color(d.type)}}
            }})
        .style("stroke-width", linkwidth)
        .on("mouseover", function(d){{
                revealLink(d, d3.select(this).style("stroke"));
                d3.select(this)
                    .style("stroke-opacity", 1)
                    .style("stroke-width", linkwidth*2)}})
        .on("mouseout", function(d){{
                removeReveal();
                d3.select(this)
                    .transition()
                    .duration(800)
                    .style("stroke-opacity", oplink)
                    .style("stroke-width", linkwidth)}});
    
    //removes any edges between nodes on same axis.
    cell.selectAll("path[show="+false+"]").remove()

    cell.selectAll(".node")
        .data(nodes)
      .enter().append("circle")
        .attr("class", "node")
        .attr("transform", function(d) {{ return "rotate(" + degrees(angles(d[p.x])) + ")"; }})
        .attr("cx", function(d) {{ return radius(d[p.y]); }})
        .attr("r", nodesize)
        .attr("stroke-width", nodestroke)
        .attr("stroke", nodestrokecolor)
        .style("fill-opacity", opnode)
        .style("fill", nodeColor)
        .on("mouseover", function(d){{
                d3.select(this)
                    .style("fill-opacity", 1)
                    .attr("stroke-width", nodestroke*3)
                    .attr("stroke", 'black')
                    .attr("r", nodesize*1.5) 
                   revealNode(d, d3.select(this).style("fill"));
                d3.selectAll(".node")
                    .transition()
                    .duration(hoverOverTime*0.2)
                    .style("fill-opacity", function(n){{
                        if (n.name == d.name){{
                            return 1}}
                        else {{
                            return opnode}}
                    }})
                    .style("stroke-width", function(n){{
                        if (n.name == d.name){{
                            return nodestroke*3}}
                        else {{
                            return nodestroke}}
                    }})
                    .attr("stroke", function(n){{
                        if (n.name == d.name){{
                            return 'black'}}
                        else {{
                            return nodestrokecolor}}
                    }})
                    .attr("r", function(n){{
                        if (n.name == d.name){{
                            return nodesize*1.5}}
                        else {{
                            return nodesize}}
                    }})
                d3.selectAll(".link")
                    .transition()
                    .delay(hoverOverTime*0.1)
                    .duration(hoverOverTime*0.2)
                    .style("stroke-opacity", function(l){{
                        if (l.source.name == d.name || l.target.name == d.name){{
                            return 1}}
                        else {{
                            return oplink}}
                    }})
                    .style("stroke-width", function(l){{
                        if (l.source.name == d.name || l.target.name == d.name){{
                            return linkwidth*2.5}}
                        else {{
                            return linkwidth}}
                    }})
                }})
        .on("mouseout", function(d){{
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
                }});
}};


function degrees(radians) {{
  return radians / Math.PI * 180 - 90;
}}
</script>
</body>
</html>
"""

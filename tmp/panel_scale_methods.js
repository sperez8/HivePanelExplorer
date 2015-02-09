  // ****************************************** //


 //         WEB PAGE LAYOUT PARAMETERS         //


// ****************************************** //

//display title of panel and number of nodes and links
d3.select("body").select("#title").select("#thetitle")
    .html(SVGTitle)

N = nodes.length
E = links.length
d3.select("body").select("#title").select("#info")
    .html(N+' nodes, '+E+' edges')

  // ****************************************** //


 //       ASSIGNMENT AND POSITION SCALES       //


// ****************************************** //

//get the angles of the axis depending on the number of axes and if they are doubled or not
var angle = get_angles(numAxes,doubleAxes)

//if doubled axes are requested, then we need to bind twice the amount of DOM elements from the nodes{} and links{} datasets
if (doubleAxes){
    var seriesLinksNames = [0,1]
    var seriesNodesNames = [0,1]
    var angleRange = d3.range(numAxes*2)
} else {
    var seriesLinksNames = [0]
    var seriesNodesNames = [0]
    var angleRange = d3.range(numAxes)
};

//scale to assign an axis number to an angle
var angles = d3.scale.ordinal()
    .domain(angleRange)
    .range(angle);

var asgScales = {};
    posScales = {};

//get witdh of the "panel" div and the number of traits to figure out the number of hive plots and their size in the panel
var width = document.getElementById("panel").offsetWidth
    height = width
    padding = width*0.06;
    legend_padding = padding/4
    panels = Math.max(columntraits.length, rowtraits.length)
    size = (width-padding-legend_padding)/panels
    num_panels = columntraits.length*rowtraits.length
    //console.log(width, height, padding, size)

//returns numerical thresholds to bin log scaled node assignment data into the number of axes required.
function log_thresholds(min,max){
    span = Math.abs(max-min)
    t = d3.range(Math.log(1),Math.log(span+1),Math.log(span+1)/numAxes)
    k = []
    for (var i = 1; i < numAxes; i++) {
        if (max<=0 && min <=0){
            k.push(-Math.exp(t[i])+1)
        } else{
            k.push(Math.exp(t[i])-1)
        }
    };
    if (max<=0 && min <=0){k.reverse()}
    return k
}


//ensures a numercial, and not an alphabetical sort
function sortNumber(a,b) {
    return a - b;
}

function get_trait_values(trait){
    return nodes.map(function (d) {return Number(d[trait])})
}

//returns numerical thresholds to bin node assignment data into about equally sized bins.
function even_thresholds(trait){
    data = get_trait_values(trait)
    total = data.length
    data.sort(sortNumber)
    k = []
    for (var i = 1; i < numAxes; i++) {
        index = parseInt(total*i/numAxes)
        k.push(data[index]+ 0.000000000000001) //add arbitrarily small value to ensure that, when binning integer values, all axes are populated.
    };
    k = k.sort(sortNumber)
    return k
}

function zip(arrays) {
    return Array.apply(null,Array(arrays[0].length)).map(function (_,i){
        return arrays.map(function (array){return array[i]})
    });
}

function make_rank_scale(trait){
    rankScale = [];
    data = get_trait_values(trait)
    total = data.length
    
    indices = Array.apply(null, Array(total)).map(function (_, i) {return i;});
    both = zip([data,indices])

    both.sort(function (a, b) {
        a = a[0];
        b = b[0];

        return a < b ? -1 : (a > b ? 1 : 0);
    });

    for (var i = 0; i < both.length; i++) {
        var datum = both[i][0];
        var ind = both[i][1];

        rankScale[ind] = i/parseFloat(both.length-1)
    }
    return rankScale
}


// get the columntraits used for node assignment onto axes and build the desired linear, log 
//or evenly distributed scales to use later when plotting nodes and links
console.log('\nAssignment values for grouping of nodes on axes:')
for (var i in columntraits) {
    trait = columntraits[i];
    categorical = !check_quantitative([nodes[0][trait]]) //check if trait is a qualitative or categorical attribute
    if (categorical){
        keys = get_categories(trait)
        asgScales[trait] = d3.scale.ordinal()
            .domain(keys)
            .range(d3.range(numAxes));
        console.log('Categorical trait', trait, 'has categories: ', keys)
        columnTraitScales[trait]="categorical"
    } else {
        max = d3.max(nodes, function(d) {
            return Number(d[trait])});
        min = d3.min(nodes, function(d) {
            return Number(d[trait])});
        type = 'linear'
        if (columnTraitScales[i]=="even"){
            t = even_thresholds(trait)
            asgScales[trait+String(i)] = d3.scale.threshold()
                    .domain(t)
                    .range(d3.range(numAxes))
            type = "even-distribution"
        }
        else if (columnTraitScales[i]=="log" && ((max>=0&&min>=0 ) || (max<=0&&min<=0)) ){
            t = log_thresholds(min,max)
            asgScales[trait+String(i)] = d3.scale.threshold()
                                .domain(t)
                                .range(d3.range(numAxes))
            type = 'log'
        } else {
            asgScales[trait+String(i)] = d3.scale.quantile()
                                .domain([min,max])
                                .range(d3.range(numAxes));
        }
        console.log('Quantitative trait', trait+String(i), 'has a', type, 'scale, and cut offs: ')
        for (var j = 0;j <= numAxes-1;j++) {
            console.log('\t axis', j, asgScales[trait+String(i)].invertExtent(j))
        };
    }
}


// get the rowtraits used for node positionning on axes and build the desired linear orlog 
//scales to use later when plotting nodes and links
console.log('\nScaled values for positioning of nodes onto axes:')
for (var i in rowtraits) {
    trait = rowtraits[i];
    categorical = !check_quantitative([nodes[0][trait]])  //check if trait is a qualitative or categorical attribute
    if (categorical){
        keys = get_categories(trait)
        posScales[trait] = d3.scale.ordinal()
            .domain(keys)
            .rangeBands([0, 1], 1.0/keys.length/3);
        console.log('Categorical trait', trait, 'has categories: ', keys)
        rowTraitScales[trait]=="categorical"
    } else {
        max = d3.max(nodes, function(d) {
            return Number(d[trait])});
        min = d3.min(nodes, function(d) {
            return Number(d[trait])});
        type = 'linear' 

        if (rowTraitScales[i]=="rank"){
            type = 'rank'            
            rankScale = make_rank_scale(trait)
            posScales[trait] = rankScale

        } else if (rowTraitScales[i]=="log"){
            if ((max > 0 && min > 0)||(max < 0 && min < 0)){
                type = 'log'
                posScales[trait+String(i)] = d3.scale.log()
                                        .domain([min,max])
                                        .range([0, 1])
            } else if (max > 0 && min == 0){
                type = 'log'
                posScales[trait+String(i)] = logspecial()
                                        .domain([min,max])
                                        .range([0, 1])
            } else if (max == 0 && min < 0){ 
                type = 'log'
                posScales[trait+String(i)] = logspecial(false)
                                        .domain([min,max])
                                        .range([0, 1])
            } else {
                posScales[trait+String(i)] = d3.scale.linear()
                                    .domain([min,max])
                                    .range([0, 1]);
            }
        } else {
            posScales[trait+String(i)] = d3.scale.linear()
                                    .domain([min,max])
                                    .range([0, 1]);
        }
        console.log('Quantitative trait', trait+String(i), 'has', type, 'scale with min and max value: ', min, ',', max)
    }
}

//create all combinations of node assignment and position rules
function cross(a, b){
    var c = [], n = a.length, m = b.length, i, j;
    for (i = -1;++i < n;) for (j = -1;++j < m;) c.push({x: a[i], i: i, y: b[j], j: j});
    return c;

};

  // ****************************************** //


 //          MAKING THE SVG AND HIVES          //


// ****************************************** //

//default behaviour of tool tip
var tooltip = d3.select("body").append("div")   
    .attr("class", "tooltip")               
    .style("opacity", 0);

var tooltipOpacity = 0.7

//create a timer so that mouseover events are called successively
//to speed up animation.
var hoverTimer

//delay for hover animations
var hoverDelay = 5 //milliseconds

function clearHoverTimer() {
    clearTimeout(hoverTimer)
}

var highlightTime = 500 //milliseconds

//create svg drawing without the "#oanel" 
var svg = d3.select("body").select("#container").select("#panel").append("svg")
    .attr("class", SVGTitle)
    .attr("width", width)
    .attr("height", width)
    .style("background-color", bkgcolor)
  .append("g")
    .attr("transform", "translate(" + (size/2 + padding) + "," + (size/2 + padding) + ")");//(0,0) coordinates correspond to the center of the first hive.

//add labels for column and row rules
svg.append("text")
    .attr("x", (width - padding - size)/2)
    .attr("y", -(size/2 + padding*3/4))
    .attr("text-anchor", "middle")
    .attr("class","legend")
    .text('A X I S   A S S I G N M E N T') //add name of property used for node positionning, the rowtrait

svg.append("text")
    .attr("x", -(width - padding - size)/2)
    .attr("y", -(size/2 + padding*3/4))
    .attr("text-anchor", "middle")
    .attr("class","legend")
    .text('A X I S   P O S I T I O N') //add name of property used for node positionning, the rowtrait
    .attr("transform", function(d) { 
        return "rotate(-90)";
        })

//each cell contains a hive plot and is characterized by a node assignment rule (columnttrait) and a node positionning rule. 
var cell = svg.selectAll(".cell")
  .data(cross(columntraits,rowtraits)) //data is the combination or column and row traits.
.enter().append("g")
  .attr("class", "cell")
  .attr("transform", function(d) { return "translate(" + (d.i) * size + "," + d.j * size + ")";})
  .each(plot);
  
//format the labels for axes
function formatAxisLegend(trait,j,axis){
    values = asgScales[trait+String(j)].domain()
    type = columnTraitScales[j]
    //console.log(values, type)

    if (type=="categorical"){
        return values[axis]
    } else {
        range = asgScales[trait+String(j)].invertExtent(axis)
        r0 = Math.round(range[0]*100)/100
        r1 = Math.round(range[1]*100)/100
        if (isNaN(range[0])){return 'x≤'+ r1}
        else if (isNaN(range[1])){return 'x>'+ r0}
        else {return r0+'<x≤'+r1}
        }
}

//build each hive plot
function plot(p){
    var cell = d3.select(this);

    //calculate the slength and position of each axes depending on the size of the hive plot.
    var innerRadius = size*0.03
    var outerRadius = size*0.46
    var radius = d3.scale.linear().range([innerRadius, outerRadius]);

    //column labels (when one plotting first row, where p.i=0)
    if (p.i == 0){
    cell.append("text")
        .attr("x", function(d) { return d.i})
        .attr("y", function(d) { return d.j-size/2 -padding/2})
        .attr("text-anchor", "middle")
        .attr("class","viztext")
        .text(capitalize(p.y)) //add name of property used for node positionning, the rowtrait
        .attr("transform", function(d) { 
            return "rotate(-90)";
            })
    }

    //column labels (when one plotting first column, where p.j=0)
    if (p.j==0){
    cell.append("text")
        .attr("x", function(d) { return d.i;})
        .attr("y", function(d) { return d.j-size/2 - padding/2;})
        .attr("text-anchor", "middle")
        .attr("class","viztext")
        .text(capitalize(p.x)) //add name of property used for node assignment, the columntrait

    }

    //creates axis labels
    //some parameters
    var outer_radius = radius.range()[1]*1.05
        x_shift = 50
        y_shift = 45
        stagger = 0

    cell.selectAll(".axis")
        .data(angle)
      .enter().append("text")
        .attr("transform", function(d,i) {
            if (!doubleAxes){
                a = angles(d)
            } else if (i % 2 == 0) {
                a = get_angles(numAxes, false)[i/2]
            } else {a = 0}
            theta = a-Math.PI
            h = outer_radius
            y = h*Math.cos(theta)
            x = -h*Math.sin(theta)
            if (x>20){x = x-x_shift} else if (x<-20) {x = x+x_shift}
            if (y>30){
                console.log(theta, x, y, stagger)
                y = y+y_shift+stagger

                stagger = -stagger
            }
            //console.log(theta, x, y, stagger)
            return "translate("+x+","+y+")";
        })
        .attr("class","legend")
        .attr("text-anchor", function(d,i) {
            if (!doubleAxes){
                a = angles(d)
            } else if (i % 2 == 0) {
                a = get_angles(numAxes, false)[i/2]
            } else {a = 0}
            theta = a-Math.PI
            h = outer_radius
            y = h*Math.cos(theta)
            x = -h*Math.sin(theta)

            if (x>60){
                return "start"
            } else if (x<-60) {
                return "end"
            } else {
                return "middle"
            }
        })
        .text(function(d,k) {
            if (!doubleAxes){return formatAxisLegend(p.x,String(p.i),k)}
            else if (k % 2 == 0){return formatAxisLegend(p.x,String(p.i),k/2)}
            else {return ''}
        })

    //build axes
    cell.selectAll(".axis")
        .data(angle)
      .enter().append("line")
        .attr("class", "axis")
        .attr("transform", function(d) { return "rotate(" + degrees(angles(d)) + ")";})
        .attr("x1", radius.range()[0])
        .attr("x2", radius.range()[1])
        .attr("stroke-width",0.7)
        .attr("stroke", "black");

    //seriesLinks reflects the fact that double axes are being plotted.
    var seriesLinks = cell.selectAll(".seriesLinks")
                        .data(seriesLinksNames)
                      .enter().append("g")
                        .attr("class", "seriesLinks")
                        .each(hiveLinks);

    //plot links as paths between nodes
    function hiveLinks(h){
        var axesType = d3.select(this);
        var isSource = true

        axesType.selectAll(".link")
            .data(links)
          .enter().append("path")
            .attr("class", "link")
            .attr("d", d3.hive.link() //use Mbostocks hive plot library
                .angle(function(d) {
                    if (!doubleAxes){
                        a = angles(asgScales[p.x+String(p.i)](d[p.x]))
                    } else if (isSource){ //keep track of source and target to make link
                        a = angles(asgScales[p.x+String(p.i)](d[p.x]*2+h)) //on h==0, want the source to be on the 1st axis but on h==1 we want the source to become the target
                        isSource = false
                    } else {
                        a = angles(asgScales[p.x+String(p.i)](d[p.x]*2+1-h))
                        isSource = true
                    }
                    return a
                })
                .radius(function (l) {
                    if (rowTraitScales[p.j]=="rank"){
                        return radius(rankScale[nodes.indexOf(l)])
                    } else {
                        return radius(posScales[p.y+String(p.j)](l[p.y])) //pos
                    }
                })
            )            
            .attr("show", function (l) { //the 'show' attribute is false when links are between nodes on the same axes
                //or when the link connects nodes that are not on neighboring axes and cross over a third axes.
                s = asgScales[p.x+String(p.i)](l.source[p.x])
                t = asgScales[p.x+String(p.i)](l.target[p.x])
                if (!doubleAxes){
                    if (t == s) {
                        return false
                    } else if (numAxes > 3 && Math.abs(s-t) >1 ) {
                        return false
                    } else {
                        return true}
                } else {
                    s = s*2+h
                    t = t*2+1-h
                    if (h==0){
                        if (t+1 == s) { //from one axes group to another
                            show = true
                        } else if (s+1 == t) { //within doubled axes link
                            show = true
                        }  else if (t==numAxes*2-1 && s==0) {
                            show = true
                        } else {
                            show = false
                        }
                    } else if (h==1){ //the second time around, the source plays the role of the target and vice versa
                        if (t+1 == s) {
                            show = true
                        }
                        else if (s+1 == t) {
                            show = true
                        }
                        else if (s==numAxes*2-1 && t==0) {
                            show = true
                        } else {
                            show = false
                        }
                    }
                    return show
                }
            })
            .style("fill", linkfill) //linkfill is "none" so that only the arc of the path is seen.
            .style("stroke-opacity", oplink)
            .style("stroke", function(l) {
                if (edgeColor){
                return edgeColor} else {
                    return "grey"
                }
            })
            .style("stroke-width", linkwidth)
            .classed({"clicked":false})
            .on("click", function(){
                if (d3.select(this).classed("clicked")){
                    d3.select(this)
                        .classed({"clicked":false})
                    link_mouseout()
                    node_mouseout()
                    removeReveal()
                } else {
                    d3.select(this)
                        .classed({"clicked":true})
                        .call(link_full_reveal,d,d.source.name, d.target.name)
                }
            })
            .on("mouseover", function(l){
                var link = d3.select(this)
                var cx = d3.event.pageX
                var cy = d3.event.pageY

                hoverTimer = setTimeout(function(){
                        link_tooltip(cx, cy, l, l.source.name, l.target.name);
                        //link.call(highlight_links)  //not responsive because manipulating the DOM is expensive.
                    }, hoverDelay)
            })
            .on("mouseout", function(){
                clearHoverTimer()
                remove_tooltip()
                //if (!d3.select(this).classed("clicked")){
                //    d3.select(this).call(link_mouseout)
                //}
            });

        //removes any edges between nodes on same axis.
        axesType.selectAll("path[show="+false+"]").remove()

        };

    var seriesNodes = cell.selectAll(".seriesNodes")
                    .data(seriesLinksNames)
                  .enter().append("g")
                    .attr("class", "seriesNodes")
                    .each(hiveNodes);

    //plot nodes second so they appear on top of links
    function hiveNodes(h){
        var axesType = d3.select(this);
        axesType.selectAll(".node")
            .data(nodes)
          .enter().append("circle")
            .attr("class", "node")
            .attr("transform", function(d) { 
                if (doubleAxes){ //plot nodes of even axes when h=0 then on odd axes when h=1
                    return "rotate(" + degrees(angles(asgScales[p.x+String(p.i)](d[p.x]*2 + h))) + ")"  
                } else {
                    return "rotate(" + degrees(angles(asgScales[p.x+String(p.i)](d[p.x]))) + ")"
               }
            })

            .attr("cx", function (d) {
                //console.log(d.name, p.y, d[p.y], posScales[p.y+String(p.j)](d[p.y]))
                if (rowTraitScales[p.j]=="rank"){
                    return radius(rankScale[nodes.indexOf(d)])
                } else {
                    return radius(posScales[p.y+String(p.j)](d[p.y])) //pos
                }
            })
            .attr("r", nodesize)
            .attr("stroke-width", nodestroke)
            .attr("stroke", nodestrokecolor)
            .style("fill-opacity", opnode)
            .style("fill", function(d) { 
                return nodeColor
            })
            .classed({"clicked":false})
            .on("click", function(d){
                if (d3.select(this).classed("clicked")){
                    d3.select(this).classed({"clicked":false})
                    node_mouseout()
                    link_mouseout()
                    removeReveal()
                } else {
                    d3.select(this)
                        .classed({"clicked":true})
                        .call(node_full_reveal,d)
                }
            })
            .on("mouseover", function(d){
                clearHoverTimer()
                //var node = d3.select(this)
                var cx = d3.event.pageX
                var cy = d3.event.pageY

                hoverTimer = setTimeout(function(){
                        node_tooltip(cx, cy, d, p.x, p.y, d[p.x], d[p.y]);
                        //node.call(highlight_nodes) //not responsive because manipulating the DOM is expensive.
                    }, hoverDelay)
            })
            .on("mouseout", function(d){                
                remove_tooltip() 
                clearHoverTimer()
                //if (!d3.select(this).classed("clicked")){
                //    d3.select(this)
                //        .call(node_mouseout)  
                //} 
            })
    };

    };


  // ****************************************** //


 //         SOME DISPLAY FUNCTIONS             //


// ****************************************** //

var node_tooltip = function(cx, cy, d, px, py, x, y){
    if (py!=px){
        text = '<b>' + d.name +'</b><br>'+ px + ': ' + round_value(x) + '<br>' + py + ': ' + round_value(y)
    } else { text = '<b>' + d.name +'</b><br>'+ px + ': ' + round_value(x)}
    tooltip   
        .style("opacity", tooltipOpacity)
        .html(text) 
            .style("height", "45px")
            .style("left", (cx + 5) + "px")     
            .style("top", (cy - 28) + "px");
}


var node_full_reveal = function(node,d) {
    revealNode(d, node.style("fill"))

    d3.selectAll(".node")
        .each(function(n){
            if (n.name == d.name){
                node = d3.select(this)
                node.classed({"clicked":true})
                highlight_nodes(node)
            }
        })
}

/////with queue brocken@!!!!!
/*var node_full_reveal = function(node,d) {
    revealQueue = queue(1)
    revealQueue
        .defer(revealNode, d, node.style("fill"))

    tasks = []
    d3.selectAll(".node")
        .each(function(n){
            if (n.name == d.name){
                node = d3.select(this)
                node.classed({"clicked":true})
                t = []
                t.push(highlight_nodes)
                t.push(node)
                tasks.push(t)
            }
        })
    tasks.forEach(function(t) {console.log(t[1]); revealQueue.defer(t[0], t[1])})
}*/

var node_mouseout = function(node) {
    if (node){
        node
            .transition()
            .duration(hoverOverTime/2)
            .attr("r", nodesize)
            .attr("stroke-width", nodestroke)
            .attr("stroke", nodestrokecolor)
            .style("fill-opacity", function(d,i){
                if (d3.select(this).classed("important")){
                    return opnode_more
                }else{
                    return opnode
                }})
    } else {
        d3.selectAll(".node")
            .transition()
            .duration(hoverOverTime/2)
            .attr("r", nodesize)
            .attr("stroke-width", nodestroke)
            .attr("stroke", nodestrokecolor)
            .style("fill-opacity", function(d,i){
                if (d3.select(this).classed("important")){
                    return opnode_more
                }else{
                    return opnode
                }})
    }
}


var remove_tooltip = function(){
    tooltip.style("opacity", 0);
}

d3.selection.prototype.moveToFront = function() {
  return this.each(function(){
    this.parentNode.appendChild(this);
  });
};

var highlight_nodes = function(selection) {
    selection
        .transition()
        .duration(highlightTime)
        .attr("r", nodesize*1.8)
        .attr("stroke-width", nodestroke*3)
        .attr("stroke", 'black')
        .style("fill-opacity", 1)
    };

var link_full_reveal = function(link,d,source,target) {
    revealLink(d, link.style("stroke"));
    d3.selectAll(".link")
        .each(function(l){
            if (l.source.name == source && l.target.name == target){
                d3.select(this).call(highlight_links)
            }
        })
    d3.selectAll(".node")
        .each(function(n){
            if (n.name == source || n.name == target){
                d3.select(this).call(highlight_nodes)
            }
        })
}

var link_tooltip = function(cx, cy, d, source, target){
    tooltip    
        .style("opacity", tooltipOpacity);
    tooltip.html('source: ' + source + '<br>' + 'target: ' + target)
        .style("height", "32px")
        .style("left", (cx + 5) + "px")     
        .style("top", (cy - 28) + "px");
}

var link_mouseout = function(link) {
    if (link){
        link
            .transition()
            .duration(hoverOverTime)
            .style("stroke-opacity", oplink)
            .style("stroke-width", linkwidth)
    } else {
    d3.selectAll(".link")
        .transition()
        .duration(hoverOverTime)
        .style("stroke-opacity", oplink)
        .style("stroke-width", linkwidth)
    }
}

var highlight_links = function(selection) {
    selection            
        .transition()
        .duration(highlightTime)
        .style("stroke-opacity", 1)
        .style("stroke-width", linkwidth*2)
    };

function make_node_full_reveal_text(node) {
    text = ''
    for (key in node) {
        if (key == 'name'){
            text = text + "<b><big>" + key + ": " + round_value(node[key]) + "</big></b>"
        } else {
            text = text +", <b>"+key+"</b>: " + round_value(node[key])
        }
    };
    return text
}

function make_link_reveal_text(link) {
    text = ''
    for (key in link) {
        if (key == 'source'){
            text = text + "<b><big>" + key + ": " + link[key].name + "</big></b>"
        }
        else if (key == 'target'){
            text = text + ", <b><big>" + key + ": " + link[key].name + "</big></b>"
        } else {
            text = text +", <b>"+key+"</b>: " + link[key]
        }
    };
    return text
}

var revealNode = function(d, color, callback){
    removeReveal()
    d3.select("body").select("#reveal").append("p")
        .html(make_node_full_reveal_text(d))
        .style("color", color)
        .style("background-color", "white")
        .transition()
        .duration(hoverOverTime*2)
        .style("background-color", calculate_brackground(color))
    //callback(null,true)
    };

var revealLink = function(d,color){
    removeReveal()
    d3.select("body").select("#reveal").append("p")
        .html(make_link_reveal_text(d))
        .style("color", color)
    };

var removeReveal = function(){
    d3.select("body").select("#reveal").selectAll("p")
        .remove();
    };

  // ****************************************** //


 //              SEARCH FUNCTIONS              //


// ****************************************** //


function show_node() {
    var node = document.getElementById("lostNode").value
    var revealed = false
    d3.selectAll("circle").each(function(d) {
        if (d['name'] == node) {
            d3.select(this)
                .moveToFront()
                .call(highlight_nodes,true)
            if (!revealed){
                revealNode(d, d3.select(this).style("fill"))
                revealed = true

                //BROCKEN
                // d3.select(this)
                //     .transition()
                //     .delay(1000)
                //     .call(removeReveal)
                }
            }
        })
    };



  // ****************************************** //


 //         CONTROL PANEL FUNCTIONS            //


// ****************************************** //

function remove_options(selector) {
    //first remove all the previous options:
    if (selector.length > 0){
        for (var i = selector.length - 1;i >= 0;i--) {
            selector.remove(i);
        }
    }
    return selector
};

function add_options(selector, data, property){
    options = []
    for (var i = data.length - 1;i >= 0;i--) {
        value = data[i][property]
        if (options.indexOf(value)>=0){}
        else{
            options.push(value)
        }
    }
    quantitative = check_quantitative(options)

    if (quantitative){
        newOptions = []
        for (i in options) {
            newOptions.push(Number(options[i]))
        }
        options = newOptions
        options.sort(sortNumber)
    } else {
        options.sort() //sort in ascending order
    }

    for (i in options) {
        option = document.createElement("option")
        option.text = String(options[i])
        selector.add(option)
    }
    return quantitative
}

function update_properties(sel) {
    ruleNumber = find_rule_number_from_selection(sel)
    make_property_options(ruleNumber)
}

function update_values(sel) {
    ruleNumber = find_rule_number_from_selection(sel)
    make_value_options(ruleNumber)
}

function find_rule_number_from_selection(sel) {
    if (sel) {
        ruleNumber = sel.id.slice(-1)
        if (ruleNumber == parseInt(ruleNumber)){
            return ruleNumber
        }
    } else {
        console.log("Error, couldn't find appropriate selection.")
    }
}

function find_rule_type_from_selection(sel) {
    if (sel) {
        if (sel.id.indexOf('Color') >= 0){
            return 'Color'
        }
        if (sel.id.indexOf('Filter') >= 0){
            return 'Filter'
        }
    } else {
        console.log("Error, couldn't find appropriate selection.")
    }
}

function make_property_options(ruleNumber) {
    var mark = document.getElementById("node_or_link" + ruleNumber).value
    var property = document.getElementById("property" + ruleNumber)
    remove_options(property)
    if (mark == "node"){
        options = []
        for (key in nodes[0]){
            options.push(key)
        }
        options.sort()
        for (var i in options) {
            option = document.createElement("option")
            option.text = options[i]
            property.add(option)
        };
    } else if (mark == "link") {
        options = []
        for (key in links[0]){
            options.push(key)
        }
        options.sort()
        for (var i in options) {
            key = options[i]
            if (key != "source" && key != "target"){
                option = document.createElement("option")
                option.text = key
                property.add(option)
            }
        };
    }
    make_value_options(ruleNumber)
};
make_property_options(1)


function make_value_options(ruleNumber) {
    ruleNumber = typeof ruleNumber !== 'undefined' ? ruleNumber : 1;

    mark = document.getElementById("node_or_link"+ruleNumber).value
    property = document.getElementById("property"+ruleNumber).value
    valueSelector = document.getElementById("value"+ruleNumber)

    //first remove all the previous options:
    remove_options(valueSelector)
    
    if (mark == "node") {
        quantitative = add_options(valueSelector, nodes, property)
    } else if (mark == "link") {
        quantitative = add_options(valueSelector, links, property)
    }

    equality = document.getElementById("equality"+ruleNumber)
    remove_options(equality)
    equal = document.createElement("option")
    equal.text = '='
    equality.add(equal)

    if (quantitative) {
        greater = document.createElement("option")
        less = document.createElement("option")
        greater.text = '>'
        less.text = '<'
        equality.add(greater)
        equality.add(less)
    }
}


  // ****************************************** //


 //        COLOR AND FILTER FUNCTIONS          //


// ****************************************** //

function create_color_box(ruleNumber) {

    colorBox = document.getElementById("node_color" + ruleNumber)
    d3.select(colorBox).on('input', function() {
        colorBox = document.getElementById("node_color" + ruleNumber) //need to do this again or it grabs the recent colorBox
        color = colorBox.value // get the current value of the input field.
        colorBox.style.fontWeight = "800"
        colorBox.style.backgroundColor = "white"
        colorBox.style.color = color
        computedStyle = window.getComputedStyle(colorBox)
        computedColor = computedStyle.color
        d3.select(this)
            .transition()
            .duration(hoverOverTime)
            .style("background-color", calculate_brackground(computedColor))
            .style("color", color)
    });
}
create_color_box(1)

function color_filter_or_undo(sel) {
    ruleNumber = find_rule_number_from_selection(sel)
    button = document.getElementById("ruleButton"+ruleNumber)
    ruleState = button.value //Can be Highlight, Filter or Undo
    removeReveal()
    if (ruleState == 'Filter') {
        success = make_coloring(ruleNumber)
        if (success) {
            switch_button(button, "Filter", "Undo")
        }
    }
    else if (ruleState == 'Highlight') {
        success = make_coloring(ruleNumber)
        if (success) {
            switch_button(button, "Highlight", "Undo")
        }

    } else if (ruleState == 'Undo') {
        //reset all links and nodes to defaults
        d3.selectAll(".link")
            .style("stroke", edgeColor)
            .style("visibility", "visible")
            .style("fill-opacity", oplink)

        d3.selectAll(".node")
            .style("fill", nodeColor)
            .style("visibility", "visible")
            .style("fill-opacity", opnode)
            .classed({"important":false})

        if (hasClass(button, "highlight")){
            switch_button(button, "Highlight", "Undo")
        } else if (hasClass(button, "filter")){
            switch_button(button, "Filter", "Undo")
        }
        redo_rules(ruleNumber)
        removeReveal()
    }
}

function make_coloring(ruleNumber) {
    mark = document.getElementById("node_or_link"+ruleNumber).value
    property = document.getElementById("property"+ruleNumber).value
    value = document.getElementById("value"+ruleNumber).value
    ruleButton = document.getElementById("node_color"+ruleNumber)
    filterButton = document.getElementById("filter_type"+ruleNumber)
    equality = document.getElementById("equality"+ruleNumber).value
    success = false
    color = ''
    filter = ''
    count = 0
    if (ruleButton != null) {
        color = ruleButton.value
        console.log('Coloring ' + ' ' + mark + 's' + ' with a ' + property + equality + value + ' ' + color)
        if (color != ''){
            if (mark == "node"){
                count = color_marks("circle", "fill", property, value, color, equality)
            } else if (mark == "link"){
                count = color_marks("path", "stroke", property, value, color, equality)
            }
        }
    } else if (filterButton != null) {
        filter = filterButton.value
        console.log('Filtering (' + filter + ') ' + mark + 's' + ' with a ' + property + equality + value)
        if (filter == 'keep') {
            if (equality == '='){
                equality = '!='
            } else if (equality == '<'){
                equality = '>'
            } else if (equality == '>'){
                equality = '<'
            }
        }
        if (mark == "node"){
            count = color_marks("circle", "visibility", property, value, "hidden", equality)
        } else if (mark == "link"){
            count = color_marks("path", "visibility", property, value, "hidden", equality)
        }
    }
    if (count > 0){
        success = true
        reveal_count(mark, filter, color, count)
    }
    return success
}

function reveal_count(mark, filter, color, count){
    if (filter == 'hide' || filter == 'keep'){action = 'filtered out'
    } else {action = 'colored'}

    if (mark == 'link'){beginning = 'On average, per hive, '
    } else {beginning = ''}

    if (count > 1){mark = mark + 's were'
    } else {mark = mark + ' was'}

    text = beginning + Math.ceil(count) + ' ' + mark + ' ' + action + '.'


    removeReveal()
    d3.select("body").select("#reveal").append("p")
        .html(text)
        .style("color", color)
};

function color_marks(mark, styling, property, value, color, equality) {
    count = 0
    if (equality == '>'){
        d3.selectAll(mark).each(function(d){
            if (Number(d[property]) > Number(value)) {
                count ++
                d3.select(this)
                    .each(function(){
                        if (mark == 'cirle'){
                            d3.select(this).moveToFront()}
                    })
                    .style(styling, color)
                    .style("fill-opacity", opnode_more)
                    .classed({"important":true})
                if (styling == 'visibility' && mark == 'circle'){
                    d3.selectAll(".link")
                        .each(function(l){
                            if (l.source.name == d.name || l.target.name == d.name){
                                d3.select(this).style(styling, color)
                            }
                        });
                }
            }
        })
    }
    else if (equality == '<'){
        d3.selectAll(mark).each(function(d){
            if (Number(d[property]) < Number(value)) {
                count ++
                d3.select(this)
                    .each(function(){
                        if (mark == 'cirle'){
                            d3.select(this).moveToFront()}
                    })
                    .style(styling, color)
                    .style("fill-opacity", opnode_more)
                    .classed({"important":true})
                if (styling == 'visibility' && mark == 'circle'){
                    d3.selectAll(".link")
                        .each(function(l){
                            if (l.source.name == d.name || l.target.name == d.name){
                                //d3.select(this).style(styling, color)
                            }
                        });
                }
           }
        })
    }
    else if (equality == '='){
        d3.selectAll(mark).each(function(d){
            if (d[property] == value) {
                count ++
                d3.select(this)
                    .each(function(){
                        if (mark == 'cirle'){
                            d3.select(this).moveToFront()}
                    })
                    .style(styling, color)
                    .style("fill-opacity", opnode_more)
                    .classed({"important":true})
                if (styling == 'visibility' && mark == 'circle'){
                    d3.selectAll(".link")
                        .each(function(l){
                            if (l.source.name == d.name || l.target.name == d.name){
                                d3.select(this).style(styling, color)
                            }
                        });
                }
           }
        })
    } else if (equality == '!='){
        d3.selectAll(mark).each(function(d){
            if (d[property] != value) {
                count ++
                d3.select(this)
                    .each(function(){
                        if (mark == 'cirle'){
                            d3.select(this).moveToFront()}
                    })
                    .style(styling, color)
                    .style("fill-opacity", opnode_more)
                    .classed({"important":true})
                if (styling == 'visibility' && mark == 'circle'){
                    d3.selectAll(".link")
                        .each(function(l){
                            if (l.source.name == d.name || l.target.name == d.name){
                                d3.select(this).style(styling, color)
                            }
                        });
                }
           }
        })
    }
    if (!doubleAxes){return count/num_panels}
    else {return count/num_panels/2}
};



  // ****************************************** //


 //        MANIPULATING RULES AND BUTTONS      //


// ****************************************** //

function switch_button(button, name1, name2) {
    if (button.value == name1){
        button.value = name2
    } else if (button.value == name2) {
        button.value = name1
    }

}

function count_rules() {
    count = 1
    while (true) {
        form = document.getElementById("ruleForm"+count)
        if (form == null) {
            return count
        } else {
            count = count + 1
        }
    }
}

function remove_add_rule_button() {
    addColorRule = document.getElementById("addColorRule")
    form = addColorRule.parentNode
    form.removeChild(addColorRule)
    form.parentNode.removeChild(form)
    div = form.parentNode
    if (div != null) {
        div.parentNode.removeChild(div)
    }
    addFilterRule = document.getElementById("addFilterRule")
    form = addFilterRule.parentNode
    form.removeChild(addFilterRule)
    form.parentNode.removeChild(form)
    div = form.parentNode
    if (div != null) {
        div.parentNode.removeChild(div)
    }
}

function place_add_rule() {
    d3.select("body").select("#controlpanel").append("div").html("<form action='' class='darktext leftrule'>"
        +"<input value='+ coloring rule' id='addColorRule' onclick='add_rule(this);' "
        +"type='button' class='darktext addbutton' /> </form>")
    d3.select("body").select("#controlpanel").append("div").html("<form action='' class='darktext'>"
        +"<input value='+ filtering rule' id='addFilterRule' onclick='add_rule(this);' "
        +"type='button' class='darktext addbutton filter' /> </form>")
}

function add_rule(sel){
    ruleType = find_rule_type_from_selection(sel)
    ruleNumber = count_rules()
    remove_add_rule_button()
    if (ruleType == 'Color') {
        var newRule = ColorRuleTemplate.format(ruleNumber, ruleNumber, ruleNumber, ruleNumber, ruleNumber, ruleNumber, ruleNumber, ruleNumber)
    } else if (ruleType == 'Filter') {
        var newRule = FilterRuleTemplate.format(ruleNumber, ruleNumber, ruleNumber, ruleNumber, ruleNumber, ruleNumber, ruleNumber, ruleNumber)
    }
    d3.select("body").select("#controlpanel").append("div")
        .html(newRule)

    make_property_options(ruleNumber)
    create_color_box(ruleNumber)
    place_remove_icon(ruleNumber)
    place_add_rule()
}

function remove_rule(sel){
    ruleNumber = find_rule_number_from_selection(sel)
    rule = document.getElementById("ruleForm"+ruleNumber)
    console.log(sel, rule, ruleNumber)
    container = rule.parentNode
    container.removeChild(rule)

}

function redo_rules(undoneRule) {
    ruleNumber = 1
    while(true){
        if (ruleNumber != undoneRule){
            button = document.getElementById("ruleButton"+ruleNumber)
            if (button == null){
                return null
            } else {
                //check if button that button hasn't already been undone, ie isn't coloring anything
                if (button.value == 'Undo') {
                    make_coloring(ruleNumber)
                }

            }
        }
        ruleNumber++
    }

}


  // ****************************************** //


 //              RANDOM FUNCTIONS              //


// ****************************************** //

function get_angles(numAxes,doubleAxes){
    if (doubleAxes){
        if (numAxes==3){
            a = [-0.35, 0.35, 1.75, 2.44, 3.84, 4.54]
        } else if (numAxes == 2){
            a = [-2.09, -1.05, 1.05, 2.09]
        } else if (numAxes == 4){
            a = [-0.26, 0.26, 1.31, 1.83, 2.88, 3.4, 4.45, 4.97]
        }
    } else {
        if (numAxes==3){
            a = [0.0001, 2.09, 4.19]
        } else if (numAxes == 2){
            a = [-1.57, 1.57]
        } else if (numAxes == 4){
            a = [0.0001, 1.57, 3.14, 4.71]
        }
    }
    return a
}


function calculate_brackground(color) {
    c = convertRGB(color)
    brightness = Math.sqrt(c[0] * c[0] * .241 + c[1] * c[1] * .691 + c[2] * c[2] * .068);
    if (brightness < 200){
        return "white"
    }
    else {return "#696773"}
}

function check_quantitative(options){
    for (o in options) {
        opt = options[o]
        if (isNaN(opt)) {
            return false
        }
    };
    return true
}

function degrees(radians) {
  return radians / Math.PI * 180 - 90;
}

function convertRGB(rgb)
{
    var regex = /rgb *\( *([0-9]{1,3}) *, *([0-9]{1,3}) *, *([0-9]{1,3}) *\)/;
    var values = regex.exec(rgb);
    if(values.length != 4)
    {
        return rgb;// fall back to what was given.              
    }
    var r = Math.round(parseFloat(values[1]));
    var g = Math.round(parseFloat(values[2]));
    var b = Math.round(parseFloat(values[3]));
    return [r,g,b]
}

function hasClass(element, cls) {
    return (' ' + element.className + ' ').indexOf(' ' + cls + ' ') > -1;
}

function capitalize(str) {
    var lower = str.toLowerCase();
    return lower.replace(/(^| )(\w)/g, function(x) {
        return x.toUpperCase();
        });
}

String.prototype.format = function () {
    var i = 0, args = arguments;
    return this.replace(/{}/g, function () {
        return typeof args[i] != 'undefined' ? args[i++] : '';
    });
};

function round_value(value){
    if (isNaN(value)){
        return value
    } else {
        value = Number(value)
        if (value == 0 || value == -0){ return value}
        new_value = Math.round(value * 1000) / 1000
        if (new_value == 0){
            new_value = Math.round(value * 100000) / 100000
            if (new_value == 0){
                return Number(value)
            } else {
                return new_value
            }
        } else {
            return new_value
        }
    }
}

function get_categories(trait){
    values = d3.nest().key(function(d) {return d[trait]})
                    .rollup(function(leaves) { return leaves.length;})
                    .entries(nodes);
    var keys = [];

    for (var key in values) {
        if (values.hasOwnProperty(key)) {
        keys.push(values[key].key);
        }
    }

    keys.sort()
    return keys
}

function logspecial(positive) {
  position = (typeof position === "undefined") ? true : position;
  return d3_scale_log(d3.scale.linear().domain([0, 1]), 10, positive, [1, 10]);
};

function d3_scale_log(linear, base, positive, domain) {

  function log(x) {
    return (positive ? Math.log(x <= 0 ? 0.00000000000000001 : x) : -Math.log(x >= 0 ? 0.0000000000001 : -x)) / Math.log(base);
  }

  function pow(x) {
    return positive ? Math.pow(base, x) : -Math.pow(base, -x);
  }

  function scale(x) {
    return linear(log(x));
  }

  scale.invert = function(x) {
    return pow(linear.invert(x));
  };

  scale.domain = function(x) {
    if (!arguments.length) return domain;
    positive = x[0] >= 0;
    linear.domain((domain = x.map(Number)).map(log));
    return scale;
  };

  scale.base = function(_) {
    if (!arguments.length) return base;
    base = +_;
    linear.domain(domain.map(log));
    return scale;
  };

    function d3_scale_linearRebind(scale, linear) {
      return d3.rebind(scale, linear, "range", "rangeRound", "interpolate", "clamp");
    }

  return d3_scale_linearRebind(scale, linear);
}


ColorRuleTemplate = "<form action='' class = 'darktext rules' id = 'ruleForm{}' name = 'ruleForm'>"+
"                    If a "+
"                    <select id= 'node_or_link{}' onchange='update_properties(this)' class = 'darktext'>"+
"                        <option>node</option>"+
"                        <option>link</option>"+
"                    </select>'s"+
"                    <select id= 'property{}' onchange='update_values(this)' class = 'darktext' maxwidth='5px'>"+
"                        <option>property</option>"+
"                    </select>"+
"                    <select id= 'equality{}' class = 'darktext'>"+
"                        <option>=</option>"+
"                    </select>"+
"                    <select id= 'value{}' class = 'darktext'>"+
"                        <option>value</option>"+
"                    </select>"+
"                    , color:   "+
"                    <input type='text' id='node_color{}' size='7' value=''/>  "+
"                    <input value ='Highlight' id = 'ruleButton{}' name = 'ruleButton' onclick='color_filter_or_undo(this);' type = 'button' class = 'darktext highlight'/>"+
"                </form>"

FilterRuleTemplate = "<form action='' class = 'darktext rules filter' id = 'ruleForm{}' name = 'ruleForm'>"+
"                    If a "+
"                    <select id= 'node_or_link{}' onchange='update_properties(this)' class = 'darktext'>"+
"                        <option>node</option>"+
"                        <option>link</option>"+
"                    </select>'s"+
"                    <select id= 'property{}' onchange='update_values(this)' class = 'darktext' maxwidth='5px'>"+
"                        <option>property</option>"+
"                    </select>"+
"                    <select id= 'equality{}' class = 'darktext'>"+
"                        <option>=</option>"+
"                    </select>"+
"                    <select id= 'value{}' class = 'darktext'>"+
"                        <option>value</option>"+
"                    </select>"+
"                    <select id= 'filter_type{}' class = 'darktext'>"+
"                        <option>hide</option>"+
"                        <option>keep</option>"+
"                    </select>"+
"                    <input type = 'checkbox' value ='Filter' id = 'ruleButton{}' name = 'ruleButton' onclick='color_filter_or_undo(this);' type = 'button' class = 'darktext filter'/> Filter <br>"+
"                </form>"

//creates the icon to remove rules
function place_remove_icon(ruleNumber) {

    function insertAfter(referenceNode, newNode) {
        referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
    }

    var icon = document.createElement("d")
    icon.innerHTML = "<img src='remove_icon.svg' class='icon' id = 'removeIcon"+ruleNumber+"' onclick='remove_rule(this)'>"
    var div = document.getElementById("equality"+ruleNumber);
    insertAfter(div, icon);
}
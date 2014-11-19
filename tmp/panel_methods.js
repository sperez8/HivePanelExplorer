  // ****************************************** //


 //         WEB PAGE LAYOUT PARAMETERS         //


// ****************************************** //

d3.select("body").select("#title").select("#thetitle")
    .html(SVGTitle)

N = nodes.length
E = links.length
d3.select("body").select("#title").select("#info")
    .html(N+' nodes, '+E+' edges')

  // ****************************************** //


 //       ASSIGNMENT AND POSITION SCALES       //


// ****************************************** //

var angle = get_angles(numAxes,doubleAxes)

if (doubleAxes){
    var seriesNames = [0,1]
    var angleRange = d3.range(numAxes*2)
} else {
    var seriesNames = [0]
    var angleRange = d3.range(numAxes)
};

console.log(angleRange)


var angles = d3.scale.ordinal()
    .domain(angleRange)
    .range(angle);

console.log(angles.range(), angles.domain())

var asgScales = {};
    posScales = {};

var width = document.getElementById("panel").offsetWidth
    height = width
    padding = width/0.7*0.05;
    panels = Math.max(columntraits.length, rowtraits.length)
    size = (width-padding)/panels
    num_panels = columntraits.length*rowtraits.length

console.log('\nAssignment values for grouping of nodes on axes:')
for (var i in columntraits) {
    trait = columntraits[i];
    categorical = !check_quantitative([nodes[0][trait]])
    if (categorical){
        keys = get_categories(trait)
        asgScales[trait] = d3.scale.ordinal()
            .domain(keys)
            .range(d3.range(numAxes));
        console.log('Categorical trait ', trait, ' has categories: ', keys)
    } else {
        max = d3.max(nodes, function(d) {
            return Number(d[trait])});
        min = d3.min(nodes, function(d) {
            return Number(d[trait])});
        asgScales[trait] = d3.scale.quantile()
                                .domain([min,max])
                                .range(d3.range(numAxes));
        console.log('Quantitative trait ', trait, ' has values and cut offs: ')
        for (var i = 0; i <= numAxes-1; i++) {
            console.log('\t axis', i, asgScales[trait].invertExtent(i))
        };
    }
}

console.log('\nScaled values for positioning of nodes onto axes:')
for (var i in rowtraits) {
    trait = rowtraits[i];
    categorical = !check_quantitative([nodes[0][trait]])
    if (categorical){
        keys = get_categories(trait)
        posScales[trait] = d3.scale.ordinal()
            .domain(keys)
            .rangeBands([0, 1], 1.0/keys.length/3);
        console.log('Categorical trait ', trait, ' has categories: ', keys)
    } else {
        max = d3.max(nodes, function(d) {
            return Number(d[trait])});
        min = d3.min(nodes, function(d) {
            return Number(d[trait])});
        posScales[trait] = d3.scale.linear()
                                .domain([min,max])
                                .range([0, 1]);
        console.log('Quantitative trait ', trait, ' has min and max value: ', min, ',', max)
    }
}

function cross(a, b){
    var c = [], n = a.length, m = b.length, i, j;
    for (i = -1; ++i < n;) for (j = -1; ++j < m;) c.push({x: a[i], i: i, y: b[j], j: j});
    return c;

};


  // ****************************************** //


 //          MAKING THE SVG AND HIVES          //


// ****************************************** //

var tooltip = d3.select("body").append("div")   
    .attr("class", "tooltip")               
    .style("opacity", 0);

var svg = d3.select("body").select("#container").select("#panel").append("svg")
    .attr("class", SVGTitle)
    .attr("width", width)
    .attr("height", width)
    .style("background-color", bkgcolor)
  .append("g")
    .attr("transform", "translate(" + (size/2 + padding) + "," + (size/2 + padding) + ")"); //(0,0) coordinates correspond to the center of the first hive.

var cell = svg.selectAll(".cell")
  .data(cross(columntraits,rowtraits))
.enter().append("g")
  .attr("class", "cell")
  .attr("transform", function(d) { return "translate(" + (d.i) * size + "," + d.j * size + ")"; })
  .each(plot);
  
function plot(p){
    var cell = d3.select(this);

    var innerRadius = size*0.05
    var outerRadius = size*0.45
    var radius = d3.scale.linear().range([innerRadius, outerRadius]);

    if (p.i == 0){
    cell.append("text")
        .attr("x", function(d) { return d.i; })
        .attr("y", function(d) { return d.j-size/2 - padding/2})
        .attr("text-anchor", "middle")
        .attr("class","viztext")
        .text(capitalize(p.y))
        .attr("transform", function(d) { 
            return "rotate(-90)"; //"translate("+ d.i-size/2 + "," + d.j-size/2+")
            })
    }

    if (p.j==0){
    cell.append("text")
        .attr("x", function(d) { return d.i; })
        .attr("y", function(d) { return d.j-size/2 - padding/2; })
        .attr("text-anchor", "middle")
        .attr("class","viztext")
        .text(capitalize(p.x))

    }

    // Uncomment to see the cutoffs of the scale
    //console.log(asgScales[p.x].invertExtent(0), asgScales[p.x].invertExtent(1), asgScales[p.x].invertExtent(2)) 
    // cell.selectAll(".axis")
    //     .data(angle)
    //   .enter().append("text")
    //     .attr("transform", function(d) { return "rotate(" + degrees(angles(d)) + ")translate("+radius.range()[1] + 40+","+0+")"; })
    //     //.attr("x", function(d) {return Math.sin(angles(d))*(radius.range()[1])} )
    //     //.attr("y", function(d) {return - Math.cos(angles(d))*(radius.range()[1])} )
    //     .text(function(d,i) {return asgScales[p.x](i)})

    cell.selectAll(".axis")
        .data(angle)
      .enter().append("line")
        .attr("class", "axis")
        .attr("transform", function(d) { return "rotate(" + degrees(angles(d)) + ")"; })
        .attr("x1", radius.range()[0])
        .attr("x2", radius.range()[1])
        .attr("stroke-width",0.7)
        .attr("stroke", "black");

    //format all viz text the same
    cell.selectAll("text")
        .attr("font-family", "Helvetica Neue")
        .attr("fill", "#4E3D54")
        .attr("font-size", "17px")

    var series = cell.selectAll(".series")
                        .data(seriesNames)
                      .enter().append("g")
                        .attr("class", "series")
                        .each(hive);

    function hive(h){
        var axesType = d3.select(this);
        var isSource = true

        axesType.selectAll(".link")
            .data(links)
          .enter().append("path")
            .attr("class", "link")
            .attr("d", d3.hive.link()
                .angle(function(d) {
                    if (!doubleAxes){
                        a = angles(asgScales[p.x](d[p.x]))
                    } else if (isSource){ //keep track of source and target to make link
                        a = angles(asgScales[p.x](d[p.x])*2+h) //on h==0, want the source to be on the 1st axis but on h==1 we want the source to become the target
                        isSource = false
                    } else {
                        a = angles(asgScales[p.x](d[p.x])*2+1-h)
                        isSource = true
                    }
                    return a
                })
                .radius(function(d) {
                    return radius(posScales[p.y](d[p.y])); })
            )
            .attr("show", function (d) {
                s = asgScales[p.x](d.source[p.x])
                t = asgScales[p.x](d.target[p.x])
                if (!doubleAxes){
                    if (t == s) {
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
            .style("fill", linkfill)
            .style("stroke-opacity", oplink)
            .style("stroke", function(d) {
                if (edgeColor){
                return edgeColor} else {
                    return "grey"
                }
            })
            .style("stroke-width", linkwidth)
            .on("click", function(d){
                d3.select(this)
                    .call(link_full_reveal,d,d.source.name, d.target.name)
            })
            .on("mouseover", function(d){
                d3.select(this).call(link_tooltip,d,d.source.name, d.target.name)
                d3.select(this).call(highlight_links)
            })
            .on("mouseout", function(d){
                remove_tooltip()
                node_mouseout()
                link_mouseout()
            });

        //removes any edges between nodes on same axis.
        axesType.selectAll("path[show="+false+"]").remove()

        axesType.selectAll(".node")
            .data(nodes)
          .enter().append("circle")
            .attr("class", "node")
            .attr("transform", function(d) { 
                if (doubleAxes){
                    return "rotate(" + degrees(angles(asgScales[p.x](d[p.x])*2 + h)) + ")"  
                } else {
                    return "rotate(" + degrees(angles(asgScales[p.x](d[p.x]))) + ")"
               }
            })

            .attr("cx", function(d) {
                    return radius(posScales[p.y](d[p.y]));})
            .attr("r", nodesize)
            .attr("stroke-width", nodestroke)
            .attr("stroke", nodestrokecolor)
            .style("fill-opacity", opnode)
            .style("fill", function(d) { 
                return nodeColor
            })
            .on("click", function(d){
                d3.select(this)
                    .call(node_full_reveal,d)
            })
            .on("mouseover", function(d){
                d3.select(this).call(node_tooltip,d,p.x,p.y, d[p.x], d[p.y])
            })
            .on("mouseout", function(d){
                node_mouseout()
                remove_tooltip()

            })
        };
    };


  // ****************************************** //


 //         SOME DISPLAY FUNCTIONS             //


// ****************************************** //

var node_tooltip = function(node, d, px, py, x, y){
    node.transition()
        .delay(hoverOverTime/2)   
        .duration(100)
        .call(highlight_nodes)
    tooltip.transition()
        .delay(hoverOverTime/2)   
        .duration(400)      
        .style("opacity", opnode_more);
    tooltip.html(px + ': ' + round_value(x) + ', <br>' + py + ': ' + round_value(y))
        .style("left", (d3.event.pageX + 5) + "px")     
        .style("top", (d3.event.pageY - 28) + "px");
}

var node_full_reveal = function(node,d) {
    node
        .call(highlight_nodes)
        revealNode(d, node.style("fill"));
    d3.selectAll(".node")
        .each(function(n){
            if (n.name == d.name){
                d3.select(this).call(highlight_nodes)
            }
        })
/*    d3.selectAll(".link")
        .each(function(l){
            if (l.source.name == d.name || l.target.name == d.name){
                d3.select(this).call(highlight_links)
            }
        })*/
}

var node_mouseout = function(node) {
    removeReveal();
/*    d3.selectAll(".link")
        .transition()
        .duration(hoverOverTime)
        .style("stroke-opacity", oplink)
        .style("stroke-width", linkwidth)*/
    d3.selectAll(".node")
        .transition()
        .duration(hoverOverTime)
        .attr("r", nodesize)
        .attr("stroke-width", nodestroke)
        .attr("stroke", nodestrokecolor)
        .style("fill-opacity", opnode)
    }

var remove_tooltip = function(){
    tooltip.transition()        
        .duration(500)      
        .style("opacity", 0);  
}

d3.selection.prototype.moveToFront = function() {
  console.log('moving to front')
  return this.each(function(){
    this.parentNode.appendChild(this);
  });
};

var highlight_nodes = function(selection) {
    selection
        .style("fill-opacity", 1)
        .style("stroke-width", nodestroke*3)
        .attr("stroke", 'black')
        .attr("r", nodesize*1.8)
    };

var link_full_reveal = function(link,d,source,target) {
    link
        .call(highlight_links)
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

var link_tooltip = function(link, d, source, target){
    link.transition()
        .delay(hoverOverTime/2)   
        .duration(100)
        .call(highlight_links)
    tooltip.transition()
        .delay(hoverOverTime/2)   
        .duration(400)      
        .style("opacity", .7);
    tooltip.html('source: ' + source + ', <br>' + 'target: ' + target)
        .style("left", (d3.event.pageX + 5) + "px")     
        .style("top", (d3.event.pageY - 28) + "px");
}

var link_mouseout = function(node) {
    d3.selectAll(".link")
        .transition()
        .duration(hoverOverTime)
        .style("stroke-opacity", oplink)
        .style("stroke-width", linkwidth)
    }

var highlight_links = function(selection) {
    selection            
        .transition()
        .delay(hoverOverTime*0.1)
        .duration(hoverOverTime*0.2)
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

var revealNode = function(d,color){
    removeReveal()
    d3.select("body").select("#reveal").append("p")
        .html(make_node_full_reveal_text(d))
        .style("color", color)
        .style("background-color", "white")
        .transition()
        .duration(hoverOverTime*2)
        .style("background-color", calculate_brackground(color))

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

                d3.select(this)
                    .transition()
                    .delay(1000)
                    .call(removeReveal)
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
        for (var i = selector.length - 1; i >= 0; i--) {
            selector.remove(i);
        }
    }
    return selector
};

function add_options(selector, data, property){
    options = []
    for (var i = data.length - 1; i >= 0; i--) {
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
    }

    options.sort() //sort in ascending order

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
        removeReveal()
        //reset all links and nodes to defaults
        d3.selectAll(".link")
            .style("stroke", edgeColor)
            .style("visibility", "visible")
            .style("fill-opacity", oplink);

        d3.selectAll(".node")
            .style("fill", nodeColor)
            .style("visibility", "visible")
            .style("fill-opacity", opnode);

        if (hasClass(button, "highlight")){
            switch_button(button, "Highlight", "Undo")
        } else if (hasClass(button, "filter")){
            switch_button(button, "Filter", "Undo")
        }
        redo_rules(ruleNumber)
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
    color = '#B1AFC4'
    filter = ''
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
    console.log(mark, styling, property, value, color, equality)
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
        +"<input value='Add coloring rule' id='addColorRule' onclick='add_rule(this);' "
        +"type='button' class='darktext addbutton' /> </form>")
    d3.select("body").select("#controlpanel").append("div").html("<form action='' class='darktext'>"
        +"<input value='Add filtering rule' id='addFilterRule' onclick='add_rule(this);' "
        +"type='button' class='darktext addbutton filter' /> </form>")
}

function add_rule(sel){
    ruleType = find_rule_type_from_selection(sel)
    ruleNumber = count_rules()
    remove_add_rule_button()
    if (ruleType == 'Color') {
        var newRule = ColorRuleTemplate.format(ruleNumber, ruleNumber, ruleNumber, ruleNumber, ruleNumber, ruleNumber, ruleNumber)
    } else if (ruleType == 'Filter') {
        var newRule = FilterRuleTemplate.format(ruleNumber, ruleNumber, ruleNumber, ruleNumber, ruleNumber, ruleNumber, ruleNumber)
    }
    d3.select("body").select("#controlpanel").append("div")
        .html(newRule)

    make_property_options(ruleNumber)
    create_color_box(ruleNumber)
    place_add_rule()
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
            angles = [-0.35, 0.35, 1.75, 2.44, 3.84, 4.54]
        } else if (numAxes == 2){
            angles = [-2.09, -1.05, 1.05, 2.09]
        } else if (numAxes == 4){
            angles = [-0.26, 0.26, 1.31, 1.83, 2.88, 3.4, 4.45, 4.97]
        }
    } else {
        if (numAxes==3){
            angles = [0.0001, 2.09, 4.19]
        } else if (numAxes == 2){
            angles = [-1.57, 1.57]
        } else if (numAxes == 4){
            angles = [0.0001, 1.57, 3.14, 4.71]
        }
    }
    return angles
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
        return rgb; // fall back to what was given.              
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
        new_value = Math.round(Number(value) * 1000) / 1000
        if (new_value == 0){
            new_value = Math.round(Number(value) * 100000) / 100000
            if (new_value == 0){
                new_value = Math.round(Number(value) * 10000000) / 10000000
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
                    .rollup(function(leaves) { return leaves.length; })
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
"                    <input value ='Filter' id = 'ruleButton{}' name = 'ruleButton' onclick='color_filter_or_undo(this);' type = 'button' class = 'darktext filter'/>"+
"                </form>"
HivePlotter
===========

A Python script that takes a network and writes the HTML and JavaScript files necessary to create hive plots in D3.


**Warning:** Please note that the code is under heavy development. A fully functional code will be available in the next few weeks.


## Why hive plots?
Visualizing large networks is tricky; conventional graph layout such as force directed layouts are inconsistent, often resemble "hair balls" and can even suggest patterns which aren't actually there. Comes in Martin Krzywinski (Genome Science Center, Vancouver, BC) and develops [hive plots](http://www.hiveplot.net/), a coherent network layout algorithm that places nodes using predefined rules. Hive plots facilitate the visualization of structural patterns in a network and the comparison on networks.

## Why HivePlotter?
[D3](http://d3js.org/) is a JavaScript library used to produce beautiful and interactive graphics in HTML. [Mike Bostock]( http://bost.ocks.org/mike/hive/) developed a D3 library specifically for plotting beautiful hive plots. Unfortunately, making D3 plots is quite difficult, and often isn't part of a researcher's skill set. Yet many researchers study their data using networks! From social networks to biological networks, all deserve beautiful visualizations. HivePlotter provides an easy to use python interface to build hive plots.

##Details

####Versions and Dependencies
HivePlotter was developped using Python version 2.7. The following packages are required to run HivePlotter:
* numpy
* networkx

####Input
The network should be stored in two csv input files. The node file should look like:

| Node | Property 1 | Property 2|
|:----:|:----------:|:----------:|
| Alice | girl | 12 |
| Bob | boy | 11 |
| Cam | boy | 13 |


The link file needs to specify edges using sources and targets (thought the directionality of the link will be ignored unless specified). The 'Node number' or the 'Node name' as specified in the node input file can be used to specify an edge. The link input file should look like:

|Source | Target | Property 1 | Property 2|
|:------:|:------:|:----------:|:----------:|
|Bob | Alice | friends | ...|
Bob | Cam | enemies | ...|
|Alice | Cam | friends | ...|

\* *In development: Inputting the network as an instance of a [networkx](https://networkx.github.io/) is in the works.*


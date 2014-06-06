HivePlotter
===========

A Python script that takes a network and writes the Html and Javascript files necessary to create hive plots in D3.

## Why hive plots?
Visualizing large networks is tricky; convential graph layout algorithms such as force directed algorithms often ressemble "hair balls" and sometimes suggest patterns which aren't actually there. Comes in Martin Krzywinski (Genome Science Center, Vancouver, BC) and develops [hive plots](http://www.hiveplot.net/), are a coherent network layout algorithm that places nodes using predefined rules. Hive plots facilitate the visualization of structural patterns in a network and the comparaison on networks.

## Why HivePlotter?
[D3](http://d3js.org/) is a Javascript library used to produce beautiful and interactive graphics in html. Mike Bostock developed a D3 library specifically for plotting beautiful hive plots. Unfortunately, making D3 plots is quit difficult, and often isn't part of a researcher's skill set. Yet many researchers study their data in networks! From social networks to biological networks, all deserve beautiful visualizations. HivePlotter provides an easy to use python interface to build hive plots.

##Details

**Input**
The network should be stored in two csv input files. The node file should look like:
kkk

The link file should look like:
xxx

*In development:* Inputting the network using an instance of a [networkx](https://networkx.github.io/) is in the works.

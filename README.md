HivePanelExplorer
===========

Hive Panel Explorer is a Python script that takes a network and creates a static HTML page with interactive SVG graphics in D3. The visualization produced is a matrix of hive plots plotted using attributes of the nodes and edges (such as degree and centrality). The interactive features let users explore their network and discover patterns in their network. For more information on the design of the tool and on the kind of patterns it can reveal, check out this [Oxford Bioinformatics application note](https://academic.oup.com/bioinformatics/advance-article/doi/10.1093/bioinformatics/btaa683/5876826). For even more detail, check out [Sarah Perez's Master Thesis](https://open.library.ubc.ca/cIRcle/collections/ubctheses/24/items/1.0166317)

Please cite this project using:
> Sarah E I Perez, Aria S Hahn, Martin Krzywinski, Steven J Hallam, Hive Panel Explorer: an interactive network visualization tool, Bioinformatics, , btaa683, https://doi.org/10.1093/bioinformatics/btaa683

## Why visualize networks?
Networks capture the structure of a system with relationships, wither its a social circle, a protein-protein interaction network, the World Wide Web, or other. These networks are composed of nodes (people, proteins, web pages) and edges (friendships, interactions, weblinks). These networks can get very big and visualizing them can help discover new connective patterns and properties, like social cliques, protein hubs, and modules of highly connected web pages.

## Why hive plots?
Visualizing large networks is tricky; conventional graph layout such as force directed layouts are inconsistent, often resemble "hair balls" and can even suggest patterns which aren't actually there. Comes in Martin Krzywinski (Genome Science Center, Vancouver, BC) and develops [hive plots](http://www.hiveplot.net/), a coherent network layout algorithm that places nodes using predefined rules. Hive plots facilitate the visualization of structural patterns in a network and the comparison of networks.

## Why HivePanelExplorer?
Why make one hive plot when you can make many? Why create static viz when you can interact with the data?

A hive panel is exactly what it sounds like: a layout of multiple hive plots, all representing your network in a different way. These multiple projections come in handy when you have "big data" : you can pick multiple properties of nodes (degree, clustering coefficient, gender in social networks, protein family in PPI networks etc.) to organize the nodes and layout the network differently on each plot. In this way, you can compare the positions and edges between nodes on different hive plots. Check out the wiki for examples of patterns (*coming soon!*).

### How does it work?
[D3](http://d3js.org/) is a JavaScript library used to produce beautiful and interactive graphics in HTML. [Mike Bostock]( http://bost.ocks.org/mike/hive/) developed a D3 library specifically for plotting beautiful hive plots. Unfortunately, writing in JavaScript code and D3 can be challenging, and often isn't part of a researcher's skill set. Yet many researchers' data is best analyzed and visualized using networks! From social networks to biological networks, all deserve beautiful visualizations. HivePanelExplorer (HyPE) provides an easy to use interface to build interactive hive panels. From a simple python script a static HTML page is created along with all the files necessary for you to customize, explore, and export your hive panel.

##An example running HyPE
To create an interactive hive panel of the test Friends network illustrated above, simply run the following command in your local copy of the repository.

```
$ cd ~/.../git/HivePanelExplorer/hivepanel
$ python create_panel.py -nodes ../test/friends_data/friends_nodes.txt -edges ../test/friends_data/friends_edges.txt -format txt
```

##Details

####Versions and Dependencies
HyPE was developed using Python version 2.7. The [NumPy](http://www.numpy.org/) package is currently required. The *networkx* package is included as different versions aren't compatible with current implementations. Most modern browsers support SVG and thus D3 features. See [http://caniuse.com/svg](http://caniuse.com/svg) for more details. 

####Input
Current input files accepted are:
* two text files (tab or comma separated), one for the nodes, one for the edges
* a graphml file

In the case of text files, the node file should look like the table below where all columns after the first column (arbitrarily called "Node" in this example) contain node properties. These properties can be categorical or quantitative and can be encoded as text or numbers. The first column must contain the names of the nodes to be used to identify edges in the edge file.

| Node | Gender | Height | Other property ... |
|:----:|:----------:|:----------:|:----------:|
| Alice | girl | 70 | ... |
| Matt | boy | 72 | ... |
| Zans | alien | 57 | ... |
| ... | ... | ... | ... |


The edge file needs to specify the sources and targets (though the directionality of the edge won't change the way it looks in the hive plot) in the first two columns of the file. The edges input file should look like:

|Source | Target | Relationship type | Other property ... |
|:------:|:------:|:----------:|:---:|
| Zans | Alice | enemies | ... |
| Matt | Zans | friends | ... |
| ... | ... | ... | ... |

Again, the edge properties can be encoded as text or numbers.


## The old hive plot gui
An older version of this repository was advertised as a python gui for making hive plots. It is no loner being managed by it's contents can be found in the *hiveplot* folder. The graphical user interface (GUI) written using Tkinter in Python takes a network and writes the HTML and JavaScript files necessary to create single hive plots in D3. Check out the [wiki page](https://github.com/sperez8/HivePlotter/wiki) for a step-by-step example of how to make a hive plot.

Happy hive panel exploring!


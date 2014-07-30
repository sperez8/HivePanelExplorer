HivePlotter
===========

A graphical user interface (GUI) written using Tkinter in Python that takes a network and writes the HTML and JavaScript files necessary to create hive plots in D3. Check out the [wiki page](https://github.com/sperez8/HivePlotter/wiki) for a step-by-step example of how to make a hive plot.

**Update** The GUI is now fully functional and contains all the basic features needed to plot a proper hive. Additional interactive and coloring features are on their way.

## Why hive plots?
Visualizing large networks is tricky; conventional graph layout such as force directed layouts are inconsistent, often resemble "hair balls" and can even suggest patterns which aren't actually there. Comes in Martin Krzywinski (Genome Science Center, Vancouver, BC) and develops [hive plots](http://www.hiveplot.net/), a coherent network layout algorithm that places nodes using predefined rules. Hive plots facilitate the visualization of structural patterns in a network and the comparison of networks.

## Why HivePlotter?
[D3](http://d3js.org/) is a JavaScript library used to produce beautiful and interactive graphics in HTML. [Mike Bostock]( http://bost.ocks.org/mike/hive/) developed a D3 library specifically for plotting beautiful hive plots. Unfortunately, writing in javascript code and D3 can be challenging, and often isn't part of a researcher's skill set. Yet many researchers' data is best analyzed and visualized using networks! From social networks to biological networks, all deserve beautiful visualizations. HivePlotter provides an easy to use interface to build hive plots.

##Details

####Versions and Dependencies
HivePlotter was developed using Python version 2.7. The following packages are required to run HivePlotter:
* numpy

####Input
The network should be stored in two csv input files: one storing nodes and one storing edges. The node file should look like the table below where all columns after the first column (arbitrarily called "Node" in this example) contain node properties. These properties can be encoded as text or numbers. The first column must contain the names of the nodes to be used to identify edges in the edge file.

| Node | Gender | Height |
|:----:|:----------:|:----------:|
| Alice | girl | 12 |
| Bob | boy | 11 |
| Cam | boy | 13 |


The edge file needs to specify the sources and targets (though the directionality of the edge won't change the way it looks in the hive plot - yet) in the first two columns of the file. The edges input file should look like:

|Source | Target | Relationship | Property 2...|
|:------:|:------:|:----------:|:----------:|
|Bob | Alice | friends | ...|
Bob | Cam | enemies | ...|
|Alice | Cam | friends | ...|

Again, the edge properties can be encoded as text or numbers.

##An example using the GUI
To run the user interface and make your own hive plots, simply run the following command in your local copy of the repository.

'''
$ cd ~/.../git/HivePlotter/scripts
$ python gui.py
'''

See the [wiki page](https://github.com/sperez8/HivePlotter/wiki) for an example.

Happy hive plot making!


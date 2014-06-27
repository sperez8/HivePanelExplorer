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
The network should be stored in two csv input files. The node file should look like the table below where all columns after the "Node" column contain node properties. These properties can be encoded as strings of text or numbers.

| Node | Gender | Height |
|:----:|:----------:|:----------:|
| Alice | girl | 12 |
| Bob | boy | 11 |
| Cam | boy | 13 |


The link file needs to specify edges using sources and targets (though the directionality of the link doesn't yet change anything down the line). The 'Node number' or the 'Node name' as specified in the node input file can be used to specify an edge. The link input file should look like:

|Source | Target | Relationship | Property 2...|
|:------:|:------:|:----------:|:----------:|
|Bob | Alice | friends | ...|
Bob | Cam | enemies | ...|
|Alice | Cam | friends | ...|

Again, the edge properties can be encoded as a string of text or numbers.

##An example using the GUI
To run the user interface and make your own hive plots, simply run the following command in your local copy of this repository.

'''
$ cd ~/.../git/scripts
$ python gui.py
'''

You should see a window like this:

XX

By default, the interface loads the path to input files for the test network called 'friends' and calls the hive plot 'hive1'. For this example, I choose to use 3 axes, not double. 

Next we need to choose how to assign nodes to axes and place the nodes on axes. Since we would like the node assignment and positioning rules to be based on node properties, we click "Submit Network" to update the rule menus. The node properties labelled in the input csv file (much like the one above) are now options for node assignment and positioning rules.

XX

In the 'friends' network I chose to place the nodes on axis given their degree. I then chose to position the nodes on each axis given their gender. Sorter by alphabetical order, the nodes which are 'alien' will apear at the center, 'boy' in the middle and 'girl' towards the ends of the axes. Finally we select how we want to color the edges: either all the same color ('uniform') or using an edge property. In this example, I choose to color them by 'relationship'. Once you have made your choices, click 'Load Parameters'.

XX

Since there are two kinds of relationships, the number of colors is automatically set to 2. If 'relationship' were a numerical variable you would change 'Number of Colors' to however many bins you want to use to categories these values and color the edges accordingly. Last but not least, select the node color and the edge color palette hue.

Click "Create Hive". Now open the file 'hive1.html' in the 'tests' folder in the github repository using a browser (modern browsers preferred). It should look like the image below. The interface window remains for you to try different placing and coloring rules. Don't forget the 'Load Parameters' before you change the color scheme.

Happy hive making!





Once we have selecte

Resources on C. elegans:
http://www.wormbook.org/chapters/www_gaba/gaba.html


Four publically available C. elegans connectomes can be found here:

 http://openconnecto.me/graph-services/download/



The herm_pharynx connectome, which was used here, has detailed information here: https://github.com/ericmjonas/circuitdata/tree/master/celegans_herm

nodes: 279	links: 3225

Cells

cell_id : auto-inc cell ID
cell_name : official cell name, from original brenner paper
cell_class : an attempt at determining the cell class
soma_pos : position along the body axis, range : [0, 1]
role: text string of Motor, sensory, interneuron
neurotransmitter: text string of type of neurotransmitter
Synapses

Synapses; note that the electrical synapses are undirected, the chemical synapses directed.

from_id : from cell id
to_id : to cell id
synapse_type: 'E' for electrical, 'C' for chemical
count : # of this kind of synapse
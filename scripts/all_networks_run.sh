for n in 'JP' 'SBS' 'MD'
do
	# python plot_networks.py -networks $n -maketable
	#for edge in 'pos' 
	for level in 'phylum' 'order' 'class'
	do
		python plot_networks.py -taxarep -level $level -networks $n
		python latex_table.py -convert -header -tabfile "/Users/sperez/Desktop/LTSPnetworks/plots/representation_"$n"_"$level".txt" 
		#python plot_networks.py -networks $n -edgetype $edge
		# python plot_networks.py -networks $n -calculate -edgetype $edge
		# python plot_networks.py -networks $n -distribution -edgetype $edge &
		# for fraction in 0.1 1
		# do
		# # 	python plot_networks.py -networks $n -bcplot -percentnodes $fraction #-showcomponents 5.5
		#  	python plot_networks.py -networks $n -simulate -edgetype $edge -treatment -fraction $fraction -showcomponents 5.5 &
		#  	python plot_networks.py -networks $n -simulate -edgetype $edge -measure -fraction $fraction -showcomponents 5.5 &
		#  	wait
		# done
	done
done

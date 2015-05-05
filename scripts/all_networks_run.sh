for n in 'JP' 'SBS'
do
	# python plot_networks.py -networks $n -maketable
	for edge in 'pos' 
	do
		#python plot_networks.py -networks $n -edgetype $edge
		# python plot_networks.py -networks $n -calculate -edgetype $edge
		# python plot_networks.py -networks $n -distribution -edgetype $edge &
		for fraction in 0.1 1
		do
		# 	python plot_networks.py -networks $n -bcplot -percentnodes $fraction #-showcomponents 5.5
		 	python plot_networks.py -networks $n -simulate -edgetype $edge -treatment -fraction $fraction -showcomponents 5.5 &
		 	python plot_networks.py -networks $n -simulate -edgetype $edge -measure -fraction $fraction -showcomponents 5.5 &
		 	wait
		done
	done
done

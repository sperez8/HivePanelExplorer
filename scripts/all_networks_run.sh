for n in 'MD' 'JP' #'SBS'
do
	# python plot_networks.py -networks $n -maketable
	for edge in 'neg' 'both' 'pos'
	do
		python plot_networks.py -networks $n -calculate -edgetype $edge
		# python plot_networks.py -networks $n -distribution -edgetype $edge &
		# for fraction in 0.1 0.2 1
		# do
		# 	python plot_networks.py -networks $n -simulate -edgetype $edge -treatment -fraction $fraction & #-showcomponents 5.5
		# 	python plot_networks.py -networks $n -simulate -edgetype $edge -measure -fraction $fraction & #-showcomponents 5.5
		# 	wait
		# done
	done
	wait
done

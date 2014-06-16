
numAxes = 3
doubleAxes = True
cutoffValues = [1,15,269]
axisAssignRule = 'degree'
axisPositRule = 3
color = 'white'

#edge styling
edgeColorPalette = ['blue','red']
edgeColorRule = 1

#node styling
nodeColorPalette = ['blue', 'red']
nodeColorRule = 1

#python scripts/main.py -n /Users/sperez/git/microbPLSA/MicrobProcessor/D3/hiveplots/Data/WL_Nodes_ALL.csv -e /Users/sperez/git/microbPLSA/MicrobProcessor/D3/hiveplots/Data/WL_EDGES_ALL.csv -t aria -d


'''
# Below are variables which would normally be inputer by the user.
# For the sake of developing the script I have stored them here for convenience

numAxes = 3
doubleAxes = False
axisAssignRule = 2
axisPositRule = 'degree'

color = 'green'

#edge styling
edgeColorPalette = ['blue', 'purple']
edgeColorRule = 2 #'average connecting degree'


#example command
#python scripts/main.py -n tests/test_nodes_friends.csv -e tests/test_edges_friends.csv -t friends -d
'''
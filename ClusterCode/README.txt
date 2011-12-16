Step 1:
place in list of hashtag co-counts
rename CoCounts.txt
Run preProcess.py (creates prePro.txt)

Step 2:
Run creatingClusters.py
	This function creates topWord list 
	Also creates initial cluster list based on 1%

Step 3:
Run createTopLists.py
	Make sure you have a folder named classes
	extracts each top hashtag list

Step 4:
Run createRealClusters.py
	Bottleneck step
	Compares lists and keeps only if there is overlap

Step 5:
Run createNewTopWords.py and then createGraph.py
	Move graph.txt to matlab
	Save as excel

Step 6:
Open data file
Run createGraphMatix followed by myKmeans
Move clusterID into python folder

Step 7:
Run spectralClusters.py (folder spectralClusters is now needed)

Step 8:
Run newCombiningLines.py 
	Rename file created to editedReal.txt

Step 9:
Run finalProgram.py (need finalCluster folder)

We're done!


# Appendix A: generating data for Graphviz
mkdir textFiles/graphs
cat textFiles/clusters.txt | ./get_graph_data.py 0.1 > textFiles/graphs/graph-data.dot
fdp -Tpdf textFiles/graphs/graph-data.dot -o textFiles/graphs/graph10.pdf

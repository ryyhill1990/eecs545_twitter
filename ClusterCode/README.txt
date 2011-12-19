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
Open data file in matlab: data = importdata('graph.txt');
Run createGraphMatix followed by myKmeans
Move clusterID into python folder

Step 7:
mkdir textFiles/spectralClusters
Run spectralClusters.py (folder spectralClusters is now needed)

Step 8:
Run newCombiningLines.py 
	Rename file created to editedReal.txt
	mv textFiles/combinedLines.txt textFiles/editedReal.txt

Step 9:
mkdir textFiles/finalClusters
Run finalProgram.py (need finalClusters folder)

We're done!



#### Appendix A: generating data for Graphviz ###

# generating graph on not-fully-processed data
mkdir textFiles/graphs
cat textFiles/clusters.txt | ./get_graph_data.py 0.1 > textFiles/graphs/graph-data.dot
fdp -Tpdf textFiles/graphs/graph-data.dot -o textFiles/graphs/noFilterGraph10.pdf
cat textFiles/clusters.txt | ./get_graph_data.py 0.5 > textFiles/graphs/graph-data.dot
fdp -Tpdf textFiles/graphs/graph-data.dot -o textFiles/graphs/noFilterGraph50.pdf
cat textFiles/clusters.txt | ./get_graph_data.py 0.9 > textFiles/graphs/graph-data.dot
fdp -Tpdf textFiles/graphs/graph-data.dot -o textFiles/graphs/noFilterGraph90.pdf

# generating graph for fully-processed data
cat textFiles/finalData/editedReal.txt | ./get_graph_data.py 1 --mode=final > textFiles/graphs/graph-data.dot
fdp -Tpdf textFiles/graphs/graph-data.dot -o textFiles/graphs/finalmetis.pdf
cat textFiles/finalData/editedRealNS.txt | ./get_graph_data.py 1 --mode=final > textFiles/graphs/graph-data.dot
fdp -Tpdf textFiles/graphs/graph-data.dot -o textFiles/graphs/finalNS.pdf
cat textFiles/finalData/editedRealS.txt | ./get_graph_data.py 1 --mode=final > textFiles/graphs/graph-data.dot
fdp -Tpdf textFiles/graphs/graph-data.dot -o textFiles/graphs/finalS.pdf

# generating graph on not-fully-processed data
cat textFiles/realClusters.txt | ./get_graph_data.py 0.1 > textFiles/graphs/graph-data.dot
fdp -Tpdf textFiles/graphs/graph-data.dot -o textFiles/graphs/filtereGraph10.pdf
cat textFiles/realClusters.txt | ./get_graph_data.py 0.5 > textFiles/graphs/graph-data.dot
fdp -Tpdf textFiles/graphs/graph-data.dot -o textFiles/graphs/filtereGraph50.pdf
cat textFiles/realClusters.txt | ./get_graph_data.py 0.9 > textFiles/graphs/graph-data.dot
fdp -Tpdf textFiles/graphs/graph-data.dot -o textFiles/graphs/filtereGraph90.pdf

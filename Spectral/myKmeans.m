%define K to be the K smallest eigenvalues; i.e. the number of clusters
K=300;


%yVectors = V(:,1:K);
yVectors = newV(:,1:K);
%now we want to cluster with yi = yVector(:,i)

[IDX, C, SUMD] = kmeans(yVectors,K);

sum(SUMD)

fileID = fopen('clusterID.txt','w');

fprintf(fileID, '%d \n', IDX);

fclose(fileID);
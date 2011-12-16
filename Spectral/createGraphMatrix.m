%assume that formatGraph as been open
%and that data is in the matrix data

n = size(data,1);
topWordCount = data(n,1);

similarityMatrix = zeros(topWordCount,topWordCount);
degreeMatrix = zeros(topWordCount,topWordCount);
    
for i = 1:n
    x = data(i,1);
    y = data(i,2);
    
    if x~=y
        similarityMatrix(x,y) = data(i,3)/data(i,4);
    end
    
end

similarityMatrix = (similarityMatrix+similarityMatrix')/2;


for i = 1:topWordCount
    rowSum = sum(similarityMatrix(i,:));
    
    degreeMatrix(i,i) = rowSum;
    
end

L = degreeMatrix - similarityMatrix;

[V,D] = eig(L);



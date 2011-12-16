n = size(similarityMatrix,1);

fileID = fopen('fullGraphMatrix.txt','w');


for i = 1: n
    for j = 1:n
        
        fprintf(fileID, '%f ', similarityMatrix(i,j));
    end
    
    fprintf(fileID, '\n');
end

fclose(fileID);
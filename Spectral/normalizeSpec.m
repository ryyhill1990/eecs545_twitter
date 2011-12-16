n = size(degreeMatrix,1);
inverseDegree = zeros(n,n);
for i = 1 : n
    
    inverseDegree(i,i) = 1/degreeMatrix(i,i);
    
end

Lhat = inverseDegree*L;

[newV,newD] = eig(Lhat);
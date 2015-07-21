# runTest.sh

# while read line;
for filePath in ./testRawIdf/*
do 
	fileName=$(basename "$filePath")
	line="${fileName%.*}"
	echo -e "$line:\n";
	Rscript ./sigmoidFitting/idfSeriesToTuples_Testing.r "${line}"
	./modelFitting/supportVecIDF_test.py "${line}"
done < testEventNames


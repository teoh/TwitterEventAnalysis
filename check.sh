# check.sh

# Counts the occurence of a keyword in all
# CSV files in the current directory

# args: 
# $1 - the keyword to search for

# usage: 
# The pwd contain A.csv has 100 tweets with 'earthquake'
# , B.csv has 200 tweets with 'earthquake'
# ./check.sh earthquake

# output:
# A.csv
# 100 
# B.csv
# 2000


if [ $# -eq 0 ]; then
	#statements
	echo "usage: ./check <keyword>"
	exit -1
fi

echo Searching for $1

for f in *.csv; do
	echo checking $f
	cat $f | grep -i $1 | wc -l
done	
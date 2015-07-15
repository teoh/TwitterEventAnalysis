# unzip.sh

# unzip a range of .zip files from the current directory to 
# a destination directory 

# prefix: The prefix of the file series to be extracted
# 		  eg: 2015_05_12
# start:  The start hour of file series (0-23)
# end:    End hour
# destination: Directory in which zip files are extracted

# usage: ./unzip.sh 2014_11_25_ 15 20 ~/Desktop/destinationDir

if (( $# < 4 )); then
	echo "usage: ./unzip <prefix> <start> <end> <destination>"
	exit -1
fi

# store args in local vars
prefix=$1
start=$2
end=$3
destination=$4

echo "Prefix      : $prefix"
echo "Start       : $start"
echo "End         : $end"
echo "Destination : $destination"

for n in `seq -w $start $end`; do 
	fname=$prefix$n

	echo "Unzipping $fname"

	unzip -d $destination $fname
done
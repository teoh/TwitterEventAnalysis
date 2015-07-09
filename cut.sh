# cut.sh

# select first 3 columns in a list of CSV files
# and store in the cut directory (relative) with the same filename

# DO NOT USE THIS SCRIPT!
# MySQL LOAD DATA discards the remaining columns when 
# only the first 3 columns are specified 

for f in *.csv; do
	echo cutting $f
	cat $f | cut -d$'\t' -f1-3 > ../cut/$f
	echo finished $f
done
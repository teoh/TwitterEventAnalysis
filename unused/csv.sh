# csv.sh

# Initial collection of scripts. These have been separated into
# the other scripts in this directory

# selects the first 3 columns from the input twitter
# data file - id, creation_date and content and outputs

cut -d$'\t' -f1-3 

# usage

cat 2015_05_12_12.csv | cut -d$'\t' -f1-3 > ../cut/11.csv

# select first 3 columns in a list of CSV files
for f in *.csv; do
	#statements
	cat $f | cut -d$'\t' -f1-3 > ../cut/$f
	echo finished $f
done

# check for keyword before putting in database
for f in *.csv; do
	echo $f
	cat $f | grep -i 8051 | wc -l
done	

# mysql LOAD from command line
for f in *.csv
do
    mysql -e "LOAD DATA LOCAL INFILE '~/Desktop/internship/data/4u9525/cut/$f' INTO TABLE tweet IGNORE 1 LINES (id, @date_var, content) SET creation_date = STR_TO_DATE(@date_var, '%a %b %e %k:%i:%s GMT %Y')	;" -u root --password=internship twitter
done
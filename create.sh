# create.sh

# create the desired table in the database "twitter"

# usage: ./create.sh <table_name>

table_name=$1

echo "Creating table: $table_name"

#mysql -u root --password=internship -e "use twitter; set @table_name='$table_name'; source /Users/internship/Desktop/internship/chandanStuff/twitter-events/sql/create.sql;"

mysql -u root --password=internship -e "use twitter; set @table_name='$table_name'; select @table_name; drop table if exists $table_name; create table $table_name (id BIGINT UNSIGNED, content VARCHAR(150), creation_date DATETIME );"


# alter.sh

# this script will add indices to all of the tables in the "twitter" database

# usage: ./alter.sh <table_name>

declare -a eventList=("4u9525" "boston_bombing" "charlotte" "chelyabinsk_meteor" "chibok_kidnap" "garissa" "MH17" "nepal_quake" "nepal_quake2" "peshawar_school" "qz8501" "savar_collapse" "typhoon_haiyan" "afghan_landslide" "ontake_eruption" "cyclone_phailin" "sydney_hostage")

for table_name in "${eventList[@]}"
do
	echo "Altering table: $table_name"
	mysql -u root --password=internship -e "use twitter; ALTER TABLE $table_name ADD INDEX (creation_date);"
	echo "Finished altering!"
done


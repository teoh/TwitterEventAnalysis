#createAndLoad.sh

# I got lazy and decided to lump the create table and load table processes in one file. this script will do only for one event

# usage: ./createAndLoad.sh

declare -a eventList=("nepal_quake"	"nepal_quake2"	"peshawar_school"	"qz8501"	"savar_collapse"	"typhoon_haiyan"	"afghan_landslide"	"ontake_eruption"	"cyclone_phailin"	"sydney_hostage")

for event_name in "${eventList[@]}"
do
	# event_name=MH17
	./create.sh $event_name
	./load.sh $event_name
done
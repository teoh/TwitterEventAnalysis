#exportFreq.sh

# this script will export the tables to csv files

# eventName=sydney_hostage

# declare -a keywords=("sydney" "hostage")

# for kword in "${keywords[@]}"
# do
# 	echo "(Event,keyword): ($eventName,$kword)"
# 	echo "Exporting..."
# 	mysql -u root --password=internship -e "use twitter_freq; SELECT * FROM ${eventName}_freq_${kword} INTO OUTFILE './${eventName}_freq_${kword}.csv';"
# 	mv /usr/local/mysql-5.6.25-osx10.8-x86_64/data/*.csv /Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/results 
# done



declare -a events=("4u9525" "boston_bombing" "charlotte" "chelyabinsk_meteor" "chibok_kidnap" "garissa" "MH17" "nepal_quake" "nepal_quake2" "peshawar_school" "qz8501" "savar_collapse" "typhoon_haiyan" "afghan_landslide" "ontake_eruption" "cyclone_phailin" "sydney_hostage")
declare -a kwArr=("4u9525 gwi18g germanwings" "boston bomb" "charlotte royal baby" "chelyabinsk meteor explosion" "bring back girls haram boko chibok kidnap" "garissa attack" "mh17 malaysia" "quake earthquake nepal" "nepal quake" "peshawar school taliban" "qz8501 awq8501 airasia air asia" "savar rana collapse" "haiyan typhoon philippines" "barik landslide mudslide" "ontake erupt volcano" "cyclone phailin odisha" "sydney hostage")

for ind in {0..16}  # eventName in "${events[@]}"
do
	echo "Event: $eventName"
	eventName=${events[$ind]}
	declare -a keywords=(${kwArr[$ind]}) #=============
	for kword in "${keywords[@]}"
	do
		echo "       (Event,keyword): ($eventName,$kword)"
		echo "       Exporting..."
		mysql -u root --password=internship -e "use twitter_freq; SELECT * FROM ${eventName}_freq_${kword} INTO OUTFILE './${eventName}_freq_${kword}.csv';"
		mv /usr/local/mysql-5.6.25-osx10.8-x86_64/data/*.csv /Users/internship/Desktop/internship/chandanStuff/twitter-events/scripts/results 
	done
done
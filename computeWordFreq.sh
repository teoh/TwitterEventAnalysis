# computeWordFreq.sh

# this script will take one table corresponding to an event in the twitter database and compute frequencies for a given key word

declare -a events=("4u9525" "boston_bombing" "charlotte" "chelyabinsk_meteor" "chibok_kidnap" "garissa" "MH17" "nepal_quake" "nepal_quake2" "peshawar_school" "qz8501" "savar_collapse" "typhoon_haiyan" "afghan_landslide" "ontake_eruption" "cyclone_phailin" "sydney_hostage")

declare -a kwArr=("4u9525 gwi18g germanwings" "boston bomb" "charlotte royal baby" "chelyabinsk meteor explosion" "bring back girls haram boko chibok kidnap" "garissa attack" "mh17 malaysia" "quake earthquake nepal" "nepal quake" "peshawar school taliban" "qz8501 awq8501 airasia air asia" "savar rana collapse" "haiyan typhoon philippines" "barik landslide mudslide" "ontake erupt volcano" "cyclone phailin odisha" "sydney hostage")

for ind in {0..16}  # eventName in "${events[@]}"
do
	eventName=${events[$ind]}
	declare -a keywords=(${kwArr[$ind]}) #=============
	for kword in "${keywords[@]}"
	do
		echo "(Event,keyword): ($eventName,$kword)"
		echo "      Creating keyword table..."
		# ====mysql -u root --password=internship -e "use twitter_freq; create table if not exists ${eventName}_freq_${kword} as (select creation_date, sum(content regexp '${kword}') as numOccur, count(id) as total from twitter.${eventName} group by creation_date);"
		mysql -u root --password=internship -e "use twitter_freq; create table if not exists ${eventName}_freq_${kword} as (select creation_date, sum(content regexp '${kword}') as numOccur, count(id) as total from twitter.${eventName} group by day(creation_date), hour(creation_date), minute(creation_date) );"
		echo "      Adding prop and IDF columns..."
		mysql -u root --password=internship -e "use twitter_freq; alter table ${eventName}_freq_${kword} add column prop double, add column IDF double;"
		echo "      Computing prop and IDF columns..."
		mysql -u root --password=internship -e "use twitter_freq; update ${eventName}_freq_${kword} set prop=numOccur/total, IDF=log10( (total+1)/(numOccur+1) );"
	done

done





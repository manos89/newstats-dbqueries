from pymongo import MongoClient

def get_facets(SearchWord):
	client = MongoClient('mongodb://localhost:27017/')
	db = client['basketstats']
	rexpr='(?i).*{SW}.*'.replace('{SW}',SearchWord)
	results=db['players'].aggregate([
		{'$match':{'BasicInfo.playerName':{'$regex':rexpr}}},
		{'$facet':{'age':[{ '$unwind': '$BasicInfo.age'},{ '$sortByCount':'$BasicInfo.age'}],
				'position':[{ '$unwind': '$BasicInfo.position'},{ '$sortByCount':'$BasicInfo.position'}],
				'gender':[{ '$unwind': '$BasicInfo.gender'},{ '$sortByCount':'$BasicInfo.gender'}],
				'nationality':[{ '$unwind': '$BasicInfo.nationality'},{ '$sortByCount':'$BasicInfo.nationality'}],
				'team':[{ '$unwind': '$BasicInfo.teamName'},{ '$sortByCount':'$BasicInfo.teamName'}],
				'league':[{ '$unwind': '$BasicInfo.leagueName'},{ '$sortByCount':'$BasicInfo.leagueName'}],}}
		])
	for r in results:
		print r

def get_number_of_team_games(Season,Team):
	client = MongoClient('mongodb://localhost:27017/')
	db = client['basketstats']
	results=db['players'].aggregate([
		{'$unwind':'$Stats.'+Season+'.fullStats'},
		{'$match':{'Stats.'+Season+'.fullStats.playerTeam':Team}},
		{'$group':{'_id':'$Stats.'+Season+'.fullStats.GameId'}},
		{'$count':'games'}
		])
	for r in results:
		print r

def get_game(gameId,Season):
	client = MongoClient('mongodb://localhost:27017/')
	db = client['basketstats']
	results=db['players'].aggregate([		
		{'$unwind':'$Stats.'+Season+'.fullStats'},
		{'$match':{'Stats.'+Season+'.fullStats.GameId':gameId}},
		{'$project':{'Stats.'+Season+'.fullStats':1,'BasicInfo.playerName':1}}
		
		])
	count=0
	for r in results:
		print r
		count+=1
	print count

def get_player_games(Payerid,Season):
	client = MongoClient('mongodb://localhost:27017/')
	db = client['basketstats']
	results=db['players'].aggregate([
		{'$match':{'BasicInfo.playerID':Payerid}},
		{'$unwind':'$Stats.'+Season+'.fullStats'},
		{'$project':{'Stats.'+Season+'.fullStats':1,'BasicInfo.playerName':1}}
		])
	for r in results:
		print r


# get_facets('dimitris')
# get_game('20171712318516114','2018')
# get_number_of_team_games('2018','Olympiacos')
# get_player_games('108725','2018')
from pymongo import MongoClient

def get_facets(SearchWord):
	client = MongoClient('mongodb://localhost:27017/')
	db = client['basketstats']
	rexpr='(?i).*{SW}.*'.replace('{SW}',SearchWord)
	results=db['2018'].aggregate([
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

get_facets('mich')
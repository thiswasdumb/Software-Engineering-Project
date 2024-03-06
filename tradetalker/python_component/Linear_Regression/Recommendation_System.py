import pandas as pd
import random
from flask import Flask
from python_component.Database.TradeTalker_DB import Database

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'TradeTalkerDB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

class Recommendation_System:
	def __init__(self, user_id):
		self.user_id = user_id    #for now, will be an input in future
		self.rand = random.Random
		self.rec = set({})
		self.db = Database(self.app)
		data = self.db.follow_get_user_following_companies(user_id)
		records = []
		# if db function that selects id name and industry, then can skip next bit, this bit would instead need a selects * from company id
		for id in data:
			company_data = self.db.company_select_by_id(id[0])  #0 bcs should still be in a tuple
			record = (company_data[0], company_data[1], company_data[4]) #id, name, industry
			records.append(record)
		data = records
		self.followed = pd.DataFrame.from_records(data, columns = ['id','name','industry'])

	def recommend(self):
		self.rec = set({})
		self.article_recs()
		self.industry_recs()
		self.leftover_recs()
		return self.rec

	def article_recs(self):
		#get liked articles' key words and followed companies
		article_words = self.db.liked_articles_get_words(self.user_id) #if summary, split() contents of each tuple and convert to set

		"""
		#for testing (without db)
		df = {
			"name"    : ["d","g","s"],
			"industry": ["coal","food","food"]
		}
		followed = pd.DataFrame(df)
		article_words = [["a","b","c","d","e","f","g"],["d","c","a","q","g","l","o"]]
		"""
		#adds companies appearing in key words to recommendations
		for words in article_words:
			#certaian words appear in company names but do not imply any specific company, so should be blacklisted
			blacklist = set(("group", "plc", "ord", "mining", "systems", "banking", "value", "retail", "european", "engineering", "industries", "investment", "trust", "american", "international"))
			words = set(words).difference(blacklist)

			#check if each word is a company, check if it is an already followed company so it doesn't waste time querying the db
			for wrd in words:
				if (wrd in self.followed['name'].to_list()):
					continue
				out = self.isCompany(wrd)
				if (out[0]):
					self.rec.add(out[1][0])

	def industry_recs(self):
		#get followed companies, their industry and dividend yield
		total_count = len(self.followed)


		industries = (self.followed['industry'].value_counts() / total_count).to_dict()

		"""
		print(len(rec))
		print(industries['food'])
		"""
		#function gets n non-followed companies from database
		#apply function to each industry in dict, with n being the value counts thing
		def get_companies(num, val):
			results = []

			#get all companies of the selected industry and shuffles
			data = self.db.company_select_by_industry(val)
			random.shuffle(data)

			#adds n companies, ensuring they are not yet followed
			count = 0
			while (num > 0):
				id = data[count][0]                         #gets id of next company
				if(self.db.follow_check(self.user_id, id) is None):
					results.append(id)
					num -= 1
				count += 1
			return results

		#add companies sharing industry with followed to rec
		for key in industries.keys():
			n = int(industries[key] * 10)
			if (n >= 1):
				self.rec.update(get_companies(n, key))

	def leftover_recs(self):
		#if not many companies are recommended, adds soem at random
		if (len(self.rec)<10):
			not_followed = self.db.follow_get_user_not_following_companies
			if not_followed is None:
				not_followed = []
			while (len(self.rec)<10):
				if (not_followed == []):
					break
				x = not_followed[self.rand.randint(len(not_followed))] #maybe get an order by stock price or summat
				self.rec.add(x)
	
	#check key word is in company table
	def isCompany(self, wrd):
		x = self.db.company_search_for_name(wrd)
		return (x is not None), x #isCompany, companyId tuple
		"""
		if (wrd == "d" or wrd == "q"):
			return True
		else:
			return False
		"""
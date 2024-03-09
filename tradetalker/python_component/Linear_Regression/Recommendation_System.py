import pandas as pd
import random
from flask import Flask

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'TradeTalkerDB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

class Recommendation_System:
	#data is a dict, each key has a list of dicts (records) keys: following, non_following, keywords
	def __init__(self, data, industry_groups):
		self.industry_groups = industry_groups
		self.rand = random.Random
		self.rec = set({})
		self.followed = pd.DataFrame.from_dict(data['following'])
		self.not_followed = pd.DataFrame.from_dict(data['non_following'])

		#joins list
		self.article_words = set(','.join(data['keywords']).split(','))

	def recommend(self):
		self.rec = set({})
		self.article_recs()
		self.industry_recs()
		self.leftover_recs()
		return self.rec

	def article_recs(self):
		#adds companies appearing in key words to recommendations
		#certain words appear in company names but do not imply any specific company, so should be blacklisted
		blacklist = set(("group", "plc", "ord", "mining", "systems", "banking", "value", "retail", "european", "engineering", "industries", "investment", "trust", "american", "international"))
		words = set(words).difference(blacklist)
		#check if each word is a company, check if it is an already followed company so it doesn't waste time querying the db
		for wrd in words:
			out = self.isCompany(wrd)
			if (out[0]):
				self.rec.add(out[1][0])

	def industry_recs(self):
		#get followed companies, their industry and dividend yield
		total_count = len(self.followed)

		industries = (self.followed['industry'].value_counts() / total_count).to_dict()
		#function gets n non-followed companies from database
		#apply function to each industry in dict, with n being the value counts thing
		def get_companies(num, val):
			group_key = next((key for key, value in self.industry_groups.items() if (val in item for item in value)), None)
			if (group_key is None):
				raise KeyError
			results = []
			#get all companies of the selected industry and shuffles
			industry_filtered = self.not_followed[self.not_followed.Industry.isin(industry_groups[group_key])]
			random.shuffle(industry_filtered)

			#adds n companies, ensuring they are not yet followed
			count = 0
			while (num > 0):
				id = industry_filtered[count][0]                         #gets id of next company
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
			while (len(self.rec)<10):
				if (self.not_followed == []):
					break
				x = self.not_followed[self.rand.randint(len(self.not_followed))] #maybe get an order by stock price or summat
				self.rec.add(x)
	
	#check key word is in a not_followed CompanyName
	def isCompany(self, wrd):
		x = self.not_followed[self.not_followed.CompanyName.str.contains(wrd)]['CompanyId']
		return (x is not None), x #isCompany, companyId tuple
		"""
		if (wrd == "d" or wrd == "q"):
			return True
		else:
			return False
		"""
industry_groups = {
    "Finance and Banking": [
        "Insurance - Property & Casualty",
        "Insurance - Diversified",
        "Insurance - Specialty",
        "Banks - Diversified",
        "Banks - Regional",
        "Financial Data & Stock Exchanges",
        "Asset Management",
    ],
    "Technology and Telecommunications": [
        "Telecom Services",
        "Internet Content & Information",
        "Software - Application",
    ],
    "Retail and Consumer Goods": [
        "Discount Stores",
        "Packaged Foods",
        "Food Distribution",
        "Luxury Goods",
        "Beverages - Non-Alcoholic",
        "Beverages - Wineries & Distilleries",
        "Specialty Retail",
        "Apparel Retail",
        "Home Improvement Retail",
        "Grocery Stores",
        "Household & Personal Products",
        "Department Stores",
    ],
    "Manufacturing and Industrial": [
        "Other Industrial Metals & Mining",
        "Copper",
        "Rental & Leasing Services",
        "Aerospace & Defense",
        "Residential Construction",
        "Oil & Gas Integrated",
        "Oil & Gas Refining & Marketing",
        "Industrial Distribution",
        "Specialty Chemicals",
        "Specialty Industrial Machinery",
        "Packaging & Containers",
        "Paper & Paper Products",
        "Furnishings, Fixtures & Appliances",
    ],
    "Healthcare and Pharmaceuticals": [
        "Drug Manufacturers - General",
        "Drug Manufacturers - Specialty & Generic",
        "Medical Instruments & Supplies",
        "Medical Devices",
    ],
    "Real Estate": [
        "REIT - Diversified",
        "REIT - Industrial",
    ],
    "Utilities": [
        "Utilities - Independent Power Producers",
        "Utilities - Regulated Electric",
        "Utilities - Regulated Water",
        "Utilities - Diversified",
    ],
    "Entertainment and Hospitality": [
        "Restaurants",
        "Lodging",
        "Airlines",
        "Gambling",
    ],
    "Other": [
        "Gold",
        "Tobacco",
        "Consulting Services",
        "Conglomerates",
        "Specialty Business Services",
        "Advertising Agencies",
        "Publishing",
        "Other Precious Metals & Mining",
    ]
}

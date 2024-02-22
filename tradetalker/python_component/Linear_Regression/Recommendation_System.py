import pandas as pd

#input, followed companies, liked articles
#output, list of companies (that aren't already being followed)
rec = []

#get liked articles' key words and followed companies
df = {
	"name"    : ["d","g","s"],
	"div"     : [40,10,20],
	"industry": ["coal","food","food"]
}
followed = pd.DataFrame(df)
article_words = [["a","b","c","d","e","f","g"],["d","c","a","q","g","l","o"]]

def isCompany(wrd):
    #return (query company table for wrd)
	if (wrd == "d" or wrd == "q"):
		return True
	else:
		return False

for wrd in article_words:
	if (isCompany(wrd) and not (wrd in followed['name'])):
		rec.append(wrd)

#get followed companies, their industry and dividend yield
div_yields = (followed['div'].value_counts(normalize=True)*10).to_list()
industries = (followed['industry'].value_counts(normalize=True)*10).to_list()

#fucntion gets n non-followed companies from database, specify div/industry
#apply function to each company in dataframe, wtih n being the value counts thing


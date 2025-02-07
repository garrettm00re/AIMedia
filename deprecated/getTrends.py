import pytrends

# get top rising trends in the last 7 days in the 'investing' category

categories = {'investing': 107}
geo = 'US'
tz = 0 # offset from PST in minutes
gprop = [None, 'news']
timeframe = 'today 7-d'

pytrends = pytrends.TrendReq()

trending_searches_df = pytrends.trending_searches(pn='united_states') 

print(trending_searches_df)

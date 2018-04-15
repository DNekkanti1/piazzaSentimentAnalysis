from piazza_api import Piazza
from piazza_api.rpc import PiazzaRPC
import json
import pandas as pd
import re
from datetime import datetime
# from bs4 import BeautifulSoup

# p = PiazzaRPC("jcfrsqcwoyyi5")
# p.user_login()
# print(json.dumps(p.content_get(961), indent=2))

'''
	Variables
'''


p = Piazza()
p.user_login()
user_profile = p.get_user_profile()
# course = p.network("jcfrsqcwoyyi5") # CS186
# course = p.network("j5vqc3j229b6u7") # CS170
course = p.network("ir6ikxxrjtm3j5") # CS61b

posts = course.iter_all_posts(limit=10)
# for post in posts:
# 	print(json.dumps(post, indent=2))

# search_words = ["System R", "Grace Hash Join", "Query Optimization", "IO", "hash join"]
# search_words = ["hash join", "table scan", "sort merge join", "system r", "dependency graph", "hw 4", "query optimization"]
# search_words = ["max flow", "dynamic programming", "dp", "linear programming", "np", "reduction", "greedy", "recurrence", "bipartite"]
search_words = ["asymptotic", "disjoint set", "tree", "hash", "heap", "graph", "traversal", "dynamic programming", "sort", "reduction"]



start_post = 5668
end_post = 5500

n = 50

cids_to_content = {} #dictionary in the form {cid: message content + ' ' + subject content})

# Earliest post date
year = 2017
month = 12
day = 01

# Return object
result = {}
'''
Format for result
{
	word: {
		avg_sentiment: float
		porportion_posts: float
	}
}
'''

for word in search_words:
	result[word] = {
					'total_sentiment': 0.0,
					'average_sentiment': 0.0, 
					'number_posts': 0, 
					'proportion_posts': 0.0}
'''
	Helper Functions
'''
def contains(s, word_list):
    rtn = {}
    for keyword in word_list:
        rtn[keyword] = 0
    for w in s.split():
        if w in word_list:
            rtn[w] += 1
    for key,value in sorted(rtn.items(), key=lambda x:-x[1]):
        print("{}: {}".format(key, value))
    return rtn

current_post = start_post

# TODO: search in time range
# for cid in range(current_post, current_post - n, -1):
# while (current_post >= end_post):
for current_post in range(start_post, end_post, -1):
	print("\n")
	print("POST ID: " + str(current_post))
	try:
		post = course.get_post(current_post)
		history = post['history']
		subject = history[0]['subject']
		content = history[0]['content']
		entry = re.sub("<.*?>", "", content + ' ' + subject)
		entry = re.sub("&#34;", "",entry)
		# entry = BeautifulSoup(content + ' ' + subject, "lxml").get_text()
		cids_to_content[str(current_post)] = entry #add post id : content to the dictionary
		current_post -= 1
		n += 1

		# print(post)
		# print(subject)
		# print(content)

		# contained_search_words = contains(subject + " " + content, search_words)
		# for contained in contained_search_words:
		# 	print(contained)

		# print(json.dumps(post['history'], indent=2))
	except:
		current_post -= 1
		continue

all_messages_df = pd.DataFrame({'cids':list(cids_to_content.keys()), 'content':list(cids_to_content.values())})
all_messages_df.set_index('cids')

#read the vaper sentiment analyzer lexicon into a dataframe - there should be one column: the polarities
lex = ''.join(open("vader_lexicon.txt").readlines())
lex_polarities = pd.read_table("vader_lexicon.txt", header=None, delim_whitespace=True, usecols=[0,1])
lex_polarities.set_index(0, inplace=True)
lex_polarities.columns = ['polarity']
lex_polarities['polarity'] = pd.to_numeric(lex_polarities['polarity'], errors='coerce')

# print("cids_to_content")
# print(cids_to_content)
#use the above lexicon to calculate the overall sentiment for each word
#the total sentiment of one post will be the sum of the sentiments of the sentiments of its words

#CLEANING TEXT CONTENT BEFORE SENTIMENT ANALYSIS
#lowercase the message + subject content to match the lowercase lexicon
#replace all punctuation with a single space 
print("content")
print(all_messages_df['content'])
all_messages_df['lower_content'] = [text.lower() for text in all_messages_df['content']]
punct_re = r'[^ \t\n\r\f\va-zA-Z0-9_]'
all_messages_df['no_punc']=[re.sub(punct_re, " ", text) for text in all_messages_df['lower_content']]
#convert content into a tidy format to make sentiments easy to calculate. index is cid of the post
tidy_format = []
print(all_messages_df['no_punc'])

for text, cid in zip(all_messages_df['no_punc'], all_messages_df['cids']):
	split = text.split()
	for i in range(len(split)):
		word = split[i]
		new_row = {} 
		new_row['index'] = cid 
		new_row['num'] = i 
		new_row['word'] = word 
		tidy_format.append(new_row)

print("\n")
print('TIDY FORMAT')
# print(json.dumps(tidy_format, indent=2))
tidy_format = pd.DataFrame.from_dict(tidy_format) 
tidy_format.set_index('index', inplace=True)
# tidy_format.tail()

print(tidy_format.head())

print("\n")
print('lex_polarities')
print(lex_polarities.head())

#find the sentiment of each tweet: we can join the table with the lexicon table.
merged = tidy_format.merge(lex_polarities, how='left', left_on='word', right_index=True) 
merged.sort_index(inplace=True)
merged.fillna(0.0)
grouped = merged.groupby('index')['polarity'].sum()

print("\n")
print('merged')
print(merged.head())

print("\n")
print('grouped')
print(grouped)


all_messages_df['polarity'] = grouped.values
# all_messages_df['polarity'][all_messages_df['cids']==grouped['index']] = grouped['index']
# all_messages_df['polarity'].fillna(0, inplace=True)


print("all_messages_df")
print(all_messages_df)

print("polarity")
print(all_messages_df['polarity'])


for index, row in all_messages_df.iterrows():
	for search_word in search_words:
		text = row['no_punc']
		polarity = row['polarity']
		if search_word in text:
			result[search_word]['total_sentiment'] += polarity
			result[search_word]['number_posts'] += 1

for key in result.keys():
	if result[key]['number_posts'] != 0:
		result[key]['average_sentiment'] = float(result[key]['total_sentiment']) / float(result[key]['number_posts'])
	if n != 0:
		result[key]['proportion_posts'] = float(result[key]['number_posts']) / float(n)

print(json.dumps(result, indent=2))

# contained_search_words = contains(subject + " " + content, search_words)
# 	for contained in contained_search_words:
# 		print(contained)

# print(course.get_post(-1)['history'])

# print("ANALYZING EXAMPLE POST")
# example_post = course.get_post(961)
# print("length: " + str(len(example_post)))
# i = 0
# print(example_post.keys())
# print(example_post['history'])
# for i in range(32):
# 	print("i")
# 	print(example_post[i])

# print(p.content_get(961))
from piazza_api import Piazza
from piazza_api.rpc import PiazzaRPC
import json
import pandas as pd
import re

# p = PiazzaRPC("jcfrsqcwoyyi5")
# p.user_login()
# print(json.dumps(p.content_get(961), indent=2))

p = Piazza()
p.user_login()
user_profile = p.get_user_profile()
course = p.network("jcfrsqcwoyyi5")
course.get_post(961)
posts = course.iter_all_posts(limit=10)
# for post in posts:
# 	print(json.dumps(post, indent=2))

# search_words = ["System R", "Grace Hash Join", "Query Optimization", "IO", "hash join"]
search_words = ["hash", "join"]

cids_to_content = {} #dictionary in the form {cid: message content + ' ' + subject content})


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
	result[word] = {'avg_sentiment': 0.0, 
					'number_posts': 0, 
					'porportion_posts': 0.0}

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

current_post = 961
# TODO: search in time range
for cid in range(961, 950, -1):
	print("\n")
	print("POST ID: " + str(cid))
	post = course.get_post(cid)
	history = post['history']
	subject = history[0]['subject']
	content = history[0]['content']
	cids_to_content[str(cid)] = content + ' ' + subject #add post id : content to the dictionary
	# print(post)
	# print(subject)
	# print(content)

	contained_search_words = contains(subject + " " + content, search_words)
	for contained in contained_search_words:
		print(contained)

	# print(json.dumps(post['history'], indent=2))

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
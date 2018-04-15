from piazza_api import Piazza
from piazza_api.rpc import PiazzaRPC
import json
import pandas as pd

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
all_messages_df = pd.DataFrame({'cids':list(cids_to_content.values()).toarray(), 'content':list(cids_to_content.keys()).toarray()})
all_messages_df.set_index('cids')

#read the vaper sentiment analyzer lexicon into a dataframe - there should be one column: the polarities
lex = ''.join(open("vader_lexicon.txt").readlines())
lex_polarities = pd.read_table("vader_lexicon.txt", header=None, delim_whitespace=True, usecols=[0,1])
lex_polarities.set_index(0, inplace=True)
lex_polarities.columns = ['polarity']
lex_polarities['polarity'] = pd.to_numeric(sent['polarity'], errors='coerce')

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
for cid in range(961, 959, -1):
	print("\n")
	print("POST ID: " + str(cid))
	post = course.get_post(cid)
	history = post['history']
	subject = history[0]['subject']
	content = history[0]['content']
	cids_to_content[post] = content + ' ' + subject #add post id : content to the dictionary
	print(post)
	# print(subject)
	# print(content)

	contained_search_words = containos(subject + " " + content, search_words)
	for contained in contained_search_words:
		print(contained)

	# print(json.dumps(post['history'], indent=2))

#use the above lexicon to calculate the overall sentiment for each word
#the total sentiment of one post will be the sum of the sentiments of the sentiments of its words

#CLEANING TEXT CONTENT BEFORE SENTIMENT ANALYSIS
#lowercase the message + subject content to match the lowercase lexicon
#replace all punctuation with a single space 
all_messages_df['lower_content'] = [text.lower() for text in all_messages_df['content']]
punct_re = r'[^ \t\n\r\f\va-zA-Z0-9_]'
all_messages_df['no_punc']=[re.sub(punct_re, " ", text) for text in trump['lower_content']]
#convert content into a tidy format to make sentiments easy to calculate. index is cid of the post
tidy_format = []
for index, row in all_messages_df.iterrows():
	text = row['no_punc'] 
	split = text.split()
	for i in range(len(split)):
		word = split[i]
		new_row = {} 
		new_row['index'] = index 
		new_row['num'] = i 
		new_row['word'] = word 
		tidy_format.append(new_row)

tidy_format = pd.DataFrame.from_dict(tidy_format) 
tidy_format.set_index('index', inplace=True)
# tidy_format.tail()

#find the sentiment of each tweet: we can join the table with the lexicon table.
merged = tidy_format.merge(lex_polarities, left_on='word', right_index=True) 
merged.sort_index(inplace=True)
grouped = merged.groupby('index')['polarity'].sum()
all_messages_df['polarity'] = grouped
all_messages_df['polarity'].fillna(0, inplace=True)


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
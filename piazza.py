from piazza_api import Piazza
from piazza_api.rpc import PiazzaRPC
import json
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

def containos(s, word_list):
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
	print(post)
	# print(subject)
	# print(content)

	contained_search_words = containos(subject + " " + content, search_words)
	for contained in contained_search_words:
		print(contained)

	# print(json.dumps(post['history'], indent=2))

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
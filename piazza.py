from piazza_api import Piazza
from piazza_api.rpc import PiazzaRPC
import json
from datetime import datetime
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
search_words = ["hash join", "table scan", "hash", "join", "table", "sort merge join"]


result = {}
'''
Format for result
{
	word: {
		avg_sentiment: float
		number_posts: int
		porportion_posts: float
	}
}

'''

for word in search_words:
	result[word] = {'avg_sentiment': 0.0, 
					'number_posts': 0, 
					'porportion_posts': 0.0}

def containos(s, word_list):
    rtn = set()
    # for keyword in word_list:
    #     rtn[keyword] = 0
    for word in word_list:
    	if word in s:
    		rtn.add(word)
    # for w in s.split():
    #     if w in word_list:
    #         # rtn[w] += 1
    #         rtn.add(w)
    # for key,value in sorted(rtn.items(), key=lambda x:-x[1]):
    #     print("{}: {}".format(key, value))
    return rtn

def post_range(course, post_ID, year, month, day):
    assert len(year)==4
    assert len(month)==2
    assert len(day)==2
    try:
        range_beginning = datetime.strptime("{} {} {}".format(year,month,day), '%Y %m %d')
        print(range_beginning)
    except:
        print("enter a proper date!!!")
    latest_date = datetime.MAXYEAR
    # end_range_cid = -1
    while(range_beginning<latest_date):
        try:
            curr_post = course.get_post(post_ID)
            latest_date_string = curr_post['change_log']['when']
            latest_date = datetime.strptime(latest_date_string,"%Y-%m-%dT%H:%M:%S")
            process(curr_post)
            post_ID -= 1
        except:
            print("something is fucked up")
    return post_ID

# def post_range(course, post_ID, year, month, day):
#     assert len(year)==4
#     assert len(month)==2
#     assert len(day)==2
#     try:
#         range_beginning = datetime.strptime("{} {} {}".format(year,month,day), '%Y %m %d')
#         print(range_beginning)
#     except:
#         print("enter a proper date!!!")
#     latest_date = datetime.MAXYEAR
#     while(range_beginning<latest_date):
#         try:
#             curr_post = course.get_post(post_ID)
#             latest_date_string = curr_post['change_log']['when']
#             latest_date = datetime.strptime(latest_date_string,"%Y-%m-%dT%H:%M:%S")
#             process(curr_post)
#             post_ID -= 1
#         except:
#             print("something is fucked up")
#     return

def process(post):
    print("processed")
    return

current_post = 961
# TODO: search in time range
n = 15
for cid in range(current_post, current_post - n, -1):
	print("\n")
	print("POST ID: " + str(cid))
	post = course.get_post(cid)
	history = post['history']
	subject = history[0]['subject']
	content = history[0]['content']
	# print(post)
	# print(subject)
	# print(content)

	contained_search_words = containos(subject + " " + content, search_words)
	for contained in contained_search_words:
		print(contained)
		result[contained]['number_posts'] += 1

	# print(json.dumps(post['history'], indent=2))

for key in result.keys():
	result[key]['porportion_posts'] = float(result[key]['number_posts']) / float(n)

print("RESULT")
print(json.dumps(result, indent=2))

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
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

# current_post = 961
# for cid in range(961, 950, -1):
# 	post = course.get_post(cid)
# 	print(json.dumps(post, indent=2))

print("ANALYZING EXAMPLE POST")
example_post = course.get_post(961)
print("length: " + str(len(example_post)))
# i = 0
print(example_post['history'])
# for i in range(32):
# 	print("i")
# 	print(example_post[i])

# print(p.content_get(961))
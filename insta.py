from instagrapi import Client

print("hi")
cl = Client()
cl.login("testlimoo", "2832318ars")

user_id = cl.user_id_from_username("testlimoo")
res = cl.direct_thread_by_participants(user_ids= [user_id])
print(res)
print("hi")
import json, csv, tweepy, constants, sys

auth = tweepy.OAuthHandler(constants.TWITTER_API_KEY, constants.TWITTER_API_SECRET)
auth.set_access_token(constants.TWITTER_ACCESS_TOKEN, constants.TWITTER_ACCESS_SECRET)

api = tweepy.API(auth)

f = api.get_list_members(list_id=sys.argv[1])

c = csv.writer(open("members.csv", "w+"))

for member in f:
    c.writerow([
        member.name,
        "",
        "",
        "@"+member.screen_name,
        member.followers_count
    ])
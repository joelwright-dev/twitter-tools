import json, csv, tweepy, constants, sys, gspread, pprint
from oauth2client.service_account import ServiceAccountCredentials

personalised_message = "Hey [NAME], I'm a 17 year old entrepreneur building the future of Web 3.0 through my agency. Here's a little information about me:\n• I am currently studying in my final year of schooling 👨🏻‍🎓\n• I love programming and have done so since the age of 12, I know how to produce incredible front ends with functional backends and connect them to the blockchain 👨🏻‍💻\n• I run a Web 3 agency to pay for my dream car (Nissan Skyline GTR R34) and have the best suit at my school formal 🕴🏻\nLet's connect 🤝"

scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]
file_name = 'client_key.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
client = gspread.authorize(creds)

auth = tweepy.OAuthHandler(constants.TWITTER_API_KEY, constants.TWITTER_API_SECRET)
auth.set_access_token(constants.TWITTER_ACCESS_TOKEN, constants.TWITTER_ACCESS_SECRET)

api = tweepy.API(auth)

#f = api.get_list_members(list_id=sys.argv[1],count=200)

sheet = client.open('Web 3 Agency Prospects').sheet1
python_sheet = sheet.get_all_records()
pp = pprint.PrettyPrinter()

preview_sheet = open("preview.csv","w")

def update_followers():
    updates = []
    current_row = 2
    for account in python_sheet:
        try:
            user_data = api.get_user(screen_name=account["Twitter Handle"].replace("@",""))
            updates.append([user_data.followers_count])
            current_row += 1
            print(f"Updated {account['Name']}: {account['Follower Count']} => {user_data.followers_count}")
        except:
            confirm = input(f"Attempting to remove {account['Name']} (Y/N): ")
            if(confirm == "Y"):
                sheet.delete_row(current_row)
                print(f"Removed {account['Name']}")
            else:
                pass
    sheet.update(f"F2:F{current_row}", updates)

def run():
    sheet = client.open('Web 3 Agency Prospects').sheet1
    python_sheet = sheet.get_all_records()
    for account in python_sheet:
        if account["Contacted?"] == "N" and account["Follower Count"] >= 12531:
            print(api.get_direct_messages())

if("-u" in sys.argv):
    update_followers()
elif("-r" in sys.argv):
    run()
import json, csv, tweepy, constants, sys, gspread, pprint
from oauth2client.service_account import ServiceAccountCredentials

personalised_message = "Hey [NAME], I'm a 17 year old entrepreneur building the future of Web 3.0 through my agency. Here's a little information about me:\n\n• I am currently studying in my final year of schooling 👨🏻‍🎓\n• I love programming and have done so since the age of 12, I know how to produce incredible front ends with functional backends and connect them to the blockchain 👨🏻‍💻\n• I run a Web 3 agency to pay for my dream car (Nissan Skyline GTR R34) and have the best suit at my school formal 🕴🏻\n\nI love the content you're putting out and the value you're adding but I've noticed there are a few things you're missing out on which will skyrocket your reach and connection with followers.\n\nLet's connect and discuss these opportunities."

scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]
file_name = 'client_key.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
client = gspread.authorize(creds)

auth = tweepy.OAuthHandler(constants.TWITTER_API_KEY, constants.TWITTER_API_SECRET)
auth.set_access_token(constants.TWITTER_ACCESS_TOKEN, constants.TWITTER_ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True)
tclient = tweepy.Client(
    bearer_token=constants.TWITTER_BEARER_TOKEN,
    consumer_key=constants.TWITTER_API_KEY,
    consumer_secret=constants.TWITTER_API_SECRET,
    access_token=constants.TWITTER_ACCESS_TOKEN,
    access_token_secret=constants.TWITTER_ACCESS_SECRET
)

#f = api.get_list_members(list_id=sys.argv[1],count=200)

pp = pprint.PrettyPrinter()

def update_contacted_prospects():
    sheet = client.open('Web 3 Agency Prospects').sheet1
    python_sheet = sheet.get_all_records()
    current_row = 2
    for prospect in python_sheet:
        print(f"Checking status of f{prospect['Name']}")
        if(prospect["Contacted?"] == "N"):
            if(tclient.get_direct_message_events(participant_id=api.get_user(screen_name=prospect["Twitter Handle"].replace("@","")).id).data != None):
                try:
                    sheet.update(f"B{current_row}", "Y")
                    print(f"Updated contacted status of {prospect['Name']}")
                except:
                    print(f"Failed to update status of {prospect['Name']}")
        current_row += 1

def update_followers():
    sheet = client.open('Web 3 Agency Prospects').sheet1
    python_sheet = sheet.get_all_records()
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
    current_row = 2
    for account in python_sheet:
        if account["Contacted?"] == "N" and account["Follower Count"] >= 12531:
            try:
                api.send_direct_message(recipient_id=api.get_user(screen_name=account["Twitter Handle"].replace("@","")).id, text=personalised_message.replace("[NAME]", account["Name"]))
                sheet.update(f"B{current_row}", "Y")
                print(f"Direct messaged {account['Name']}")
            except:
                print(f"Could not direct message {account['Name']}")
        current_row += 1

def add_members(member_list):
    sheet = client.open('Web 3 Agency Prospects').sheet1
    python_sheet = sheet.get_all_records()
    members = api.get_list_members(list_id=member_list,count=200)
    new_prospects = []
    for member in members:
        if member.name not in python_sheet:
            new_prospects.append([member.name,"N","N",f"@{member.screen_name}",f"https://twitter.com/{member.screen_name}",member.followers_count])
    sheet.append_rows(values=new_prospects, insert_data_option="INSERT_ROWS")

if("-u" in sys.argv):
    update_followers()
elif("-r" in sys.argv):
    run()
elif("-m" in sys.argv):
    add_members(sys.argv[sys.argv.index("-m")+1])
elif("-d" in sys.argv):
    update_contacted_prospects()
elif("-a" in sys.argv):
    update_followers()
    update_contacted_prospects()
    run()
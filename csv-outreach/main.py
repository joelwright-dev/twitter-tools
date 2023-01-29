import json, csv, tweepy, constants, sys, gspread, pprint, logging, openai
from oauth2client.service_account import ServiceAccountCredentials

messages = {
    "L":"Hey [NAME], I'm Joel Wright, 17 year old blockchain enthusiast, developer, and entrepreneur. I'm reaching out regarding a unique opportunity which I'm only giving to one lucky creator, and I'm hoping that's you.\n\nHere's what I'm offering you, completely free of charge:\n➜Personalized artwork, tailored to your liking for your personal brand\n➜A custom NFT collection which gives access to a service of your choice (newsletter, Discord server, etc.)\n➜A minting website for your followers to pay you to have access to your unique membership\n\nHow does this benefit you?\n➜Followers using your NFT as a profile picture boost your reach outside of your followers feeds, and expands into theirs\n➜You determine your mint price so you earn exactly what you want to\n➜Creating a sense of urgency and exclusivity, your followers will become more engaged in your content at the chance to gain access to said membership.\n\nWhy should you trust me?\n➜We both have nothing to lose, I'm starting my Web3 agency and am learning as I go, you aren't paying a dime for my service, and we can both earn in the future.\n➜I have experience developing smart contracts and full stack websites as shown on my GitHub: https://github.com/joelwright-dev\n\nI would love to hear back from you about this opportunity so we can get your collection created and selling to your followers.",
    "I":"Hey [NAME], I'm Joel Wright, 17 year old blockchain enthusiast, developer, and entrepreneur. I'm reaching out regarding a unique opportunity regarding adding a new source of income to your online presence as a creator and leader in the space.\n\nHere's what I'm offering you:\n➜ Personalized artwork, tailored to your liking for your personal brand\n➜ A custom NFT collection which gives access to a service of your choice (newsletter, Discord server, etc.)\n➜ A minting website for your followers to pay you to have access to your unique membership\n\nHow does this benefit you?\n➜ Followers using your NFT as a profile picture boost your reach outside of your followers feeds, and expands into theirs\n➜ You determine your mint price so you earn exactly what you want to\n➜ Creating a sense of urgency and exclusivity, your followers will become more engaged in your content at the chance to gain access to said membership.\n\nWhy should you trust me?\n➜ I earn when you earn. I take a commission of 10% on every mint of your collection, meaning it's in my best interest to make sure your collection is the bomb!\n➜ I have experience developing smart contracts and full stack websites as shown on my GitHub: https://github.com/joelwright-dev\n\nI would love to hear back from you about this opportunity so we can get your collection created and selling to your followers. For more information, read more about our services at threezero.digital and get started by filling out the form.",
    "B":"Hey [NAME], I'm Joel Wright, 17 year old blockchain enthusiast, developer, and entrepreneur. I'm reaching out regarding a unique opportunity regarding adding a new source of income to your online presence as a creator and leader in the space.\n\nHere's what I'm offering you:\n➜ Personalized artwork, tailored to your liking for your personal brand\n➜ A custom NFT collection which gives access to a service of your choice (newsletter, Discord server, etc.)\n➜ A minting website for your followers to pay you to have access to your unique membership\n\nHow does this benefit you?\n➜ Followers using your NFT as a profile picture boost your reach outside of your followers feeds, and expands into theirs\n➜ You determine your mint price so you earn exactly what you want to\n➜ Creating a sense of urgency and exclusivity, your followers will become more engaged in your content at the chance to gain access to said membership.\n\nWhy should you trust me?\n➜ I earn when you earn. I take a commission of 10% on every mint of your collection, meaning it's in my best interest to make sure your collection is the bomb!\n➜ I have experience developing smart contracts and full stack websites as shown on my GitHub: https://github.com/joelwright-dev\n\nI would love to hear back from you about this opportunity so we can get your collection created and selling to your followers. For more information, read more about our services at threezero.digital and get started by filling out the form.",
    "G":"Hey [NAME], I'm Joel Wright, I've noticed you're also a part of the 1% Club by NFT God, I recently joined and love what everyone in the community is building!\n\nI'm looking for creators just like you who are looking to increase their growth and revenue on Twitter.\n\nHere's what I'm offering you:\n➜ Personalized artwork, tailored to your liking for your personal brand\n➜ A custom NFT collection which gives access to a service of your choice (newsletter, Discord server, etc.)\n➜ A minting website for your followers to pay you to have access to your unique membership\n\nHow does this benefit you?\n➜ Followers using your NFT as a profile picture boost your reach outside of your followers feeds, and expands into theirs\n➜ You determine your mint price so you earn exactly what you want to\n➜ Creating a sense of urgency and exclusivity, your followers will become more engaged in your content at the chance to gain access to said membership.\n\nWhy should you trust me?\n➜ I earn when you earn. I take a commission of 10% on every mint of your collection, meaning it's in my best interest to make sure your collection is the bomb!\n➜ I have experience developing smart contracts and full stack websites as shown on my GitHub: https://github.com/joelwright-dev\n\nI would love to hear back from you about this opportunity so we can get your collection created and selling to your followers. For more information, read more about our services at threezero.digital and get started by filling out the form.",
    "T":"Hey [NAME], I love your tweet/thread about ______.\n\nI'm Joel and I help content creators like yourself monetize your audience.\n\nDo you mind if I ask you some questions about your solopreneurship?"
}

chatgpt_prompt = "Generate me a cold message using this template but replace [SYNOPSIS] with a personalized summary of their profile with this information about their profile:\n\n'[BIO]':\n\n'Hey [NAME], I love your content about [SYNOPSIS].\n\nI'm Joel and I help content creators like yourself monetize your audience. Do you mind if I ask you some questions about your online presence?'"

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
    access_token_secret=constants.TWITTER_ACCESS_SECRET,
    wait_on_rate_limit=True
)

openai.api_key = constants.OPENAI_API_KEY

pp = pprint.PrettyPrinter()

def update_contacted_prospects():
    sheet = client.open('Web 3 Agency Prospects').sheet1
    python_sheet = sheet.get_all_records()
    current_row = 2
    updates = []
    print(tclient.get_direct_message_events())
    for prospect in python_sheet:
        print(f"Checking status of {prospect['Name']}")
        if(prospect["Contacted?"] == "N"):
            try:
                if(tclient.get_direct_message_events(participant_id=api.get_user(screen_name=prospect["Twitter Handle"].replace("@","")).id).data != None):
                    # sheet.update(f"B{current_row}", "Y")
                    updates.append(["Y"])
                    print(f"Updated contacted status of {prospect['Name']}")
                else:
                    updates.append(["N"])
                    print(f"Updated contacted status of {prospect['Name']}")
            except Exception as Argument:
                logging.exception(f"Failed to update status of {prospect['Name']}")
                updates.append(["N"])
        else:
            updates.append(["Y"])
            print(f"Updated contacted status of {prospect['Name']}")
        current_row += 1
    sheet.update(f"B2:B{current_row}", updates)

def update_replied_prospects():
    sheet = client.open('Web 3 Agency Prospects').sheet1
    python_sheet = sheet.get_all_records()
    current_row = 2
    updates = []
    #1595676806245683201
    sender = api.get_user(user_id=1595676806245683201)
    for prospect in python_sheet:
        print(f"Checking status of {prospect['Name']}")
        if(prospect["Status (Y/N/P)"] == "N"):
            try:
                data = tclient.get_direct_message_events(participant_id=api.get_user(screen_name=prospect["Twitter Handle"].replace("@","")).id).data
                for index, message in enumerate(data):
                    if(api.get_user(user_id=api.get_direct_message(id=message.id)._json["message_create"]["sender_id"]) != sender):
                        updates.append(["P"])
                        print(f"1 Updated contacted status of {prospect['Name']} to P")
                        break
                    elif(index == len(data)-1):
                        updates.append([prospect["Status (Y/N/P)"]])
                        print(f"2 Updated contacted status of {prospect['Name']} to {prospect['Status (Y/N/P)']}")
                    else:
                        continue
            except Exception as Argument:
                logging.exception(f"Failed to update status of {prospect['Name']}")
                updates.append([prospect["Status (Y/N/P)"]])
        else:
            updates.append([prospect["Status (Y/N/P)"]])
            print(f"3 Updated contacted status of {prospect['Name']} to {prospect['Status (Y/N/P)']}")
        print(updates)
        current_row += 1
    sheet.update(f"C2:C{current_row}", updates)

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

def run(group):
    sheet = client.open('Web 3 Agency Prospects').sheet1
    python_sheet = sheet.get_all_records()
    current_row = 2
    updates = []
    for account in python_sheet:
        if account["Contacted?"] == "N" and account["Group"] == group:
            try:
                #api.create_friendship(screen_name=account["Twitter Handle"].replace("@",""), follow=False)
                api.send_direct_message(recipient_id=api.get_user(screen_name=account["Twitter Handle"].replace("@","")).id, text=messages[group].replace("[NAME]", account["Name"]))
                updates.append(["Y"])
                print(updates)
                print(f"Direct messaged {account['Name']}")
            except Exception as e:
                updates.append([account["Contacted?"]])
                print(f"Could not direct message {account['Name']} - Reason: {e}")
        else:
            updates.append([account["Contacted?"]])
        current_row += 1
    sheet.update(f"B2:B{current_row}", updates)

def run_gpt(group):
    sheet = client.open('Web 3 Agency Prospects').sheet1
    python_sheet = sheet.get_all_records()
    current_row = 2
    updates = []
    for account in python_sheet:
        if account["Contacted?"] == "N" and account["Group"] == group:
            try:
                #api.create_friendship(screen_name=account["Twitter Handle"].replace("@",""), follow=False)
                api.send_direct_message(recipient_id=api.get_user(screen_name=account["Twitter Handle"].replace("@","")).id, text=account["AI Message"])
                updates.append(["A"])
                print(updates)
                print(f"Direct messaged {account['Name']}")
            except Exception as e:
                updates.append([account["Contacted?"]])
                print(f"Could not direct message {account['Name']} - Reason: {e}")
        else:
            updates.append([account["Contacted?"]])
        current_row += 1
    sheet.update(f"B2:B{current_row}", updates)

def generate_gpt(gpt_prompt):
    sheet = client.open('Web 3 Agency Prospects').sheet1
    python_sheet = sheet.get_all_records()
    unique_messages = []
    current_row = 2
    for prospect in python_sheet:
        try:
            bio = api.get_user(screen_name=prospect["Twitter Handle"].replace("@","")).description
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=gpt_prompt.replace("[NAME]",prospect["Name"]).replace("[BIO]",bio),
                temperature=0.5,
                max_tokens=256,
            )
            unique_messages.append([response['choices'][0]["text"].strip()])
            print(response['choices'][0]["text"].strip())
        except:
            print("Failed to generate GPT response")
            unique_messages.append([""])
        current_row += 1
        print(str(current_row) + "/" + str(len(python_sheet)))
    sheet.update(f"H2:h{current_row}", unique_messages)

def add_members(member_list, group):
    sheet = client.open('Web 3 Agency Prospects').sheet1
    python_sheet = sheet.get_all_records()
    members = api.get_list_members(list_id=member_list,count=200)
    new_prospects = []
    for member in members:
        print(f"Adding {member.screen_name}")
        if member.screen_name not in str(python_sheet):
            new_prospects.append([member.name,"N","N",group,f"@{member.screen_name}",f"https://twitter.com/{member.screen_name}",member.followers_count])
            print(f"Added {member.screen_name}")
    sheet.append_rows(values=new_prospects, insert_data_option="INSERT_ROWS")

if("-u" in sys.argv):
    update_followers()
elif("-r" in sys.argv):
    run(sys.argv[sys.argv.index("-r")+1])
elif("-rg" in sys.argv):
    run_gpt(sys.argv[sys.argv.index("-rg")+1])
elif("-m" in sys.argv):
    add_members(sys.argv[sys.argv.index("-m")+1], sys.argv[sys.argv.index("-g")+1])
elif("-d" in sys.argv):
    update_contacted_prospects()
elif("-c" in sys.argv):
    update_replied_prospects()
elif("-g" in sys.argv):
    generate_gpt("Generate me a cold outreach message using this template: 'Hey [NAME], I love [SYNOPSIS].\n\nI'm Joel and I help content creators like yourself monetize your audience. Do you mind if I ask you some questions about your online presence?' \n\n but replace [SYNOPSIS] with a short, personalized summary of their profile with this information from their twitter bio:\n\n'[BIO]'")
elif("-a" in sys.argv):
    update_followers()
    update_contacted_prospects()
    run()
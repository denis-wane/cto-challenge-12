'''
Created on Aug 12, 2017

@author: denis.r.wane
'''
import tweepy
import configparser
import sys

#get twitter connection keys from a file
def getkeys():
    path_input = input("Please specify the path to your key file (see readme file for key file format): ")
    config = configparser.ConfigParser()
    config.read(path_input)
    
    key = config.get("SectionOne","CONSUMER_KEY")
    secret = config.get("SectionOne","CONSUMER_SECRET")
    token = config.get("SectionOne","ACCESS_TOKEN")
    token_secret = config.get("SectionOne","ACCESS_TOKEN_SECRET")
    
    return key, secret, token, token_secret

#authorize the twitter handle using the keys from the getkeys function
#return the authorized tweepy API object
def authorize():
    key, secret, token, token_secret = getkeys()
    auth = tweepy.auth.OAuthHandler(key, secret)
    auth.set_access_token(token, token_secret)
    
    return tweepy.API(auth)

#prompts the user to select the twitter user they are interested in
#expects an authorized tweepy api handle
def select_user(api):
    while True:
        try:
            user_in = input("Please enter the user you're interested in: ")
            user = api_handle.get_user(user_in)
            break
        except:
            again = input("Could not find that user.  Would you like to try again?  Y or N: ")
            if again == 'N':
                sys.exit() 
    
    return user

#prompts the user to pick a list from all that are available
def print_lists(user_lists):
    print("Please select from the following lists: ")
    i = 1
    for list in user_lists:
        print(i, " - ", list.name)
        i+=1

#validates the user list selection (must choose the list number)
def choose_list(user_lists):
    i = 0
    while True:
        try:
            list_input = int(input("Please enter the number of the list you are interested in: "))
            chosen = user_lists[list_input-1]
            break
        except:
            i+=1
            if (i == 1):
                print("Please enter a valid list number!")
            else:
                print("What are you some kind of MO-RON, number only: ") 
    return chosen

#simple function to make sure a Y or N is always entered when prompting for Y/N
def yes_or_no(msg):
    answer = input(msg, " Y or N: ")
    
    while True:
        if answer == 'N':
            break
        elif answer == 'Y': 
            break
        else:
            answer = input("Please enter Y or N: ")
    
    return answer
              
api_handle = authorize()

while True:
    user = select_user(api_handle)

    try:
        lists = api_handle.lists_all(user.screen_name)
    except:
        retry = yes_or_no("Sorry, that user doesn't have any lists!  Would you like to try another twitter handle?")
        if retry == 'N':
            sys.exit()
    else:
        break

print_lists(lists)

chosen_list = choose_list(lists)

follow = yes_or_no("Would you like to follow everyone in ", chosen_list.name, "?")
if follow == 'N':
    print("Okay - you won't follow them!")
    sys.exit()

try: 
    x = 0    
    print("You are now following ", chosen_list.name, " list members: ")
    for mem in tweepy.Cursor(api_handle.list_members, user.screen_name, chosen_list.slug).items():
        api_handle.create_friendship(mem.screen_name)
        print (mem.screen_name)
        x+=1
    print(x, " new friendships were added :) ")
except:
    print("Something went wrong!")
    sys.exit()





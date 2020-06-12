import json, sys, re

# log-generator.py

# Ignores accounts array and collects messages from all accounts.
ALL_ACOUNTS = False
# Which accounts to ignore messages from when ALL_ACCOUNTS is true.
IGNORE = []
# Which accounts' messages to collect when ALL_ACCOUNTS is false.
ACCOUNTS = []


# Add the date & account stamp to each message
STAMP_MESSAGE = False
# Record when a piece of media is shared, or any other action that isn't text.
SHOW_ACTIONS = False

def main(argv):
    if len(argv) <= 1:
        print("Usage: python3 log-generator.py [file]\nFile - Messages json file")
        exit()
    else:
        data = json.load(open(argv[1],"r"))
    file = open("log.txt","w")
    messages = getMessages(getAllAccounts(data) if ALL_ACOUNTS else ACCOUNTS, data)
    for msg in messages:
        file.write(f'{msg}\n')
    
def getMessages(accounts, file):
    for dm in file:
        if STAMP_MESSAGE: yield f'\n=== Conversation with: {"".join(formatParticipants(dm["participants"]))} ==='
        for msg in reversed(dm["conversation"]):
            if msg["sender"] in accounts:
                t = msg["created_at"]
                if SHOW_ACTIONS:
                    if "story_share" in msg:
                        yield generateLog(t,msg,f'--{msg["story_share"]}--')
                    elif "video_call_action" in msg:
                        yield generateLog(t,msg,f'--{msg["video_call_action"]}--')
                    elif "media_owner" in msg:
                        yield generateLog(t,msg,f'--Shared {msg["media_owner"]}\'s post--')
                    elif "media" in msg:
                        yield generateLog(t,msg,"--Shared media--")
                text = msg["text"] if "text" in msg else ""
                if text == "" or text == None: continue
                yield generateLog(t,msg,re.sub(r"[\n]|[\r\n]|[\r]",' ',text))

def generateLog(time, message, text):
    return f'{time[0:10]} | {time[11:19]} <{message["sender"]}>: {text}' if STAMP_MESSAGE else text

def getAllAccounts(file):
    accounts = []
    for i in range(len(file)):
        people = file[i]["participants"]
        for j in range(len(people)):
            if not people[j] in accounts and people[j] not in IGNORE:
                accounts.append(people[j])
    return accounts
    
def formatParticipants(accounts):
    for i in range(len(accounts)):
        if i == len(accounts) - 1:
            yield accounts[i]
        else:
            yield accounts[i] + ", "

if __name__ == "__main__":
    main(sys.argv)
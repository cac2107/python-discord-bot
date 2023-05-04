import re
import constants
import random

def make_message(initial, member):
    games = get_games()
    gamere = re_maker(games)
    finisher = constants.DEFAULT_FINISHER

    word_count = len(initial.split(" "))
    if word_count <= 2:
        return f"That's an awfully short introduction {member.name} but we can't all be Cicero. Welcome to Impera...\n" + finisher

    # Variable Section
    age = get_age(initial)
    military = get_military(initial)
    rules = read_rules(initial)
    interchange = search_interchange(initial)
    customs = search_customs(initial)
    reserve = search_reserve(initial)
    woods = search_woods(initial)
    labs = search_labs(initial)
    teamkill = search_teamkill(initial)
    stoner = search_stoner(initial)
    friends = search_friends(initial)
    groupraid = search_groupraid(initial)
    mmos = search_mmos(initial)
    tarkov = search_tarkov(initial)
    na = search_na(initial)
    eu = search_eu(initial)
    shoreline = search_shoreline(initial)
    factory = search_factory(initial)
    level = search_level(initial)
    teamwork = search_teamwork(initial)
    key = search_everykey(initial)
    usergames = search_games(initial, gamere)
    if usergames is not False:
        usergames = list(set(usergames))

    age_msg = f"rhank you for the description, we have more than a handful of members around {age}!"
    game_msg = ""

    # Primary Area
    primary_check = [(military, constants.MILITARY_MESSAGE), (usergames, game_msg), (customs, constants.CUSTOMS_MESSAGE),
    (reserve, constants.RESERVE_MESSAGE), (woods, constants.WOODS_MESSAGE), (labs, constants.LABS_MESSAGE), (teamkill, constants.TEAMKILL_MESSAGE),
    (stoner, ":peace: Welcome to Impera! :peace:"), (friends, constants.FRIENDS_MESSAGE), (groupraid, constants.GROUPRAID_MESSAGE),
    (mmos, constants.MMO_MESSAGE), (tarkov, constants.TARKOV_MESSAGE), (na, constants.NA_MESSAGE), (eu, constants.EU_MESSAGE)]
    primary_present = check_true(primary_check)

    # Secondary Area
    secondary_check = [(age, age_msg), (rules, constants.RULES_MESSAGE), (interchange, constants.INTERCHANGE_MESSAGE),
    (shoreline, constants.SHORELINE_MESSAGE), (factory, constants.FACTORY_MESSAGE), (level, constants.LEVEL_MESSAGE),
    (teamwork, constants.TEAMWORK_MESSAGE), (key, constants.KEY_MESSAGE)]
    secondary_present = check_true(secondary_check)

    # Checks for having no keywords triggered.
    if primary_present is False and secondary_present is False:
        messages = constants.DEFAULT_MESSAGES
        return messages[random.randint(0, len(messages) - 1)] + "\n" + finisher

    message = ""

    if usergames is not False:
        game_msg += "we have many members who play "
        for i in range(len(usergames)):
            game_msg += (usergames[i].capitalize())
            if len(usergames) > 1 and i == len(usergames) - 2:
                game_msg += ", and "
            elif i != len(usergames) - 1:
                game_msg += ", "
            else:
                game_msg += "!"

    if primary_present:
        message = message_adder(primary_check, message)

    if secondary_present:
        message = message_adder(secondary_check, message)

    return message + f"\n{finisher}"

def get_age(message):
    agestr = re.search("[\d]{2} years old", message.lower())
    if agestr:
        span = agestr.span()
        age = re.findall("[\d]{2}", message[span[0]:span[1]])[0]
        return age
    else:
        return False

def get_military(message):
    with open('branches.txt', 'r') as f:
        branches = f.readlines()
    branch_re = re_maker(branches)
    militarystr = re.findall(branch_re, message.lower())
    return occurance_return(militarystr)

def read_rules(message):
    rules_str = re.search("((read the rules)|reading the rules)", message.lower())
    if rules_str:
        return True
    else:
        return False

def search_games(message, myre):
    games = re.findall(myre, message.lower())
    if len(games) > 0:
        return games
    else:
        return False

# I set this up to be a bit longer than necessary so its format is clearer.
def search_interchange(message):
    # Set the keyword that you want to search for
    keyword = "interchange"
    # re.findall is not as efficient but easier than re.search
    occurances = re.findall(keyword, message.lower())
    # If the keyword is in the message, "occurences" length will be greater than 0
    if len(occurances) > 0:
        return True
    else:
        return False

# Primary
def search_customs(message):
    keywords = re_maker(["customs"])
    occurances = re.findall(keywords, message.lower())
    return occurance_return(occurances)

# Primary
def search_woods(message):
    keywords = re_maker(["woods"])
    occurances = re.findall(keywords, message.lower())
    return occurance_return(occurances)

# Primary
def search_reserve(message):
    keywords = re_maker(["reserve"])
    occurances = re.findall(keywords, message.lower())
    return occurance_return(occurances)

# Secondary
def search_shoreline(message):
    keywords = re_maker(["shoreline"])
    occurances = re.findall(keywords, message.lower())
    return occurance_return(occurances)

# Secondary
def search_factory(message):
    keywords = re_maker(["factory"])
    occurances = re.findall(keywords, message.lower())
    return occurance_return(occurances)

# Primary
def search_labs(message):
    keywords = re_maker(["labs"])
    occurances = re.findall(keywords, message.lower())
    return occurance_return(occurances)

# Secondary
def search_level(message):
    keywords = re_maker(["level [\d]{2}", "lvl [\d]{2}"])
    occurances = re.findall(keywords, message.lower())
    return occurance_return(occurances)

# Secondary
def search_teamwork(message):
    keywords = re_maker(["teamwork based", "teamwork focused", "teamwork oriented"])
    occurances = re.findall(keywords, message.lower())
    return occurance_return(occurances)

# Secondary
def search_everykey(message):
    keywords = re_maker(["every key"])
    occurances = re.findall(keywords, message.lower())
    return occurance_return(occurances)

# Primary
def search_teamkill(message):
    keywords = re_maker(["tk'd", "teamkilled", "team killed", "tkd"])
    occurances = re.findall(keywords, message.lower())
    return occurance_return(occurances)

# Primary
def search_stoner(message):
    keywords = re_maker(["stoner"])
    occurances = re.findall(keywords, message.lower())
    return occurance_return(occurances)

# Primary
def search_friends(message):
    keywords = re_maker(["make new friends"])
    occurances = re.findall(keywords, message.lower())
    return occurance_return(occurances)

# Primary
def search_groupraid(message):
    keywords = re_maker(["group to raid"])
    occurances = re.findall(keywords, message.lower())
    return occurance_return(occurances)

# Primary
def search_mmos(message):
    keywords = re_maker(["several mmos", "many mmos", "a lot of mmos"])
    occurances = re.findall(keywords, message.lower())
    return occurance_return(occurances)

# Primary
def search_tarkov(message):
    keywords = re_maker(["looking to get better at tarky", "looking to get better at tarkov", "looking to get better at eft"])
    occurances = re.findall(keywords, message.lower())
    return occurance_return(occurances)

# Primary
def search_na(message):
    keywords = re_maker(["NA"])
    occurances = re.findall(keywords, message)
    return occurance_return(occurances)

# Primary
def search_eu(message):
    keywords = re_maker(["EU"])
    occurances = re.findall(keywords, message)
    return occurance_return(occurances)

def occurance_return(a_list):
    if len(a_list) > 0:
        return True
    else:
        return False

def get_rules():
    rule1 = "1.) Have fun.\n\t- Do not be toxic.\n\t- If you need to rage, do not direct it at anyone.\n\t- Do not actively attack or be aggressive towards anyone\n"
    rule2 = "2.) You must remain active. If you go inactive for more than a month you will be removed.\n"
    rule3 = "3.) Only post NSFW content in NSFW approved channels.\n"
    rule4 = f"4.) If you have a problem that you cannot resolve easily, submit a complaint form in <#{constants.HUMAN_RESOURCES_CHANNEL}>. If it is an emergency, please message a member of leadership. That's what we're here for!\n"
    rule5 = "5.) Loot goes to the killer, unless decided otherwise before the raid or by the killer himself. Don't be a loot goblin.\n"
    rule6 = "6.) No spamming. No excessive amounts of messages, emojis, capital letters or tagging users or groups.\n"
    rule7 = "7.) If you discuss topics pertaining to gender, sexuality, religion, politics, or race, you will not be defended by Leadership. These topics have no place here, and quickly turn into heated debates that do not belong on this server.\n"
    rule8 = f"8.) No advertising. You can promote your videos or streams in <#{constants.CLIPS_CHANNEL}>. If you wish to be an affiliated streamer, see <#{constants.APPLY_FOR_PROMOTION_CHANNEL}>. No Discord links or Real Money Transactions.\n"
    rules = "**THE RULES:**\n\n" + rule1 + rule2 + rule3 + rule4 + rule5 + rule6 + rule7 + rule8
    
    return rules

def get_kick_msg():
    with open("kick_message.txt") as f:
        return f.read()

def get_games():
    with open("games.txt") as f:
        games = f.readlines()
    return games

def re_maker(a_list):
    myre = "("
    for i in range(len(a_list)):
        myre += a_list[i].strip()
        if i != len(a_list) - 1:
            myre += "|"
    myre += ")"
    return myre

def check_true(a_list):
    for item in a_list:
        if item[0] is True:
            return True
    return False

def message_adder(a_list, message):
    first_msg = ""
    conjunctions = [" Additionally, ", " Also, "]

    for item in a_list:
        if item[0] is not False:
            first_msg = item[1]
            break

    if len(message) == 0:
        if first_msg != constants.STONER_MESSAGE:
            return first_msg.capitalize()
        else:
            print("STONER HERE")
            return first_msg
    else:
        myrando = random.randint(0, 1)
        message += conjunctions[myrando]
        message += first_msg
    
    return message

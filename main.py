# --------------------------
# CMPT310 - Assignment2
# Sen Lin - 301250505
# sla248@sfu.ca
# --------------------------

# object for each rule.
# head - str, body - list[str]
class Rule:
    def __init__(self, head, body):
        self.head = head
        self.body = body


# globalData
knowledgeBase = []


def readFile():
    fileName = input("Please enter file name in the current directory(.txt):")
    try:
        with open(fileName) as f:
            lines = f.read().splitlines()
            print("{0} is opened".format(fileName))
            return lines
    except(FileNotFoundError, IOError):
        print("Files not found, please try again")
        return readFile()


# rules - list[str]
def initKnowledgeBase(rules):
    for r in rules:
        rule = getAlphaList(r)
        knowledgeBase.append(Rule(rule[0], rule[1:]))


# atoms - list[str]
def getAlphaList(atoms):
    return [item for item in atoms if item.isalpha() is True]


# get user
def getUserInputGoal():
    return [input("Please enter a query (an atom), enter non-alphabetical character to exit:")]


# goal - str
# helper to check if item is known fact
def isKnownFact(goal):
    for rule in knowledgeBase:
        if rule.head == goal and len(rule.body) == 0:
            return True
    return False


# list for handling infinite looping.
proving = []


# goals - list[str], proved - dictionary
def solve(goals, proved):
    # handle case when length of goals is 0. (when last item is known fact)
    if len(goals) == 0:
        return True
    goal = goals[0]
    print("Current goals are {0}".format(set(goals)))
    print("  ", "Now proving: ", goal)
    subGoals = goals[1:]

    # if is known fact, add item to proved.
    if isKnownFact(goal):
        print("     ", "{0} is a known fact".format(goal))
        proved[goal] = True
        return solve(subGoals, proved)

    # continue searching if current goal is proved.
    if goal in proved.keys():
        print("Goal {0} was proved".format(goal))
        return True and solve(subGoals, proved)

    # handle case when item is in proving
    # avoid looping by setting looping constraint
    if goal in proving and proving.count(goal) > 3:
        print("Breaking infinite loop")
        return False

    for rule in knowledgeBase:
        if rule.head == goal:
            print("    ->", "{0} can be proved by proving {1}".format(goal, rule.body))
            count = 0
            for item in rule.body:
                if item in proved.keys():
                    count +=1
            if count is not 0 and count == len(rule.body):
                proved[goal] = True
                print("Atom {0} is proved".format(goal))
                return True
            proving.append(goal)
            result = solve(rule.body + subGoals, proved)
            if result:
                proved[goal] = True
                print("Atom {0} is proved".format(goal))
                return True
            if not isKnownFact(rule.body[0]):
                print("Failed to prove {0} by {1}".format(goal, rule.body))
    return False


def initiate():
    rules = readFile()

    initKnowledgeBase(rules)
    while True:
        goals = getUserInputGoal()
        # goal = "a"
        if goals[0].isalpha() is False:
            print("Invalid input, please restart.")
            break
        result = solve(goals, {})
        del proving[:]
        if result:
            print("Goal {0} is proved".format(goals[0]))
            print("Atom {0} is a logical consequence of the set of rules".format(goals[0]))
        else:
            print("Failed to prove goal {0}".format(goals[0]))
            print("Atom {0} is Not a logical consequence of the set of rules".format(goals[0]))
        print("------------------------------------------------")

    return 0


initiate()

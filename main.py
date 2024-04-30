import time
import math
import random

classTypes = ["Mage", "Archer", "Swordsman", "Healer"]
statNames = ["Attack", "Speed", "Defence", "Magic", "Health"]
classStats = [
    [2, 5, 6, 10, 100],
    [3, 10, 5, 5, 100],
    [10, 5, 6, 2, 100],
    [2, 4, 7, 10, 100]
]
userName = ""
userClass = -1
userStats = [0 for i in range(5)]
statAdjustment = [0 for i in range(5)]
userMoney = 500
userStatus = "Good"
userLevel = 0
userExp = 0
currentLocation = "Home"
placesToTravel = [["Royal Palace", "Institute of Magic", "Beasagon", "Home"], [120, 100, 300, 0]]
distanceToHome = 0
activityMenu = ["View Stats", "Travel", "Shop", "Inventory", "Interact"]
itemsToBuy = [["Heal Potion", "Stat Boost", "Weapon", "Teleporter"], [50, 200, 300, 2000]]
itemsToFind = [
    ["Heal Potion", "Stat Boost", "Weapon", "Teleporter", "Everyday Item", "Artifact", "Garbage"],
    [50, 200, 300, 2000, 300, 2000, 0]
]
monsterTypes = [
    ["Slime", "Great Dragon", "Fire Ape", "Ice Bear"],
    # Attack
    [1, 100, 30, 50],
    # Speed
    [80, 30, 70, 50],
    # Defence
    [1, 100, 50, 70],
    # Magic
    [10, 80, 50, 50],
    # Health
    [30, 300, 120, 120]
]
monsterExp = [10, 50, 25, 25]
inventory = ["Heal Potion"]
escapeAttempt = [False, False]
monsterStats = [0 for i in range(5)]
monsterChoice = -1

def indexInList(item, myList):
    foundIndex = -1
    for index in range(len(myList)):
        if item == myList[index]:
            foundIndex = index
            break
    return foundIndex


def listToText(myList):
    finalMessage = '\n'
    for index in range(len(myList)):
        finalMessage += '(' + str(index) + ') ' + myList[index] + '\n'
    return finalMessage


def checkMenuRange(question, myList, isCancelable=False):
    global userName
    index = int(input(question + listToText(myList)))
    while True:
        if isCancelable and index == -1:
            return index
        elif index < 0 or index > len(myList) - 1:
            index = int(input(userName + " is confused! Please give them a valid thing to do!\n"))
        else:
            return index


def starLine(rows, sleepTime):
    stars = '*' * 100
    for i in range(rows):
        print(stars)
    time.sleep(sleepTime)


def printStats(classIndex, stats):
    global statNames, classStats
    for j in range(len(classStats[classIndex])):
        print("\t" + statNames[j] + ": " + str(stats[j]))


def showInventory():
    global inventory
    starLine(1, 0)
    if (len(inventory) < 1):
        print("Inventory is EMPTY!")
        return
    uniqueInventory = list(set(inventory))
    for i in range(len(uniqueInventory)):
        print('(' + str(i) + ') ' + uniqueInventory[i] + ' (x' + str(inventory.count(uniqueInventory[i])) + ')')
    starLine(1, 0)


def shopkeeperName():
    # Change when travel locations are changed.
    global currentLocation, placesToTravel
    shopkeepers = ['Rowan', 'Mrinal', 'Wuqan', 'Kriti']
    index = placesToTravel[0].index(currentLocation)
    return shopkeepers[index]


def useItemMenu():
    global statNames, userName, userStats, statAdjustment, userStatus, currentLocation, placesToTravel, distanceToHome
    global itemsToFind, inventory, escapeAttempt
    showInventory()
    uniqueInventory = list(set(inventory))
    if len(inventory) < 1:
        return
    chosenItem = checkMenuRange("What Item will you use?", uniqueInventory, True)
    if chosenItem == -1:
        return
    itemToUse = indexInList(uniqueInventory[chosenItem], itemsToFind[0])
    if itemToUse == 0:
        if userStatus == "Good":
            print("Heal Potion had no effect!")
        else:
            print(userName + " was healed!!")
            userStatus = "Good"
    elif itemToUse == 1:
        checkStatBoost = checkMenuRange("Which stat would you like to temporarily boost?", ["Attack", "Speed", "Defence", "Magic"])
        numBoost = math.ceil(userStats[checkStatBoost] * .1)
        userStats[checkStatBoost] += numBoost
        statAdjustment[checkStatBoost] += numBoost
        print(statNames[checkStatBoost] + " stat boosted by 10%!")
    elif itemToUse == 2:
        numBoost = math.ceil(userStats[0] * .2)
        userStats[0] += numBoost
        statAdjustment[0] += numBoost
        print("Attack stat boosted by 20%!")
    elif itemToUse == 3:
        checkLocation = checkMenuRange("Which location would you like to teleport to?", placesToTravel[0], True)
        if checkLocation == -1:
            return
        currentLocation = placesToTravel[0][checkLocation]
        distanceToHome = placesToTravel[1][checkLocation]
        escapeAttempt[1] = True
        resetUserStats()
    else:
        print("There is a time and place for every item!")
        starLine(1, 2)
    if itemToUse in range(0, 4):
        print("Current Stats:")
        for i in range(len(statNames)):
            print(statNames[i] + ":" + str(userStats[i]))
        inventory.remove(itemsToFind[0][itemToUse])

def playerAttack():
    global userStatus, userStats, escapeAttempt, monsterStats
    runStat = random.randint(0, 100)
    fightChoice = checkMenuRange("What are you gonna do?", ["Fight", "Item", "Run"])

    if fightChoice == 0:
        attackType = checkMenuRange("Choose an attack!", ["Attack (fist/weapon)", "Magic", "Dodge"])
        monDefPercentage = 1 - monsterStats[2]/12
        damage = userStats[0] * monDefPercentage
        if attackType == 0:
            print("DHISHOOM!!")
            print("Damage " + str(damage))
            monsterStats[4] -= damage
        elif attackType == 1:
            print("SHIOOON!!")
            criticalChance = random.randint(0, 100)
            criticalBonus = 1
            if criticalChance > 70:
                print("CRITICAL HIT!!")
                criticalBonus = 1.4
            damage = userStatus[3] * monDefPercentage * criticalBonus
            print("Damage " + str(damage))
            monsterStats[4] -= damage
        else:
            # Attempt to dodge
            escapeAttempt[0] = True
        print("Monster Health: " + str(monsterStats[4]))
        starLine(1, 2)
    elif fightChoice == 1:
        useItemMenu()
    else:
        # Try to Run
        if (userStats[1]/20)*100 <= runStat:
            print("Got away safely!")
            resetUserStats()
            escapeAttempt[1] = True
            starLine(2, 1)
        else:
            print("Could not escape!")

def monsterAttack():
    global userStatus, userName, userStats, monsterStats, monsterChoice
    if userStatus != "Good":
        userStats[4] -= 5
        print(userName + " health is now " + str(userStats[4]))
    print("Monster Turn")
    starLine(1, 1)
    attackOptionChance = random.randint(0, 100)
    userDefPercentage = 1 - (userStats[2]/20)
    if monsterChoice == 0:
        # Slime
        if attackOptionChance < 45:
            print("Slime liquid thrown!")
            userStats[4] -= (monsterStats[3] * userDefPercentage)
            unluckyChance = random.randint(0, 100)
            if unluckyChance < 30:
                print(userName + " was burned from slime liquid!")
                userStatus = "Injured"
        elif attackOptionChance < 90:
            print("Slime head butted!")
            userStats[4] -= (monsterStats[0] * userDefPercentage)
        else:
            tauntChance = random.randint(0, 100)
            if tauntChance < 10:
                print("Self Heal!")
                monsterStats[4] *= 1.1
            else:
                print("He He you are worse than me!")
    elif monsterChoice == 1:
        # Great Dragon
        if attackOptionChance < 45:
            print("Fire Breadth!")
            userStats[4] -= (monsterStats[3] * userDefPercentage)
            unluckyChance = random.randint(0, 100)
            if unluckyChance < 30:
                print(userName + " was burned!")
                userStatus = "Injured"
        elif attackOptionChance < 90:
            print("Dragon attacked with its tail!")
            userStats[4] -= (monsterStats[0] * userDefPercentage)
        else:
            tauntChance = random.randint(0, 100)
            if tauntChance < 10:
                print("Self Heal!")
                monsterStats[4] *= 1.1
            else:
                print("You Absolute Fool!")
    elif monsterChoice == 2:
        # Fire Ape
        if attackOptionChance < 45:
            print("Fire Breadth!")
            userStats[4] -= (monsterStats[3] * userDefPercentage)
            unluckyChance = random.randint(0, 100)
            if unluckyChance < 30:
                print(userName + " was burned!")
                userStatus = "Injured"
        elif attackOptionChance < 90:
            print("Fire Ape punched!")
            userStats[4] -= (monsterStats[0] * userDefPercentage)
        else:
            tauntChance = random.randint(0, 100)
            if tauntChance < 10:
                print("Self Heal!")
                monsterStats[4] *= 1.1
            else:
                print("LOL you thought you could defeat me!")
    else:
        # Ice Bear
        if attackOptionChance < 45:
            print("Ice Breadth!")
            userStats[4] -= (monsterStats[3] * userDefPercentage)
            unluckyChance = random.randint(0, 100)
            if unluckyChance < 30:
                print(userName + " was frost bitten!")
                userStatus = "Injured"
        elif attackOptionChance < 90:
            print("Ice Bear kicked!")
            userStats[4] -= (monsterStats[0] * userDefPercentage)
        else:
            tauntChance = random.randint(0, 100)
            if tauntChance < 10:
                print("Self Heal!")
                monsterStats[4] *= 1.1
            else:
                print("You Absolute Fool!")
    print(userName + " Health: " + str(userStats[4]))

def resetUserStats():
    global userStats, statAdjustment
    for i in range(len(statAdjustment)):
        userStats[i] -= statAdjustment[i]
        statAdjustment[i] = 0

if __name__ == '__main__':
    # global classTypes, statNames, classStats, userName, userClass, userStats, userMoney, userLevel, userExp
    # global placesToTravel, distanceToHome, activityMenu, itemsToBuy, itemsToFind, monsterTypes, monsterExp, inventory
    # global escapeAttempt, monsterStats, monsterChoice
    userName = input("Hello!! What is your user name?\n").capitalize()
    print("Welcome " + userName + " to this magic world where you will decide how the story will go!!")
    starLine(3, 1)
    for i in range(len(classTypes)):
        print(classTypes[i] + ":")
        printStats(i, classStats[i])
        starLine(1, 1.5)
    userClass = checkMenuRange("What is " + userName + "'s class?", classTypes)
    userStats = classStats[userClass]
    starLine(2, 2)
    print("From now on you will be known as " + userName + " the " + classTypes[userClass])

    # userName = 'Sarah'
    # userClass = 0
    # userStats = classStats[0]

    # Main Story
    mainStory = True
    while mainStory and userStats[4] > 0:
        choice = checkMenuRange("Hey " + userName + "! What would you like to do?", activityMenu)
        if choice == 0:
            printStats(userClass, userStats)
        elif choice == 1:
            travelChoice = checkMenuRange("Where would you like to travel to?", placesToTravel[0], True)
            if travelChoice == -1:
                isTravel = False
            else:
                isTravel = True
                print("And so, " + userName + " set off on the journey to " + placesToTravel[0][travelChoice])
                if placesToTravel[0][travelChoice] == distanceToHome:
                    print("Well that was fast! You are already there!")
                    isTravel = False

            # Travel Loop
            distDivider = random.randint(3, 6)
            distTravelled = math.ceil(placesToTravel[1][travelChoice]/distDivider)
            isTravelNeg = placesToTravel[1][travelChoice] < distanceToHome
            while isTravel and userStats[4] > 0:
                if not isTravelNeg:
                    distanceToHome += distTravelled
                    if distanceToHome >= placesToTravel[1][travelChoice]:
                        print("You have reached " + placesToTravel[0][travelChoice])
                        isTravel = False
                else:
                    distanceToHome -= distTravelled
                    if distanceToHome <= placesToTravel[1][travelChoice]:
                        print("You have reached " + placesToTravel[0][travelChoice])
                        isTravel = False
                if not isTravel:
                    distanceToHome = placesToTravel[1][travelChoice]
                    break

                # random pickup or battle
                if random.randint(0, 100) < 60:
                    inFight = True
                    monsterPercentage = random.randint(0, 100)
                    # Slime 45
                    if monsterPercentage <= 45:
                        monsterChoice = 0
                    # Great Dragon 5
                    elif monsterPercentage <= 50:
                        monsterChoice = 1
                    # Fire Ape 25
                    elif monsterPercentage <= 75:
                        monsterChoice = 2
                    # Ice Bear 25
                    else:
                        monsterChoice = 3
                    starLine(1, 2)
                    print("You have been challenged to fight by " + monsterTypes[0][monsterChoice])
                    starLine(1, 1)
                    monsterStats = [
                        monsterTypes[1][monsterChoice],
                        monsterTypes[2][monsterChoice],
                        monsterTypes[3][monsterChoice],
                        monsterTypes[4][monsterChoice],
                        monsterTypes[5][monsterChoice]
                    ]
                    chanceAdditional = 0
                    currentTurn = -1
                    if userStats[1] > monsterStats[1]:
                        chanceAdditional = random.randint(25, 50)
                    turnChance = 50 + chanceAdditional

                    if random.randint(0, 100) < turnChance:
                        currentTurn *= -1

                    while inFight and userStats[4] > 0:
                        if currentTurn == 1:
                            playerAttack()
                            if escapeAttempt[1]:
                                escapeAttempt[1] = False
                                break
                        else:
                            incChance = 0
                            if userStats[1] > monsterStats[1]:
                                incChance = random.randint(25, 50)
                            dodgeChance = 25 + incChance
                            failChance = random.randint(0, 100)
                            if escapeAttempt[0]:
                                if failChance < dodgeChance:
                                    print(userName + " has narrowly avoided the attack!")
                                else:
                                    print("Dodge failed!!")
                                    monsterAttack()
                                escapeAttempt[0] = False
                            else:
                                monsterAttack()
                        starLine(1, 2)
                        currentTurn *= -1

                        if userStats[4] <= 0:
                            print(userName + " has been bested. May they rest in peace!")

                        if monsterStats[4] <= 0:
                            print(userName + " has defeated the monster " + monsterTypes[0][monsterChoice])
                            resetUserStats()
                            userExp += monsterExp[monsterChoice]
                            print(userName + " has gained " + str(monsterExp[monsterChoice]) + " experience!")
                            starLine(1, 1)
                            if userExp % ((userLevel + 1)*10) == 0:
                                userExp = 0
                                if userLevel < 20:
                                    userLevel += 1
                                    print(userName + " has levelled up! They are now in level " + str(userLevel))
                                    starLine(1, 1)
                                    print("You have 1 new stat point where would you like to use it?")
                                    print("Current Stats:")
                                    printStats(userClass, userStats)
                                    statIncChoice = checkMenuRange("", statNames)
                                    userStats[statIncChoice] += 1
                                    print(statNames[statIncChoice] + ": " + str(userStats[statIncChoice] - 1) + " -> " + str(userStats[statIncChoice]))
                            break
                else:
                    # random pickup
                    starLine(1, 1)
                    print("Travelling.....")
                    starLine(1, 1)
                    pickUpChance = random.randint(0, 100)
                    # Heal Potion 15
                    if pickUpChance < 15:
                        itemFound = itemsToFind[0][0]
                    # Stat Boost 15
                    elif pickUpChance < 30:
                        itemFound = itemsToFind[0][1]
                    # Weapon 10
                    elif pickUpChance < 40:
                        itemFound = itemsToFind[0][2]
                    # Teleporter 5
                    elif pickUpChance < 45:
                        itemFound = itemsToFind[0][3]
                    # Everyday Item 20
                    elif pickUpChance < 65:
                        itemFound = itemsToFind[0][4]
                    # Artifact 5
                    elif pickUpChance < 70:
                        itemFound = itemsToFind[0][5]
                    # Garbage 30
                    else:
                        itemFound = itemsToFind[0][6]

                    print(userName + " has found " + itemFound)
                    addItemCheck = checkMenuRange("Would you like to add this item to your inventory?", ["Yes", "No"])
                    if addItemCheck == 0:
                        print(itemFound + " was added to your inventory.")
                        inventory.append(itemFound)
                    else:
                        print(itemFound + " was discarded.")

                    starLine(1, 1)
                    print(userName + " continues journey!")
                    starLine(1, 1)
        elif choice == 2:
            while True:
                print("Current Balance: $ " + str(userMoney))
                welcome = "Hey I am " + shopkeeperName() + (". Welcome to my shop! How may I help you? Are you looking "
                                                            "to Buy/Sell?")
                shopChoice = checkMenuRange(welcome, ["Buy", "Sell", "Show Inventory"], True)
                if shopChoice == -1:
                    break
                elif shopChoice == 0:
                    # Buy
                    starLine(1, 0)
                    buyChoice = checkMenuRange("What would you like to Buy today then?", itemsToBuy[0])
                    if userMoney - itemsToBuy[1][buyChoice] >= 0:
                        inventory.append(itemsToBuy[0][buyChoice])
                        userMoney -= itemsToBuy[1][buyChoice]
                    else:
                        sorryMessage = ("Sorry you can't afford " + itemsToBuy[0][buyChoice] +
                                        " at the moment. You need $" + str(itemsToBuy[1][buyChoice] - userMoney) +
                                        " more.")
                        print(sorryMessage)
                    starLine(1, 0)
                elif shopChoice == 1:
                    if len(inventory) > 0:
                        showInventory()
                        sellChoice = checkMenuRange("What would you like to sell?", inventory, True)
                        if sellChoice != -1:
                            itemIndex = indexInList(inventory[sellChoice], itemsToFind[0])
                            salePrice = math.floor(itemsToFind[1][itemIndex] * .9)
                            confirmMessage = ("Are you sure you want to sell " + inventory[sellChoice] +
                                              ", our best price is $" + str(salePrice))
                            confirmChoice = checkMenuRange(confirmMessage, ["Yes", "No"])
                            if confirmChoice == 0:
                                userMoney += salePrice
                                inventory.remove(itemsToFind[0][itemIndex])
                                print("Item sold, current balance is $" + str(userMoney))
                            else:
                                print("Okay, your loss then!!")
                    else:
                        print("Sorry, you have nothing to sell!")
                elif shopChoice == 2:
                    showInventory()
        elif choice == 3:
            showInventory()
        elif choice == 4:
            print("Interact")

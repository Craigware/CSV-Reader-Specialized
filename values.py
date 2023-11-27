import csv
import os
clear = lambda: os.system('cls')


def readIndStats():
    with open('./resp.csv', 'r') as f:
        statistics = csv.reader(f, delimiter=" ", quotechar="|")
        responses = []
        for row in statistics:
            split = row[1].split(",")
            responses.append((split[0], split[1:32]))

        for resp in responses:
            for rating in range(len(resp[1])):
                match(resp[1][rating].lower()):
                    case "favorite":
                        resp[1][rating] = 5
                    case "cool":
                        resp[1][rating] = 4
                    case "average":
                        resp[1][rating] = 3
                    case "mid":
                        resp[1][rating] = 2
                    case "gross":
                        resp[1][rating] = 1

    return responses


def readCreatureStats():
    with open('./resp.csv', 'r') as f:
        statistics = csv.reader(f, delimiter=" ", quotechar="|")
        creatures = next(statistics)

        isOption = False
        options = []
        i = 0
        creature = ""
        while i != len(creatures):
            if "[" in creatures[i]:
                isOption = True
            if isOption:
                creature += creatures[i]
            if "]" in creatures[i]:
                creature = creature.split(",")
                options.append((creature[0],[]))
                creature = ""
                isOption = False
            i += 1

        for row in statistics:
            responses = row[1].split(",")
            i = -1
            for value in responses:
                match(value):
                    case "Favorite":
                        options[i][1].append(5)
                    case "Cool":
                        options[i][1].append(4)
                    case "Average":
                        options[i][1].append(3)
                    case "Mid":
                        options[i][1].append(2)
                    case "Gross":
                        options[i][1].append(1)
                i += 1
    return options


def popularRankings(creatures):
    rankings = []

    for option in creatures:
        overall = 0
        for rating in option[1]:
            overall += rating
        rankings.append((option[0], overall))

    for x in range(len(rankings)):
        for i in range(len(rankings)):
            if rankings[x][1] < rankings[i][1]:
                rankings[x], rankings[i] = rankings[i], rankings[x]

    i = len(creatures)
    for ranking in rankings:
        message = ""
        if i < 10:
            message += " "
        if i >= len(creatures) - 2:
            message += "\033[91m"
        elif i <= 3:
            message += f"\033[92m"
        else:
            message += f"\033[96m"
        message += f"{i}. {ranking[0]}, with {ranking[1]} points \033[0m"
        print(message)
        i -= 1


def countRating(creatures, rating):
    rankings = []

    for option in creatures:
        overall = 0
        for matched_rating in option[1]:
            if rating == matched_rating:
                overall += 1
        rankings.append((option[0], overall))

    for x in range(len(rankings)):
        for i in range(len(rankings)):
            if rankings[x][1] < rankings[i][1]:
                rankings[x], rankings[i] = rankings[i], rankings[x]

    i = len(creatures)
    for ranking in rankings:
        message = ""
        if i < 10:
            message += " "
        if i >= len(creatures) - 2:
            message += "\033[91m"
        elif i <= 3:
            message += f"\033[92m"
        else:
            message += f"\033[96m"
        message += f"{i}. {ranking[0]}, with {ranking[1]} points \033[0m"
        print(message)
        i -= 1


def countAll(creatures):
    for creature in creatures:
        creatureIndRating(creature, True)


def creatureIndRating(creature, printMessage=False):
    favorite = 0; cool = 0; average = 0; mid = 0; gross = 0
    for value in creature[1]:
        match(value):
            case 5:
                favorite += 1
            case 4:
                cool += 1
            case 3:
                average += 1
            case 2:
                mid += 1
            case 1:
                gross += 1

    if (printMessage):
        message = f"{creature[0]} :: \033[94mFavorites: {favorite}, Cools: {cool}, \033[93mAverages: {average}, Mids: {mid}, \033[91mGrosses: {gross}\033[0m"
        print(message)

    return(favorite, cool, average, mid, gross)



def mostControversial(creatures):
    resp = []
    for creature in creatures:
        ratings = creatureIndRating(creature)
        total = 0
        for value in ratings:
            total += value

            positive = ratings[0] + (ratings[1])
            negative = ratings[4] + (ratings[3])
            positive_percentage = round(positive/total * 100, 2)
            negative_percentage = round(negative/total * 100, 2)

        resp.append((creature[0], [abs(positive - negative), positive_percentage, negative_percentage]))

    for x in range(len(resp)):
        for i in range(len(resp)):
            if resp[x][1] > resp[i][1]:
                resp[x], resp[i] = resp[i], resp[x]

    i = len(resp)
    for r in resp:
        message = ""
        if i < 10:
            message += " "

        if i >= len(creatures) - 2:
            message += "\033[91m"
        elif i <= 3:
            message += f"\033[92m"
        else:
            message += f"\033[96m"

        message += f"{i}. {r[0]}, with {r[1][1]}% positive ratings, and {r[1][2]}% negative ratings.\033[0m"
        print(message)
        i -= 1


def overallPerception(responses):
    positive = 0; negative = 0; neutral = 0; overall = 0
    for response in responses:
        for rating in response[1]:
            match(rating):
                case 5:
                    positive += 1
                case 4:
                    positive += 1
                case 3:
                    neutral += 1
                case 2:
                    negative += 1
                case 1:
                    negative += 1
            overall += 1

    positive_percentage = round(positive/overall * 100, 2)
    negative_percentage = round(negative/overall * 100, 2)
    neutral_percentage = round(neutral/overall * 100, 2)
    message = f"{positive_percentage}% positive responses, {neutral_percentage}% neutral responses, {negative_percentage}% negative responses."
    print(message)
    message = f"{positive} positive responses, {neutral} neutral responses, {negative} negative responses."
    print(message)


commands = {
    "Most Popular": ": Get a list of the most popular creatures.",
    "Most Gross": ": Get a list of creatures rated with the most 'gross'.",
    "Most Mid": ": Get a list of creatures rated with the most 'mid'.",
    "Most Average": ": Get a list of creatures rated with the most 'average'.",
    "Most Cool": ": Get a list of creatures rated with the most 'cool'.",
    "Most Favorite": ": Get a list of creatures rated with the most 'favorite'.",
    "All Ratings": ": Get a list of all the ratings supplied to a creature",
    "Most Controversial": ": Get a list of the most controversial creatures",
    "Q": ": Quit."
}

individual_statistics = readIndStats()
creature_statistics = readCreatureStats()

running = True
while(running):
  print("\033[91m----------------------------------------------\033[0m")
  print("Run another command or press q to quit.")
  i = input()
  i = i.lower()

  clear()
  match(i):
    case "help":
      for option in commands:
        print(option, commands[option])
    case "most popular":
      popularRankings(creature_statistics)
    case "most gross":
      countRating(creature_statistics, 1)
    case "most mid":
      countRating(creature_statistics, 2)
    case "most average":
      countRating(creature_statistics, 3)
    case "most cool":
      countRating(creature_statistics, 4)
    case "most favorite":
      countRating(creature_statistics, 5)
    case "all ratings":
      countAll(creature_statistics)
    case "overall perception":
      overallPerception(individual_statistics)
    case "most controversial":
      mostControversial(creature_statistics)
    case "q":
      running = False
      break
    case _:
      print("\033[91m Not a supported command, type help for help.")
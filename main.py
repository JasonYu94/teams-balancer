import random
import math

from all_players import all_players

def extract_player_details_from_sign_up_list(sign_up_list: str, all_players: list[dict]):
    player_names = [string.split('. ')[1] for string in sign_up_list.splitlines()]

    names = []
    plus_ones = []

    for name in player_names:
        if '+' in name:
            plus_ones.append(name)
        else:
            names.append(name)
    
    validate_sign_up_sheet_with_all_players_list(sign_up_sheet_names=names, all_players=all_players)

    players = []
    for player in all_players:
        if player["name"] in names:
            players.append(player)

    plus_ones = map(lambda name: {"name": name, "skill_lvl": DEFAULT_SKILL_LVL}, plus_ones)
    return list(players) + list(plus_ones)


def validate_sign_up_sheet_with_all_players_list(sign_up_sheet_names: list, all_players: list[dict]):
    all_player_names_list = [player["name"] for player in all_players]
    for name in sign_up_sheet_names:
        if not name in all_player_names_list:
            raise(Exception(f"{name} is not in the all_players list. What a plonker!"))


def gaussianise_skill_lvl_of_players(player_details_list: list[dict], sigma: float):
    for player in player_details_list:
        rand_num = random.normalvariate(mu=0, sigma=sigma)
        player["skill_lvl"] += rand_num
    return player_details_list


def generate_teams(player_details_list, num_teams):
    sorted_players = sorted(player_details_list, key=lambda x: x['skill_lvl'])
    teams = [[] for _ in range(num_teams)]  
    l_counter = 0
    r_counter = len(sorted_players) - 1
    add_worst = True
    team_counter = 0

    while l_counter <= r_counter:
        team_index = team_counter % num_teams
        team = teams[team_index]

        if add_worst:
            team.append(sorted_players[l_counter])
            l_counter += 1
        else:
            team.append(sorted_players[r_counter])
            r_counter -= 1
        team_counter += 1
        if team_index == (num_teams-1):
            add_worst = not add_worst
    
    return teams


def calculate_recommended_num_of_teams(player_list):
    return math.floor(len(player_list)/6)


def print_teams(teams, display_player_skill_lvl=False, display_team_sum=True):
    for team_number in range(len(teams)):
        print(f"------------Team {team_number + 1}--------------")
        sum = 0
        for player in teams[team_number]:
            print(f"{player["name"]} ----- {player["skill_lvl"]}") if display_player_skill_lvl else print(player["name"])
            sum += player["skill_lvl"]
        print(f"sum ========================== {sum}") if display_team_sum else None


###################################### FILL IN MISC DETAILS #############################################

sign_up_list = """1. example 1
2. example 2
"""

DEFAULT_SKILL_LVL = 4

#########################################################################################################

if __name__ == "__main__":
    players = extract_player_details_from_sign_up_list(sign_up_list, all_players)
    # players = gaussianise_skill_lvl_of_players(players, sigma=0.3)
    teams = generate_teams(player_details_list=players, num_teams=3) # num_teams=calculate_recommended_num_of_teams(players)
    print(f"number of players: {len(players)}")
    print_teams(teams, display_player_skill_lvl=False, display_team_sum=False)

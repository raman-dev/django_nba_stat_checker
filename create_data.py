import sqlite3
from nba_stat_checker.models import Player,Team,PlayerGeneralStatRecord

def players_add():
    #connect ot the players db
    #add each player to the Player model
    connection = sqlite3.connect('players.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM players')

    for row in cursor:
        #each player record in players create a player object
        p = Player(player_id=row[0],last_name=row[1],first_name=row[2],full_name=row[3],num_stats=row[4],is_active=row[5])
        p.save()
    cursor.close()
    connection.close()

def add_stats():
    connection = sqlite3.connect('players.db')
    cursor = connection.cursor()
    #now grab all players 
    #for each player
    players = Player.objects.all()
    for player in players:
        #each player has n records
        #create n record objects and save them 
        #use the id to grab all rows from players.db gen_stats table
        cursor.execute('SELECT * FROM gen_stats WHERE PLAYER_ID='+str(player.player_id))
        #should get every stat record from gen_stats table
        #now create and object for each record retrieved
        for row in cursor:
            record = row[:6] + (int(row[6]),) + row[7:11] + (float(row[11]),float(row[12]),float(row[13])) + row[14:17] + (float(row[17]),float(row[18])) + row[19:21] + (float(row[21]),float(row[22]),float(row[23]),row[24],row[25])
            #print(record)
            p = PlayerGeneralStatRecord(player=player,stat_cid=record[1],season_id=record[2],team_abbreviation=record[3],player_age=record[4],
            gp=record[5],gs=record[6],minp=record[7],fgm=record[8],fga=record[9],
            fg3m=record[11],fg3a=record[12],fg3_pct=record[13],ftm=record[14],
            fta=record[15],ft_pct=record[16],oreb=record[17],dreb=record[18],reb=record[19],
            ast=record[20],stl=record[21],blk=record[22],tov=record[23],pf=record[24],pts=record[25]
            )
            p.save()

    cursor.close()
    connection.close()


team_names = {
    'ATL':"Atlanta Hawks",
    'BOS':"Boston Celtics",
    'BKN':"Brooklyn Nets",
    'CHA':"Charlotte Hornets",
    'CHI':"Chicago Bulls",
    'CLE':"Cleveland Cavaliers",
    'DAL':"Dallas Mavericks",
    'DEN':"Denver Nuggets",
    'DET':"Detroit Pistons",
    'GSW':"Golden State Warriors",
    'HOU':"Houston Rockets",
    'IND':"Indiana Pacers",
    'LAC':"LA Clippers",
    'LAL':"Los Angeles Lakers",
    'MEM':"Memphis Grizzlies",
    'MIA':"Miami Heat",
    'MIL':"Milwaukee Bucks",
    'MIN':"Minnesota Timberwolves",
    'NOP':"New Orleans Pelicans",
    'NYK':"New York Knicks",
    'OKC':"Oklahoma City Thunder",
    'ORL':"Orlando Magic",
    'PHI':"Philadelphia 76ers",
    'PHX':"Phoenix Suns",
    'POR':"Portland Trail Blazers",
    'SAC':"Sacramento Kings",
    'SAS':"San Antonio Spurs",
    'TOR':"Toronto Raptors",
    'UTA':"Utah Jazz",
    'WAS':"Washington Wizards"
}

#first get all unique values for season_id
def update_team():
    name_list = PlayerGeneralStatRecord.objects.order_by('team_abbreviation').values_list('team_abbreviation').distinct()
    #now with a list of abbreviations take 
    #the original and remove the single quotes from both ends
    transformed = {}
    for name in name_list:
        transformed[name[0]]=(name[0])[2:5]
    print(transformed)
    #for every record in the database
    #for each key in the transformed map change it to the value
    for key,value in transformed.items():
        PlayerGeneralStatRecord.objects.filter(team_abbreviation=key).update(team_abbreviation=value)
        
def create_teams():
    #create a team object for every team in this list
    i = 0
    for key,value in team_names.items():
        t = Team(team_id=i,name=value,team_abbreviation=key)
        t.save()
        i+=1

def player_to_teams():
    #get every record from the general stat database that has season_id 2018-2019
    record_list = PlayerGeneralStatRecord.objects.filter(season_id='2018-19')
    #the higher ocunt on the record
    # record.player_id should have access to this 
    #go through this list and get all 
    #check for any pair of records that have the same player_id
    n = len(record_list)
    i = 0
    record_list_clean = []
    while i < n - 1:
        a = record_list[i]
        j = i + 1
        skip_add = 0
        while j <= n - 1:
            b = record_list[j]
            if a.player_id == b.player_id:
                #if the player_id are the same then compare the xtat_cid
                #the larger stat_cid is the winner
                if a.stat_cid > b.stat_cid:
                    record_list_clean.append(a)
                else:
                    record_list_clean.append(b)
                skip_add =1
                break
            j+=1
        i+=1
        if skip_add == 0:
            record_list_clean.append(a)
    #use record_list_clean
    #now grab the player objects and assign the corresponding team object to the player
    for record in record_list_clean:
        print(record.team_abbreviation)
        team = Team.objects.get(team_abbreviation=record.team_abbreviation)
        player = Player.objects.get(player_id=record.player_id)
        player.team = team
        player.save()
from re import M
from unicodedata import name
from rest_framework import viewsets, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from olympic.api import serializers
from olympic import models
from django.db import connections
import io
import pandas as pd

class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PersonSerializer
    queryset = models.Person.objects.all()
    
    def list(self, request):
        cursor = connections['default'].cursor()
        cursor.execute("""SELECT * FROM olympic_person """)
        response = cursor.fetchall()
        return Response(response)

class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TeamSerializer
    queryset = models.Person.objects.all()
    
    def list(self, request):
        cursor = connections['default'].cursor()
        cursor.execute("""SELECT * FROM olympic_team """)
        response = cursor.fetchall()
        return Response(response)

class NationalityViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.NationalitySerializer
    queryset = models.Person.objects.all()

    def list(self, request):
        cursor = connections['default'].cursor()
        cursor.execute("""SELECT * FROM olympic_nationality """)
        response = cursor.fetchall()
        return Response(response)

class GameViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GameSerializer
    queryset = models.Person.objects.all()

    def list(self, request):
        cursor = connections['default'].cursor()
        cursor.execute("""SELECT * FROM olympic_game """)
        response = cursor.fetchall()
        return Response(response)

class ParticipationGameViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ParticipationGameSerializer
    queryset = models.Person.objects.all()

    def list(self, request):
        cursor = connections['default'].cursor()
        cursor.execute("""SELECT * FROM olympic_participationgame """)
        response = cursor.fetchall()
        return Response(response)


class FileUploadViewSet(ViewSet):
    serializer_class = serializers.UploadFileSerializer

    def list(self, request):
        return Response("GET API")

    def create(self, request):
        serializer_class = serializers.UploadFileSerializer(data=request.data)
        if 'csvFile' not in request.FILES or not serializer_class.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            handleFile(request.FILES['csvFile'].read().decode('utf-8'))
            return Response(status=status.HTTP_201_CREATED)
        
def handleFile(f):
    cursor = connections['default'].cursor()
    print("teams")
    insertTeamsDB(f,cursor)
    connections['default'].commit()
    print("NOC")
    insertNationality(f,cursor)
    connections['default'].commit()
    print("sport")
    insertSportDB(f,cursor)
    connections['default'].commit()
    print("event")
    insertEventDB(f,cursor)
    connections['default'].commit()
    print("person")
    insertPersonDB(f,cursor)
    connections['default'].commit()
    print("game")
    insertGameDB(f,cursor)
    connections['default'].commit()
    print("participation")
    insertParticipationDB(f,cursor)
    connections['default'].commit()

    connections['default'].close() 

def insertParticipationDB(f, cursor):
    participation = pd.read_csv(io.StringIO(f))
    to_participation_db = makePaticipationGames(participation,cursor)
    cursor.executemany("""INSERT INTO olympic_participationgame ( medal, events_id, game_id, person_id) 
                          SELECT ?,?,?,?
                          WHERE NOT EXISTS (SELECT person_id, events_id FROM olympic_participationgame 
                                WHERE person_id = ? AND events_id = ?)""", to_participation_db)

def insertGameDB(f, cursor):
    game   = pd.read_csv(io.StringIO(f),usecols=['Games', 'Year', 'Season']).drop_duplicates()
    to_game_db = makeGameToDb(game)
    cursor.executemany("""INSERT INTO olympic_game ( game, year, season) 
                    SELECT ?,?,?
                    WHERE NOT EXISTS (SELECT game FROM olympic_game 
                                    WHERE game = ?)""", to_game_db)

def insertPersonDB(f, cursor):
    person = pd.read_csv(io.StringIO(f),usecols=['Name','Height','Weight','NOC','Team']).drop_duplicates()
    to_person_db = makePersontoDB(person,cursor)

    cursor.executemany("""INSERT INTO olympic_person ( name, height, weight, nationality_id, team_id) 
                    SELECT ?,?,?,?,?
                    WHERE NOT EXISTS (SELECT name FROM olympic_person 
                                    WHERE name = ?)""", to_person_db)

def insertEventDB(f,cursor):
    event  = pd.read_csv(io.StringIO(f),usecols=['Event']).drop_duplicates()
    to_event_db  = oneDataArray(event,'Event')
    cursor.executemany("""INSERT INTO olympic_event (event) 
                    SELECT (?)
                    WHERE NOT EXISTS (SELECT event FROM olympic_event 
                                    WHERE event = ?)""", to_event_db)

def insertSportDB(f,cursor):
    sport  = pd.read_csv(io.StringIO(f),usecols=['Sport']).drop_duplicates()
    to_sport_db  = oneDataArray(sport,'Sport')
    cursor.executemany("""INSERT INTO olympic_sport (sport) 
                    SELECT (?)
                    WHERE NOT EXISTS (SELECT sport FROM olympic_sport 
                                    WHERE sport = ?)""", to_sport_db)

def insertTeamsDB(f,cursor):
    team   = pd.read_csv(io.StringIO(f),usecols=['Team']).drop_duplicates()
    to_team_db   = oneDataArray(team,'Team')
    
    cursor.executemany("""INSERT INTO olympic_team (team) 
                    SELECT (?)
                    WHERE NOT EXISTS (SELECT team FROM olympic_team 
                                    WHERE team = ?)""", to_team_db)

def insertNationality(f,cursor):
    nation = pd.read_csv(io.StringIO(f),usecols=['NOC']).drop_duplicates()
    to_nation_db = oneDataArray(nation,'NOC')
    cursor.executemany("""INSERT INTO olympic_nationality (nation) 
                    SELECT (?)
                    WHERE NOT EXISTS (SELECT nation FROM olympic_nationality 
                                    WHERE nation = ?)""", to_nation_db)

def oneDataArray(data, colunm):
    data_db   = data[colunm].values
    to_data_db = []
    for i in data_db:
        to_data_db.append((i,i))

    return to_data_db

def makePersontoDB(person, cursor):
    person['Height'] = person['Height'].fillna(0)
    person['Weight'] = person['Weight'].fillna(0)
    name   = person['Name'].values
    height = person['Height'].values
    weight = person['Weight'].values
    nation = person['NOC'].values
    team   = person['Team'].values
    
        
    cursor.execute("SELECT * FROM olympic_nationality")
    nations = cursor.fetchall()

    cursor.execute("SELECT * FROM olympic_team")
    teams = cursor.fetchall()
    
    to_person_db = []
    for i in range(len(nation)):
        nationID = locationID(nations,nation[i])
        teamID= locationID(teams,team[i])
        to_person_db.append((name[i],height[i],weight[i],nationID, teamID, name[i]))

    return to_person_db

def makeGameToDb(game):
    games  = game['Games'].values
    year   = game['Year'].values
    season = game['Season'].values
    to_game_db = []
    for i in range(len(games)):
        to_game_db.append((games[i], str(year[i]),("WT","SM")[season[i] == "Summer"], games[i]))
    return to_game_db

def makePaticipationGames(participation, cursor):
    event  = participation['Event'].values
    game   = participation['Games'].values
    person = participation['Name'].values
    participation['Medal'] = participation['Medal'].fillna("NA")
    medals = participation['Medal'].values
    
    cursor.execute("SELECT * FROM olympic_event")
    events = cursor.fetchall()
    cursor.execute("SELECT id_game, game FROM olympic_game")
    games = cursor.fetchall()
    cursor.execute("SELECT id_person, name FROM olympic_person")
    persons = cursor.fetchall()

    to_participation_db =[]
    for i in range(len(person)):
        if( medals[i] == "NA"):
            medal = "NA"
        else:
            if(medals[i] == 'Bronze'):
                medal = "BZ"
            else:
                if(medals[i] == 'Silver'):
                    medal = "SV"
                else:
                    medal = "GD"
        event_ = locationID(events,event[i])
        person_= locationID(persons,person[i])
        game_  = locationID(games,game[i])
        to_participation_db.append(( medal, event_, game_, person_, person_, event_))

    return to_participation_db

def locationID(data, location):
    for row in data:
         if row[1] == location:
            return row[0]
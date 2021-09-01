from imports import *
from controller.helpers import get_timestamp
from models.match import Match


class Round:
    def __init__(self, name, players_pairs):
        self.players_pairs = players_pairs
        self.matchs = self.create_matchs()
        self.name = name
        self.start_date = get_timestamp()
        self.end_date = ""

    def __str__(self):
        return self.name

    def create_matchs(self):
        matchs = []
        for pair in self.players_pairs:
            matchs.append(Match(pair))
        return matchs

    def mark_as_complete(self):
        self.end_date = get_timestamp()
        print(self.end_date + " : " + self.name + " terminé.")
        print("Rentrer les résultats des matchs:")
        for match in self.matchs:
            match.play_match()

    def get_serialized_round(self):
        return json.dumps({
            "name": self.name,
            "players_pair": self.players_pairs,
            "matchs": [match.get_serialized_match() for match in self.matchs],
            "start_date": self.start_date,
            "end_date": self.end_date,
        })
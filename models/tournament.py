from models.round import Round


class Tournament:
    def __init__(self, name, place, date, time_control, players, nb_rounds=4, desc=""):
        self.name = name
        self.place = place
        self.date = date
        self.time_control = time_control
        self.players = players
        self.nb_rounds = nb_rounds
        self.rounds = []
        self.desc = desc

    def __str__(self):
        return f"Tournoi: {self.name}"

    def create_round(self, round_number):
        players_pairs = self.create_players_pairs(current_round=round_number)
        round = Round("Round " + str(round_number + 1), players_pairs)
        self.rounds.append(round)

    def create_players_pairs(self, current_round):

        # Premier round, on trie les joueurs par rang
        if current_round == 0:
            sorted_players = sorted(self.players, key=lambda x: x.rank, reverse=True)

        # Rounds suivant, on les trie par rapport à leur score total
        else:
            sorted_players = []
            score_sorted_players = sorted(self.players, key=lambda x: x.total_score, reverse=True)

            # Si deux joueurs ont le même score, on les retrie par rapport à leur rang
            for i, player in enumerate(score_sorted_players):
                try:
                    sorted_players.append(player)
                except player.total_score == score_sorted_players[i+1].total_score:
                    if player.rank > score_sorted_players[i+1].rank:
                        hi_player = player
                        lo_player = score_sorted_players[i+1]
                    else:
                        hi_player = score_sorted_players[i+1]
                        lo_player = player
                    sorted_players.append(hi_player)
                    sorted_players.append(lo_player)
                except IndexError:
                    sorted_players.append(player)

        # Split du tri en 2 moitiés
        sup_part = sorted_players[len(sorted_players)//2:]
        inf_part = sorted_players[:len(sorted_players)//2]

        players_pairs = []

        # Création des pairs
        for i, player in enumerate(sup_part):
            a = 0
            while True:
                try:
                    player2 = inf_part[i+a]

                # Bout de liste, on assigne j1 au dernier joueur de la liste inférieure
                except IndexError:
                    player2 = inf_part[i]
                    players_pairs.append((player, player2))

                    # On assigne les joueurs dans leurs liste played_with respective de manière
                    # à indiquer qu'ils ont déjà joués ensemble

                    player.played_with.append(player2)
                    player2.played_with.append(player)
                    break

                # Si j1 a deja joué contre j2, on test avec j3
                if player in player2.played_with:
                    a += 1
                    continue

                # Si les 2 joueurs n'ont jamais joués ensemble, on créé la pair, puis
                # On assigne les joueurs dans leurs liste played_with respective de manière
                # à indiquer qu'ils ont déjà joués ensemble
                else:
                    players_pairs.append((player, player2))
                    player.played_with.append(player2)
                    player2.played_with.append(player)
                    break

        return players_pairs

    def get_rankings(self, by_score=True):

        # Par défaut, on retourne le classement du tournoi par rapport aux points marqués par
        # chaque joueurs
        if by_score:
            sorted_players = sorted(self.players, key=lambda x: x.tournament_score, reverse=True)
        else:
            sorted_players = sorted(self.players, key=lambda x: x.rank, reverse=True)

        return sorted_players

    def get_serialized_tournament(self, save_rounds=False):

        # Si sauvegarde juste après création, les rounds ne sont pas encore créés.
        serialized_tournament = {
            "name": self.name,
            "place": self.place,
            "date": self.date,
            "time_control": self.time_control,
            "players": [player.get_serialized_player(save_turnament_score=True) for player in self.players],
            "nb_rounds": self.nb_rounds,
            "rounds": [round.get_serialized_round() for round in self.rounds],
            "desc": self.desc
        }

        if save_rounds:
            serialized_tournament["rounds"] = [round.get_serialized_round() for round in self.rounds]

        return serialized_tournament

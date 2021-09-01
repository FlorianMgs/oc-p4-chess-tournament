from models.tournament import Tournament
from views.view import View
from views.create_tournament import CreateTournament
from controller.player_controller import create_player, load_players, update_rankings


def create_tournament(loadPlayers=False):

    # Récupération des infos du tournoi
    user_entries = CreateTournament().display_menu()

    # Chargement des joueurs
    if loadPlayers:
        players = load_players()
    # Creation des joueurs
    else:
        print(f"Création de {str(user_entries['nb_players'])} joueurs.")
        players = []
        while len(players) < user_entries['nb_players']:
            players.append(create_player())

    # Creation du tournoi
    tournament = Tournament(
        user_entries['name'],
        user_entries['place'],
        user_entries['date'],
        user_entries['time_control'],
        players,
        user_entries['nb_rounds'],
        user_entries['desc'])

    return tournament


def play_tournament(tournament):

    menu = View()
    print()
    print(f"Début du tournoi {tournament.name}")
    print()

    for i in range(tournament.nb_rounds):

        # Création du round
        tournament.create_round(round_number=i)

        # On joue le round
        current_round = tournament.rounds[-1]
        print()
        print(current_round.start_date + " : Début du " + current_round.name)
        print()

        # Round terminé, on passe au round suivant, on peux aussi mettre à jour les classements manuellement
        while True:
            user_input = menu.get_user_entry(
                msg_display="Que faire ?\n0 - Round suivant\n1 - Mettre à jour les classements\n> ",
                msg_error="Veuillez faire un choix.\n> ",
                value_type="selection",
                assertions=["0", "1"]
            )
            print()

            # Round suivant
            if user_input == "0":
                current_round.mark_as_complete()
                break
            # Changement des rangs
            elif user_input == "1":
                for player in tournament.players:
                    rank = menu.get_user_entry(
                        msg_display=f"Rang de {player}:\n> ",
                        msg_error="Veuillez entrer un nombre entier.",
                        value_type="numeric"
                    )
                    update_rankings(player, rank, score=False)

    # Une fois le tournoi terminé, on retourne les résultats
    return tournament.get_rankings()



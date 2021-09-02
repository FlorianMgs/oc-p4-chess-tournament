from models.tournament import Tournament
from views.view import View
from views.tournament import CreateTournament, LoadTournament
from controller.player_controller import create_player, update_rankings
from controller.database import save_db, load_player, load_tournament


def create_tournament(loadPlayers=False):

    # Récupération des infos du tournoi
    user_entries = CreateTournament().display_menu()

    # Chargement des joueurs
    if loadPlayers:
        # players = load_player()
        pass

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

    # Save du tournoi dans la bdd
    save_db("tournaments", tournament.get_serialized_tournament())

    return tournament


def play_tournament(tournament):

    menu = View()
    print()
    print(f"Début du tournoi {tournament.name}")
    print()

    new_tournament_loaded = False

    while True:

        # Si nouveau tournoi chargé: Calcul des rounds restants à jouer
        a = 0
        if new_tournament_loaded:
            for round in tournament.rounds:
                if round.end_date == "":
                    a += 1
            nb_rounds_to_play = tournament.nb_rounds - a
            new_tournament_loaded = False
        else:
            nb_rounds_to_play = tournament.nb_rounds

        for i in range(nb_rounds_to_play):

            # Création du round
            tournament.create_round(round_number=i+a)

            # On joue le dernier round créé
            current_round = tournament.rounds[-1]
            print()
            print(current_round.start_date + " : Début du " + current_round.name)
            print()

            # Round terminé, on passe au round suivant, on peux aussi mettre à jour les classements manuellement
            while True:
                user_input = menu.get_user_entry(
                    msg_display="Que faire ?\n0 - Round suivant\n1 - Mettre à jour les classements\n2 - Sauvegarder le tournoi\n3 - Charger un tournoi\n> ",
                    msg_error="Veuillez faire un choix.\n> ",
                    value_type="selection",
                    assertions=["0", "1", "2", "3"]
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

                # Sauvegarder le tournoi
                elif user_input == "2":
                    save_db("touranments", tournament.get_serialized_tournament(save_rounds=True))

                # Charger un tournoi
                elif user_input == "3":
                    serialized_loaded_tournament = LoadTournament().display_menu()
                    tournament = load_tournament(serialized_loaded_tournament)
                    new_tournament_loaded = True
                    break

            if new_tournament_loaded:
                break

        if new_tournament_loaded:
            continue

        else:
            break

    # Une fois le tournoi terminé, on retourne les résultats
    return tournament.get_rankings()





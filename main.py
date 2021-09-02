from views.view import View
from views.tournament import LoadTournament
from views.player import CreatePlayer
from controller.database import save_db, load_tournament
from controller.tournament_controller import create_tournament, play_tournament
from controller.player_controller import update_rankings

menu = View()

if __name__ == "__main__":

    # menu principal:
    # 0 - Creer un tournoi
    # 1 - Charger un tournoi
    # 2 - Créer des joueurs
    # q - Quitter

    while True:
        print()
        user_input = menu.get_user_entry(
            msg_display="Que faire ?\n0 - Créer un tournoi\n1 - Charger un tournoi\n2 - Créer des joueurs\nq - Quitter\n> ",
            msg_error="Veuillez entrer une valeur valide",
            value_type="selection",
            assertions=["0", "1", "2", "q"]
        )

        if user_input == "0":
            tournament = create_tournament()
            break
        elif user_input == "1":
            serialized_tournament = LoadTournament().display_menu()
            tournament = load_tournament(serialized_tournament)
            break
        elif user_input == "2":
            user_input = menu.get_user_entry(
                msg_display="Nombre de joueurs à créer:\n> ",
                msg_error="Veuillez entrer une valeur numérique valide ",
                value_type="numeric"
            )
            for i in range(user_input):
                serialized_new_player = CreatePlayer().display_menu()
                save_db("players", serialized_new_player)
        else:
            quit()

    # on joue le tournoi
    print()
    user_input = menu.get_user_entry(
        msg_display="Que faire ?\n0 - Jouer le tournoi\nq - Quitter\n> ",
        msg_error="Veuillez entrer une valeur valide",
        value_type="selection",
        assertions=["0", "q"]
    )

    # on récupère les résultats une fois le tournoi terminé
    if user_input == "0":
        rankings = play_tournament(tournament)
    else:
        quit()

    # on affiche les résultats
    print()
    print(f"Tournoi {tournament.name} terminé !\nRésultats:")
    for i, player in enumerate(rankings):
        print(f"{str(i + 1)} - {player}")

    # on met à jour les classements
    print()
    user_input = menu.get_user_entry(
        msg_display="Mise à jour des classements\n0 - Automatiquement\n1 - Manuellement\nq - Quitter\n> ",
        msg_error="Veuillez entrer une valeur valide",
        value_type="selection",
        assertions=["0", "1", "q"]
    )
    if user_input == "0":
        for i, player in enumerate(rankings):
            update_rankings(player, i+1)

    elif user_input == "1":
        for player in rankings:
            rank = menu.get_user_entry(
                msg_display=f"Rang de {player}:\n> ",
                msg_error="Veuillez entrer un nombre entier.",
                value_type="numeric"
            )
            update_rankings(player, rank)

    else:
        quit()

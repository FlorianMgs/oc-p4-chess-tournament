from controller.database import save_db
from models.player import Player
from views.player import CreatePlayer


def create_player():

    # Récupération des infos du joueur
    user_entries = CreatePlayer().display_menu()

    # Création du joueur
    player = Player(
        user_entries['name'],
        user_entries['first_name'],
        user_entries['dob'],
        user_entries['sex'],
        user_entries['rank'])

    # Sauvegarde du joueur dans la database
    save_db("players", player.get_serialized_player())

    return player


def update_rankings(player, rank, score=True):
    if score:
        player.total_score += player.tournament_score
    player.rank = rank
    print(f"Update du rang de {player}:\nScore total: {player.total_score}\nRang: {player.rank}")


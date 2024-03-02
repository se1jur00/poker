import telebot
from Player import Player
from Game import Game
from config import BOT_TOKEN
bot = telebot.TeleBot(BOT_TOKEN)



all_players = {1157904844:['24efg', 1000], 895228111: ['tankipo', 1000], 455461393: ['tankipo15', 1000]}

games  = {}

@bot.message_handler(commands=['start'])
def start(message):
    print(type(message.from_user.id))
    if message.from_user.id not in all_players:
        bot.send_message(message.from_user.id,'Введите свой никнейм')
        bot.register_next_step_handler(message, create_player)
    else:
        bot.send_message(message.from_user.id,  f'{all_players[message.from_user.id][0]}, Вы уже зарегистрированы.')


@bot.message_handler(commands=['start_game'])
def start_game(message):
    print(games[message.chat.id].players)
    if len(games[message.chat.id].players) >= 2:
        bot.send_message(message.chat.id, 'Игра начинается, идёт раздача карт в личные сообщения.')
        games[message.chat.id].start_round()
        for player in games[message.chat.id].players.values():
            bot.send_message(player.id,','.join([str(card) for card in player.cards]))
        bot.send_message(message.chat.id, f'Малый блайнд - {games[message.chat.id].SB.name}, \nБольшой блайнд - {games[message.chat.id].BB.name}')
        if len(games[message.chat.id].players) > 2:
            bot.send_message(message.chat.id, f'{all_players[games[message.chat.id].next_player][0]}, ожидается ваша ставка')

def create_player(message):
    global all_players
    user_id = message.from_user.id
    nickname = message.text
    coins = 1000
    all_players[user_id] = [nickname, coins]
    bot.send_message(message.from_user.id, 'Регистрация успешна! На вашем счету 1000 монет.')
    print(all_players)

@bot.message_handler(commands=['create_game'])
def create_game(message):
    global games
    if message.chat.id not in games:
        game = Game()
        games[message.chat.id] = game
        bot.send_message(message.chat.id, 'Игра успешно создана')
    else:
        bot.send_message(message.chat.id, 'Игра уже создана')

@bot.message_handler(commands=['bet'])
def bet(message):
    bet = int(telebot.util.extract_arguments(message.text))
    print(bet)
    print(games[message.chat.id].BB.bet)
    if bet >= games[message.chat.id].BB.bet:
        player = games[message.chat.id].players[message.from_user.id]
        games[message.chat.id].place_bet(player, bet)
        games[message.chat.id].get_next_player_id()
        bet_players =  [player for player in games[message.chat.id].players.values() if player.bet > 0]
        if len(bet_players) == len(games[message.chat.id].players):
            games[message.chat.id].lay_cards_on_table()
            bot.send_message(message.chat.id, ','.join(map(str, games[message.chat.id].table)))
        print(games[message.chat.id].bank)

@bot.message_handler(commands=['fold'])
def fold(message):
    games[message.chat.id].kick_player(message.from_user.id)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'start':
        print(message.from_user.id)
        print(all_players)
        if message.from_user.id not in all_players:
            print(1)
            bot.send_message(message.chat.id, 'Зарегистрируйтесь в боте для начала игры.')
        elif len(games[message.chat.id].players) >= 6:
            bot.send_message(message.from_chat.id, 'Игра заполнена')
        else:
            player = Player(message.from_user.id, all_players[message.from_user.id][0], all_players[message.from_user.id][1])
            games[message.chat.id].join(player)








bot.polling(none_stop=True, interval=0)



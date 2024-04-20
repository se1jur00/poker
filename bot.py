import telebot
from Player import Player
from Game import Game
from config import BOT_TOKEN
from telebot import types
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
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_fold = types.KeyboardButton("/fold")
        key_call = types.KeyboardButton("/call")
        keyboard.add(key_fold, key_call)
        bot.send_message(message.chat.id,
                         text =  f'Малый блайнд - {games[message.chat.id].SB.name}, \nБольшой блайнд - {games[message.chat.id].BB.name}')
        bot.send_message(message.chat.id, 'Выберите опцию или сделайте ставку',  reply_markup= keyboard)
        if len(games[message.chat.id].players) > 2:
            bot.send_message(message.chat.id, f'{all_players[games[message.chat.id].next_player["player_id"]][0]}, ожидается ваша ставка')





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
    if message.from_user.id in games[message.chat.id].players:
        bet = int(telebot.util.extract_arguments(message.text))
        print(bet)
        print(games[message.chat.id].BB.bet)
        if bet + games[message.chat.id].players[message.from_user.id].bet >= games[message.chat.id].max_bet:
            player = games[message.chat.id].players[message.from_user.id]
            games[message.chat.id].place_bet(player, bet)
            games[message.chat.id].get_next_player_id()
            bet_players =  [player for player in games[message.chat.id].players.values() if player.bet > 0]
            bets = [player.bet for player in bet_players]
            if len(bet_players) == len(games[message.chat.id].players) :
                if len(set(bets)) == 1:
                    games[message.chat.id].lay_cards_on_table()
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    key_fold = types.KeyboardButton("/fold")
                    key_call = types.KeyboardButton("/call")
                    key_check = types.KeyboardButton("/check")
                    keyboard.add(key_fold, key_call, key_check)
                    bot.send_message(message.chat.id, ','.join(map(str, games[message.chat.id].table)))
                    bot.send_message(message.chat.id,
                                     f'{list(games[message.chat.id].players.values())[0].name}, ожидается ваша ставка',
                                     reply_markup= keyboard)
                else:
                    max_bet = max(bets)
                    next_player = [player for player in bet_players if player.bet < max_bet][0]
                    bot.send_message(message.chat.id, f'{next_player.name}, повысьте или уравняйте ставку')
            else:
                next_player = games[message.chat.id].next_player['object']
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                key_fold = types.KeyboardButton("/fold")
                key_call = types.KeyboardButton("/call")
                keyboard.add(key_fold, key_call, )
                bot.send_message(message.chat.id, f'{next_player.name}, \nсделайте стаку', reply_markup= keyboard)
            print(games[message.chat.id].bank)
    else:
        bot.send_message(message.chat.id, 'Вы не можете сделать ставку')

@bot.message_handler(commands=['fold'])
def fold(message):
    id = message.from_user.id
    name = games[message.chat.id].players[id].name
    games[message.chat.id].kick_player(message.from_user.id)
    bot.send_message(message.chat.id, f'{name} выбыл из игры')


@bot.message_handler(commands=['call'])
def call(message):
    id = message.from_user.id
    next_player_name, player_index = games[message.chat.id].call(id)
    if player_index != 0:
        bot.send_message(message.chat.id, f'{next_player_name}, сделайте ставку ')
    else:
        games[message.chat.id].lay_cards_on_table()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_fold = types.KeyboardButton("/fold")
        key_call = types.KeyboardButton("/call")
        key_check = types.KeyboardButton("/check")
        keyboard.add(key_fold, key_call, key_check)
        bot.send_message(message.chat.id, ','.join(map(str, games[message.chat.id].table)))
        bot.send_message(message.chat.id,
                         f'{list(games[message.chat.id].players.values())[0].name}, сделайте check или ставку',
                         reply_markup=keyboard)




@bot.message_handler(commands=['check'])
def check(message):
    id = message.from_user.id
    status = games[message.chat.id].check(id)
    if status == 'OK':
        next_player = games[message.chat.id].next_player['object']
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_fold = types.KeyboardButton("/fold")
        key_call = types.KeyboardButton("/call")
        key_check = types.KeyboardButton("/check")
        keyboard.add(key_fold, key_call, key_check)
        bot.send_message(message.chat.id, f'{next_player.name}, сделайте check или ставку ', reply_markup=keyboard)
    elif status == 'OK BB':
        games[message.chat.id].lay_cards_on_table()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_fold = types.KeyboardButton("/fold")
        key_call = types.KeyboardButton("/call")
        key_check = types.KeyboardButton("/check")
        keyboard.add(key_fold, key_call, key_check)
        bot.send_message(message.chat.id, ','.join(map(str, games[message.chat.id].table)))
        bot.send_message(message.chat.id,
                         f'{games[message.chat.id].players.values()[0].name}, сделайте check или ставку',
                         reply_markup=keyboard)
    elif status == 'END':
        next_player = games[message.chat.id].next_player['object']
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_fold = types.KeyboardButton("/fold")
        key_call = types.KeyboardButton("/call")
        key_check = types.KeyboardButton("/check")
        keyboard.add(key_fold, key_call, key_check)
        bot.send_message(message.chat.id, ','.join(map(str, games[message.chat.id].table)))
        bot.send_message(message.chat.id, f'{next_player.name}, сделайте check или ставку ', reply_markup=keyboard)

    elif len(status) == 2:
        bot.send_message(message.chat.id, f'выиграл {status[1].name} с комбинацией {status[0]}')
        games.pop(message.chat.id)

    else:
        bot.send_message(message.chat.id, 'вы не можете сделать check')



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



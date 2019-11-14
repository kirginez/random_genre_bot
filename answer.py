def get_artist_lastfm(url):
    import requests
    response = requests.get(url)
    data = response.json()
    top_list = []
    for artist in data['topartists']['artist']:
        top_list.append(artist['name'])
    return(top_list)

def generate_cart(genre):
    answer = ('<b>%s</b>\n') %genre['genre']
    if genre['lastfm']:
        answer += ('\nartists:\n')
        top_list = get_artist_lastfm(genre['lastfm']);
        for artist in top_list:
            answer += ('%s\n') %artist
    if genre['score']:
        import re
        answer += ('\n%s / 5 ❤️\n') %str(genre['score']).replace('.00','')
        answer = re.sub("0\s","",answer)
    return(answer)


def generate_keyboard(genre, user):
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    import mysql.connector
    buttons = []
    if genre['wiki']:
        buttons.append([InlineKeyboardButton(text = 'WIKIPEDIA', url = genre['wiki'])])  
    if genre['bandcamp']:
        buttons.append([InlineKeyboardButton(text = 'BANDCAMP', url = genre['bandcamp'])])

    if genre['user_score']:
        score = genre['user_score']
    else:
        score = 0
    send_score = 0
    score_buttons = []
    for i in range(int(score)):
        send_score += 1
        score_buttons.append(InlineKeyboardButton(text = '❤️', callback_data = genre['key_genre'] +  '|' + str(send_score) + '|' + str(user)))
    for i in range(5 - send_score):
        send_score += 1
        score_buttons.append(InlineKeyboardButton(text = '🖤', callback_data = genre['key_genre'] +  '|' + str(send_score) + '|' + str(user)))
    buttons.append(score_buttons)
    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
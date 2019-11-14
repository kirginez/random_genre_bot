import mysql.connector

def get_random_genre(user):
    import random
    
    con = mysql.connector.connect(host='sql7.freemysqlhosting.net',database='sql7311775',user='sql7311775',password='rSzNAJZgMQ')
    cursor = con.cursor(dictionary=True)
    cursor.execute('SELECT * FROM MAIN ORDER BY RAND() LIMIT 1')
    genre = cursor.fetchall()[0]
    
    frml = "SELECT score FROM scores WHERE key_genre = '%s' AND user_id = '%s';" %(genre['key_genre'], user)
    cursor.execute(frml)
    fet = cursor.fetchall()
    if fet:
        genre['user_score'] = fet[0]['score']
    else:
        genre['user_score'] = None
    return genre

def change_score(score_changer):
    
    genre = score_changer[0]
    current_score = int(score_changer[1])
    user = score_changer[2]

    con = mysql.connector.connect(host='sql7.freemysqlhosting.net',database='sql7311775',user='sql7311775',password='rSzNAJZgMQ')
    cursor = con.cursor(dictionary=True)
    
    frml = "SELECT score FROM scores WHERE key_genre = '%s' AND user_id = '%s';" %(genre, user)
    cursor.execute(frml)

    fet = cursor.fetchall()

    if fet:
        if fet[0]['score'] == current_score:
            frml = "DELETE FROM scores WHERE key_genre = '%s' AND user_id = '%s'" %(genre, user)
            current_score = None
        else:
            frml = "UPDATE scores SET score = %i WHERE key_genre = '%s' AND user_id = '%s'" %(current_score, genre, user)      
    else:
        frml = "INSERT INTO scores (key_genre, user_id, score) VALUES ('%s', '%s', %i)" %(genre, user, current_score)
    cursor.execute(frml)
    con.commit()

    frml = "SELECT AVG (score) FROM scores WHERE key_genre = '%s'" %(genre)
    cursor.execute(frml)
    new_score = cursor.fetchall()[0]['AVG (score)']

    if new_score:
        frml = "UPDATE MAIN SET score = %f WHERE key_genre = '%s'" %(new_score, genre)
        
    else:
        frml = "UPDATE MAIN SET score = Null WHERE key_genre = '%s'" %(genre)
    cursor.execute(frml)
    con.commit()

    frml = "SELECT * FROM MAIN WHERE key_genre = '%s'" %(genre)
    cursor.execute(frml)
    result = cursor.fetchall()[0]

    result['user_score'] = current_score

    con.close()
    return result
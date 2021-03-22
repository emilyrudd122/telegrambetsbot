import sqlite3

conn = sqlite3.connect("mydb.db")
cur = conn.cursor()

BET_STATUSES = ['waiting', 'win', 'lose']


def input_bet(p1, p2, winner, winner_map, coef, bet, post_id, game_type):
    sql = """
        insert into bets(p1,p2,winner,winner_map,coef,bet,status,post_id, game_type)
        values (?,?,?,?,?,?,?,?,?)
    """
    bette = (p1, p2, winner, winner_map, coef, bet, BET_STATUSES[0], post_id, game_type)
    print(bette)
    
    
    cur.execute(sql, bette)
    conn.commit()
    
def get_unmarked_bets():
    res = cur.execute("select * from bets where status=?", (BET_STATUSES[0],))
    result = res.fetchall()
    return result

def get_bet(post_id):
    res = cur.execute("select*from bets where post_id=?", (post_id,))
    result = res.fetchall()
    # print(result)
    return result

def update_bet_status(post_id, status):
    cur.execute("update bets set status=? where post_id=?", (BET_STATUSES[status], post_id,))
    conn.commit()
    
def get_bank():
    res = cur.execute("select razmer from bank")
    result = res.fetchone()[0]
    
    return result
    
# def update_stavki(typee="plus")
#     bank_now = get_bank()
    
#     if typee == 'minus':
#         bank = int(bank_now) - int(summa)
#     elif typee == 'plus':
#         bank = int(bank_now) + int(summa)
        
#     cur.execute("update bank set razmer = ? where id = 1", (str(bank),))
#     conn.commit()
    
    
def update_bank(summa, typee="plus"):
    # esli typee = minus to ot banka otnimaetsya, po defolty idet v plus
    bank_now = get_bank()   
    
    if typee == 'minus':
        bank = int(bank_now) - int(summa)
    elif typee == 'plus':
        bank = int(bank_now) + int(summa)
        
    cur.execute("update bank set razmer = ? where id = 1", (str(bank),))
    conn.commit()
    
     
import sqlite3

conn = sqlite3.connect("mydb.db")
cur = conn.cursor()

BET_STATUSES = ['waiting', 'win', 'lose']

def get_number():
    sql = "select nomer_stavki from nomer"
    res = cur.execute(sql)
    result = res.fetchall()[0][0]
    return result

def input_bet(p1, p2, winner, winner_map, coef, bet, post_id, excel_row):
    sql = """
        insert into bets(p1,p2,winner,winner_map,coef,bet,status,post_id, excel_row)
        values (?,?,?,?,?,?,?,?,?)
    """
    bette = (p1, p2, winner, winner_map, coef, bet, BET_STATUSES[0], post_id, excel_row)
    # print(bette)
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

def update_number():
    next_num = str(int(get_number()) + 1)
    sql = """
            update nomer set nomer_stavki=?
    """
    cur.execute(sql, [(next_num)])
    conn.commit()
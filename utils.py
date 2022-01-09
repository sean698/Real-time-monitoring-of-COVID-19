import time 
import pymysql

def get_time():
    """
    :return: Latest update time
    """
    sql = "select update_time from details order by update_time desc limit 1"
    res = query(sql)
    datetime_obj = res[0][0]
    time_str = datetime_obj.strftime("%Y-%m-%d %X")
    return time_str

def get_conn():
    """
    :return: conn，cursor
    """
    # Create connection to database
    conn = pymysql.connect(host="localhost",
                           user="pig",
                           password="",
                           db="covid_map",
                           charset="utf8")
    # Create cursor
    cursor = conn.cursor()  # Returned data stored in tuple
    return conn, cursor

def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

def query(sql, *args):
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res

def get_c1_data():
    """
    :return: Return data for <div id=c1>
    """
    # Use latest data
    sql = "select sum(confirm)," \
          "(select suspect from history order by ds desc limit 1)," \
          "sum(heal)," \
          "sum(dead) " \
          "from details " \
          "where update_time=(select update_time from details order by update_time desc limit 1) "
    res = query(sql)
    # Since res is a tuple, we return res[0]    res == ((X, X, X, X),)
    return res[0]

def get_c2_data():
    """
    :return: Return data for <div id=c2>
    """
    sql = "select province,sum(confirm) " \
          "from details " \
          "where update_time=(select update_time from details order by update_time desc limit 1) " \
          "group by province"
    res = query(sql)
    return res

def get_l1_data():
	sql = "select ds,confirm,suspect,heal,dead from history"
	res = query(sql)
	return res

def get_l2_data():

	sql = "select ds,confirm_add,suspect_add from history"
	res = query(sql)
	return res	
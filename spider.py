import requests
import json
import time
import traceback
import utils

def get_tencent_data(): 
    """
    :return: Return history data and today's data
    """
    today_url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    history_url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,nowConfirmStatis,provinceCompare'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    }
    # Get today's data
    r = requests.get(today_url, headers)
    res = json.loads(r.text) 
    today_data_all = json.loads(res['data'])
    # Get history data
    r = requests.get(history_url, headers)
    res = json.loads(r.text) 
    history_data_all = res['data']

    # Process history data
    history = {}
    # Details for each day
    for i in history_data_all["chinaDayList"]:
        year = i['y'] + '.'
        ds = year + i["date"]
        # Change the formate of the date otherwise errors would occur when data inserted into database
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y-%m-%d", tup)  
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds] = {"confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead}
    for i in history_data_all["chinaDayAddList"]:
        year = i['y'] + '.'
        ds = year + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y-%m-%d", tup)
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds].update({"confirm_add": confirm, "suspect_add": suspect, "heal_add": heal, "dead_add": dead})


    # Process today's data
    details = []
    # Time for last update
    update_time = today_data_all["lastUpdateTime"]
    # All data for different provinces
    data_province = today_data_all['areaTree'][0]["children"]

    for pro_infos in data_province:
        province_name = pro_infos["name"]  
        for city_infos in pro_infos["children"]:
            city_name = city_infos["name"]
            confirm = city_infos["total"]["confirm"]
            confirm_add = city_infos["today"]["confirm"]
            heal = city_infos["total"]["heal"]
            dead = city_infos["total"]["dead"]
            details.append([update_time, province_name, city_name, confirm, confirm_add, heal, dead])

    return history, details

def update_details():
    """
    Update details table
    :return:
    """
    cursor = None
    conn = None
    try:
        li = get_tencent_data()[1]  # [0] is history dic, [1] is today's data list 
        conn, cursor = utils.get_conn()
        sql = "insert into details(update_time,province,city,confirm,confirm_add,heal,dead) values(%s,%s,%s,%s,%s,%s,%s)"
        sql_query = 'select %s=(select update_time from details order by id desc limit 1)' # Check the latest update time
        cursor.execute(sql_query,li[0][0])
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()} Start updating today's data")
            for item in li:
                cursor.execute(sql, item)
            conn.commit()  # commit update delete insert operations
            print(f"{time.asctime()} Finish update today's data")
        else:
            print(f"{time.asctime()} Latest data already!")
    except:
        traceback.print_exc()
    finally:
        utils.close_conn(conn, cursor)


def insert_history():
    """
    Insert history data, only used in the first time
    :return:
    """
    cursor = None
    conn = None
    try:
        dic = get_tencent_data()[0]  # [0] is history dic, [1] is today's data list 
        print(f"{time.asctime()} Start inserting history data")
        conn, cursor = utils.get_conn()
        sql = "insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for k, v in dic.items():
            # item format {'2020-01-13': {'confirm': 41, 'suspect': 0, 'heal': 0, 'dead': 1}
            cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("suspect"),
                                 v.get("suspect_add"), v.get("heal"), v.get("heal_add"),
                                 v.get("dead"), v.get("dead_add")])

        conn.commit() 
        print(f"{time.asctime()} Finish inserting history data")
    except:
        traceback.print_exc()
    finally:
        utils.close_conn(conn, cursor)


def update_history():
    """
    Updating history table
    :return:
    """
    cursor = None
    conn = None
    try:
        dic = get_tencent_data()[0]  # [0] is history dic, [1] is today's data list 
        print(f"{time.asctime()} Start updating history data")
        conn, cursor = utils.get_conn()
        sql = "insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "select confirm from history where ds=%s"
        for k, v in dic.items():
            # item format {'2020-01-13': {'confirm': 41, 'suspect': 0, 'heal': 0, 'dead': 1}
            if not cursor.execute(sql_query, k):
                cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("suspect"),
                                     v.get("suspect_add"), v.get("heal"), v.get("heal_add"),
                                     v.get("dead"), v.get("dead_add")])
        conn.commit()  
        print(f"{time.asctime()} Finish updating history data")
    except:
        traceback.print_exc()
    finally:
        utils.close_conn(conn, cursor)

if __name__ == '__main__':
    update_details()
    update_history()
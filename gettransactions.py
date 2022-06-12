from time import sleep
import requests
import json
import sqlite3
import telebot
import os
from dotenv import load_dotenv
import datetime


load_dotenv()
API_KEY = os.getenv("API_KEY")

address = 'TSaJqQ1AZ2bEYyqBwBmJqCBSPv8KPRTAdv'
only_confirned = "true"
data_limit = "200"
order_by = "asc"
print(order_by)
#&order_by={order_by}
url = f"https://api.trongrid.io/v1/accounts/{address}/transactions/trc20?only_confirmed={only_confirned}&limit={data_limit}"

headers = {"Accept": "application/json"}

response = requests.get(url, headers=headers)

# contract_address = '41b62570d190572fca2d6f0bd9debdca13f3bbd641'

default_symbol = "USDT"

connection = sqlite3.connect("trondb.db")
cursor = connection.cursor()

table = ''' CREATE TABLE TRANSACTIONS(
            timestamp INTEGER NOT NULL,
            transaction_id VARCHAR(350) NOT NULL,
            symbol CHAR(50) NOT NULL,
            to_address VARCHAR(350) NOT NULL,
            from_address VARCHAR(350) NOT NULL,
            value INTEGER NOT NULL
); '''

try:
    cursor.execute(table)
    print("table created successfully")
except Exception as e:
    print(e)

datas =response.json()


bot = telebot.TeleBot(API_KEY)
bot.config['api_key'] = API_KEY

for data in datas['data']:
    try:
        #print(data)
        # print(data['raw_data']['contract'][0])
        # print(data['raw_data']['contract'][0]['parameter']['value']['amount'])
        # print(data['raw_data']['contract'][0]['parameter']['value']['owner_address'])
        # print(data['raw_data']['contract'][0]['parameter']['value']['to_address'])
        timestamp = data['block_timestamp']
        db_selectall = '''
            SELECT timestamp FROM TRANSACTIONS
        '''
        cursor.execute(db_selectall)
        db_timestamps = cursor.fetchall()
        timestamp_list = []        
        
        try:
            for data in db_timestamps:
                print(f"----------------------------------->    Data appended with value {data[0]}")
                timestamp_list.append(data[0])
        except Exception as e:
            print(e)


        print(timestamp_list)
        if timestamp not in timestamp_list:
            transaction_id = data['transaction_id']
            symbol = data['token_info']['symbol']
            from_address = data['from']
            to_address = data['to']
            transaction_type = data['type']
            value = data['value']
            timestamp = data['block_timestamp']
            if symbol == default_symbol:
                my_time = datetime.datetime.utcfromtimestamp(int(timestamp)/1000)
                # print(timestamp)
                insert_data = f"INSERT INTO TRANSACTIONS VALUES ({timestamp},{transaction_id},{symbol},{to_address},{from_address},{value})"
                cursor.execute(insert_data)

                if to_address == address:
                    # print(f"You have successfully received {value} from {from_address} to {to_address} with transaction ID {transaction_id} at {my_time} UTC.")
                    bot.send_message("-1001778640424", f"You have successfully received {value} from {from_address} to {to_address} with transaction ID {transaction_id} at {my_time} UTC.")
                
                if from_address == address:
                    # print(f"You have successfully transfered {value} from {from_address} to {to_address} with transaction ID {transaction_id} at {my_time} UTC.")
                    bot.send_message("-1001778640424", f"You have successfully transfered {value} from {from_address} to {to_address} with transaction ID {transaction_id} at {my_time} UTC.")
    except Exception as e:
        print(e)
        # sleep(40000)

bot.poll()
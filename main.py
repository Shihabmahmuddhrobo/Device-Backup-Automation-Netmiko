import gspread
from netmiko import ConnectHandler
from datetime import datetime
import time
import threading  #implements threading in Python

# getting the current time as a timestamp
start = time.time()


gc = gspread.service_account(filename="credentials.json")

# For Access the  sheet
sheet = gc.open_by_key("17FnwUfTOTWAGiX0FnkMO4OYA3Mbt0b3xG-7-m3NhzNw")
value_list = sheet.sheet1.get_all_values()


def backup(device):
    connection = ConnectHandler(**device)
    print('Entering the enable mode...')
    connection.enable()

    output = connection.send_command('show run')
    # print(output)
    prompt = connection.find_prompt()
    hostname = prompt[0:-1]
    # print(hostname)

    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hours = now.hour

    filename = f'{hostname}_{year}-{month}-{day}-{hours}_backup.txt'
    with open(filename, 'w') as backup:
        backup.write(output)
        print(f'Backup of {hostname} completed successfully')
        print('#' * 30)

    print('Closing connection')
    connection.disconnect()
# creating an empty list (it will store the threads)
threads = list()

for value in value_list[1:]:
    print(value[1])
    print(value[2])
    print(value[3])
    device = {
        'device_type': value[5],
        'host': value[1],
        'username': value[2],
        'password': value[3],
        'port': value[4],  # optional, default 22
        'secret': 'cisco',  # this is the enable password
        'verbose': True  # optional, default False
    }
    # creating a thread for each router that executes the backup function
    th = threading.Thread(target=backup, args=(device,))
    threads.append(th)  # appending the thread to the list

# starting the threads
for th in threads:
    th.start()

# waiting for the threads to finish
for th in threads:
    th.join()

end = time.time()
print(f'Total execution time:{end - start}')




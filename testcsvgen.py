import csv
from datetime import datetime

login = "login"
passwd = "password"

now = datetime.now()
formated_now = now.strftime("%Y%m%dT%H%M")

print(now)
print(formated_now)
filename = "MFC_data_config_{}_{}.csv".format(login,formated_now)
print(filename)

with open(filename, "w", newline="") as file:
    writer = csv.writer(file, dialect="excel")
    writer.writerow([login,passwd])

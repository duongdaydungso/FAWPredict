import pandas as pd
import math
import csv
import datetime
from datetime import date
import sys

weather_table = pd.read_csv("data/weather_data.csv")
regression_table = pd.read_csv("data/regression_data.csv")
faw_table = [[]]
with open("data/faw_data.csv", newline="") as faw_file:
    reader = csv.reader(faw_file, delimiter=',')
    faw_table = [
        [str(x) for x in row] for row in reader
    ]

PUPAL = 7

class FAWPrediction():
    def __init__(self, cur_time, cur_age):
        self.cur_time = cur_time
        self.cur_age = cur_age
        tmp = cur_time.split('-')
        self.cur_date = date(int(tmp[0]), int(tmp[1]), int(tmp[2]))
        return
    def calculate_mode_lookup(self):
        return
    def calculate_mode_regression(self):
        day_index = weather_table[weather_table['datetime'] == self.cur_time].index.values[0]
        temp = int(weather_table.temp[day_index])
        x, y =  regression_table.a_parameter[self.cur_age], regression_table.b_parameter[self.cur_age]
        dev_time = 0
        i = self.cur_age
        cnt = 0
        while(i != PUPAL):
            x, y =  regression_table.a_parameter[i], regression_table.b_parameter[i]
            temp = math.ceil(weather_table.temp[day_index + cnt])
            temp = min(temp, 30)
            dev_time += math.ceil(1 / (x * temp + y))
            i = (i + 1) % 9
            
        dev_day = (self.cur_date) + datetime.timedelta(days=dev_time)
        print(dev_day)
        return    
    
cal_mode = ""
cur_time = ""
cur_age = 0
for i in range(len(sys.argv)):
    if(sys.argv[i] == "--mode"): cal_mode = sys.argv[i + 1]
    if(sys.argv[i] == "--date"): cur_time = sys.argv[i + 1]
    if(sys.argv[i] == "--age"): cur_age = int(sys.argv[i + 1])

calculate = FAWPrediction(cur_time, cur_age)
if (cal_mode == "regression"):
    calculate.calculate_mode_regression()
else:
    calculate.calculate_mode_lookup()
"""
using number represent for age:
    0: egg
    1: first instar
    2: second instar
    3: third instar
    4: fourth instar
    5: fifth instar
    6: sixth instar
    7: pupal stage
    8: larval stage
date format: yyyy-mm-dd
"""
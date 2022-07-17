
import pandas as pd
import math
import csv
import datetime
from datetime import date
import sys

from pyparsing import col

weather_table = pd.read_csv("data/weather_data.csv")
regression_table = pd.read_csv("data/regression_data.csv")
faw_table = [[]]
with open("data/faw_data.csv", newline="") as faw_file:
    reader = csv.reader(faw_file, delimiter=',')
    faw_table = [
        [int(x) for x in row] for row in reader
    ]

DEVELOPEMENT_STAGE = [
    'egg', 'instar_1', 'instar_2', 'instar_3', 'instar_4', 'instar_5', 'instar_6', 'larval', 'adult'
]
NUM_STAGE = 8
BASE_TEMPURATURE = 20
            
def get_tempurature(query_time):
    day_index = weather_table[weather_table['datetime'] == query_time].index.values[0]
    temp = math.ceil(weather_table.temp[day_index])
    return temp
class FAWPrediction():
    def __init__(self, cur_time, cur_age):
        self.cur_time = cur_time
        self.cur_age = cur_age
        tmp = cur_time.split('-')
        self.cur_date = date(int(tmp[0]), int(tmp[1]), int(tmp[2]))
        return
    def calculate_mode_lookup(self):
        age = self.cur_age
        cur_k = 0
        dev_time = 0
        dev_day = self.cur_date
        cur_period = 0
        if(age == NUM_STAGE):
            age = 0
            dev_time = 3
            dev_day = dev_day + datetime.timedelta(dev_time)
            cur_k = get_tempurature(str(dev_day)) - faw_table[1][0]
            print(DEVELOPEMENT_STAGE[age], (dev_day))
        dev_time = 1
        while (age < 8):
            dev_day = dev_day + datetime.timedelta(dev_time)
            temp = get_tempurature(str(dev_day))
            cur_k += temp - faw_table[1][age]
            print
            if(cur_k > faw_table[2][age]):
                age = age + 1
                temp_day = dev_day + datetime.timedelta(dev_time)
                print(DEVELOPEMENT_STAGE[age], temp_day)
        return
    
    def calculate_mode_regression(self):
        
        def calculate_dev_day(stage, temp):
            x, y =  regression_table.a_parameter[stage], regression_table.b_parameter[stage]
            temp = min(temp, 30)
            ans = math.ceil(1 / (x*temp+y))
            if(stage != NUM_STAGE - 1): 
                return ans
            else:        
                sub = 0
                for i in range(0, NUM_STAGE - 2):
                    x, y =  regression_table.a_parameter[i], regression_table.b_parameter[i]
                    sub += 1 / math.ceil(1 / (x*temp+y))
                ans -= sub
                return ans
        
        day_index = weather_table[weather_table['datetime'] == self.cur_time].index.values[0]
        temp = int(weather_table.temp[day_index])
        x, y =  regression_table.a_parameter[self.cur_age], regression_table.b_parameter[self.cur_age]
        dev_time = 0
        i = self.cur_age
        cnt = 0
        dev_day = self.cur_date
        while(i != NUM_STAGE - 1):
            temp = math.ceil(weather_table.temp[day_index + cnt])
            temp = min(temp, 30)
            dev_time = calculate_dev_day(i, temp)
            dev_day = dev_day + datetime.timedelta(days=dev_time)
            print(DEVELOPEMENT_STAGE[i], dev_day)
            i = (i + 1) % NUM_STAGE
        return    
if __name__ == "__main__":
    cal_mode = ""
    cur_time = ""
    location = ""
    cur_age = 0
    for i in range(len(sys.argv)):
        if(sys.argv[i] == "--mode"): cal_mode = sys.argv[i + 1]
        if(sys.argv[i] == "--location"): location = sys.argv[i + 1]
        if(sys.argv[i] == "--date"): cur_time = sys.argv[i + 1]
        if(sys.argv[i] == "--age"): cur_age = int(sys.argv[i + 1])

    if(cal_mode == "" or cur_time == "" or location == ""):
        print("Can't process now")
        exit()

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
    7: larval stage
    8: adult
date format: yyyy-mm-dd
"""
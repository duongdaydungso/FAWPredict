
from numpy import base_repr
import pandas as pd
import math
import csv
import datetime
from datetime import date
import sys

from pyparsing import col

weather_table = pd.read_csv("data/weather_data.csv")
regression_table = pd.read_csv("data/regression_data.csv")
"""
faw_table = [[]]
with open("data/faw_data.csv", newline="") as faw_file:
    reader = csv.reader(faw_file, delimiter=',')
    faw_table = [
        [int(x) for x in row] for row in reader
    ]
"""

DEVELOPEMENT_STAGE = [
    'egg', 'instar_1', 'instar_2', 'instar_3', 'instar_4', 'instar_5', 'instar_6', 'pupal', 'adult'
]
NUM_STAGE = 8
BASE_TEMPURATURE = 20

faw_table = [[], []]

def create_faw_table():
    for i in range(0, NUM_STAGE):
        x, y = regression_table.a_parameter[i], regression_table.b_parameter[i]
        faw_table[0].append(int(-y / x))
        faw_table[1].append(int((BASE_TEMPURATURE - faw_table[0][i]) / (x * BASE_TEMPURATURE + y)))
        if i > 0 and i < NUM_STAGE - 1: 
            faw_table[1][i] += faw_table[1][i - 1]

def get_tempurature(query_time: str):
    day_index = weather_table[weather_table['datetime'] == query_time].index.values[0]
    temp = int(weather_table.temp[day_index])
    return temp

class FAWPrediction():
    
    def __init__(self, cur_time: str, cur_age: int):
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
            cur_k = get_tempurature(str(dev_day)) - faw_table[0][0]
            print(DEVELOPEMENT_STAGE[0], (dev_day))
        dev_time = 1
        while (age < NUM_STAGE):
            dev_day = dev_day + datetime.timedelta(dev_time)
            temp = get_tempurature(str(dev_day))
            cur_k += temp - faw_table[0][age]
            if(cur_k > faw_table[1][age]):
                temp_day = dev_day + datetime.timedelta(dev_time)
                print(DEVELOPEMENT_STAGE[age + 1], temp_day)
                age = age + 1
        return
    
    def calculate_mode_regression(self):
        
        def calculate_dev_time(stage: int, temp: int):
            x, y =  regression_table.a_parameter[stage], regression_table.b_parameter[stage]
            ans = math.ceil(1 / (x*temp+y))
            if(stage != NUM_STAGE - 1): 
                return ans
            else:        
                sub = 0
                for i in range(0, NUM_STAGE - 1):
                    x, y =  regression_table.a_parameter[i], regression_table.b_parameter[i]
                    sub += math.ceil(1 / (x*temp+y))
                ans -= sub
                return ans
        
        dev_time = 3
        age = self.cur_age
        cnt = 0
        dev_day = self.cur_date
        if(age == NUM_STAGE):
            dev_day += datetime.timedelta(dev_time)
            print(DEVELOPEMENT_STAGE[0], dev_day)
            age = 0
        for i in range(age, NUM_STAGE):
            dev_time = calculate_dev_time(i, get_tempurature(str(dev_day)))
            dev_day += datetime.timedelta(dev_time)
            print(DEVELOPEMENT_STAGE[i + 1], dev_day)
        return    

if __name__ == "__main__":
    create_faw_table()
    cal_mode = "lookup"
    cur_time = "2020-09-03"
    location = "vinhphuc"
    cur_age = 8
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
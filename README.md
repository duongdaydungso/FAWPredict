# FAWPredict

Fall-army-worm predict repo

## Setup

1. Clone repo
2. `cd FAWpredict`
3. `pip install -r requirements.txt`

## How to run

Open the terminal and type
  
    python FAWPredict.py --mode [SELECT_MODE] --date [SELECT_DATE] --age [SELECT_AGE]
    
- [SELECT_MODE]: `regression` mode or `lookup` mode
- [SELECT_DATE]: format: yyyy-mm-dd (Example: 2022-04-01)
- [SELECT_AGE]: a number from 0-8 represent for development stages of worm
```   
0: egg
1: first instar
2: second instar
3: third instar
4: fourth instar
5: fifth instar
6: sixth instar
7: pupal stage
8: larval stage
```

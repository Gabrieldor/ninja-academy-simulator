from numpy.random import f, rand
import pandas as pd
import numpy as np
import math
import itertools
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class minion():
    AC = 13
    hp_range = np.array([4])
    hp = 0
    dmg = 6
    slvl = 1
    dlvl = 6
    natk = 1
    entity = 'Minion'
    ecrit = False
    dead = False

class miniBoss():
    AC = 17
    hp_range = np.arange(10,21)
    hp = 0
    dmg = 8
    slvl = 8
    dlvl = 8
    natk = 1
    entity = 'MiniBoss'
    ecrit = False
    dead = False

class boss():
    AC = 16
    hp_range = np.arange(25,101)
    hp = 0
    dmg = 10
    slvl = 8
    dlvl = 10
    natk = 1
    entity = 'Boss'
    ecrit = False
    dead = False

class beginner():
    lvl = 6
    salvl = round(lvl/20)
    AC = 10+salvl
    body = math.ceil(lvl/10)
    hp = 10+body
    max_hp = 10+body
    dmg = 2+math.ceil(lvl/10)
    slvl = math.ceil(lvl/5)+4
    dlvl = 1
    entity = 'Beginner'
    ecrit = False
    dead = False
    natk = 2

class low():
    lvl = 21
    salvl = round(lvl/20)
    AC = 12+salvl
    body = math.ceil(lvl/10)
    hp = 10+body
    max_hp = 10+body
    dmg = 2+math.ceil(lvl/10)
    slvl = math.ceil(lvl/5)
    dlvl = 4
    entity = 'Low'
    ecrit = False
    dead = False
    natk = 2

class mid():
    lvl = 51
    salvl = round(lvl/20)
    AC = 14+salvl
    body = math.ceil(lvl/10)
    hp = 10+body
    max_hp = 10+body
    dmg = 2+math.ceil(lvl/10)
    slvl = math.ceil(lvl/5)
    dlvl = 8
    entity = 'Mid'
    ecrit = False
    dead = False
    natk = 2

class high():
    lvl = 86
    salvl = round(lvl/20)
    AC = 16+salvl
    body = math.ceil(lvl/10)
    hp = 10+body
    max_hp = 10+body
    dmg = 2+math.ceil(lvl/10)
    slvl = math.ceil(lvl/5)
    dlvl = 12
    entity = 'High'
    ecrit = False
    dead = False
    natk = 2

partysize = list(range(2,6))
test2 = ['a','b','c','d']
lvls = [beginner(),low(), mid(), high()]
players = list(itertools.combinations_with_replacement(lvls,4))
bosses = 1
b = boss()
minibosses = np.array([2,3,4,5])
minions = np.arange(4,21)

def get_entities(players):
    entities = []
    for p in players:
        entities.append(p.entity)
    return entities
def get_playerHP(players):
    hps = []
    for p in players:
        hps.append(p.max_hp)
    return hps

def test(times):
    result = []
    enemies = [[b]]
    i=0
    while i < times:
        for player in players:
            for enemy in enemies:
                for l in player:
                    l.hp = l.max_hp
                b.hp = get_max_hp('boss',(get_avg_lvl(player)/4+get_max_lvl(player)/2))
                b.natk = len(player)
                b.dmg = 6+math.floor(get_avg_lvl(player)/10)
                b.AC = 12+math.floor(get_avg_lvl(player)/10)
                b.slvl = math.floor(get_avg_lvl(player)/7)
                c_result = combat(list(player).copy(), enemy.copy())
                c_result.insert(1, b.hp)
                result.append(c_result)
        i+=1
    return result
            

def combat(player, enemies):
    rplayer = tuple(player.copy())
    turns = 1
    while len(enemies) != 0 and len(player) != 0:
        ptarget = enemies[get_HP(enemies)]
        etarget = player[np.random.randint(0,len(player))]
        for lvl in player:
            nopatk = 0
            if len(enemies) == 0:
                break
            while nopatk < lvl.natk:
                if lvl.ecrit is False:
                    atk = roll(lvl.slvl)
                    if atk > ptarget.AC:
                        if np.random.randint(1,11) == 10:
                            ptarget.hp -= np.random.randint(1,lvl.dmg+1)*2
                        else:
                            ptarget.hp -= np.random.randint(1,lvl.dmg+1)
                    else:
                        if np.random.randint(1,11) == 1:
                            lvl.ecrit = True
                        elif np.random.randint(1,11) > 6:
                            ptarget.hp -= math.floor(np.random.randint(1,lvl.dmg+1)/2)
                    if ptarget.hp <= 0:
                        enemies.remove(ptarget)
                        if len(enemies) == 0:
                            break
                        ptarget = enemies[get_HP(enemies)]
                else:
                    lvl.ecrit = False
                nopatk += 1
        for enemy in enemies:
            noatk = 0
            while noatk < enemy.natk:
                if enemy.ecrit is False:
                    atk = roll(enemy.slvl)
                    if atk > etarget.AC:
                        if np.random.randint(1,11) == 10:
                            etarget.hp -= np.random.randint(1,enemy.dmg+1)*2
                        else:
                            etarget.hp -= np.random.randint(1,enemy.dmg+1)
                    else:
                        if np.random.randint(1,11) == 1:
                            enemy.ecrit = True
                        elif np.random.randint(1,11) > 6:
                            etarget.hp -= math.floor(np.random.randint(1,enemy.dmg+1)/2)
                    if etarget.hp <= 0:
                        player.remove(etarget)
                        if len(player) == 0:
                            break
                        etarget = player[np.random.randint(0,len(player))]
                else:
                    enemy.ecrit = False 
                noatk += 1
        turns += 1
            
    if len(player) == 0:
        return ['Unsuccessful',f'{get_playerHP(rplayer)}',turns, f'{get_entities(rplayer)}', b.natk]
    elif len(enemies) == 0:
        return ['Successful',f'{get_playerHP(rplayer)}', turns, f'{get_entities(rplayer)}',b.natk]

def get_max_hp(etype,avg):
    if etype == 'boss':
        return ((math.ceil(avg)+24))
                
def get_HP(enemies):
    hps = []
    for e in enemies:
        hps.append(e.hp)
    return np.argmin(np.array(hps))

def get_avg_lvl(player):
    avg_p_lvl = 0
    for p in player:
        avg_p_lvl += p.lvl
    return avg_p_lvl/len(player)
def get_total_lvl(player):
    avg_p_lvl = 0
    for p in player:
        avg_p_lvl += p.lvl
    return avg_p_lvl
def get_max_lvl(player):
    lvl = []
    for p in player:
        lvl.append(p.lvl)
    return np.max(lvl)

def roll(slvl):
    return np.random.randint(1,21) + slvl

def exportcsv(rdf):
    rdf.to_csv('results.csv', sep=';')
def exporttxt(txt):
    with open('results.txt','w') as f:
        f.write(txt)

def prob(rdf):
    up = []
    sp = []
    for p in rdf['Party'].unique():
        df = rdf[rdf['Party'] == p]
        turnsavg = df['Turns Taken'].mean()
        max = df.count()['Text']
        if "Successful" in df.Text.unique():
            s = df['Text'].value_counts()['Successful']
        else:
            s = 0
        if 'Unsuccessful' in df.Text.unique():
            u = df['Text'].value_counts()['Unsuccessful']
        else:
            u = 0
        up.append((s/max)*100)
        sp.append((u/max)*100)
        #print(f'{p} had {(s/max)*100:.2f}% of Success against {(u/max)*100:.2f}% Unsuccess taking an average of {turnsavg:.2f} turns')
    return up,sp
        
    
result = test(1000)
rdf =  pd.DataFrame(result)
rdf.columns = ['Text','Enemy HP','Player Max HP','Turns Taken','Party','No Atks']
up,sp = prob(rdf)
sns.set(font_scale=0.70)
fig, ax = plt.subplots(ncols=2)
sns.barplot(y=rdf['Party'].unique()[:20],x=up[:20],palette=['blue'], ax=ax[0])
sns.barplot(y=rdf['Party'].unique()[20:],x=up[20:],palette=['blue'], ax=ax[1])
for a in ax:
    a.set_title('Party Against Boss')
    a.set_xlabel('Percentage of Winning')
    a.set_ylabel('Party')
    a.set_xticks(range(0,101,10))
plt.show()
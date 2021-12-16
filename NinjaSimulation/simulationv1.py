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
    entity = 'minion'
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
    entity = 'miniBoss'
    ecrit = False
    dead = False

class boss():
    AC = 21
    hp_range = np.arange(25,101)
    hp = 100
    max_hp = 100
    dmg = 10
    slvl = 12
    dlvl = 10
    natk = 2
    entity = 'boss'
    ecrit = False
    dead = False

class beginner():
    AC = 21
    hp_range = np.arange(11,21)
    hp = 20
    max_hp = 20
    dmg = 4
    slvl = 1
    dlvl = 1
    entity = 'beginner'
    ecrit = False
    dead = False

class low():
    AC = 23
    hp_range = np.arange(14,31)
    hp = 30
    max_hp = 30
    dmg = 8
    slvl = 7
    dlvl = 4
    entity = 'low'
    ecrit = False
    dead = False

class mid():
    AC = 25
    hp_range = np.arange(17,41)
    hp = 40
    max_hp = 40
    dmg = 10
    slvl = 13
    dlvl = 8
    entity = 'mid'
    ecrit = False
    dead = False

class high():
    AC = 27
    hp_range = np.arange(20,51)
    hp = 50
    max_hp = 50
    dmg = 12
    slvl = 19
    dlvl = 12
    entity = 'high'
    ecrit = False
    dead = False

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
                b.hp = b.max_hp
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
                    break
            else:
                lvl.ecrit = False
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
                        break
                else:
                    enemy.ecrit = False 
                noatk += 1
        turns += 1
            
    if len(player) == 0:
        return ['Unsuccessful',f'{get_playerHP(rplayer)}',turns, f'{get_entities(rplayer)}', b.natk]
    elif len(enemies) == 0:
        return ['Successful',f'{get_playerHP(rplayer)}', turns, f'{get_entities(rplayer)}',b.natk]
                
def get_HP(enemies):
    hps = []
    for e in enemies:
        hps.append(e.hp)
    return np.argmin(np.array(hps))


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
        
    
result = test(100)
rdf =  pd.DataFrame(result)
rdf.columns = ['Text','Enemy HP','Player Max HP','Turns Taken','Party','No Atks']
b.natk = 4
result2 = test(100)
rdf2 = pd.DataFrame(result2)
rdf2.columns = ['Text','Enemy HP','Player Max HP','Turns Taken','Party','No Atks']
up,sp = prob(rdf)
up2,sp2 = prob(rdf2)
sns.set(font_scale=0.75)
fig, ax = plt.subplots()
ax.set_title('Party Against Boss, 2-4 Attacks')
ax.set_xlabel('Percentage of Winning')
ax.set_ylabel('Party')
ax.set_xticks(range(0,101,10))
sns.barplot(y=rdf['Party'].unique(),x=up,palette=['blue'])
sns.barplot(y=rdf2['Party'].unique(),x=up2,palette=['green'])
blue_patch = mpatches.Patch(color='blue', label='2 atks')
green_patch = mpatches.Patch(color='green', label='4 atks')
plt.legend(handles=[blue_patch,green_patch])
plt.show()
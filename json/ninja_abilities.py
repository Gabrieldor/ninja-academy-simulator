import ninja_helper as helper

def split_dmg(dmg):
    result = {}
    f_split = dmg.split('d')
    result['num'] = int(f_split[0])
    s_split = f_split[1].split('+')
    try:
        result['d'] = int(s_split[0])
        result['add'] = int(s_split[1])
    except:
        s_split = f_split[1].split('-')
        result['d'] = int(s_split[0])
        result['add'] = int(s_split[1])
    return result

def get_types(types):
    result = {}
    type = types.split(',')
    for t in type:
        t = t.replace(' ','').lower()
        result[t] = True
    return result

def get_self(status_self, hands, require_row):
    self = {}
    conditions = {}
    remove = {}
    require = {}
    if status_self:
        statuses = status_self.split(',')
        for status in statuses:
            if 'special' in status:
                self[status[8:]] = get_specials(status[8:])
            else:
                if ' ' in status:
                    status_s = status.split(' ')
                    conditions[status_s[0]] = status_s[1]
                else:
                    if status[0] == "-":
                        remove[status[1:]] = True
                    else:
                        conditions[status] = True
    if conditions:
        self['conditions'] = conditions
    if remove:
        self['remove'] = remove
    if hands:
        require['hands'] = hands
    if 'self' in require_row:
        requirements = require_row[5:].split(',')
        for r in requirements:
            if r[0] == '-':
                require['conditions'] = {r[1:]:False}
            else:
                require['conditions'] = {r:True}
    if require:
        self['require'] = require
    return self

def get_specials(special):
    if special == 'move':
        move = {}
        move['goalType'] = 'select'
        move['speed'] = 1
        return move

def get_target(status_target, minRNG, maxRNG ,require_row):
    target = {}
    conditions = {}
    remove = {}
    require = {}
    statuses = status_target.split(',')
    for status in statuses:
        if 'targetType' in status:
            status = status.split(':')[1]
            target['targetType'] = status
        else:
            if ' ' in status:
                status_s = status.split(' ')
                conditions[status_s[0]] = status_s[1]
            else:
                if status[0] == "-":
                    remove[status[1:]] = True
                else:
                    conditions[status] = True
    if minRNG or maxRNG:
        require['range'] = {'max':maxRNG,'min':minRNG}
    if 'target' in require_row:
        requirements = require_row.split(':')[1].split(',')
        for r in requirements:
            if r[0] == '-':
                require['conditions'] = {r[1:]:False}
            else:
                require['conditions'] = {r:True}
    if conditions:
        target['conditions'] = conditions
    if remove:
        target['remove'] = remove
    if require:
        target['require'] = require
    return target


def abilities_to_dict(dfs):
    abilities = {}
    for df in dfs:
        for i in df.index:
            row = df.loc[i]

            icon = helper.path_to_img(row['Action'])
            id = row['Way'].replace('-','_').lower() + "_" + row['Id'].lower()
            ability = {
                'ap':int(row['Ap Cost']),
                'description':row['Description'],
                'icon':icon,
                'id':id,
                'name':row["Action"],
                'self':get_self(row['Status Self'],int(row['Hands']),row['Require']),
                'skill':row["Skill"].lower(),
                'target':get_target(row['Status Target'],int(row['MinRNG']),int(row['MaxRNG']),row['Require']),
                'tier':int(row['Tier']),
                'types':get_types(row['Types']),
                'way':row['Way'].lower()

            }
            if not ability['self']:
                ability = {k: v for k, v in ability.items() if v}
            abilities[id] = ability
    return abilities

helper.dict_to_db('tests/abilities',abilities_to_dict(helper.get_csvs('abilities_db')))










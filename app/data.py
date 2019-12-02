import random
import string

import pandas as pd

piece_types = ["corners", ]
stickers = pd.DataFrame({
    'type': [0 for _ in range(24)],
    'faces': 'UBL URB UFR ULF LUB LFU LDF LBD FUL FRU FDR FLD RUF RBU RDB RFD BUR BLU BDL BRD DFL DRF DBR DLB'.split(),
    'letter': list('ABCDEFGHIJKLMNOPQRSTUVWX')
})


def case_name(row):
    t1 = stickers.iloc[row['target1']]
    t2 = stickers.iloc[row['target2']]
    return f"UFR-{t1['faces']}-{t2['faces']} ({t1['letter']}{t2['letter']})"


cases = pd.read_csv('comms.tsv', sep='\t', header=0)
cases['repr'] = cases.apply(case_name, axis=1)

users = pd.DataFrame(columns=['key'])
times = pd.DataFrame(columns=['user_id', 'time', 'date', 'case_id'])


def new_session():
    sid = "".join(random.choices(string.ascii_lowercase + string.digits, k=50))
    users.append({'key': sid}, ignore_index=True)
    return sid


def next_case():
    return random.choice(cases.index)


def case_for_id(case_id):
    c = dict(cases.iloc[int(case_id)])
    c['id'] = case_id
    c['name'] = case_name(c)
    return c


def history(user_id):
    h = times.copy()[times['user_id'] == user_id].sort_values(by='date', ascending=False)
    names = cases.loc[list(h['case_id']), 'repr']
    h['case_name'] = list(names)
    return h


def submit(form_data):
    form_data['time'] = float(form_data['time'])
    form_data['user_id'] = users.index[users['key'] == form_data['user_id']]
    global times
    times = times.append(form_data, ignore_index=True)
    times['date'] = times['date'].astype(int)
    times['case_id'] = times['case_id'].astype(int)


if __name__ == '__main__':
    print(cases.iloc[190])

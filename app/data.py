import random

import pandas as pd

piece_types = ["corners", ]
stickers = pd.DataFrame([
    {'type': 0, 'faces': s, 'letter': c, }
    for s, c in zip(
        'UBL URB UFR ULF LUB LFU LDF LBD FUL FRU FDR FLD RUF RBU RDB RFD BUR BLU BDL BRD DFL DRF DBR DLB'.split(),
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    )
])

cases = pd.read_csv('comms.tsv', sep='\t', header=0)
times = pd.DataFrame(columns=['time', 'date', 'case_id'])


def next_case(pt=0):
    return random.choice(cases.index)


def case_for_id(case_id):
    c = dict(cases.iloc[int(case_id)])
    c['id'] = case_id
    t1 = stickers.iloc[c['target1']]
    t2 = stickers.iloc[c['target2']]
    c['name'] = f"UFR-{t1['faces']}-{t2['faces']} ({t1['letter']}{t2['letter']})"
    return c


def history():
    return times


def submit(form_data):
    form_data['time'] = float(form_data['time'])
    global times
    times = times.append(form_data, ignore_index=True)
    print(times)


if __name__ == '__main__':
    print(cases.iloc[190])

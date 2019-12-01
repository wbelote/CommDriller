import random

import pandas as pd

piece_types = ["corners", ]
stickers = pd.DataFrame([
    {'type': 0, 'faces': s, 'letter': c, }
    for s, c in zip(
        'UBL URB UFR ULF LUB LFU LDF LBD FUL FRU FDR FLD RUF RBU RDB RFD BUR BLU BDL BRD DFL DRF DBR DLB'.split(),
        'ABCDEFGHIJKLMNOPQRSTOVWXYZ'
    )
])

cases = pd.read_csv('comms.tsv', sep='\t', header=0)
times = pd.DataFrame(columns=['time', 'date', 'case'])


def next_case(pt=0):
    return cases.iloc[random.choice(cases.index)]


def case_for_id(case_id):
    return cases.iloc[case_id]


def history():
    return times


def submit(form_data):
    times.append(form_data)


if __name__ == '__main__':
    print(random.choice(cases.index))

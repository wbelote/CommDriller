import pandas as pd

piece_types = ["corners", ]
stickers = pd.DataFrame([
    {'faces': s, 'letter': c, }
    for s, c in zip(
        'UBL URB UFR ULF LUB LFU LDF LBD FUL FRU FDR FLD RUF RBU RDB RFD BUR BLU BDL BRD DFL DRF DBR DLB'.split(),
        'ABCDEFGHIJKLMNOPQRSTOVWXYZ'
    )
])

if __name__ == '__main__':
    print(stickers)

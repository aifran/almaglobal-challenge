from enum import Enum

rofex_to_yf_tickers = {
    "YPFD": "YPFD.BA",
    "GGAL": "GGAL.BA",
    "PAMP": "PAMP.BA",
    "DLR": "ARS=X"
}


class Month(Enum):
    ENE = 1
    FEB = 2
    MAR = 3
    ABR = 4
    MAY = 5
    JUN = 6
    JUL = 7
    AGO = 8
    SEP = 9
    OCT = 10
    NOV = 11
    DIC = 12


month_to_number = {m.name: m.value for m in Month}

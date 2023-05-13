CodesW = {
    'КСП': '09.02.07',
    'КБУ': '38.02.01',
    'ККД': '38.02.04',
    'КБД': '38.02.07',
    'КПО': '40.02.01',
    'КПД': '40.02.02',
}
Codes = ['09.02.07',
         '38.02.01',
         '38.02.04',
         '38.02.07',
         '40.02.01',
         '40.02.02']
CodesN = {
    '09.02.07': 0,
    '38.02.01': 1,
    '38.02.04': 2,
    '38.02.07': 3,
    '40.02.01': 4,
    '40.02.02': 5
}

number =""


def setCodesTable(table):
    global number
    global Codes
    number = [[], [], [], [], [], []]
    tableC=[]
    for key in table:
        str = key[0] + key[1] + key[2]
        tableC.append(CodesW[str])
    N=len(tableC)
    print(N)
    for i in range(0, N):
        number[CodesN[tableC[i]]].append(i)
    print(number)
from flask import Flask, request, render_template

import timetableCreator

# -*- coding: utf-8 -*-
app = Flask(__name__)
app.config['DEBUG'] = True
import diplom
import GetData

starts=False
@app.route('/')
def index():  # put application's code here
    global starts
    if not starts:
        diplom.main()
        starts=True
    table=diplom.table
    GetData.setCodesTable(table)
    number=GetData.number
    codes=GetData.Codes
    error=timetableCreator.error
    return render_template('index.html',table=table,num=number,code=codes,error=error)

if __name__ == '__main__':
    app.run()

'''
В 1 уровне table идут названия групп
по словарю 1 уровня можно получить расписание по группам на чет и нечет
'''
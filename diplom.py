import sys
import tableConverter
import timetableCreator

table=""

def main():
    # DEBUG
    sys.argv.append('.\start_file.xls')

    selected_lists = tableConverter.getListsFromFile()

    # формируем расписания
    timetables, failed_lessons = timetableCreator.listsToTimetables(selected_lists)
    global table
    table=timetables
    #
    # timetables_json = tableConverter.saveTimetableToJson(timetables, failed_lessons)
    # with open('.\json_data.json', 'w') as outfile:
    #     outfile.write(timetables_json)

    # print(timetables_json)
    # записываем их в файл
    tableConverter.saveTimetableToFile(timetables)

    # DEBUG
    f = open("result.txt", "w")
    f.write(str(timetables))
    f.close()


if __name__ == '__main__':
    main()

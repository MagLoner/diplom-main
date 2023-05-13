error = ""
def listsToTimetables(lists):
    [lessons_list, ordered_lessons_list] = lists
    # парсим лист в список пар
    lessons = list_to_lessons(lessons_list)
    # парсим заказные пары
    ordered_lessons_list = ordered_lessons_list_parse(ordered_lessons_list)
    # формируем расписание
    return lessons_to_timetables(lessons, ordered_lessons_list)

def lessons_to_timetables(lessons, ordered_lessons):
    timetables = {} # массив расписаний, 1 элемент - 1 расписание для группы
    failed_lessons = []

    # формируем список групп в timetables
    for lesson in lessons:
        # добавляем группу в timetables если ее там еще нет
        if (not lesson['group'] in timetables):
            #print("Добавляем группу " + lesson['group'])
            timetables[lesson['group']] = {
                'even': [[], [], [], [], [], [], []], # четная неделя
                'odd': [[], [], [], [], [], [], []] # нечетная неделя
            }

    # в дни добавляем пустые предметы
    for group in timetables:
        timetable = timetables[group]
        for week in timetable:
            week = timetable[week]
            for day in week:
                for i in range(20):
                    day.append('')
    
    # работаем отдельно по каждой группе
    for group in timetables.keys():
        week = 'even' # начинаем с четной недели
        
        # получаем список запланированных занятий у этой группы
        lessons_of_group = get_lessons_of_group(lessons, group)

        # формируем расписание
        fill_timetable(timetables, group, lessons_of_group, ordered_lessons, failed_lessons)
    
    return timetables, failed_lessons

'''
Алгоритм заполнения расписания:
1. Проверить, что пара свободна
2. Внести пару
3. Перейти на следующий день
Повторять пока не кончатся пары
'''
def fill_timetable(timetables, group, week_lessons, ordered_lessons, failed_lessons):
    day = 0 # начинаем с понедельника
    lesson_num = 0 # начинаем с 1 пары
    week = 'even' #  начинаем с четной недели
    global error
    while len(week_lessons) > 0:
        day += 1
        if (day >= 5):
            if (week == 'even'):
                week = 'odd'
                day = 0
            else:
                week = 'even'
                day = 0
                lesson_num += 1
                if (lesson_num == 8):
                    # пару поставить не удалось
                    error = f" {error} {lesson['group']}: {lesson['lesson']}, {lesson['teacher']};            "
                    print(f"Пару поставить не удалось: {lesson['group']},{lesson['lesson']}, {lesson['teacher']}")

                    failed_lesson = {}
                    failed_lesson['group'] = group
                    failed_lesson['lesson'] = lesson['lesson']
                    failed_lesson['teacher'] = lesson['teacher']
                    failed_lesson['hours'] = lesson['hours']
                    failed_lesson['cabinet'] = lesson['cabinet']
                    failed_lessons.append(failed_lesson)

                    # удаляем пару из week_lessons
                    if (lesson['hours'] < 2):
                        week_lessons.remove(lesson)
                    else:
                        lesson['hours'] -= 1
                    # возвращаемся на первую пару первого дня
                    day = 0
                    lesson_num = 0
                    continue

        lesson = week_lessons[0]

        # проверяем, что на эту пару не установлена другая
        if timetables[group][week][day][lesson_num] != '':
            continue

        # проверяем, что препод может вести эту пару в этот день
        if lesson['teacher'] in ordered_lessons:
            if ordered_lessons[lesson['teacher']][day][lesson_num] == False:
                continue

        # проверяем свободен ли урок
        if not is_lesson_free(timetables, lesson, week == 'even', day, lesson_num, lesson['teacher']):
            continue

        # ура, можем ставить сюда пару
        # размещение пары на своем месте
        timetables[group][week][day][lesson_num] = lesson
        # удаляем пару из week_lessons
        if (lesson['hours'] < 2):
            week_lessons.remove(lesson)
        else:
            lesson['hours'] -= 1
        # возвращаемся на первую пару первого дня
        day = 0
        lesson_num = 0

# из списка общего списка занятий возвращает занатия только для определенной группы
def get_lessons_of_group(lessons, target_group):
    result = []
    for lesson in lessons:
        if lesson['group'] == target_group:
            result.append(lesson)
    return result

# функция проверяет, свободен ли определенный предмет на конкретную неделю на конкретной паре
def is_lesson_free(timetables, lesson, is_week_even, day, lesson_num, teacher_name = '') -> bool:
    if is_week_even:
        week = 'even'
    else:
        week = 'odd'
    # проверяем что пара не занята
    for timetable in timetables:
        timetable = timetables[timetable]
        try:
            # если эта пара уже занята
            if timetable[week][day][lesson_num]['lesson'] == lesson['lesson']:
                # проверяем, занята ли она тем же преподом
                if timetable[week][day][lesson_num]['teacher'] == teacher_name:
                    return False
                else:
                    continue
            else:
                continue
        except:
            continue
    # проверяем что кабинет не занят
    if lesson['cabinet'] == '' or lesson['cabinet'] == '100/А':
        return True
    for timetable in timetables:
        timetable = timetables[timetable]
        # проверяем каждую группу на определенный день определенную пару
        try:
            if timetable[week][day][lesson_num]['cabinet'] == lesson['cabinet']:
                return False
            else:
                continue
        except:
            continue
    return True

def list_to_lessons(lessons_list):
    # забираем значения таблицы
    table = lessons_list.values

    # ищем номер первой строки с парой
    first_row_num = None
    for idx, row in enumerate(table):
        temp = str(row[4])
        is_nan = temp == 'nan'
        if is_nan:
            continue
        if temp.isnumeric():
            first_row_num = idx
            break

    # от первой строки парсим все последующие, получая в результате массив с данными по парам
    lessons = []
    for i in range(first_row_num, len(table)):
        if str(table[i][0]) == 'nan':
            table[i][0] = ''
        if str(table[i][6]) == 'nan':
            table[i][6] = ''
        new_lesson = {
            'teacher': str(table[i][0]),
            'lesson': str(table[i][1]),
            'group': str(table[i][2]),
            'hours': int(table[i][4]),
            'cabinet': str(table[i][6]),
        }
        lessons.append(new_lesson)

    return lessons
    
def ordered_lessons_list_parse(ordered_lessons_list):
    # забираем значения таблицы
    table = ordered_lessons_list.values

    # ищем номер первой строки с нормером пары
    first_row_num = None
    for idx, row in enumerate(table):
        temp = str(row[2])
        is_nan = temp == 'nan'
        if is_nan:
            continue
        if temp.isnumeric():
            first_row_num = idx
            break

    # нашли первую строчку с фамилией препода, парсим заказные пары
    teachers = []
    result = {}
    i = first_row_num
    while True:
        try:
            teacher_name = table[i][0]
        except:
            break
        if str(teacher_name) == 'nan':
            break
        teachers.append(teacher_name)
        result[teacher_name] = parse_x_marks(table, i)
        i += 7

    return result

def parse_x_marks(table, pos):
    result = []
    for i in range(6):
        result.append([])
        for j in range(8):
            if table[pos+1+i][2+j] == 'x' or table[pos+1+i][2+j] == 'х':
                result[i].append(False)
            else:       
                result[i].append(True)
    return result

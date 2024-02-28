from random import randint
from RU_LOCAL import ru, ru_fuel_marks
from EN_LOCAL import en


def make_visitors_dict(file):
    """
    Function makes dictionary with visitors form file
    :param file: input file with visitors
    :return: dictionary with arrive time in keys and list of full visitor's info in values:
        arrive time(str),
        volume(int),
        fuel mark(str),
        time of fueling(int)
    :rtype: dict
    """
    with open(file, 'r', encoding='UTF-8') as input_file:
        input_list = input_file.readlines()
    for i in range(len(input_list)):
        input_list[i] = input_list[i].replace('\n', '')
    visitors_dict = {}
    for m in range(len(input_list)):
        input_list[m] = input_list[m].split()
        if int(input_list[m][1]) <= 10:
            time = int((-(-(int(input_list[m][1]) / 10) // 1) + randint(0, 1)))
        else:
            time = int((-(-(int(input_list[m][1]) / 10) // 1) + randint(-1, 1)))
        visitors_dict[input_list[m][0]] = \
            [input_list[m][0], int(input_list[m][1]), input_list[m][2], time]
    return visitors_dict


def make_machine_list(file):
    """
    Function makes list with full information about machines from file
    :param file: input file with station info
    :return: list including lists with machines info:
        number(int),
        max queue(int),
        fuel marks(set),
        visitors in queue(list),
        time before leaving(int)
    :rtype: list
    """
    with open(file, 'r', encoding='UTF-8') as station_file:
        m_list = station_file.readlines()

    for i in range(len(m_list)):
        info = m_list[i].split()
        m_list[i] = [int(info[0]), int(info[1]), set(info[2:]), [], -1]
    return m_list


def get_info(m_list, num, info_type='visitors'):
    """
    Support function, returns required value from list with machines info
    :param m_list: machine list
    :param num: number of machine
    :param info_type: definition of return value:
        1, 'q' or 'queue' returns max queue
        2, 'm' or 'marks' returns fuel marks
        3, 'v' or 'visitors' returns list of current visitors
        4, 't' or 'time' returns time before leaving
    :return: required value from machine list
    """
    if info_type in [1, 'q', 'queue']:
        return m_list[num - 1][1]
    elif info_type in [2, 'm', 'marks']:
        return m_list[num - 1][2]
    elif info_type in [3, 'v', 'visitors']:
        return m_list[num - 1][3]
    elif info_type in [4, 't', 'time']:
        return m_list[num - 1][4]


def add_visitor(visitor, m_list):
    """
    Function adds visitor to current visitors in machine list
     and returns visitor info and number of machine,
     if visitor cannot get in line, returns empty list
    :param visitor: info about visitor
    :param m_list: machine list
    :return: visitor info and number of machine / []
    """
    if not visitor:
        return []

    queues = []
    for i in range(len(m_list)):
        if visitor[2] in get_info(m_list, i+1, 'm') and \
                len(get_info(m_list, i+1)) < get_info(m_list, i+1, 'q'):
            queues.append(len(get_info(m_list, i+1)))

    if not queues:
        return []

    for i in range(len(m_list)):
        if len(get_info(m_list, i+1)) == min(queues):
            m_list[i][3].append(visitor)
            return [visitor, i+1]


def remove_visitor(m_list):
    """
    Function removes leaving visitors from machine list and returns info about removed visitors
    :param m_list: list with machines info
    :return: list with info of removed visitors
    """
    visitors_out = []
    for i in range(len(m_list)):
        if not get_info(m_list, i+1):
            m_list[i][4] = -1
        else:
            if get_info(m_list, i+1, 'time') == -1:
                m_list[i][4] = get_info(m_list, i+1)[0][3] - 1
            if get_info(m_list, i+1, 'time') == 0:
                visitors_out.append(m_list[i][3].pop(0))
                m_list[i][4] = -1
            else:
                m_list[i][4] -= 1
    return visitors_out


def print_info(info, time, m_list):
    """
    Function prints information about updates on gas station
    :param info: dictionary with information about arriving, leaving and lost visitors
    :param time: current time
    :param m_list: machine list
    :return: None
    """
    if info['in'] != []:
        print(ru['In'], time, ru['new client'] + ':', *info['in'][0],
              ru['joined the queue'], '№' + str(info['in'][1]))
        for m in range(len(m_list)):
            print(ru['Machine'], '№', m_list[m][0], ru['max queue'], m_list[m][1],
                  ru['Fuel marks'], *m_list[m][2], ' -> ' + len(m_list[m][3]) * '*')
    if info['out'] != []:
        for i in range(len(info['out'])):
            print(ru['In'], time, ru['client'], *info['out'][i], ru['refueled car'])
            for m in range(len(m_list)):
                print(ru['Machine'], '№', m_list[m][0], ru['max queue'], m_list[m][1],
                      ru['Fuel marks'], *m_list[m][2], ' -> ' + len(m_list[m][3]) * '*')
    if info['lost'] != []:
        print(ru['In'], time, ru['new client'] + ':', *info['lost'], ru['could not refuel'])
        for m in range(len(m_list)):
            print(ru['Machine'], '№', m_list[m][0], ru['max queue'], m_list[m][1],
                  ru['Fuel marks'], *m_list[m][2], ' -> ' + len(m_list[m][3]) * '*')



PRICES = {ru_fuel_marks[80]: 42.51,
          ru_fuel_marks[92]: 48.89,
          ru_fuel_marks[95]: 52.42,
          ru_fuel_marks[98]: 67.28}

machine_list = make_machine_list('station_info.txt')
visitors_dict = make_visitors_dict('input.txt')

visited_cars = [] #list of cars that visited station
lost_cars = [] #list of cars that station lost

revenue = 0
lost_cars_count = 0
lost_revenue = 0
volumes = {ru_fuel_marks[80]: 0, ru_fuel_marks[92]: 0, ru_fuel_marks[95]: 0, ru_fuel_marks[98]: 0}

for hour in range(24):
    for minute in range(60):

        info = {'in': [], 'out': [], 'lost': []}

        current_time = ('0'+str(hour))[-2:] + ':' + ('0'+str(minute))[-2:]
        current_visitor = visitors_dict.get(current_time, [])

        info['out'] = remove_visitor(machine_list)

        info['in'] = add_visitor(current_visitor, machine_list)

        if info['in']:
            visited_cars.append(info['in'][0])
            revenue += PRICES[info['in'][0][2]] * info['in'][0][1]
            volumes[info['in'][0][2]] += info['in'][0][1]
        else:
            info['lost'] = current_visitor
            if info['lost']:
                lost_cars.append(info['lost'])
                lost_cars_count += 1
                lost_revenue += PRICES[info['lost'][2]] * info['lost'][1]

        print_info(info, current_time, machine_list)

for i in range(len(machine_list)):
    visitors = get_info(machine_list, i + 1)
    while visitors:
        visitor = visitors.pop(0)

        lost_cars.append(visitor)
        lost_cars_count += 1
        lost_revenue += PRICES[visitor[2]] * visitor[1]
        visited_cars.remove(visitor)
        revenue -= PRICES[visitor[2]] * visitor[1]
        volumes[visitor[2]] -= visitor[1]

        print( print(ru['In'], '00:00', ru['client'] + ':', *visitor, ru['arrived late']))
        for m in range(len(machine_list)):
            print(ru['Machine'], '№', machine_list[m][0], ru['max queue'], machine_list[m][1],
                  ru['Fuel marks'], *machine_list[m][2], ' -> ' + len(machine_list[m][3]) * '*')

for mark, volume in volumes.items():
    print(mark, ':', volume, ru['liters'])

print(ru['revenue'] + ': ', round(revenue, 2))
print(ru['lost revenue'] + ': ', round(lost_revenue, 2))
print(ru['lost clients'] + ': ', lost_cars_count)

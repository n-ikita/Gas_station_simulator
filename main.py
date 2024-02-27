from random import randint
from RU_LOCAL import ru

def make_visitors_dict(file):
    with open(file, 'r', encoding='UTF-8') as f:
        s = f.readlines()
        for i in range(len(s)):
            s[i] = s[i].replace('\n', '')
        visitors_dict = {}
        for m in range(len(s)):
            s[m] = s[m].split()
            if int(s[m][1]) < 10:
                time = 1
            if int(s[m][1]) == 10:
                time = int((-(-(int(s[m][1]) / 10) // 1) + randint(0, 1)))
            if int(s[m][1]) > 10:
                time = int((-(-(int(s[m][1]) / 10) // 1) + randint(-1, 1)))
            visitors_dict[s[m][0]] = [s[m][0], int(s[m][1]), s[m][2], time]
        return visitors_dict


def make_machine_list(file):
    with open(file, 'r', encoding='UTF-8') as station_file:
        m_list = station_file.readlines()

    for i in range(len(m_list)):
        info = m_list[i].split()
        m_list[i] = [int(info[0]), int(info[1]), set(info[2:]), [], -1]
    return m_list


def get_info(m_list, num, info_type='visitors'):
    if info_type in [1, 'q', 'queue']:
        return m_list[num - 1][1]
    elif info_type in [2, 'm', 'marks']:
        return m_list[num - 1][2]
    elif info_type in [3, 'v', 'visitors']:
        return m_list[num - 1][3]
    elif info_type in [4, 't', 'time']:
        return m_list[num - 1][4]


def add_visitor(visitor, m_list):
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


"""def print_info(info, time, m_list):

    if info['in'] != []:
    
        print('В '+ time + ' новый клиент:' + ' ' + info['in'][0][0] + ' ' + info['in'][0][2] + ' '
              + str(info['in'][0][1]) + ' ' + str(info['in'][0][3]) + ' ' + 'встал в очередь к автомату №'
              + str(info['in'][1]))
        for m in range(len(m_list)):
            print('Автомат №' + str(m_list[m][0]) + ' максимальная очередь: ' + str(m_list[m][1])
                  + ' Марки бензина: ', *m_list[m][2], ' -> ' + len(m_list[m][3]) * '*')
    if info['out'] != []:
        for i in range(len(info['out'])):
            print('В ' + time + ' клиент ' + info['out'][i][0] + ' ' + info['out'][i][2] + ' '
                  + str(info['out'][i][1]) + ' ' + str(info['out'][i][3]) + ' заправил свой автомобиль и покинул АЗС' )
            for m in range(len(m_list)):
                print('Автомат №' + str(m_list[m][0]) + ' максимальная очередь: ' + str(m_list[m][1])
                      + ' Марки бензина: ', *m_list[m][2], ' -> ' + len(m_list[m][3]) * '*')
    if info['lost'] != []:
        print('В ' + time + ' новый клиент: ' + time + ' ' + info['lost'][2] + ' '
              + str(info['lost'][1]) + ' ' + str(info['lost'][3]) + ' не смог заправить свой автомобиль и покинул АЗС')
        for m in range(len(m_list)):
            print('Автомат №' + str(m_list[m][0]) + ' максимальная очередь: ' + str(m_list[m][1])
                  + ' Марки бензина: ', *m_list[m][2], ' -> ' + len(m_list[m][3]) * '*')
"""


def print_info(info, time, m_list):
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


def print_info_late(time, m_list):
    for i in range(len(m_list)):
        visitors = get_info(m_list, i+1)
        while visitors:
            visitor = visitors.pop(0)

            print('В ' + time + ' клиент: ' + visitor[0] + ' ' + visitor[2] + ' '
                  + str(visitor[1]) + ' ' + str(visitor[3]) + ' не успел заправить свой автомобиль и покинул АЗС')
            for m in range(len(m_list)):
                print('Автомат №' + str(m_list[m][0]) + ' максимальная очередь: ' + str(m_list[m][1])
                      + ' Марки бензина: ', *m_list[m][2], ' -> ' + len(m_list[m][3]) * '*')


PRICES = {'АИ-80': 40.4,
          'АИ-92': 42.3,
          'АИ-95': 49.5,
          'АИ-98': 59.5}

machine_list = make_machine_list('station_info.txt')
visitors_dict = make_visitors_dict('input.txt')

visited_cars = [] #list of cars that visited station
lost_cars = [] #list of cars that station lost

revenue = 0
lost_cars_count = 0
lost_revenue = 0
volumes = {'АИ-80': 0, 'АИ-92': 0, 'АИ-95': 0, 'АИ-98': 0}

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

print(ru['Revenue'] + ': ', revenue)
print(ru['lost clients'] + ': ', lost_cars_count)
print(ru['lost revenue'] + ': ', lost_revenue)

import datetime


start = open('start.log')
start_list = start.read().split('</DocId>\n')
start_out = [i.replace('INFO o.a.j.u.BeanShellTestElement: UC01_Request SearchCityRequestRq = <?xml version="1.0" standalone="yes"?><DocId>', '').split(' ') for i in start_list]
start_out = start_out[:-1]

stop = open('stop.log')
stop_list = stop.read().split('</DocId>\n')
stop_out = [i.replace('INFO o.a.j.u.BeanShellTestElement: UC01_Response SearchCityRequestRs = <?xml version="1.0" standalone="yes"?><DocId>', '').split(' ') for i in stop_list]
stop_out = stop_out[:-1]
start.close()
stop.close()


time_start = datetime.datetime.strptime((start_out[0][0] + ' ' + start_out[0][1][:-4]), '%Y-%m-%d %H:%M:%S') #дата и время начала операции
time_stop = datetime.datetime.strptime((stop_out[-1][0] + ' ' + stop_out[-1][1][:-4]), '%Y-%m-%d %H:%M:%S') #дата и время начала


t = time_start
sec = datetime.timedelta(seconds=1)
list_time = [] # список контрольного времени
while (t <= time_stop):
    list_time.append(t)
    t += sec


list_tr = []#список с транзакциями

for i in range(len(start_out)):
    x = start_out[i]
    y = stop_out[i]
    date_time_start_str = x[0] + ' ' + x[1]
    date_time_start_obj = datetime.datetime.strptime(date_time_start_str, '%Y-%m-%d %H:%M:%S.%f')
    date_time_stop_srt = y[0] + ' ' + y[1]
    date_time_stop_obj = datetime.datetime.strptime(date_time_stop_srt, '%Y-%m-%d %H:%M:%S.%f')
    t = date_time_stop_obj - date_time_start_obj
    list_tr.append([date_time_start_obj,
                    date_time_stop_obj,
                    t])

itog = open('itog.log', 'w')

for i in list_time:
    c = 0
    time_tr = datetime.timedelta(milliseconds=0)
    for j in list_tr:
        if j[0] <= i <= j[1]:
            c += 1
            time_tr += j[2]

    if c:
        itog.write(f"{i};{c};{int(time_tr.total_seconds() * 1000/c)}\n")
    else: itog.write(f"{i};{c};{0}\n")


itog.close()






from config.database import mongo

item = mongo['signin'].find()[0]
for img in range(len(item['signin_activity']['draw_every_day'])):
    item['signin_activity']['draw_every_day'][img]['img'] = 'http:' + item['signin_activity']['draw_every_day'][img]['img']
for img in range(len(item['signin_activity']['prize_info'])):
    item['signin_activity']['prize_info'][img] = 'http:' + item['signin_activity']['prize_info'][img]
item['signin_activity']['task_list'][0]['img_button'] = 'http:' + item['signin_activity']['task_list'][0]['img_button']
mongo['signin'].update_one({'isCheckInOfToday': 0}, {'$set': item})
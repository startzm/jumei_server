from config.database import r, mongo


class HomeAct():
    # 向redis导入首页活动信息
    collect = 'act'

    @classmethod
    def _get_data(cls):
        # 随机取5个活动
        activities = {}
        act_set = mongo[cls.collect]
        for act in act_set.aggregate([{'$sample': {'size': 5}}]):
            act = dict(act)
            act['_id'] = str(act['_id'])
            act['img'] = dict(zip(range(len(act['img'])), act['img']))
            activities[str(act['_id'])] = act
        return activities

    @classmethod
    def set_cache(cls):
        cls._del_cache()
        activities = cls._get_data()
        for k, v in activities.items():
            r.hmset('home_act:' + k, v)

    @classmethod
    def _del_cache(cls):
        # 删除现有活动
        if r.keys(pattern='home_act:*'):
            r.delete(*r.keys(pattern='home_act:*'))

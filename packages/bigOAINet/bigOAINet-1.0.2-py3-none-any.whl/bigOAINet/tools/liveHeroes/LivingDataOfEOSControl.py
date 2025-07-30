import mxupy as mu

from mxupy import IM
from liveheroes.m.Models import *
from liveheroes.UserControl import UserControl

class LivingDataOfEOSControl(mu.EntityXControl):

    class Meta:
        model_class = LivingDataOfEOS

    
    def add_or_update_model(this, userId, model):
        # todo: 暂时不添加，太猛了，数据库受不了
        return IM()
        # def _do(im):
        #     # 获取今天的日期
        #     today = date.today()

        #     # 将date对象转换为datetime对象，时间部分设置为午夜（00:00:00）
        #     today_datetime = datetime.combine(today, datetime.min.time())
        #     today_timestamp = int(today_datetime.timestamp())

        #     # 查询今天userId对应的LivingDataOfEOS记录
        #     living_data = LivingDataOfEOS.select().where(
        #         LivingDataOfEOS.userId == userId,
        #         LivingDataOfEOS.livingDate == today_timestamp
        #     ).get_or_none()

        #     if living_data:
        #         # 如果记录存在，则比较字段值并更新
        #         update_fields = {}
        #         for k in LivingDataOfEOS._meta.fields:
        #             if k != 'livingDataOfEOSId' and k != 'livingDate' and k in model:
        #                 # 比较字段值，如果传入的model中的值大于当前记录的值，则更新
        #                 if model[k] > getattr(living_data, k):
        #                     update_fields[k] = model[k]

        #         if update_fields:
        #             # 更新记录
        #             rows = LivingDataOfEOS.update(**update_fields).where(
        #                 LivingDataOfEOS.livingDataOfEOSId == living_data.livingDataOfEOSId
        #             ).execute()
        #             im.data = rows
        #     else:
        #         # 如果记录不存在，则插入新记录
        #         new_living_data = LivingDataOfEOS(
        #             userId=userId,
        #             livingDate=today_timestamp,
        #             cumulativeViewers=model.get('cumulativeViewers', 0),
        #             onlineViewers=model.get('onlineViewers', 0),
        #             newFollowers=model.get('newFollowers', 0),
        #             completedOrders=model.get('completedOrders', 0),
        #             totalSalesAmount=model.get('totalSalesAmount', 0),
        #             conversionRate=model.get('conversionRate', 0)
        #         )
        #         new_living_data.save()
        #         im1 = this.dbe.to_dict(new_living_data)

        #         if not im1.success:
        #             return im1

        #         im.data = im1.data

        # return this.dbe.run(_do)



    


  

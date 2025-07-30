import mxupy as mu

from datetime import datetime, date
from liveheroes.m.Models import *

class LivingDataOfBuyinControl(mu.EntityXControl):

    class Meta:
        model_class = LivingDataOfBuyin

    def add_or_update_model(self, userId, model):
        """ 删除音频文件夹，需校验令牌

        Args:
            userId (int): 用户id
            model (LivingDataOfBuyin): 电商直播数据

        Returns:
            IM: 结果
        """
        def _do():
            
            # 获取今天的日期
            today = date.today()
            today_datetime = datetime.combine(today, datetime.min.time())
            today_timestamp = int(today_datetime.timestamp())
            
            # 查询今天userId对应的LivingDataOfBuyin记录
            im = self.get_one(where=[{'userId':userId}, {'livingDate':today_timestamp}])
            if im.error:
                return im
            living_data = im.data
            
            if living_data:
                # 如果记录存在，则比较字段值并更新
                update_fields = {}
                for k in self.fields:
                    if k in ['livingDataOfBuyinId', 'livingDate']:
                        continue
                    
                    if hasattr(model, k):
                        # 比较字段值，如果传入的model中的值大于当前记录的值，则更新
                        if getattr(model, k) > getattr(living_data, k):
                            update_fields[k] = getattr(model, k)

                if update_fields:
                    im = self.update_by_id(living_data.livingDataOfBuyinId, update_fields)
                    if im.error:
                        return im
            else:
                # 如果记录不存在，则插入新记录
                new_living_data = LivingDataOfBuyin(
                    userId=userId,
                    livingDate=today_timestamp,
                    totalSalesAmount=mu.get_attr(model, 'totalSalesAmount', 0),
                    averageOnlineViewers=mu.get_attr(model, 'averageOnlineViewers', 0),
                    conversionRate=mu.get_attr(model, 'conversionRate', 0),
                    uvValue=mu.get_attr(model, 'uvValue', 0),
                    newFollowers=mu.get_attr(model, 'newFollowers', 0)
                )
                im = self.add(new_living_data)
                if im.error:
                    return im
                
            return im

        return self.run(_do)

   


    


  

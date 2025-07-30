import mxupy as mu
from bigOAINet.db.data.m.Province import Province

class ProvinceControl(mu.EntityXControl):
    class Meta:
        model_class = Province
    
    def get_id(self, name):
        """
        获取编号

        参数:
            name (str): 省份名称

        返回:
            int: 省份编号，如果未找到则返回-1
        """
        def _do(im):
            mc = self.model_class
            im.data = -1
            im.data = mc.get(mc.name.contains(name)).provinceId

        return self.run(_do)

    def add_province(self, id, countryId, name, enname):
        """
        添加（用于初始化数据）

        参数:
            id (int): 区域id
            countryId (int): 国家id
            name (str): 名称
            enName (str): 英文名称

        返回:
            IM: 返回操作结果
        """
        def _do(im):
            
            mc = self.model_class
            
            if mc.select().where(mc.provinceId == id).exists():
                im.success = False
                im.msg = f'已经存在 provinceId 为 {id} 的记录。'
                return
            
            c = {
                'provinceId':id,
                'countryId':countryId,
                'name':name,
                'enname':enname
            }    
            im.data = mc.create(**c)

        return self.run(_do)
    
    
    def init_data(self):
        """
        初始化数据

        参数:

        返回:
            IM: 返回操作结果
        """
        
        cs = [
            (1000, 47, "北京", "Beijing"),
            (1001, 47, "上海", "Shanghai"),
            (1002, 47, "天津", "Tianjin"),
            (1003, 47, "重庆", "Chongqing"),
            (1004, 47, "浙江省", "Zhejiang"),
            (1005, 47, "广东省", "Guangdong"),
            (1006, 47, "江苏省", "Jiangsu"),
            (1007, 47, "河北省", "Hebei"),
            (1008, 47, "山西省", "Shanxi"),
            (1009, 47, "四川省", "Sichuan"),
            (1010, 47, "河南省", "Henan"),
            (1011, 47, "辽宁省", "Liaoning"),
            (1012, 47, "吉林省", "Jilin"),
            (1013, 47, "黑龙江省", "Heilongjiang"),
            (1014, 47, "山东省", "Shandong"),
            (1015, 47, "安徽省", "Anhui"),
            (1016, 47, "福建省", "Fujian"),
            (1017, 47, "湖北省", "Hubei"),
            (1018, 47, "湖南省", "Hunan"),
            (1019, 47, "海南省", "Hainan"),
            (1020, 47, "江西省", "Jiangxi"),
            (1021, 47, "贵州省", "Guizhou"),
            (1022, 47, "云南省", "Yunnan"),
            (1023, 47, "陕西省", "Shanxi"),
            (1024, 47, "甘肃省", "Gansu"),
            (1025, 47, "广西区", "Guangxi"),
            (1026, 47, "宁夏区", "Ningxia"),
            (1027, 47, "青海省", "Qinghai"),
            (1028, 47, "新疆区", "Xinjiang"),
            (1029, 47, "西藏区", "Tibet"),
            (1030, 47, "内蒙古区", "Inner Mongolia"),
            (1031, 47, "香港", "Hongkong"),
            (1032, 47, "澳门", "Macao"),
            (1033, 47, "台湾", "Taiwan"),
            (1090, 47, "北京", "Beijing"),
            (4273, 47, "国外", "Abroad "),
        ]
        for c in cs:
            im = self.add_province(int(c[0]), int(c[1]), str(c[2]), str(c[3]))
            if im.error:
                return im
        return im
            

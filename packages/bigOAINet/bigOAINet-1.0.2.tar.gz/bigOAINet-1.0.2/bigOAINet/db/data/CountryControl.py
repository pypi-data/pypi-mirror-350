import mxupy as mu
from mxupy import IM
from bigOAINet.db.data.m.Country import Country

class CountryControl(mu.EntityXControl):
    class Meta:
        model_class = Country
        
    def get_id(self, name):
        """
        获取编号

        参数:
            name (str): 国家名称

        返回:
            int: 国家编号，如果未找到则返回-1
        """
        def _do(im):
            mc = self.model_class
            im.data = -1
            # 性能更好
            im.data = mc.get(mc.name.contains(name)).countryId
            
            # query = mc.select().where(mc.name.contains(name))
            # for country in query:
            #     im.data = country.countryId
            #     return
            # query = mc.select().where(mc.name.contains(name))

        return self.run(_do)

    def add_country(self, id, iso, name, enname):
        """
        添加（用于初始化数据）

        参数:
            id (int): 区域id
            iso (str): 国际标准化组织代码
            name (str): 名称
            enName (str): 英文名称

        返回:
            IM: 返回操作结果
        """
        def _do(im):
            
            mc = self.model_class
            
            if mc.select().where(mc.countryId == id).exists():
                im.success = False
                im.msg = f'已经存在 countryId 为 {id} 的记录。'
                return
            
            c = {
                'countryId':id,
                'iso':iso,
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
            (1, "AD", "安道尔", "Andorra"),
            (2, "AE", "阿联酋", "United Arab Em."),
            (3, "AF", "阿富汗", "Afghanistan"),
            (4, "AG", "安提瓜和巴布达", "Antigua and Barbuda"),
            (5, "AI", "安圭拉", "Anguilla"),
            (6, "AL", "阿尔巴尼亚", "Albania"),
            (7, "AM", "亚美尼亚", "Armenia"),
            (8, "AN", "荷属安的列斯群岛", "NETHERLANDS ANTILLES"),
            (9, "AO", "安哥拉", "Angola"),
            (10, "AR", "阿根廷", "Argentina"),
            (11, "AS", "美属萨摩亚", "American Samoa"),
            (12, "AT", "奥地利", "Austria"),
            (13, "AU", "澳大利亚", "Australia"),
            (14, "AW", "阿鲁巴群岛", "Aruba"),
            (15, "AZ", "阿塞拜疆", "Azerbaijan"),
            (16, "BA", "波斯尼亚", "Bosnia"),
            (17, "BB", "巴巴多斯", "Barbados"),
            (18, "BD", "孟加拉", "Bangladesh"),
            (19, "BE", "比利时", "Belgium"),
            (20, "BF", "布基纳法索", "Burkina Faso"),
            (21, "BG", "保加利亚", "Bulgaria"),
            (22, "BH", "巴林", "Bahrain"),
            (23, "BI", "布隆迪", "Burundi"),
            (24, "BJ", "贝宁", "Benin"),
            (25, "BL", "圣巴瑟米（法）", "Saint Barthelemy"),
            (26, "BM", "百慕大", "Bermuda"),
            (27, "BN", "文莱", "Brunei"),
            (28, "BO", "玻利维亚", "Bolivia"),
            (29, "BQ", "荷兰加勒比区", "Bonaire Sint Eustatius Saba"),
            (30, "BR", "巴西", "Brazil"),
            (31, "BS", "巴哈马", "Bahamas"),
            (32, "BT", "不丹", "Bhutan"),
            (33, "BV", "布韦岛（挪）", "Bouvet Island"),
            (34, "BW", "博茨瓦纳", "Botswana"),
            (35, "BY", "白俄罗斯", "Belarus"),
            (36, "BZ", "伯利兹", "Belize"),
            (37, "CA", "加拿大", "Canada"),
            (38, "CC", "科科斯群岛", "Cocos (Keeling) Islands"),
            (39, "CD", "刚果民主共和国", "The Democratic Republic of the Congo"),
            (40, "CF", "中非共和国", "Central African Republic"),
            (41, "CG", "刚果", "Congo"),
            (42, "CH", "瑞士", "Switzerland"),
            (43, "CI", "科特迪瓦", "Côte d'Ivoire"),
            (44, "CK", "库克群岛", "Cook Islands"),
            (45, "CL", "智利", "Chile"),
            (46, "CM", "喀麦隆", "Cameroon"),
            (47, "CN", "中国", "China"),
            (48, "CO", "哥伦比亚", "Colombia"),
            (49, "CR", "哥斯达黎加", "Costa Rica"),
            (50, "CU", "古巴", "Cuba"),
            (51, "CV", "佛得角", "Cape Verde"),
            (52, "CW", "库拉索", "Curacao"),
            (53, "CX", "圣诞岛", "Christmas Island"),
            (54, "CY", "塞浦路斯", "Cyprus"),
            (55, "CZ", "捷克", "Czech"),
            (56, "DE", "德国", "Germany"),
            (57, "DJ", "吉布提", "Djibouti"),
            (58, "DK", "丹麦", "Denmark"),
            (59, "DM", "多米尼克", "Dominica"),
            (60, "DO", "多米尼加", "Dominican Rep"),
            (61, "DZ", "阿尔及利亚", "Algeria"),
            (62, "EC", "厄瓜多尔", "Ecuador"),
            (63, "EE", "爱沙尼亚", "Estonia"),
            (64, "EG", "埃及", "Egypt"),
            (65, "EH", "西撒哈拉", "Western Sahara"),
            (66, "ER", "厄立特里亚", "Eritrea"),
            (67, "ES", "西班牙", "Spain"),
            (68, "ET", "埃塞俄比亚", "Ethiopia"),
            (69, "EU", "欧盟", "EU"),
            (70, "FI", "芬兰", "Finland"),
            (71, "FJ", "斐济", "Fiji"),
            (72, "FK", "福克兰群岛（马尔维纳斯群岛）", "Falkland Islands (Malvinas)"),
            (73, "FM", "密克罗尼西亚联邦", "Micronesia, Federated States of"),
            (74, "FO", "法罗群岛", "Faroe Islands"),
            (75, "FR", "法国", "France"),
            (76, "GA", "加蓬", "Gabon"),
            (77, "GB", "英国", "Great Britain"),
            (78, "GD", "格林纳达", "Grenada"),
            (79, "GE", "格鲁吉亚", "Georgia"),
            (80, "GF", "法属圭亚那", "French Guiana"),
            (81, "GG", "格恩西岛", "Guernsey"),
            (82, "GH", "加纳", "Ghana"),
            (83, "GI", "直布罗陀", "Gibraltar"),
            (84, "GL", "格陵兰", "Greenland"),
            (85, "GM", "冈比亚", "Gambia"),
            (86, "GN", "几内亚", "Guinea"),
            (87, "GP", "瓜德罗普", "Guadeloupe"),
            (88, "GQ", "赤道几内亚", "Equatorial Guinea"),
            (89, "GR", "希腊", "Greece"),
            (90, "GS", "南乔治亚岛", "South Georgia and the Islands"),
            (91, "GT", "危地马拉", "Guatemala"),
            (92, "GU", "关岛", "Guam"),
            (93, "GW", "几内亚比绍", "Guinea-Bissau"),
            (94, "GY", "圭亚那", "Guyana"),
            (95, "HK", "中国香港", "Hong Kong"),
            (96, "HM", "赫德岛和麦克唐纳群岛", "Heard Island and McDonald Islands"),
            (97, "HN", "洪都拉斯", "Honduras"),
            (98, "HR", "克罗地亚", "Croatia"),
            (99, "HT", "海地", "Haiti"),
            (100, "HU", "匈牙利", "Hungary"),
            (101, "ID", "印度尼西亚", "Indonesia"),
            (102, "IE", "爱尔兰", "Ireland"),
            (103, "IL", "以色列", "Israel"),
            (104, "IN", "印度", "India"),
            (105, "IO", "英属印度洋领地", "British Indian Ocean Territory"),
            (106, "IQ", "伊拉克", "Iraq"),
            (107, "IR", "伊朗", "Iran"),
            (108, "IS", "冰岛", "Iceland"),
            (109, "IT", "意大利", "Italy"),
            (110, "JM", "牙买加", "Jamaica"),
            (111, "JO", "约旦", "Jordan"),
            (112, "JP", "日本", "Japan"),
            (113, "KE", "肯尼亚", "Kenya"),
            (114, "KG", "吉尔吉斯斯坦", "Kyrgyzstan"),
            (115, "KH", "柬埔寨", "Cambodia"),
            (116, "KI", "基里巴斯", "Kiribati"),
            (117, "KM", "科摩罗", "Comoros"),
            (118, "KN", "圣基茨和尼维斯", "Saint Kitts and Nevis"),
            (119, "KP", "朝鲜", "Democratic People's Republic of Korea"),
            (120, "KR", "韩国", "South Korea"),
            (121, "KV", "科索沃", "Kosovo"),
            (122, "KW", "科威特", "Kuwait"),
            (123, "KY", "开曼群岛", "Cayman Islands"),
            (124, "KZ", "哈萨克斯坦", "Kazakhstan"),
            (125, "LA", "老挝", "Laos"),
            (126, "LB", "黎巴嫩", "Lebanon"),
            (127, "LC", "圣卢西亚", "Saint Lucia"),
            (128, "LI", "列支敦士登", "Liechtenstein"),
            (129, "LK", "斯里兰卡", "Sri Lanka"),
            (130, "LR", "利比里亚", "Liberia"),
            (131, "LS", "莱索托", "Lesotho"),
            (132, "LT", "立陶宛", "Lithuania"),
            (133, "LU", "卢森堡", "Luxembourg"),
            (134, "LV", "拉脱维亚", "Latvia"),
            (135, "LY", "利比亚", "Libya"),
            (136, "MA", "摩洛哥", "Moroco"),
            (137, "MC", "摩纳哥", "Monaco"),
            (138, "MD", "摩尔多瓦", "Republic of Moldova"),
            (139, "ME", "黑山", "Montenegro"),
            (140, "MG", "马达加斯加", "Madagascar"),
            (141, "MH", "马绍尔群岛", "Marshall Islands"),
            (142, "MK", "马其顿", "Republic of Macedonia"),
            (143, "ML", "马里", "Mali"),
            (144, "MM", "缅甸", "Myanmar"),
            (145, "MN", "蒙古", "Mongolia"),
            (146, "MO", "中国澳门", "Macau"),
            (147, "MP", "北马里亚纳群岛", "Northern Mariana Islands"),
            (148, "MQ", "马提尼克", "Martinique"),
            (149, "MR", "毛里塔尼亚", "Mauritania"),
            (150, "MS", "蒙特塞拉特", "Montserrat"),
            (151, "MT", "马耳他", "Malta"),
            (152, "MU", "毛里求斯", "Mauritius"),
            (153, "MV", "马尔代夫", "Maldives"),
            (154, "MW", "马拉维", "Malawi"),
            (155, "MX", "墨西哥", "Mexico"),
            (156, "MY", "马来西亚", "Malaysia"),
            (157, "MZ", "莫桑比克", "Mozambique"),
            (158, "NA", "纳米比亚", "Namibia"),
            (159, "NC", "新喀里多尼亚", "New Caledonia"),
            (160, "NE", "尼日尔", "Niger"),
            (161, "NF", "诺福克岛", "Norfolk Island"),
            (162, "NG", "尼日利亚", "Nigeria"),
            (163, "NI", "尼加拉瓜", "Nicaragua"),
            (164, "NL", "荷兰", "Netherlands"),
            (165, "NO", "挪威", "Norway"),
            (166, "NP", "尼泊尔", "Nepal"),
            (167, "NR", "瑙鲁", "Nauru"),
            (168, "NU", "纽埃", "Niue"),
            (169, "NZ", "新西兰", "New Zealand"),
            (170, "OM", "阿曼", "Oman"),
            (171, "PA", "巴拿马", "Panama"),
            (172, "PE", "秘鲁", "Peru"),
            (173, "PF", "法属波利尼西亚", "French Polynesia"),
            (174, "PG", "巴布亚新几内亚", "Papua New Guinea"),
            (175, "PH", "菲律宾", "Philippines"),
            (176, "PK", "巴基斯坦", "Pakistan"),
            (177, "PL", "波兰", "Poland"),
            (178, "PM", "圣皮埃尔和密克隆", "Saint Pierre and Miquelon"),
            (179, "PN", "皮特凯恩", "Pitcairn"),
            (180, "PR", "波多黎各", "Puerto Rico"),
            (181, "PS", "加沙地带", "Gaza Strip"),
            (182, "PT", "葡萄牙", "Portugal"),
            (183, "PW", "帕劳", "Palau"),
            (184, "PY", "巴拉圭", "Paraguay"),
            (185, "QA", "卡塔尔", "Qatar"),
            (186, "RE", "留尼旺群岛", "Reunion"),
            (187, "RO", "罗马尼亚", "Romania"),
            (188, "RS", "塞尔维亚", "Serbia"),
            (189, "RU", "俄罗斯", "Russia"),
            (190, "RW", "卢旺达", "Rwanda"),
            (191, "SA", "沙特阿拉伯", "Saudi Arabia"),
            (192, "SB", "所罗门群岛", "Solomon Islands"),
            (193, "SC", "塞舌尔", "Seychelles"),
            (194, "SD", "苏丹", "Sudan"),
            (195, "SE", "瑞典", "Sweden"),
            (196, "SG", "新加坡", "Singapore"),
            (197, "SH", "圣赫勒拿，阿森松岛和特里斯坦达库尼亚", "Saint Helena, Ascension and Tristan Da Cunha"),
            (198, "SI", "斯洛文尼亚", "Slovenia"),
            (199, "SJ", "斯瓦尔巴特群岛", "Svalbard"),
            (200, "SK", "斯洛伐克", "Slovakia"),
            (201, "SL", "塞拉利昂", "Sierra Leone"),
            (202, "SM", "圣马力诺", "San Marino"),
            (203, "SN", "塞内加尔", "Senegal"),
            (204, "SO", "索马里", "Somalia"),
            (205, "SR", "苏里南", "Suriname"),
            (206, "SS", "南苏丹", "South Sudan"),
            (207, "ST", "圣多美和普林西比", "Sao Tome and Principe"),
            (208, "SV", "萨尔瓦多", "El Salvador"),
            (209, "SX", "荷属圣马丁", "Sint Maarten"),
            (210, "SY", "叙利亚", "Syrian Arab Republic"),
            (211, "SZ", "斯威士兰", "Swaziland"),
            (212, "TC", "特克斯和凯科斯群岛", "Turks and Caicos Islands"),
            (213, "TD", "乍得", "Chad"),
            (214, "TG", "多哥", "Togo"),
            (215, "TH", "泰国", "Thailand"),
            (216, "TJ", "塔吉克斯坦", "Tajikistan"),
            (217, "TK", "托克劳群岛", "Tokelau"),
            (218, "TL", "东帝汶", "East Timor"),
            (219, "TM", "土库曼斯坦", "Turkmenistan"),
            (220, "TN", "突尼斯", "Tunisia"),
            (221, "TO", "汤加", "Tonga"),
            (222, "TR", "土耳其", "Turkey"),
            (223, "TT", "特里尼达和多巴哥", "Trinidad and Tobago"),
            (224, "TV", "图瓦卢", "Tuvalu"),
            (225, "TW", "中国台湾", "Taiwan"),
            (226, "TZ", "坦桑尼亚", "Tanzania, United Republic of"),
            (227, "UA", "乌克兰", "Ukraine"),
            (228, "UG", "乌干达", "Uganda"),
            (229, "UM", "美国本土外小岛屿", "United States Minor Outlying Islands"),
            (230, "US", "美国", "USA"),
            (231, "UY", "乌拉圭", "Uruguay"),
            (232, "UZ", "乌兹别克斯坦", "Uzbekistan"),
            (233, "VA", "梵蒂冈", "Vatican City State"),
            (234, "VC", "圣文森特和格林纳丁斯", "Saint Vincent and the Grenadines"),
            (235, "VE", "委内瑞拉", "Venezuela"),
            (236, "VG", "英属维尔京群岛", "British Virgin lslands"),
            (237, "VI", "维京群岛", "Virgin Islands"),
            (238, "VN", "越南", "Vietnam"),
            (239, "VU", "瓦努阿图", "Vanuatu"),
            (240, "WF", "瓦利斯群岛和富图纳群岛", "Wallis and Futuna"),
            (241, "WS", "萨摩亚", "Samoa"),
            (242, "YE", "也门", "Yemen"),
            (243, "YT", "马约特岛", "Mayotte"),
            (244, "ZA", "南非", "South Africa"),
            (245, "ZM", "赞比亚", "Zambia"),
            (246, "ZW", "津巴布韦", "Zimbabwe")
        ]
        for c in cs:
            im = self.add_country(int(c[0]), str(c[1]), str(c[2]), str(c[3]))
            if im.error:
                return im
        return im

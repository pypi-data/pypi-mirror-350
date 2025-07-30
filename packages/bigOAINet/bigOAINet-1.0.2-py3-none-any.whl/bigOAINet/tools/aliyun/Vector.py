import os
from mxupy import ApiControl

# from dashscope import TextEmbedding
# from dashvector import Client

# pip install dashscope -i https://pypi.tuna.tsinghua.edu.cn/simple
# pip install dashvector -i https://pypi.tuna.tsinghua.edu.cn/simple

class Vector(ApiControl):
    """ 
        向量检索服务（DashVector）
        空间: bigOAINET.llm.aliyun.vector
        一个 Cluster(相当于数据库的库) 对应一个 APP
        一门 Collection(相当于数据库的表) 对应一个 课程 名称为 项目名_应用名_课程名, 缩写为 Coll
        Partition: 一个Collection可以分成多个Partition, 此collection下的每个Partition的结构都一模一样
        官方网址: 
        https://dashvector.console.aliyun.com/cn-hangzhou/playground
        
        返回的对象一般包含的属性
        code: 错误编码, 如果为0, 一般代表操作成功
        message: 错误消息, 如果成功一般为0
        requests_id: 会话id, 随机的32位uuid: 5382cfc3-05f0-4ceb-a648-a1150d485149
        output: 输出的结果
    """
    def __init__(self, cname):
        """ 初始化

        Args:
            cname (str): collection 名称。
        Returns:
            无
        """
        # self.api_key = os.getenv('ALIYUN_API_KEY')
        # self.vector_key = os.getenv('ALIYUN_VECTOR_API_KEY')
        # self.vector_url = os.getenv('ALIYUN_VECTOR_API_URL')
        self.api_key = 'sk-879c45ea8b464c94a5fc4316652315e8'
        self.vector_key = 'sk-Jav2x0kmIGqR7t0IJ4N4FKG9dredwAB26DF0D6B3311EF96F52E56D8B8FC8A'
        self.vector_url = 'vrs-cn-bcd3wiabw0003d.dashvector.cn-hangzhou.aliyuncs.com'
        
        
        self.client = self.getClient()
        self.coll = self.getColl(cname)
        self.collName = cname
    
    def vectorization(self, text, model='text-embedding-v1'):
        """ 向量化字符串
            模型中文名      模型英文名          向量维度        单次请求文本最大行数    单行最大输入字符长度    支持语种
            通用文本向量    text-embedding-v1   1536            25                      2048                中文、英语、西班牙语、法语、葡萄牙语、印尼语。
        Args:
            text (str): 指令, Range of input length should be [1, 2048] 文本长度最大为 2048
            model (str): v1:中文、英文等, v2:增加日、德、俄, v3:增加越、泰、意
        Returns:
            embedList(list[float]): 向量结果, 如: [1.2,1.3,1.4,1.9]
        """
        from dashscope import TextEmbedding
        
        if text == None or text == '': 
            return None
        
        if len(text) > 2048:
            text = text[0:2048]
        
        rsp = TextEmbedding.call(model=model, input=text, api_key=self.api_key)
        if rsp.code != '':
            return rsp
        embeddings = [record['embedding'] for record in rsp.output['embeddings']]
        return embeddings if isinstance(text, list) else embeddings[0]
    
    def sparseVectorization(self, text):
        # from dashscope import TextEmbedding
        
        # vectorizer = CountVectorizer()
        # sparse_vector = vectorizer.fit_transform(text)
        # print(sparse_vector)
        return text
    
    
    
    def newDoc(self, vector_text, id=None, fields=None, sparse_vector=None, score=0.0):
        """ 新建向量文档
        Args:
            vector_text (str): 文本
            id (str): 主键
            fields (doct): 键值对
            sparse_vector:TODO?稀疏向量
            score:分数
        Returns:
        
        """
        from dashvector import Doc
        
        if id != None:
            id = str(id)
            
        return Doc(id=id, vector=self.vectorization(vector_text), fields=fields, sparse_vector=sparse_vector, score=score)
    
    def newDocWithFile(self, path, id=None, fields=None, sparse_vector=None, score=0.0):
        """ 新建向量文档
        Args:
            path (str): 文件路径, 支持 txt md pdf word ipynb ppt xls 等文件
            id (str): 主键
            fields (doct): 键值对
            sparse_vector:TODO?稀疏向量
            score:分数
        Returns:
        
        """
        import File as fi
        
        text = ''
        ext = fi.getExtension(path)
        if ext == 'txt' or ext == 'md':
            text = fi.readAllText(path)
        elif ext == 'doc' or ext == 'docx':
            text = fi.readWordText(path)
        elif ext == 'ppt' or ext == 'pptx':
            text = fi.readPptText(path)
        elif ext == 'xls' or ext == 'xlsx':
            text = fi.readExcelText(path)
        elif ext == 'pdf':
            text = fi.readPdfText(path)
        
        return self.newDoc(text, id, fields, sparse_vector, score)
    
    
    
    def getClient(self):
        """ 获取 Client 实例
        Args:
        Returns:
            Client (obj): Client 实例
        """
        from dashvector import Client
        c = Client(
            api_key = self.vector_key,
            endpoint = self.vector_url
        )
        return c
    
    
    
    # Collection
    def createColl(self, metric='cosine', dtype=float, dimension=1536, fields_schema=None, timeout=-1):
        """ 创建 Coll 实例
        Args:
            metric (str): cosine:适用于语义搜索场景, dotproduct:适用于搜索推荐场景, euclidean:适用于图像和多模态搜索场景
            dtype (float): 向量化类型, 当metric值为cosine时, dtype必须为float
            dimension (int): 向量纬度, text-embedding-v1模型对应的纬度为1536
            fields_schema (obj): 表结构, 如{'name': str, 'weight': float, 'age': int}, 字段名与类型的一一对应关系
            timeout (int):-1, 表示不作限制
        Returns:
            code (int): 错误码
            message (str): 消息
            request_id (str): 会话唯一id
        """
        if metric == 'cosine':
            dtype = float
            
        ret = self.client.create(
            name = self.collName,
            metric = metric,
            dtype = dtype,
            dimension = dimension,
            fields_schema = fields_schema,
            timeout = timeout
        )
        
        # 需要判断成功否再赋值
        if ret.code == 0:
            self.collName = cname
            self.coll = self.getColl(cname)
        
        return ret
    
    def deleteColl(self):
        """ 删除 Coll 实例
        Args:
        
        Returns:
        
        """
        ret = self.client.delete(self.collName)
        return ret
    
    def descColl(self):
        """ 描述 Coll 实例
        Args:
        
        Returns:
        
        """
        ret = self.client.describe(self.collName)
        return ret
    
    def statsColl(self):
        """ 统计 Coll 实例
        Args:
        
        Returns:
        
        """
        if self.coll == None:
            return None
        
        ret = self.coll.stats()
        return ret
    
    def getColl(self, cname):
        """ 获取 collection 实例
        Args:
            cname (str): Collection名称
        Returns:
            collection (obj): collection 实例
        """
        if cname == '' or cname == None:
            return None, '集合名称不能为空'
        
        coll = self.client.get(cname)
        return coll
    
    def getColls(self):
        """ 获取所有 Collection 集
        Args:
        Returns:
        
        """
        colls = self.client.list()
        return colls
    
    
    
    # Partition
    def createPart(self, pname, timeout=10):
        """ 创建 Partition 实例
        Args:
            pname (str): Partition 名称
            timeout (int):-1, 超时时长, 单位秒
        Returns:
        
        """
        if self.coll == None:
            return None
        
        ret = self.coll.create_partition(
            name = pname,
            timeout = timeout
        )
        return ret
    
    def deletePart(self, pname):
        """ 删除 Part 实例
        Args:
            pname (str): Partection名称
        Returns:
            删除 名为default的partition时, 返回
            {"code": -2992, "message": "Not allowed to delete default partition", "requests_id": "8438df0f-2d5f-469a-ac81-c3d34c849272"}
        """
        if self.coll == None:
            return None
        ret = self.coll.delete_partition(pname)
        return ret
    
    def descPart(self, pname):
        """ 创建 Coll 实例
        Args:
            pname (str): Partition 名称
        Returns:
            Client (obj): Client 实例
        """
        if self.coll == None:
            return None
        ret = self.coll.describe_partition(pname)
        return ret
    
    def statsPart(self, pname):
        """ 统计 Part 实例
        Args:
            pname (str): Partition 名称
        Returns:
        
        """
        if self.coll == None:
            return None
        ret = self.coll.stats_partition(pname)
        return ret
    
    def getParts(self):
        """ 获取 Partition 列表
            此列表只是 Partition 名称集
            没有获取单个 Partition 是因为获取到了也没有作用
        Args:
            cname (str): Collection 名称
        Returns:
            Parts (list[obj]): Partition 列表
        """
        if self.coll == None:
            return None
        
        ps = self.coll.list_partitions()
        return ps
    
    
    
    # 操作
    def insert(self, vector_text, pname=None, id=None, fields=None, sparse_vector=None):
        """ 插入记录
            对于刚创建的 collection, 如果立马插入数据, 则报
            {"code": -2030, "message": "Status of collection is incorrect", "requests_id": "9da609e0-9342-4c5b-b73f-cc631f428413"}
            需要等几秒后才能正常插入数据
        Args:
            vector_text (str): 文本
            pname (str): Partition名称, 如果未指定, 则插入到名为default的Partition中, 其他函数也是这种情况
                default的Partition名称不能修改, 也不能删除, 删除时, 返回
                {"code": -2992, "message": "Not allowed to delete default partition", "requests_id": "8438df0f-2d5f-469a-ac81-c3d34c849272"}
            id (str): 主键, 如果不传, 则生成16位数字的随机主键
            fields (doct): 键值对, 可以与 createColl 的字段不同，但是多出的字段不能作为 query 的过滤条件
            sparse_vector:TODO?稀疏向量
        Returns:
        
        """
        from dashvector import Doc
        
        if self.coll == None:
            return None, 'Collection 不存在。'
        
        if id != None:
            id = str(id)
        
        r = self.coll.insert(
            Doc(id=id, vector=self.vectorization(vector_text), fields=fields, sparse_vector=sparse_vector), partition=pname
        )
        return r.get()
    
    def insertList(self, docs, pname=None, async_req=False):
        """ 批量插入, 支持异步
        Args:
            docs (list): 文本
            pname (str): Partition名称
            async_req (bool): 异步否
        Returns:
        
        """
        if self.coll == None:
            return None
        
        r = self.coll.insert(
            docs, partition=pname, async_req=async_req
        )
        # 其他函数get的作用都如此, 不再累述。
        # 此处get函数的作用, 
        # 等待异步插入操作完成。
        # 获取操作的结果, 这个结果可能是成功的确认, 也可能是一个错误码或错误消息。
        # 如果异步操作中有任何异常, get() 方法会将这些异常传递给调用者。
        # r: 直接返回的结果
        # {"code": -999, "message": "", "requests_id": ""}
        # r.get(): get后返回的结果
        # {"code": 0, "message": "Success", "requests_id": "4535e838-7233-9c3c-ad6c-0774fd5a1f1e", 
        # "output": [
            # {"doc_op": "update", "id": "0", "code": 0, "message": ""}, 
            # {"doc_op": "update", "id": "1", "code": 0, "message": ""}, 
            # ...
        # ], "usage": {"write_units": 20}}
        return r.get()
    
    def upsert(self, vector_text, id, pname=None, fields=None):
        """ 更新或插入
        Args:
            vector_text (str): 文本
            id (str): 主键
            pname (str): Partition名称
            fields (doct): 键值对
            sparse_vector:TODO?稀疏向量
            异步:TODO?
        Returns:
        
        """
        from dashvector import Doc
        
        if self.coll == None:
            return None
        
        if id != None:
            id = str(id)
        
        r = self.coll.upsert(
            Doc(id=id, vector=self.vectorization(vector_text), fields=fields), partition=pname
        )
        return r.get()
    
    def upsertList(self, docs, pname=None, async_req=False):
        """ 批量更新, 支持异步
        Args:
            docs (list): 文本
            pname (str): Partition名称
            async_req (bool): 异步否
        Returns:
            {"code": -999, "message": "", "requests_id": ""}
            code = -999 时, 官方说明说是‘未知异常’, 但是值却插入到Collection中
        """
        if self.coll == None:
            return None
        
        r = self.coll.upsert(
            docs, partition=pname, async_req=async_req
        )
        return r.get()
    
    def update(self, vector_text, id, pname=None, fields=None):
        """ 更新
        Args:
            vector_text (str): 文本
            id (str): 主键
            pname (str): Partition名称
            fields (doct): 键值对
            sparse_vector:TODO?稀疏向量
            异步:TODO?
        Returns:
        
        """
        from dashvector import Doc
        
        if self.coll == None:
            return None
        
        if id != None:
            id = str(id)
        
        r = self.coll.update(
            Doc(id=id, vector=self.vectorization(vector_text), fields=fields), partition=pname
        )
        return r.get()
    
    def updateList(self, docs, pname=None, async_req=False):
        """ 批量更新, 支持异步
        Args:
            docs (list): 文本
            pname (str): Partition名称
            async_req (bool): 异步否
        Returns:
        
        """
        if self.coll == None:
            return None
        
        r = self.coll.update(
            docs, partition=pname, async_req=async_req
        )
        return r.get()
   
    def delete(self, id, pname=None):
        """ 获取
        Args:
            id (str): 主键
            pname (str): Partition名称
        Returns:
        """
        if self.coll == None:
            return None
        
        if id != None:
            id = str(id)
        
        r = self.coll.delete(id, partition=pname)
        return r.get()
    
    def deleteList(self, ids, pname=None, async_req=False):
        """ 获取
        Args:
            ids (list[str]): 主键集
            pname (str): Partition名称
            async_req (bool): 异步否
        Returns:
        
        """
        if self.coll == None:
            return None
        
        r = self.coll.delete(ids, partition=pname, async_req=async_req)
        return r.get()
    
    def deleteAll(self, pname=None, async_req=False):
        """ 获取
        Args:
            pname (str): Partition名称
            async_req (bool): 异步否
        Returns:
        
        """
        if self.coll == None:
            return None
        
        r = self.coll.delete(delete_all=True, partition=pname, async_req=async_req)
        return r.get()
    
    
    
    # 查询
    def fetch(self, id, pname=None):
        """ 获取
        Args:
            id (str): 主键
            pname (str): Partition名称
        Returns:
        
        """
        if self.coll == None:
            return None
        
        if id != None:
            id = str(id)
        
        doc = self.coll.fetch(id, partition=pname)
        return doc
    
    def fetchList(self, ids, pname=None, async_req=False):
        """ 获取
        Args:
            ids (list[str]): 主键集
            pname (str): Partition名称
            async_req (bool): 异步否
        Returns:
        
        """
        if self.coll == None:
            return None
        
        docs = self.coll.fetch(ids, partition=pname, async_req=async_req)
        return docs
    
    def query(self, vector_text=None, pname=None, filter=None, id=None, output_fields=None, include_vector=False, topk=10, sparse_vector=None):
        """ 检索, 查出score最低的前几条数据, 0分匹配度最高, 排到最前, score越高排到越后
        Args:
            vector_text (str): 文本
            pname (str): Partition名称
            filter (str): 过滤条件, 如 'age > 18', 过滤条件一定是 createColl 是指定的 fields_schema 中的字段才有效, 
                否则报 {"code": -2015, "message": "Invalid Filter", "requests_id": "04e25459-55c9-42a2-9105-995f48b7f273"} 的错误
                条件支持 = 、> 、>= 、< 、<=、and、or、() 操作符，条件长度最大值为 10240, 如: 'age=30 and (weight=70 or weight>=80)'
            id (str): 主键, id与vectorText不能同时传
            output_fields (list[str]): ['name', 'age']
            include_vector: 是否返回向量数据, 默认false
            topk: 返回条数
            sparse_vector: TODO 稀疏向量?怎么得到
        Returns:
            {
                "code": 0, "message": "Success", "requests_id": "b2114f7d-7d5d-4ad3-8b88-2cf4993b5ad0", 
                "output": [
                    {"id": "102", "fields": {"age": 30, "weight": 70.0, "name": "zhangsan1"}, "score": -0.0}, 
                    {"id": "9999", "fields": {"name": "zhangsan1", "weight": 90.0, "age": 40}, "score": 0.9714}
                ], 
                "usage": {"read_units": 9}
            }
        """
        if self.coll == None:
            return None
        
        # 两者不能同时传值
        if id != None and vector_text != None:
            vector_text = None
            
        if id != None:
            id = str(id)
        
        r = self.coll.query(
            id=id,
            topk=topk,
            filter=filter,             
            partition=pname,
            output_fields=output_fields,
            include_vector=include_vector,
            vector=self.vectorization(vector_text),
            sparse_vector=sparse_vector
        )
        return r
    
    def queryGroupBy(self, group_by_field, vector_text=None, pname=None, group_count=10, group_topk=10, 
                     filter=None, id=None, output_fields=None, include_vector=False, sparse_vector=None, async_req=False):
        """ 检索
        Args:
            group_by_field (str): 分组字段
            vector_text (str): 向量文本
            pname (str): Partition名称
            group_count (str): 返回多少分组
            group_topk (str): 每组返回多少文档
            filter (str): 过滤条件, 如 age > 18
            id (int): 索引
            output_fields (list[str]): ['name', 'age']
            include_vector: 是否返回向量数据, 默认false
            sparse_vector (str): 
            async_req: 异步否
        Returns:
        
        """
        if self.coll == None:
            return None
        
        # 两者不能同时传值
        if id != None and vector_text != None:
            vector_text = None
        
        if id != None:
            id = str(id)
        
        r = self.coll.query_group_by(
            group_by_field=group_by_field,
            group_count=group_count,
            group_topk=group_topk,
            id=id,
            async_req=async_req,
            filter=filter,
            partition=pname,
            output_fields=output_fields,
            include_vector=include_vector,
            vector=self.vectorization(vector_text),
            sparse_vector=sparse_vector,
        )
        return r
    
  
        
if __name__ == '__main__':
    
    # setx ALIYUN_VECTOR_API_KEY 你的APIKEY 设置后需要重启
    # setx ALIYUN_VECTOR_API_URL 你的APIURL 设置后需要重启
    
    cname = 'group_by_demo'
    # pname = 'yiping2'
    # pname = None # 与 'default' 效果等同
    pname = 'default'
    
    vec = Vector(cname)
    
    # print('createColl: ')
    # c = vec.createColl(fields_schema={'name': str, 'weight': float, 'age': int})
    # print(c)
    
    # print('getColl: ')
    # c = vec.getColl(cname)
    # print(c)
    
   
    # print('deleteColl: ')
    # c = vec.deleteColl()
    # print(c)
   
    
    # print('descColl: ')
    # c = vec.descColl()
    # print(c)
    
    # print('statsColl: ')
    # a = vec.statsColl()
    # print(a)
    
    # print('getColls: ')
    # c = vec.getColls()
    # print(c)
    
    
    
    # print('createPart: ')
    # c = vec.createPart(pname)
    # print(c)
    
    # print('getParts: ')
    # c = vec.getParts()
    # print(c)
    
    # print('descPart: ')
    # c = vec.descPart(pname)
    # print(c)
    
    # print('statsPart: ')
    # c = vec.statsPart(pname)
    # print(c)
    
    # print('deletePart: ')
    # c = vec.deletePart(pname)
    # print(c)
    
    
    
    # print('insert: ')
    # r = vec.insert('勇敢', pname, '105', 
    # {
    #     # 'name': 'zhangsan1', 
    #     'weight':70.0, 
    #     'age':30,
    #     'www':'www'
    # })
    # print(r)
    
    
    # print('insertList: ')
    # docs = []
    # for i in range(3, 7):
    #     docs.append(vec.newDoc('' + str(i), i, {
    #             'name': 'zhangsan1', 
    #             'weight':70.0, 
    #             'age':30 
    #         })
    #     )
    # r = vec.insertList(docs, pname, True)
    # print(r)
    
    
    
    # print('upsert: ')
    # r = vec.upsert('rrrrrr', '102', pname, {
    #     'name': 'zhangsan111111111', 
    #     'weight':80.0, 
    #     'age':30 
    # })
    # print(r)
    
    # print('upsertList1: ')
    # docs = []
    # for i in range(5):
    #     docs.append(vec.newDoc('' + str(i), i, {
    #             'name': 'zhangsan1', 
    #             'weight':90.0, 
    #             'age':40 
    #         })
    #     )
    # r = vec.upsertList(docs, pname, True)
    # print(r)
    
    # print('upsertList2: ')
    # docs = []
    # for i in range(9999, 10000):
    #     # path = 'D:/测试文件/office/1.docx'
    #     # path = 'D:/测试文件/office/1.pptx'
    #     # path = 'D:/测试文件/office/1.xlsx'
    #     path = 'D:/测试文件/office/1.pdf'
    #     docs.append(vec.newDocWithFile(path, i, {
    #             'name': 'zhangsan1', 
    #             'weight':90.0, 
    #             'age':40 
    #         })
    #     )
    # r = vec.upsertList(docs, pname, True)
    # print(r)
    
    # print('update: ')
    # r = vec.update('rrrrrr', '101', pname)
    # print(r)
    
    # print('updateList: ')
    # docs = []
    # for i in range(3):
    #     docs.append(vec.newDoc('' + str(i), i, {
    #             'name': 'zhangsan1', 
    #             'weight':90.0, 
    #             'age':40 
    #         })
    #     )
    # r = vec.updateList(docs, pname, True)
    # print(r)
    
   
    
    # print('delete: ')
    # r = vec.delete('101', pname)
    # print(r)
    
    # print('deleteList: ')
    # r = vec.deleteList(['100', '101'], pname, True)
    # print(r)
    
    # print('deleteAll: ')
    # r = vec.deleteAll(pname, True)
    # print(r)
    
    
    
    
    # print('fetch: ')
    # r = vec.fetch('9999', pname)
    # print(r)
    
    # print('fetchList: ')
    # r = vec.fetchList(['100', '101'], pname)
    # print(r)
    
    
    # print('query: ')
    # r = vec.query('勇敢', pname, 'age=30 and (weight=70 or weight=80)', topk=2, include_vector=False)
    # print(r)
    # r = vec.query(None, pname, id=102, topk=2, include_vector=False)
    # print(r)
    
    
    # # 分组时, 一定要保证存在 Schema, 且字段是 Schema 中的字段, 不然会返回 'Invalid GroupBy Request'
    # print('queryGroupBy: ')
    # r = vec.queryGroupBy('name', 'rrrrrr', pname, 2, 2, id=6)
    # print(r)
    
    
    
    # print('vectorization: ')
    # c = vec.vectorization('你是我的眼')
    # print(c)
from peewee import fn
import mxupy as mu
from bigOAINet.db.rbac.m.RightCategory import RightCategory

class RightCategoryControl(mu.TreeEntityXControl):
    
    class Meta:
        model_class = RightCategory
        instance_name = 'rightCategoryControl'
        
    def __init__(self):
        
        paths = [
            mu.TreeDataPath(
                nameFieldName="name",
                namePathFieldName="namePath",
                isAllowRepeat=False,
                isAllowRepeatOfAll=True
            ),
            mu.TreeDataPath(
                nameFieldName="code",
                namePathFieldName="codePath",
                isAllowRepeat=False,
                isAllowRepeatOfAll=True
            )
        ]
        
        super().__init__(td=mu.TreeData(idFieldName='rightCategoryId', paths=paths))

if __name__ == '__main__':
    global rightCategoryControl
    rightCategoryControl = RightCategoryControl()
    mc = rightCategoryControl.model_class
    
    # id
    # path
    # depth
    # hasChildren
    # sort
    # parentId
    # name
    # namePath
    # code
    # codePath
    
    mc = rightCategoryControl.model_class
    
    where = {'id':('>', 100)}
    # print('\nsql')
    # exp, sql = rightCategoryControl.where_to_sql(where=where)
    # print(exp, '\n', sql)
    
    # print('\nexists')
    # im = rightCategoryControl.exists(where=where)
    # print(im)
    
    # print('\nexists_by_id')
    # im = rightCategoryControl.exists_by_id(id=8)
    # print(im)
    
    # print('\nget_count')
    # im = rightCategoryControl.get_count(where=where)
    # print(im)
    
    # order_by = {'id':'desc'}
    # order_by = [{'depth':'desc'}, {'code':'desc'}]
    # group_by = ['depth']
    # having = [{'id':('>', 0)}]
    
    
    print('\nget_one')
    im = rightCategoryControl.get_one(where=where, to_dict=True)
    print(im)
    # for i in range(10):
    #     im = rightCategoryControl.get_one(where=where, offset=i)
    #     print(im)
    
    print('\nget_one_by_id')
    im = rightCategoryControl.get_one_by_id(id=60, select=['code','name'],  to_dict=True)
    print(im)
    
    # print('\nget_list')
    # im = rightCategoryControl.get_list(where=where, order_by=order_by, limit=3, offset=2)
    # print(im)
    


    # print('\nadd')
    # im = rightCategoryControl.add(mc(path='1', depth='1', hasChildren='1', sort='1', parentId='1', name='12', namePath='12', code='12', codePath='1'))
    # im = rightCategoryControl.add({
    #     'path':'1', 'depth':'1', 'hasChildren':'1', 
    #     'sort':'1', 'parentId':'1', 'name':'12', 
    #     'namePath':'12', 'code':'12', 'codePath':'1'
    # })
    # print(im)
    
    # print('\nadd_or_update(add)')
    # im = rightCategoryControl.add_or_update(mc(path='1', depth='1', hasChildren='1', sort='1', parentId='1', name='12', namePath='12', code='12', codePath='1'))
    # print(im)
    # print('\nadd_or_update(update)')
    # im = rightCategoryControl.add_or_update(mc(id = 1, path='1', depth='1', hasChildren='1', sort='1', parentId='1', name='12', namePath='12', code='12', codePath='1'))
    # print(im)
    
    # print('\nupdate_by_id')
    # im = rightCategoryControl.update_by_id(7, mc(path='1', name='查询4'), fields=['name'])
    # print(im)
    
    # print('\nupdate')
    # # im = rightCategoryControl.update(where={'id':('>', 6)}, model=mc(path='9', name='查询9'), fields=['name','path'])
    # im = rightCategoryControl.update(where={'id':('>', 6)}, model={'path':'9', 'name':'查询8'}, fields=['name','path'])
    # print(im)
    
    # print('\ndelete')
    # im = rightCategoryControl.delete(where={'id':('>', 12)})
    # print(im)
    
    # print('\ndelete_by_id')
    # im = rightCategoryControl.delete_by_id(id=12)
    # print(im)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # qcs = [
    #     {'id':('>', 1)},
    #     # {'codePath':('=','')},
    #     # {'code':('&(contains))','v')},
    #     # {'code':('&(contains','v')},
    #     # {'code':('&(not_contains','v')},
    #     # [{'codePath':('!=(','')}, {'codePath':('&is_not_null)',)}, {'namePath':('((&=','')}, {'namePath':('|is_null))',)}],
        
    #     # [{'name':('=','添加')}, {'code':('=','add1')}],
    #     # [{'name':('=','添加')}, {'code':('&=','add')}],
        
    #     # {'codePath':('|is_nulL')},
    #     # {'codePath':('is_nulL')},
    #     # {'codePath':('is_null')},
        
    #     # {'id':1},
    #     # {'id':'1'},
        
    #     # {'name':1},
    #     # {'name':'1'},
        
    #     # {'code':('&(contains','v')},
    #     # {'code':('&(contains','v')},
    #     # {'code':('&(not_contains','v')},
        
        
    #     # {'codePath':''},
    #     # {'codePath':('=','')},
    #     # {'codePath':None},
    #     # {'codePath':'is_nulL'},
    #     # {'codePath':('is_nulL','')},
    #     # {'codePath':('=',None)},
    #     # [{'codePath':''}, {'codePath':'is_nulL'}],
    #     # [{'codePath':('=','')}, {'codePath':('=|',None)}],
    #     # [{'codePath':''}, {'codePath':('|is_nulL',)}],
    #     # [{'codePath':('!=','')}, {'codePath':('&is_Not_nulL',)}],
    #     # [{'codePath':('!=','')}, {'codePath':('!=&',None)}],
    #     # [{'id':('>=',2)}, {'id':('<',5)}],
    #     # [{'id':('!=',1)}, {'id':('<>',2)}],
    #     # [{'id':1}, {'name':1}],
    #     # None,
    #     # {'id':1},
    #     # [{'id':1}],
    #     # [{'id':('!=',1)}],
    #     # {'code':('&(contains','v')},
    #     # [{'name':('not_contains','投票')}, {'code':('&(contains','v')}, {'id':('|in)',[1,2,3])}],
    #     # [{'code':('&(contains','v')}, {'id':('|in)',[2,3])}],
    #     # [{'name':'is_null'}, {'code':('&contains','v')}, {'id':('in',[1,2,3])}],
    #     # {'parentId':'is_null'},
    #     # {'parentId':'is_not_null'},
    #     # {'parentId':('(is_null', '11111111')}, # value 会被忽略掉
    #     # {'parentId':('is_null')}
    # ]
    # for qc in qcs:
    #     # print()
    #     # rightCategoryControl.to_sql(qc)
        
    #     # im = rightCategoryControl.get_count(qc)
    #     # print("get_count:" + str(im))
        
    #     # im = rightCategoryControl.get_list(where=qc)
    #     # print("get_list:" + str(len(im)))
        
    #     im = rightCategoryControl.get_one(None, qc, {'name':'asc'})
    #     print("get_one:id=" + str(getattr(im, 'id', -1)) + getattr(im, 'name', ''))
        
    #     # print("get_one:id=" + str(getattr(im, 'id')) if im else '-1' + )
        
        
    #     # print(qc)
    #     # print()
    #     # rightCategoryControl.to_sql(qc)
    #     # print("get_one:id=" + str(getattr(im, 'id')) if im else -1)
    #     # # print("get_one:" + str(1 if im != None else 0))
        
        
    # im = rightCategoryControl.get_count({'id':'1', 'code':'vote'})
    # im = rightCategoryControl.get_count([
    #     { 'f':'id', 'v':2 }, 
    #     { 'f':'id', 'o':'=', 'v':2 }, 
    #     { 'f':'id', 'o':'=', 'v':1, 'lb':'((', 'rb':')', 't':'&'}, 
    #     { 'f':'id', 'o':'=', 'v':1, 'lb':'(', 'rb':'))', 't':'|'}
    # ])
    # im = rightCategoryControl.get_count({'id':1})
    # print(im)
    
    # im = rightCategoryControl.get_one(['name'], (mc.id > 1 & mc.id < 3))
    # print(im)
    
    # im = rightCategoryControl.get_one(['name'], (mc.id > 0 & mc.id < 4), mc.code.asc())
    # print(im)
    # im = rightCategoryControl.get_one(['name'], (mc.id > 0 & mc.id < 4), [mc.code.asc()])
    # print(im)
    # im = rightCategoryControl.get_one(['name'], (mc.id > 0 & mc.id < 4), [mc.code.asc(), mc.name.desc()])
    # print(im)
    
    # im = rightCategoryControl.get_one(['name'], (mc.id > 0 & mc.id < 4), mc.code.asc(), [mc.hasChildren])
    # print(im)
    
    # im = rightCategoryControl.get_one(['name'], (mc.id > 0 & mc.id < 4), order_by=None, group_by=[mc.hasChildren], having=fn.COUNT(mc.id) > 2)
    # print(im)
    
    # im = rightCategoryControl.get_one(['name'], (mc.id > 0 & mc.id < 4), order_by=None, group_by=None, having=(fn.COUNT(mc.id) > 1 & fn.COUNT(mc.id) < 100))
    # print(im)
    
    # im = rightCategoryControl.get_one(['name'], ((mc.id > 10) & (mc.id < 4)), order_by=mc.code.desc(), group_by=None, limit=10)
    # print(im)
    
    # im = rightCategoryControl.get_one(None, ((mc.id > 0) & (mc.id < 4)), order_by=mc.code.desc(), group_by=None, limit=10, to_dict=True)
    # im = rightCategoryControl.get_one(['name', 'parentId'], ((mc.id > 0) & (mc.id < 4)), order_by=mc.code.desc(), group_by=None, limit=10, to_dict=True, recurse=False)
    # im = rightCategoryControl.get_one(None, ((mc.id > 0) & (mc.id < 4)), order_by=mc.code.desc(), group_by=None, limit=10, to_dict=True, recurse=False)
    # im = rightCategoryControl.get_one(None, ((mc.id > 10) & (mc.id < 4)), order_by=mc.code.desc(), group_by=None, limit=10, to_dict=False, recurse=False)
    # im = rightCategoryControl.get_one(['name'], ((mc.id > 0) & (mc.id < 4)), order_by=mc.code.desc(), group_by=None, limit=10, to_dict=True)
    # im = rightCategoryControl.get_one(['name'], ((mc.id > 0) & (mc.id < 4)), order_by=mc.code.desc(), group_by=None, limit=10, to_dict=False)
    # print(im)
    
    # im = rightCategoryControl.get_list(None, ((mc.id > 1) & (mc.id < 4) | (mc.id = 1) ), order_by=mc.code.desc(), group_by=None, limit=10, to_dict=False, recurse=False)
    # im = rightCategoryControl.get_list(None, ((mc.id > 1) & (mc.id < 4)), order_by=mc.code.desc(), group_by=None, limit=10, to_dict=True, recurse=False)
    # print(im)
    
    # print(type(mc.name.contains('f')))
    # print(type(mc.id.in_([1, 2, 3])))
    # print(type(mc.name == '1' & (mc.name == '2')))
    
    # a = mc.name == '1' & (mc.name == '2' | mc.id == 1)
    # print(type(mc.name == '1' & (mc.name == '2' | mc.id == 1)))
    # print(1)
    
    # 'name' == '1' & ('name' == '2' | 'id' == 1) 动态变成 
    
    
    
    
    
    
    # rightCategoryControl.model_class.create(
    #     parentId=None,
    #     path='1', 
    #     depth=1,
    #     hasChildren=True,
    #     code='vote',
    #     codePath='vote',
    #     name='投票',
    #     namePath='投票',
    # )
    
    # rightCategoryControl.model_class.create(
    #     parentId=1,
    #     path='1,2', 
    #     depth=2,
    #     hasChildren=False,
    #     code='add',
    #     codePath='add',
    #     name='添加',
    #     namePath='添加',
    # )
    
    # rightCategoryControl.model_class.create(
    #     parentId=1,
    #     path='1,3', 
    #     depth=2,
    #     hasChildren=False,
    #     code='update',
    #     codePath='update',
    #     name='修改',
    #     namePath='修改',
    # )
    
    
    # # 是否匹配树形结构的字段
    # has = rightCategoryControl.has_pattern_fields()
    # print(has)
    # has = rightCategoryControl.has_pattern_fields(['path'])
    # print(has)
    # has = rightCategoryControl.has_pattern_fields(['name'])
    # print(has)
    # has = rightCategoryControl.has_pattern_fields(['name', 'path'])
    # print(has)
    
    # has = rightCategoryControl.has_same_name(
    #     mc(
    #         parentId=1,
    #         path='1,3', 
    #         depth=2,
    #         hasChildren=False,
    #         code='update2',
    #         codePath='update',
    #         name='修改1',
    #         namePath='修改'
    #     )
    # )
    # print(has)
    
    # im = rightCategoryControl.validate_name(
    #     mc(
    #         parentId=1,
    #         path='1,3', 
    #         depth=2,
    #         hasChildren=False,
    #         code='update1',
    #         codePath='update',
    #         name='',
    #         namePath='修改'
    #     )
    # )
    # print(im)
    
    # im = rightCategoryControl.fix_pattern(
    #     mc(
    #         parentId=None,
    #         path='1,3', 
    #         depth=2,
    #         hasChildren=False,
    #         code='update1',
    #         codePath='update',
    #         name='修改',
    #         namePath='修改'
    #     )
    # )
    # print(im)
    
    # print(rightCategoryControl.table_name)
    
    
    
    
    
    
    
    
    
    
    # id
    # path
    # depth
    # hasChildren
    # sort
    # parentId
    # name
    # namePath
    # code
    # codePath
    
    # mc = rightCategoryControl.model_class
    
    # # where = [{'codePath':('!=(','')}, {'codePath':('&is_not_null)',)}, {'namePath':('((&=','')}, {'namePath':('|is_null))',)}]
    # where = {'id':('>', 0)}
    # # 打印条件 sql
    # print('\nsql')
    # exp, sql = rightCategoryControl.where_to_sql(where=where)
    # print(exp, '\n', sql)
    
    # # 是否存在
    # print('\nexists')
    # im = rightCategoryControl.exists(where=where)
    # print(im)
    
    # print('\nexists_by_id')
    # im = rightCategoryControl.exists_by_id(id=8)
    # print(im)
    
    # # 获取数量
    # print('\nget_count')
    # im = rightCategoryControl.get_count(where=where)
    # print(im)
    
    # order_by = {'id':'desc'}
    # order_by = [{'depth':'desc'}, {'code':'desc'}]
    # group_by = ['depth']
    # having = [{'id':('>', 0)}]
    # # having = [{'codePath':('!=(','')}, {'codePath':('&is_not_null)',)}, {'namePath':('((&=','')}, {'namePath':('|is_null))',)}]
    # # having = {'id':5}
    
    # # 获取单条
    # print('\nget_one')
    # # im = rightCategoryControl.get_one(where=where, order_by=order_by, group_by=group_by, having=having, offset=0)
    # for i in range(10):
    #     im = rightCategoryControl.get_one(where=where, offset=i)
    #     print(im)
    
    # print('\nget_one_by_id')
    # im = rightCategoryControl.get_one_by_id(id=6, select=['code','name'])
    # print(im)
    
    # print('\nget_list')
    # # im = rightCategoryControl.get_list(where=where, order_by=order_by, group_by=group_by, having=having)
    # im = rightCategoryControl.get_list(where=where, order_by=order_by, limit=5, offset=2)
    # print(im)
    


    # print('\nadd')
    # im = rightCategoryControl.add(mc(path='1', depth='1', hasChildren='1', sort='1', parentId='1', name='12', namePath='12', code='12', codePath='1'))
    # print(im)
    
    # print('\nadd_or_update(add)')
    # im = rightCategoryControl.add_or_update(mc(path='1', depth='1', hasChildren='1', sort='1', parentId='1', name='12', namePath='12', code='12', codePath='1'))
    # print(im)
    # print('\nadd_or_update(update)')
    # im = rightCategoryControl.add_or_update(mc(id = 1, path='1', depth='1', hasChildren='1', sort='1', parentId='1', name='12', namePath='12', code='12', codePath='1'))
    # print(im)
    
    # print('\nupdate_by_id')
    # im = rightCategoryControl.update_by_id(7, mc(path='1', name='查询4'), fields=['name'])
    # print(im)
    
    # print('\nupdate')
    # im = rightCategoryControl.update(where={'id':('>', 6)}, model=mc(path='9', name='查询9'), fields=['name','path'])
    # print(im)
    
    # print('\ndelete')
    # im = rightCategoryControl.delete(where={'id':('>', 12)})
    # print(im)
    
    # print('\ndelete_by_id')
    # im = rightCategoryControl.delete_by_id(id=12)
    # print(im)
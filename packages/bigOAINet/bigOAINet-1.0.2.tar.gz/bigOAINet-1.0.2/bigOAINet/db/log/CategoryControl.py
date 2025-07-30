from peewee import Model, IntegerField, CharField, DateTimeField, DoesNotExist
from playhouse.shortcuts import model_to_dict
from datetime import datetime
from bigOAINet.db.log.m.Category import Category
from bigOAINet.db.log.LogControl import LogControl
from mxupy import IM, Condition, TreeEntityXControl, TreeData, TreeDataPath

class CategoryControl(TreeEntityXControl):
    instance = None

    @staticmethod
    def get_instance():
        if CategoryControl.instance is None:
            CategoryControl.instance = CategoryControl(TreeData(
                id_field_name='category_id',
                parent_id_field_name='parent_category_id',
                paths=[TreeDataPath(
                    name_field_name='name',
                    name_path_field_name='name_path',
                    is_allow_repeat=False
                )]
            ))
        return CategoryControl.instance

    def __init__(self, tree_data):
        self.tree_data = tree_data


    def add(self, name_path):
        im = IM()
        if not name_path:
            return im.error("添加失败，namePath不能为空。")
        
        categories = name_path.split('/')
        pid = 0
        for i, name in enumerate(categories):
            name_path = '/'.join(categories[:i+1])
            try:
                entity = Category.get(Category.name_path == name_path)
            except DoesNotExist:
                entity = Category.create(
                    name=name,
                    parent_category_id=pid,
                    add_time=datetime.now()
                )
                im.result = entity.id
                if im.is_error:
                    return im
                pid = entity.id
            else:
                pid = entity.id
        return im

    def delete(self, id, is_exists_verify=True):
        im = IM()
        try:
            if Category.select().where(Category.parent_category_id == id).exists():
                return im.error("删除失败，该分类下有子分类。")
            if LogControl.get_instance().exists(Condition("category_id", "=", id)):
                return im.error("删除失败，该分类下有注册项。")
            return super().delete(id, is_exists_verify)
        except DoesNotExist:
            return im.error("分类不存在。")

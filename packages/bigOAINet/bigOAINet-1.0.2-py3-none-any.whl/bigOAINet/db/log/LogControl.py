from datetime import datetime
from threading import Lock
from mxupy import IM, EntityXControl

class LogControl(EntityXControl):
    _lock_add = Lock()
    _lock_log = Lock()
    
    _cache_of_logs = []
    _cache_of_logs_to_file = []

    def log(self, name_path, title, content="", level=1, link_id=-1, link_type="", link_id2=-1, link_type2="", ext_data="", is_to_file=True):
        user_id = -1
        entity = self.add(
            title=title,
            content=content,
            ip='获取IP地址',
            add_time=datetime.now(),
            level=level,
            link_id=link_id,
            link_type=link_type,
            link_id2=link_id2,
            link_type2=link_type2,
            ext_data=ext_data,
            name_path=name_path,
            user_id=user_id
        )

        items = self._cache_of_logs_to_file if is_to_file else self._cache_of_logs
        items.append(entity)

        if len(items) >= 50:
            for item in items:
                # 这里添加逻辑，例如批量插入数据库或写入文件
                pass
            self._cache_of_logs_to_file = [] if is_to_file else self._cache_of_logs

        return IM(result=entity.id)



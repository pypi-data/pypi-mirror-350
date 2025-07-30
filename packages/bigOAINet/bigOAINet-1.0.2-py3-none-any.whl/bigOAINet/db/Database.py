from mxupy import DatabaseHelper, read_config
import bigOAINet as bigo
# 读取配置信息
dbi = read_config().get('database', {})
# print(dbi)

# 名称、用户名、密码、地址、端口
name = dbi.get('name', '')
username = dbi.get('username', 'root')
password = dbi.get('password', '')
host = dbi.get('host', '127.0.0.1')
port = int(dbi.get('port', '3306'))

# 编码、最大连接数、空闲时长、超时时长、模型路径
charset = dbi.get('charset', 'utf8')
max_connections = int(dbi.get('max_connections', '100000'))
stale_timeout = int(dbi.get('stale_timeout', '60'))
timeout = int(dbi.get('timeout', '60'))

dh = DatabaseHelper(name=name, username=username, password=password, host=host, port=port,
                    charset=charset, stale_timeout=stale_timeout, timeout=timeout,  max_connections=max_connections)
db = dh.db

if __name__ == '__main__':
    # db.connect()
    # db.drop_tables([bigo.Agent])
    db.create_tables([bigo.KeyValue, bigo.ValueEx, bigo.Industry, bigo.Attachment, bigo.Card, bigo.Country, bigo.Province, bigo.City, bigo.County, bigo.Enterprise, bigo.EnterpriseUser, bigo.DepartmentType, bigo.Department, bigo.User, bigo.UserBind, bigo.UserNoBind, bigo.Login, bigo.DepartmentUser, bigo.DepartmentManager, bigo.DepartmentAndSubject, bigo.Duty, bigo.DutyUser, bigo.Muster, bigo.MusterDepartment, bigo.ProRank, bigo.ProRankUser, bigo.Group, bigo.GroupUser, bigo.FriendGroup, bigo.Friend, bigo.Invitation, bigo.Category, bigo.Log, bigo.RightCategory, bigo.Right, bigo.RightAndData, bigo.RoleCategory, bigo.Role, bigo.RoleAndSubject, bigo.RoleAndRight, bigo.RoleExclusive, bigo.RoleInherit, bigo.Agent, bigo.KB, bigo.AgentUser, bigo.Room, bigo.Session, bigo.Chat, bigo.RoomUser])
    # db.close()

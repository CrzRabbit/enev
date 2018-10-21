import aiomysql
from common.common import *
from debug.log import *

def log(sql, args=()):
    logi(logcf.database, 'SQL: {0}{1}'.format(sql, ' % {0}'.format(tuple(args)) if args else ''))

async def create_pool(loop, **kw):
    logi(logcf.base, 'create database connection pool...')
    global __pool
    __pool = await aiomysql.create_pool(
        host=kw.get('host', '127.0.0.1'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['database'],
        charset=kw.get('charset', 'utf8'),
        autocommit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop
    )

async def select(sql, args, size=None):
    log(sql.replace('?', '%s'), args)
    global __pool
    with (await __pool) as conn:
        cur = await conn.cursor(aiomysql.DictCursor)
        try:
            await cur.execute(sql.replace('?', '%s'), args or ())
        except Exception as e:
            loge(logcf.database, '{}\n'.format(e))
        if size:
            rs = cur.fetchmany(size)
        else:
            rs = cur.fetchall()
        await cur.close()
        return rs

async def execute(sql, args, autocommit=True):
    log(sql.replace('?', '%s'), args)
    affected = None
    with (await __pool) as conn:
        if not autocommit:
            await conn.begin()
        try:
            cur = await conn.cursor()
            await cur.execute(sql.replace('?', '%s'), args or ())
            affected = cur.rowcount
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            pass
            loge(logcf.database, '{}\n'.format(e))
        return affected

class ModelMetaClass(type):

    def __new__(cls, name, bases, attrs):
        #排除Model类本身
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        #获取tablename
        tableName = attrs.get('__table__', None) or name
        tableId = attrs.get('__id__', None)
        tableIdB = attrs.get('__id_b__', None)
        logi(logcf.modle, 'Find model {0} (table {1}).'.format(name, tableName))
        #获取所有field和主键名
        mappings = dict()
        fields = []
        primary_key = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                mappings[k] = v
                if v.primary_key:
                    if primary_key:
                        raise RuntimeError('Duplicate primary key for field: {0}.'.format(k))
                    primary_key = k
                else:
                    fields.append(k)

        if not primary_key:
            raise RuntimeError('Primary key not found.')
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '{0}'.format(f), fields))
        attrs['__mappings__'] = mappings        #映射关系
        attrs['__table__'] = tableName          #表名
        attrs['__primary_key__'] = primary_key  #主键
        attrs['__fields__'] = fields            #其他属性
        attrs['__id__'] = tableId
        attrs['__id_b__'] = tableIdB
        #构造默认的select, insert, update, delete, delete all语句
        attrs['__select__'] = 'SELECT {0}, {1} FROM {2} '.format(primary_key, ', '.join(escaped_fields), tableName)
        attrs['__insert__'] = 'INSERT INTO {0} ({1}) VALUES ({2})'.format(tableName, ', '.join(escaped_fields), create_args_string(len(escaped_fields)))
        attrs['__update__'] = 'UPDATE {0} set {1} WHERE {2}=?'.format(tableName, ', '.join(map(lambda f: '{0}=?'.format(mappings.get(f).name or f), fields)), primary_key)
        attrs['__delete__'] = 'DELETE FROM {0} WHERE {1}=?'.format(tableName, primary_key)
        attrs['__delete_all__'] = 'DELETE FROM {0}'.format(tableName)
        #attrs['__insert__'] = 'INSERT INTO {0} ({1}) VALUES ({2})'.format(tableName, ', '.join(escaped_fields), create_args_string(len(escaped_fields)))
        #print(attrs)
        return type.__new__(cls, name, bases, attrs)

def create_args_string(len):
    args = list()
    for i in range(len):
        args.append("?")
    return ', '.join(args)

class Model(dict, metaclass=ModelMetaClass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' has no key {0}.".format(key))

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logd(logcf.modle, 'Using default value for {0}: {1}'.format(key, value))
                setattr(self, key, value)
        return value

    @classmethod
    async def find(cls, pk):
        rs = await select('{0} where {1}=?'.format(cls.__select__, cls.__primary_key__), [pk], 1)
        if len(rs._result) == 0:
            return None
        return cls(**rs._result[0])

    @classmethod
    async def findAll(cls, where=None, args=None, **kw):
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = dict()
        orderby = kw.get('orderby', None)
        if orderby:
            sql.append('orderby')
            sql.append(orderby)
        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, dict) and len(limit) == 2:
                sql.append('?, ?')
                args.extend(limit)
            else:
                raise ValueError('Invalit limit value: {0}'.format(limit))
        rs = await select(' '.join(sql), args)
        if len(rs._result) == 0:
            return returncode.fail, None
        return returncode.success, [cls(**r) for r in rs._result]

    @classmethod
    async def clear(cls):
        args = list()
        rows = await execute(cls.__delete_all__, args)
        logd(logcf.modle, 'Clear completed, {0} rows affected'.format(rows))

    async def save(self):
        rows = None
        args = list(map(self.getValueOrDefault, self.__fields__))
        #args.append('{0}'.format(self.getValueOrDefault(self.__primary_key__)))
        rows = await execute(self.__insert__, args)
        if rows != 1:
            logw(logcf.database, 'Insert value failed, affected rows: {0}'.format(rows))
        elif rows == 1:
            logi(logcf.database, 'Insert success.')
            return returncode.success
        return returncode.fail

    async def update(self):
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        rows = await execute(self.__update__, args)
        if rows == 0:
            logw(logcf.database, 'Updata value failed, no rows affected.')
            return returncode.fail
        elif rows==1:
            logi(logcf.database, 'Update success.')
            return returncode.success
        return returncode.fail

    @classmethod
    async def verify(cls, *args):
        level = args.__len__()
        sql = cls.__select__
        sql += 'where'
        sql += ' {}=?'.format(cls.__id__[0])
        for i in range(1, level):
            sql += ' and {}=?'.format(cls.__id__[i])
        rs = await select(sql, args, 1)
        if len(rs._result) == 0:
            #print(rs._result)
            return returncode.fail, None
        return returncode.success, cls(**rs._result[0])

    @classmethod
    async def verify_b(cls, *args):
        level = args.__len__()
        sql = cls.__select__
        sql += 'where'
        sql += ' {}=?'.format(cls.__id_b__[0])
        for i in range(1, level):
            sql += ' and {}=?'.format(cls.__id_b__[i])
        rs = await select(sql, args, 1)
        if len(rs._result) == 0:
            # print(rs._result)
            return returncode.fail, None
        return returncode.success, cls(**rs._result[0])

    async def remove(self):
        args = list()
        args.append(self.getValue(self.__primary_key__))
        rows = await execute(self.__delete__, args)
        if rows != 1:
            logw(logcf.database, 'Remove failed, {0} rows affected.'.format(rows))
            return returncode.fail
        elif rows == 1:
            return returncode.success
        return returncode.fail

class Field(object):

    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<{0} {1}: {2}>'.format(self.__class__.__name__, self.column_type, self.name)

class StringField(Field):

    def __init__(self, name = None, primary_key = False, default = None, ddl = 'varchar(100)'):
        super().__init__(name, ddl, primary_key, default)

class IntegerField(Field):

    def __init__(self, name = None, primary_key = False, default = None, ddl = 'bigint'):
        super().__init__(name, ddl, primary_key, default)

class BooleanField(Field):

    def __init__(self, name = None, primary_key = False, default = False, ddl = 'boolean'):
        super().__init__(name, ddl, primary_key, default)

class FloatField(Field):

    def __init__(self, name = None, primary_key = False, default = 0., ddl = 'real'):
        super().__init__(name, ddl, primary_key, default)

class TextField(Field):

    def __init__(self, name = None, primary_key = False, default = '', ddl = 'text'):
        super().__init__(name, ddl, primary_key, default)
import asyncio
import aiomysql
import logging; logging.basicConfig(level=logging.INFO)

def log(sql, args=()):
    logging.info('SQL: {0}{1}'.format(sql, ' % {0}'.format(tuple(args)) if args else ''))

@asyncio.coroutine
def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    print(kw)
    global __pool
    __pool = yield from aiomysql.create_pool(
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

@asyncio.coroutine
def select(sql, args, size=None):
    log(sql.replace('?', '%s'), args)
    global __pool
    with (yield from __pool) as conn:
        cur = yield from conn.cursor(aiomysql.DictCursor)
        yield from cur.execute(sql.replace('?', '%s'), args or ())
        if size:
            rs = cur.fetchmany(size)
        else:
            rs = cur.fetchall()
        yield from cur.close()
        #logging.info('Rows returned: {0}'.format(len(rs)))
        return rs

@asyncio.coroutine
def execute(sql, args, autocommit=True):
    log(sql.replace('?', '%s'), args)
    with (yield from __pool) as conn:
        if not autocommit:
            yield from conn.begin()
        try:
            cur = yield from conn.cursor()
            cur.execute(sql.replace('?', '%s'), args or ())
            affected = cur.rowcount
            if not autocommit:
                yield from conn.commit()
        except BaseException as e:
            if not autocommit:
                yield from conn.rollback()
            raise
        return affected

class ModelMetaClass(type):

    def __new__(cls, name, bases, attrs):
        #排除Model类本身
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        #获取tablename
        tableName = attrs.get('__table__', None) or name
        logging.info('Find model {0} (table {1}).'.format(name, tableName))
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
        #构造默认的select, insert, update, delete, delete all语句
        attrs['__select__'] = 'SELECT {0}, {1} FROM {2} '.format(primary_key, ', '.join(escaped_fields), tableName)
        attrs['__insert__'] = 'INSERT INTO {0} ({1}, {2}) VALUES ({3})'.format(tableName, ', '.join(escaped_fields), primary_key, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'UPDATE {0} set {1} WHERE {2}=?'.format(tableName, ', '.join(map(lambda f: '{0}=?'.format(mappings.get(f).name or f), fields)), primary_key)
        attrs['__delete__'] = 'DELETE FROM {0} WHERE {1}=?'.format(tableName, primary_key)
        attrs['__delete_all__'] = 'DELETE FROM {0}'.format(tableName)
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
                logging.debug('Using default value for {0}: {1}'.format(key, value))
                setattr(self, key, value)
        return value

    @classmethod
    @asyncio.coroutine
    def find(cls, pk):
        rs = yield from select('{0} where {1}=?'.format(cls.__select__, cls.__primary_key__), [pk], 1)
        if len(rs.__dict__['_result']) == 0:
            return None
        return cls(**rs.__dict__['_result'][0])

    @classmethod
    @asyncio.coroutine
    def findAll(cls, where=None, args=None, **kw):
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
        rs = yield from select(' '.join(sql), args)
        return [cls(**r) for r in rs.__dict__['_result']]

    @classmethod
    @asyncio.coroutine
    def clear(cls):
        args = list()
        rows = yield from execute(cls.__delete_all__, args)
        logging.warning('Clear completed, {0} rows affected'.format(rows))

    @asyncio.coroutine
    def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append('{0}'.format(self.getValueOrDefault(self.__primary_key__)))
        rows = yield from execute(self.__insert__, args)
        if rows != 1:
            logging.warning('Insert value failed, affected rows: {0}'.format(rows))
        elif rows == 0:
            logging.warning('Insert success~!')

    @asyncio.coroutine
    def update(self):
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        rows = yield from execute(self.__update__, args)
        if rows == 0:
            logging.warning('Updata value failed, no rows affected.')

    @asyncio.coroutine
    def remove(self):
        args = list()
        args.append(self.getValue(self.__primary_key__))
        rows = yield from execute(self.__delete__, args)
        if rows != 1:
            logging.warning('Remove failed, {0} rows affected.'.format(rows))


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
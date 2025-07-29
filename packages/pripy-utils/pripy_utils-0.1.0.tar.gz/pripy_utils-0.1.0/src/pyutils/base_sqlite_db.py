from abc import ABC, abstractmethod


class BaseSqliteDb(ABC):
    def __init__(self):
        self.db_name = ""
        self.db_connection = None
        self.data_path = ""
        pass
    #创建数据库
    @abstractmethod
    def create_db(self, db_name: str):
        """创建数据库"""
        pass
    def drop_db(self, db_name: str):
        """删除数据库"""
        pass
    def drop_table(self, table_name: str):
        """删除表"""
        pass
    #CRUD operations
    @abstractmethod
    def create_table(self, tabel_name: str, table_fields: dict):
        """创建表"""
        pass
    @abstractmethod
    def insert_table(self, table_name: str, data: dict):
        """插入"""
        pass
    def update_table(self, table_name: str, data: dict):
        """更新"""
        pass
    def delete_table(self, table_name: str, data: dict):
        """删除"""
        pass
    def select_table(self, table_name: str, data: dict):
        """查询"""
        pass
    pass

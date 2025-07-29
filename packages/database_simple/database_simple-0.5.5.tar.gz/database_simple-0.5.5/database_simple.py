"""
Made by HQO (https://github.com/MAJHQO) and idea extended from library: database_creatorplus (https://pypi.org/project/database-creatorplus/)
"""

import psycopg2 as psy, sqlite3 as sq,flet as ft

__version__="0.5.5"

class Database:

    def __init_tables__(self):
        try:
            if(self.connect_type==True):
                self.cursor.execute("Select table_name FROM information_schema.tables where table_schema='public'")
            else:
                self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type = 'table'")
            tables_name=self.cursor.fetchall()
            if(len(tables_name)!=0):
                for name in tables_name:
                    columns_table=[]
                    if(self.connect_type==True):
                        self.cursor.execute(f"Select column_name from information_schema.columns where table_name='{name[0]}'")
                    else:
                        self.cursor.execute(f"Select name from Pragma_table_info('{name[0]}')")
                    columns=self.cursor.fetchall()
                    for column_name in columns:
                        columns_table.append(column_name[0])
                    self.__tables__[name[0]]=self.__Table(columns_table,1300, name[0], self)
        except Exception as ex:
            raise Exception(f"{ex}")

    def __init__(self, bd_type:bool, **kwargs):
        """
        Используется для создания и взаимодействия с базой данных

        - [bd_type]: определяет тип используемой базы данных
            - False: sqlite3
            - True: psycopg2
        - [kwargs]: принимает именованные аргументы для инициализации объекта базы данных
        """
        try:
            self.__connect__= psy.connect(database=kwargs['database'], password=kwargs['password'], user=kwargs['user'], port=kwargs['port']) if bd_type else sq.connect(kwargs['db_name'], check_same_thread=False)
            self.cursor=self.__connect__.cursor()
            self.connect_type=bd_type
            self.__tables__={}
            self.__init_tables__()

        except Exception as ex:
            raise Exception(f"{ex}")
        
    def request_execute(self, request:str):
        """
        Используется для выполнения SQL - запросов в базу данных
        """
        try:
            self.cursor.execute(request)
            self.__connect__.commit()
            if(request.lower().find("select")!=-1):
                return self.cursor.fetchall()
        except Exception as ex:
            raise Exception(f"{ex}")
        
    def create_table(self, table_name:str, table_structure:dict[str:str], table_width:int):
        """
        Используется для создания таблицы в базе данных

        [table_structure]: содержит столбцы их типы данных в виде {'cell_name':'cell_type'}
        """
        try:
            if(self.__tables__.get(table_name)==None):
                keys=table_structure.keys()
                values_str=""
                columns=[]
                for key in keys:
                    values_str+=f"{key} {table_structure[key]}, "
                    columns.append(key)
                self.cursor.execute(f"Create table {table_name}({values_str[:-2]})")
                self.__tables__[table_name]=self.__Table(columns,table_width ,table_name,self)
                self.__connect__.commit()
        except Exception as ex:
            raise Exception(f"{ex}")
        
    def drop_all_tables(self):
        """
        Метод для удаления всех таблиц из базы данных
        """
        try:
            self.cursor.execute("DROP SCHEMA public CASCADE;")
            self.__connect__.commit()
            self.cursor.execute("CREATE SCHEMA public;")
            self.__connect__.commit()
        except Exception as ex:
            raise Exception(f"{ex}")
        
    class __Table:
        def __init__(self, column:list[str], table_width:int, table_name:str, db_object):
            self.__column=[ft.DataColumn(ft.Text(data, width=200, text_align=ft.TextAlign.CENTER)) for data in column]
            self.table_name=table_name
            self.__cursor__=db_object.cursor
            self.__table=ft.Column(
                [ft.DataTable(self.__column,[], width=table_width)],
                width=table_width,height=300, scroll=ft.ScrollMode.ADAPTIVE)
        def isfloat(value):
            try:
                float(value)
                return True
            except ValueError:
                return False
            
        def viewMode(self,obj):
            view_dialog=ft.AlertDialog(
                title=ft.Text("Просмотр данных", size=14), 
                content=ft.Text(obj.control.data.split('|')[0], size=13),
                actions=[ft.ElevatedButton("Выйти", color=ft.Colors.RED, on_click=lambda _:obj.page.close(view_dialog))])
            obj.page.open(view_dialog)

        def changeMode(self,obj):
            change_dialog=ft.AlertDialog(
                title=ft.Text("Изменение данных", size=14), 
                actions=[
                    ft.ElevatedButton("Изменить", on_click=self.__updateCellData__),
                    ft.ElevatedButton("Выйти", color=ft.Colors.RED, on_click=lambda _: obj.page.close(change_dialog))])
            if (obj.control.data.lower().find("references")!=-1):
                change_dialog.content=ft.DropdownM2(options=[])
                
            else:
                pass

            obj.page.open(change_dialog)

        def viewMode_handler(self,obj):
            if (type(obj.page.controls[1])==ft.Column and type(obj.page.controls[1].controls[0])==ft.DataTable):
                for rows in obj.page.controls[1].rows:
                    for i in range(0,len(rows)):
                        if(i!=0):
                            rows[i].on_click=self.viewMode

                obj.control.value='Изменение'
                obj.control.on_click=self.changeMode_handler

        def changeMode_handler(self,obj):
            if (type(obj.page.controls[1])==ft.Column and type(obj.page.controls[1].controls[0])==ft.DataTable):
                for rows in obj.page.controls[1].rows:
                    for i in range(0,len(rows)):
                        if(i!=0):
                            rows[i].on_click=self.changeMode

                obj.control.value='Просмотр'
                obj.control.on_click=self.viewMode_handler
            
        def getTable(self, db_object:object):
            self.__cursor__.execute(f"Select * from {self.table_name}")
            result=self.__cursor__.fetchall()
            columns=db_object.get_table_columns(self.table_name).split(",")
            columns_type=db_object.get_table_columns_type(self.table_name)

            if(len(self.__table.controls[-1].rows)):
                self.__table.controls[-1].rows.clear()
            
            if (len(result)==0):
                return False

            for row in result:
                self.__table.controls[-1].rows.append(ft.DataRow([]))
                for i in range(0,len(row)):
                    if(i==0):
                        self.__table.controls[-1].rows[-1].cells.append(ft.DataCell(
                            ft.TextField(
                                str(row[i]), 
                                read_only=True, 
                                border_color=ft.Colors.TRANSPARENT, 
                                width=200, 
                                text_align=ft.TextAlign.CENTER)
                        ))
                    else:
                        self.__table.controls[-1].rows[-1].cells.append(ft.DataCell(
                            ft.TextField(
                                str(row[i]), 
                                read_only=True, 
                                border_color=ft.Colors.TRANSPARENT, 
                                width=200, 
                                text_align=ft.TextAlign.CENTER,
                                on_click=self.viewMode,
                                data=f"{row[i]}|{row[0]}|{columns[i]}|{self.table_name}|{columns_type[i][0]}")
                        ))
            return self.__table

        def select_request(self, columns:str, contidion:str):
            try:
                self.__cursor__.execute(f"Select {columns} from {self.table_name} where {contidion}")
                return self.__cursor__.fetchall()
            except Exception as ex: 
                raise Exception(f"{ex}")
            
        def delete_request(self, db_object:object,contidion=""):
            f"""
            Используеся для удаления данных из таблицы {self.table_name}
            
             - [contidion | условие]: если данный параметр не передан в метод - запрос осуществляет удаление все записей из таблицы
            """
            try:
                if (len(contidion)==0):
                    self.__cursor__.execute(f"Delete from {self.table_name}")
                else:
                    self.__cursor__.execute(f"Delete from {self.table_name} where {contidion}")
                db_object.__connect__.commit()
            except Exception as ex: 
                raise Exception(f"{ex}")
            
        def insert_request(self, values:list, db_object:object):
            """
            Используется для записи данных в таблицу
             - (values) [column_value]: по порядку нахождения столбцов в таблице
            """
            try:
                values_str=""
                columns_str=db_object.get_table_columns(self.table_name)
                for elem in values:
                    if(type(elem) not in [int, float]):
                        values_str+=f"'{elem}', "
                    else:
                        values_str+=f"{elem}, "
                self.__cursor__.execute(f"Insert into {self.table_name}({columns_str}) values ({values_str[:-2]})")
                db_object.__connect__.commit()
            except Exception as ex: 
                raise Exception(f"{ex}")
            
        def update_request(self, set_values:dict, condition: str, db_object:object):
            """
            Используется для обновления данных в таблице
             - (set_values) {column_name: column_value}
            """
            try:
                columns=list(set_values)
                set_expression=""
                for column in columns:
                    if (type(set_values[column]) not in [int, float]):
                        set_expression+=f"Set {column}='{set_values[column]}', "
                    else:
                        set_expression+=f"Set {column}={set_values[column]}, "
                self.__cursor__.execute(f"Update table {self.table_name} {set_expression[:-2]} where {condition}")
                db_object.__connect__.commit()
            except Exception as ex: 
                raise Exception(f"{ex}")
            
        def __updateCellData__(self, obj, db_object:object):
            try:
                if (obj.page.overlay[-1].content.value!=obj.control.data.split('|')[0]):
                    if (obj.page.overlay[-1].content.value.isdigit() or self.isfloat(obj.page.overlay[-1].content.value)):
                        self.__cursor__.execute(f"Update table {self.table_name} set {obj.control.data.split('|')[2]}={obj.page.overlay[-1].content.value}")
                    else:
                        self.__cursor__.execute(f"Update table {self.table_name} set {obj.control.data.split('|')[2]}='{obj.page.overlay[-1].content.value}'")
                    db_object.__connect__.commit()
                else:
                    return False
            except Exception as ex:
                raise Exception(f"{ex}")
        
    # def load_table(self, table_name:str|list, table_width:int) -> __Table | None:
    #     """
    #     Инициализирует Table объекты, для возможности использования [get_table_obj]
    #     """
    #     if(type(table_name)==str):
    #         column=self.get_table_columns(table_name).split(',')
    #         self.__tables__[table_name]=self.__Table(column,table_width,table_name,self)
    #         return self.__tables__[table_name]
    #     else:
    #         for table in table_name:
    #             column=self.get_table_columns(table).split(',')
    #             self.__tables__[table]=self.__Table(column,table_width,table_name,self)
    
    def get_table_obj(self, table_name:str)->__Table:
        """
        Возвращает объект Table, позволяющие взаимодействовать с конкреткной таблицей в базе данных
        """
        try:
            return self.__tables__[table_name] if self.__tables__.get(table_name)!=None else self.load_table()
        except Exception as ex:
            raise Exception(f"{ex}")
        
    def get_table_columns(self, table_name:str):
        """
        Возвращает столбцы заданной таблицы 
        """
        try:
            if(self.__tables__[table_name]!=None):
                if (self.connect_type):
                    self.cursor.execute(f"Select column_name from information_schema.columns where table_name='{table_name}'")
                else:
                    self.cursor.execute(f"SELECT name FROM PRAGMA_TABLE_INFO('{table_name}')")
                result=self.cursor.fetchall()
                column_str=""
                for column in result:
                    column_str+=column[0]+", "
                return column_str[:-2]
            else:
                return False
        except Exception as ex:
            raise Exception(f"{ex}")
        
    def get_table_columns_type(self, table_name:str):
        """
        Возращает типы столбцов заданной таблицы в порядке возрастания (от 1 к последнему)
        """
        try:
            if(table_name in self.__tables__.keys()):
                if(self.connect_type):
                    self.cursor.execute(f"Select data_type from information_schema.columns where table_name='{table_name}'")
                else:
                    self.cursor.execute(f"SELECT type FROM PRAGMA_TABLE_INFO('{table_name}')")
                result=self.cursor.fetchall()
                return result
            else:
                return False
        except Exception as ex:
            raise Exception(f"{ex}")
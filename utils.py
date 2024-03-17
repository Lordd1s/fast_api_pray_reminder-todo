import time
import aiohttp
import aiofiles
import json
import aiosqlite


async def create_sql():
    async with aiosqlite.connect("database(sqlite3)/database.db") as conn:
        # cur.execute("CREATE TABLE todos(id INTEGER PRIMARY KEY AUTOINCREMENT, todo TEXT, when_to_do VARCHAR(20))")
        # cur.execute("ALTER TABLE todos ADD description TEXT NULL;")
        await conn.execute("INSERT INTO todos(description) VALUES ('description')")

        # cur.execute("SELECT * FROM todos")
        # result = cur.fetchall()
        # print(result)


class Parse:
    @staticmethod
    async def load_api(file_path_name: str):
        """
        params: file_path_name take only ".json" files to read!
        returns: coroutine object
        """
        async with aiofiles.open(file_path_name, mode="r", encoding="utf-8") as file:
            content = await file.read()
            return json.loads(content)

    @staticmethod
    async def dump_api(response_obj: str, file_name_path: str):
        """
        This method works only with module "aiohttp" and "aiofiles"!
        params: file_name_path take only '.json' files!
                      response_obj accepts an object(website) to be parsed!
        """
        head = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    response_obj, headers={"User-Agent": head}
                ) as response:
                    data = await response.json()
                    async with aiofiles.open(
                        file_name_path, mode="w", encoding="utf-8"
                    ) as file:
                        await file.write(json.dumps(data, indent=4, ensure_ascii=False))
            return True
        except aiohttp.ClientError as e:
            print(f"An error occurred: {e}")
            return False


class Todo:
    """
    First you will need to database(.db) file!
    """

    def __init__(self, path: str):
        self.path = path

    async def db_operations(
        self, query: str, many: bool = True, pk: tuple[int] = None, value: tuple = None
    ):
        print(query.split()[0])
        """_summary_

        Args:
            query (str): SQL query
            many (bool, optional): if "query" starting with 'SELECT' 
                                    You can return one(False) or many(True) objects from [table_name]. Defaults to True.
            pk (tuple[int], optional): This argument need to 'UPDATE' or 'DELETE'! 
                                Like 'WHERE id = pk' in SQL. Defaults to None.
            value (tuple, optional): "value" to 'UPDATE' or 'INSERT' method. 
                                    "value" can take "pk" too (example: value=(some_val, ...,  pk) <- by order)
                                                                            ^ if you use parameter WHERE [] = ?. 
                                    Defaults to None!
            
        Returns:
            str: Success(list_type_object) or failure message(sqlite3.Error_type)
        """
        async with aiosqlite.connect(self.path) as conn:
            cursor = await conn.cursor()
            try:
                match query.split()[0]:
                    case "SELECT":
                        await cursor.execute(query)
                        rows = await cursor.fetchall() if many else await cursor.fetchone()
                        return rows
                    case "DELETE":
                        await cursor.execute(query, (pk,))
                        await conn.commit()
                    case "UPDATE":
                        try:
                            await cursor.execute(query, value)
                        except aiosqlite.Error as e:
                            await conn.rollback()
                            return e
                        else:
                            await conn.commit()
                    case "INSERT":
                        try:
                            await cursor.execute(query, value)
                        except aiosqlite.Error as e:
                            await conn.rollback()
                            return e
                        else:
                            await conn.commit()
            except aiosqlite.Error as e:
                return e


if __name__ == "__main__":
    # TODO Manual TESTS
    # create_sql()
    # time.sleep(2)
    a = Todo("database(sqlite3)/database.db")

    # sql_update_query = """UPDATE todos SET description = ? where id = ?"""
    # data = ("test 2023", 1)
    # a.db_operations(sql_update_query, value=data)

    # a.db_operations("UPDATE todos SET description = ? WHERE id = ?", value=("test", 1))
    # print(a.db_operations("DELETE FROM todos WHERE id = ?", pk=(3,)))
    # print(type(sqlite3.Error))
    # print(a.db_operations("SELECT * FROM todos ORDER BY when_to_do"))

    # print("2023-09-04" < "2023-09-03")
    ...

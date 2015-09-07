import os, sys, unittest

sys.path.append("..")
sys.path.append("../../Frame_Mock")
# needed for framework module
sys.path.append("../../DB_Framework")

import frame_mock as mock
test_module = __import__("sqlite_db")
import framework_db

def dummy_use(arg_1):
    _ = arg_1

def dummy_use_many(*many_args):
    for arg_item in many_args:
        dummy_use(arg_item)


DB_NAME = "sql_db"
DB_PATH = "test_sql.db"

class SQLite_TestCase(unittest.TestCase):

    def setUp(self):


        pass

    def tearDown(self):
        # restore mocked objects when tests are done
        for item in mock.list_mocked_method:
            item.restore()
            mock.list_mocked_method.remove(item)
        if os.path.isfile(DB_PATH):

            os.remove(DB_PATH)

    def test__init__set_default(self):
        print "test__init__set_default"

        s_db = test_module.SQLiteDB(db_table_struct=None)
        self.assertEquals(s_db.db_name, "")
        self.assertEquals(s_db.db_path, os.getcwd() + os.sep)
        self.assertEquals(s_db.column, 0)
        self.assertEquals(s_db.row, 0)
        self.assertEquals(s_db.items, ())
        self.assertEquals(s_db.keys, ())
        self.assertEquals(s_db.sql_query_create, "")

    def test__init__(self):
        print "test__init__"

        s_db = test_module.SQLiteDB(DB_NAME, DB_PATH)
        self.assertEquals(s_db.db_name, DB_NAME)
        self.assertEquals(s_db.db_path, os.getcwd() + os.sep + DB_PATH)
        self.assertEquals(s_db.column, 3)
        self.assertEquals(s_db.row, 3)
        self.assertEquals(s_db.items, ('field_name', 'description', 'id'))
        self.assertEquals(s_db.keys, ('field_name', 'id'))
        self.assertNotEquals(s_db.sql_query_create, "")

    def test_create(self):
        print "test_create"

        s_db = test_module.SQLiteDB(DB_NAME, DB_PATH)
        rc, rm, data = s_db.create_table()
        self.assertEquals(rc, 0)
        self.assertEquals(rm, "")
        self.assertEquals(data, ())


    def test_check_structure(self):
        print "test_check_structure"

        s_db = test_module.SQLiteDB(DB_NAME, DB_PATH)
        rc, rm, data = s_db.create_table()
        self.assertEquals(rc, 0)
        self.assertEquals(rm, "")
        self.assertEquals(data, ())

        rc, rm = s_db.check_structure()
        self.assertEquals(rc, 0)
        self.assertEquals(rm, "")

    def test_add_record(self):
        print "test_add_record"

        s_db = test_module.SQLiteDB(DB_NAME, DB_PATH)
        rc, rm, data = s_db.create_table()
        self.assertEquals(rc, 0)
        self.assertEquals(rm, "")
        self.assertEquals(data, ())

        records = [
            ("task_1", "simple task 1", 1),
            ("task_1", "simple task 1", 2),
            ("task_2", "simple task 2", 1),
            ("task_2", "simple task 2", 2)
        ]

        rc, rm = s_db.add_record(records[0])
        self.assertEquals(rc, 0)
        self.assertEquals(rm, "")
        rc, rm, data = s_db.read_all()
        self.assertEquals([records[0]], data)

        rc, rm = s_db.add_record(records[1])
        self.assertEquals(rc, 0)
        self.assertEquals(rm, "")
        rc, rm, data = s_db.read_all()
        self.assertEquals(records[0:2], data)

    def test_add_record_to_much_values(self):
        print "test_add_record"

        s_db = test_module.SQLiteDB(DB_NAME, DB_PATH)
        rc, rm, data = s_db.create_table()
        self.assertEquals(rc, 0)
        self.assertEquals(rm, "")
        self.assertEquals(data, ())

        records = ("task_1", "simple task 1", 1, 2)

        rc, rm = s_db.add_record(records)
        self.assertEquals(rc, framework_db.ERROR_SQL_QUERY_VALUES)
        err_msg = "Wrong amount of values"

        self.assertEquals(rm, err_msg)
        rc, rm, data = s_db.read_all()
        self.assertEquals(data, ())

    def test_add_record_duplicated_items(self):
        print "test_add_record_duplicated_items"

        s_db = test_module.SQLiteDB(DB_NAME, DB_PATH)
        rc, rm, data = s_db.create_table()
        self.assertEquals(rc, 0)
        self.assertEquals(rm, "")
        self.assertEquals(data, ())

        record = ("task_1", "simple task 1", 1)
        rc, rm = s_db.add_record(record)
        self.assertEquals(rc, 0)
        self.assertEquals(rm, "")

        rc, rm = s_db.add_record(record)
        self.assertEquals(rc, framework_db.ERROR_ITEM_NOT_UNIQUE)
        err_msg = 'UNIQUE constraint failed: main_table.field_name, main_table.id'
        self.assertEquals(rm, err_msg)

    def test_get_rows_count(self):
        print "test_get_rows_count"

        s_db = test_module.SQLiteDB(DB_NAME, DB_PATH)
        rc, rm, data = s_db.create_table()
        self.assertEquals(rc, 0)
        self.assertEquals(rm, "")
        self.assertEquals(data, ())
        rc,rm,data =  s_db.get_rows_count()
        self.assertEquals(rc, 0)
        self.assertEquals(data, 0)

        records = [
            ("task_1", "simple task 1", 1),
            ("task_1", "simple task 1", 2),
            ("task_2", "simple task 2", 1),
            ("task_2", "simple task 2", 2)
        ]

        for item in records:
            s_db.add_record(item)

        rc,rm,data =  s_db.get_rows_count()
        self.assertEquals(rc, 0)
        self.assertEquals(data, 4)

        records_2 = [
            ("task_3", "simple task 3", 1),
            ("task_3", "simple task 3", 2),
            ("task_4", "simple task 4", 1),
            ("task_4", "simple task 4", 2),
            ("task_5", "simple task 5", 1),
            ("task_5", "simple task 6", 2)
        ]

        for item in records_2:
            s_db.add_record(item)

        rc,rm,data =  s_db.get_rows_count()
        self.assertEquals(rc, 0)
        self.assertEquals(data, 10)

    def test_delete_record(self):
        print "test_delete_record"

        s_db = test_module.SQLiteDB(DB_NAME, DB_PATH)
        rc, rm, data = s_db.create_table()
        self.assertEquals(rc, 0)
        self.assertEquals(rm, "")
        self.assertEquals(data, ())
        rc,rm,data =  s_db.get_rows_count()
        self.assertEquals(rc, 0)
        self.assertEquals(data, 0)

        records = [
            ("task_1", "simple task 1", 1),
            ("task_1", "simple task 1", 2),
        ]

        for item in records:
            s_db.add_record(item)

        rc, rm, data =  s_db.get_rows_count()
        self.assertEquals(rc, 0)
        self.assertEquals(data, 2)

        #rmv_record = (("task_1", "simple task 1", 1))
        rmv_record = (("task_1", 1))
        rc, rm =  s_db.delete_record(rmv_record)

        rc,rm,data =  s_db.get_rows_count()
        self.assertEquals(rc, 0)
        self.assertEquals(data, 1)

    def test_delete_record_item_not_exist_in_db(self):
        print "test_delete_record_item_not_exist_in_db"

        s_db = test_module.SQLiteDB(DB_NAME, DB_PATH)
        rc, rm, data = s_db.create_table()
        self.assertEquals(rc, 0)
        self.assertEquals(rm, "")
        self.assertEquals(data, ())
        rc,rm,data =  s_db.get_rows_count()
        self.assertEquals(rc, 0)
        self.assertEquals(data, 0)

        records = [
            ("task_1", "simple task 1", 1),
            ("task_1", "simple task 1", 2),
        ]

        for item in records:
            s_db.add_record(item)

        rc, rm, data =  s_db.get_rows_count()
        self.assertEquals(rc, 0)
        self.assertEquals(data, 2)

        rmv_record = (("task_777", 1))
        rc, rm =  s_db.delete_record(rmv_record)

        rc,rm,data =  s_db.get_rows_count()
        self.assertEquals(rc, 0)
        self.assertEquals(data, 2)

    def test_delete_record_too_much_values(self):
        print "test_delete_record_too_much_values"

        s_db = test_module.SQLiteDB(DB_NAME, DB_PATH)
        rc, rm, data = s_db.create_table()
        self.assertEquals(rc, 0)
        self.assertEquals(rm, "")
        self.assertEquals(data, ())
        rc,rm,data =  s_db.get_rows_count()
        self.assertEquals(rc, 0)
        self.assertEquals(data, 0)

        records = [
            ("task_1", "simple task 1", 1),
            ("task_1", "simple task 1", 2),
        ]

        for item in records:
            s_db.add_record(item)

        rc, rm, data =  s_db.get_rows_count()
        self.assertEquals(rc, 0)
        self.assertEquals(data, 2)

        rmv_record = (("task_777", 1, 2))
        rc, rm =  s_db.delete_record(rmv_record)
        self.assertEquals(rc, framework_db.ERROR_SQL_QUERY_VALUES)

        rc,rm,data =  s_db.get_rows_count()
        self.assertEquals(rc, 0)
        self.assertEquals(data, 2)
    #
    # def test_delete_update_record(self):
    #     print "test_update_record"
    #
    #     s_db = test_module.SQLiteDB(DB_NAME, DB_PATH)
    #     rc, rm, data = s_db.create_table()
    #     self.assertEquals(rc, 0)
    #     self.assertEquals(rm, "")
    #     self.assertEquals(data, ())
    #     rc,rm,data =  s_db.get_rows_count()
    #     self.assertEquals(rc, 0)
    #     self.assertEquals(data, 0)
    #
    #     record = ("task_1", "simple task 1", 1)
    #
    #     s_db.add_record(record)
    #
    #     rc, rm, data =  s_db.get_rows_count()
    #     self.assertEquals(rc, 0)
    #     self.assertEquals(data, 1)
    #
    #     record_upd = ("task_1", "simple task 2", 1)
    #     s_db.update_record(record_upd)
    #     rc, rm, data =  s_db.get_rows_count()
    #     self.assertEquals(rc, 0)
    #     self.assertEquals(data, 1)
    #
    #     rc, rm, data =  s_db.read_all()
    #     print "DATA [%s]" %str(data)
    #     self.assertEquals(data[0], record_upd)
    #
    #
    # def test_delete_update_record_too_much_values(self):
    #     print "test_update_record_too_much_values"
    #
    #     s_db = test_module.SQLiteDB(DB_NAME, DB_PATH)
    #     rc, rm, data = s_db.create_table()
    #     self.assertEquals(rc, 0)
    #     self.assertEquals(rm, "")
    #     self.assertEquals(data, ())
    #     rc,rm,data =  s_db.get_rows_count()
    #     self.assertEquals(rc, 0)
    #     self.assertEquals(data, 0)
    #
    #     record = ("task_1", "simple task 1", 1)
    #
    #     s_db.add_record(record)
    #
    #     rc, rm, data =  s_db.get_rows_count()
    #     self.assertEquals(rc, 0)
    #     self.assertEquals(data, 1)
    #
    #     record_upd = ("task_1", "simple task 2", 1)
    #     s_db.add_record(record_upd)
    #     rc, rm, data =  s_db.get_rows_count()
    #     self.assertEquals(rc, 0)
    #     self.assertEquals(data, 1)


    def test_delete_update_record_by_keys(self):
        print "test_delete_update_record_by_keys"

        s_db = test_module.SQLiteDB(DB_NAME, DB_PATH)
        rc, rm, data = s_db.create_table()
        self.assertEquals(rc, 0)
        self.assertEquals(rm, "")
        self.assertEquals(data, ())
        rc,rm,data =  s_db.get_rows_count()
        self.assertEquals(rc, 0)
        self.assertEquals(data, 0)

        record = ("task_1", "simple task 1", 1)

        s_db.add_record(record)
        record_upd = ("task_1", "simple task 2", 1)

        rc, rm, data =  s_db.get_rows_count()
        self.assertEquals(rc, 0)
        self.assertEquals(data, 1)

        rc, rm = s_db.update_record_by_keys(record_upd)
        self.assertEquals(rc, 0)
        rc, rm, data =  s_db.read_all()
        print "DATA [%s]" %str(data)

if __name__ == "__main__":
    unittest.main()




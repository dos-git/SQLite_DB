import os, sys, unittest

sys.path.append("..")
sys.path.append("../../Frame_Mock")
# needed for framework module
sys.path.append("../../DB_Framework")

import frame_mock as mock
test_module = __import__("sqlite_db")

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
        rc, rm = s_db.add_record(records[1])
        print "RC %d" % rc
        print rm


if __name__ == "__main__":
    unittest.main()




import os, sys, sqlite3

sys.path.append("../DB_Framework")

import framework_db as frame_db
from pprint import pprint

class SQLiteDB(frame_db.Database):

    _table_struct = {
        "name"  :   ("main_table",),
        "pk"    :   ("field_name", "id"),
        "items" :   (
                    ( "field_name",     "TEXT",     "NOT NULL", "DEFAULT \"\"" ),
                    ( "description",    "TEXT",     "NOT NULL", "DEFAULT \"\"" ),
                    ( "id",             "INTEGER",  "NOT NULL", "DEFAULT 0" )
        )
    }

    def __init__(self, db_name="", db_path="", db_table_struct=_table_struct):
        super(SQLiteDB,self).__init__(db_name, db_path, db_table_struct)



    def check_structure(self):

        rc = 0; rm = ""

        sql_get_structure = "select sql from sqlite_master where type = 'table' " + \
                            "and name = \'%s\';" % ( self.db_table_name )
        rc, rm, data = self.execute(sql_get_structure)

        db_structure =  str(data[0][0] + ";")
        if db_structure == self.sql_query_create:
            rc = frame_db.NOERROR
        else:
            rc = frame_db.ERROR_TABLE_DIFF
            rm = "Table definition differs - structure [%s]" % sql_get_structure

        return rc, rm


    def parse_error(self, error_code, error_msg):

        rc = 0; rm = ""
        err_msg_table_exist = "table %s already exists" % self.db_table_name

        if error_msg == err_msg_table_exist:
            rc, rm = self.check_structure()
        else:
            rc = error_code
            rm = error_msg

        return rc, rm


    def execute(self, sql_query, values=(), commit=False):

        rc = 0; rm = ""; data = ()
        db_connection = None

        if os.path.exists(self.db_path):
            try:

                db_connection = sqlite3.connect(self.db_path)
                db_connection.text_factory = str
                db_cursor = db_connection.cursor()
                db_cursor.execute(sql_query, values)

                if commit == True:
                    db_connection.commit()
                else:
                    data = db_cursor.fetchall()

                if len(data) == 0:
                    data = ()

            except sqlite3.Error as e:

                err_msg = str(e)
                rc, rm = self.parse_error(err_msg)

            finally:
                if db_connection:
                    db_connection.close()

        else:
            rm =  "Database %s does not exist." % self.db_path
            rc = frame_db.ERROR_TABLE_NOT_EXISTS

        return rc, rm, data


if __name__ == "__main__":

    s = SQLiteDB()
    pass
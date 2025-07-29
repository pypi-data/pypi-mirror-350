"""
An object based interface to the databases using a sqlalchemy engine

-------------- In-line Select Query --------------
To pull data, all you have to do is create a DBHandler object, then run
the select method with your query as a string for the first argument. By
default it will return a list of dictionaries, with each dictionary
corresponding to a row of returned results.

Note: By default the select method limits the list returned to 1000 rows. The "limit"
parameter allows you to adjust this amount, or set it to None to return all rows. However,
data is prefetched into memory, so for large results it's recommended you set the
"prefetch" parameter to "False". This will cause the method to return an iterator
intstead of a list.

-------------- example ----------------------------
from mst.sql import DBHandler

dbh = DBHandler()
strms = dbh.select('SELECT STRM, DESCR from core_stu.ps_term_tbl', limit=4)

for strm in strms:
    print(strm)

---------- Output ---------
{'STRM': '0000', 'DESCR': 'Begin Term - Srvc Indicatr Use'}
{'STRM': '1003', 'DESCR': '1900 Academic Year'}
{'STRM': '1005', 'DESCR': '1901 Academic Year'}
{'STRM': '1009', 'DESCR': '1902 Academic Year'}


-------------- Reading From SQL File --------------
If you set a directory, you can pass the name of an sql file (.sql extension is optional)
in that directory and it will retrieve and run that file. The DBHandler assumes the first
positional argument is a filename if a directory is set, so to use a string as a query
instead, use the "qry" keyword

Note: The DBHandler stores the last query and params used. If no query-string or
filename is passed in to a select method, it will instead reuse the previous one if it
exists.
-------------- example ----------------------------

dbh = DBHandler("sys*", dir='/local/mstapp/queries/')
strms = dbh.select('get_strms', limit=4)
strms2 = dbh.select(qry='SELECT STRM, DESCRSHORT from core_stu.ps_term_tbl', limit=4)

for strm in strms:
    print(strm)

print('-------')

for strm in strms2:
    print(strm)

--------- Output ---------
{'STRM': '0000', 'DESCRSHORT': 'XX0000'}
{'STRM': '1003', 'DESCRSHORT': 'AY1900'}
{'STRM': '1005', 'DESCRSHORT': 'AY1901'}
{'STRM': '1009', 'DESCRSHORT': 'AY1902'}
-------
{'STRM': '0000', 'DESCRSHORT': 'XX0000'}
{'STRM': '1003', 'DESCRSHORT': 'AY1900'}
{'STRM': '1005', 'DESCRSHORT': 'AY1901'}
{'STRM': '1009', 'DESCRSHORT': 'AY1902'}


--------- Selecting Rows As Other Datatypes ---------
The DBHandler returns rows as dictionaries by default, but it can also return them
as other data types:

Method Name      | What is Returned
-----------------|----------------------------
select_dicts()   | list of dictionaries
select_lists()   | list of lists
select_tuples()  | list of tuples
select_vals()    | list, only first item per row is returned
select_sqa_row() | SQLAlchemy's row object

SQLAlchemy's row object behaves like a tuple for the most part. It does however have
it's own unique set of methods available. Documentation on it can be found here:
https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row

Note: all methods starting with "select_" inherit all properties of the main select().

-------------- example ----------------------------
dbh = DBHandler(dir='/local/mstapp/queries/')

strm_tuples = dbh.select_tuples('get_strms', limit=3)
strm_lists = dbh.select_lists('get_strms', limit=3)
strm_vals = dbh.select_vals('get_strms', limit=3)
strm_sqa_rows = dbh.select_sqa_rows('get_strms', limit=3)

for strm_list in (strm_tuples, strm_lists, strm_vals, strm_sqa_rows):

    for strm in strm_list:
        print(f'type: {type(strm)}, value: {strm}')
    print()

--------- Output ---------
type: <class 'tuple'>, value: ('0000', 'XX0000')
type: <class 'tuple'>, value: ('1003', 'AY1900')
type: <class 'tuple'>, value: ('1005', 'AY1901')

type: <class 'list'>, value: ['0000', 'XX0000']
type: <class 'list'>, value: ['1003', 'AY1900']
type: <class 'list'>, value: ['1005', 'AY1901']

type: <class 'str'>, value: 0000
type: <class 'str'>, value: 1003
type: <class 'str'>, value: 1005

type: <class 'sqlalchemy.engine.row.Row'>, value: ('0000', 'XX0000')
type: <class 'sqlalchemy.engine.row.Row'>, value: ('1003', 'AY1900')
type: <class 'sqlalchemy.engine.row.Row'>, value: ('1005', 'AY1901')


--------- Inserting Values into Query ---------
You can securely pass values into queries using the format :value and corresponding
keyword arguments. Alternatively, a dictionary can be passed in using the "params"
argument. With both methods, any parameters passed in that don't appear in the query
will simply be ignored.

-------------- example ----------------------------

dbh = DBHandler()
qry = "SELECT STRM,
              DESCRSHORT,
              ACAD_CAREER
         FROM core_stu.ps_term_tbl
        WHERE ACAD_CAREER = :acad_career
        LIMIT 4"

ugrd_strms = dbh.select(qry=qry, acad_career='UGRD')

parameters = {'acad_career': 'GRAD', 'unused_param': 'foo'}
grad_strms = dbh.select(qry=qry, params=parameters)

for strm in ugrd_strms
    print(strm)
for strm in grad_strms
    print(strm)

--------- Output ---------
{'STRM': '0000', 'DESCRSHORT': 'XX0000', 'ACAD_CAREER': 'UGRD'}
{'STRM': '1003', 'DESCRSHORT': 'AY1900', 'ACAD_CAREER': 'UGRD'}
{'STRM': '1005', 'DESCRSHORT': 'AY1901', 'ACAD_CAREER': 'UGRD'}
{'STRM': '1009', 'DESCRSHORT': 'AY1902', 'ACAD_CAREER': 'UGRD'}
{'STRM': '0000', 'DESCRSHORT': 'XX0000', 'ACAD_CAREER': 'GRAD'}
{'STRM': '1003', 'DESCRSHORT': 'AY1900', 'ACAD_CAREER': 'GRAD'}
{'STRM': '1005', 'DESCRSHORT': 'AY1901', 'ACAD_CAREER': 'GRAD'}
{'STRM': '1009', 'DESCRSHORT': 'AY1902', 'ACAD_CAREER': 'GRAD'}


--------- Inserting a list -----------------------
In addition to inserting scalar values, you can similarly insert sequence values for
use with the IN clause. Just add a list or tuple to the parameters and it will be
automatically converted to the appropriate format for use in the query.

---------------- example ---------------------

dbh = DBHandler()

strms = dbh.select(
    qry="SELECT STRM,
                DESCRSHORT,
                ACAD_CAREER
           FROM core_stu.ps_term_tbl
          WHERE STRM IN :these_strms
            AND ACAD_CAREER = :career",
    these_strms=['5027', '5043', '5127'],
    career='UGRD')

for strm in strms:
    print(strm)

-------------- ouput -------------------------

{'STRM': '5027', 'DESCRSHORT': 'SP2022', 'ACAD_CAREER': 'UGRD'}
{'STRM': '5043', 'DESCRSHORT': 'FS2022', 'ACAD_CAREER': 'UGRD'}
{'STRM': '5127', 'DESCRSHORT': 'SP2023', 'ACAD_CAREER': 'UGRD'}


--------- Select_first_<type>() methods ---------
In instances where only one item need be returned, the select_first_<type> methods
provide a cleaner and less expensive means of doing so. Instead of returning a list of
the given type, it will simply return one instance of the type corresponding to the
first row that would be returned.
------------------ example ------------------------

dbh = DBHandler("sys*", dir='/local/mstapp/queries/')
strm = dbh.select_first_list('get_strms')

print(strm)

--------- Output ---------
['0000', 'Begin Term - Srvc Indicatr Use']


--------- The Execute Method ---------
The select_<type>() methods are intended to be used only for SELECT queries. Therefore
they will roll-back any changes made and raise an exception if given a query returns
nothing. The execute() method is like the select method but without this
guardrail so that it can run insert, update, and delete queries.

WARNING: For queries that return results, this will load the entire result set into
memory, for large result sets use the open_qry() method instead.
------------------ example ------------------------

dbh = DBHandler()
qry = "INSERT INTO groups (groupId, groupName)
            VALUES (:group_id, :group_name)"

dbh.execute(qry, group_id='CHS', group_name='Chess Club')


--------- Returning an Iterator ---------
When working with very large datasets, retrieving and storing all data at once may
use a prohibitive amount of memory. To be more memory efficient we can instead set the
"prefetch" parameter to False and it will return a CursorResult object instead.
The CursorResult is an iterator and as such will retrieve rows one-at-a-time, or in
batches, as they are requested.
CursorResults have some limitations: they are not subscriptable, you cannot use len()
on them, they can only be iterated over once and will close automatically once the
last item is retrieved.
For more information on see the documentation for the CursorResult class below
------------------ example ------------------------

dbh = DBHandler(dir=f'{proj_dir}queries/')
strms = dbh.select_lists('get_strms', prefetch=False)

print(type(strms))

for strm in strms:
    print(strm)

--------- Output ---------
<class 'mst.sql.sql.CursorResult'>
['0000', 'XX0000']
['1003', 'AY1900']
['1005', 'AY1901']
['1009', 'AY1902']
"""

import os
import re
import getpass
import urllib
import csv
import sqlalchemy
from sqlalchemy import create_engine as ce
from mst.core import local_env
from mst.authsrv import AuthSRV


__all__ = ["HOSTS", "DBHandler", "CursorResult"]

HOSTS = {
    "sysd": "sysdb-dev.srv.mst.edu",
    "syst": "sysdb-test.srv.mst.edu",
    "sysp": "sysdb.srv.mst.edu",
}


def convert(row, return_type):
    if return_type == "dict":
        return row._asdict()
    if return_type == "tuple":
        return tuple([val for val in row])  # SQLAlchemy's _tuple() method actually does nothing
    if return_type == "list":
        return [val for val in row]
    if return_type == "val":
        return row[0]
    return row


class DBHandler:
    """An object based interface to the databases using a sqlalchemy engine. Designed
        to streamline and extend sqlalchemy's functionality when using traditional
        sql instead of the ORM.

    Args:
        host (str, optional): Name of the host database being connected to. Used to derive
            uri if a uri argument is not passed. replaces a trailing asterisk, if it
            exists, with a letter denoting the environment.
        uri (str, optional): The uri used to setup the connection engine, overrides
            host/user/database/password if passed.
        user (str, optional): The username used when connecting to the database, will
            also be used as database name if none is provided.
        database (str, optional): Name of database being connected to. If not passed will
            instead attempt to use the "user" argument.
        password (str, optional): Password to use when connecting to database, if not
            passed will search authsrv for a "mysql" instance to use instead.
        dir (str, optional): Path to the directory that will be searched when
            looking up sql files. If set to None the DBHandler will assume the first
            positional argument is a query string instead of a file name. Existence of directory is
            checked, but only at method runtime, not object initialization.
        write_dir (str, optional): Path to the directory files will be written to if select_csv()
            is used. The argument write_dir can also be provided to the the select_csv() method
            itself, in which case it will override, but not replace, the value set here. Like with
            dir argument, existence is checked when running select_csv(), not upon initialization.
        limit (str, optional): Sets a default upper limit to the number of returned rows. If set to
            None, queries that return data will return all rows. The limit argument can also be
            passed into specific select methods, in which case it will override, but not replace,
            the value set here. In the previous version this value was always 1000 by default.
        ssl_required (bool, optional) Default is 'False'. If 'ssl_required' is passed with 'True', ssl will be required.
            If 'ssl_required' is passed with 'False' it will be left to the database server to
            determine if ssl is use.  Documentation for seems to imply that there is no method of
            explicately preventing sqlachemy from using ssl.  If the database "prefers" and ssl
            it will be attempted.  If that fails, and the server does not require ssl, the an insecrure
            connection will be attempted.
        ssl_verify_cert (bool, optional) Default is 'False'. If 'True' it will require verification
            of the database servers certificate before creating an encrypted connection. If this
            fails, the connection should fail.
        ssl_ca (str, optional) This is the absolute path to an ssl Certificate Authority.
        **kwargs: All additional keyword arguments will be passed through to SQLAlchemy's
            ce function.
    """

    def __init__(
        self,
        host="sys*",
        uri=None,
        user=None,
        database=None,
        password=None,
        dir=None,
        write_dir=None,
        limit=None,
        ssl_required=False,
        ssl_verify_cert=False,
        ssl_ca=None,
        **kwargs,
    ):
        self.env = local_env()
        self.last_qry = None
        self.last_params = {}
        self.dir = dir
        self.write_dir = write_dir
        self.limit = limit
        self.ssl_req = ssl_required
        self.ssl_verify = ssl_verify_cert
        self.ssl_ca = ssl_ca

        global HOSTS
        if uri is None:
            target_host = None

            if host in HOSTS:
                target_host = HOSTS[host]
            elif match := re.search("^(.*)\*$", host):
                suffix = "d"
                suffixes = {"dev": "d", "test": "t", "prod": "p"}

                if self.env in suffixes:
                    suffix = suffixes[self.env]

                envhost = f"{match.group(1)}{suffix}"
                target_host = HOSTS.get(envhost, None)

            # re.match automatically pins to the front of the string
            elif match := re.match("(.*)mst.edu$", host):
                target_host = host
            else:
                raise ValueError(f"Target Host '{host}' is invalid")

            if not user:
                user = getpass.getuser()
            if not database:
                database = user
            if not password:
                password = AuthSRV().fetch(user=user, instance="mysql")
            password = urllib.parse.quote(password)
            uri = f"mysql+pymysql://{user}:{password}@{target_host}/{database}"

        connect_args = {}
        if self.ssl_req:
            connect_args["ssl"] = {}
            connect_args["ssl"]["verify_cert"] = False
            if self.ssl_verify:
                connect_args["ssl"]["verify_cert"] = self.ssl_verify
            if self.ssl_ca is not None:
                connect_args["ssl"]["ssl_ca"] = self.ssl_ca

        self.db = ce(
            uri,
            connect_args=connect_args,
            pool_recycle=1800,
            pool_pre_ping=True,
            **kwargs,
        )

    def execute(
        self,
        file=None,
        params=None,
        qry=None,
        force_return=False,
        return_type="id",
        **kwargs,
    ):
        """Runs a query with the passed in parameters (if any). Intended for queries that
            do not return rows.

        Args:
            file (str, optional): filename of a .sql file
            params (dict, optional): name/value pairs for each bound parameter
            qry (str, optional): literal query to be used in place of a file name
            **kwargs: Arbitrary keyword arguments, will be used as bound parameters if
                params argument is absent

        Note1:
            Every bound parameter indicated in the string must correspond to a dictionary item in
            params or **kwargs, although dictionary items not corresponding to any bound parameter
            in string will just be ignored.
        Note2:
            In a previous version, self.last_qry and self.last_params were used by default when no
            qry or params values were available, but this caused issues when the bindparams()
            method of sqlalchemy was used (like when passing in lists) so it has been removed. If
            you have a query failing due to lack of qry or params arguments, this may be why.

        Returns:
            sqlalchemy.engine.CursorResult: only if the qry returns rows and the
                force_return argument is set to True.
        """

        if qry is None:
            if file is None:
                raise ValueError("No file or query string provided")

            elif self.dir is None:
                qry = file

            else:
                if not os.path.isdir(self.dir):
                    raise NotADirectoryError(f"'{self.dir}' is not a valid directory")

                if not re.search("\.sql$", file):
                    file += ".sql"

                with open(f"{self.dir}{file}", "r") as f:
                    qry = f.read()

        if params is None:
            params = kwargs

        self.last_qry = qry
        self.last_params = params

        text_clause = sqlalchemy.text(qry)

        for key, val in params.items():
            if isinstance(val, list):
                text_clause = text_clause.bindparams(sqlalchemy.bindparam(key, expanding=True))

        with self.db.begin() as conn:
            results = conn.execute(text_clause, params)
        if force_return:
            if not results.returns_rows and results.lastrowid and return_type == "id":
                return results.lastrowid
            return results

    def select(
        self,
        file=None,
        params=None,
        qry=None,
        return_type="dict",
        prefetch=True,
        limit="inherit",
        **kwargs,
    ):
        """Runs a select query with the passed in parameters (if any). The main select
            method, all others are special cases of it. It wraps around the execute
            method adding additional functionality only relevent for queries that return
            rows.

        Args:
            file (str, optional): filename of a .sql file, if directory is None will
                instead be treated as the query itself.
            params (dict, optional): name/value pairs for each bound parameter
            qry (str, optional): literal query to be used in place of a file name, only
                needed if a directory has been set, but you still want to use a string.
            return_type (str, optional): Tells the method what type of object to return.
            prefetch (str, optional): Determines whether the method will return a list
                preloaded with all rows, or a CursorResult object which will return rows
                individually. See CursorResult documentation for breakdown of reasons to
                choose one or the other.
            limit (int, optional): Puts an upper limit to the number of returned rows. Overrides but
                does not replace value (if set) at object initialization. A value of None will
                return all rows. In the previous version this value defaulted to 1000.
            **kwargs: Arbitrary keyword arguments, will be used as bound parameters if
                params argument is absent

        Returns:
            list: A list of dictionaries with column names as keys
        """

        if return_type and return_type[-1] == "s":
            return_type = return_type[:-1]

        valid_return_types = (
            "dict",
            "tuple",
            "list",
            "sqa_row",
            "val",
            "first_row",
            "cursor",
        )
        if not return_type in valid_return_types:
            raise ValueError(
                f"Unrecognized return type: '{return_type}'\n\
                               valid return types: {valid_return_types}"
            )

        cursor = self.execute(file, params, qry, force_return=True, **kwargs)

        if return_type == "cursor":
            return cursor

        if return_type == "first_row":
            return convert(cursor.first(), return_type)

        if limit == "inherit":
            limit = self.limit

        if prefetch:
            return_list = []

            if limit is None:
                limit = cursor.rowcount

            for n in range(limit):
                next_row = cursor.fetchone()
                if next_row is None:
                    break
                return_list.append(convert(next_row, return_type))
            return return_list

        return CursorResult(cursor=cursor, qry=qry, params=params, return_type=return_type, limit=limit)

    def select_dicts(self, *args, return_type=None, **kwargs):
        """Runs a select query with the passed in parameters (if any).

        Args: See select() docstring

        Returns:
            list: A list of dictionaries with column names as keys
        """
        return self.select(*args, return_type="dict", **kwargs)

    def select_first_dict(self, *args, **kwargs):
        """Runs a select query with the passed in parameters (if any).

        Args: See select() docstring

        Returns:
            dict: A dictionary with column names as keys if query returns one or more rows
            None: If the query returns zero rows
        """
        first_row = self.select(*args, return_type="first_row", **kwargs)
        if first_row is None:
            return None
        return first_row._asdict()

    def select_tuples(self, *args, **kwargs):
        """Runs a select query with the passed in parameters (if any).

        Args: See select() docstring

        Returns:
            list: A list of tuples corresponding to returned rows
        """
        return self.select(*args, return_type="tuple", **kwargs)

    def select_first_tuple(self, *args, **kwargs):
        """Runs a select query with the passed in parameters (if any) and returns
            the first row as a tuple.

        Args: See select() docstring

        Returns:
            tuple: The first returned row as a tuple if query returns one or more rows
            None: If the query returns zero rows
        """
        first_row = self.select(*args, return_type="first_row", **kwargs)
        if first_row is None:
            return None
        return tuple([val for val in first_row])

    def select_lists(self, *args, **kwargs):
        """Runs a select query with the passed in parameters (if any).

        Args: See select() docstring

        Returns:
            list: A list of lists corresponding to returned rows
        """
        return self.select(*args, return_type="list", **kwargs)

    def select_first_list(self, *args, **kwargs):
        """Runs a select query with the passed in parameters (if any) and returns
            the first row as a list.

        Args: See select() docstring

        Returns:
            list: The first returned row as a list if query returns one or more rows
            None: If the query returns zero rows
        """
        first_row = self.select(*args, return_type="first_row", **kwargs)
        if first_row is None:
            return None
        return [val for val in first_row]

    def select_sqa_rows(self, *args, **kwargs):
        """Runs a select query with the passed in parameters (if any).

        Args: See select() docstring

        Returns:
            list: sqlalchemy.engine.row objects which behave similarly named tuples.
                Information and available methods can be found in the SQLAlchemy documentation:
                https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row
        """
        return self.select(*args, return_type="sqa_row", **kwargs)

    def select_first_sqa_row(self, *args, return_type=None, **kwargs):
        """Runs a select query with the passed in parameters (if any) and returns the
            first row as an sqlalchemy.engine.row object.

        Args: See select() docstring

        Returns:
            if query returns one or more rows:
                sqlalchemy.engine.row object:
                Information and available methods can be found in the SQLAlchemy documentation:
                https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Row
            if query returns zero rows:
                None: this matches the behavior of sqlalchemy's cursorresult.first() method
        """
        return self.select(*args, return_type="first_row", **kwargs)

    def select_vals(self, *args, return_type=None, **kwargs):
        """Runs a select query with the passed in parameters (if any).

        Args: See select() docstring

        Returns:
            list: A list containing the first item of each row returned
            None: If the query returns zero rows or the first row is empty
        """
        return self.select(*args, return_type="val", **kwargs)

    def select_first_val(self, *args, return_type=None, **kwargs):
        """Runs a select query with the passed in parameters (if any).

        Args: See select() docstring

        Returns:
            The first item of the first row returned if query returns anything
        """
        first_row = self.select(*args, return_type="first_row", **kwargs)
        if first_row is None:
            return None
        if len(first_row) == 0:
            return None
        return first_row[0]

    def select_columns(self, *args, **kwargs):
        """Returns the column names of the results that would be returned by the query

        Args: See select() docstring

        Returns:
            list: A list of strings
        """
        raw_cr = self.select(*args, return_type="cursor", **kwargs)
        columns = [key for key in raw_cr.keys()]
        return columns

    def select_csv(self, *args, file_name="untitled", write_dir=None, **kwargs):
        """Writes a csv file based on data returned by query, overwriting any existing csv
        existing in the same location

        Args:
            Inherits all select() args
            file_name (str, optional): name of the csv file to be written
            write_dir (str, optional): the folder to write the csv file, defaults to the
            dbhandler's write_dir if one is set, otherwise defaults to the current directory

        Returns:


        """
        if write_dir:
            if not os.path.isdir(write_dir):
                raise NotADirectoryError(f"'{write_dir}' is not a valid directory")
        else:
            if self.write_dir is None:
                write_dir = ""
            elif not os.path.isdir(self.write_dir):
                raise NotADirectoryError(f"'{self.write_dir}' is not a valid directory")
            else:
                write_dir = self.write_dir

        cols = self.select_columns(*args, **kwargs)
        rows = self.select_lists(*args, **kwargs)
        file_path = f"{write_dir}/{file_name.split('.')[0]}.csv"
        with open(file_path, "w") as file:

            csv_writer = csv.writer(file)
            csv_writer.writerow(cols)
            for row in rows:
                csv_writer.writerow(row)

        return file_path

    def rowcount(self, *args, **kwargs):
        """Shows how many rows the select query would return

        Args: See select() docstring

        Returns:
            int: query result length
        """
        return self.select(*args, return_type="cursor", **kwargs).rowcount

    def open_qry(self, *args, prefetch=None, **kwargs):
        """Returns the CursorResult for a select query.

        Note: The CursorResult is only closed when the last row is returned or the
        close_qry() method is called.

        Args: See select() docstring

        Returns:
            An sqlalchemy.CursorResult object. The list of methods available for
                cursorResult objects can be found in SQLAlchemy documentation:
                https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.CursorResult
        """
        return self.select(*args, prefetch=False, **kwargs)


class CursorResult:
    """An object based interface to the database using a sqlalchemy engine. Rows are returned
        one-at-a-time or in batches of specified size as a list. Elements can accessed via
        for-loop, the next() function or the built-in .next_<type>() methods. Returned by
        all DBHandler select methods if prefetch argument is set to False, and by the
        open_qry() method by default.

        Advantages:
            - Saves memory by not preloading all results into an array
            - May have better performance if there is a lot of database-side, per-element
                calculation
        Disadvantages:
            - Results are not: searchable, subscriptable, sortable, or mutable
            - Only accesses each element once as it iterates through them
            - May have worse performance when churning through large resultsets

    Args:
        cursor (Type[sqlalchemy.engine.CursorResult]): The SQLAlchemy object that
            this class is wrapping around. Returned by DBHandler.select() if return type is
            is set to "cursor".
        qry (str): The query that was used to generate the cursor
        params (dict): The parameters (if any) used to generate the cursor
        return_type (str): The default object type each row will be returned as
        limit (int, optional): The max number of rows to return before raising StopIteration
    """

    def __init__(self, cursor, qry, params, return_type, limit=None):
        self.cursor = cursor
        self.qry = qry
        self.params = params
        self.return_type = return_type
        self.limit = limit
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.count += 1
        if self.limit is not None:
            if self.count > self.limit:
                raise StopIteration

        next_row = self.cursor.fetchone()

        if not next_row:
            raise StopIteration
        return convert(next_row, self.return_type)

    def next(self, return_type=None, batch_size=1):
        """Fetches and returns the next row

        Args:
            return_type (str, optional): Specifies what object type to return, will
                default to whatever self.return_type is set as.
            batch_size (int, optional): If set to anything (positive) other than 1,
                instead of returning the next row will return a list of the next n rows

        Returns:
            Whatever return_type specifies, unless batch_size is not 1, in which case it
            will return a list of whatever return_type specifies
        """
        if return_type is None:
            return_type = self.return_type

        if batch_size == 1:
            next_row = self.cursor.fetchone()
            if next_row is None:
                return None
            return convert(next_row, return_type)

        next_list = self.cursor.fetchmany(batch_size)
        return [convert(row, return_type) for row in next_list]

    def next_dict(self, batch_size=1):
        """Fetches and returns the next row

        Args:
            batch_size (int, optional): If set to anything (positive) other than 1,
                instead of returning the next row will return a list of the next
                "batch_size" rows

        Returns:
            A dictionary, or a list of "batch_size" dictionaries
        """
        return self.next(return_type="dict", batch_size=batch_size)

    def next_tuple(self, batch_size=1):
        """Fetches and returns the next row

        Args:
            batch_size (int, optional): If set to anything (positive) other than 1,
                instead of returning the next row will return a list of the next
                "batch_size" rows

        Returns:
            A tuple, or a list of "batch_size" tuples
        """
        return self.next(return_type="tuple", batch_size=batch_size)

    def next_list(self, batch_size=1):
        """Fetches and returns the next row

        Args:
            batch_size (int, optional): If set to anything (positive) other than 1,
                instead of returning the next row will return a list of the next
                "batch_size" rows

        Returns:
            A list, or a list of "batch_size" lists
        """
        return self.next(return_type="list", batch_size=batch_size)

    def next_sqa_row(self, batch_size=1):
        """Fetches and returns the next row

        Args:
            batch_size (int, optional): If set to anything (positive) other than 1,
                instead of returning the next row will return a list of the next
                "batch_size" rows

        Returns:
            An sqlalchemy row object, or a list of "batch_size" sqlalchemy row objects
        """
        return self.next(return_type="sqa_row", batch_size=batch_size)

    def columns(self):
        """Returns the column names of the rows that the query returns"""
        return [key for key in self.cursor.keys()]

    def close(self):
        """Closes the CursorResult. Note CursorResult closes automatically when last
        row is returned"""
        self.cursor.close()

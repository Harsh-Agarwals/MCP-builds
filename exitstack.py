from contextlib import ExitStack
import sqlite3

# ExitStack is used to manage multiple context managers in a single `with` statement, expecially if we don't have count of resources. 

# It works by pushing context managers into stack and then popping them off in reverse order during exit. 

# Creating context manager using class
class DataConn:
    def __init__(self, db_name) -> None:
        self.db_name = db_name

    def __enter__(self):
        """
        Open the Database connection
        This method runs when the with block is entered. It's responsible for setting up the resource (like opening a file or acquiring a lock).
        """
        self.conn = sqlite3.connect(database=self.db_name, check_same_thread=False,)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close the connection
        This method runs when the with block is exited. It's responsible for cleaning up the resource (like closing a file or releasing a lock).
        """
        self.conn.close()
        if exc_type:
            raise

class MyContextManager:
    def __enter__(self):
        print("Entering the context.")
        return self  # this is returned and accessible inside `with`
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exiting the context.")
        if exc_type:
            print(f"An error occurred: {exc_val}")
        return True  # if `True`, suppresses the exception

# Another method to build context manager
from contextlib import contextmanager

@contextmanager
def my_context():
    print("Entering the context cm.")
    yield # code inside `with` block runs here
    print("Exiting the context cm.")

# Example resources
class FileResource:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        print(f"Opening file {self.filename}")
        return open(self.filename, 'r')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Closing file {self.filename}")
        return False  # Don't suppress exceptions

# Using ExitStack to open and close multiple files dynamically
files_to_open = ['data/f2.txt', 'data/f3.txt', 'data/f6.txt']

if __name__=="__main__":
    db = "test.db"
    # with DataConn(db) as conn:
    #     cursor = conn.cursor()

    # with MyContextManager() as cm:
    #     print("Inside the context.")

    # with my_context():
    #     print("Inside the context cm.")

    with ExitStack() as stack:
        a=stack.enter_context(DataConn("test2.db"))
        b=stack.enter_context(MyContextManager())
        c=stack.enter_context(my_context())

        print("Inside the context of DB, MyContextManager, and my_context")
        files_list = [stack.enter_context(FileResource(file)) for file in files_to_open]
        for f in files_list:
            f.read()
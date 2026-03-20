import sqlite3

# A context manager is a way to manage resources (like opening and closing files, acquiring and releasing locks, etc.) automatically when a block of code is executed. It ensures that no matter what happens within that block (even if there’s an error), the resource is properly cleaned up afterward.

# with open("file.txt", "r") as file:
#     content = file.read()
#     print(content)

# What’s happening here?

# Context manager: The open() function returns a context manager.
# with statement: It ensures that once the block of code is done, the file is automatically closed.
# Automatic cleanup: Even if an error occurs inside the block, the file.close() is still guaranteed to be called.

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
    print("Entering the context.")
    yield # code inside `with` block runs here
    print("Exiting the context.")

if __name__=="__main__":
    db = "test.db"
    with DataConn(db) as conn:
        cursor = conn.cursor()

    with MyContextManager() as cm:
        print("Inside the context.")

    with my_context():
        print("Inside the context.")
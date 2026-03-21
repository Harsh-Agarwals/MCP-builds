import asyncio
from contextlib import AsyncExitStack

# The AsyncExitStack is part of the contextlib module, and it is similar to ExitStack, but designed to handle asynchronous context managers. It's used when you want to manage multiple asynchronous context managers that require async with blocks.

# It ensures that multiple asynchronous context managers are properly entered and exited, even if the number of them isn't known upfront. It helps manage resources like database connections, network connections, and other async I/O operations that need to be cleaned up in reverse order.

class AsyncNetworkConnection:
    def __init__(self, connection) -> None:
        self.connection = connection
        
    async def __aenter__(self):
        print(f"Connecting {self.connection}")
        await asyncio.sleep(2)
        return f"Connected {self.connection}"

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(f"Exiting {self.connection}")
        await asyncio.sleep(1)
        print(f"Exited {self.connection}")
        if exc_type:
            print(f"Error {exc_val}")

class AsyncDatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name

    async def __aenter__(self):
        print(f"Connecting to database: {self.db_name}")
        # Simulating async DB connection setup
        await asyncio.sleep(1)
        return self.db_name

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(f"Closing database: {self.db_name}")
        await asyncio.sleep(1)
        if exc_type:
            print(f"Error occurred: {exc_val}")
        return True  # Suppress exceptions

async def async_task():
    async with AsyncExitStack() as stack:
        db_conn = await stack.enter_async_context(AsyncDatabaseConnection("MyDatabase"))

        # Simulating an operation that could raise an error
        print(f"Working with {db_conn}...")
        raise ValueError("Something went wrong!")

        # Code below won't be executed due to exception
        print("This line won't run.")

async def main():
    async with AsyncExitStack() as stack:
        a=await stack.enter_async_context(AsyncNetworkConnection("A"))
        b=await stack.enter_async_context(AsyncNetworkConnection("B"))
        c=await stack.enter_async_context(AsyncNetworkConnection("C"))

        print(f"Three connections: {a}, {b}, {c}")

if __name__=="__main__":
    asyncio.run(main())
    print("ONTO NEW TASK")
    asyncio.run(async_task())

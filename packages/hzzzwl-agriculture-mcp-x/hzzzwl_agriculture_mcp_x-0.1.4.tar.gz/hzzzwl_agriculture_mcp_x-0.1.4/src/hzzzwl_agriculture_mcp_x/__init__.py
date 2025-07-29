import asyncio

#from .server import main
from .server import main as async_main

__version__ = "0.1.4"

def main():
    """Main entry point for the package."""
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
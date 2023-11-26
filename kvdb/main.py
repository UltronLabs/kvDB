import sys
import argparse
from kvdb.interface import KVDB
from kvdb.constants import (
    BAD_KEY,
    DB_CONNECTION_ERROR,
    UNEXPECTED_ERROR,
    OK,
)


def main():
    parser = argparse.ArgumentParser(description="A simple key-value database CLI.")
    parser.add_argument("dbname", help="The name of the database.")
    parser.add_argument(
        "verb", choices=["get", "set", "delete"], help="The operation to perform."
    )
    parser.add_argument("key", help="The key to operate on.")
    parser.add_argument(
        "value",
        nargs="?",
        default=None,
        help='The value to set (only required for "set" operation).',
    )

    args = parser.parse_args()

    try:
        db = KVDB.connect(args.dbname)
    except Exception as e:
        print(f"Database connection error: {e}", file=sys.stderr)
        return DB_CONNECTION_ERROR

    try:
        if args.verb == "get":
            result = db[args.key]
            print(f"Retrieved value: {result}")
        elif args.verb == "set":
            db[args.key] = args.value
            if args.value is not None:
                db.commit()
        elif args.verb == "delete":
            del db[args.key]
            db.commit()
    except KeyError:
        print("Key not found", file=sys.stderr)
        return BAD_KEY
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return UNEXPECTED_ERROR

    return OK


if __name__ == "__main__":
    main()

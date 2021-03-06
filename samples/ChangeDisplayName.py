#!/usr/bin/env python3

# Set the current users display name.
# Args: host:port username password display_name
# Error Codes:
# 2 - Could not find the server.
# 3 - Bad URL Format.
# 4 - Bad username/password.
# 11 - Serverside Error

import asyncio
import sys

sys.path.append('../')

import samples_common

from matrix_client.api import MatrixRequestError, MatrixHttpLibError
from matrix_client.client import MatrixBaseClient

host, username, password = samples_common.get_user_details(sys.argv)

client = MatrixBaseClient(host)


async def main():
    try:
        await client.login_with_password(username, password)
    except MatrixRequestError as e:
        print(e)
        if e.code == 403:
            print("Bad username or password.")
            sys.exit(4)
        else:
            print("Check your server details are correct.")
            sys.exit(2)
    except MatrixHttpLibError as e:
        print(e)
        sys.exit(3)

    user = client.get_user(client.user_id)

    if len(sys.argv) < 5:
        print("Current Display Name: %s" % await user.get_display_name())

        displayname = input("New Display Name: ")
    else:
        displayname = sys.argv[4]

    try:
        await user.set_display_name(displayname)
    except MatrixRequestError as e:
        print(e)
        sys.exit(11)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

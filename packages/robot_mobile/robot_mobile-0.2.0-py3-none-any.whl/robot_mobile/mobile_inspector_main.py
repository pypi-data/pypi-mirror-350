import asyncio
import sys

from robot_mobile.mobile_inspector import InspectServer

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("参数错误", file=sys.stderr)
    else:
        inspect_server = InspectServer(int(sys.argv[1]), sys.argv[2])
        asyncio.run(inspect_server.start())

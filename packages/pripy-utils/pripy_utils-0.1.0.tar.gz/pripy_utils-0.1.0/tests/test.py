
import os
import sys
# 添加项目根目录到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.pyutils import log
from src.pyutils import timeCost

@timeCost
def test():
    log("test")

test()
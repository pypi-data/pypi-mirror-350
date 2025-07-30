import inspect
import logging
import os

_isConfigLog = False


@staticmethod
def initLog():
    # logging.getLogger("myLogger")
    console_handler = logging.StreamHandler()
    log_handler = logging.FileHandler("app.log", mode="w+", encoding="utf-8")
    console_handler.setLevel(logging.DEBUG)
    log_handler.setLevel(logging.DEBUG)
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s-%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d_%H:%M:%S",
        handlers=[console_handler, log_handler],
    )
    return


@staticmethod
def loge(msg):
    log(msg, logging.ERROR)


@staticmethod
def logd(msg):
    log(msg, logging.DEBUG)


@staticmethod
def logi(msg):
    log(msg, logging.INFO)


count = 0


@staticmethod
def log(msg, level=logging.INFO, frameIndex=1):
    global _isConfigLog
    if not _isConfigLog:
        initLog()
        _isConfigLog = True
    # 增加log文件大小限制，如果超过50MB，重新创建一个新的log文件
    # maxBytes = 1024 * 1024 * 50  # 50MB
    if count == 0:
        log_file = "app.log"
    else:
        log_file = f"app{count+1}.log"
    if os.path.exists(log_file):
        file_size = os.path.getsize(log_file)
        if file_size > 1024 * 1024 * 50:
            # 重新创建一个新的log文件
            # 移除旧的log_handler hanlder
            logging.getLogger().removeHandler(log_handler)
            log_handler = logging.FileHandler(log_file, mode="w+", encoding="utf-8")
            log_handler.setLevel(logging.DEBUG)
            logging.getLogger().addHandler(log_handler)
        else:
            # 继续使用旧的log_handler
            # size = file_size / (1024 * 1024)
            # print(f"当前log文件大小：{size:.2f}MB，继续使用旧的log_handler")
            pass

    # stacks = traceback.format_stack()

    statcks2 = inspect.stack()
    frame = statcks2.pop(frameIndex)
    name = frame.filename.split("\\").pop(-1)
    r = 0
    try:
        r = name.rindex("/")
        r += 1
    except Exception:
        try:
            r = name.rindex("\\")
            r += 1
        except Exception:
            pass

    callStack = f" <===[{name[r:]}${frame.function}:({frame.lineno})]"

    # print(callStack)
    # frame.filename
    # stc = stacks[-2:]
    # for s in stc:
    #     print("=="+s)
    if isinstance(msg, Exception) or isinstance(msg, str) == False:
        # if isinstance(msg, Exception):
        # log(f"-------{msg}")
        msg = repr(msg)

    callStack = f"{msg:<80} {callStack}"

    match level:
        case logging.DEBUG:
            logging.debug(callStack)
        case logging.INFO:
            logging.info(callStack)
        case logging.ERROR:
            logging.error(callStack)
        case logging.WARNING:
            logging.warn(callStack)
    return


def test():
    log("test")
    logd("test")
    loge("test")


if __name__ == "__main__":
    test()

import time
import traceback

from . import log

def timeCost(func):
    def wrapper(*args, **argss):
        try:
            start = time.time()
            result = func(*args, **argss)
            end = time.time()
            duration = end - start
            #把秒转化为时分秒格式：
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            seconds = duration % 60
            duration_str = f"{int(hours)}:{int(minutes)}:{int(seconds)}"            
            log(f"{func.__name__} cost: {duration_str}= {duration} seconds")
        except Exception as e:
            traceback.print_exc()
            log(e)
            if hasattr(argss, "callback"):
                if argss["callback"] != None:
                    argss["callback"]("opso !")
            return "opso !"
        return result

    return wrapper
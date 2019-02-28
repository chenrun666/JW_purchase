from bin.MyException import StopException

try:
    raise StopException("stop")
except StopException as e:
    print(e.msg)

except Exception as e:
    print(e)

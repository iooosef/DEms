import sys
import platform
import eel


@eel.expose  # Expose function to JavaScript
def say_hello_py(x):
    """Print message from JavaScript on app initialization, then call a JS function."""
    print("Hello from %s" % x)
    eel.say_hello_js("Python through Eel {from within say_hello_py()}!")

eel.init('web')
eel.start('index.html', mode='edge')

# """
# 原理是：
# 测试环境：
# 1、测试环境设置启动页面为vue的测试服务端口，然后将app设为None，
# 2、将端口和vue的public/index.html 中的eel.js绑定/
# 生产环境：
# 和正常的一样使用
# """
# def start_eel(develop):
#     """Start Eel with either production or development configuration."""
#     directory = 'web'
#     app = 'edge'
#     page = 'index.html'
#     eel_kwargs = dict(
#         mode=app,
#         port=0,
#         size=(1280, 800))
#     eel.init(directory)
#     say_hello_py("Python World!")
#     eel.say_hello_js(
#         "Python World!"
#     )  # Call a JavaScript function (must be after `eel.init()`)
#     try:
#         eel.start(page, **eel_kwargs)
#     except EnvironmentError:
#         # If Chrome isn't found, fallback to Microsoft Edge on Win10 or greater
#         if sys.platform in ["win32", "win64"] and int(platform.release()) >= 10:
#             eel.start(page, mode="edge", **eel_kwargs)
#         else:
#             raise


if __name__ == "__main__":
    print("Opening python...")
    # start_eel(False)

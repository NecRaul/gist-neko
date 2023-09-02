import os
import platform

def set_environment_variable(key, value):
    os_name = platform.system()
    os.environ[key] = value
    # Save the environment variable permanently
    if (os_name == "Windows"):
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS) as reg_key:
            winreg.SetValueEx(reg_key, key, 0, winreg.REG_SZ, value)
    else:
        print("It doesn't work on non-Windows systems unfortunately.\nI'm working on a fix.")
        # with open("~/.bashrc", "a") as file:
        #     file.write(f"\nexport {key}={value}")
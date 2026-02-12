try:
    from importlib.metadata import version as get_version
except ImportError:
    import pkg_resources
    def get_version(package_name):
        return pkg_resources.get_distribution(package_name).version

import os
from pypodo.properties import TODO_RC_FILE
from pypodo.config import get_user_config_directory_pypodo, todofilefromconfig, todobackupfolderfromconfig

def version():
    """
    entry point for --version
    """
    print("version pypodo            : " + get_version("pypodo"))
    print("location of todo file     : " + todofilefromconfig())
    print("location of config file   : " + os.path.join(get_user_config_directory_pypodo(), TODO_RC_FILE))
    print("location of backup folder : " + todobackupfolderfromconfig())
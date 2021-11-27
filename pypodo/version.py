import pkg_resources
import os
from pypodo.properties import TODO_RC_FILE
from pypodo.config import get_user_config_directory_pypodo, todofilefromconfig, todobackupfolderfromconfig

def version():
    """
    entry point for --version
    """
    print("version pypodo            : "
        + pkg_resources.get_distribution("pypodo").version
    )
    print("location of todo file     : " + todofilefromconfig())
    print("location of config file   : " + os.path.join(get_user_config_directory_pypodo(), TODO_RC_FILE))
    print("location of backup folder : " + todobackupfolderfromconfig())
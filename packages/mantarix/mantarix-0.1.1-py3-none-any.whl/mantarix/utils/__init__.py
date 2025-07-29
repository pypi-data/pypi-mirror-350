from mantarix.utils.browser import open_in_browser
from mantarix.utils.classproperty import classproperty
from mantarix.utils.deprecated import deprecated
from mantarix.utils.files import (
    copy_tree,
    get_current_script_dir,
    is_within_directory,
    safe_tar_extractall,
    which,
)
from mantarix.utils.hashing import calculate_file_hash, sha1
from mantarix.utils.network import get_free_tcp_port, get_local_ip
from mantarix.utils.once import Once
from mantarix.utils.platform_utils import (
    get_arch,
    get_bool_env_var,
    get_platform,
    is_android,
    is_asyncio,
    is_embedded,
    is_ios,
    is_linux,
    is_linux_server,
    is_macos,
    is_mobile,
    is_pyodide,
    is_windows,
)
from mantarix.utils.slugify import slugify
from mantarix.utils.strings import random_string
from mantarix.utils.vector import Vector

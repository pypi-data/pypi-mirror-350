from .main import main as nbconvert
from .new import new_main
from .hugo_fix import fix_main, to_dir_main
from .run import run
import os

submodule = os.environ["submodule"]

if submodule == "hugo_nbconvert":
    nbconvert()
elif submodule == "hugo_new":
    new_main()
elif submodule == "hugo_fix":
    fix_main()
elif submodule == "hugo_run":
    run()
elif submodule == "hugo_todir":
    to_dir_main()

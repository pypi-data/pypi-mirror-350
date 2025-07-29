#  For Krita to load your script both of these must put be in the pykrita subdirectory of your Krita resources folder


import os
import logging
from pathlib import Path
import shutil
from plugget.actions._utils import clash_import_name


# todo merge dupe code with krita pip and blender addon

# maybe if env var PLUGGET_KRITA_PLUGIN_PATH is set, use that path?

if os.name == 'posix':  # Linux or macOS
    home = os.path.expanduser("~")
    path = os.path.join(home, ".local", "share", "krita")  # linux
    # todo mac should be ~/Library/Application Support/Krita/
elif os.name == 'nt':  # Windows
    path = os.path.join(os.environ['APPDATA'], 'krita')
    # todo add support for windows store
    #  If you installed Krita in the Windows Store, your custom resources will be in a location like:
    #  %LOCALAPPDATA%\Packages\49800Krita_RANDOM STRING\LocalCacheRoamingkrita

    # todo what about portable windows version?
    #  allow user to manually set a target folder
else:
    raise OSError("Unsupported operating system")

# pip install a submodule to the path

path = Path(path) / "pykrita"


def install(package: "plugget.data.Package", force=False, enable=True, **kwargs) -> bool:  # todo , force=False, enable=True):
    # If the “force” parameter is True, the add-on will be reinstalled, even if it has not been previously removed.

    # if a repo has plugin in root. we get the repo files content
    # if the repo has plugin in subdir, that file lives in repo_paths

    addon_paths: list[Path] = package.get_content()  # get paths to plugin files in cloned repo
    # copy addons to local addons dir
    local_script_dir = path
    local_addons_dir = Path(local_script_dir)
    # if force:
    #     from plugget.utils import rmdir
    #     rmdir(new_plugin_path)
    # shutil.move(str(plugin_path), str(new_plugin_path.parent), )  # copy plugin_path to local_addons_dir
    # todo filter repo paths
    print(f"copy files to {local_addons_dir}")
    for addon_path in addon_paths:
        print(addon_path)

        if clash_import_name(addon_path.name):
            continue

        # new_addon_path.mkdir(parents=True, exist_ok=True)
        shutil.move(str(addon_path), str(local_addons_dir))
        # todo use copy instead of move

        # todo clean up empty folders

        # check if plugin folder was copied, by checking if any files are in new_plugin_path
        # new_addon_path = local_addons_dir / addon_path.name
        # if not any(new_addon_path.iterdir()):
        #     logging.warning(f"Failed to install plugin {addon_path.name}")
        #     return False

    package.installed_paths |= {local_addons_dir / x.name for x in addon_paths}  # todo might want a dict later


def uninstall(package: "plugget.data.Package", **kwargs):
    """uninstall plugin by name"""
    # todo make plugin name an action kwarg

    for p in package.installed_paths:
        p = Path(p)
        print("remove", p)
        # delete all paths,. p can be folder or file. force delete and children
        if p.is_dir():
            shutil.rmtree(p, ignore_errors=True)
        else:
            p.unlink(missing_ok=True)


    print("PLUGGET uninstalled plugin_name ", package.package_name)

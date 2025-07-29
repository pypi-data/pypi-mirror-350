from WtFileUtils.vromfs.VROMFs import VROMFs
from WtFileUtils.FileSystem.FSDirectory import FSDirectory
from WtFileUtils.FileSystem.FileSystemQuery import MassFileSystemQuery
import os
import re

def fetch_normal_vromfs_paths(wt_install_path):
    """
    fetchs all the normally used vromfs paths from the wt install
    :param wt_install_path:
    :return: list[str]
    """
    files = os.listdir(wt_install_path + "/cache")
    input_path = None
    for file in files:
        if file.startswith("binary"):
            input_path = os.path.join(wt_install_path, "cache", file)
            break

    if input_path is None:
        print("unable to find binary path")
    good_ui = []
    ui_path = os.path.join(wt_install_path, "ui")
    for f in os.listdir(ui_path):
        if f.endswith("vromfs.bin"):
            good_ui.append(os.path.join(ui_path, f))
    raw_vromfs_files = [os.path.join(input_path, x) for x in os.listdir(input_path)]
    raw_vromfs_files.extend(good_ui)
    return raw_vromfs_files


def dump_all(wt_install_path, dump_path, silent=False):
    """
    Dumps all the files from the binary folder (which is the most up to date VROMFS) to dump_path.
    AKA this emulates what most vromfs dumpers do
    MY BLK UNPACKER IS NOT THE FASTEST, SO THIS IS RATHER SLOW (can take a few minutes)
    """
    files = os.listdir(wt_install_path + "/cache")
    input_path = None
    for file in files:
        if file.startswith("binary"):
            input_path = os.path.join(wt_install_path, "cache", file)
            break
    if input_path is None:
        print("unable to find binary path")
    raw_vromfs_files = os.listdir(input_path)
    d = FSDirectory("Base", None)
    for file in raw_vromfs_files:
        temp_path = os.path.join(input_path, file)
        VROMFs(temp_path).get_directory(directory=d)
        print(f"Loaded {temp_path}")
    if not os.path.exists(dump_path):
        os.mkdir(dump_path)
    if os.path.isdir(dump_path):
        d.dump_files(dump_path, skip=True)
    else:
        print("bad file path")
    print("completed")

"""

"""
def lookup(wt_install_path, data_to_lookup, filename_include=None, filename_exclude=None,path_include=None,path_exclude=None):
    """
    A function to look up files that contain certain data
    you can apply filters to the searched files based on name and path
    for all searches, if you supply a compiled re (re.Pattern) object, it will do a re match instead of a (if x in y) match
    all files are bytes, not strings, so you must use b""
    probably not finished
    :param wt_install_path: the warthunder installation path
    :param data_to_lookup: what value(s) to look up in the file
    :param filename_include:
    :param filename_exclude:
    :param path_include:
    :param path_exclude:
    :return:
    """
    if not isinstance(data_to_lookup, list):
        data_to_lookup = [data_to_lookup]
    files = os.listdir(wt_install_path + "/cache")
    input_path = None
    for file in files:
        if file.startswith("binary"):
            input_path = os.path.join(wt_install_path, "cache", file)
            break
    if input_path is None:
        print("unable to find binary path")
    raw_vromfs_files = os.listdir(input_path)
    d = FSDirectory("Base", None)
    for file in raw_vromfs_files:
        temp_path = os.path.join(input_path, file)
        VROMFs(temp_path).get_directory(directory=d)
        print(f"Loaded {temp_path}")

    m = MassFileSystemQuery(path_include, path_exclude, filename_include, filename_exclude)
    for f in d.search_for_files(m):
        f_data = f[1].get_data()
        for m in data_to_lookup:
            if isinstance(m, bytes):
                if m in f_data:
                    print('/'.join(f[0]))
                    break
            if isinstance(m, re.Pattern):
                if m.match(f_data) is not None:
                    print('/'.join(f[0]))
    # print(type(re.compile(".*"))), <class 're.Pattern'>

def dump_individual_vromfs(wt_install_path, out_dir, to_include):
    """
    dumps each vromfs to a named folder in the output dir
    each folder is the named after its vromfs parent
    :param wt_install_path: the install path of war thunder
    :param out_dir: the output folder
    :param to_include: the names of the vromfs to dump, if you put an "*", then it dumps all the vromfs
    :return: None
    """
    raw_vromfs_files = fetch_normal_vromfs_paths(wt_install_path)

    raw_vromfs_files = [r"D:\SteamLibrary\steamapps\common\War Thunder\cache\binary.2.45.1\regional.vromfs.bin"]
    for file in raw_vromfs_files:
        d = VROMFs(file).get_directory()
        print(f"Loaded {file}")
        file_name = file.split("\\")[-1]
        dump_path = os.path.join(out_dir, file_name)
        if not os.path.exists(dump_path):
            os.mkdir(dump_path)
        d.dump_files(dump_path, skip=True)
        print(f"Dumped vromfs {file} to {dump_path}")



if __name__ == '__main__':
    path = r"D:\SteamLibrary\steamapps\common\War Thunder"
    dump_all(path, "dump", silent=True)
    # dump_individual_vromfs(path, "dump2", "")
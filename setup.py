import os
import pathlib
import shutil

PATH_LIST = []
IGNORE_FILES = ["setup.py"]
IGNORE_EXTENTIONS = ["jpg", "png", "jpeg", "mo"]
NAME_TO_REPLACE = [
    "django_easystart",
    "django-easystart",
    "easystart",
    "Easystart",
    "EasyStart",
]


def ignore_pyc_files(dirname, filenames):
    ignore = [name for name in filenames if name.endswith(".pyc")]
    ignore += [
        "__pycache__",
        "node_modules",
        "env",
        "media",
        "db.sqlite3",
        "package-lock.json",
        "translation-stats.json",
        "webpack-stats.json",
        "setup.py",
        ".git",
        "static/dist",
    ]
    return ignore


def get_list_of_files(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + get_list_of_files(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


def copy_project(easystart_path, project_path):
    try:
        # if path already exists, remove it before copying with copytree()
        if os.path.exists(project_path):
            shutil.rmtree(project_path)
        shutil.copytree(easystart_path, project_path, ignore=ignore_pyc_files)

    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == e.errno.ENOTDIR:
            shutil.copy(easystart_path, project_path)
        else:
            print("Directory not copied. Error: %s" % e)


def change_name_project_in_files(files, new_name, old_name="easystart"):
    # Replace old_name for new_name
    for path_file in files:
        if os.path.isdir(path_file):
            continue

        file = path_file.split("/")[-1]
        ext = file.split(".")[-1]
        if file in IGNORE_FILES or ext in IGNORE_EXTENTIONS:
            continue

        replace_name(path_file, new_name, old_name)


def replace_name(file_path, new_name, old_name):
    try:
        with open(f"{file_path}", "r") as f:
            filedata = f.read()

        filedata = filedata.replace(old_name, new_name)
        with open(f"{file_path}", "w") as f:
            filedata = f.write(filedata)
    except UnicodeDecodeError:
        pass


if __name__ == "__main__":
    project_name = "easystart"
    description = "Django Easystart"
    domain = "easystart.com"

    description_in = input("Description (Default: Django Easystart): ")
    if description_in:
        description = description_in
        project_name = description_in.replace(" ", "_").lower()
        domain = f"{project_name}.com"

    name = input(f"Slug (Default: {project_name}): ")
    if name:
        project_name = name
        domain = f"{project_name}.com"

    domain_in = input(f"Domain (Default: {domain}): ")
    if domain_in:
        domain = domain_in

    project_dir = project_name

    new_project_path = os.getcwd()
    easystart_path = pathlib.Path(__file__).parent.resolve()

    # Create New Project
    print("Trying create new project...")
    copy_project(easystart_path, f"{new_project_path}/{project_dir}")

    # Rename Project
    os.rename(
        f"{new_project_path}/{project_dir}/easystart",
        f"{new_project_path}/{project_dir}/{project_name}",
    )

    # Change easystart name from <project_name> in files
    files = get_list_of_files(f"{new_project_path}/{project_dir}")
    for old_name in NAME_TO_REPLACE:
        change_name_project_in_files(files, project_name, old_name)

    # Change description
    change_name_project_in_files(files, description, f"Django {project_name}")
    # Change domain
    change_name_project_in_files(files, domain, f"{project_name}.com")
    change_name_project_in_files(files, domain, f"{project_name}.io")

    print("Finish to create project")

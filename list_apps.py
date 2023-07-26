import os

# paths = os.getenv("PATH", "/usr/bin").split(":")
paths = ["/usr/bin"]

# os.listdir raises an error is something is not a path so I'm creating
# a small function that only executes it if 'p' is a directory
def listdir(p):
    return os.listdir(p) if os.path.isdir(p) else [ ]

# Checks if the path specified by x[0] and x[1] is a file
def isfile(path, file):
    fullpath = os.path.join(path, file)
    return True if os.path.isfile(fullpath) else False

# Checks if the path specified by x[0] and x[1] is executable
def isExecutable(path, file):
    fullpath = os.path.join(path, file)
    return True if os.access(fullpath, os.X_OK) else False

if __name__ == "__main__":
    apps = []
    for path in paths:
        files = filter(lambda x: isfile(path, x), listdir(path))
        executables = filter(lambda x: isExecutable(path, x), files)
        executables_apps = filter(lambda x: x.startswith("app-"), executables)
        apps.extend(executables_apps)

    print(apps)

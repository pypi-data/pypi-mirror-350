# Wrapper for running python scripts inside a predefined virtual environment
#
# Run with "--help" for usage instructions

import os
import sys
import shutil
import random
import pkgutil
import pathlib
import hashlib
import platform
import importlib
import subprocess



################################################################################
# Globals
################################################################################

DEBUG_MODE = os.getenv("WRAPVENV_DEBUG", "") != ""

DEFAULT_REQUERIMENTS_FROZEN_FILE = f"requirements-frozen-{platform.system()}.txt"

if platform.system() == "Linux":
    venv_dir_base = os.path.join(pathlib.Path.home(),       ".cache", "wrapvenv")
else:  # Windows
    venv_dir_base = os.path.join(os.environ["USERPROFILE"], ".wrapvenv_cache")

CURRENT_PYTHON_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}"


################################################################################
# Auxiliary functions
################################################################################

def debug_print(x):
    if DEBUG_MODE:
        print(f"[{os.path.basename(sys.argv[0])}] {x}")


def get_venv_context(venv_dir, force_recreation=False):
    """
    Return a "virtual environment context" which can later be used in
    "run_in_venv()" to run arbitrary python scripts inside that context

    @param venv_dir: Folder where the virtual environment can be found. If the
        folder does not exist a new virtual environment will be created there.

    @param force_recreation: If set to true, the virtual environment will always
        be created from scratch, even if the "venv_dir" folder already existed
        (in that case it will be deleted first)

    @return a "virtual environment context" that needs to be given later as an
        argument to "run_in_venv()" in order for it to execute python scripts
        inside the virtual environment

    Example:

      venv_ctx = get_venv_context(".my_venv", True)
      run_in_venv(venv_ctx, "my_script.py arg1 arg2")
    """

    # Delete "venv_dir" if requested
    #
    if force_recreation and os.path.exists(venv_dir):
        print(f"Deleting previously existing virtual environment folder: {venv_dir}...")
        shutil.rmtree(venv_dir)

    # Run "pip -m venv" (or an equivalent command) to (re)generate the venv
    # folder
    #
    if not os.path.exists(venv_dir):

        if shutil.which("python3"):
            python_cmd = "python3"
        else:
            python_cmd = "python"

        if sys.version_info < (3,12,0):
            module_exists = pkgutil.find_loader
        else:
            module_exists = importlib.util.find_spec

        if module_exists("venv") and module_exists("ensurepip"):
            cmd = f"{python_cmd} -m venv {venv_dir}"
        elif module_exists("virtualenv"):
            cmd = f"{python_cmd} -m virtualenv -p {python_cmd} {venv_dir}"
        else:
            print("FATAL: Cannot find a method to install a virtual environment on this machine")
            sys.exit(-1)

        debug_print(f"Creating new virtual environment folder: {venv_dir}...")
        debug_print(f"Running command outside virtual environment: {cmd}")
        subprocess.run(cmd, check=True, shell=True)


    # Return a tuple containing the path to the python EXE and and extended
    # environment where the PATH variable points inside the virtual environment
    #
    if platform.system() == "Linux":
        bin_subdir = "bin"
        if os.path.exists(os.path.join(venv_dir, bin_subdir, "python3")):
            python_exe = os.path.join(venv_dir, bin_subdir, "python3")
        else:
            python_exe = os.path.join(venv_dir, bin_subdir, "python")

    else:  # Windows
        bin_subdir = "Scripts"
        if os.path.exists(os.path.join(venv_dir, bin_subdir, "python3.exe")):
            python_exe = os.path.join(venv_dir, bin_subdir, "python3.exe")
        else:
            python_exe = os.path.join(venv_dir, bin_subdir, "python.exe")

    return (
        python_exe,                                                                      # Exe
        dict(
            os.environ,
            PYTHONIOENCODING="utf-8",
            PATH=os.path.join(venv_dir, bin_subdir) + os.pathsep + os.getenv("PATH","")  # Environ
        )
    )


def run_in_venv(venv_ctx, cmd, blocking=True):
    """
    Run a python script inside a virtual environment.

    @param venv_ctx: object obtained in a previous call to "get_venv_context()"

    @param cmd: string containing the path/name of a python script plus its
        arguments (if any).
        This string will be run with python interpreter from the provided
        virtual environment. Note that, because of this, the string does not
        really need to start with the path to a python script, and could instead
        be something like "-m pip install ..."

    @param blocking: if "True", the function will only return after cmd has
        finished executing. Otherwise, it will return immediately.

    @return:
        - When blocking == True, return a tuple where the first element is the
          return code and the second one a string with the output of the
          executed command
        - When blocking == False, return a tuple of two elements, "poll" and
          "stdout", meant to be used like this by the calling function:

              while True:
                  realtime_output = stdout.readline()

                  retcode = poll()

                  if realtime_output == '' and retcode is not None:
                      break

                  if realtime_output:
                      print(realtime_output.strip(), flush=True)

      Example:

        venv_ctx = get_venv_context(".my_venv", True)
        run_in_venv(venv_ctx, "my_script.py arg1 arg2")
    """

    debug_print(f"Running command inside virtual environment: {venv_ctx[0]} {cmd}")

    if blocking:
        try:
            return (0,
                    subprocess.check_output(
                        f"{venv_ctx[0]} {cmd}",
                        shell=True,
                        env=venv_ctx[1],
                        stderr=subprocess.STDOUT).decode(
                            "utf-8",
                            errors="replace").replace("\r", ""))

        except subprocess.CalledProcessError as e:
            return (e.returncode, e.stdout.decode(
                            "utf-8",
                            errors="replace").replace("\r", ""))

    else:
        p = subprocess.Popen(
            f"{venv_ctx[0]} {cmd}",
            env      = venv_ctx[1],
            shell    = True,
            encoding = "utf-8",
            errors   = "replace",
            stdout   = subprocess.PIPE,
            stderr   = subprocess.STDOUT
        )

        return (p.poll, p.stdout)


def is_text_file(file_path):
    """
    Check if a file is a text file by making sure it can be decoded as UTF-8

    @param file_path: Path of the file to check

    @return True if the file seems to be a text file. False otherwise.

    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read()
        return True  # No exception, valid UTF-8

    except UnicodeDecodeError:
        return False  # Exception, not valid UTF-8


def recursive_replace(directory, old_str, new_str):
    """
    Recursively search for text files in directory and replace text.

    @param directory: Path containing the files where the replace will take
        place

    @param old_str: String to replace.

    @param new_str: Replacement string.

    @return Nothing
    """

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)

            if is_text_file(file_path):

                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                if old_str in content:
                    print(f"Updating file {file_path}...")

                    content = content.replace(old_str, new_str)

                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(content)



################################################################################
# main() Execution starts here.
################################################################################

if "--help" in sys.argv:

    help_txt = f"""
Usage:

    wrapvenv [--clean]  [--reqs <requirements-frozen.txt>] [arg1, [arg2, ...]]

        This runs 'python arg1 arg2 ...' inside a virtual environment which
        contains all the modules listed in <requirements-frozen.txt>

        <requirements-frozen.txt> is a file listing all the python modules (and
        their versions) you want to have inside the virtual environment. You can
        generate such a file calling this script with '--freeze' (read the
        corresponding documentation below to understand how).

        If option '--reqs <requirements-frozen.txt>' is *not* present, then a
        file called "{DEFAULT_REQUERIMENTS_FROZEN_FILE}" in the current folder
        will be used instead (in case it exists)

        Some ways in which you can use it:

            1. wrapvenv my_script.py 103 203
            2. wrapvenv -m webbrowser -n 'https://www.python.org'
            3. wrapvenv

        (The last one will simply open a python interpreter inside the virtual
        environment)

        The virtual environment folder will be created inside here:

          {venv_dir_base}

        The folder itself will be named after a hash of the frozen requirements
        file. This makes it possible not to have to re-install the virtual
        environment each time as long as the frozen requirements do not change.

        If the '--clean' flag is provided the virtual environment will be
        re-created no matter what.

    wrapvenv --freeze <requirements.txt>

        This creates <requirements-frozen.txt>. It works like this:

            1. You first need to specify which python modules you want in your
               virtual environment, and save them to a file, like this:

                   termcolor
                   pexpect
                   pandas
                   pyserial

            2. Then call 'wrapvenv --freeze'. Example:

                   $ wrapvenv --freeze my_requirements.txt

            3. The script will create a new virtual environment and install each
               of the listed modules. Then it will generate a new file called
               like the input file plus an appended suffix
               ('frozen-{platform.system()}'):

                   my_requirements-frozen-{platform.system()}.txt

               This new file is like the input file *but*:

                   - Each module contains a version number (the latest one
                     available at that moment)
                   - There might be extra modules listed (those that come as
                     dependencies of the ones in the original list)

    wrapvenv --help

        Print this help message

Example:

    # Create virtual environment

    $ echo "termcolor"  > my_requirements.txt
    $ echo "pexpect"   >> my_requirements.txt
    $ echo "pandas"    >> my_requirements.txt
    $ echo "pyserial"  >> my_requirements.txt
    $ wrapvenv --freeze my_requirements.txt


    # Run script inside the just created virtual environment (the first time it
    # will take some time because it needs to create the virtual environment)

    $ wrapvenv --reqs my_requirements-frozen-{platform.system()}.txt my_python_script.py


    # Run script inside the just created virtual environment again (the second
    # time will be very fast because it will reuse the already installed virtual
    # environment)

    $ wrapvenv --reqs my_requirements-frozen-{platform.system()}.txt my_python_script.py

Notes:

    A. This script uses "pip install ..." under the hood. If you want to pass
       extra options to pip you can do so by setting environment variable
       "WRAPVENV_EXTRA_OPTS" before calling this script. This is useful, for
       example, to deal with certificate problems when running behind a
       corporate network that man-in-the-middles traffic. Example:

           $ export WRAPVENV_EXTRA_OPTS="--trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org"

    B. The argument to "--reqs" is expected to be a list of frozen requirements
       (ie. a list which you have generated calling "--freeze" which contains a
       complete list of packages and the exact desired version), *however*,
       despite not being recommended, for convenience, you can also use a non
       frozen list directly such as in this example:

           $ echo "termcolor"  > my_requirements.txt
           $ echo "pexpect"   >> my_requirements.txt
           $ echo "pandas"    >> my_requirements.txt
           $ echo "pyserial"  >> my_requirements.txt
           $ wrapvenv --reqs my_requirements.txt my_python_script.py

       The main drawbacks of doing this are:

           - The latest version of each package will be installed, which changes
             depending on when you run the script for the first time.

           - The next time you run it, because the hash of the txt file has not
             changed, dependencies will not be updated (ie. they will remain
             "frozen" at some arbitrary point in the past, more specifically
             when you first executed it)

           - Dependencies of packages are also installed (this does *not* happen
             when you use a real "frozen" file), which is also a source of
             noise.

       ...however it can be useful as a quick an dirty way of running a script
       with some dependencies in one step.

"""

    print(help_txt)

    sys.exit(0)


if "--freeze" in sys.argv:
    # Use the non-frozen reqs file to process it and generate a new frozen reqs
    # file.

    print("Working. Please wait...")

    nonfrozen_reqs = sys.argv[sys.argv.index("--freeze")+1]

    if nonfrozen_reqs[-4:] != ".txt":
        print("FATAL: The requirements file must end in .txt!")
        sys.exit(-1)

    frozen_reqs =                        \
        nonfrozen_reqs[:-4]            + \
        f"-frozen-{platform.system()}" + \
        nonfrozen_reqs[-4:]

    # Create the virtual environment folder structure (deleting the previous one
    # in case it existed)
    #
    venv_tmp = os.path.join(venv_dir_base,
                            f"__TMP__{random.randint(100000, 999999)}")
    venv_ctx = get_venv_context(venv_tmp, True)

    # Install all requirements
    #
    debug_print("Installing updated requirements inside virtual environment...")

    ret, output = run_in_venv(venv_ctx,  "-m pip install --quiet --upgrade pip")

    if ret != 0:
        print("FATAL: Could not upgrade pip. Aborting...")
        debug_print(f"DEBUG: {output}")
        sys.exit(-1)

    ret, _ = run_in_venv(venv_ctx, f"-m pip install --quiet -r {nonfrozen_reqs}")

    if ret != 0:
        print(f"FATAL: Could not install requirements. Make sure file '{nonfrozen_reqs}' contains valid references. Aborting...")
        sys.exit(-1)

    open(os.path.join(venv_tmp, "_updated_mark_"),
         "w", encoding="utf-8").write("YES")

    # Obtain the pip frozen manifest and update the frozen requirements file
    #
    _, output = run_in_venv(venv_ctx, "-m pip freeze")

    open(frozen_reqs, "w", encoding="utf-8").write(output)

    # Obtain the hash of the new manifest file and use its value to rename the
    # folder.
    #
    new_hash = hashlib.md5((open(frozen_reqs, "r").read() +
                            CURRENT_PYTHON_VERSION).encode("utf8")).hexdigest()[0:8]

    new_folder = os.path.join(venv_dir_base, new_hash)

    if os.path.exists(new_folder):
        shutil.rmtree(new_folder)

    recursive_replace(venv_tmp,
                      os.path.basename(venv_tmp),
                      os.path.basename(new_folder))

    os.rename(venv_tmp, new_folder)

    end_txt = f"""

    Done!

      - A new virtual environment has been created here: '{new_folder}'

            {new_folder}

      - Its frozen requirements have been saved to '{frozen_reqs}'
    """

    print(end_txt)

    sys.exit(0)

else:
    # This is the typical use case: just use the already frozen reqs file that
    # is known to work.

    if "--reqs" in sys.argv:
        frozen_reqs = sys.argv[sys.argv.index("--reqs")+1]
    else:
        frozen_reqs = DEFAULT_REQUERIMENTS_FROZEN_FILE

    if frozen_reqs[-4:] != ".txt":
        print("FATAL: The requirements file must end in .txt!")
        sys.exit(-1)

    if not os.path.exists(frozen_reqs):
        print(f"FATAL: Requirements file ({frozen_reqs}) not found!")
        sys.exit(-1)

    # (Re)create the virtual environment folder structure if at least one of
    # these conditions happens:
    #
    #   - The virtual environment folder does not exist
    #   - The user requests to recreate it ("--clean")
    #
    venv_dir = os.path.join(
        venv_dir_base,
        hashlib.md5((open(frozen_reqs, "r").read() +
                     CURRENT_PYTHON_VERSION).encode("utf8")).hexdigest()[0:8]
    )

    venv_ctx = get_venv_context(venv_dir, "--clean" in sys.argv)

    # Install all requirements
    #
    if not os.path.exists(os.path.join(venv_dir, "_updated_mark_")):
        debug_print("Installing frozen requirements inside virtual environment...")

        ret, output = run_in_venv(venv_ctx,  "-m pip install --quiet --upgrade pip")
        if ret != 0:
            print("FATAL: Could not upgrade pip. Aborting...")
            debug_print(f"DEBUG: {output}")
            sys.exit(-1)

        install_log = os.path.join(venv_dir, ".install_log.txt")
        extra_opts  = os.getenv("WRAPVENV_EXTRA_OPTS", "")

        if "=" in open(frozen_reqs, "r").read():
            ret, _ = run_in_venv(venv_ctx, f"-m pip install --quiet --no-deps -r {frozen_reqs} --log {install_log} {extra_opts}")
        else:
            # Special case! We are not receiving a "real" frozen file (with all
            # dependencies "frozen" to a specific version) but just a list of
            # python modules to install without version. This is *not* the way
            # wrapvenv is meant to be used... but instead of failing, let's just
            # install the latst version of all packages and its dependencies and
            # call it a day
            #
            ret, _ = run_in_venv(venv_ctx, f"-m pip install --quiet           -r {frozen_reqs} --log {install_log} {extra_opts}")


        if ret != 0:
            print(f"FATAL: Could not install requirements. Make sure file '{frozen_reqs}' contains valid references. Aborting...")
            sys.exit(-1)

        open(os.path.join(venv_dir, "_updated_mark_"), "w", encoding="utf-8").write("YES")

    if "--clean" in sys.argv:
        sys.argv.remove("--clean")

    if "--reqs" in sys.argv:
        sys.argv.remove("--reqs")
        sys.argv.remove(frozen_reqs)

    poll, stdout = run_in_venv(venv_ctx, " ".join(sys.argv[1:]), blocking=False)

    while True:
        try:
            rt_output = stdout.read(1)
        except KeyboardInterrupt:
            rt_output = ""

        retcode   = poll()

        if rt_output == '' and retcode is not None:
            break

        if rt_output:
            try:
                print(rt_output, flush=True, end="")
            except Exception:
                print("--- Line suppressed due to invalid characters ---")

    sys.exit(retcode)

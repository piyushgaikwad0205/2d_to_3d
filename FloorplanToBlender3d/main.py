from subprocess import check_output
from FloorplanToBlenderLib import (
    IO,
    config,
    const,
    execution,
    dialog,
    floorplan,
    stacking,
)  # floorplan to blender lib
import os

"""
Create Blender Project from floorplan
This file contains a simple example implementation of creations of 3d models from
floorplans. You will need blender and an image of a floorplan to make this work.

FloorplanToBlender3d
Copyright (C) 2022 Daniel Westberg
"""


def create_blender_project(data_paths):
    if not os.path.exists("." + target_folder):
        os.makedirs("." + target_folder)

    target_base = target_folder + const.TARGET_NAME
    target_path = target_base + const.BASE_FORMAT
    target_path = (
        IO.get_next_target_base_name(target_base, target_path) + const.BASE_FORMAT
    )

    # Create blender project
    check_output(
        [
            blender_install_path,
            "-noaudio",  # this is a dockerfile ubuntu hax fix
            "--background",
            "--python",
            blender_script_path,
            program_path,  # Send this as parameter to script
            target_path,
        ]
        + data_paths
    )

    outformat = config.get(
        const.SYSTEM_CONFIG_FILE_NAME, "SYSTEM", const.STR_OUT_FORMAT
    ).replace('"', "")
    # Transform .blend project to another format!
    if outformat != ".blend":
        check_output(
            [
                blender_install_path,
                "-noaudio",  # this is a dockerfile ubuntu hax fix
                "--background",
                "--python",
                "./Blender/blender_export_any.py",
                "." + target_path,
                outformat,
                target_base + outformat,
            ]
        )
        print("Object created at:" + program_path + target_base + outformat)

    print("Project created at: " + program_path + target_path)


if __name__ == "__main__":
    """
    Do not change variables in this file but rather in ./config.ini or ./FloorplanToBlenderLib/const.py
    """
    dialog.figlet()
    image_path = ""
    blender_install_path = ""
    data_folder = const.BASE_PATH
    target_folder = const.TARGET_PATH
    blender_install_path = config.get_default_blender_installation_path()
    floorplans = []
    image_paths = []
    program_path = os.path.dirname(os.path.realpath(__file__))
    blender_script_path = const.BLENDER_SCRIPT_PATH
    dialog.init()
    data_paths = list()

    # Detect where/if blender is installed on pc
    auto_blender_install_path = (
        IO.blender_installed()
    )  # TODO: add this to system.config!

    if auto_blender_install_path is not None:
        blender_install_path = auto_blender_install_path

    # Use default blender path
    print(f"Using Blender installation path: {blender_install_path}")

    # Use ConfigFile by default
    var = ""  # Default to ConfigFile
    if var in ["N", "n", "StackingFile", "stacking", "stackingfile"]:
        stacking_def_path = "./Stacking/all_separated_example.txt"
        var = input(f"Enter path to Stacking file : [default = {stacking_def_path}]: ")
        if var:
            stacking_def_path = var
        data_paths = stacking.parse_stacking_file(stacking_def_path)
        print("Using stacking file mode")

    else:
        # Use default config
        config_path = "./Configs/default.ini"
        print(f"Using default config: {config_path}")
        
        floorplans.append(floorplan.new_floorplan(config_path))
        
        # Skip image selection, use defaults
        print("Using default images from config file")

        print("")
        print("Generate datafiles in folder: Data")
        print("")
        print("Clean datafiles")

        # Auto-clean cached data
        print("Clearing cached data...")
        IO.clean_data_folder(data_folder)

        if len(floorplans) > 1:
            data_paths.append(execution.simple_single(f) for f in floorplans)
        else:
            data_paths = [execution.simple_single(floorplans[0])]

    print("")
    print("Creates blender project")
    print("")

    if isinstance(data_paths[0], list):
        for paths in data_paths:
            create_blender_project(paths)
    else:
        create_blender_project(data_paths)

    print("")
    print("Done, Have a nice day!")

    dialog.end_copyright()

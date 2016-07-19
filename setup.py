import cx_Freeze
# Change "App" to the name of your python script
executables = [cx_Freeze.Executable("Megajump.py")]

cx_Freeze.setup(
    name="MegaJump",
    version = "1",
    options={"build_exe": {"packages":["pyglet", "gameFunc", "pygame"]}},
    executables = executables
    )

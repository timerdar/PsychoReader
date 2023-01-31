from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': ['pymorphy2', 'vk_api', 're'], 'excludes': []}

base = 'Win32GUI'

executables = [
    Executable('main.py', base=base, target_name = 'main.exe')
]

setup(name='PsychoReader v0.51',
      version = 'v0.51',
      description = 'PsychoReader for vk pages',
      options = {'build_exe': build_options},
      executables = executables)
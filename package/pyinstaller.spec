# -*- mode: python -*-
import os
from glob import glob


# Change this flag if you want to debug the packaging output
DEBUG_PACKAGING = True


# Get PyQt5 and DLL locations
from inspect import getfile
import PyQt5
pyqt_dir = os.path.dirname(getfile(PyQt5))
pyqt_dlls = os.path.join(pyqt_dir, 'plugins', 'platforms')

# PyInstaller Cipher flag.
block_cipher = None

# Adding all css and images as part of additional resources
if DEBUG_PACKAGING:
  data_files_glob = glob(os.path.join('resources', 'css', '*.css'))
  data_files_glob += glob(os.path.join('resources', 'images', '*.*'))
  data_files_glob += glob(os.path.join('resources', 'fonts', '*.*'))
  data_files_glob += glob(os.path.join('resources', 'pygamezero', '*.*'))
else:
  data_files_glob = glob(os.path.join('mu','resources', 'css', '*.css'))
  data_files_glob += glob(os.path.join('mu', 'resources', 'images', '*.*'))
  data_files_glob += glob(os.path.join('mu', 'resources', 'fonts', '*.*'))
  data_files_glob += glob(os.path.join('mu', 'resources', 'pygamezero', '*.*'))
data_files = []

# Paths are a bit tricky: glob works on cwd (project root), pyinstaller relative
# starts on spec file location, and packed application relative starts on
# project root directory.
if DEBUG_PACKAGING:
    for df in data_files_glob:
        data_files += [(os.path.join('..', df), os.path.join(os.path.dirname(df), '..'))]
else:
    for x in data_files_glob:
        data_files += [(os.path.join('..', x), os.path.dirname(x))]


# No binary files added at the moment, additional DLLs go here
binary_files = []

# General settings
app_name = 'mu'
icon_win = 'package/icons/win_icon.ico'
icon_mac = 'package/icons/mac_icon.icns'

# If UPX is available set the path here
upx_path = False

# Printing useful info to the console
print('Running packaging in Debug mode: %s' % DEBUG_PACKAGING)
print('Spec file resources selected: %s' % data_files)
print('Spec file binaries selected: %s' % binary_files)


a = Analysis(['../run.py'],
             pathex=['../', pyqt_dir],
             binaries=binary_files,
             datas=data_files,
             hiddenimports = ['sip', 'pgzero', 'pygame'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure,
          a.zipped_data,
          cipher=block_cipher)

if DEBUG_PACKAGING:
    exe = EXE(pyz,
              a.scripts,
              exclude_binaries=True,
              name=app_name,
              debug=True,
              strip=False,
              upx=True,
              console=False,
              icon=icon_win)

    coll = COLLECT(exe,
                   a.binaries,
                   a.zipfiles,
                   a.datas,
                   strip=False,
                   upx=True,
                   name=app_name)
else:
    exe = EXE(pyz,
              a.scripts,
              a.binaries,
              a.zipfiles,
              a.datas,
              name=app_name,
              debug=False,
              strip=False,
              upx=upx_path,
              console=False,
              icon=icon_win)

    # The macOS .app bundle can only be done in one-file mode
    app = BUNDLE(exe,
                 name=app_name + '.app',
                 icon=icon_mac,
                 bundle_identifier='mu.codewith.app.editor',
                 info_plist={'NSHighResolutionCapable': 'True'})

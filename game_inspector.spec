# -*- mode: python -*-
from kivy_deps import sdl2, glew, gstreamer
block_cipher = None


a = Analysis(['game_inspector.py'],
             pathex=[''],
             binaries=[],
             datas=[('no_screenshot.png', '.'), ('fps_inspector_sdk\\python\\fps_inspector_sdk\\lib', 'fps_inspector_sdk\\lib'), ('screen_recorder_sdk\\python\\screen_recorder_sdk\\lib', 'screen_recorder_sdk\\lib'), ('game_overlay_sdk\\python\\game_overlay_sdk\\lib', 'game_overlay_sdk\\lib')],
             hiddenimports=['win32timezone'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins + gstreamer.dep_bins)],
          name='game_inspector',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )

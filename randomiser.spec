# -*- mode: python -*-

block_cipher = None


a = Analysis(['randomiser4.py'],
             pathex=['C:\\Users\\rahul\\Documents\\Python\\WAV Randomiser'],
             binaries=[],
             datas=[('pi.gif', 'img')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='WAV Randomiser',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='a.ico')

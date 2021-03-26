# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['icon_2.png', 'proof.py'],
             pathex=['D:\\kjchen\\Documents\\學習資料\\學習課程目錄\\108-1_MCU\\投資學\\Handout\\台指選擇權套利\\autoOptionsArbitrage'],
             binaries=[],
             datas=[],
             hiddenimports=[],
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
          [],
          name='icon_2',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='con=')

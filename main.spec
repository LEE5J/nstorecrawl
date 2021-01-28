# -*- mode: python ; coding: utf-8 -*-


block_cipher = None
added_files = [('nstore.ui','.'),('category_data.csv','.')]

a = Analysis(['main.py'],
             pathex=['C:\\Users\\5j\\PycharmProjects\\\cowboykr_crawlnstore'],
             binaries=[],
             datas=[('./nstore.ui','.'),('./chromedriver.exe', '.'),('./category_data.csv','.')],
             hiddenimports=["tools",
                            "search_engine"
                            ],
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
          name='ver0_9_13',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True)

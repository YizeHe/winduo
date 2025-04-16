import zipapp

# 将项目目录打包为 .pyz 文件
zipapp.create_archive(
    source="simpleGUI",       # 项目目录
    target="simpleGUI.pyz",   # 输出文件名
    main="main:main",          # 入口点
    
)
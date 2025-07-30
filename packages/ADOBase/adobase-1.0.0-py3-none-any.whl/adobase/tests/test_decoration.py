from adobase import ADOFAILevel

# 加载关卡
level = ADOFAILevel.load('main.adofai')

# 获取13号砖块所有装饰物
print('13号砖块所有装饰物:', level.get_tile_decoration(13))

# 添加一个AddDecoration装饰物到14号砖块
level.add_decoration(14, 'AddDecoration', 'default')
print('添加后14号砖块装饰物:', level.get_tile_decoration(14))

# 批量修改所有AddDecoration装饰物的scale
level.batch_edit_decoration('AddDecoration', scale=[200, 200])
print('批量修改后AddDecoration装饰物:', level.batch_get_decoration_info('AddDecoration'))

# 删除14号砖块的第一个AddDecoration装饰物
level.remove_decoration(14, 'AddDecoration', 0)
print('删除后14号砖块装饰物:', level.get_tile_decoration(14))

# 保存结果
level.save('decoration_demo_out.json') 
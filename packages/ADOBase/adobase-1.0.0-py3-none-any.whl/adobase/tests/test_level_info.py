from adobase import ADOFAILevel

# 加载关卡
level = ADOFAILevel.load('main.adofai')

# 获取全部关卡信息
print('全部关卡信息:', level.get_level_info())

# 获取基础信息
print('基础信息:', level.get_level_info('levelbase'))

# 编辑关卡信息
level.edit_level_info(version=16, bpm=150)
print('修改后关卡信息:', level.get_level_info('version', 'bpm'))

# 打印关卡信息
level.print_level_info('artist', 'song')

# 保存结果
level.save('level_info_demo_out.json') 
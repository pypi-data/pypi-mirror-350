from adobase import ADOFAILevel

# 加载关卡
level = ADOFAILevel.load('main.adofai')

# 获取1号砖块所有事件
print('1号砖块所有事件:', level.get_tile_event(1))

# 添加一个MoveTrack事件到2号砖块
level.add_event(2, 'MoveTrack', 'default')
print('添加后2号砖块事件:', level.get_tile_event(2))

# 批量修改所有MoveTrack事件的duration
level.batch_edit_event('MoveTrack', duration=2)
print('批量修改后MoveTrack事件:', level.batch_get_event_info('MoveTrack'))

# 删除2号砖块的第一个MoveTrack事件
level.remove_event(2, 'MoveTrack', 0)
print('删除后2号砖块事件:', level.get_tile_event(2))

# 保存结果
level.save('event_demo_out.json') 
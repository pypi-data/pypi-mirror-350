"""
ADOFAI 关卡参数定义模块
包含关卡文件中所有可用的参数常量和类型定义
"""
from typing import Set, TypedDict, Any

# 所有关卡参数名
LEVEL_PARAM_NAMES = (
    'version', 'artist', 'specialArtistType', 'artistPermission', 'song', 'author',
    'separateCountdownTime', 'previewImage', 'previewIcon', 'previewIconColor',
    'previewSongStart', 'previewSongDuration', 'seizureWarning',
    'levelDesc', 'levelTags', 'artistLinks',
    'speedTrialAim', 'difficulty', 'requiredMods',
    'songFilename', 'bpm', 'volume', 'offset', 'pitch', 'hitsound', 'hitsoundVolume',
    'countdownTicks', 'trackColorType', 'trackColor', 'secondaryTrackColor',
    'trackColorAnimDuration', 'trackColorPulse', 'trackPulseLength', 'trackStyle',
    'trackTexture', 'trackTextureScale', 'trackGlowIntensity', 'trackAnimation',
    'beatsAhead', 'trackDisappearAnimation', 'beatsBehind', 'backgroundColor',
    'showDefaultBGIfNoImage', 'showDefaultBGTile', 'defaultBGTileColor',
    'defaultBGShapeType', 'defaultBGShapeColor', 'bgImage', 'bgImageColor',
    'parallax', 'bgDisplayMode', 'imageSmoothing', 'lockRot', 'loopBG',
    'scalingRatio', 'relativeTo', 'position', 'rotation', 'zoom', 'pulseOnFloor',
    'bgVideo', 'loopVideo', 'vidOffset', 'floorIconOutlines', 'stickToFloors',
    'planetEase', 'planetEaseParts', 'planetEasePartBehavior',
    'defaultTextColor', 'defaultTextShadowColor', 'congratsText', 'perfectText',
    'legacyFlash', 'legacyCamRelativeTo', 'legacySpriteTiles'
)
LEVEL_PARAMS: Set[str] = set(LEVEL_PARAM_NAMES)
LEVEL_BASE = 'levelbase'

class LevelSettingsDict(TypedDict, total=False):
    pass
for name in LEVEL_PARAM_NAMES:
    LevelSettingsDict.__annotations__[name] = Any

def is_valid_param(param: str) -> bool:
    """检查参数是否为有效的ADOFAI参数"""
    return param == LEVEL_BASE or param in LEVEL_PARAMS 
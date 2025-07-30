<div align="center">

# Clovers Divine

_✨ 今日运势和塔罗牌占卜合集 ✨_

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![pypi](https://img.shields.io/pypi/v/clovers_divine.svg)](https://pypi.python.org/pypi/clovers_divine)
[![pypi download](https://img.shields.io/pypi/dm/clovers_divine)](https://pypi.python.org/pypi/clovers_divine)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Github](https://img.shields.io/badge/GitHub-Clovers-00CC33?logo=github)](https://github.com/clovers-project/clovers)
[![license](https://img.shields.io/github/license/clovers-project/clovers-divine.svg)](./LICENSE)

</div>

# 安装

```bash
pip install clovers_divine
```

# 配置

<details>

<summary>在 clovers 配置文件内按需添加下面的配置项</summary>

```toml
[clovers_divine]
# 今日运势用户数据路径
daily_fortune_data = "data/divine/daily_fortune"
# 今日运势背景资源路径
daily_fortune_resorce = "data/divine/daily_fortune/basemap/"
# 今日运势标题字体路径
daily_fortune_title_font = "data/divine/daily_fortune/font/Mamelon.otf"
# 今日运势文本字体路径
daily_fortune_text_font = "data/divine/daily_fortune/font/sakura.ttf"
# 塔罗牌牌面资源路径
tarot_resource = "data/divine/tarot"
# 塔罗牌合并转发开关
tarot_merge_forward = true
```

</details>

# 说明

今日运势和 id 绑定,一天内同一用户不同群的的占卜结果是相同的

`今日运势` 占卜今日运势

`占卜` 启用塔罗牌占卜

`塔罗牌` 抽一张塔罗牌并解读

## 今日运势资源

本插件会遍历 `daily_fortune_resorce` 路径下所有 `.png` `.jpg` `.jpeg` 文件作为插件的今日运势抽签主题

原版主题图片大小为 480\*480，如果需要添加主题图片请注意下面的规则

标题位置中心点是 (140, 99)，标题字号是 45

文本位置中心点是 (140, 297)，文本字号是 25，文本每行 9 字符最高支持 4 行（从右到左竖向排版）

## 塔罗牌资源

本插件会认为 `tarot_resource` 路径下的每个文件夹都是一套主题。

插件会遍历主题路径下所有 `.png` `.jpg` `.jpeg` 文件作为塔罗牌卡面，但建议主题下的文件夹有如下子路径

- MajorArcana 大阿卡纳
- Pentacles 星币
- Swords 宝剑
- Cups 星杯
- Wands 权杖

塔罗牌文件名的规则

当卡片资源为小阿卡纳牌（MinorArcana）时

如果卡片为宫廷牌（Court Cards），那么文件名格式为

`{suit}{point}.{suffix}` 如 `圣杯王后.png`

否则文件名格式为

`{suit}-{point}.{suffix}` 如 `圣杯-01.png`

当卡片资源为大阿卡纳牌（MajorArcana）时

文件名格式为

`{n}-{suit}.{suffix}` 如 `01-魔术师.png`

下面是图片的命名规则，对后缀名没有要求

```bash
└ MyTheme
  ├ Cups
  │ ├ 圣杯-01.png
  │ ├ 圣杯-02.png
  │ ├ ……
  │ └ 圣杯王后.png
  └ MajorArcana
    ├ 0-愚者.png
    ├ 01-魔术师.png
    ├ ……
    └ 21-世界.png
```

在抽牌时插件会随机一个主题，如果主题内没有对应卡片则会用其他主题的对应卡牌补位。

请注意资源内至少要有一套完整的塔罗牌主题。

# 著作权信息

- `copywriting.json` by KafCoppelia (MIT License)
- `tarot.json` by KafCoppelia (MIT License)

**本仓库 divine 路径内的的资源来自以下项目，感谢各位原作者！**

[nonebot_plugin_fortune](https://github.com/MinatoAquaCrews/nonebot_plugin_fortune)

[nonebot_plugin_tarot](https://github.com/MinatoAquaCrews/nonebot_plugin_tarot)

[nonebot_plugin_batarot](https://github.com/Perseus037/nonebot_plugin_batarot)

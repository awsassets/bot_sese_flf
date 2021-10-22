# bot_sese_flf

【典】不可以涩涩插件，生成敲敲图。（我就要涩涩 / 看别人敲我也敲）

*flf*: <ruby>
伏 <rp>(</rp><rt>**F**u</rt><rp>)</rp>
拉 <rp>(</rp><rt>**L**a</rt><rp>)</rp>
夫 <rp>(</rp><rt>**F**u</rt><rp>)</rp>
</ruby> （仅作为代号使用，两者无关联）

### Preview

<img src='https://cdn.jsdelivr.net/gh/fz6m/Private-picgo@moe-2021/img/20211023052448.gif' width='40%' />

### Usage

作为 [botoy](https://github.com/opq-osc/botoy) 插件使用，将整个 `bot_sese_flf` 文件夹放入你的插件文件夹即可自动导入。

之后使用 `ss ${text}` 命令使用该功能，最终会在图片上渲染 `${text}` 部分内容。

### Options

绘图过程中存在一些魔法参数，正常情况下默认好用，在你没有十足了解前，你不应该去修改他。

var|default|desc
:-:|:-:|:-
`scale`|`1`|适配高清反锯齿时的参数，当变大时会让字体更清晰，图片体积更大，同时还影响到文字位置的绘制
`fixed_padding_bottom`|`10 * scale`|文字距离图片下部的距离
`fixed_x_padding`|`4 * 2 * scale`|文字最长的情况，左右必须预留的空白距离之和
`init_font_size`|`24 * scale`|第一次尝试绘制时的基础字体大小，若绘制时发现距离不足字号将衰减，最终衰减至 `min_font_limit` 大小
`min_font_limit`|`init_font_size / 1.65`|最小绘制字号，当衰减至比这个字号还小时，将放弃绘制（此时文字将很难看清，绘制没有意义）
`start_draw_text_index`|`10`|开始绘制文字的帧数
`throttle_w`|`360`|最终图片宽度
`throttle_h`|`204`|最终图片高度

注：并不是所有的参数都被抽离，这些参数仅用来提供给希望理解绘制过程的人参考使用。

### Resources

 - `bot_sese_flf/font`: 存放字体文件

 - `bot_sese_flf/origin`: 存放初始 gif 图片



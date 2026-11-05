# Ins Editorial Layout

Agent Skill for Instagram-style editorial photo layouts. Ins 风杂志排版、照片日记与留白拼图。

## 功能

- TYP：大字断行与星芒贴纸。
- JNL：括号画中画照片日记。
- GAL：暖白画廊留白，默认单张居中无字。
- MAG：极简留白与衬线注脚。
- 默认 1080 × 1440（3:4），保留 Ins 风格顶底栏。

## 使用

下载仓库，将仓库根目录（包含 SKILL.md）命名为 ins-editorial-layout，并将该文件夹放入所用 Agent 支持的技能目录，然后请求：

> 使用 ins-editorial-layout，把这些照片每张做一页，使用无字留白版。

> 使用 ins-editorial-layout，制作杂志感大字和星芒贴纸排版。

## 文件

- SKILL.md：技能说明。
- references/layout_families.md：版式参考。
- scripts/colx_ins_engine.py：Python 渲染引擎。

## 运行依赖

脚本依赖 Python、Pillow，以及自行提供的可用字体文件。渲染引擎是供调用的 Python 类，需要传入图片和字体路径。

仓库保留原始 Skill 内容；版式数量及导出能力以说明和实际实现为准。


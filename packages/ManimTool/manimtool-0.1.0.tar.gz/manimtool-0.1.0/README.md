# 导入 Import

```python
from ManimTool import *
```

依赖库(Requires)：`manim`

***发现任何bug或问题，请反馈到tommy1008@dingtalk.com，谢谢！**

***If you find any bugs or issues, please report them to tommy1008@dingtalk.com, thank you!** 

# Manim工具 Manim Tool

了解更多详情，请前往[Manim Community](https://www.manim.community)。

For more details, visit [Manim Community](https://www.manim.community).

## 公式与图形 Formulas and Graphics

```python
def ChineseMathTex(*texts, font="SimSun", tex_to_color_map={}, **kwargs):
```

**创建中文数学公式。** 在此函数的公式部分和`tex_to_color_map`中直接写入中文即可，无需包裹`\text{}`，返回`MathTex`。`font`，设置公式中的中文字体。所有原版参数都可使用。

**Creates Chinese mathematical formulas.** You can directly write Chinese characters in the formula part of this function and in `tex_to_color_map` without wrapping them in `\text{}`. Returns `MathTex`. The `font` parameter sets the Chinese font for the formula. All original parameters can be used.

```python
def YellowLine(**kwargs):
```

**创建黄色的`Line`。** 所有原版参数都可使用。

**Creates a yellow `Line`.** All original parameters can be used.

```python
def LabelDot(dot_label, dot_pos, label_pos=DOWN, buff=0.1):
```

**创建一个带有名字的点，返回带有点和名字的`VGroup`。** `dot_label`，点的名字，字符串。`dot_pos`，点的位置，位置列表`[x,y,z]`。`label_pos`，点的名字相对于点的位置，Manim中的八个方向。`buff`，点的名字与点的间距，数值。

**Creates a point with a name. Returns a `VGroup` containing the point and its name.**  `dot_label` is the name of the point (a string). `dot_pos` is the position of the point (a list `[x, y, z]`). `label_pos` is the position of the label relative to the point (one of the eight directions in Manim). `buff` is the spacing between the label and the point (a numerical value).

```python
def MathTexLine(mathtex: MathTex, direction=UP, buff=0.5, **kwargs):
def MathTexBrace(mathtex: MathTex, direction=UP, buff=0.5, **kwargs):
def MathTexDoublearrow(mathtex: MathTex, direction=UP, buff=0.5, **kwargs):
```

**创建可以标注内容的图形，返回带有图形和标注内容的`VGroup`。** `mathtex`，标注的公式，`MathTex`类型。`direction`，标注内容相对于线的位置，Manim中的八个方向。`buff`，标注内容与图形的间距，数值。图形的所有原版参数都可使用。

**Creates graphics that can annotate content. Returns a `VGroup` containing the graphic and the annotation.** `mathtex` is the formula to be annotated (of type `MathTex`). `direction` is the position of the annotation relative to the line (one of the eight directionsin Manim). `buff` is the spacing between the annotation and the graphic (a numerical value). All original parameters of the graphics can be used.

```python
def ExtendedLine(line: Line, extend_distance: float) -> Line:
```

**将一条线延长`extend_distance`的距离，返回延长后的`Line`。** `line`，`Line`类型。`extend_distance`，要延长的距离，数值。

**Extends a line by `extend_distance`. Returns the extended `Line`.** `line` must be of type `Line`. `extend_distance` is the distance to extend (a numerical value).

## 交点 Intersection Points

```python
def CircleInt(circle1, circle2):
def LineCircleInt(line, circle):
def LineInt(line1: Line, line2: Line) -> Optional[Tuple[float, float]]:
def LineArcInt(line: Line, arc: Arc) -> list:
```

**函数名代表了寻找具体图形交点的功能**，例如`LineCircleInt`代表寻找`Line`和`Circle`的交点，返回点位置`[x,y,z]`，如果没有交点会返回`None`。

**The function names represent the function of finding the intersection points of specific shapes.** For example, `LineCircleInt` represents finding the intersection points of `Line` and `Circle`. Returns point position `[x,y,z]`. If there are no intersection points, it will return `None`.

## 动画 Animations

```python
def VisDrawArc(scene: Scene, arc: Arc, axis=OUT, run_time=1):
```

 **创建可视化（显示半径）的绘弧动画。** 直接使用即可，无需写入`self.play()`内。 `scene`，动画场景。`arc`， 已经定义好的`Arc`。`axis`，只有2个值`IN`和`OUT`，分别表示正方向还是反方向作弧。`run_time`，这是绘弧动画的时长。

**Creates a visualized arc drawing animation (with radius display).** Can be used directly without wrapping in `self.play()`. `scene` refers to the animation scene. `arc` is the predefined `Arc` object. `axis` accepts two values: `IN` (positive direction) and `OUT` (negative direction), indicating the drawing direction of the arc. `run_time` denotes the duration of the arc drawing animation.

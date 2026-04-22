<details>
<summary> <span style="padding: 2px 5px; border-radius: 10px;"> c++ 耗时 </span> </summary>

style="background-color: #007acc; color: white; padding: 2px 5px; border-radius: 10px;"

```cpp
#include <chrono>
#include <iostream>

int main() {
  system("chcp 65001");
  namespace c = std::chrono;
  auto start = c::steady_clock::now();
  auto duration = c::duration<double, std::milli>(c::steady_clock::now() - start);
  std::cout << "耗时 1: " << duration.count() << " ms \n";

  system("pause");
  return 0;
}
```
</details>

<details>
<summary> <span > Issue with double-click </span> </summary>
<video src="attachments/70f0c806-0281-4eec-9f66-4f550eb628b6" title="doubleclick.mp4" controls></video>
The issue seems to stem from `interface/interface_handlers.cc:4745~4752` . 
I create a report #153636 for this.
I'm unsure if this should be addressed in the current PR or how best to solve it. 
</details>

---


**这是加粗的文字**
*这是斜体的文字*
- **严重错误:** <span style="color: red; font-weight: bold;">[ERROR] 致命错误：请立即检查。</span>
- **成功提示:** <span style="color: #008000;">✓ 配置已成功加载。</span>
- **行内高亮:** 变量名必须是 <span style="background-color: #ffcccc;">小写字母</span> 开头。

这个 Bug 属于：
- 状态：<span style="background-color: #CC0000FF; color: white; padding: 2px 5px; border-radius: 10px;">处理中</span>
- 模块：<span style="background-color: #e6e6e6; color: #0800FFFF; padding: 2px 5px; border-radius: 3px; border: 1px solid #FFAFAFFF;">核心算法</span>

- **警示标题:** <span style="font-size: 1.5em; color: darkred; border-bottom: 2px solid darkred;">⚠️ 重要通告</span>
- **微小提示:** <span style="font-size: 0.8em; color: #666;">（此功能在 v1.0 后已弃用）</span>

这是带有阴影的标签：
<span style="
  background-color: #FF000011;
  padding: 5px 10px;
  border-radius: 15px;
  box-shadow: 2px 2px 10px #FF000078;
">带有阴影的标签内容</span>



<span style="font-family: monospace;">这是一段等宽字体</span>，但它仍然和 <span style="color: blue;">蓝色字体</span> 在同一行显示。
<mark>这通常是黄色高亮</mark>
<kbd>这是一个键盘按键提示</kbd> (某些主题可能带有边框和颜色)

### <center> 文件保存：按 <kbd>Ctrl</kbd> + <kbd>S</kbd> </center>

强制换行：请注意，这是第一行，后面我将用 <br> 实现换行。

<details>
<summary> 引用 </summary>

> [!NOTE]
>
> # 描述过时懒得改

> [!IMPORTANT]
>
> **VoronoiLinker修改的[neliut/VoronoiLinker](https://github.com/neliut/VoronoiLinker),支持Blender最新版本**

> [!TIP]

> [!WARNING]

> [!CAUTION]

</details>
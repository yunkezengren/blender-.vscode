# WS-04 `.inl`、调用约定与命名约束

<div style="font-family:'Segoe UI','Microsoft YaHei',system-ui,-apple-system,sans-serif;display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:16px 0 20px;padding:10px 14px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px">
<span style="font-size:11px;font-weight:700;letter-spacing:.1em;color:#64748B;margin-right:2px">导航</span>
<a href="../README.md" style="font-size:13px;color:#334155;background:#F1F5F9;border:1px solid #E2E8F0;border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap">总入口</a>
<a href="./README.md" style="font-size:13px;color:#2563EB;background:#EFF6FF;border:1px solid #BFDBFE;border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap">本章 08-窗口系统与核心类型</a>
<a href="./03-启动术语与构建形态详解.md" style="font-size:13px;color:#7A3AED;background:#F5F3FF;border:1px solid #DDD6FE;border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap">‹ 启动术语与构建形态详解</a>
</div>

<div style="font-family:'Segoe UI','Microsoft YaHei',system-ui,-apple-system,sans-serif;margin:18px 0 22px;padding:14px 18px;background:#F5F3FF;border-left:4px solid #7C3AED;border-radius:10px">

**基准说明**：Blender **5.4.0-alpha** 本地工作树 + 本机两份 MSVC CRT 源码。

本文回答四类「代码组织与平台约束」问题：

1. `.inl` 文件是什么？两个 MSVC 版本的 CRT 源码有什么区别？
2. `__cdecl` 是什么？为什么 CRT 到处标它？
3. `bpy_module_delay_init` 可以改名，`dealloc_obj_dealloc` 必须叫这个吗？
4. Python 对象销毁（`tp_dealloc`）的契约是什么？

</div>

## §1 `.inl` 是什么

### §1.1 它只是"被 `#include` 的源文件"

`.inl` = **inline**（内联）。但它**不是 C++ 关键字 `inline` 的扩展**
（标准里内联函数仍然写在 `.h` / `.hpp` / `.cpp` 里）。

**`.inl` 是一个纯约定俗成的扩展名**，意思是：

> 「这个文件**不是独立编译单元**，它只是等待被 `#include` 的代码片段。」

编译器对 `.inl` 没有任何特殊处理——它看到的就是被 `#include` 展开的普通文本。

### §1.2 证据：四个 `exe_*.cpp` 共用一个 `.inl`

本机 MSVC 目录下：

```
crt\src\vcruntime\
    exe_main.cpp           ← main 入口
    exe_wmain.cpp          ← wmain 入口
    exe_winmain.cpp        ← WinMain 入口
    exe_wwinmain.cpp       ← wWinMain 入口
    exe_common.inl         ← 四者共享的公共实现
```

**四个 `.cpp` 的内容几乎完全一样**：

```cpp
// exe_main.cpp
#define _SCRT_STARTUP_MAIN
#include "exe_common.inl"

extern "C" DWORD mainCRTStartup(LPVOID)
{
    return __scrt_common_main();
}
```

```cpp
// exe_wmain.cpp
#define _SCRT_STARTUP_WMAIN
#include "exe_common.inl"

extern "C" DWORD wmainCRTStartup(LPVOID)
{
    return __scrt_common_main();
}
```

```cpp
// exe_winmain.cpp
#define _SCRT_STARTUP_WINMAIN
#include "exe_common.inl"

extern "C" DWORD WinMainCRTStartup(LPVOID)
{
    return __scrt_common_main();
}
```

```cpp
// exe_wwinmain.cpp
#define _SCRT_STARTUP_WWINMAIN
#include "exe_common.inl"

extern "C" DWORD wWinMainCRTStartup(LPVOID)
{
    return __scrt_common_main();
}
```

**唯一的差别是两处**：`#define` 的宏名，和入口函数的名字。

### §1.3 为什么这样组织（核心设计）

因为 `__scrt_common_main_seh` 里的 `invoke_main` 有**四个变体**：

```cpp
// exe_common.inl · L76
#if defined _SCRT_STARTUP_MAIN
    static int __cdecl invoke_main()
    {
        return main(__argc, __argv, _get_initial_narrow_environment());
    }
#elif defined _SCRT_STARTUP_WMAIN
    static int __cdecl invoke_main()
    {
        return wmain(__argc, __wargv, _get_initial_wide_environment());
    }
#elif defined _SCRT_STARTUP_WINMAIN
    static int __cdecl invoke_main()
    {
        return WinMain(reinterpret_cast<HINSTANCE>(&__ImageBase), nullptr,
                       _get_narrow_winmain_command_line(),
                       __scrt_get_show_window_mode());
    }
#elif defined _SCRT_STARTUP_WWINMAIN
    static int __cdecl invoke_main()
    {
        return wWinMain(...);
    }
#endif
```

**如果不用 `.inl`，而是把公共实现放在 `.cpp` 里、用普通函数调用**，就会出问题：

| 方案 | 问题 |
| --- | --- |
| 公共实现放 `.cpp`，四份 `.cpp` 各自链接 | 需要**运行时**分发（虚函数/函数指针），有开销 |
| 公共实现放 `.cpp`，用宏区分 | 宏不跨翻译单元，`.cpp` 里的 `#if` 看不到别的文件定义的宏 |
| **公共实现放 `.inl`，每个 `.cpp` 各自 `#include`** | **每个 `.cpp` 都编译出自己的特化版本**，零运行时开销 |

**所以 `.inl` 是「编译期多态」的实现手段**：让同一份代码在四个不同的宏环境下
各编译一次，各自生成针对自己入口点的 `invoke_main` 和 `__scrt_common_main_seh`。

### §1.4 `.inl` 与其他扩展名的区别

| 扩展名 | 含义 | 会被单独编译吗 |
| --- | --- | --- |
| `.h` / `.hpp` | 头文件，声明 + 内联函数 + 模板 | ❌ 不 |
| **`.inl`** | **"要 include 的实现代码"** | ❌ 不 |
| `.ipp` | 同 `.inl`（template implementation） | ❌ 不 |
| `.tcc` | 同 `.inl`（template C++ code） | ❌ 不 |
| `.def` | 模块导出定义（Windows） | 特殊处理 |
| `.inc` | 通用的"被 include 的片段" | ❌ 不 |

**`.inl` / `.ipp` / `.tcc` 三者没有本质区别，只是不同项目的习惯。**

### §1.5 Blender 里的类似用法

Blender 也有大量的 `*.cc` 被 `#include`，只是不用 `.inl` 后缀：

```dml-ignore
source/blender/nodes/intern/geometry_nodes_repeat_zone.cc     ← 独立编译
source/blender/functions/intern/lazy_function_graph_executor_generic.hh
    ↑ 这个名字带 generic，实际是被 lazy_function_graph_executor.cc include 的
```

**Blender 用 `.hh` 装模板实现**（C++ 社区的通行做法），MSVC 的 CRT 用 `.inl`。

<hr style="border:none;height:1px;background:linear-gradient(90deg,#BFDBFE,#E2E8F0 55%,transparent);margin:34px 0">

## §2 两份 CRT 源码的区别：**零**

### §2.1 实测结果

```
D:\Soft\Visual Studio\VC\Tools\MSVC\14.44.35207\crt\src\vcruntime\exe_common.inl
    大小: 10,371 字节    行数: 331

C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\
    VC\Tools\MSVC\14.29.30133\crt\src\vcruntime\exe_common.inl
    大小: 10,371 字节    行数: 331

逐行对比: 0 行差异
```

**文件逐字节完全相同。**

### §2.2 为什么会这样

因为**这段代码已经稳定了二十多年**。`__scrt_common_main_seh` 的逻辑
（初始化 CRT → 构造全局对象 → 调 main → exit）从 VC6 时代就没变过。

微软只在新版本里做**极小的**修改（比如安全加固、新的 TLS 回调支持）。
`14.29`（VS2019）和 `14.44`（VS2022）之间这段没动过。

### §2.3 那这两个版本真正差在哪

| 层面 | 是否变化 |
| --- | --- |
| `exe_common.inl`（这段启动代码） | ❌ **没变** |
| 编译器本身（优化、C++ 标准支持） | ✅ 变了很多 |
| 其他 CRT 源码（`heap/`、`stdio/`、`locale/`） | ✅ 有变化 |
| 运行时行为（`malloc` 实现、`printf` 格式化） | ✅ 有变化 |
| 安全加固（`/GS`、CFG、`_set_security_error_handler`） | ✅ 有变化 |

**所以对于"读懂启动流程"这个目的，两个版本读哪个都一样。**

### §2.4 对你调试的实际影响

如果你的 Blender 是用 **VS2019** 编译的，而调试器现在指向 **VS2022** 的路径，
**读源码时不会遇到任何不一致**——因为文件相同。

**结论：不用纠结版本，随便挑一个读。**

> 附带一个小知识：TBB 的版本差异就大得多了。`tbb12_debug.dll` 和
> `tbb12.dll` 的行为在不同 TBB 版本间有显著变化，那才是调试时需要注意版本的地方。

<hr style="border:none;height:1px;background:linear-gradient(90deg,#BFDBFE,#E2E8F0 55%,transparent);margin:34px 0">

## §3 `__cdecl` 是什么

### §3.1 一句话

**`__cdecl` = C declaration，x86 的一种"函数调用约定"（calling convention）。**

### §3.2 调用约定解决什么问题

函数调用时，双方必须就三件事达成一致：

| 问题 | 谁决定 |
| --- | --- |
| **参数怎么传** | 栈？寄存器？顺序从左到右还是从右到左？ |
| **谁清理栈** | 调用方（caller）还是被调方（callee）？ |
| **函数名怎么修饰** | `foo` 还是 `_foo` 还是 `_foo@8`？ |

**调用约定就是这三件事的"契约"。** 如果调用方和被调方理解不一致，栈会错位，程序崩溃。

### §3.3 x86 上主要的几种调用约定

| 约定 | 参数顺序 | 谁清栈 | 名字修饰 | 典型用途 |
| --- | --- | --- | --- | --- |
| **`__cdecl`** | **右到左** | **调用方** | `_foo` | **C 默认**、可变参数（`printf`） |
| `__stdcall` | 右到左 | **被调方** | `_foo@8` | Win32 API |
| `__fastcall` | 前两个用寄存器 | 被调方 | `@foo@8` | 性能敏感 |
| `__thiscall` | `this` 用 ECX | 被调方 | — | MSVC 的 C++ 成员函数 |
| `__vectorcall` | 用 XMM/YMM 寄存器 | 被调方 | — | SIMD |

### §3.4 为什么 `__cdecl` 是"C 默认"

因为它**唯一支持可变参数**：

```cpp
printf("%d %s %f", 1, "x", 3.14);   // 参数个数不定
```

**只有调用方知道实际传了几个参数**，所以只能由**调用方清栈**。
`__stdcall`（被调方清栈）在这种情况下无法工作。

### §3.5 为什么 CRT 到处标 `__cdecl`

```cpp
static int __cdecl invoke_main()
static __declspec(noinline) int __cdecl __scrt_common_main_seh()
static int __cdecl main(...)     // 你写的 main 其实也是 __cdecl
```

**三个原因**：

| 原因 | 说明 |
| --- | --- |
| **1. 必须和 `main` 的约定一致** | `invoke_main` 要调 `main`，两者必须约定相同 |
| **2. `main` 的约定由标准固定** | C 标准要求 `main` 是 C 链接（`__cdecl`） |
| **3. 防止项目级默认设置改变它** | MSVC 有 `/Gz`（默认 `__stdcall`）等编译选项 |

**第 3 条最关键**：如果某个项目用 `/Gz` 把所有函数默认改成 `__stdcall`，
而 CRT 没显式写 `__cdecl`，那么 `invoke_main` 调 `main` 时约定不匹配 → **栈破坏**。

所以 CRT 里**每个关键函数都显式标 `__cdecl`**，不依赖编译器的默认值。

### §3.6 在 x64 上还有意义吗

**几乎没有。** x64（和 ARM64）只有**一种**调用约定：

| 平台 | 调用约定数量 |
| --- | --- |
| x86 (32 位) | 多种（`__cdecl` / `__stdcall` / ...） |
| **x64** | **1 种**（微软的 x64 约定） |
| ARM64 | 1 种 |

**所以在 x64 上 `__cdecl` 是"空装饰"**——编译器接受它，但不改变任何行为。

**那为什么还留着**：因为同一份源码要同时支持 x86 和 x64。
在 x86 上有意义，在 x64 上无害。

> 你在 64 位 Blender 的栈里看到 `__cdecl`，只是源码里的装饰，不影响运行。

### §3.7 与 `extern "C"` 的区别（容易混淆）

```cpp
extern "C" DWORD mainCRTStartup(LPVOID)   // 这里有 extern "C"
```

| | `extern "C"` | `__cdecl` |
| --- | --- | --- |
| 作用 | **禁止 C++ name mangling** | **规定调用约定** |
| 影响符号名 | ✅ `foo` vs `?foo@@YAXXZ` | ✅ `_foo` vs `_foo@8` |
| 影响参数传递 | ❌ | ✅ |
| 影响谁清栈 | ❌ | ✅ |

**两者是独立的正交概念。** 一个函数可以：
- 是 `extern "C"` 且 `__cdecl`（最常见）
- 是 `extern "C"` 且 `__stdcall`（Win32 API 回调）
- 是 C++ 链接且 `__stdcall`（COM 接口方法）

`mainCRTStartup` 必须 `extern "C"`（否则链接器找不到符号），
但它**不标 `__cdecl`** —— 因为入口点的调用约定由操作系统决定（`LPVOID` 参数，`DWORD` 返回）。

<hr style="border:none;height:1px;background:linear-gradient(90deg,#BFDBFE,#E2E8F0 55%,transparent);margin:34px 0">

## §4 `dealloc_obj_dealloc` 必须叫这个名字吗

### §4.1 先给结论

**不必。名字可以随便改，但"必须赋给 `tp_dealloc`"这个约束必须满足。**

### §4.2 名字与约束的区别

```cpp
// bpy_interface.cc · L1147-L1159
static void dealloc_obj_dealloc(PyObject *self);       // 声明

static PyTypeObject dealloc_obj_Type;                  // 类型对象（空定义）

/* Use our own `dealloc` so we can free a property if we use one. */
static void dealloc_obj_dealloc(PyObject *self)        // 定义
{
  bpy_module_delay_init(((dealloc_obj *)self)->mod);

  /* NOTE: for sub-classed `PyObject` objects
   * we can't call #PyObject_DEL() directly or it will crash. */
  dealloc_obj_Type.tp_free(self);
}
```

然后在 `PyInit_bpy` 里赋值：

```cpp
// bpy_interface.cc · L1170-L1173
dealloc_obj_Type.tp_name = "dealloc_obj";
dealloc_obj_Type.tp_basicsize = sizeof(dealloc_obj);
dealloc_obj_Type.tp_dealloc = dealloc_obj_dealloc;      // ★ 关键这一行
dealloc_obj_Type.tp_flags = Py_TPFLAGS_DEFAULT;
```

**真正的约束是 `tp_dealloc = dealloc_obj_dealloc` 这个赋值，不是函数名本身。**

如果你把它改名为 `my_cleanup_fn`，只要把赋值改成：

```cpp
dealloc_obj_Type.tp_dealloc = my_cleanup_fn;
```

**一样能工作。**

### §4.3 那为什么叫这个名

因为**约定俗成的命名模式**：

```dml-ignore
<类型名>_<方法名>
  dealloc_obj  +  dealloc   =  dealloc_obj_dealloc
```

**对比 CPython 自己的实现**（`Objects/typeobject.cc` 里到处都是）：

```c
static void object_dealloc(PyObject *self)
static void type_dealloc(PyTypeObject *self)
static void long_dealloc(PyLongObject *self)
static void dict_dealloc(PyDictObject *self)
```

**这是 PEP 7（CPython 的 C 风格指南）的命名习惯**：`<typename>_<method>`。

**好处**：一眼就能看出"这个函数是处理 `dealloc_obj` 类型的 `dealloc`"。

### §4.4 `dealloc_obj_dealloc` 的签名**必须**是特定的

虽然名字自由，但**签名是固定的**：

```cpp
void (*tp_dealloc)(PyObject *self);
```

源码里是这样声明的（Python 的 `object.h`）：

```c
typedef void (*destructor)(PyObject *);
```

**所以你必须写成**：

```cpp
static void your_name(PyObject *self);   // ✅ 返回 void，参数 PyObject*
```

**不能**写成：

```cpp
static int your_name(PyObject *self);    // ❌ 返回类型不对
static void your_name(dealloc_obj *self); // ❌ 参数类型不对（虽然内部可以转）
```

**返回类型和参数类型都不能变**，否则就是函数指针类型不匹配（编译期报错或运行时未定义行为）。

### §4.5 为什么需要用 `dealloc_obj` 而不用 `PyObject`

```cpp
static void dealloc_obj_dealloc(PyObject *self)
{
  bpy_module_delay_init(((dealloc_obj *)self)->mod);
  //                     ↑ 这里强转
```

因为 `tp_dealloc` 的签名是 `void (*)(PyObject *)`，
但 Blender 需要访问 `dealloc_obj` 特有的 `mod` 字段。

**所以有两个设计点**：

| 设计 | 原因 |
| --- | --- |
| 参数类型是 `PyObject *` | Python C API 的固定契约 |
| 内部强转成 `dealloc_obj *` | 访问子类特有字段 |
| 用 `struct dealloc_obj { PyObject_HEAD; PyObject *mod; }` | **`PyObject_HEAD` 必须在开头**，这样强转合法 |

### §4.6 `PyObject_HEAD` 的布局约束

```cpp
// bpy_interface.cc · L1062
struct dealloc_obj {
  PyObject_HEAD           // ← 必须是第一个成员
  /* Type-specific fields go here. */
  PyObject *mod;
};
```

`PyObject_HEAD` 展开后是两个字段：

```c
#define PyObject_HEAD PyObject ob_base;
```

```c
typedef struct _object {
  Py_ssize_t ob_refcnt;     // 引用计数
  PyTypeObject *ob_type;    // 类型指针
} PyObject;
```

**所以 `dealloc_obj` 的实际内存布局是**：

```dml-ignore
偏移 0   ┌──────────────────┐
        │ ob_refcnt (8 字节)│  ┐
偏移 8   ├──────────────────┤  │ PyObject_HEAD
        │ ob_type  (8 字节) │  ┘
偏移 16  ├──────────────────┤
        │ mod      (8 字节) │  ← dealloc_obj 自己的字段
        └──────────────────┘
```

**因为 `PyObject_HEAD` 在开头，所以 `(PyObject*)` 和 `(dealloc_obj*)` 指向同一个地址**。
这是 C 语言里"模拟继承"的标准手法，也是 Python C API 的核心约定。

> ⚠️ 如果谁把 `mod` 放到 `PyObject_HEAD` 前面，强转就会读到错误的内存，
> **程序直接崩溃**。所以注释写"Type-specific fields go here"是严肃的警告。

### §4.7 那 `bpy_module_delay_init` 能改名吗

**能，完全自由。** 它只是个普通的 `static` 函数：

```cpp
// bpy_interface.cc · L1069
static void bpy_module_delay_init(PyObject *bpy_proxy)
```

**为什么它能自由改名**：

| 特性 | 说明 |
| --- | --- |
| `static` | 只在本翻译单元可见，不进符号表 |
| 不是回调 | 只被 `dealloc_obj_dealloc` 直接调用 |
| 不赋值给任何函数指针 | 没有外部约束 |

### §4.8 一张表说清"哪些名字是自由的"

| 名字 | 自由度 | 约束来源 |
| --- | --- | --- |
| `dealloc_obj`（结构体名） | **自由** | 只在本文件用 |
| `dealloc_obj_Type`（变量名） | **自由** | 只在本文件用 |
| `dealloc_obj_dealloc`（函数名） | **自由** | 只要赋给 `tp_dealloc` 就行 |
| `dealloc_obj_dealloc`（**签名**） | ❌ **固定** | `void (*)(PyObject *)` |
| `tp_dealloc`（字段名） | ❌ **固定** | Python C API 定义 |
| `tp_name` / `tp_basicsize` 等 | ❌ **固定** | 同上 |
| `bpy_module_delay_init` | **自由** | `static` 普通函数 |
| `PyInit_bpy` | ❌ **固定** | Python 模块导出符号，必须叫 `PyInit_<模块名>` |
| `struct dealloc_obj` 的 `mod` 字段位置 | ❌ **必须在 `PyObject_HEAD` 之后** | 内存布局约束 |

### §4.9 `PyInit_bpy` 为什么不能改名

这是**强制的**，因为 Python 的 import 机制按名字查找：

```cpp
PyMODINIT_FUNC PyInit_bpy()      // 模块名是 "bpy"，符号必须是 PyInit_bpy
```

| 模块名 | 导出符号 |
| --- | --- |
| `bpy` | `PyInit_bpy` |
| `_bpy` | `PyInit__bpy` |
| `mathutils` | `PyInit_mathutils` |
| `bmesh` | `PyInit_bmesh` |

**这是 Python 扩展模块的 ABI 约定**，改了就 `import` 不进来。

### §4.10 `__formal`：调试器给"无名参数"编的名字

在断点栈里看到过：

```dml-ignore
blender.exe!main(int argc, const char * * __formal) Line 348
```

**`__formal` 不在 Blender 源码里**——全仓库搜索命中 **0 处**。
它是 **MSVC 调试器合成的占位名**。

#### 为什么这个参数没有名字

源码（creator.cc · L332-L338）：

```cpp
int main(int argc,
#ifdef USE_WIN32_UNICODE_ARGS
         const char ** /*argv_c*/      // ← 名字被注释掉了
#else
         const char **argv
#endif
)
```

**Windows 上 `USE_WIN32_UNICODE_ARGS` 成立，所以第二个参数只有类型、没有名字。**

C++ 允许无名参数：

```cpp
void f(int, double);      // 合法，函数体内不能用这两个参数
```

于是调试器想显示这个参数时**没有名字可用**，MSVC 就填入 `__formal`。

#### `formal` 的含义

| 术语 | 英文 | 含义 |
| --- | --- | --- |
| **形参** | **formal parameter** | 函数**定义**里声明的参数 |
| **实参** | actual parameter / **argument** | 函数**调用**时传入的值 |

**`__formal` 的字面意思：「这是一个形参（但没有名字）」**

`__` 双下划线表示"实现内部产生的名字"，不是用户代码写的。

#### 和 `/*argv_c*/` 的因果关系

```dml-ignore
为什么写 /*argv_c*/ 而不是 /*argv*/
  ↓ 避免和函数体内重新声明的 argv 混淆
副作用：这个参数在 Windows 上彻底没有名字
  ↓
结果：调试器显示 __formal
```

**`__formal` 是"注释掉参数名"这个决定在调试器里的直接投影。**
如果当初写成 `const char **argv_c`（不注释），栈上就会显示 `argv_c` 而不是 `__formal`。

#### `__formal` 出现的其他场景

| 场景 | 例子 |
| --- | --- |
| 参数名被注释掉 | Blender 这里 |
| 参数名省略（只留类型） | `void f(int, double)` |
| 编译器生成的合成参数 | 构造函数里的隐藏 `this`、返回值 RVO 参数 |

**共同点：源码里没有可用名字，调试器必须编一个。**

> 同类命名还有 `__$ReturnUdt`（返回值优化用的隐藏参数）、`__this`（成员函数的 this 指针）。
> 它们都是"源码里没写、但 ABI 上必须存在"的东西。

<hr style="border:none;height:1px;background:linear-gradient(90deg,#BFDBFE,#E2E8F0 55%,transparent);margin:34px 0">

## §5 `tp_dealloc` 的完整契约

既然讲到这里，把 Python 对象销毁的机制说清楚。

### §5.1 什么时候触发

`tp_dealloc` 在**引用计数归零**时被调用：

```dml-ignore
某处 Py_DECREF(obj)  →  计数 -1  →  == 0 ?
                                    ├─ 是 → 调用 ob_type->tp_dealloc(obj)
                                    └─ 否 → 什么也不做
```

### §5.2 标准释放流程（三步）

一个正确的 `tp_dealloc` 必须做三件事：

```dml-ignore
① 清理自己持有的引用（Py_DECREF 或 Py_XDECREF 成员）
② 释放为对象分配的内存
③ 如果支持子类化，还要减少类型对象的引用计数
```

### §5.3 Blender 的版本为什么"少了一步"

```cpp
static void dealloc_obj_dealloc(PyObject *self)
{
  bpy_module_delay_init(((dealloc_obj *)self)->mod);   // ① 先做业务逻辑
  dealloc_obj_Type.tp_free(self);                       // ② 再释放内存
}
```

**没有第 ③ 步（减少类型引用计数）**，为什么？

因为 `dealloc_obj_Type` 是**静态的、不参与引用计数的类型对象**（不是 `PyType_Ready` 那种堆类型）。
它的生命周期是进程级的，不需要担心。

**也没有 `Py_DECREF(mod)`**，为什么？

因为 `mod` 是 **borrow 的引用**（见注释 `dob->mod = bpy_proxy; /* borrow */`）。
它不增加引用计数，所以也不该减少。

### §5.4 `tp_free` 与 `PyObject_DEL` 的区别

```cpp
/* NOTE: for sub-classed `PyObject` objects
 * we can't call #PyObject_DEL() directly or it will crash. */
dealloc_obj_Type.tp_free(self);
```

**这个注释点出了一个常见陷阱。**

| 方式 | 用哪个分配器释放 |
| --- | --- |
| `PyObject_DEL(obj)` | 硬编码 `PyObject_Free`（默认分配器） |
| `PyObject_GC_Del(obj)` | GC 分配器 |
| **`ob_type->tp_free(obj)`** | **类型自己配置的分配器** |

**为什么必须用 `tp_free`**：
如果类型在 `tp_alloc` 时用了**自定义分配器**（比如从内存池分配），
而释放时用了默认的 `PyObject_Free`，就是**分配器不匹配** → 堆损坏。

**所以 CPython 的规范做法是：`tp_dealloc` 里总是调 `Py_TYPE(self)->tp_free(self)`**，
而不是硬编码 `PyObject_DEL`。

### §5.5 为什么用 `dealloc_obj` 这个"假 __file__" trick

回到 Blender 的设计动机（源码注释 L1191-L1193）：

```cpp
/* 3) We don't know the file-path at this point, workaround by assigning a dummy value
 *    which calls back when its freed so the real loading can take place. */
```

**完整时序**：

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"\"Segoe UI\",\"Microsoft YaHei\",sans-serif","fontSize":"15px","lineColor":"#94A3B8","edgeLabelBackground":"#FFFFFF","clusterBkg":"#F8FAFC","clusterBorder":"#CBD5E1"},"flowchart":{"htmlLabels":false,"curve":"basis","nodeSpacing":52,"rankSpacing":64,"padding":14,"diagramPadding":16,"useMaxWidth":true},"sequence":{"useMaxWidth":true,"wrap":true,"mirrorActors":false,"messageMargin":36}}}%%
sequenceDiagram
    participant PY as "Python import 机制"
    participant EXT as "PyInit_bpy"
    participant MOD as "bpy_proxy 模块对象"
    participant DOB as "dealloc_obj 实例"
    participant INIT as "bpy_module_delay_init"

    EXT->>MOD: "PyModule_Create()"
    EXT->>DOB: "tp_alloc() 创建实例"
    EXT->>DOB: "dob-&gt;mod = bpy_proxy (borrow)"
    EXT->>MOD: "PyModule_AddObject(__file__, dob)"
    EXT-->>PY: "返回 bpy_proxy"

    Note over PY: "Python 认为 __file__ 是模块的真实路径"
    PY->>MOD: "设置 __file__ = 真实路径"
    Note over DOB: "被覆盖 → 引用计数归零"
    DOB->>DOB: "tp_dealloc → dealloc_obj_dealloc()"
    DOB->>INIT: "bpy_module_delay_init(mod)"
    Note over INIT: "此刻 __file__ 已就绪<br/>可以拿到真实路径"
    INIT->>INIT: "main_python_enter(argv[0] = 路径)"
    INIT->>MOD: "PyDict_Update() 合并 Python 包的 dict"
    INIT->>MOD: "给 bpy/bpy.types/_bpy 塞 capsule"
```

**这是一个"利用析构时机"的巧妙设计**：

| 时刻 | `__file__` 状态 | 能否初始化 |
| --- | --- | --- |
| `PyInit_bpy` 执行中 | ❌ 还没设置 | ❌ |
| **`dealloc_obj` 析构时** | ✅ **刚设置好** | ✅ **最佳时机** |

**本质**：用一个"占位对象"把初始化**推迟到第一个可利用的时机**。

### §5.6 这个模式叫什么

在 C++ 里，类似的技术叫 **"RAII on destruction"** 或 **"scope guard"**。
但这里的动机不同：**不是为了保证清理，而是为了"在某个事件发生时执行代码"**。

更准确的类比是 **"析构回调"（destructor callback）** 或 **"sentinel object"**。

## §6 四种入口点的对照

把 CRTP 那边的知识串起来：

| 入口文件 | 宏 | 入口函数 | 用户函数 |
| --- | --- | --- | --- |
| `exe_main.cpp` | `_SCRT_STARTUP_MAIN` | `mainCRTStartup` | `int main(int, char**)` |
| `exe_wmain.cpp` | `_SCRT_STARTUP_WMAIN` | `wmainCRTStartup` | `int wmain(int, wchar_t**)` |
| `exe_winmain.cpp` | `_SCRT_STARTUP_WINMAIN` | `WinMainCRTStartup` | `int WinMain(...)` |
| `exe_wwinmain.cpp` | `_SCRT_STARTUP_WWINMAIN` | `wWinMainCRTStartup` | `int wWinMain(...)` |

**四者都 `#include "exe_common.inl"`，靠宏选择 `invoke_main` 的特化版本。**

**Blender 走第一个**（`exe_main.cpp`），所以入口是 `mainCRTStartup`，
拿到的是窄字符 `char**`，进而必须在 [08-02 §2](02-main函数全文解析.md) 里
用 `GetCommandLineW()` 重取 UTF-8 参数。

## 附录：源码索引

| 符号 | 文件 | 行 |
| --- | --- | --- |
| `exe_main.cpp` 全文 | `%VS%\...\crt\src\vcruntime\exe_main.cpp` | 1-17 |
| `exe_wmain.cpp` / `exe_winmain.cpp` / `exe_wwinmain.cpp` | 同目录 | 1-17 各 |
| `_SCRT_STARTUP_*` 宏分支 | `exe_common.inl` | 76-145 |
| `__scrt_common_main`（含 `/GS` cookie） | `exe_common.inl` | 323-331 |
| `__scrt_common_main_seh` | `exe_common.inl` | 235-318 |
| `dealloc_obj` 结构体 | bpy_interface.cc | 1062-1066 |
| `bpy_module_delay_init` | bpy_interface.cc | 1069 |
| `dealloc_obj_dealloc` 前置声明 | bpy_interface.cc | 1147 |
| `dealloc_obj_dealloc` 定义 | bpy_interface.cc | 1152-1159 |
| `tp_dealloc` 赋值 | bpy_interface.cc | 1172 |
| `PyInit_bpy` | bpy_interface.cc | 1163 |
| `dealloc_obj` 占位 `__file__` | bpy_interface.cc | 1195-1200 |
| `main_python_enter` 调用 | bpy_interface.cc | 1088 |

## 附录二：三分钟自测

**`.inl`**

1. `.inl` 是编译器认识的扩展名吗？它对 `.inl` 有特殊处理吗？
2. 为什么 MSVC 要用 `.inl` 而不是把公共实现放在 `.cpp` 里？
3. `exe_main.cpp` 和 `exe_wmain.cpp` 的差别有哪两处？
4. 你本机两个 MSVC 版本的 `exe_common.inl` 有什么区别？（提示：实测）

**调用约定**

5. 调用约定要规定哪三件事？
6. 为什么 `__cdecl` 是 C 的默认约定？它和可变参数有什么关系？
7. `extern "C"` 和 `__cdecl` 分别管什么？为什么是正交的？
8. x64 上 `__cdecl` 有意义吗？为什么源码还留着？

**命名约束**

9. `dealloc_obj_dealloc` 可以改名吗？改名后要同步改什么？
10. 哪些东西的名字是**不能**改的？各举一个例子。
11. `tp_dealloc` 的签名是什么？如果改成 `int (*)(PyObject*)` 会怎样？
12. 为什么 `dealloc_obj` 里 `PyObject_HEAD` 必须在第一个成员？
13. 为什么释放内存要用 `tp_free` 而不是 `PyObject_DEL`？
14. 栈里的 `__formal` 是源码写的还是调试器编的？它为什么会出现？
15. `formal parameter` 和 `actual parameter` 分别对应中文什么词？

**设计意图**

16. 为什么 Blender 要用"假 `__file__` + 析构回调"这种方式初始化？
17. `main_python_enter` 为什么不能直接在 `PyInit_bpy` 里调用？

<div style="font-family:'Segoe UI','Microsoft YaHei',system-ui,-apple-system,sans-serif;margin:38px 0 4px;padding:13px 16px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;display:flex;flex-wrap:wrap;align-items:center;gap:8px">
<span style="font-size:11px;font-weight:700;letter-spacing:.1em;color:#64748B;margin-right:2px">继续阅读</span>
<a href="../README.md" style="font-size:13px;color:#334155;background:#F1F5F9;border:1px solid #E2E8F0;border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap">总入口</a>
<a href="./03-启动术语与构建形态详解.md" style="font-size:13px;color:#2563EB;background:#EFF6FF;border:1px solid #BFDBFE;border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap">‹ 启动术语与构建形态详解</a>
<span style="font-size:13px;color:#334155;background:#F1F5F9;border:1px solid #E2E8F0;border-radius:999px;padding:3px 12px;text-decoration:none;white-space:nowrap">回到顶部</span>
</div>

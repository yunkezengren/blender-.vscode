# C++标准库组件详细分析（第301-350号）

本文档详细分析了50个C++标准库组件，每个组件包含功能说明、使用场景和完整代码示例。

---

## 301. std::asin - 反正弦函数

### 功能说明

`std::asin`计算给定值的反正弦（arcsine），返回以弧度表示的角度。该函数是`<cmath>`头文件中定义的数学函数，属于C++标准库的数学运算组件。

**函数原型**：
```cpp
float asin(float arg);
double asin(double arg);
long double asin(long double arg);
```

**参数说明**：
- `arg`：要计算反正弦的值，必须在区间[-1.0, 1.0]内

**返回值**：
- 返回[-π/2, +π/2]范围内的反正弦值（弧度）
- 如果arg超出有效范围，返回NaN并可能设置errno

**重要特性**：
- 输入值必须在[-1, 1]范围内，否则结果为未定义或NaN
- 返回值单位为弧度，如需角度需转换：`degrees = radians * 180 / π`

### 使用场景

1. **三角函数计算**：在物理引擎中计算角度，如根据对边和斜边比值求夹角
2. **计算机图形学**：计算光照角度、视线角度等几何运算
3. **信号处理**：将信号幅值转换回相位角
4. **机器人学**：根据关节位置计算关节角度
5. **导航系统**：根据两点距离计算方位角

### 代码示例

```cpp
#include <iostream>
#include <cmath>
#include <iomanip>

const double PI = 3.14159265358979323846;

int main() {
    // 基本用法：计算常见值的反正弦
    double values[] = {0.0, 0.5, 1.0, -1.0, 0.70710678118};
    
    std::cout << "=== std::asin 示例 ===" << std::endl;
    std::cout << std::fixed << std::setprecision(6);
    
    for (double val : values) {
        double radian = std::asin(val);
        double degree = radian * 180.0 / PI;
        std::cout << "asin(" << val << ") = " << radian << " rad (" 
                  << degree << "°)" << std::endl;
    }
    
    // 实际应用：根据边长比例求角度
    double opposite = 3.0;
    double hypotenuse = 6.0;
    double sine_value = opposite / hypotenuse;
    double angle_rad = std::asin(sine_value);
    double angle_deg = angle_rad * 180.0 / PI;
    
    std::cout << "\n实际应用：" << std::endl;
    std::cout << "对边=" << opposite << ", 斜边=" << hypotenuse << std::endl;
    std::cout << "夹角 = " << angle_deg << "°" << std::endl;
    
    // 错误处理示例
    double invalid = 2.0; // 超出范围
    double result = std::asin(invalid);
    if (std::isnan(result)) {
        std::cout << "\nasin(2.0) 结果无效（超出[-1,1]范围）" << std::endl;
    }
    
    return 0;
}
```

---

## 302. std::any - 任意类型容器(C++17)

### 功能说明

`std::any`是C++17引入的类型安全容器，可以存储任意类型的单个值。它位于`<any>`头文件中，提供了类型擦除机制，使容器能够持有任何可复制构造的类型。

**主要成员函数**：

| 函数 | 说明 |
|------|------|
| `any()` | 默认构造函数，创建空any对象 |
| `any(const any& other)` | 拷贝构造函数 |
| `any(any&& other)` | 移动构造函数 |
| `template<class T> any(T&& value)` | 从值构造 |
| `emplace<T>(args...)` | 原地构造类型T的对象 |
| `reset()` | 销毁存储的对象 |
| `has_value()` | 检查是否包含值 |
| `type()` | 返回存储值的type_info |

**类型转换**：
- `any_cast<T>(any_obj)`：转换为类型T，失败抛出bad_any_cast
- `any_cast<T>(&any_obj)`：返回指针，失败返回nullptr

### 使用场景

1. **异构容器**：存储不同类型的对象，如配置系统中的任意配置值
2. **类型擦除**：实现泛型接口，隐藏具体类型细节
3. **动态类型系统**：脚本语言绑定、解释器实现
4. **消息传递系统**：不同类型消息的统一定义
5. **插件系统**：插件返回不同类型的数据给主程序

### 代码示例

```cpp
#include <iostream>
#include <any>
#include <string>
#include <vector>

int main() {
    // 基本用法：存储不同类型的值
    std::any a;
    
    // 存储整数
    a = 42;
    std::cout << "存储整数: " << std::any_cast<int>(a) << std::endl;
    
    // 存储字符串
    a = std::string("Hello, std::any!");
    std::cout << "存储字符串: " << std::any_cast<std::string>(a) << std::endl;
    
    // 存储浮点数
    a = 3.14159;
    std::cout << "存储浮点数: " << std::any_cast<double>(a) << std::endl;
    
    // 使用emplace原地构造
    a.emplace<std::vector<int>>({1, 2, 3, 4, 5});
    auto& vec = std::any_cast<std::vector<int>&>(a);
    std::cout << "存储vector: ";
    for (int n : vec) std::cout << n << " ";
    std::cout << std::endl;
    
    // 实际应用：配置系统
    std::cout << "\n=== 配置系统示例 ===" << std::endl;
    std::vector<std::any> config;
    config.push_back(std::string("app_name"));
    config.push_back(8080);  // port
    config.push_back(true);  // debug_mode
    config.push_back(1.5);   // scale_factor
    
    std::cout << "配置项数量: " << config.size() << std::endl;
    
    // 安全访问（使用指针形式）
    if (auto ptr = std::any_cast<int>(&config[1])) {
        std::cout << "端口号: " << *ptr << std::endl;
    }
    
    // 检查类型
    std::cout << "\n类型检查:" << std::endl;
    for (const auto& item : config) {
        std::cout << "类型: " << item.type().name() << std::endl;
    }
    
    // 清空
    a.reset();
    std::cout << "\n清空后has_value: " << std::boolalpha << a.has_value() << std::endl;
    
    return 0;
}
```

---

## 303. std::adjacent_find - 查找相邻重复元素

### 功能说明

`std::adjacent_find`是`<algorithm>`头文件中的算法，用于在范围内查找第一对相邻的相等元素。支持自定义比较谓词，提供灵活的判断逻辑。

**函数原型**：
```cpp
// 使用operator==比较
ForwardIt adjacent_find(ForwardIt first, ForwardIt last);

// 使用自定义谓词
ForwardIt adjacent_find(ForwardIt first, ForwardIt last, BinaryPredicate p);
```

**参数说明**：
- `first`, `last`：要搜索的范围 [first, last)
- `p`：二元谓词，接受两个元素返回bool

**返回值**：
- 找到时：指向第一对相邻相等元素中第一个元素的迭代器
- 未找到时：返回`last`

**复杂度**：
- 最坏情况：调用谓词或operator==次数为`(last - first) - 1`
- 线性时间复杂度O(n)

### 使用场景

1. **数据验证**：检查输入序列中是否有连续重复的数据点
2. **日志分析**：查找日志中连续重复的异常记录
3. **去重预处理**：在排序去重前快速检查是否存在相邻重复
4. **模式识别**：检测时间序列数据中的重复模式
5. **数据压缩**：识别可压缩的连续重复数据段

### 代码示例

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <string>

int main() {
    // 基本用法：查找相邻相等元素
    std::vector<int> nums = {1, 2, 3, 3, 4, 5, 6, 6, 7};
    
    auto it = std::adjacent_find(nums.begin(), nums.end());
    if (it != nums.end()) {
        std::cout << "找到相邻重复: " << *it << " 在位置 " 
                  << std::distance(nums.begin(), it) << std::endl;
    }
    
    // 查找所有相邻重复
    std::cout << "\n所有相邻重复对:" << std::endl;
    auto current = nums.begin();
    while (current != nums.end()) {
        auto found = std::adjacent_find(current, nums.end());
        if (found != nums.end()) {
            std::cout << "  值 " << *found << " 在位置 " 
                      << std::distance(nums.begin(), found) << std::endl;
            current = found + 1;
        } else {
            break;
        }
    }
    
    // 使用自定义谓词：查找差值小于2的相邻元素
    std::vector<int> data = {1, 3, 5, 8, 10, 15};
    auto pred_it = std::adjacent_find(data.begin(), data.end(),
        [](int a, int b) { return std::abs(b - a) < 2; });
    
    if (pred_it != data.end()) {
        std::cout << "\n差值小于2的相邻元素: " << *pred_it 
                  << " 和 " << *(pred_it + 1) << std::endl;
    }
    
    // 实际应用：检查连续时间戳
    std::vector<std::string> timestamps = {
        "2024-01-01", "2024-01-02", "2024-01-02", "2024-01-03"
    };
    
    auto dup = std::adjacent_find(timestamps.begin(), timestamps.end());
    if (dup != timestamps.end()) {
        std::cout << "\n警告: 发现重复时间戳: " << *dup << std::endl;
    }
    
    // 没有重复的情况
    std::vector<int> unique_nums = {1, 2, 3, 4, 5};
    auto no_dup = std::adjacent_find(unique_nums.begin(), unique_nums.end());
    std::cout << "\n无重复序列检查结果: " 
              << (no_dup == unique_nums.end() ? "无相邻重复" : "有重复") 
              << std::endl;
    
    return 0;
}
```

---

## 304. std::acos - 反余弦函数

### 功能说明

`std::acos`计算给定值的反余弦（arccosine），返回以弧度表示的角度。位于`<cmath>`头文件，是三角函数族的重要成员。

**函数原型**：
```cpp
float acos(float arg);
double acos(double arg);
long double acos(long double arg);
```

**参数说明**：
- `arg`：要计算反余弦的值，有效范围[-1.0, 1.0]

**返回值**：
- 返回[0, π]范围内的反余弦值（弧度）
- 输入越界时返回NaN

**与asin的区别**：
- `asin`返回值域：[-π/2, π/2]
- `acos`返回值域：[0, π]
- `asin(x) + acos(x) = π/2`

### 使用场景

1. **向量夹角计算**：根据点积公式计算两向量夹角：`θ = acos((a·b)/(|a||b|))`
2. **几何计算**：已知邻边和斜边求夹角
3. **机器学习**：计算余弦相似度的逆运算
4. **游戏开发**：计算角色朝向与目标的角度差
5. **机器人学**：根据位置坐标计算关节旋转角度

### 代码示例

```cpp
#include <iostream>
#include <cmath>
#include <iomanip>
#include <vector>

const double PI = 3.14159265358979323846;

struct Vec3D {
    double x, y, z;
    double length() const {
        return std::sqrt(x*x + y*y + z*z);
    }
    double dot(const Vec3D& other) const {
        return x*other.x + y*other.y + z*other.z;
    }
};

int main() {
    // 基本用法
    std::cout << "=== std::acos 基本示例 ===" << std::endl;
    std::cout << std::fixed << std::setprecision(6);
    
    double values[] = {1.0, 0.5, 0.0, -0.5, -1.0};
    for (double val : values) {
        double rad = std::acos(val);
        double deg = rad * 180.0 / PI;
        std::cout << "acos(" << std::setw(6) << val << ") = " 
                  << rad << " rad = " << deg << "°" << std::endl;
    }
    
    // 验证恒等式
    std::cout << "\n验证: asin(0.5) + acos(0.5) = π/2" << std::endl;
    double x = 0.5;
    double sum = std::asin(x) + std::acos(x);
    std::cout << "结果: " << sum << " (π/2 = " << PI/2 << ")" << std::endl;
    
    // 实际应用：计算向量夹角
    std::cout << "\n=== 向量夹角计算 ===" << std::endl;
    Vec3D v1 = {1.0, 0.0, 0.0};
    Vec3D v2 = {1.0, 1.0, 0.0};
    Vec3D v3 = {0.0, 1.0, 0.0};
    
    auto calcAngle = [](const Vec3D& a, const Vec3D& b) {
        double cos_theta = a.dot(b) / (a.length() * b.length());
        // 处理浮点误差
        cos_theta = std::max(-1.0, std::min(1.0, cos_theta));
        return std::acos(cos_theta) * 180.0 / PI;
    };
    
    std::cout << "v1与v2夹角: " << calcAngle(v1, v2) << "°" << std::endl;
    std::cout << "v1与v3夹角: " << calcAngle(v1, v3) << "°" << std::endl;
    
    // 三角形边长求角
    std::cout << "\n=== 三角形边长求角 ===" << std::endl;
    double a = 3.0, b = 4.0, c = 5.0; // 3-4-5直角三角形
    // 余弦定理: cos(C) = (a² + b² - c²) / (2ab)
    double cos_C = (a*a + b*b - c*c) / (2*a*b);
    double angle_C = std::acos(cos_C) * 180.0 / PI;
    std::cout << "边长" << a << ", " << b << ", " << c 
              << " 的夹角C = " << angle_C << "°" << std::endl;
    
    return 0;
}
```

---

## 305. std::void_t - void类型工具(C++17)

### 功能说明

`std::void_t`是C++17引入的辅助类型模板，定义于`<type_traits>`头文件。它将任意类型序列映射为`void`，是SFINAE技术和类型特征检测的核心工具。

**定义**：
```cpp
template< class... >
using void_t = void;
```

**核心用途**：
- **SFINAE条件检测**：检测类型是否具备特定成员或特性
- **类型特征萃取**：在编译期判断类型的能力
- **条件模板特化**：根据类型特征选择不同实现

**工作原理**：
当模板参数替换失败时，SFINAE原则会排除该重载，而非编译错误。`void_t`可将复杂的类型检测转化为简单的`void`返回类型判断。

### 使用场景

1. **检测成员存在性**：检查类型是否有特定成员变量或函数
2. **检测类型特征**：判断类型是否支持某些操作（如迭代、比较）
3. **条件API设计**：为不同类型提供差异化的接口
4. **静态断言**：编译期验证类型满足特定要求
5. **模板元编程**：构建复杂的类型运算和转换

### 代码示例

```cpp
#include <iostream>
#include <type_traits>
#include <string>
#include <vector>

// void_t定义（C++17之前需要自定义）
template<typename... Ts>
using void_t = void;

// 检测是否有begin()成员函数
template<typename T, typename = void>
struct has_begin : std::false_type {};

template<typename T>
struct has_begin<T, void_t<decltype(std::declval<T>().begin())>> 
    : std::true_type {};

// 检测是否有value_type类型成员
template<typename T, typename = void>
struct has_value_type : std::false_type {};

template<typename T>
struct has_value_type<T, void_t<typename T::value_type>> 
    : std::true_type {};

// 检测是否为可调用对象
template<typename T, typename = void>
struct is_callable : std::false_type {};

template<typename T>
struct is_callable<T, void_t<decltype(&T::operator())>> 
    : std::true_type {};

// 条件函数：只有对有begin()的类型才启用
template<typename T>
std::enable_if_t<has_begin<T>::value, void>
print_first(const T& container) {
    if (!container.empty()) {
        std::cout << "首元素: " << *container.begin() << std::endl;
    }
}

template<typename T>
std::enable_if_t<!has_begin<T>::value, void>
print_first(const T&) {
    std::cout << "该类型没有begin()成员" << std::endl;
}

int main() {
    std::cout << "=== std::void_t 类型检测 ===" << std::endl;
    
    // 检测std::vector
    std::cout << "std::vector<int>:" << std::endl;
    std::cout << "  has_begin: " << has_begin<std::vector<int>>::value << std::endl;
    std::cout << "  has_value_type: " << has_value_type<std::vector<int>>::value << std::endl;
    
    // 检测原生数组
    std::cout << "\nint[10]:" << std::endl;
    std::cout << "  has_begin: " << has_begin<int[10]>::value << std::endl;
    
    // 检测自定义类型
    struct MyClass {
        void foo() {}
        using value_type = int;
    };
    
    std::cout << "\nMyClass:" << std::endl;
    std::cout << "  has_value_type: " << has_value_type<MyClass>::value << std::endl;
    
    // 条件函数调用
    std::cout << "\n=== 条件函数调用 ===" << std::endl;
    std::vector<int> vec = {1, 2, 3};
    int arr[3] = {1, 2, 3};
    int x = 42;
    
    std::cout << "vector: ";
    print_first(vec);
    
    std::cout << "array: ";
    print_first(arr);
    
    std::cout << "int: ";
    print_first(x);
    
    // Lambda检测
    auto lambda = [](int a, int b) { return a + b; };
    std::cout << "\nLambda is_callable: " << is_callable<decltype(lambda)>::value << std::endl;
    
    return 0;
}
```

---

## 306. std::vector::pop_back - 向量尾部移除

### 功能说明

`std::vector::pop_back`是`std::vector`的成员函数，用于移除向量的最后一个元素。这是一个常数时间操作O(1)，不返回被移除的元素。

**函数原型**：
```cpp
void pop_back();
```

**参数**：无

**返回值**：无

**复杂度**：
- 时间复杂度：O(1)，常数时间
- 不重新分配内存，不移动其他元素

**前提条件**：
- 调用前向量必须非空，否则行为未定义
- 建议使用`empty()`检查后再调用

**异常安全**：
- 不抛出异常（noexcept）
- 即使元素析构抛出异常，也不会传播

### 使用场景

1. **栈实现**：vector作为栈容器时弹出顶部元素
2. **批处理**：处理完最后一个元素后移除
3. **撤销操作**：实现undo功能时回退最后一个操作
4. **游戏循环**：移除已出屏幕的游戏对象
5. **数据处理流**：消费队列中的数据

### 代码示例

```cpp
#include <iostream>
#include <vector>
#include <string>

int main() {
    // 基本用法
    std::vector<int> nums = {1, 2, 3, 4, 5};
    
    std::cout << "初始向量: ";
    for (int n : nums) std::cout << n << " ";
    std::cout << " (size=" << nums.size() << ")" << std::endl;
    
    // 安全地移除尾部元素
    while (!nums.empty()) {
        std::cout << "移除: " << nums.back() << ", 剩余: ";
        nums.pop_back();
        for (int n : nums) std::cout << n << " ";
        std::cout << " (size=" << nums.size() << ")" << std::endl;
    }
    
    // 实际应用：栈实现
    std::cout << "\n=== 栈实现示例 ===" << std::endl;
    std::vector<std::string> stack;
    
    // 压栈
    stack.push_back("第一帧");
    stack.push_back("第二帧");
    stack.push_back("第三帧");
    
    std::cout << "栈内容（底->顶）:" << std::endl;
    for (const auto& item : stack) {
        std::cout << "  " << item << std::endl;
    }
    
    // 弹栈
    std::cout << "\n弹栈过程:" << std::endl;
    while (!stack.empty()) {
        std::cout << "弹出: " << stack.back() << std::endl;
        stack.pop_back();
    }
    
    // 实际应用：任务队列处理
    std::cout << "\n=== 任务队列处理 ===" << std::endl;
    std::vector<std::string> tasks = {
        "下载文件", "解析数据", "生成报告", "发送邮件", "清理缓存"
    };
    
    // 后进先出（LIFO）处理
    std::cout << "LIFO处理顺序:" << std::endl;
    while (!tasks.empty()) {
        std::cout << "  处理: " << tasks.back() << std::endl;
        tasks.pop_back();
    }
    
    // 重新填充，演示FIFO
    tasks = {"任务A", "任务B", "任务C"};
    std::cout << "\nFIFO处理顺序:" << std::endl;
    while (!tasks.empty()) {
        std::cout << "  处理: " << tasks.front() << std::endl;
        tasks.erase(tasks.begin());  // FIFO需要erase，效率较低
    }
    
    return 0;
}
```

---

## 307. std::vector::insert - 向量插入元素

### 功能说明

`std::vector::insert`是`std::vector`的成员函数，用于在指定位置插入元素。支持单个元素、多个相同元素或范围插入，是vector的重要修改操作。

**函数原型**：
```cpp
// 插入单个元素
iterator insert(iterator position, const T& x);
iterator insert(iterator position, T&& x);  // C++11移动语义

// 插入n个相同元素
void insert(iterator position, size_type n, const T& x);

// 插入迭代器范围
void insert(iterator position, InputIt first, InputIt last);

// 插入初始化列表（C++11）
iterator insert(iterator position, std::initializer_list<T> il);
```

**参数说明**：
- `position`：插入位置的迭代器
- `x`：要插入的值
- `n`：插入元素个数
- `first`, `last`：要插入的范围
- `il`：初始化列表

**复杂度**：
- 线性时间O(n)，n为插入后元素数量
- 可能需要重新分配内存（引发所有迭代器失效）

### 使用场景

1. **有序插入**：维护有序vector时插入新元素
2. **批量导入**：从其他容器导入数据到指定位置
3. **数据合并**：合并多个数据源到主容器
4. **编辑功能**：文本编辑器的插入字符功能
5. **动态数组操作**：实现动态增长的数组逻辑

### 代码示例

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    // 基本用法：插入单个元素
    std::vector<int> vec = {1, 3, 4};
    
    // 在位置1插入2
    auto it = vec.begin() + 1;
    vec.insert(it, 2);
    
    std::cout << "插入单个元素后: ";
    for (int n : vec) std::cout << n << " ";
    std::cout << std::endl;
    
    // 在开头插入0
    vec.insert(vec.begin(), 0);
    std::cout << "在开头插入0: ";
    for (int n : vec) std::cout << n << " ";
    std::cout << std::endl;
    
    // 插入多个相同元素
    vec.insert(vec.begin() + 2, 3, 99);
    std::cout << "在位置2插入3个99: ";
    for (int n : vec) std::cout << n << " ";
    std::cout << std::endl;
    
    // 插入范围
    std::vector<int> source = {100, 200, 300};
    vec.insert(vec.end(), source.begin(), source.end());
    std::cout << "在末尾插入范围: ";
    for (int n : vec) std::cout << n << " ";
    std::cout << std::endl;
    
    // 插入初始化列表
    vec.insert(vec.begin(), {-1, -2, -3});
    std::cout << "在开头插入初始化列表: ";
    for (int n : vec) std::cout << n << " ";
    std::cout << std::endl;
    
    // 实际应用：有序插入
    std::cout << "\n=== 有序插入示例 ===" << std::endl;
    std::vector<int> sorted;
    int values[] = {5, 2, 8, 1, 9, 3};
    
    for (int val : values) {
        // 找到插入位置
        auto pos = std::lower_bound(sorted.begin(), sorted.end(), val);
        sorted.insert(pos, val);
        
        std::cout << "插入 " << val << " 后: ";
        for (int n : sorted) std::cout << n << " ";
        std::cout << std::endl;
    }
    
    // 实际应用：文本编辑器
    std::cout << "\n=== 文本编辑器示例 ===" << std::endl;
    std::vector<char> text = {'H', 'l', 'l', 'o'};
    std::cout << "初始文本: ";
    for (char c : text) std::cout << c;
    std::cout << std::endl;
    
    // 在位置1插入'e'
    text.insert(text.begin() + 1, 'e');
    std::cout << "插入'e'后: ";
    for (char c : text) std::cout << c;
    std::cout << std::endl;
    
    // 插入多个空格
    text.insert(text.begin() + 5, 2, ' ');
    std::cout << "插入空格后: ";
    for (char c : text) std::cout << c;
    std::cout << std::endl;
    
    // 性能提示
    std::cout << "\n性能提示:" << std::endl;
    std::cout << "- insert在末尾使用push_back更高效" << std::endl;
    std::cout << "- 频繁中间插入考虑使用list或deque" << std::endl;
    std::cout << "- insert可能使所有迭代器失效" << std::endl;
    
    return 0;
}
```

---

## 308. std::unordered_map::insert_or_assign - 插入或赋值(C++17)

### 功能说明

`std::unordered_map::insert_or_assign`是C++17引入的成员函数，结合了insert和operator[]的功能。如果键不存在则插入，存在则赋值，并返回操作结果信息。

**函数原型**：
```cpp
// 拷贝版本
std::pair<iterator, bool> insert_or_assign(const Key& k, const T& obj);

// 移动版本
std::pair<iterator, bool> insert_or_assign(const Key& k, T&& obj);
template<class K>
std::pair<iterator, bool> insert_or_assign(K&& k, T&& obj);  // 透明查找
```

**参数说明**：
- `k`：要插入或赋值的键
- `obj`：要插入或赋值的值

**返回值**：
- `pair<iterator, bool>`：迭代器指向元素，bool表示是否插入（true）或赋值（false）

**与insert的区别**：
- `insert`：键存在时不操作，返回false
- `insert_or_assign`：键存在时更新值，返回false但已修改
- `operator[]`：键不存在时默认构造，存在时返回引用

**复杂度**：平均O(1)，最坏O(n)

### 使用场景

1. **缓存更新**：更新缓存值并知道是否是新插入
2. **计数器逻辑**：初始化或递增计数器
3. **配置更新**：更新配置项并追踪变更
4. **去重统计**：统计唯一值出现次数
5. **会话管理**：创建新会话或更新现有会话

### 代码示例

```cpp
#include <iostream>
#include <unordered_map>
#include <string>

int main() {
    std::unordered_map<std::string, int> cache;
    
    // 插入新键
    auto [it1, inserted1] = cache.insert_or_assign("user1", 100);
    std::cout << "插入 " << it1->first << " = " << it1->second 
              << ", 是否新插入: " << std::boolalpha << inserted1 << std::endl;
    
    // 对现有键赋值
    auto [it2, inserted2] = cache.insert_or_assign("user1", 200);
    std::cout << "更新 " << it2->first << " = " << it2->second 
              << ", 是否新插入: " << inserted2 << std::endl;
    
    // 批量操作
    std::cout << "\n=== 批量操作示例 ===" << std::endl;
    std::unordered_map<std::string, int> scores;
    
    // 玩家得分更新
    std::string players[] = {"Alice", "Bob", "Alice", "Charlie", "Bob", "Alice"};
    int points[] = {10, 20, 15, 30, 25, 5};
    
    for (int i = 0; i < 6; ++i) {
        auto [it, inserted] = scores.insert_or_assign(players[i], 0);
        if (!inserted) {
            // 已存在，累加分数
            it->second += points[i];
            std::cout << players[i] << " 获得 " << points[i] 
                      << " 分，总分: " << it->second << std::endl;
        } else {
            // 新玩家，设置初始分
            it->second = points[i];
            std::cout << players[i] << " 加入游戏，初始分: " << points[i] << std::endl;
        }
    }
    
    std::cout << "\n最终得分:" << std::endl;
    for (const auto& [name, score] : scores) {
        std::cout << "  " << name << ": " << score << std::endl;
    }
    
    // 与insert和operator[]对比
    std::cout << "\n=== 方法对比 ===" << std::endl;
    std::unordered_map<int, std::string> map1, map2, map3;
    
    // insert: 不更新现有值
    map1.insert({1, "A"});
    map1.insert({1, "B"});  // 不生效
    std::cout << "insert后: " << map1[1] << std::endl;
    
    // operator[]: 更新但不知道是否是新插入
    map2[1] = "A";
    map2[1] = "B";
    std::cout << "operator[]后: " << map2[1] << std::endl;
    
    // insert_or_assign: 更新并知道是否新插入
    auto [it, is_new] = map3.insert_or_assign(1, "A");
    std::cout << "第一次insert_or_assign, 是否新插入: " << is_new << std::endl;
    auto [it2, is_new2] = map3.insert_or_assign(1, "B");
    std::cout << "值变为: " << it2->second << ", 是否新插入: " << is_new2 << std::endl;
    
    return 0;
}
```

---

## 309. std::unordered_map::insert - 无序映射插入

### 功能说明

`std::unordered_map::insert`是标准无序映射容器的插入操作，用于添加新的键值对。如果键已存在，插入失败并返回指向现有元素的迭代器。

**函数原型**：
```cpp
// 插入单个值
std::pair<iterator, bool> insert(const value_type& value);
std::pair<iterator, bool> insert(value_type&& value);  // C++11

// 带位置提示
iterator insert(const_iterator hint, const value_type& value);
iterator insert(const_iterator hint, value_type&& value);

// 插入范围
void insert(InputIt first, InputIt last);

// 插入初始化列表（C++11）
void insert(std::initializer_list<value_type> ilist);
```

**返回值**：
- 单元素插入：返回`pair<iterator, bool>`，iterator指向元素，bool表示是否成功插入
- 带hint插入：返回指向新插入元素的迭代器

**复杂度**：
- 平均：O(1)
- 最坏情况：O(n)，当发生哈希冲突和重哈希时

### 使用场景

1. **字典构建**：构建单词到定义的映射
2. **索引建立**：创建数据索引结构
3. **配置加载**：从文件加载键值对配置
4. **去重集合**：使用set语义存储唯一键
5. **关联数据**：建立ID到对象的关联

### 代码示例

```cpp
#include <iostream>
#include <unordered_map>
#include <string>
#include <vector>

int main() {
    std::unordered_map<int, std::string> map;
    
    // 方法1：使用value_type（pair）
    auto result1 = map.insert(std::make_pair(1, "One"));
    std::cout << "插入 {1, 'One'}: " << (result1.second ? "成功" : "失败") << std::endl;
    
    // 方法2：使用emplace（更高效）
    auto result2 = map.emplace(2, "Two");
    std::cout << "emplace {2, 'Two'}: " << (result2.second ? "成功" : "失败") << std::endl;
    
    // 方法3：使用初始化列表
    auto result3 = map.insert({3, "Three"});
    std::cout << "插入 {3, 'Three'}: " << (result3.second ? "成功" : "失败") << std::endl;
    
    // 重复键插入失败
    auto result4 = map.insert({1, "New One"});
    std::cout << "再次插入键1: " << (result4.second ? "成功" : "失败") << std::endl;
    std::cout << "键1的值: " << result4.first->second << std::endl;
    
    // 批量插入
    std::cout << "\n=== 批量插入 ===" << std::endl;
    std::vector<std::pair<int, std::string>> items = {
        {4, "Four"}, {5, "Five"}, {6, "Six"}
    };
    map.insert(items.begin(), items.end());
    
    std::cout << "批量插入后大小: " << map.size() << std::endl;
    
    // 初始化列表插入
    map.insert({{7, "Seven"}, {8, "Eight"}, {9, "Nine"}});
    std::cout << "初始化列表插入后大小: " << map.size() << std::endl;
    
    // 实际应用：构建单词频率表
    std::cout << "\n=== 单词频率统计 ===" << std::endl;
    std::unordered_map<std::string, int> word_count;
    std::string text = "the quick brown fox jumps over the lazy dog the fox";
    
    std::istringstream iss(text);
    std::string word;
    while (iss >> word) {
        auto [it, inserted] = word_count.insert({word, 1});
        if (!inserted) {
            ++it->second;  // 已存在，计数+1
        }
    }
    
    std::cout << "词频统计:" << std::endl;
    for (const auto& [w, count] : word_count) {
        std::cout << "  " << w << ": " << count << std::endl;
    }
    
    // 性能提示
    std::cout << "\n性能提示:" << std::endl;
    std::cout << "- insert失败时返回指向现有元素的迭代器" << std::endl;
    std::cout << "- 使用emplace避免不必要的拷贝" << std::endl;
    std::cout << "- hint参数可提高插入效率（如果位置正确）" << std::endl;
    
    return 0;
}
```

---

## 310. std::unordered_map::find - 无序映射查找

### 功能说明

`std::unordered_map::find`用于在无序映射中查找指定键的元素。这是unordered_map最常用的查找操作，通过哈希表实现平均O(1)的查找效率。

**函数原型**：
```cpp
iterator find(const Key& key);
const_iterator find(const Key& key) const;

template<class K>
iterator find(K&& x);  // C++20透明查找
template<class K>
const_iterator find(K&& x) const;
```

**参数说明**：
- `key`：要查找的键
- `x`：兼容类型的查找键（C++20）

**返回值**：
- 找到时：指向该键值对的迭代器
- 未找到时：返回`end()`

**复杂度**：
- 平均：O(1)，常数时间
- 最坏：O(n)，当所有键哈希到同一桶时

**与at的区别**：
- `find`：不存在的键返回end()，不抛出异常
- `at`：不存在的键抛出`out_of_range`异常
- `operator[]`：不存在的键会默认构造

### 使用场景

1. **条件查找**：检查键是否存在后再操作
2. **可选访问**：安全地获取可能存在的值
3. **存在性测试**：快速判断键是否在映射中
4. **缓存检查**：检查缓存是否命中
5. **权限验证**：检查用户是否有特定权限

### 代码示例

```cpp
#include <iostream>
#include <unordered_map>
#include <string>

int main() {
    std::unordered_map<std::string, int> scores = {
        {"Alice", 100},
        {"Bob", 85},
        {"Charlie", 92}
    };
    
    // 基本查找
    auto it = scores.find("Alice");
    if (it != scores.end()) {
        std::cout << "找到 Alice, 分数: " << it->second << std::endl;
    }
    
    // 未找到的情况
    auto not_found = scores.find("David");
    if (not_found == scores.end()) {
        std::cout << "未找到 David" << std::endl;
    }
    
    // 安全访问模式
    std::cout << "\n=== 安全访问模式 ===" << std::endl;
    std::string names[] = {"Alice", "Bob", "David", "Eve"};
    
    for (const auto& name : names) {
        auto it = scores.find(name);
        if (it != scores.end()) {
            std::cout << name << " 的分数是 " << it->second << std::endl;
        } else {
            std::cout << name << " 不在系统中" << std::endl;
        }
    }
    
    // 实际应用：配置系统
    std::cout << "\n=== 配置系统示例 ===" << std::endl;
    std::unordered_map<std::string, std::string> config = {
        {"host", "localhost"},
        {"port", "8080"},
        {"debug", "true"}
    };
    
    auto get_config = [&config](const std::string& key, 
                               const std::string& default_val) -> std::string {
        auto it = config.find(key);
        return (it != config.end()) ? it->second : default_val;
    };
    
    std::cout << "host: " << get_config("host", "127.0.0.1") << std::endl;
    std::cout << "port: " << get_config("port", "80") << std::endl;
    std::cout << "timeout: " << get_config("timeout", "30") << std::endl;
    
    // 查找后修改值
    std::cout << "\n=== 查找后修改 ===" << std::endl;
    if (auto it = scores.find("Bob"); it != scores.end()) {
        std::cout << "Bob原分数: " << it->second << std::endl;
        it->second += 5;  // 加分
        std::cout << "Bob新分数: " << it->second << std::endl;
    }
    
    // 比较：find vs operator[] vs at
    std::cout << "\n=== 方法比较 ===" << std::endl;
    
    // find：安全，不会修改容器
    if (scores.find("Zoe") == scores.end()) {
        std::cout << "find: Zoe 不存在" << std::endl;
    }
    
    // operator[]：会插入新元素
    std::cout << "operator[] 访问Zoe: " << scores["Zoe"] << std::endl;
    std::cout << "现在Zoe在容器中: " << (scores.find("Zoe") != scores.end()) << std::endl;
    
    // at：会抛出异常
    try {
        std::cout << "at 访问不存在的键: " << scores.at("Nobody") << std::endl;
    } catch (const std::out_of_range& e) {
        std::cout << "at 抛出异常: " << e.what() << std::endl;
    }
    
    return 0;
}
```

---

## 311. std::unordered_map::erase - 无序映射删除

### 功能说明

`std::unordered_map::erase`用于从unordered_map中移除元素。支持按迭代器、按键值或按范围删除，返回删除的元素数量或迭代器。

**函数原型**：
```cpp
// 按迭代器删除单个元素
iterator erase(iterator position);
iterator erase(const_iterator position);

// 按迭代器删除范围
iterator erase(const_iterator first, const_iterator last);

// 按键删除
size_type erase(const key_type& key);
```

**参数说明**：
- `position`：要删除元素的迭代器
- `first`, `last`：要删除范围的迭代器
- `key`：要删除元素的键

**返回值**：
- 迭代器版本：返回被删除元素之后的迭代器
- 键版本：返回删除的元素数量（0或1）

**复杂度**：
- 平均：O(1)
- 最坏：O(n)

**注意事项**：
- 删除后引用该元素的迭代器失效
- 不影响其他元素的迭代器（与vector不同）

### 使用场景

1. **缓存淘汰**：删除过期或最少使用的缓存项
2. **会话清理**：删除过期的用户会话
3. **数据过滤**：根据条件删除不符合要求的条目
4. **资源释放**：删除对象后释放相关资源
5. **撤销操作**：撤销添加操作时的删除

### 代码示例

```cpp
#include <iostream>
#include <unordered_map>
#include <string>

int main() {
    std::unordered_map<int, std::string> map;
    for (int i = 1; i <= 10; ++i) {
        map[i] = "Value " + std::to_string(i);
    }
    
    std::cout << "初始大小: " << map.size() << std::endl;
    
    // 方法1：按键删除
    size_t removed = map.erase(5);
    std::cout << "删除键5: " << (removed ? "成功" : "失败") 
              << ", 剩余大小: " << map.size() << std::endl;
    
    // 删除不存在的键
    removed = map.erase(99);
    std::cout << "删除键99: " << (removed ? "成功" : "失败") << std::endl;
    
    // 方法2：按迭代器删除
    auto it = map.find(3);
    if (it != map.end()) {
        auto next = map.erase(it);
        std::cout << "删除键3, 下一个元素: " 
                  << (next != map.end() ? next->first : -1) << std::endl;
    }
    
    // 方法3：遍历中安全删除（C++20前的方法）
    std::cout << "\n=== 条件删除示例 ===" << std::endl;
    std::unordered_map<std::string, int> scores = {
        {"Alice", 95}, {"Bob", 60}, {"Charlie", 45}, 
        {"David", 80}, {"Eve", 30}
    };
    
    // 删除低于及格线的学生
    for (auto it = scores.begin(); it != scores.end(); ) {
        if (it->second < 60) {
            std::cout << "删除不及格学生: " << it->first 
                      << " (" << it->second << "分)" << std::endl;
            it = scores.erase(it);  // 返回下一个有效迭代器
        } else {
            ++it;
        }
    }
    
    std::cout << "及格学生:" << std::endl;
    for (const auto& [name, score] : scores) {
        std::cout << "  " << name << ": " << score << std::endl;
    }
    
    // 实际应用：LRU缓存简单实现
    std::cout << "\n=== LRU缓存淘汰示例 ===" << std::endl;
    std::unordered_map<std::string, std::string> cache;
    cache["page1"] = "Content 1";
    cache["page2"] = "Content 2";
    cache["page3"] = "Content 3";
    
    // 模拟访问page2
    std::cout << "访问: " << cache["page2"] << std::endl;
    
    // 模拟缓存满了，删除page1（最少使用）
    if (cache.erase("page1")) {
        std::cout << "淘汰page1" << std::endl;
    }
    
    std::cout << "缓存内容:" << std::endl;
    for (const auto& [key, val] : cache) {
        std::cout << "  " << key << " => " << val << std::endl;
    }
    
    // 清空整个map
    map.clear();
    std::cout << "\n清空后大小: " << map.size() << std::endl;
    
    return 0;
}
```

---

## 312. std::unordered_map::empty - 检查无序映射是否为空

### 功能说明

`std::unordered_map::empty`是const成员函数，用于快速检查容器是否不包含任何元素。这是检查容器状态的最有效方式，时间复杂度为O(1)。

**函数原型**：
```cpp
[[nodiscard]] bool empty() const noexcept;
```

**返回值**：
- `true`：容器为空（size() == 0）
- `false`：容器包含至少一个元素

**特性**：
- 标记为`[[nodiscard]]`：调用结果不应被忽略（C++20）
- `noexcept`保证：不抛出任何异常
- O(1)时间复杂度：直接检查内部计数器

**与size()的比较**：
- `empty()`：通常更快，直接返回布尔状态
- `size()`：返回元素数量，可能需要计算
- 语义上`empty()`表达意图更清晰

### 使用场景

1. **前置条件检查**：操作前验证容器非空
2. **循环终止条件**：遍历或处理直到容器为空
3. **默认值返回**：空容器时返回默认值
4. **资源管理**：空容器时释放相关资源
5. **状态报告**：向用户报告容器状态

### 代码示例

```cpp
#include <iostream>
#include <unordered_map>
#include <string>

// 安全的pop操作（模拟栈）
template<typename K, typename V>
bool safe_pop(std::unordered_map<K, V>& map, K& key_out, V& value_out) {
    if (map.empty()) {
        return false;
    }
    auto it = map.begin();
    key_out = it->first;
    value_out = it->second;
    map.erase(it);
    return true;
}

int main() {
    // 基本用法
    std::unordered_map<int, std::string> map;
    
    std::cout << "初始状态: " << (map.empty() ? "空" : "非空") << std::endl;
    
    map[1] = "One";
    std::cout << "插入后: " << (map.empty() ? "空" : "非空") << std::endl;
    
    map.clear();
    std::cout << "清空后: " << (map.empty() ? "空" : "非空") << std::endl;
    
    // 实际应用：消息队列处理
    std::cout << "\n=== 消息队列处理 ===" << std::endl;
    std::unordered_map<int, std::string> messages;
    
    // 模拟接收消息
    messages[1001] = "用户登录";
    messages[1002] = "数据更新";
    messages[1003] = "请求处理";
    
    // 处理所有消息
    while (!messages.empty()) {
        auto it = messages.begin();
        std::cout << "处理消息 " << it->first << ": " << it->second << std::endl;
        messages.erase(it);
    }
    std::cout << "消息队列已清空" << std::endl;
    
    // 实际应用：配置验证
    std::cout << "\n=== 配置验证示例 ===" << std::endl;
    std::unordered_map<std::string, std::string> required_config = {
        {"database", "localhost"},
        {"username", "admin"},
        {"password", "secret"}
    };
    std::unordered_map<std::string, std::string> user_config;
    
    // 用户加载配置...
    user_config["database"] = "mydb";
    user_config["username"] = "user";
    // password未设置
    
    // 检查缺失的配置
    std::unordered_map<std::string, std::string> missing;
    for (const auto& [key, default_val] : required_config) {
        if (user_config.find(key) == user_config.end()) {
            missing[key] = default_val;
        }
    }
    
    if (!missing.empty()) {
        std::cout << "警告：以下配置项缺失，使用默认值:" << std::endl;
        for (const auto& [key, val] : missing) {
            std::cout << "  " << key << " = " << val << std::endl;
            user_config[key] = val;
        }
    }
    
    if (!user_config.empty()) {
        std::cout << "\n最终配置:" << std::endl;
        for (const auto& [key, val] : user_config) {
            std::cout << "  " << key << " = " << val << std::endl;
        }
    }
    
    // 性能比较
    std::cout << "\n=== empty() vs size() ===" << std::endl;
    std::cout << "推荐做法:" << std::endl;
    std::cout << "  if (map.empty()) { ... }  // 语义清晰，高效" << std::endl;
    std::cout << "  if (map.size() == 0) { ... }  // 可读性较差" << std::endl;
    std::cout << "\nempty()直接检查内部状态，不计算大小" << std::endl;
    
    return 0;
}
```

---

## 313. std::unordered_map::contains - 检查是否包含键(C++20)

### 功能说明

`std::unordered_map::contains`是C++20引入的成员函数，用于检查容器中是否存在指定的键。它比传统的`find() != end()`模式更直观、可读性更好。

**函数原型**：
```cpp
bool contains(const Key& key) const;

template<class K>
bool contains(K&& x) const;  // 透明查找，C++20
```

**参数说明**：
- `key`：要查找的键
- `x`：兼容类型的查找键（透明查找版本）

**返回值**：
- `true`：容器包含该键
- `false`：容器不包含该键

**与find的区别**：
- `contains`：返回bool，仅检查存在性
- `find`：返回迭代器，可用于访问值
- `contains`语义更明确，代码更易读

**复杂度**：平均O(1)，最坏O(n)

### 使用场景

1. **存在性检查**：只需知道键是否存在，不需要值
2. **前置条件验证**：操作前确认键已存在
3. **集合操作**：实现集合的交并差运算
4. **权限检查**：检查用户是否有某项权限
5. **缓存检查**：快速判断键是否在缓存中

### 代码示例

```cpp
#include <iostream>
#include <unordered_map>
#include <string>

// C++20之前的contains实现（兼容性代码）
template<typename Map, typename Key>
bool contains_compat(const Map& map, const Key& key) {
    return map.find(key) != map.end();
}

int main() {
    std::unordered_map<std::string, int> scores = {
        {"Alice", 100},
        {"Bob", 85},
        {"Charlie", 92}
    };
    
    // C++20的contains用法
    std::cout << "=== contains 基本用法 ===" << std::endl;
    
    if (scores.contains("Alice")) {
        std::cout << "Alice在系统中" << std::endl;
    }
    
    if (!scores.contains("David")) {
        std::cout << "David不在系统中" << std::endl;
    }
    
    // 与find方法的比较
    std::cout << "\n=== 方法比较 ===" << std::endl;
    
    // 旧方法（C++17及以前）
    bool exists_old = (scores.find("Alice") != scores.end());
    std::cout << "find方法: " << exists_old << std::endl;
    
    // C++20新方法
    bool exists_new = scores.contains("Alice");
    std::cout << "contains方法: " << exists_new << std::endl;
    
    // 实际应用：权限系统
    std::cout << "\n=== 权限系统示例 ===" << std::endl;
    std::unordered_map<std::string, std::unordered_map<std::string, bool>> permissions;
    
    // 设置权限
    permissions["admin"]["read"] = true;
    permissions["admin"]["write"] = true;
    permissions["admin"]["delete"] = true;
    permissions["user"]["read"] = true;
    permissions["user"]["write"] = false;
    
    // 检查权限
    auto check_permission = [&permissions](const std::string& role, 
                                          const std::string& action) {
        if (!permissions.contains(role)) {
            return false;  // 角色不存在
        }
        if (!permissions[role].contains(action)) {
            return false;  // 权限未定义
        }
        return permissions[role][action];
    };
    
    std::cout << "admin read: " << check_permission("admin", "read") << std::endl;
    std::cout << "user delete: " << check_permission("user", "delete") << std::endl;
    std::cout << "guest read: " << check_permission("guest", "read") << std::endl;
    
    // 实际应用：多集合操作
    std::cout << "\n=== 集合操作示例 ===" << std::endl;
    std::unordered_map<int, bool> set1, set2;
    
    // 填充集合
    for (int i = 1; i <= 5; ++i) set1[i] = true;
    for (int i = 3; i <= 7; ++i) set2[i] = true;
    
    // 交集
    std::cout << "交集: ";
    for (const auto& [val, _] : set1) {
        if (set2.contains(val)) {
            std::cout << val << " ";
        }
    }
    std::cout << std::endl;
    
    // 差集
    std::cout << "差集(set1 - set2): ";
    for (const auto& [val, _] : set1) {
        if (!set2.contains(val)) {
            std::cout << val << " ";
        }
    }
    std::cout << std::endl;
    
    // 并集
    std::cout << "并集: ";
    for (const auto& [val, _] : set1) std::cout << val << " ";
    for (const auto& [val, _] : set2) {
        if (!set1.contains(val)) std::cout << val << " ";
    }
    std::cout << std::endl;
    
    // 兼容性代码使用
    std::cout << "\n兼容性contains: " << contains_compat(scores, "Alice") << std::endl;
    
    return 0;
}
```

---

## 314. std::uninitialized_move_n - 未初始化移动n个元素

### 功能说明

`std::uninitialized_move_n`是C++17引入的内存算法，定义于`<memory>`头文件。它将n个元素从源范围移动到未初始化的目标内存，使用移动语义避免不必要的拷贝。

**函数原型**：
```cpp
template<class InputIt, class Size, class NoThrowForwardIt>
std::pair<InputIt, NoThrowForwardIt> 
uninitialized_move_n(InputIt first, Size count,
                     NoThrowForwardIt d_first);
```

**参数说明**：
- `first`：源范围的起始迭代器
- `count`：要移动的元素数量
- `d_first`：目标内存的起始位置（未初始化）

**返回值**：
- `pair`：第一个元素指向源范围尾后位置，第二个元素指向目标范围尾后位置

**与uninitialized_copy_n的区别**：
- `copy_n`：拷贝构造目标对象
- `move_n`：移动构造目标对象，源对象变为可移动但不确定状态
- 对于可移动类型（如含资源的类），move更高效

### 使用场景

1. **容器扩容**：vector扩容时移动元素到新内存
2. **内存池管理**：从内存池分配并移动构造对象
3. **数据结构实现**：实现高效的动态数组、队列
4. **资源转移**：转移大量资源所有权到新位置
5. **性能优化**：避免拷贝大型对象的深拷贝开销

### 代码示例

```cpp
#include <iostream>
#include <memory>
#include <vector>
#include <string>

class Resource {
public:
    std::string data;
    int* resource;
    
    Resource(const std::string& d) : data(d), resource(new int[100]) {
        std::cout << "构造: " << data << std::endl;
    }
    
    Resource(const Resource& other) : data(other.data), resource(new int[100]) {
        std::cout << "拷贝构造: " << data << std::endl;
        std::copy(other.resource, other.resource + 100, resource);
    }
    
    Resource(Resource&& other) noexcept 
        : data(std::move(other.data)), resource(other.resource) {
        std::cout << "移动构造: " << data << std::endl;
        other.resource = nullptr;
    }
    
    ~Resource() {
        if (resource) {
            std::cout << "析构: " << data << std::endl;
            delete[] resource;
        }
    }
};

int main() {
    // 基本用法
    std::cout << "=== 基本用法 ===" << std::endl;
    std::vector<std::string> source = {"one", "two", "three", "four", "five"};
    
    // 分配未初始化内存
    std::string* dest = static_cast<std::string*>(
        ::operator new[](sizeof(std::string) * 3));
    
    // 移动前3个元素
    auto [src_end, dest_end] = std::uninitialized_move_n(
        source.begin(), 3, dest);
    
    std::cout << "源范围新位置: " << std::distance(source.begin(), src_end) << std::endl;
    std::cout << "目标元素: ";
    for (int i = 0; i < 3; ++i) {
        std::cout << dest[i] << " ";
    }
    std::cout << std::endl;
    
    // 检查源是否被移动（对于string，应为空或原值取决于实现）
    std::cout << "源数组状态: ";
    for (const auto& s : source) {
        std::cout << "\"" << s << "\" ";
    }
    std::cout << std::endl;
    
    // 手动析构目标对象（因为operator new分配的是原始内存）
    for (int i = 0; i < 3; ++i) {
        dest[i].~string();
    }
    ::operator delete[](dest);
    
    // 实际应用：资源管理类
    std::cout << "\n=== 资源移动示例 ===" << std::endl;
    std::vector<Resource> resources;
    resources.emplace_back("Resource A");
    resources.emplace_back("Resource B");
    resources.emplace_back("Resource C");
    
    // 分配新内存
    Resource* new_memory = static_cast<Resource*>(
        ::operator new[](sizeof(Resource) * 3));
    
    std::cout << "\n开始移动..." << std::endl;
    std::uninitialized_move_n(resources.begin(), 3, new_memory);
    
    std::cout << "\n移动后新位置资源:" << std::endl;
    for (int i = 0; i < 3; ++i) {
        std::cout << "  " << new_memory[i].data << std::endl;
    }
    
    // 清理
    for (int i = 0; i < 3; ++i) {
        new_memory[i].~Resource();
    }
    ::operator delete[](new_memory);
    
    // 与uninitialized_copy_n对比
    std::cout << "\n=== 对比：copy_n vs move_n ===" << std::endl;
    std::vector<Resource> copy_source;
    copy_source.emplace_back("CopyTest");
    
    Resource* copy_dest = static_cast<Resource*>(::operator new[](sizeof(Resource)));
    Resource* move_dest = static_cast<Resource*>(::operator new[](sizeof(Resource)));
    
    std::cout << "\n使用copy_n:" << std::endl;
    std::uninitialized_copy_n(copy_source.begin(), 1, copy_dest);
    
    std::cout << "\n使用move_n:" << std::endl;
    std::uninitialized_move_n(copy_source.begin(), 1, move_dest);
    
    copy_dest->~Resource();
    move_dest->~Resource();
    ::operator delete[](copy_dest);
    ::operator delete[](move_dest);
    
    return 0;
}
```

---

## 315. std::uninitialized_fill_n - 未初始化填充n个元素

### 功能说明

`std::uninitialized_fill_n`定义于`<memory>`头文件，用于在未初始化的内存区域构造n个相同的对象。它在C++11中标准化，是内存管理的基础算法。

**函数原型**：
```cpp
template<class ForwardIt, class Size, class T>
void uninitialized_fill_n(ForwardIt first, Size count, const T& value);
```

**参数说明**：
- `first`：目标范围的起始迭代器（指向未初始化内存）
- `count`：要构造的元素数量
- `value`：用于填充的值

**返回值**：无（void）

**异常安全**：
- 如果构造过程中抛出异常，已构造的对象会被析构
- 满足基本异常安全保证

**与fill_n的区别**：
- `fill_n`：对**已初始化**的对象赋值
- `uninitialized_fill_n`：在**未初始化**内存上构造对象
- 错误混用会导致未定义行为

### 使用场景

1. **内存池初始化**：预分配内存并初始化对象池
2. **容器构造**：实现容器的resize或assign操作
3. **批量对象创建**：快速创建大量相同初始值的对象
4. **数组扩展**：动态数组扩容时初始化新槽位
5. **默认值填充**：为新分配内存设置默认值

### 代码示例

```cpp
#include <iostream>
#include <memory>
#include <string>
#include <vector>

struct Widget {
    int id;
    std::string name;
    
    Widget(int i = 0, const std::string& n = "default") 
        : id(i), name(n) {
        std::cout << "构造 Widget(" << id << ", \"" << name << "\")" << std::endl;
    }
    
    Widget(const Widget& other) : id(other.id), name(other.name) {
        std::cout << "拷贝构造 Widget(" << id << ")" << std::endl;
    }
    
    ~Widget() {
        std::cout << "析构 Widget(" << id << ")" << std::endl;
    }
};

int main() {
    // 基本用法
    std::cout << "=== 基本用法 ===" << std::endl;
    
    // 分配原始内存
    Widget* memory = static_cast<Widget*>(::operator new[](sizeof(Widget) * 5));
    
    // 使用uninitialized_fill_n构造5个相同的Widget
    Widget prototype(42, "prototype");
    std::uninitialized_fill_n(memory, 5, prototype);
    
    std::cout << "\n构造完成后的对象:" << std::endl;
    for (int i = 0; i < 5; ++i) {
        std::cout << "  [" << i << "] id=" << memory[i].id 
                  << ", name=\"" << memory[i].name << "\"" << std::endl;
    }
    
    // 手动析构（必须使用显式析构，因为内存是operator new分配的）
    std::cout << "\n手动析构..." << std::endl;
    for (int i = 0; i < 5; ++i) {
        memory[i].~Widget();
    }
    ::operator delete[](memory);
    
    // 实际应用：vector的resize实现原理
    std::cout << "\n=== vector resize 模拟 ===" << std::endl;
    
    class SimpleVector {
        int* data_;
        size_t size_;
        size_t capacity_;
        
    public:
        SimpleVector() : data_(nullptr), size_(0), capacity_(0) {}
        
        void resize(size_t new_size, int value = 0) {
            if (new_size > capacity_) {
                // 分配新内存
                int* new_data = static_cast<int*>(
                    ::operator new[](sizeof(int) * new_size));
                
                // 移动旧元素
                for (size_t i = 0; i < size_; ++i) {
                    new (new_data + i) int(std::move(data_[i]));
                    data_[i].~int();
                }
                
                // 使用uninitialized_fill_n初始化新元素
                std::uninitialized_fill_n(new_data + size_, 
                                         new_size - size_, value);
                
                ::operator delete[](data_);
                data_ = new_data;
                capacity_ = new_size;
            }
            size_ = new_size;
        }
        
        void push_back(int val) {
            resize(size_ + 1);
            data_[size_ - 1] = val;
        }
        
        void print() const {
            std::cout << "[ ";
            for (size_t i = 0; i < size_; ++i) {
                std::cout << data_[i] << " ";
            }
            std::cout << "]" << std::endl;
        }
        
        ~SimpleVector() {
            for (size_t i = 0; i < size_; ++i) {
                data_[i].~int();
            }
            ::operator delete[](data_);
        }
    };
    
    SimpleVector vec;
    vec.resize(3, 100);
    std::cout << "resize(3, 100)后: ";
    vec.print();
    
    vec.resize(6, 200);
    std::cout << "resize(6, 200)后: ";
    vec.print();
    
    // 与fill_n的区别演示
    std::cout << "\n=== fill_n vs uninitialized_fill_n ===" << std::endl;
    int arr1[3] = {1, 2, 3};  // 已初始化
    int* arr2 = static_cast<int*>(::operator new[](sizeof(int) * 3));  // 未初始化
    
    // 对已初始化数组使用fill_n（正确）
    std::fill_n(arr1, 3, 42);
    std::cout << "fill_n结果: " << arr1[0] << " " << arr1[1] << " " << arr1[2] << std::endl;
    
    // 对未初始化内存使用uninitialized_fill_n（正确）
    std::uninitialized_fill_n(arr2, 3, 42);
    std::cout << "uninitialized_fill_n结果: " << arr2[0] << " " 
              << arr2[1] << " " << arr2[2] << std::endl;
    
    ::operator delete[](arr2);
    
    return 0;
}
```

---

---

## 316. std::uninitialized_default_construct_n - 未初始化默认构造n个

### 功能说明

`std::uninitialized_default_construct_n`是C++17引入的内存算法，定义于`<memory>`头文件。它在未初始化内存上使用默认构造函数构造n个对象，支持平凡类型优化。

**函数原型**：
```cpp
template<class ForwardIt, class Size>
void uninitialized_default_construct_n(ForwardIt first, Size n);
```

**参数说明**：
- `first`：目标范围起始迭代器（未初始化内存）
- `n`：要构造的对象数量

**默认构造行为**：
- 类类型：调用默认构造函数
- 数组类型：每个元素默认构造
- 标量类型：不初始化（保持未定义值），除非提供初始化器

**与value-initialization的区别**：
- `default_construct`：不初始化标量类型
- `value_initialize`：标量类型初始化为0

### 使用场景

1. **高性能内存分配**：避免不必要的零初始化
2. **容器resize**：实现容器的默认构造resize
3. **对象池**：创建对象池时避免初始化开销
4. **延迟初始化**：分配内存后由后续逻辑初始化
5. **C++兼容层**：与C代码交互时保持数据不变

### 代码示例

```cpp
#include <iostream>
#include <memory>
#include <string>

struct Counter {
    int count;
    Counter() : count(0) {
        std::cout << "Counter默认构造, count=" << count << std::endl;
    }
};

struct PlainData {
    int x;
    int y;
    // 没有自定义构造函数，平凡类型
};

int main() {
    // 基本用法：类类型
    std::cout << "=== 类类型默认构造 ===" << std::endl;
    Counter* counters = static_cast<Counter*>(
        ::operator new[](sizeof(Counter) * 3));
    
    std::uninitialized_default_construct_n(counters, 3);
    
    std::cout << "\n构造后的值:" << std::endl;
    for (int i = 0; i < 3; ++i) {
        std::cout << "  counters[" << i << "].count = " << counters[i].count << std::endl;
    }
    
    // 清理
    for (int i = 0; i < 3; ++i) {
        counters[i].~Counter();
    }
    ::operator delete[](counters);
    
    // 实际应用：平凡类型（注意未初始化值）
    std::cout << "\n=== 平凡类型 ===" << std::endl;
    PlainData* data = static_cast<PlainData*>(
        ::operator new[](sizeof(PlainData) * 3));
    
    std::uninitialized_default_construct_n(data, 3);
    
    std::cout << "构造后的值（未定义）:" << std::endl;
    // 注意：对于平凡类型，值未定义（可能是任意值）
    for (int i = 0; i < 3; ++i) {
        std::cout << "  data[" << i << "]: x=" << data[i].x 
                  << ", y=" << data[i].y << std::endl;
    }
    
    ::operator delete[](data);
    
    // 实际应用：容器默认构造
    std::cout << "\n=== 容器实现示例 ===" << std::endl;
    
    template<typename T>
    class RawBuffer {
        T* data_;
        size_t size_;
        
    public:
        RawBuffer(size_t n) : size_(n) {
            data_ = static_cast<T*>(::operator new[](sizeof(T) * n));
            std::uninitialized_default_construct_n(data_, n);
        }
        
        T& operator[](size_t i) { return data_[i]; }
        const T& operator[](size_t i) const { return data_[i]; }
        
        ~RawBuffer() {
            for (size_t i = 0; i < size_; ++i) {
                data_[i].~T();
            }
            ::operator delete[](data_);
        }
    };
    
    // 使用示例
    RawBuffer<Counter> buffer(5);
    std::cout << "\nBuffer构造完成" << std::endl;
    std::cout << "buffer[2].count = " << buffer[2].count << std::endl;
    
    // 对比其他构造方式
    std::cout << "\n=== 构造方式对比 ===" << std::endl;
    
    // 方式1: uninitialized_default_construct_n（不初始化标量）
    int* p1 = static_cast<int*>(::operator new[](sizeof(int) * 3));
    std::uninitialized_default_construct_n(p1, 3);
    std::cout << "default_construct: " << p1[0] << " " << p1[1] << " " << p1[2] << std::endl;
    ::operator delete[](p1);
    
    // 方式2: uninitialized_value_construct_n（初始化为0，C++17）
    int* p2 = static_cast<int*>(::operator new[](sizeof(int) * 3));
    std::uninitialized_value_construct_n(p2, 3);
    std::cout << "value_construct: " << p2[0] << " " << p2[1] << " " << p2[2] << std::endl;
    ::operator delete[](p2);
    
    // 方式3: uninitialized_fill_n（填充指定值）
    int* p3 = static_cast<int*>(::operator new[](sizeof(int) * 3));
    std::uninitialized_fill_n(p3, 3, 42);
    std::cout << "fill_n: " << p3[0] << " " << p3[1] << " " << p3[2] << std::endl;
    ::operator delete[](p3);
    
    return 0;
}
```

---

## 317. std::uniform_int_distribution - 均匀整数分布

### 功能说明

`std::uniform_int_distribution`定义于`<random>`头文件，用于生成指定范围内的均匀分布整数。它是C++11随机数库的核心组件，提供高质量的随机整数。

**类定义**：
```cpp
template<class IntType = int>
class uniform_int_distribution;
```

**成员函数**：

| 函数 | 说明 |
|------|------|
| `uniform_int_distribution(IntType a, IntType b)` | 构造函数，指定[a,b]范围 |
| `a()` / `b()` | 获取分布的下界/上界 |
| `reset()` | 重置分布状态 |
| `operator()(Generator& g)` | 生成随机数 |
| `param()` | 获取/设置分布参数 |

**特性**：
- 闭区间分布：[a, b]范围内每个整数概率相等
- 支持任何整数类型（int, long, unsigned等）
- 与特定随机数引擎（如mt19937）配合使用

### 使用场景

1. **游戏开发**：掷骰子、随机事件、战利品掉落
2. **模拟仿真**：蒙特卡洛方法、随机采样
3. **测试数据生成**：生成随机测试用例
4. **密码学**：生成随机密钥（需使用加密安全随机源）
5. **负载均衡**：随机选择服务器或任务分配

### 代码示例

```cpp
#include <iostream>
#include <random>
#include <iomanip>
#include <map>

int main() {
    // 创建随机数引擎和分布
    std::random_device rd;  // 随机种子
    std::mt19937 gen(rd()); // Mersenne Twister引擎
    
    // 1. 模拟六面骰子
    std::uniform_int_distribution<> dice(1, 6);
    
    std::cout << "=== 掷骰子模拟 ===" << std::endl;
    std::cout << "掷20次: ";
    for (int i = 0; i < 20; ++i) {
        std::cout << dice(gen) << " ";
    }
    std::cout << std::endl;
    
    // 2. 分布统计验证
    std::cout << "\n=== 分布统计 ===" << std::endl;
    std::map<int, int> stats;
    for (int i = 0; i < 10000; ++i) {
        ++stats[dice(gen)];
    }
    
    std::cout << "点数分布（10000次）:" << std::endl;
    for (const auto& [face, count] : stats) {
        double percent = 100.0 * count / 10000;
        std::cout << "  " << face << ": " << std::setw(4) << count 
                  << " (" << std::fixed << std::setprecision(2) 
                  << percent << "%)" << std::endl;
    }
    
    // 3. 不同范围的分布
    std::cout << "\n=== 不同范围的随机数 ===" << std::endl;
    
    // 随机布尔值
    std::uniform_int_distribution<> coin(0, 1);
    std::cout << "抛硬币10次: ";
    for (int i = 0; i < 10; ++i) {
        std::cout << (coin(gen) ? "正" : "反") << " ";
    }
    std::cout << std::endl;
    
    // 百分数（0-100）
    std::uniform_int_distribution<> percent(0, 100);
    std::cout << "随机百分数: " << percent(gen) << "%" << std::endl;
    
    // ASCII字符（32-126是可打印字符）
    std::uniform_int_distribution<> ascii(32, 126);
    std::cout << "随机字符: '" << static_cast<char>(ascii(gen)) << "'" << std::endl;
    
    // 4. 实际应用：随机抽奖
    std::cout << "\n=== 抽奖系统 ===" << std::endl;
    std::vector<std::string> participants = {
        "Alice", "Bob", "Charlie", "David", "Eve", 
        "Frank", "Grace", "Henry"
    };
    
    std::uniform_int_distribution<> winner_dist(0, participants.size() - 1);
    
    std::cout << "参与者: ";
    for (const auto& name : participants) {
        std::cout << name << " ";
    }
    std::cout << std::endl;
    
    std::cout << "中奖者: " << participants[winner_dist(gen)] << std::endl;
    
    // 5. 实际应用：洗牌算法
    std::cout << "\n=== 洗牌算法 ===" << std::endl;
    std::vector<int> deck;
    for (int i = 1; i <= 10; ++i) deck.push_back(i);
    
    std::cout << "原始顺序: ";
    for (int card : deck) std::cout << card << " ";
    std::cout << std::endl;
    
    // Fisher-Yates洗牌
    for (int i = deck.size() - 1; i > 0; --i) {
        std::uniform_int_distribution<> dist(0, i);
        std::swap(deck[i], deck[dist(gen)]);
    }
    
    std::cout << "洗牌后: ";
    for (int card : deck) std::cout << card << " ";
    std::cout << std::endl;
    
    // 6. 多线程安全：每个线程独立引擎
    std::cout << "\n注意：随机数引擎不是线程安全的" << std::endl;
    std::cout << "多线程应使用线程本地存储或互斥锁" << std::endl;
    
    return 0;
}
```

---

## 318. std::tolower - 转小写字符

### 功能说明

`std::tolower`定义于`<cctype>`（C风格）或`<locale>`（C++locale版本），用于将字符转换为小写形式。C++版本支持本地化，根据当前locale进行转换。

**函数原型**：
```cpp
// C风格（<cctype>）
int tolower(int ch);

// C++ locale版本（<locale>）
template<class charT>
charT tolower(charT ch, const locale& loc);
```

**参数说明**：
- `ch`：要转换的字符（unsigned char可表示范围或EOF）
- `loc`：locale对象，指定本地化规则

**返回值**：
- 可转换时：返回对应的小写字符
- 不可转换时：原样返回输入字符

**重要注意**：
- C风格版本传入char时必须先转为unsigned char
- 只对当前C locale（通常是"C"）中的字符有效
- 多语言环境需使用C++ locale版本

### 使用场景

1. **字符串比较**：不区分大小写的字符串匹配
2. **输入规范化**：将用户输入转为小写统一处理
3. **标识符处理**：变量名、命令名的大小写统一
4. **数据清洗**：清理数据中的大小写不一致
5. **搜索功能**：实现大小写不敏感的搜索

### 代码示例

```cpp
#include <iostream>
#include <cctype>      // C风格tolower
#include <locale>      // C++ locale版本
#include <string>
#include <algorithm>
#include <vector>

// 安全的C风格tolower（正确处理char）
char safe_tolower(char ch) {
    return static_cast<char>(std::tolower(static_cast<unsigned char>(ch)));
}

// 字符串转小写（C风格）
std::string to_lower_c(const std::string& str) {
    std::string result;
    result.reserve(str.size());
    for (char c : str) {
        result += safe_tolower(c);
    }
    return result;
}

// 字符串转小写（C++ locale版本）
std::string to_lower_cpp(const std::string& str, const std::locale& loc) {
    std::string result;
    result.reserve(str.size());
    for (char c : str) {
        result += std::tolower(c, loc);
    }
    return result;
}

int main() {
    // 基本用法
    std::cout << "=== C风格 tolower ===" << std::endl;
    char upper[] = "HELLO WORLD 123 !@#";
    
    std::cout << "原始: " << upper << std::endl;
    std::cout << "小写: ";
    for (char c : upper) {
        std::cout << safe_tolower(c);
    }
    std::cout << std::endl;
    
    // 处理特殊情况
    std::cout << "\n=== 特殊字符处理 ===" << std::endl;
    std::vector<char> chars = {'A', 'a', '1', '@', '\x80', -1};
    
    for (char c : chars) {
        char lowered = safe_tolower(c);
        std::cout << "字符 " << (int)c << " (" << c << ") -> " 
                  << (int)lowered << " (" << lowered << ")" << std::endl;
    }
    
    // 实际应用：不区分大小写比较
    std::cout << "\n=== 不区分大小写比较 ===" << std::endl;
    std::string str1 = "HelloWorld";
    std::string str2 = "helloworld";
    std::string str3 = "HELLOWORLD";
    
    auto case_insensitive_equal = [](const std::string& a, const std::string& b) {
        if (a.size() != b.size()) return false;
        for (size_t i = 0; i < a.size(); ++i) {
            if (safe_tolower(a[i]) != safe_tolower(b[i])) {
                return false;
            }
        }
        return true;
    };
    
    std::cout << str1 << " == " << str2 << ": " 
              << case_insensitive_equal(str1, str2) << std::endl;
    std::cout << str1 << " == " << str3 << ": " 
              << case_insensitive_equal(str1, str3) << std::endl;
    
    // 实际应用：命令解析
    std::cout << "\n=== 命令解析示例 ===" << std::endl;
    auto parse_command = [](const std::string& cmd) {
        std::string lower = to_lower_c(cmd);
        if (lower == "help" || lower == "h") return "显示帮助";
        if (lower == "quit" || lower == "q" || lower == "exit") return "退出程序";
        if (lower == "save" || lower == "s") return "保存文件";
        return "未知命令";
    };
    
    std::vector<std::string> commands = {"HELP", "Quit", "SAVE", "ExIt", "UNKNOWN"};
    for (const auto& cmd : commands) {
        std::cout << "命令 \"" << cmd << "\": " << parse_command(cmd) << std::endl;
    }
    
    // 使用transform转换整个字符串
    std::cout << "\n=== 使用std::transform ===" << std::endl;
    std::string text = "ThIs Is MiXeD CaSe TeXt";
    std::transform(text.begin(), text.end(), text.begin(), safe_tolower);
    std::cout << "转换后: " << text << std::endl;
    
    // 多语言处理（C++ locale版本）
    std::cout << "\n=== C++ locale版本 ===" << std::endl;
    std::locale current_locale("");  // 使用系统默认locale
    std::string german = "\xC4\xD6\xDC"; // ÄÖÜ (German)
    std::cout << "德语大写: " << german << std::endl;
    std::cout << "转小写: " << to_lower_cpp(german, current_locale) << std::endl;
    
    // 注意：C风格tolower对多字节字符（如UTF-8）可能无法正确处理
    std::cout << "\n注意：C风格tolower只处理单字节字符" << std::endl;
    std::cout << "处理UTF-8等多字节编码需要专门的库" << std::endl;
    
    return 0;
}
```

---

## 319. std::tmpnam - 生成临时文件名

### 功能说明

`std::tmpnam`定义于`<cstdio>`头文件，用于生成唯一的临时文件名。它创建一个不与任何现有文件冲突的文件名字符串，可用于创建临时文件。

**函数原型**：
```cpp
char* tmpnam(char* filename);
```

**参数说明**：
- `filename`：指向字符数组的指针，用于存储生成的文件名
- 如果为nullptr，返回指向内部静态缓冲区的指针

**返回值**：
- 成功时：指向包含文件名的字符串
- 失败时：返回nullptr

**文件名特点**：
- 格式通常包含进程ID和时间戳确保唯一性
- 生成名称后立即创建文件可能仍冲突（race condition）
- 线程不安全（依赖静态缓冲区）

**安全风险**：
- 存在时间检查攻击风险（TOCTOU）
- 建议改用C++17的`std::filesystem`或操作系统API

### 使用场景

1. **临时数据处理**：创建临时文件存储中间结果
2. **进程间通信**：通过临时文件传递数据
3. **备份生成**：生成唯一的备份文件名
4. **测试文件**：单元测试中创建隔离的测试文件
5. **日志轮转**：生成带时间戳的日志文件名

### 代码示例

```cpp
#include <iostream>
#include <cstdio>
#include <fstream>
#include <string>
#include <vector>

// 更安全的临时文件生成（C++17推荐）
#include <filesystem>
namespace fs = std::filesystem;

std::string create_temp_file_cpp17(const std::string& prefix = "temp") {
    fs::path temp_dir = fs::temp_directory_path();
    fs::path temp_file = temp_dir / (prefix + "_" + std::to_string(std::time(nullptr)));
    
    // 确保唯一性
    int counter = 0;
    while (fs::exists(temp_file)) {
        temp_file = temp_dir / (prefix + "_" + 
                               std::to_string(std::time(nullptr)) + 
                               "_" + std::to_string(counter++));
    }
    
    return temp_file.string();
}

int main() {
    // 传统tmpnam用法（不推荐但展示）
    std::cout << "=== std::tmpnam 基本用法 ===" << std::endl;
    
    char filename[L_tmpnam];  // L_tmpnam是所需缓冲区大小
    
    if (std::tmpnam(filename) != nullptr) {
        std::cout << "生成的临时文件名: " << filename << std::endl;
    } else {
        std::cout << "生成文件名失败" << std::endl;
    }
    
    // 生成多个临时文件名
    std::cout << "\n生成5个临时文件名:" << std::endl;
    for (int i = 0; i < 5; ++i) {
        char fname[L_tmpnam];
        if (std::tmpnam(fname) != nullptr) {
            std::cout << "  " << i + 1 << ": " << fname << std::endl;
        }
    }
    
    // 使用临时文件
    std::cout << "\n=== 使用临时文件 ===" << std::endl;
    char temp_name[L_tmpnam];
    if (std::tmpnam(temp_name) != nullptr) {
        std::cout << "创建临时文件: " << temp_name << std::endl;
        
        // 写入数据
        std::ofstream file(temp_name);
        if (file.is_open()) {
            file << "这是临时数据" << std::endl;
            file << "行2: 更多数据" << std::endl;
            file.close();
            std::cout << "数据已写入" << std::endl;
            
            // 读取并显示
            std::ifstream read_file(temp_name);
            std::string line;
            std::cout << "文件内容:" << std::endl;
            while (std::getline(read_file, line)) {
                std::cout << "  " << line << std::endl;
            }
            read_file.close();
            
            // 清理
            std::remove(temp_name);
            std::cout << "临时文件已删除" << std::endl;
        }
    }
    
    // C++17更安全的方法
    std::cout << "\n=== C++17更安全的方法 ===" << std::endl;
    try {
        fs::path temp_path = fs::temp_directory_path() / "myapp_temp";
        
        // 创建唯一的临时目录
        fs::create_directories(temp_path);
        std::cout << "临时目录: " << temp_path << std::endl;
        
        // 创建临时文件
        fs::path temp_file = temp_path / "data.txt";
        {
            std::ofstream file(temp_file);
            file << "C++17方式创建的临时数据" << std::endl;
        }
        std::cout << "临时文件: " << temp_file << std::endl;
        
        // RAII清理
        fs::remove_all(temp_path);
        std::cout << "临时目录已清理" << std::endl;
    } catch (const fs::filesystem_error& e) {
        std::cout << "文件系统错误: " << e.what() << std::endl;
    }
    
    // 安全警告
    std::cout << "\n=== 安全警告 ===" << std::endl;
    std::cout << "tmpnam存在以下问题:" << std::endl;
    std::cout << "1. 线程不安全（使用静态缓冲区）" << std::endl;
    std::cout << "2. 可能产生竞争条件（文件名生成到创建文件之间）" << std::endl;
    std::cout << "3. 文件名可能不符合所有系统要求" << std::endl;
    std::cout << "\n替代方案:" << std::endl;
    std::cout << "- C++17 std::filesystem" << std::endl;
    std::cout << "- std::tmpfile（直接创建文件）" << std::endl;
    std::cout << "- 操作系统特定API（如mkstemp）" << std::endl;
    
    return 0;
}
```

---

## 320. std::this_thread::yield - 线程让出CPU

### 功能说明

`std::this_thread::yield`定义于`<thread>`头文件，用于提示操作系统当前线程愿意让出CPU时间片，让其他线程执行。它不会阻塞线程，只是建议调度器进行线程切换。

**函数原型**：
```cpp
void yield() noexcept;
```

**参数**：无

**返回值**：无

**行为特性**：
- 仅提示调度器，不保证一定切换线程
- 不同平台实现不同（可能是空操作）
- 不释放任何锁或资源
- 适用于忙等待循环的优化

**与sleep的区别**：
- `yield`：立即返回，仅提示让出CPU
- `sleep_for`：阻塞指定时长，线程进入等待状态

### 使用场景

1. **忙等待优化**：自旋锁等忙等待场景减少CPU占用
2. **负载均衡**：让出CPU让同优先级线程执行
3. **协作式多任务**：主动让出控制权
4. **性能微调**：在多线程竞争场景优化调度
5. **调试辅助**：强制线程切换暴露竞态条件

### 代码示例

```cpp
#include <iostream>
#include <thread>
#include <atomic>
#include <mutex>
#include <chrono>

// 自旋锁实现（使用yield优化）
class SpinLock {
    std::atomic<bool> locked_{false};
    
public:
    void lock() {
        // 自旋等待
        while (locked_.exchange(true, std::memory_order_acquire)) {
            // 让出CPU，减少忙等待开销
            std::this_thread::yield();
        }
    }
    
    void unlock() {
        locked_.store(false, std::memory_order_release);
    }
};

// 共享资源
int shared_data = 0;
SpinLock spinlock;

void worker_spinlock(int id, int iterations) {
    for (int i = 0; i < iterations; ++i) {
        spinlock.lock();
        // 临界区
        ++shared_data;
        spinlock.unlock();
    }
    std::cout << "线程 " << id << " 完成" << std::endl;
}

// 任务队列（使用yield优化）
std::atomic<bool> task_ready{false};

void producer() {
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    std::cout << "生产者：准备任务..." << std::endl;
    task_ready = true;
}

void consumer() {
    std::cout << "消费者：等待任务..." << std::endl;
    
    // 忙等待，使用yield优化
    int spin_count = 0;
    while (!task_ready.load(std::memory_order_acquire)) {
        ++spin_count;
        if (spin_count % 1000 == 0) {
            std::this_thread::yield();  // 让出CPU
        }
    }
    
    std::cout << "消费者：任务已就绪（自旋了 " << spin_count << " 次）" << std::endl;
}

int main() {
    std::cout << "=== yield在自旋锁中的应用 ===" << std::endl;
    
    const int num_threads = 4;
    const int iterations = 10000;
    
    std::thread threads[num_threads];
    
    auto start = std::chrono::steady_clock::now();
    
    for (int i = 0; i < num_threads; ++i) {
        threads[i] = std::thread(worker_spinlock, i, iterations);
    }
    
    for (auto& t : threads) {
        t.join();
    }
    
    auto end = std::chrono::steady_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    
    std::cout << "最终共享数据: " << shared_data << std::endl;
    std::cout << "耗时: " << duration.count() << " ms" << std::endl;
    
    // 生产者-消费者示例
    std::cout << "\n=== 生产者-消费者示例 ===" << std::endl;
    std::thread prod(producer);
    std::thread cons(consumer);
    
    prod.join();
    cons.join();
    
    // 性能对比：有yield vs 无yield
    std::cout << "\n=== yield性能影响 ===" << std::endl;
    std::cout << "有yield的自旋等待:" << std::endl;
    std::cout << "  优点: 减少CPU占用，允许其他线程执行" << std::endl;
    std::cout << "  缺点: 可能增加延迟（上下文切换开销）" << std::endl;
    std::cout << "\n使用建议:" << std::endl;
    std::cout << "  - 短时间等待: 纯自旋（无yield）" << std::endl;
    std::cout << "  - 中等等待: 自旋+yield（如本示例）" << std::endl;
    std::cout << "  - 长时间等待: 使用条件变量或sleep" << std::endl;
    
    return 0;
}
```

---

## 321. std::this_thread::sleep_for - 线程睡眠

### 功能说明

`std::this_thread::sleep_for`定义于`<thread>`头文件，用于阻塞当前线程指定的时间。它是实现延迟执行、速率控制的主要机制。

**函数原型**：
```cpp
template<class Rep, class Period>
void sleep_for(const std::chrono::duration<Rep, Period>& sleep_duration);
```

**参数说明**：
- `sleep_duration`：睡眠时间，使用`std::chrono::duration`表示

**常用时间单位**：
- `std::chrono::nanoseconds` - 纳秒
- `std::chrono::microseconds` - 微秒
- `std::chrono::milliseconds` - 毫秒
- `std::chrono::seconds` - 秒
- `std::chrono::minutes` - 分钟
- `std::chrono::hours` - 小时

**返回值**：无

**阻塞特性**：
- 线程进入睡眠状态，不占用CPU
- 睡眠时间至少为指定时长（可能更长）
- 可能被信号中断（在某些平台上）

### 使用场景

1. **速率限制**：控制循环执行频率
2. **超时等待**：实现超时逻辑
3. **动画控制**：控制动画帧率
4. **轮询间隔**：轮询操作间添加延迟
5. **任务调度**：周期性任务执行

### 代码示例

```cpp
#include <iostream>
#include <thread>
#include <chrono>
#include <atomic>
#include <iomanip>

int main() {
    using namespace std::chrono;
    
    // 基本用法
    std::cout << "=== 基本睡眠示例 ===" << std::endl;
    
    std::cout << "开始..." << std::endl;
    auto start = std::chrono::steady_clock::now();
    
    std::this_thread::sleep_for(std::chrono::seconds(1));
    
    auto end = std::chrono::steady_clock::now();
    auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    std::cout << "睡眠结束，实际耗时: " << elapsed.count() << " ms" << std::endl;
    
    // 不同时间单位
    std::cout << "\n=== 不同时间单位 ===" << std::endl;
    
    std::cout << "睡眠100毫秒..." << std::endl;
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    
    std::cout << "睡眠500微秒..." << std::endl;
    std::this_thread::sleep_for(std::chrono::microseconds(500));
    
    std::cout << "睡眠1纳秒（可能不生效）..." << std::endl;
    std::this_thread::sleep_for(std::chrono::nanoseconds(1));
    
    // 实际应用：进度条
    std::cout << "\n=== 进度条示例 ===" << std::endl;
    const int total = 50;
    std::cout << "进度: [" << std::string(total, ' ') << "] 0%" << std::flush;
    
    for (int i = 0; i <= total; ++i) {
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
        
        int percent = (i * 100) / total;
        std::cout << "\r进度: [" << std::string(i, '=') 
                  << std::string(total - i, ' ') << "] " 
                  << percent << "%" << std::flush;
    }
    std::cout << std::endl;
    
    // 实际应用：速率限制
    std::cout << "\n=== 速率限制示例 ===" << std::endl;
    const int requests_per_second = 5;
    auto interval = std::chrono::milliseconds(1000 / requests_per_second);
    
    for (int i = 1; i <= 10; ++i) {
        auto req_start = std::chrono::steady_clock::now();
        
        // 模拟请求处理
        std::cout << "处理请求 " << i << std::endl;
        
        // 等待到下一个时间点
        std::this_thread::sleep_until(req_start + interval);
    }
    
    // 实际应用：心跳机制
    std::cout << "\n=== 心跳机制示例 ===" << std::endl;
    std::atomic<bool> running{true};
    
    std::thread heartbeat([&running]() {
        int count = 0;
        while (running) {
            std::cout << "心跳 #" << ++count << std::endl;
            std::this_thread::sleep_for(std::chrono::seconds(1));
        }
        std::cout << "心跳停止" << std::endl;
    });
    
    // 主线程执行5秒
    std::this_thread::sleep_for(std::chrono::seconds(5));
    running = false;
    heartbeat.join();
    
    // 注意事项
    std::cout << "\n=== 注意事项 ===" << std::endl;
    std::cout << "1. 睡眠精度取决于操作系统和硬件" << std::endl;
    std::cout << "2. 实际睡眠时间 >= 请求时间" << std::endl;
    std::cout << "3. 高精度定时考虑使用忙等待+睡眠混合" << std::endl;
    std::cout << "4. 长时间睡眠应检查中断条件" << std::endl;
    
    return 0;
}
```

---

---

## 322. std::terminate - 终止程序

### 功能说明

`std::terminate`定义于`<exception>`头文件，用于立即终止程序执行。它通常在标准库检测到无法处理的异常（如未捕获的异常）时被调用，但也可以显式调用。

**函数原型**：
```cpp
[[noreturn]] void terminate() noexcept;
```

**参数**：无

**返回值**：无（不返回）

**默认行为**：
- 调用`std::abort()`，立即终止程序
- 可能生成核心转储（取决于实现）
- 不调用任何析构函数

**自定义终止处理程序**：
```cpp
std::terminate_handler set_terminate(std::terminate_handler f) noexcept;
```

### 使用场景

1. **致命错误处理**：遇到不可恢复的错误时退出
2. **未捕获异常**：作为未捕获异常的最后手段
3. **安全退出**：在安全关键系统中快速失败
4. **调试支持**：生成核心转储进行调试
5. **契约违反**：前置/后置条件违反时的处理

### 代码示例

```cpp
#include <iostream>
#include <exception>
#include <cstdlib>

// 自定义终止处理程序
void custom_terminate_handler() {
    std::cerr << "自定义终止处理程序被调用!" << std::endl;
    // 可以在这里记录日志、发送警报等
    std::abort();  // 必须调用abort或exit，否则未定义行为
}

// 可能抛出异常的函数
void risky_function(bool should_throw) {
    if (should_throw) {
        throw std::runtime_error("发生了错误!");
    }
    std::cout << "函数正常执行" << std::endl;
}

// 带noexcept的函数
void noexcept_function(bool should_throw) noexcept {
    if (should_throw) {
        throw std::runtime_error("noexcept函数中抛出了异常!");
    }
}

class CriticalResource {
public:
    ~CriticalResource() {
        std::cout << "CriticalResource析构函数" << std::endl;
    }
};

int main() {
    // 设置自定义终止处理程序
    std::set_terminate(custom_terminate_handler);
    
    std::cout << "=== std::terminate 示例 ===" << std::endl;
    
    // 场景1: 显式调用terminate
    std::cout << "\n场景1: 显式调用terminate" << std::endl;
    bool run_terminate = false;  // 设置为true来测试
    
    if (run_terminate) {
        std::cout << "即将调用terminate..." << std::endl;
        std::terminate();  // 程序将在这里终止
        std::cout << "这行不会执行" << std::endl;
    }
    
    // 场景2: noexcept函数中抛出异常
    std::cout << "\n场景2: noexcept函数中的异常" << std::endl;
    bool run_noexcept = false;  // 设置为true来测试
    
    if (run_noexcept) {
        std::cout << "调用noexcept函数并抛出异常..." << std::endl;
        noexcept_function(true);  // 将导致terminate
    }
    
    // 场景3: 未捕获的异常
    std::cout << "\n场景3: 未捕获的异常" << std::endl;
    bool run_uncaught = false;  // 设置为true来测试
    
    if (run_uncaught) {
        std::cout << "抛出未捕获的异常..." << std::endl;
        risky_function(true);  // 将导致terminate
    }
    
    // 场景4: 使用try-catch正确捕获
    std::cout << "\n场景4: 正确异常处理" << std::endl;
    try {
        risky_function(true);
    } catch (const std::exception& e) {
        std::cout << "捕获异常: " << e.what() << std::endl;
    }
    
    // 场景5: terminate不调用析构函数
    std::cout << "\n场景5: 资源清理行为" << std::endl;
    bool run_resource = false;  // 设置为true来测试
    
    if (run_resource) {
        CriticalResource resource;  // 创建资源
        std::cout << "资源已创建，即将terminate..." << std::endl;
        std::terminate();  // 不会调用resource的析构函数!
    }
    
    // 安全的错误处理方式
    std::cout << "\n=== 推荐的错误处理 ===" << std::endl;
    std::cout << "1. 使用异常处理（try-catch）" << std::endl;
    std::cout << "2. 返回错误码" << std::endl;
    std::cout << "3. 使用std::optional或std::expected (C++23)" << std::endl;
    std::cout << "4. 仅在不可恢复错误时使用terminate" << std::endl;
    
    // 测试自定义处理程序
    std::cout << "\n当前终止处理程序: " 
              << (std::set_terminate(custom_terminate_handler) ? "已设置" : "默认")
              << std::endl;
    
    return 0;
}
```

---

## 323. std::strncmp - 比较前n个字符

### 功能说明

`std::strncmp`定义于`<cstring>`头文件，用于比较两个C风格字符串的前n个字符。它是C标准库函数`strncmp`的C++封装，提供安全的长度受限的字符串比较。

**函数原型**：
```cpp
int strncmp(const char* lhs, const char* rhs, size_t count);
```

**参数说明**：
- `lhs`, `rhs`：要比较的C字符串
- `count`：最多比较的字符数

**返回值**：
- `< 0`：`lhs`小于`rhs`
- `== 0`：`lhs`等于`rhs`
- `> 0`：`lhs`大于`rhs`

**比较规则**：
- 按字典序比较（基于字符的ASCII值）
- 遇到null字符或比较完count个字符后停止
- 区分大小写

**与strcmp的区别**：
- `strcmp`：比较整个字符串，直到遇到null字符
- `strncmp`：最多比较n个字符，更安全（防止缓冲区溢出）

### 使用场景

1. **前缀匹配**：检查字符串前缀是否匹配
2. **安全比较**：避免缓冲区溢出攻击
3. **固定长度字段**：比较固定宽度数据字段
4. **协议解析**：解析固定长度协议字段
5. **版本比较**：比较版本号前缀

### 代码示例

```cpp
#include <iostream>
#include <cstring>
#include <string>
#include <vector>

int main() {
    // 基本用法
    std::cout << "=== 基本用法 ===" << std::endl;
    
    const char* str1 = "Hello World";
    const char* str2 = "Hello C++";
    const char* str3 = "Hello World!";
    
    // 比较前5个字符（相等）
    int result1 = std::strncmp(str1, str2, 5);
    std::cout << "strncmp(\"" << str1 << "\", \"" << str2 << "\", 5) = " 
              << result1 << std::endl;
    
    // 比较前6个字符（不等）
    int result2 = std::strncmp(str1, str2, 6);
    std::cout << "strncmp(\"" << str1 << "\", \"" << str2 << "\", 6) = " 
              << result2 << std::endl;
    
    // 比较前11个字符（str1结束）
    int result3 = std::strncmp(str1, str3, 12);
    std::cout << "strncmp(\"" << str1 << "\", \"" << str3 << "\", 12) = " 
              << result3 << std::endl;
    
    // 实际应用：前缀匹配
    std::cout << "\n=== 前缀匹配 ===" << std::endl;
    const char* commands[] = {"help", "hello", "history", "exit", "echo"};
    const char* prefix = "he";
    
    std::cout << "前缀 \"" << prefix << "\" 匹配的命令:" << std::endl;
    for (const char* cmd : commands) {
        if (std::strncmp(cmd, prefix, std::strlen(prefix)) == 0) {
            std::cout << "  " << cmd << std::endl;
        }
    }
    
    // 实际应用：HTTP协议解析
    std::cout << "\n=== HTTP协议解析 ===" << std::endl;
    const char* http_request = "GET /index.html HTTP/1.1\r\n";
    
    if (std::strncmp(http_request, "GET ", 4) == 0) {
        std::cout << "GET请求" << std::endl;
    } else if (std::strncmp(http_request, "POST ", 5) == 0) {
        std::cout << "POST请求" << std::endl;
    }
    
    // 检查HTTP版本
    const char* version = std::strstr(http_request, "HTTP/");
    if (version && std::strncmp(version, "HTTP/1.1", 8) == 0) {
        std::cout << "HTTP/1.1版本" << std::endl;
    }
    
    // 实际应用：版本号比较
    std::cout << "\n=== 版本号比较 ===" << std::endl;
    auto compare_version = [](const char* v1, const char* v2) {
        const char* p1 = v1;
        const char* p2 = v2;
        
        while (*p1 && *p2) {
            // 跳过非数字字符
            while (*p1 && !std::isdigit(*p1)) ++p1;
            while (*p2 && !std::isdigit(*p2)) ++p2;
            
            // 提取数字部分
            int n1 = 0, n2 = 0;
            while (*p1 && std::isdigit(*p1)) {
                n1 = n1 * 10 + (*p1 - '0');
                ++p1;
            }
            while (*p2 && std::isdigit(*p2)) {
                n2 = n2 * 10 + (*p2 - '0');
                ++p2;
            }
            
            if (n1 != n2) return n1 - n2;
        }
        return *p1 - *p2;
    };
    
    const char* versions[] = {"1.0.0", "1.0.1", "1.2.0", "2.0.0"};
    std::cout << "版本比较:" << std::endl;
    for (size_t i = 0; i < 3; ++i) {
        int cmp = compare_version(versions[i], versions[i+1]);
        std::cout << "  " << versions[i] << " vs " << versions[i+1] 
                  << ": " << (cmp < 0 ? "<" : cmp > 0 ? ">" : "=") << std::endl;
    }
    
    // strncmp vs strcmp安全性对比
    std::cout << "\n=== 安全性对比 ===" << std::endl;
    char buf1[10] = "Hello";
    char buf2[100] = "Hello World! This is a very long string";
    
    // strncmp安全（指定长度）
    int safe = std::strncmp(buf1, buf2, 10);
    std::cout << "strncmp(有限长度): 安全" << std::endl;
    
    // strcmp危险（可能越界）
    // int unsafe = std::strcmp(buf1, buf2);  // 未定义行为!
    
    std::cout << "\n注意：strncmp在C++中通常被std::string::compare取代" << std::endl;
    std::cout << "但处理C字符串和底层数据时仍然有用" << std::endl;
    
    return 0;
}
```

---

## 324. std::strings - 非标准/可能为误用 ⚠️

### 重要说明

`std::strings` **不是C++标准库中的组件**。这很可能是以下情况之一：

1. **拼写错误**：用户可能想使用 `std::string`（单数）
2. **第三方库**：某些库可能定义了strings类
3. **混淆概念**：可能混淆了C#的`System.Collections.Generic.List<string>`等
4. **非标准扩展**：某些编译器可能提供非标准扩展

### 正确的替代方案

```cpp
#include <string>
#include <vector>
#include <array>
#include <list>

// 方案1: std::string - 标准字符串类
std::string s = "Hello";

// 方案2: std::vector<std::string> - 字符串数组
std::vector<std::string> strings = {"Hello", "World", "C++"};

// 方案3: std::array<std::string, N> - 固定大小字符串数组
std::array<std::string, 3> fixed_strings = {"A", "B", "C"};

// 方案4: std::list<std::string> - 字符串链表
std::list<std::string> string_list = {"Item1", "Item2"};

// 方案5: 原始字符串数组（C风格）
const char* c_strings[] = {"C", "Style", "Strings"};
```

### 标准字符串容器选择指南

| 需求 | 推荐容器 |
|------|----------|
| 单个字符串 | `std::string` |
| 动态字符串数组 | `std::vector<std::string>` |
| 固定数量字符串 | `std::array<std::string, N>` |
| 频繁插入删除 | `std::list<std::string>` 或 `std::deque<std::string>` |

### 代码示例（正确使用）

```cpp
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

int main() {
    // 使用std::vector<std::string>作为"字符串列表"
    std::vector<std::string> strings;
    
    // 添加字符串
    strings.push_back("Hello");
    strings.push_back("C++");
    strings.emplace_back("World");  // 更高效
    
    // 遍历
    std::cout << "字符串列表:" << std::endl;
    for (const auto& s : strings) {
        std::cout << "  " << s << std::endl;
    }
    
    // 排序
    std::sort(strings.begin(), strings.end());
    std::cout << "\n排序后:" << std::endl;
    for (const auto& s : strings) {
        std::cout << "  " << s << std::endl;
    }
    
    return 0;
}
```

---

## 325. std::string_view: - string_view相关(语法不完整) ⚠️

### 重要说明

`std::string_view:` 的语法是**不完整的**，正确的组件名称是 `std::string_view`（C++17引入，定义在`<string_view>`头文件）。

末尾的冒号`:`可能是：
- 打字错误
- Markdown标题语法的一部分（如`### std::string_view:`）
- 试图表示作用域但语法错误

### 正确的std::string_view

`std::string_view`是C++17引入的轻量级非拥有字符串视图，提供了对字符串数据的只读访问，无需拷贝。

**核心特性**：
- 只读视图，不拥有底层数据
- O(1)拷贝（仅复制指针和长度）
- 支持字符串字面量、std::string、字符数组等多种来源
- 生命周期管理：必须确保底层数据在view使用期间有效

### 代码示例（正确使用）

```cpp
#include <iostream>
#include <string_view>
#include <string>

// 高效函数：接受string_view避免拷贝
void print_view(std::string_view sv) {
    std::cout << "字符串: \"" << sv << "\", 长度: " << sv.length() << std::endl;
}

int main() {
    // 从字符串字面量创建
    std::string_view sv1 = "Hello";
    print_view(sv1);
    
    // 从std::string创建
    std::string str = "World";
    std::string_view sv2 = str;
    print_view(sv2);
    
    // 从字符数组创建
    const char arr[] = "Array";
    std::string_view sv3(arr);
    print_view(sv3);
    
    // 子串操作（高效，无拷贝）
    std::string_view sv4 = "Hello World";
    std::cout << "前5个字符: " << sv4.substr(0, 5) << std::endl;
    std::cout << "去掉前6个: " << sv4.substr(6) << std::endl;
    
    // 与string的区别
    std::cout << "\n=== string vs string_view ===" << std::endl;
    std::string s = "Data";
    std::string_view v = s;
    
    std::cout << "string: 拥有数据，拷贝时深拷贝" << std::endl;
    std::cout << "string_view: 不拥有数据，拷贝时浅拷贝" << std::endl;
    
    // 生命周期警告
    std::string_view dangling;
    {
        std::string temp = "临时字符串";
        dangling = temp;  // 危险：temp将在块结束时销毁
    }
    // 此时使用dangling是未定义行为!
    // std::cout << dangling << std::endl;  // 不要这样做!
    
    return 0;
}
```

---

## 326. std::strcmp - C风格字符串比较

### 功能说明

`std::strcmp`定义于`<cstring>`头文件，用于比较两个C风格（null结尾）字符串。它是C标准库字符串比较函数在C++中的封装。

**函数原型**：
```cpp
int strcmp(const char* lhs, const char* rhs);
```

**参数说明**：
- `lhs`：第一个C字符串
- `rhs`：第二个C字符串

**返回值**：
- `< 0`：`lhs`在字典序上小于`rhs`
- `== 0`：两字符串相等
- `> 0`：`lhs`在字典序上大于`rhs`

**比较规则**：
- 按字符的ASCII值逐字符比较
- 遇到第一个不同的字符或null字符时停止
- 区分大小写（'A' < 'a'）
- null字符 < 任何其他字符

**安全警告**：
- 参数必须是有效的null结尾字符串
- 非null结尾字符串会导致未定义行为（缓冲区溢出）
- 建议使用`std::string`或`strncmp`提高安全性

### 使用场景

1. **C代码兼容**：与C库或遗留代码交互
2. **底层操作**：操作系统API调用
3. **协议解析**：解析固定格式的协议数据
4. **字典排序**：实现字符串排序功能
5. **命令解析**：解析命令行参数

### 代码示例

```cpp
#include <iostream>
#include <cstring>
#include <algorithm>
#include <vector>

int main() {
    // 基本用法
    std::cout << "=== 基本比较 ===" << std::endl;
    
    const char* str1 = "Apple";
    const char* str2 = "Banana";
    const char* str3 = "Apple";
    
    int result1 = std::strcmp(str1, str2);
    std::cout << "strcmp(\"Apple\", \"Banana\") = " << result1 << std::endl;
    
    int result2 = std::strcmp(str1, str3);
    std::cout << "strcmp(\"Apple\", \"Apple\") = " << result2 << std::endl;
    
    int result3 = std::strcmp(str2, str1);
    std::cout << "strcmp(\"Banana\", \"Apple\") = " << result3 << std::endl;
    
    // 大小写敏感
    std::cout << "\n=== 大小写敏感 ===" << std::endl;
    std::cout << "strcmp(\"hello\", \"Hello\") = " 
              << std::strcmp("hello", "Hello") << std::endl;
    std::cout << "'h'(104) - 'H'(72) = " << ('h' - 'H') << std::endl;
    
    // 实际应用：命令解析
    std::cout << "\n=== 命令解析 ===" << std::endl;
    auto execute_command = [](const char* cmd) {
        if (std::strcmp(cmd, "help") == 0) {
            std::cout << "显示帮助信息" << std::endl;
        } else if (std::strcmp(cmd, "quit") == 0) {
            std::cout << "退出程序" << std::endl;
        } else if (std::strcmp(cmd, "version") == 0) {
            std::cout << "版本 1.0.0" << std::endl;
        } else {
            std::cout << "未知命令: " << cmd << std::endl;
        }
    };
    
    execute_command("help");
    execute_command("version");
    execute_command("unknown");
    
    // 实际应用：字符串排序
    std::cout << "\n=== 字符串排序 ===" << std::endl;
    std::vector<const char*> fruits = {
        "banana", "Apple", "cherry", "Date", "elderberry"
    };
    
    std::cout << "排序前: ";
    for (auto f : fruits) std::cout << f << " ";
    std::cout << std::endl;
    
    std::sort(fruits.begin(), fruits.end(), 
              [](const char* a, const char* b) {
                  return std::strcmp(a, b) < 0;
              });
    
    std::cout << "排序后: ";
    for (auto f : fruits) std::cout << f << " ";
    std::cout << std::endl;
    
    // 安全注意事项
    std::cout << "\n=== 安全对比 ===" << std::endl;
    std::cout << "C风格（不安全）:" << std::endl;
    std::cout << "  - 必须确保字符串以null结尾" << std::endl;
    std::cout << "  - 缓冲区溢出风险" << std::endl;
    std::cout << "C++风格（推荐）:" << std::endl;
    std::cout << "  - 使用std::string和compare()" << std::endl;
    std::cout << "  - 自动管理内存和长度" << std::endl;
    
    return 0;
}
```

---

## 327. std::stol - 字符串转long

### 功能说明

`std::stol`定义于`<string>`头文件，用于将字符串转换为`long`类型整数。它是C++11引入的字符串转换函数族的一部分，提供了异常安全的类型转换。

**函数原型**：
```cpp
long stol(const std::string& str, size_t* idx = nullptr, int base = 10);
long stol(const std::wstring& str, size_t* idx = nullptr, int base = 10);
```

**参数说明**：
- `str`：要转换的字符串
- `idx`：输出参数，指向转换处理的最后一个字符位置
- `base`：进制基数（2-36），默认10

**返回值**：
- 转换后的`long`类型值

**异常**：
- `std::invalid_argument`：没有可转换的字符
- `std::out_of_range`：转换结果超出long范围

**相关函数**：
- `stoi` - 转为int
- `stoll` - 转为long long
- `stoul` - 转为unsigned long
- `stoull` - 转为unsigned long long

### 使用场景

1. **配置解析**：从配置文件读取数值
2. **用户输入处理**：转换用户输入的字符串
3. **协议解析**：解析文本协议中的数值字段
4. **数据导入**：从CSV、JSON等格式导入数据
5. **数值验证**：验证并转换字符串形式的数字

### 代码示例

```cpp
#include <iostream>
#include <string>
#include <vector>
#include <stdexcept>

int main() {
    // 基本用法
    std::cout << "=== 基本转换 ===" << std::endl;
    
    std::string str1 = "12345";
    std::string str2 = "-9876";
    std::string str3 = "  42  ";
    
    long num1 = std::stol(str1);
    long num2 = std::stol(str2);
    long num3 = std::stol(str3);
    
    std::cout << "\"" << str1 << "\" -> " << num1 << std::endl;
    std::cout << "\"" << str2 << "\" -> " << num2 << std::endl;
    std::cout << "\"" << str3 << "\" -> " << num3 << std::endl;
    
    // 不同进制
    std::cout << "\n=== 不同进制 ===" << std::endl;
    
    std::string hex_str = "FF";
    std::string bin_str = "1010";
    std::string oct_str = "77";
    
    std::cout << "十六进制 \"" << hex_str << "\": " 
              << std::stol(hex_str, nullptr, 16) << std::endl;
    std::cout << "二进制 \"" << bin_str << "\": " 
              << std::stol(bin_str, nullptr, 2) << std::endl;
    std::cout << "八进制 \"" << oct_str << "\": " 
              << std::stol(oct_str, nullptr, 8) << std::endl;
    
    // 自动检测进制（0x前缀十六进制，0前缀八进制）
    std::cout << "\n=== 自动检测进制 ===" << std::endl;
    std::cout << "stol(\"0xFF\", 0) = " << std::stol("0xFF", nullptr, 0) << std::endl;
    std::cout << "stol(\"077\", 0) = " << std::stol("077", nullptr, 0) << std::endl;
    std::cout << "stol(\"99\", 0) = " << std::stol("99", nullptr, 0) << std::endl;
    
    // 使用idx参数获取处理位置
    std::cout << "\n=== 获取处理位置 ===" << std::endl;
    std::string mixed = "123abc456";
    size_t pos;
    long val = std::stol(mixed, &pos);
    std::cout << "转换 \"" << mixed << "\": 值=" << val 
              << ", 处理到位置=" << pos 
              << ", 剩余=\"" << mixed.substr(pos) << "\"" << std::endl;
    
    // 异常处理
    std::cout << "\n=== 异常处理 ===" << std::endl;
    std::vector<std::string> test_cases = {
        "123",
        "abc",      // invalid_argument
        "99999999999999999999999999999999999"  // out_of_range
    };
    
    for (const auto& s : test_cases) {
        try {
            long result = std::stol(s);
            std::cout << "\"" << s << "\" -> " << result << std::endl;
        } catch (const std::invalid_argument& e) {
            std::cout << "\"" << s << "\": 无效参数 - " << e.what() << std::endl;
        } catch (const std::out_of_range& e) {
            std::cout << "\"" << s << "\": 超出范围 - " << e.what() << std::endl;
        }
    }
    
    // 实际应用：配置文件解析
    std::cout << "\n=== 配置文件解析 ===" << std::endl;
    std::vector<std::pair<std::string, std::string>> config = {
        {"port", "8080"},
        {"timeout", "30"},
        {"max_connections", "1000"}
    };
    
    for (const auto& [key, value] : config) {
        try {
            long num = std::stol(value);
            std::cout << key << " = " << num << std::endl;
        } catch (...) {
            std::cout << key << " = \"" << value 
                      << "\" (转换失败)" << std::endl;
        }
    }
    
    return 0;
}
```

---

---

## 328. std::stof - 字符串转float

### 功能说明

`std::stof`定义于`<string>`头文件，用于将字符串转换为`float`类型浮点数。它支持十进制和科学计数法表示，是C++11字符串转换函数族的重要成员。

**函数原型**：
```cpp
float stof(const std::string& str, size_t* idx = nullptr);
float stof(const std::wstring& str, size_t* idx = nullptr);
```

**参数说明**：
- `str`：要转换的字符串
- `idx`：输出参数，指向转换处理的最后一个字符位置（可选）

**返回值**：
- 转换后的`float`类型值

**支持的格式**：
- 十进制：`123.45`、`-67.89`
- 科学计数法：`1.23e10`、`-5.67E-3`
- 正负号前缀
- 前后空白字符会被忽略

**异常**：
- `std::invalid_argument`：没有可转换的数字
- `std::out_of_range`：值超出float范围

### 使用场景

1. **配置文件解析**：读取浮点配置项
2. **科学计算**：处理实验数据的文本表示
3. **用户输入**：转换界面输入的数值
4. **数据交换**：解析JSON/XML等格式的浮点数
5. **传感器数据**：处理设备输出的字符串数据

### 代码示例

```cpp
#include <iostream>
#include <string>
#include <vector>
#include <iomanip>

int main() {
    // 基本用法
    std::cout << "=== 基本转换 ===" << std::endl;
    
    std::string str1 = "3.14159";
    std::string str2 = "-2.71828";
    std::string str3 = "  1.5  ";
    
    float num1 = std::stof(str1);
    float num2 = std::stof(str2);
    float num3 = std::stof(str3);
    
    std::cout << std::fixed << std::setprecision(6);
    std::cout << "\"" << str1 << "\" -> " << num1 << std::endl;
    std::cout << "\"" << str2 << "\" -> " << num2 << std::endl;
    std::cout << "\"" << str3 << "\" -> " << num3 << std::endl;
    
    // 科学计数法
    std::cout << "\n=== 科学计数法 ===" << std::endl;
    std::vector<std::string> sci_notations = {
        "1.23e5",
        "-4.56E-3",
        "7.89e+2",
        "0.00123e2"
    };
    
    for (const auto& s : sci_notations) {
        float val = std::stof(s);
        std::cout << "\"" << s << "\" -> " << val << std::endl;
    }
    
    // 特殊情况
    std::cout << "\n=== 特殊情况 ===" << std::endl;
    
    // 无穷大
    std::string inf_str = "inf";
    std::cout << "\"inf\" -> " << std::stof(inf_str) << std::endl;
    
    // NaN
    std::string nan_str = "nan";
    std::cout << "\"nan\" -> " << std::stof(nan_str) << std::endl;
    
    // 使用idx参数
    std::cout << "\n=== 获取处理位置 ===" << std::endl;
    std::string mixed = "3.14abc";
    size_t pos;
    float val = std::stof(mixed, &pos);
    std::cout << "转换 \"" << mixed << "\": 值=" << val 
              << ", 处理到位置=" << pos << std::endl;
    
    // 异常处理
    std::cout << "\n=== 异常处理 ===" << std::endl;
    std::vector<std::string> test_cases = {
        "3.14",
        "abc",      // 无效
        "1e400"     // 溢出
    };
    
    for (const auto& s : test_cases) {
        try {
            float result = std::stof(s);
            std::cout << "\"" << s << "\" -> " << result << std::endl;
        } catch (const std::exception& e) {
            std::cout << "\"" << s << "\": " << e.what() << std::endl;
        }
    }
    
    // 实际应用：传感器数据处理
    std::cout << "\n=== 传感器数据解析 ===" << std::endl;
    std::vector<std::string> sensor_data = {
        "TEMP:23.5",
        "HUMID:65.3",
        "PRESS:1013.25"
    };
    
    for (const auto& data : sensor_data) {
        size_t colon = data.find(':');
        if (colon != std::string::npos) {
            std::string type = data.substr(0, colon);
            std::string value_str = data.substr(colon + 1);
            
            try {
                float value = std::stof(value_str);
                std::cout << type << " = " << value << std::endl;
            } catch (...) {
                std::cout << type << ": 解析失败" << std::endl;
            }
        }
    }
    
    return 0;
}
```

---

## 329. std::stack::emplace - 栈原地构造

### 功能说明

`std::stack::emplace`是C++11引入的成员函数，用于在栈顶原地构造元素。与`push`相比，`emplace`直接在容器内构造对象，避免临时对象的创建和拷贝。

**函数原型**：
```cpp
template<class... Args>
decltype(auto) emplace(Args&&... args);
```

**参数说明**：
- `args`：传递给元素构造函数的参数包

**返回值**：
- C++17起：返回所引用元素的引用
- C++17前：void

**与push的区别**：
- `push`：接收已构造的对象，可能触发拷贝/移动
- `emplace`：原地构造，更高效（尤其对于复杂对象）
- `emplace`直接转发参数到构造函数

**底层容器要求**：
- 要求底层容器支持`emplace_back`
- 默认使用`std::deque`或`std::vector`

### 使用场景

1. **性能优化**：避免临时对象的创建和拷贝
2. **复杂对象**：构造需要多参数的自定义类
3. **资源管理**：直接构造资源密集型对象
4. **不可拷贝类型**：构造只有移动语义的类型
5. **代码简洁**：直接传递构造参数，无需先创建对象

### 代码示例

```cpp
#include <iostream>
#include <stack>
#include <string>
#include <vector>

struct Task {
    int id;
    std::string name;
    int priority;
    
    Task(int i, std::string n, int p) 
        : id(i), name(std::move(n)), priority(p) {
        std::cout << "构造 Task(" << id << ", \"" << name 
                  << "\", " << priority << ")" << std::endl;
    }
    
    Task(const Task& other) 
        : id(other.id), name(other.name), priority(other.priority) {
        std::cout << "拷贝构造 Task(" << id << ")" << std::endl;
    }
    
    Task(Task&& other) noexcept
        : id(other.id), name(std::move(other.name)), priority(other.priority) {
        std::cout << "移动构造 Task(" << id << ")" << std::endl;
    }
    
    ~Task() {
        std::cout << "析构 Task(" << id << ")" << std::endl;
    }
};

int main() {
    std::cout << "=== push vs emplace 对比 ===" << std::endl;
    
    {
        std::cout << "\n--- 使用 push ---" << std::endl;
        std::stack<Task> stack1;
        
        // push需要创建临时对象
        Task temp(1, "Task1", 5);
        stack1.push(temp);  // 拷贝构造
        
        stack1.push(Task(2, "Task2", 3));  // 移动构造
    }
    
    {
        std::cout << "\n--- 使用 emplace ---" << std::endl;
        std::stack<Task> stack2;
        
        // emplace直接原地构造，更高效
        stack2.emplace(1, "Task1", 5);
        stack2.emplace(2, "Task2", 3);
        stack2.emplace(3, "Task3", 8);
    }
    
    // 实际应用：任务调度系统
    std::cout << "\n=== 任务调度系统 ===" << std::endl;
    std::stack<Task> task_stack;
    
    // 添加任务（高优先级后入栈）
    task_stack.emplace(100, "备份数据", 3);
    task_stack.emplace(101, "发送邮件", 2);
    task_stack.emplace(102, "紧急处理", 9);
    task_stack.emplace(103, "系统更新", 5);
    
    std::cout << "\n按优先级处理任务:" << std::endl;
    while (!task_stack.empty()) {
        const Task& task = task_stack.top();
        std::cout << "处理: [" << task.id << "] " << task.name 
                  << " (优先级:" << task.priority << ")" << std::endl;
        task_stack.pop();
    }
    
    // 使用字符串栈演示
    std::cout << "\n=== 字符串处理 ===" << std::endl;
    std::stack<std::string> path_stack;
    
    // 构建路径
    path_stack.emplace("/home");
    path_stack.emplace("/home/user");
    path_stack.emplace("/home/user/documents");
    path_stack.emplace("/home/user/documents/project");
    
    std::cout << "路径栈:" << std::endl;
    while (!path_stack.empty()) {
        std::cout << "  " << path_stack.top() << std::endl;
        path_stack.pop();
    }
    
    // 性能对比总结
    std::cout << "\n=== 性能对比总结 ===" << std::endl;
    std::cout << "push:" << std::endl;
    std::cout << "  - 需要创建临时对象" << std::endl;
    std::cout << "  - 触发拷贝或移动构造" << std::endl;
    std::cout << "  - 两次构造（临时+栈内）" << std::endl;
    std::cout << "emplace:" << std::endl;
    std::cout << "  - 直接原地构造" << std::endl;
    std::cout << "  - 只有一次构造" << std::endl;
    std::cout << "  - 转发参数到构造函数" << std::endl;
    
    return 0;
}
```

---

## 330. std::stable_partition - 稳定分区

### 功能说明

`std::stable_partition`定义于`<algorithm>`头文件，将范围分为两部分，满足谓词的元素在前，不满足的在后，同时保持各分区内的相对顺序不变。

**函数原型**：
```cpp
// 单线程版本
BidirIt stable_partition(BidirIt first, BidirIt last, UnaryPredicate p);

// C++17并行执行版本
BidirIt stable_partition(ExecPolicy&& policy, 
                         BidirIt first, BidirIt last, UnaryPredicate p);
```

**参数说明**：
- `first`, `last`：要分区的范围
- `p`：一元谓词，返回true的元素分到前半部分
- `policy`：执行策略（C++17）

**返回值**：
- 指向分区边界的迭代器（第二个分区的首元素）

**复杂度**：
- 最多N·log(N)次交换，其中N = last - first
- 如果需要分配临时内存，最多N次谓词调用

**与std::partition的区别**：
- `partition`：不稳定，快但可能改变元素顺序
- `stable_partition`：稳定，保持相对顺序但可能更慢

### 使用场景

1. **数据分离**：保留原始顺序的同时分离有效/无效数据
2. **优先级队列**：按优先级分组同时保持FIFO顺序
3. **多阶段处理**：先分组再分别处理，保持数据时序
4. **UI更新**：区分可见/隐藏元素同时保持Z轴顺序
5. **批处理**：分离需要不同处理的记录

### 代码示例

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <string>

struct Student {
    std::string name;
    int score;
    int id;
    
    void print() const {
        std::cout << "[" << id << "] " << name << ": " << score << std::endl;
    }
};

int main() {
    // 基本用法
    std::cout << "=== 基本分区 ===" << std::endl;
    std::vector<int> nums = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    
    std::cout << "原始: ";
    for (int n : nums) std::cout << n << " ";
    std::cout << std::endl;
    
    // 将偶数分到前面
    auto it = std::stable_partition(nums.begin(), nums.end(), 
        [](int n) { return n % 2 == 0; });
    
    std::cout << "分区后（偶数|奇数）: ";
    for (int n : nums) std::cout << n << " ";
    std::cout << std::endl;
    std::cout << "分区点在位置: " << std::distance(nums.begin(), it) << std::endl;
    
    // 验证稳定性
    std::cout << "\n=== 稳定性验证 ===" << std::endl;
    std::vector<Student> students = {
        {"Alice", 85, 1},
        {"Bob", 92, 2},
        {"Charlie", 78, 3},
        {"David", 95, 4},
        {"Eve", 88, 5},
        {"Frank", 76, 6},
        {"Grace", 91, 7}
    };
    
    std::cout << "原始学生列表:" << std::endl;
    for (const auto& s : students) s.print();
    
    // 按及格分区（>=80为及格）
    auto pass_it = std::stable_partition(students.begin(), students.end(),
        [](const Student& s) { return s.score >= 80; });
    
    std::cout << "\n分区后（及格|不及格）:" << std::endl;
    std::cout << "及格学生:" << std::endl;
    for (auto it = students.begin(); it != pass_it; ++it) {
        it->print();
    }
    std::cout << "不及格学生:" << std::endl;
    for (auto it = pass_it; it != students.end(); ++it) {
        it->print();
    }
    
    // 注意ID顺序保持稳定！
    
    // 实际应用：文件分类
    std::cout << "\n=== 文件分类 ===" << std::endl;
    std::vector<std::string> files = {
        "document.pdf",
        "image1.png",
        "report.docx",
        "image2.jpg",
        "data.csv",
        "image3.gif",
        "notes.txt"
    };
    
    // 分离图片文件
    auto img_it = std::stable_partition(files.begin(), files.end(),
        [](const std::string& f) {
            return f.find(".png") != std::string::npos ||
                   f.find(".jpg") != std::string::npos ||
                   f.find(".gif") != std::string::npos;
        });
    
    std::cout << "图片文件:" << std::endl;
    for (auto it = files.begin(); it != img_it; ++it) {
        std::cout << "  " << *it << std::endl;
    }
    std::cout << "其他文件:" << std::endl;
    for (auto it = img_it; it != files.end(); ++it) {
        std::cout << "  " << *it << std::endl;
    }
    
    // 对比：partition（不稳定）vs stable_partition（稳定）
    std::cout << "\n=== partition vs stable_partition ===" << std::endl;
    std::vector<int> nums1 = {5, 2, 8, 1, 9, 3, 7, 4, 6};
    std::vector<int> nums2 = nums1;
    
    std::partition(nums1.begin(), nums1.end(), [](int n) { return n < 5; });
    std::stable_partition(nums2.begin(), nums2.end(), [](int n) { return n < 5; });
    
    std::cout << "原始: 5 2 8 1 9 3 7 4 6" << std::endl;
    std::cout << "partition: ";
    for (int n : nums1) std::cout << n << " ";
    std::cout << " (不稳定，顺序可能改变)" << std::endl;
    std::cout << "stable_partition: ";
    for (int n : nums2) std::cout << n << " ";
    std::cout << " (稳定，相对顺序保持)" << std::endl;
    
    return 0;
}
```

---

## 331. std::sscanf - C风格格式化输入

### 功能说明

`std::sscanf`定义于`<cstdio>`头文件，从字符串中按指定格式读取数据。它是C标准库`sscanf`的C++封装，提供强大的字符串解析能力。

**函数原型**：
```cpp
int sscanf(const char* str, const char* format, ...);
```

**参数说明**：
- `str`：要解析的源字符串
- `format`：格式控制字符串
- `...`：可变参数，接收解析结果的变量地址

**返回值**：
- 成功匹配的参数数量
- 0：没有匹配
- EOF：读取错误或格式串结束

**常用格式说明符**：
- `%d` - 十进制整数
- `%f` - 浮点数
- `%s` - 字符串
- `%c` - 字符
- `%x` - 十六进制
- `%[^chars]` - 扫描集合（直到遇到指定字符）

**安全警告**：
- 缓冲区溢出风险（使用`%Ns`限制长度）
- 类型安全差（编译期不检查参数类型）
- C++中建议使用`std::istringstream`或正则表达式

### 使用场景

1. **配置文件解析**：解析固定格式的配置
2. **日志解析**：提取日志中的结构化数据
3. **协议解析**：解析简单文本协议
4. **CSV处理**：读取逗号分隔的数据
5. **遗留代码**：与C代码库交互

### 代码示例

```cpp
#include <iostream>
#include <cstdio>
#include <string>

int main() {
    // 基本用法
    std::cout << "=== 基本解析 ===" << std::endl;
    
    const char* data1 = "123 456.78 Hello";
    int i;
    float f;
    char s[20];
    
    int result = std::sscanf(data1, "%d %f %s", &i, &f, s);
    std::cout << "匹配了 " << result << " 项:" << std::endl;
    std::cout << "  整数: " << i << std::endl;
    std::cout << "  浮点数: " << f << std::endl;
    std::cout << "  字符串: " << s << std::endl;
    
    // 日期时间解析
    std::cout << "\n=== 日期时间解析 ===" << std::endl;
    const char* datetime = "2024-03-15 14:30:00";
    int year, month, day, hour, minute, second;
    
    std::sscanf(datetime, "%d-%d-%d %d:%d:%d",
                &year, &month, &day, &hour, &minute, &second);
    
    std::cout << "解析: " << datetime << std::endl;
    std::cout << "  日期: " << year << "年" << month << "月" << day << "日" << std::endl;
    std::cout << "  时间: " << hour << ":" << minute << ":" << second << std::endl;
    
    // 使用扫描集合
    std::cout << "\n=== 扫描集合 ===" << std::endl;
    const char* path = "/home/user/documents/file.txt";
    char dirname[50], filename[50], ext[10];
    
    std::sscanf(path, "%[^/]/%[^/]/%[^/]/%[^.].%s",
                dirname, dirname, dirname, filename, ext);
    
    std::cout << "路径: " << path << std::endl;
    std::cout << "文件名: " << filename << std::endl;
    std::cout << "扩展名: " << ext << std::endl;
    
    // 实际应用：解析版本信息
    std::cout << "\n=== 版本信息解析 ===" << std::endl;
    const char* version_str = "Version: 2.5.1 (Build 12345)";
    int major, minor, patch, build;
    
    std::sscanf(version_str, "Version: %d.%d.%d (Build %d)",
                &major, &minor, &patch, &build);
    
    std::cout << "解析: " << version_str << std::endl;
    std::cout << "  版本: " << major << "." << minor << "." << patch << std::endl;
    std::cout << "  构建号: " << build << std::endl;
    
    // 安全性：限制字符串长度
    std::cout << "\n=== 安全解析（限制长度） ===" << std::endl;
    const char* long_str = "ThisIsAVeryLongStringThatCouldOverflow";
    char safe_buf[11];  // 只接收10个字符 + null
    
    std::sscanf(long_str, "%10s", safe_buf);
    std::cout << "原字符串: " << long_str << std::endl;
    std::cout << "安全接收: " << safe_buf << std::endl;
    
    // 与C++方法的对比
    std::cout << "\n=== C++替代方案 ===" << std::endl;
    std::cout << "推荐使用:" << std::endl;
    std::cout << "  - std::istringstream: 类型安全" << std::endl;
    std::cout << "  - std::regex: 复杂模式匹配" << std::endl;
    std::cout << "  - std::stoi/stod: 简单数值转换" << std::endl;
    std::cout << "\nsscanf仍有用武之地:" << std::endl;
    std::cout << "  - 固定格式简单数据" << std::endl;
    std::cout << "  - 高性能场景" << std::endl;
    std::cout << "  - C代码兼容" << std::endl;
    
    return 0;
}
```

---

## 332. std::smatch - 正则匹配结果

### 功能说明

`std::smatch`定义于`<regex>`头文件，用于存储正则表达式匹配的结果。它继承自`std::match_results`，专门用于`std::string`类型的匹配。

**类型定义**：
```cpp
using smatch = std::match_results<std::string::const_iterator>;
```

**主要成员**：

| 成员 | 说明 |
|------|------|
| `smatch::size()` | 匹配组数量（包含整个匹配） |
| `smatch::empty()` | 检查是否有匹配 |
| `smatch::operator[n]` | 访问第n个捕获组 |
| `smatch::str(n)` | 获取第n个组的字符串 |
| `smatch::position(n)` | 第n个组的起始位置 |
| `smatch::length(n)` | 第n个组的长度 |
| `smatch::prefix()` | 匹配前的字符串 |
| `smatch::suffix()` | 匹配后的字符串 |
| `smatch::begin()/end()` | 迭代器范围 |

**相关类型**：
- `std::cmatch` - C字符串匹配结果
- `std::wsmatch` - 宽字符串匹配结果

### 使用场景

1. **数据提取**：从文本中提取结构化数据
2. **日志分析**：解析日志中的关键信息
3. **验证输入**：验证并提取格式化输入
4. **文本替换**：获取匹配位置进行替换
5. **协议解析**：解析文本协议数据

### 代码示例

```cpp
#include <iostream>
#include <string>
#include <regex>

int main() {
    // 基本用法
    std::cout << "=== 基本匹配 ===" << std::endl;
    
    std::string text = "Hello 123 World 456";
    std::regex number_regex("(\\d+)");
    std::smatch match;
    
    if (std::regex_search(text, match, number_regex)) {
        std::cout << "找到匹配: " << match[0] << std::endl;
        std::cout << "位置: " << match.position() << std::endl;
        std::cout << "长度: " << match.length() << std::endl;
    }
    
    // 多捕获组
    std::cout << "\n=== 多捕获组 ===" << std::endl;
    std::string date_str = "2024-03-15";
    std::regex date_regex("(\\d{4})-(\\d{2})-(\\d{2})");
    std::smatch date_match;
    
    if (std::regex_match(date_str, date_match, date_regex)) {
        std::cout << "完整匹配: " << date_match[0] << std::endl;
        std::cout << "年: " << date_match[1] << std::endl;
        std::cout << "月: " << date_match[2] << std::endl;
        std::cout << "日: " << date_match[3] << std::endl;
        
        std::cout << "\n遍历所有组:" << std::endl;
        for (size_t i = 0; i < date_match.size(); ++i) {
            std::cout << "  [" << i << "] \"" << date_match[i] 
                      << "\" @ " << date_match.position(i) << std::endl;
        }
    }
    
    // 迭代查找所有匹配
    std::cout << "\n=== 迭代查找 ===" << std::endl;
    std::string email_text = "Contact us at: support@example.com or sales@company.org";
    std::regex email_regex("([\\w.-]+)@([\\w.-]+\\.\\w+)");
    std::smatch email_match;
    std::string::const_iterator search_start(email_text.cbegin());
    
    std::cout << "文本: " << email_text << std::endl;
    std::cout << "找到的所有邮箱:" << std::endl;
    
    while (std::regex_search(search_start, email_text.cend(), 
                           email_match, email_regex)) {
        std::cout << "  完整: " << email_match[0] << std::endl;
        std::cout << "    用户名: " << email_match[1] << std::endl;
        std::cout << "    域名: " << email_match[2] << std::endl;
        search_start = email_match.suffix().first;
    }
    
    // 实际应用：URL解析
    std::cout << "\n=== URL解析 ===" << std::endl;
    std::string url = "https://www.example.com:8080/path/to/page?key=value#section";
    std::regex url_regex("(https?)://([^/:]+)(:\\d+)?([^?#]*)?(\\?[^#]*)?(#.*)?");
    std::smatch url_match;
    
    if (std::regex_match(url, url_match, url_regex)) {
        std::cout << "URL: " << url << std::endl;
        std::cout << "协议: " << url_match[1] << std::endl;
        std::cout << "主机: " << url_match[2] << std::endl;
        std::cout << "端口: " << (url_match[3].length() ? url_match[3] : "默认") << std::endl;
        std::cout << "路径: " << url_match[4] << std::endl;
        std::cout << "查询: " << url_match[5] << std::endl;
        std::cout << "片段: " << url_match[6] << std::endl;
    }
    
    // 使用prefix和suffix
    std::cout << "\n=== Prefix 和 Suffix ===" << std::endl;
    std::string sentence = "The quick brown fox jumps";
    std::regex word_regex("brown");
    std::smatch word_match;
    
    if (std::regex_search(sentence, word_match, word_regex)) {
        std::cout << "原文: \"" << sentence << "\"" << std::endl;
        std::cout << "匹配: \"" << word_match[0] << "\"" << std::endl;
        std::cout << "前缀: \"" << word_match.prefix() << "\"" << std::endl;
        std::cout << "后缀: \"" << word_match.suffix() << "\"" << std::endl;
    }
    
    return 0;
}
```

---

[继续追加组件333-350...]

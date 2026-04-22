# Blender std:: 组件详解（第51-100名）

本文档详细介绍 Blender 源码中使用频率排名第51-100的std组件，每个组件包含用法说明和代码示例。

---

## 51. std::is_void_v (31次)
**头文件**: `<type_traits>`  
**说明**: 编译期判断类型是否为void

```cpp
// 检查类型是否为void
template<typename T>
void process(T value) {
    if constexpr (std::is_void_v<T>) {
        // T是void类型
        return;
    }
    // 处理非void类型
}
```

---

## 52. std::tuple (30次)
**头文件**: `<tuple>`  
**说明**: 固定大小的异构值集合

```cpp
// 返回多个值的函数
std::tuple<int, std::string, float> get_data() {
    return std::make_tuple(42, "hello", 3.14f);
}

// 解包tuple
auto [id, name, value] = get_data();
```

---

## 53. std::runtime_error (30次)
**头文件**: `<stdexcept>`  
**说明**: 运行时错误异常

```cpp
// 抛出运行时错误
void load_file(const std::string& path) {
    if (!file_exists(path)) {
        throw std::runtime_error("File not found: " + path);
    }
}

// 捕获异常
try {
    load_file("data.txt");
} catch (const std::runtime_error& e) {
    std::cerr << "Error: " << e.what() << std::endl;
}
```

---

## 54. std::map (30次)
**头文件**: `<map>`  
**说明**: 有序键值对容器

```cpp
// 使用map存储设置
std::map<std::string, int> settings;
settings["width"] = 1920;
settings["height"] = 1080;
settings["samples"] = 128;

// 遍历
for (const auto& [key, value] : settings) {
    std::cout << key << " = " << value << std::endl;
}
```

---

## 55. std::pow (29次)
**头文件**: `<cmath>`  
**说明**: 计算幂次

```cpp
// 计算平方和立方
double square = std::pow(x, 2.0);
double cube = std::pow(x, 3.0);

// 计算颜色gamma校正
double linear = std::pow(gamma_corrected, 2.2);
```

---

## 56. std::copy (29次)
**头文件**: `<algorithm>`  
**说明**: 复制元素范围

```cpp
// 复制vector
std::vector<int> src = {1, 2, 3, 4, 5};
std::vector<int> dst(src.size());
std::copy(src.begin(), src.end(), dst.begin());

// 复制到输出流
std::copy(vec.begin(), vec.end(), 
          std::ostream_iterator<int>(std::cout, " "));
```

---

## 57. std::copy_n (28次)
**头文件**: `<algorithm>`  
**说明**: 复制n个元素

```cpp
// 只复制前3个元素
std::vector<int> src = {1, 2, 3, 4, 5};
std::vector<int> dst(3);
std::copy_n(src.begin(), 3, dst.begin());
// dst = {1, 2, 3}
```

---

## 58. std::make_optional (27次)
**头文件**: `<optional>`  
**说明**: 创建optional对象

```cpp
// 函数可能返回空值
std::optional<int> parse_int(const std::string& s) {
    try {
        return std::make_optional(std::stoi(s));
    } catch (...) {
        return std::nullopt;
    }
}

// 使用
if (auto val = parse_int("42")) {
    std::cout << "Value: " << *val << std::endl;
}
```

---

## 59. std::ios::binary (26次)
**头文件**: `<ios>`  
**说明**: 二进制模式文件打开标志

```cpp
// 以二进制模式打开文件
std::ofstream file("data.bin", std::ios::binary | std::ios::out);
file.write(reinterpret_cast<const char*>(&data), sizeof(data));
file.close();

// 读取二进制文件
std::ifstream infile("model.blend", std::ios::binary);
```

---

## 60. std::unordered_set (25次)
**头文件**: `<unordered_set>`  
**说明**: 哈希集合，无序唯一元素

```cpp
// 存储唯一ID
std::unordered_set<std::string> used_ids;
used_ids.insert("mesh_001");
used_ids.insert("mesh_002");

// 检查是否存在
if (used_ids.find(id) != used_ids.end()) {
    // ID已存在
}
```

---

## 61. std::unordered_map (25次)
**头文件**: `<unordered_map>`  
**说明**: 哈希表，无序键值对

```cpp
// 快速查找缓存
std::unordered_map<std::string, Mesh*> mesh_cache;
mesh_cache["cube"] = create_cube_mesh();
mesh_cache["sphere"] = create_sphere_mesh();

// O(1)查找
auto it = mesh_cache.find("cube");
if (it != mesh_cache.end()) {
    render_mesh(it->second);
}
```

---

## 62. std::make_pair (25次)
**头文件**: `<utility>`  
**说明**: 创建pair对象

```cpp
// 返回键值对
auto create_entry(int id, const std::string& name) {
    return std::make_pair(id, name);
}

// 插入到map
my_map.insert(std::make_pair(key, value));

// C++11起可直接用{}，但make_pair仍有类型推导优势
auto p = std::make_pair(1, std::string("hello"));
```

---

## 63. std::reverse_iterator (24次)
**头文件**: `<iterator>`  
**说明**: 反向迭代器适配器

```cpp
// 反向遍历
std::vector<int> vec = {1, 2, 3, 4, 5};
for (auto it = vec.rbegin(); it != vec.rend(); ++it) {
    std::cout << *it << " ";  // 输出: 5 4 3 2 1
}

// 查找最后一个匹配
auto it = std::find(vec.rbegin(), vec.rend(), 3);
```

---

## 64. std::stable_sort (23次)
**头文件**: `<algorithm>`  
**说明**: 稳定排序，保持相等元素的原始顺序

```cpp
// 按优先级排序，但保持相同优先级内的原始顺序
struct Task {
    int priority;
    std::string name;
    int order;  // 原始顺序
};

std::vector<Task> tasks = {...};
std::stable_sort(tasks.begin(), tasks.end(), 
    [](const Task& a, const Task& b) {
        return a.priority < b.priority;
    });
```

---

## 65. std::fill_n (23次)
**头文件**: `<algorithm>`  
**说明**: 用值填充n个位置

```cpp
// 初始化数组的一部分
std::vector<int> buffer(100);
std::fill_n(buffer.begin(), 10, 0);  // 前10个设为0

// 清零内存
std::fill_n(reinterpret_cast<char*>(&data), sizeof(data), 0);
```

---

## 66. std::round (22次)
**头文件**: `<cmath>`  
**说明**: 四舍五入到最接近的整数

```cpp
// 像素对齐
double x = 3.7;
int pixel_x = static_cast<int>(std::round(x));  // 4

// 颜色量化
double color_val = 128.6;
int quantized = static_cast<int>(std::round(color_val));
```

---

## 67. std::is_base_of_v (22次)
**头文件**: `<type_traits>`  
**说明**: 编译期判断是否为基类

```cpp
// 类型安全检查
template<typename Derived, typename Base>
void cast_check() {
    static_assert(std::is_base_of_v<Base, Derived>, 
                  "Derived must inherit from Base");
}

// 智能指针类型检查
if constexpr (std::is_base_of_v<Shape, T>) {
    // T是Shape的派生类
}
```

---

## 68. std::deque (22次)
**头文件**: `<deque>`  
**说明**: 双端队列

```cpp
// 渲染命令队列
std::deque<RenderCommand> command_queue;

// 双端操作
command_queue.push_back(create_command());
command_queue.push_front(priority_command());

// 处理完从头部移除
auto cmd = command_queue.front();
command_queue.pop_front();
```

---

## 69. std::size_t (21次)
**头文件**: `<cstddef>`  
**说明**: 无符号整数类型，用于大小和索引

```cpp
// 遍历容器
for (std::size_t i = 0; i < vertices.size(); ++i) {
    process_vertex(vertices[i]);
}

// 缓冲区大小
std::size_t buffer_size = width * height * sizeof(Color);
```

---

## 70. std::is_convertible_v (21次)
**头文件**: `<type_traits>`  
**说明**: 编译期判断类型是否可转换

```cpp
// 类型约束
template<typename From, typename To>
void convert(const From& from, To& to) {
    static_assert(std::is_convertible_v<From, To>,
                  "Cannot convert From to To");
    to = static_cast<To>(from);
}

// 概念检查
if constexpr (std::is_convertible_v<T, double>) {
    // T可以转换为double
}
```

---

## 71. std::sin (20次)
**头文件**: `<cmath>`  
**说明**: 正弦函数

```cpp
// 旋转计算
double angle = 45.0 * M_PI / 180.0;  // 转弧度
double x = radius * std::cos(angle);
double y = radius * std::sin(angle);

// 波动效果
double wave = amplitude * std::sin(frequency * time);
```

---

## 72. std::queue (20次)
**头文件**: `<queue>`  
**说明**: FIFO队列

```cpp
// 任务队列
std::queue<std::function<void()>> task_queue;

// 添加任务
task_queue.push([]() { load_texture("diffuse.png"); });
task_queue.push([]() { load_texture("normal.png"); });

// 处理任务
while (!task_queue.empty()) {
    auto task = task_queue.front();
    task_queue.pop();
    task();
}
```

---

## 73. std::is_trivially_destructible_v (20次)
**头文件**: `<type_traits>`  
**说明**: 编译期判断是否可平凡析构

```cpp
// 内存优化
template<typename T>
void destroy_array(T* ptr, std::size_t n) {
    if constexpr (std::is_trivially_destructible_v<T>) {
        // 无需调用析构函数，直接释放
    } else {
        for (std::size_t i = 0; i < n; ++i) {
            ptr[i].~T();
        }
    }
}
```

---

## 74. std::is_trivial_v (20次)
**头文件**: `<type_traits>`  
**说明**: 编译期判断是否为平凡类型

```cpp
// memcpy安全检查
if constexpr (std::is_trivial_v<T>) {
    // 可以安全地使用memcpy
    std::memcpy(dst, src, n * sizeof(T));
} else {
    // 必须逐个复制
    for (std::size_t i = 0; i < n; ++i) {
        dst[i] = src[i];
    }
}
```

---

## 75. std::cos (20次)
**头文件**: `<cmath>`  
**说明**: 余弦函数

```cpp
// 3D旋转矩阵
double cos_a = std::cos(angle_x);
double sin_a = std::sin(angle_x);

// 球坐标转换
double x = r * std::sin(theta) * std::cos(phi);
double y = r * std::sin(theta) * std::sin(phi);
double z = r * std::cos(theta);
```

---

## 76. std::is_floating_point_v (19次)
**头文件**: `<type_traits>`  
**说明**: 编译期判断是否为浮点类型

```cpp
// 类型特化
template<typename T>
void normalize(T& value) {
    if constexpr (std::is_floating_point_v<T>) {
        // 浮点数归一化到0-1
        value = std::clamp(value, T(0), T(1));
    } else {
        // 整数处理
        value = std::max(T(0), value);
    }
}
```

---

## 77. std::memcpy (18次)
**头文件**: `<cstring>`  
**说明**: 内存复制

```cpp
// 快速复制缓冲区
void* copy_buffer(void* dst, const void* src, std::size_t size) {
    return std::memcpy(dst, src, size);
}

// 复制顶点数据
std::memcpy(vertices.data(), source_data, 
            vertex_count * sizeof(Vertex));
```

---

## 78. std::istringstream (18次)
**头文件**: `<sstream>`  
**说明**: 字符串输入流

```cpp
// 解析字符串
std::string data = "1920 1080 60";
std::istringstream iss(data);
int width, height, fps;
iss >> width >> height >> fps;

// 逐行解析
std::string line;
while (std::getline(file, line)) {
    std::istringstream line_stream(line);
    parse_line(line_stream);
}
```

---

## 79. std::accumulate (18次)
**头文件**: `<numeric>`  
**说明**: 累积计算

```cpp
// 求和
std::vector<int> values = {1, 2, 3, 4, 5};
int sum = std::accumulate(values.begin(), values.end(), 0);

// 计算平均值
double avg = std::accumulate(values.begin(), values.end(), 0.0) / values.size();

// 字符串连接
std::vector<std::string> parts = {"Hello", " ", "World"};
std::string result = std::accumulate(
    parts.begin(), parts.end(), std::string{});
```

---

## 80. std::setw (17次)
**头文件**: `<iomanip>`  
**说明**: 设置字段宽度

```cpp
// 格式化输出
std::cout << std::setw(10) << "Name" 
          << std::setw(8) << "Score" << std::endl;
std::cout << std::setw(10) << "Alice" 
          << std::setw(8) << 95 << std::endl;
// 输出:
//       Name   Score
//      Alice      95
```

---

## 81. std::reverse (17次)
**头文件**: `<algorithm>`  
**说明**: 反转元素顺序

```cpp
// 反转数组
std::vector<int> vec = {1, 2, 3, 4, 5};
std::reverse(vec.begin(), vec.end());
// vec = {5, 4, 3, 2, 1}

// 反转字符串
std::string str = "hello";
std::reverse(str.begin(), str.end());
// str = "olleh"
```

---

## 82. std::ostringstream (17次)
**头文件**: `<sstream>`  
**说明**: 字符串输出流

```cpp
// 构建格式化字符串
std::ostringstream oss;
oss << "Error at line " << line_number 
    << ": " << error_message;
std::string error_str = oss.str();

// 生成唯一ID
std::ostringstream id_gen;
id_gen << "object_" << counter++;
std::string id = id_gen.str();
```

---

## 83. std::ios::out (17次)
**头文件**: `<ios>`  
**说明**: 输出模式文件打开标志

```cpp
// 以输出模式打开文件
std::ofstream outfile("output.txt", std::ios::out | std::ios::trunc);
outfile << "Hello, World!" << std::endl;

// 追加模式
std::ofstream logfile("log.txt", std::ios::out | std::ios::app);
logfile << "New log entry" << std::endl;
```

---

## 84. std::find_if (17次)
**头文件**: `<algorithm>`  
**说明**: 查找满足条件的第一个元素

```cpp
// 查找第一个可见对象
auto it = std::find_if(objects.begin(), objects.end(),
    [](const Object& obj) {
        return obj.is_visible();
    });

if (it != objects.end()) {
    select_object(*it);
}
```

---

## 85. std::wstring (16次)
**头文件**: `<string>`  
**说明**: 宽字符字符串

```cpp
// Windows API兼容性
std::wstring wide_path = L"C:\\Program Files\\Blender\\blender.exe";
CreateFileW(wide_path.c_str(), ...);

// 转换窄字符串到宽字符串
std::string narrow = "Hello";
std::wstring wide(narrow.begin(), narrow.end());
```

---

## 86. std::monostate (16次)
**头文件**: `<variant>`  
**说明**: 空状态类型，用于variant的默认构造

```cpp
// variant可以包含空状态
using Result = std::variant<std::monostate, Success, Error>;

Result process() {
    if (!initialized) {
        return std::monostate{};  // 表示未初始化
    }
    // 处理并返回结果
    return Success{...};
}
```

---

## 87. std::make_tuple (16次)
**头文件**: `<tuple>`  
**说明**: 创建tuple对象

```cpp
// 返回多个值
auto get_position() {
    return std::make_tuple(x, y, z);
}

// 存储异构数据
auto record = std::make_tuple(
    "user_001", 
    42, 
    std::chrono::system_clock::now()
);
```

---

## 88. std::list (16次)
**头文件**: `<list>`  
**说明**: 双向链表

```cpp
// 需要频繁插入删除的场景
std::list<Command> command_history;

// 在任意位置插入（O(1)）
auto it = command_history.begin();
std::advance(it, 5);
command_history.insert(it, new_command);

// 删除元素不影响其他迭代器
command_history.remove_if([](const Command& cmd) {
    return cmd.is_expired();
});
```

---

## 89. std::is_nothrow_move_constructible_v (16次)
**头文件**: `<type_traits>`  
**说明**: 编译期判断是否不抛异常的移动构造

```cpp
// 强异常安全保证
template<typename T>
class Container {
    static_assert(std::is_nothrow_move_constructible_v<T>,
                  "T must be nothrow move constructible");
};

// 条件移动
if constexpr (std::is_nothrow_move_constructible_v<T>) {
    // 可以安全地移动
    new_data[i] = std::move(old_data[i]);
}
```

---

## 90. std::is_integral_v (16次)
**头文件**: `<type_traits>`  
**说明**: 编译期判断是否为整数类型

```cpp
// 整数特化
template<typename T>
void process(T value) {
    if constexpr (std::is_integral_v<T>) {
        // 整数处理
        value = std::clamp(value, T(0), T(255));
    } else {
        // 浮点数处理
        value = std::clamp(value, T(0.0), T(1.0));
    }
}
```

---

## 91. std::initializer_list (16次)
**头文件**: `<initializer_list>`  
**说明**: 初始化列表支持

```cpp
// 构造函数支持初始化列表
class Mesh {
public:
    Mesh(std::initializer_list<Vertex> vertices) 
        : vertices_(vertices) {}
};

// 使用
Mesh cube = {v0, v1, v2, v3, v4, v5, v6, v7};

// 遍历初始化列表
void print_all(std::initializer_list<int> values) {
    for (int v : values) {
        std::cout << v << " ";
    }
}
```

---

## 92. std::ofstream (15次)
**头文件**: `<fstream>`  
**说明**: 文件输出流

```cpp
// 写入文本文件
std::ofstream out("config.txt");
out << "width = 1920" << std::endl;
out << "height = 1080" << std::endl;
out.close();

// 写入二进制文件
std::ofstream bin("data.bin", std::ios::binary);
bin.write(reinterpret_cast<const char*>(&header), sizeof(header));
```

---

## 93. std::is_trivially_copyable_v (15次)
**头文件**: `<type_traits>`  
**说明**: 编译期判断是否可平凡复制

```cpp
// 选择最优复制策略
template<typename T>
void copy_elements(T* dst, const T* src, std::size_t n) {
    if constexpr (std::is_trivially_copyable_v<T>) {
        // 使用memcpy，更快
        std::memcpy(dst, src, n * sizeof(T));
    } else {
        // 逐个复制
        for (std::size_t i = 0; i < n; ++i) {
            dst[i] = src[i];
        }
    }
}
```

---

## 94. std::in_place_type (15次)
**头文件**: `<optional>/<variant>`  
**说明**: 原地构造标记

```cpp
// variant原地构造复杂类型
std::variant<int, std::vector<int>> v;
v.emplace<std::vector<int>>(std::in_place_type<std::vector<int>>, 
                             10, 42);  // 10个42

// optional原地构造
std::optional<ComplexObject> opt;
opt.emplace(std::in_place_type<ComplexObject>, arg1, arg2, arg3);
```

---

## 95. std::ptrdiff_t (14次)
**头文件**: `<cstddef>`  
**说明**: 指针差值类型

```cpp
// 计算指针距离
int* start = array;
int* end = array + size;
std::ptrdiff_t count = end - start;

// 安全的指针运算
std::ptrdiff_t offset = target - base;
if (offset >= 0 && offset < max_size) {
    // 有效范围
}
```

---

## 96. std::is_sorted (14次)
**头文件**: `<algorithm>`  
**说明**: 检查范围是否已排序

```cpp
// 检查排序状态
std::vector<int> data = {1, 2, 3, 4, 5};
if (std::is_sorted(data.begin(), data.end())) {
    std::cout << "Already sorted" << std::endl;
} else {
    std::sort(data.begin(), data.end());
}

// 检查部分排序
auto it = std::is_sorted_until(data.begin(), data.end());
```

---

## 97. std::is_invocable_r_v (14次)
**头文件**: `<type_traits>`  
**说明**: 编译期判断可调用对象是否返回指定类型

```cpp
// 回调类型检查
template<typename F>
void register_callback(F&& f) {
    static_assert(std::is_invocable_r_v<void, F, int>,
                  "Callback must return void and take int");
    callback_ = std::forward<F>(f);
}

// 使用
register_callback([](int x) { std::cout << x << std::endl; });
```

---

## 98. std::chrono::nanoseconds (14次)
**头文件**: `<chrono>`  
**说明**: 纳秒时间间隔

```cpp
// 高精度计时
auto start = std::chrono::high_resolution_clock::now();
// ... 执行操作 ...
auto end = std::chrono::high_resolution_clock::now();

auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(
    end - start);
std::cout << "Elapsed: " << duration.count() << " ns" << std::endl;
```

---

## 99. std::index_sequence (13次)
**头文件**: `<utility>`  
**说明**: 编译期整数序列

```cpp
// 实现tuple的get<N>
template<typename Tuple, std::size_t... Is>
void print_tuple_impl(const Tuple& t, std::index_sequence<Is...>) {
    ((std::cout << std::get<Is>(t) << " "), ...);
}

template<typename... Args>
void print_tuple(const std::tuple<Args...>& t) {
    print_tuple_impl(t, std::index_sequence_for<Args...>{});
}

// 展开参数包
template<typename T, std::size_t... Is>
auto array_to_tuple(const T* arr, std::index_sequence<Is...>) {
    return std::make_tuple(arr[Is]...);
}
```

---

## 100. std::trunc (12次)
**头文件**: `<cmath>`  
**说明**: 向零取整

```cpp
// 截断小数部分
double value = 3.7;
double truncated = std::trunc(value);  // 3.0

double negative = -3.7;
double result = std::trunc(negative);  // -3.0 (向零)

// 像素网格对齐
double x = 100.7;
int pixel_x = static_cast<int>(std::trunc(x));  // 100
```

---

## 总结

这50个组件涵盖了：

- **类型萃取** (11个): `is_void_v`, `is_base_of_v`, `is_convertible_v`, `is_trivially_destructible_v`, `is_trivial_v`, `is_floating_point_v`, `is_nothrow_move_constructible_v`, `is_integral_v`, `is_trivially_copyable_v`, `is_invocable_r_v`, `is_sorted`
- **数学函数** (5个): `pow`, `sin`, `cos`, `round`, `trunc`
- **容器** (8个): `tuple`, `map`, `unordered_set`, `unordered_map`, `deque`, `queue`, `list`
- **算法** (7个): `copy`, `copy_n`, `stable_sort`, `fill_n`, `reverse`, `find_if`, `accumulate`
- **IO** (8个): `istringstream`, `ostringstream`, `ofstream`, `setw`, `ios::binary`, `ios::out`, `wstring`
- **实用工具** (11个): `make_optional`, `make_pair`, `reverse_iterator`, `size_t`, `ptrdiff_t`, `initializer_list`, `make_tuple`, `in_place_type`, `index_sequence`, `monostate`, `runtime_error`
- **时间与性能** (1个): `chrono::nanoseconds`
- **内存操作** (2个): `memcpy`

这些组件在 Blender 源码中广泛用于类型检查、算法实现、文件IO、数学计算等场景。

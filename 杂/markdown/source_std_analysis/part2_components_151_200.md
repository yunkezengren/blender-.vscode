# C++标准库组件详细分析 (第151-200)

## 151. std::polar - 极坐标转复数

### 功能说明
`std::polar` 函数模板用于从极坐标创建复数。它接受模（幅度）和辐角（角度），返回对应的复数。

**函数签名：**
```cpp
template< class T >
complex<T> polar( const T& rho, const T& theta = T() );
```

### 使用场景
- 信号处理：将信号从极坐标形式转换为复数形式
- 图形学：处理旋转和缩放变换
- 物理模拟：处理波动和振动
- 通信系统：调制解调算法

### 代码示例
```cpp
#include <iostream>
#include <complex>
#include <cmath>

int main() {
    // 创建模为5.0，角度为π/4的复数
    double rho = 5.0;
    double theta = M_PI / 4;  // 45度
    
    std::complex<double> c = std::polar(rho, theta);
    
    std::cout << "极坐标: rho=" << rho << ", theta=" << theta << std::endl;
    std::cout << "复数形式: " << c << std::endl;
    std::cout << "实部: " << c.real() << std::endl;
    std::cout << "虚部: " << c.imag() << std::endl;
    
    // 验证：sqrt(2)/2 * 5 ≈ 3.535
    std::cout << "\n验证: 5 * cos(45°) = " << 5 * std::cos(theta) << std::endl;
    std::cout << "验证: 5 * sin(45°) = " << 5 * std::sin(theta) << std::endl;
    
    // 创建单位圆上的点
    std::cout << "\n单位圆上的点:" << std::endl;
    for (int i = 0; i < 8; ++i) {
        double angle = 2 * M_PI * i / 8;
        auto point = std::polar(1.0, angle);
        std::cout << "  角度 " << i * 45 << "°: " << point << std::endl;
    }
    
    return 0;
}
```

---

## 152. std::is_trivially_move_constructible_v - 检查平凡移动构造

### 功能说明
`std::is_trivially_move_constructible_v` 是C++17引入的变量模板，用于在编译期检查类型是否具有平凡的移动构造函数。

**定义：**
```cpp
template< class T >
inline constexpr bool is_trivially_move_constructible_v = 
    is_trivially_move_constructible<T>::value;
```

### 使用场景
- 模板元编程：优化容器实现
- 性能优化：确定是否可以使用memmove
- 概念约束（C++20）：限制模板参数类型
- 序列化库：确定高效序列化策略

### 代码示例
```cpp
#include <iostream>
#include <type_traits>
#include <string>
#include <vector>

struct Trivial {
    int x;
    double y;
};

struct NonTrivial {
    std::string s;
    NonTrivial(NonTrivial&& other) : s(std::move(other.s)) {}
};

struct Virtual {
    virtual void foo() {}
    int x;
};

int main() {
    std::cout << "平凡移动构造检查:" << std::endl;
    
    // 基本类型
    std::cout << "int: " << std::is_trivially_move_constructible_v<int> << std::endl;
    std::cout << "double: " << std::is_trivially_move_constructible_v<double> << std::endl;
    
    // 平凡结构体
    std::cout << "Trivial: " << std::is_trivially_move_constructible_v<Trivial> << std::endl;
    
    // 非平凡结构体
    std::cout << "NonTrivial: " << std::is_trivially_move_constructible_v<NonTrivial> << std::endl;
    
    // 有虚函数的类
    std::cout << "Virtual: " << std::is_trivially_move_constructible_v<Virtual> << std::endl;
    
    // 标准容器
    std::cout << "std::string: " << std::is_trivially_move_constructible_v<std::string> << std::endl;
    std::cout << "std::vector<int>: " << std::is_trivially_move_constructible_v<std::vector<int>> << std::endl;
    
    // 数组
    std::cout << "int[10]: " << std::is_trivially_move_constructible_v<int[10]> << std::endl;
    
    return 0;
}
```

---

## 153. std::is_copy_constructible_v - 检查拷贝构造

### 功能说明
`std::is_copy_constructible_v` 是C++17引入的变量模板，用于在编译期检查类型是否可以被拷贝构造。

### 使用场景
- 模板约束：确保类型可复制
- 容器适配：判断能否存储到需要拷贝的容器中
- 编译期多态：根据可拷贝性选择实现

### 代码示例
```cpp
#include <iostream>
#include <type_traits>
#include <memory>

class Copyable {
public:
    Copyable() = default;
    Copyable(const Copyable&) = default;
};

class NonCopyable {
public:
    NonCopyable() = default;
    NonCopyable(const NonCopyable&) = delete;
};

int main() {
    std::cout << "拷贝构造检查:" << std::endl;
    
    std::cout << "int: " << std::is_copy_constructible_v<int> << std::endl;
    std::cout << "Copyable: " << std::is_copy_constructible_v<Copyable> << std::endl;
    std::cout << "NonCopyable: " << std::is_copy_constructible_v<NonCopyable> << std::endl;
    std::cout << "std::unique_ptr<int>: " << std::is_copy_constructible_v<std::unique_ptr<int>> << std::endl;
    std::cout << "std::shared_ptr<int>: " << std::is_copy_constructible_v<std::shared_ptr<int>> << std::endl;
    
    return 0;
}
```

---

## 154. std::ios::ate - 打开时定位到末尾标志

### 功能说明
`std::ios::ate` 是文件打开模式标志，表示在打开文件后立即将文件指针定位到文件末尾。

### 使用场景
- 日志系统：打开现有日志并定位到末尾
- 数据追加：先查看已有内容，再在末尾添加新数据
- 数据库文件：管理可变长度记录

### 代码示例
```cpp
#include <iostream>
#include <fstream>
#include <string>

int main() {
    const char* filename = "example_ate.txt";
    
    // 先创建一些初始内容
    {
        std::ofstream init(filename);
        init << "Line 1: Initial data\n";
        init << "Line 2: More initial data\n";
    }
    
    // 使用 ate 模式打开，初始定位到末尾
    std::fstream file(filename, std::ios::in | std::ios::out | std::ios::ate);
    
    if (!file.is_open()) {
        std::cerr << "Failed to open file" << std::endl;
        return 1;
    }
    
    // 获取当前位置（文件大小）
    auto end_pos = file.tellg();
    std::cout << "File size: " << end_pos << " bytes" << std::endl;
    
    // 追加内容
    file << "Line 3: Appended data\n";
    
    // 回到开头读取
    file.seekg(0, std::ios::beg);
    std::cout << "\nFull file content:" << std::endl;
    std::string line;
    while (std::getline(file, line)) {
        std::cout << line << std::endl;
    }
    
    return 0;
}
```

---

## 155. std::from_chars_result - from_chars结果结构

### 功能说明
`std::from_chars_result` 是 `std::from_chars` 函数返回的结构体，包含解析结果的指针和错误码。

**结构定义：**
```cpp
struct from_chars_result {
    const char* ptr;      // 指向第一个未转换字符
    std::errc ec;         // 错误码
};
```

### 使用场景
- 高性能解析：替代atoi/stoi，无异常开销
- 网络协议解析：解析文本协议中的数字
- 大数据处理：批量转换大量数字字符串

### 代码示例
```cpp
#include <iostream>
#include <charconv>
#include <system_error>

int main() {
    const char* str = "12345";
    int value = 0;
    
    auto result = std::from_chars(str, str + strlen(str), value);
    
    std::cout << "Input: " << str << std::endl;
    std::cout << "Parsed value: " << value << std::endl;
    std::cout << "Success: " << (result.ec == std::errc{}) << std::endl;
    
    // 处理错误情况
    const char* invalid = "abc";
    int val2 = 0;
    auto result2 = std::from_chars(invalid, invalid + 3, val2);
    
    if (result2.ec == std::errc::invalid_argument) {
        std::cout << "Invalid argument" << std::endl;
    }
    
    return 0;
}
```

---

## 156. std::filesystem::path - 文件系统路径(C++17)

### 功能说明
`std::filesystem::path` 是C++17引入的类，用于表示和操作文件系统路径。提供跨平台的路径处理能力。

### 使用场景
- 跨平台文件操作
- 配置文件路径管理
- 日志系统路径处理
- 批量文件处理工具

### 代码示例
```cpp
#include <iostream>
#include <filesystem>

namespace fs = std::filesystem;

int main() {
    // 创建路径
    fs::path p1 = "/home/user/documents/file.txt";
    fs::path p2 = "relative/path/to/file.txt";
    
    std::cout << "Path: " << p1 << std::endl;
    std::cout << "Root name: " << p1.root_name() << std::endl;
    std::cout << "Parent path: " << p1.parent_path() << std::endl;
    std::cout << "Filename: " << p1.filename() << std::endl;
    std::cout << "Stem: " << p1.stem() << std::endl;
    std::cout << "Extension: " << p1.extension() << std::endl;
    
    // 路径操作
    fs::path base = "/home/user";
    fs::path sub = "documents/projects";
    fs::path full = base / sub / "main.cpp";
    std::cout << "\nCombined: " << full << std::endl;
    
    // 规范化路径
    fs::path messy = "/home/user/../user/./documents//file.txt";
    std::cout << "Normalized: " << messy.lexically_normal() << std::endl;
    
    return 0;
}
```

---

## 157. std::false_type - false类型常量

### 功能说明
`std::false_type` 是标准库提供的类型，继承自 `std::integral_constant<bool, false>`。常用于模板元编程中表示"假"的编译期布尔值。

### 使用场景
- 类型特征（Type Traits）基础
- SFINAE技术
- 编译期条件选择
- 自定义类型检查

### 代码示例
```cpp
#include <iostream>
#include <type_traits>

// 使用 false_type 作为 traits 的默认实现
template<typename T>
struct is_my_special_type : std::false_type {};

// 为特定类型特化
template<>
struct is_my_special_type<int> : std::true_type {};

int main() {
    std::cout << "false_type::value = " << std::false_type::value << std::endl;
    std::cout << "true_type::value = " << std::true_type::value << std::endl;
    
    std::cout << "is_my_special_type<int>: " << is_my_special_type<int>::value << std::endl;
    std::cout << "is_my_special_type<float>: " << is_my_special_type<float>::value << std::endl;
    
    return 0;
}
```

---

## 158. std::exchange - 交换并返回值(C++14)

### 功能说明
`std::exchange` 是C++14引入的实用函数，用于将变量设置为新值，同时返回变量的旧值。

### 使用场景
- 移动构造函数：转移资源所有权
- 状态标志重置：原子地获取并重置标志
- 默认值处理：获取值并设置默认值

### 代码示例
```cpp
#include <iostream>
#include <utility>
#include <memory>

class ResourceOwner {
    int* data_;
    size_t size_;
    
public:
    ResourceOwner(size_t size) : data_(new int[size]), size_(size) {}
    
    // 移动构造函数
    ResourceOwner(ResourceOwner&& other) noexcept
        : data_(std::exchange(other.data_, nullptr))
        , size_(std::exchange(other.size_, 0)) {}
    
    ~ResourceOwner() { delete[] data_; }
};

int main() {
    int x = 10;
    int old_x = std::exchange(x, 20);
    std::cout << "Old value: " << old_x << ", New value: " << x << std::endl;
    
    // 与智能指针一起使用
    std::unique_ptr<int> ptr = std::make_unique<int>(100);
    auto old_ptr = std::exchange(ptr, std::make_unique<int>(200));
    std::cout << "Old pointer value: " << *old_ptr << std::endl;
    std::cout << "New pointer value: " << *ptr << std::endl;
    
    return 0;
}
```

---

## 159. std::chrono::steady_clock - 单调时钟

### 功能说明
`std::chrono::steady_clock` 是一个单调时钟类，保证时间只向前推进，不受系统时间调整的影响。

### 使用场景
- 性能基准测试
- 超时控制
- 帧率计算
- 动画计时

### 代码示例
```cpp
#include <iostream>
#include <chrono>
#include <thread>

using namespace std::chrono;

int main() {
    // 基本计时
    auto start = steady_clock::now();
    std::this_thread::sleep_for(milliseconds(100));
    auto end = steady_clock::now();
    
    auto elapsed = duration_cast<microseconds>(end - start);
    std::cout << "Elapsed: " << elapsed.count() << " microseconds" << std::endl;
    
    // 时钟特性
    std::cout << "\nsteady_clock is steady: " << steady_clock::is_steady << std::endl;
    std::cout << "system_clock is steady: " << system_clock::is_steady << std::endl;
    
    return 0;
}
```

---

## 160. std::begin - 获取容器/数组起始迭代器

### 功能说明
`std::begin` 是一个函数模板，用于获取容器或数组的起始迭代器。使得可以统一处理标准容器和原始数组。

### 使用场景
- 泛型编程：统一处理容器和数组
- 范围for循环的基础
- 模板函数中遍历任意序列

### 代码示例
```cpp
#include <iostream>
#include <vector>
#include <array>

template<typename Container>
void print_all(const Container& c) {
    std::cout << "[";
    for (auto it = std::begin(c); it != std::end(c); ++it) {
        if (it != std::begin(c)) std::cout << ", ";
        std::cout << *it;
    }
    std::cout << "]" << std::endl;
}

int main() {
    std::vector<int> vec = {1, 2, 3, 4, 5};
    std::array<double, 4> arr = {1.1, 2.2, 3.3, 4.4};
    int c_array[] = {10, 20, 30, 40, 50};
    
    print_all(vec);
    print_all(arr);
    print_all(c_array);
    
    return 0;
}
```

---

## 161. std::back_inserter - 后向插入迭代器

### 功能说明
`std::back_inserter` 创建一个输出迭代器，在调用赋值操作时会在容器末尾插入元素。

### 使用场景
- 算法输出到动态扩展的容器
- 过滤并收集元素
- 转换并存储结果

### 代码示例
```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <iterator>

int main() {
    std::vector<int> source = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    std::vector<int> destination;
    
    // 复制所有元素
    std::copy(source.begin(), source.end(), std::back_inserter(destination));
    
    std::cout << "Copied: ";
    for (int x : destination) std::cout << x << " ";
    std::cout << std::endl;
    
    // 过滤偶数
    std::vector<int> evens;
    std::copy_if(source.begin(), source.end(), 
                 std::back_inserter(evens),
                 [](int x) { return x % 2 == 0; });
    
    std::cout << "Even numbers: ";
    for (int x : evens) std::cout << x << " ";
    std::cout << std::endl;
    
    return 0;
}
```

---

## 162. std::tie - 创建tuple引用

### 功能说明
`std::tie` 创建一个tuple的左值引用，允许将多个变量绑定到一起，常用于多值返回和解构赋值。

### 使用场景
- 多值返回解包
- 结构化绑定（C++17之前）
- 比较多个值
- 批量赋值

### 代码示例
```cpp
#include <iostream>
#include <tuple>
#include <string>

std::tuple<int, bool, std::string> get_user_info(int id) {
    if (id == 1) {
        return std::make_tuple(25, true, "Alice");
    }
    return std::make_tuple(0, false, "Unknown");
}

int main() {
    int age;
    bool active;
    std::string name;
    
    // 解包tuple
    std::tie(age, active, name) = get_user_info(1);
    std::cout << "User: " << name << ", Age: " << age 
              << ", Active: " << (active ? "Yes" : "No") << std::endl;
    
    // 忽略不需要的值
    std::tie(std::ignore, std::ignore, name) = get_user_info(1);
    std::cout << "Name only: " << name << std::endl;
    
    return 0;
}
```

---

## 163. std::thread - 线程类

### 功能说明
`std::thread` 是C++11引入的线程类，提供了对操作系统线程的封装。允许创建和管理并发执行的线程。

### 使用场景
- 并行计算
- 异步任务处理
- 后台服务
- 生产者-消费者模式

### 代码示例
```cpp
#include <iostream>
#include <thread>
#include <vector>
#include <mutex>

std::mutex mtx;

void worker(int id) {
    std::lock_guard<std::mutex> lock(mtx);
    std::cout << "Thread " << id << " is working" << std::endl;
}

int main() {
    std::cout << "Hardware concurrency: " << std::thread::hardware_concurrency() << std::endl;
    
    std::vector<std::thread> threads;
    
    // 创建多个线程
    for (int i = 0; i < 4; ++i) {
        threads.emplace_back(worker, i);
    }
    
    // 等待所有线程完成
    for (auto& t : threads) {
        t.join();
    }
    
    std::cout << "All threads completed" << std::endl;
    return 0;
}
```

---

## 164. std::streamsize - 流大小类型

### 功能说明
`std::streamsize` 是带符号整数类型，用于表示I/O操作中传输的字符数或I/O缓冲区大小。

### 使用场景
- 指定读写操作的字符数
- 设置流缓冲区大小
- 报告I/O操作结果

### 代码示例
```cpp
#include <iostream>
#include <vector>

int main() {
    std::cout << "sizeof(std::streamsize) = " << sizeof(std::streamsize) << std::endl;
    
    // 格式化输出宽度
    std::stringstream ss;
    std::streamsize width = 20;
    ss.width(width);
    ss << std::left << "Hello";
    std::cout << "Formatted output: '" << ss.str() << "'" << std::endl;
    
    return 0;
}
```

---

## 165. std::stoi - 字符串转int

### 功能说明
`std::stoi` 将字符串转换为整数，支持自动检测基数、处理前导空白和符号。

### 使用场景
- 配置文件解析
- 命令行参数处理
- 用户输入验证

### 代码示例
```cpp
#include <iostream>
#include <string>

int main() {
    std::string str1 = "12345";
    std::string str2 = "  -42  ";
    std::string str3 = "0xFF";
    
    std::cout << "stoi(\"12345\") = " << std::stoi(str1) << std::endl;
    std::cout << "stoi(\"  -42  \") = " << std::stoi(str2) << std::endl;
    std::cout << "stoi(\"0xFF\", nullptr, 0) = " << std::stoi(str3, nullptr, 0) << std::endl;
    
    // 不同进制
    std::string hex = "FF";
    std::string bin = "101010";
    std::cout << "Hex FF = " << std::stoi(hex, nullptr, 16) << std::endl;
    std::cout << "Bin 101010 = " << std::stoi(bin, nullptr, 2) << std::endl;
    
    return 0;
}
```

---

## 166. std::rotate - 旋转元素范围

### 功能说明
`std::rotate` 将范围中的元素向左旋转，使得指定位置的元素成为新的首元素。

### 使用场景
- 数组轮转算法
- 滑动窗口实现
- 循环缓冲区操作

### 代码示例
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

template<typename Container>
void print(const Container& c, const std::string& label = "") {
    if (!label.empty()) std::cout << label << ": ";
    std::cout << "[";
    for (auto it = c.begin(); it != c.end(); ++it) {
        if (it != c.begin()) std::cout << ", ";
        std::cout << *it;
    }
    std::cout << "]" << std::endl;
}

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5};
    
    print(v, "Original");
    
    std::rotate(v.begin(), v.begin() + 2, v.end());
    print(v, "After rotate");
    
    return 0;
}
```

---

## 167. std::reduce - 并行归约(C++17)

### 功能说明
`std::reduce` 是C++17引入的并行算法，对范围内的元素进行归约操作。可以并行执行，要求二元操作满足结合律。

### 使用场景
- 大规模数据求和
- 并行统计计算
- 大数据集聚合

### 代码示例
```cpp
#include <iostream>
#include <vector>
#include <numeric>
#include <execution>

int main() {
    std::vector<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    
    // 串行累加
    int sum1 = std::accumulate(numbers.begin(), numbers.end(), 0);
    std::cout << "Sum (accumulate): " << sum1 << std::endl;
    
    // 并行归约
    int sum2 = std::reduce(std::execution::par, 
                           numbers.begin(), numbers.end(), 0);
    std::cout << "Sum (reduce): " << sum2 << std::endl;
    
    // 乘积
    int product = std::reduce(numbers.begin(), numbers.end(), 1, std::multiplies<>());
    std::cout << "Product: " << product << std::endl;
    
    return 0;
}
```

---

## 168. std::plus - 加法函数对象

### 功能说明
`std::plus` 是标准库提供的函数对象类，实现二元加法操作。

### 使用场景
- 泛型算法参数
- 自定义累加器
- 函数组合

### 代码示例
```cpp
#include <iostream>
#include <vector>
#include <numeric>
#include <functional>

int main() {
    std::plus<int> add_int;
    std::plus<> add_generic;  // C++14 泛型版本
    
    std::cout << "add_int(3, 4) = " << add_int(3, 4) << std::endl;
    std::cout << "add_generic(5, 6.5) = " << add_generic(5, 6.5) << std::endl;
    
    // 与 accumulate 一起使用
    std::vector<int> numbers = {1, 2, 3, 4, 5};
    int sum = std::accumulate(numbers.begin(), numbers.end(), 0, std::plus<>());
    std::cout << "Sum: " << sum << std::endl;
    
    return 0;
}
```

---

## 169. std::next - 递增迭代器

### 功能说明
`std::next` 返回给定迭代器向前移动n个位置后的迭代器。

### 使用场景
- 获取容器中特定位置的元素
- 处理不支持随机访问的容器
- 安全的迭代器前进

### 代码示例
```cpp
#include <iostream>
#include <vector>
#include <list>

int main() {
    std::vector<int> vec = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    
    auto it1 = std::next(vec.begin(), 5);
    std::cout << "Element at index 5: " << *it1 << std::endl;
    
    // 对不支持随机访问的容器
    std::list<int> lst = {10, 20, 30, 40, 50};
    auto lit = std::next(lst.begin(), 3);
    std::cout << "Element at index 3 in list: " << *lit << std::endl;
    
    return 0;
}
```

---

## 170. std::mt19937 - Mersenne Twister随机数引擎

### 功能说明
`std::mt19937` 是Mersenne Twister伪随机数生成器的32位实现。以极高的周期和良好的统计特性著称。

### 使用场景
- 科学模拟
- 游戏开发
- 蒙特卡洛方法
- 统计抽样

### 代码示例
```cpp
#include <iostream>
#include <random>
#include <vector>
#include <algorithm>

int main() {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(1, 100);
    
    std::cout << "5 random numbers: ";
    for (int i = 0; i < 5; ++i) {
        std::cout << dis(gen) << " ";
    }
    std::cout << std::endl;
    
    // 可重复的随机序列
    std::mt19937 gen1(42);
    std::mt19937 gen2(42);
    std::cout << "\nReproducible sequence:" << std::endl;
    for (int i = 0; i < 5; ++i) {
        std::cout << dis(gen1) << " " << dis(gen2) << std::endl;
    }
    
    return 0;
}
```

---

## 171. std::memcmp - 内存比较

### 功能说明
`std::memcmp` 比较两个内存区域的字节内容。

### 使用场景
- 二进制数据比较
- 网络协议数据验证
- 原始缓冲区操作

### 代码示例
```cpp
#include <iostream>
#include <cstring>

int main() {
    char buf1[] = "Hello World";
    char buf2[] = "Hello World";
    char buf3[] = "Hello C++";
    
    int result1 = std::memcmp(buf1, buf2, strlen(buf1));
    int result2 = std::memcmp(buf1, buf3, strlen(buf1));
    
    std::cout << "buf1 vs buf2: " << result1 << " (" 
              << (result1 == 0 ? "equal" : "different") << ")" << std::endl;
    std::cout << "buf1 vs buf3: " << result2 << " ("
              << (result2 == 0 ? "equal" : "different") << ")" << std::endl;
    
    return 0;
}
```

---

## 172. std::log - 自然对数

### 功能说明
`std::log` 计算给定数值的自然对数（以e为底）。

### 使用场景
- 科学计算
- 数据分析和统计
- 信息论（熵计算）
- 复利计算

### 代码示例
```cpp
#include <iostream>
#include <cmath>

int main() {
    std::cout << "log(1) = " << std::log(1.0) << std::endl;
    std::cout << "log(e) = " << std::log(M_E) << std::endl;
    std::cout << "log(10) = " << std::log(10.0) << std::endl;
    
    // 计算任意底的对数
    auto log_base = [](double x, double base) {
        return std::log(x) / std::log(base);
    };
    
    std::cout << "log2(8) = " << log_base(8.0, 2.0) << std::endl;
    std::cout << "log10(100) = " << log_base(100.0, 10.0) << std::endl;
    
    return 0;
}
```

---

## 173. std::isdigit - 检查数字字符

### 功能说明
`std::isdigit` 检查字符是否为数字字符（'0'-'9'）。

### 使用场景
- 输入验证
- 解析器实现
- 字符串处理

### 代码示例
```cpp
#include <iostream>
#include <cctype>
#include <string>

bool is_all_digits(const std::string& str) {
    for (char c : str) {
        if (!std::isdigit(static_cast<unsigned char>(c))) {
            return false;
        }
    }
    return !str.empty();
}

int main() {
    std::string tests[] = {"12345", "12a45", "", "0"};
    
    for (const auto& s : tests) {
        std::cout << "'" << s << "' is all digits: " 
                  << (is_all_digits(s) ? "yes" : "no") << std::endl;
    }
    
    return 0;
}
```

---

## 174. std::isalnum - 检查字母数字字符

### 功能说明
`std::isalnum` 检查字符是否为字母或数字。

### 使用场景
- 标识符验证
- 密码强度检查
- 词法分析

### 代码示例
```cpp
#include <iostream>
#include <cctype>
#include <string>

bool is_valid_identifier(const std::string& str) {
    if (str.empty() || std::isdigit(static_cast<unsigned char>(str[0]))) {
        return false;
    }
    for (char c : str) {
        if (!std::isalnum(static_cast<unsigned char>(c)) && c != '_') {
            return false;
        }
    }
    return true;
}

int main() {
    std::string tests[] = {"var1", "1var", "hello_world", "hello-world"};
    
    for (const auto& s : tests) {
        std::cout << "'" << s << "' is valid identifier: "
                  << (is_valid_identifier(s) ? "yes" : "no") << std::endl;
    }
    
    return 0;
}
```

---

## 175. std::is_arithmetic_v - 检查算术类型

### 功能说明
`std::is_arithmetic_v` 检查类型是否为算术类型（整数或浮点）。

### 使用场景
- 模板约束
- 类型验证
- 泛型算法实现

### 代码示例
```cpp
#include <iostream>
#include <type_traits>

template<typename T>
void process_arithmetic(T value) {
    static_assert(std::is_arithmetic_v<T>, "Type must be arithmetic");
    std::cout << "Processing: " << value << std::endl;
}

int main() {
    std::cout << "int is arithmetic: " << std::is_arithmetic_v<int> << std::endl;
    std::cout << "double is arithmetic: " << std::is_arithmetic_v<double> << std::endl;
    std::cout << "std::string is arithmetic: " << std::is_arithmetic_v<std::string> << std::endl;
    
    process_arithmetic(42);
    process_arithmetic(3.14);
    // process_arithmetic("hello");  // 编译错误
    
    return 0;
}
```

---

## 176. std::ios_base::binary - 二进制模式

### 功能说明
`std::ios_base::binary` 是以二进制模式打开文件的标志。

### 使用场景
- 二进制文件读写
- 数据序列化
- 图像/音频文件处理

### 代码示例
```cpp
#include <iostream>
#include <fstream>
#include <vector>

int main() {
    const char* filename = "binary_data.bin";
    
    // 写入二进制数据
    {
        std::ofstream file(filename, std::ios::binary);
        std::vector<int> data = {1, 2, 3, 4, 5};
        file.write(reinterpret_cast<const char*>(data.data()), 
                   data.size() * sizeof(int));
    }
    
    // 读取二进制数据
    {
        std::ifstream file(filename, std::ios::binary);
        std::vector<int> data(5);
        file.read(reinterpret_cast<char*>(data.data()), 
                  data.size() * sizeof(int));
        
        std::cout << "Read data: ";
        for (int x : data) std::cout << x << " ";
        std::cout << std::endl;
    }
    
    return 0;
}
```

---

## 177. std::ios::beg - 流的起始位置

### 功能说明
`std::ios::beg` 表示相对于文件开头的位置，用于seek操作。

### 使用场景
- 文件定位
- 随机访问文件
- 二进制文件操作

### 代码示例
```cpp
#include <iostream>
#include <fstream>

int main() {
    const char* filename = "seek_test.txt";
    
    // 创建测试文件
    {
        std::ofstream out(filename);
        out << "ABCDEFGHIJ";
    }
    
    std::fstream file(filename);
    
    // 定位到第5个字符
    file.seekg(5, std::ios::beg);
    char c;
    file.get(c);
    std::cout << "Character at position 5: " << c << std::endl;
    
    // 回到开头
    file.seekg(0, std::ios::beg);
    file.get(c);
    std::cout << "Character at position 0: " << c << std::endl;
    
    return 0;
}
```

---

## 178. std::enable_if_t - 条件模板启用

### 功能说明
`std::enable_if_t` 是 `std::enable_if` 的类型别名，用于条件模板启用（SFINAE）。

### 使用场景
- 条件模板特化
- 重载决议控制
- 编译期多态

### 代码示例
```cpp
#include <iostream>
#include <type_traits>

// 仅对整数类型启用
template<typename T>
std::enable_if_t<std::is_integral_v<T>, T>
add(T a, T b) {
    return a + b;
}

// 仅对浮点类型启用
template<typename T>
std::enable_if_t<std::is_floating_point_v<T>, T>
add(T a, T b) {
    return a + b;
}

int main() {
    std::cout << "add(3, 4) = " << add(3, 4) << std::endl;
    std::cout << "add(3.5, 4.5) = " << add(3.5, 4.5) << std::endl;
    // add("a", "b");  // 编译错误
    
    return 0;
}
```

---

## 179. std::dynamic_pointer_cast - 动态指针转换

### 功能说明
`std::dynamic_pointer_cast` 对 `std::shared_ptr` 执行动态类型转换。

### 使用场景
- 多态类型安全转换
- 类层次结构导航
- RTTI操作

### 代码示例
```cpp
#include <iostream>
#include <memory>

class Base {
public:
    virtual ~Base() = default;
    virtual void print() const { std::cout << "Base" << std::endl; }
};

class Derived : public Base {
public:
    void print() const override { std::cout << "Derived" << std::endl; }
    void derived_only() const { std::cout << "Derived specific method" << std::endl; }
};

int main() {
    std::shared_ptr<Base> base = std::make_shared<Derived>();
    base->print();
    
    // 安全向下转换
    if (auto derived = std::dynamic_pointer_cast<Derived>(base)) {
        std::cout << "Conversion successful" << std::endl;
        derived->derived_only();
    }
    
    // 失败的转换
    std::shared_ptr<Base> real_base = std::make_shared<Base>();
    if (auto derived = std::dynamic_pointer_cast<Derived>(real_base)) {
        std::cout << "This won't print" << std::endl;
    } else {
        std::cout << "Conversion failed (expected)" << std::endl;
    }
    
    return 0;
}
```

---

## 180. std::condition_variable - 条件变量

### 功能说明
`std::condition_variable` 用于线程间同步，允许线程等待特定条件变为真。

### 使用场景
- 生产者-消费者模式
- 线程池任务调度
- 等待-通知机制

### 代码示例
```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <queue>

std::queue<int> data_queue;
std::mutex mtx;
std::condition_variable cv;
bool finished = false;

void producer() {
    for (int i = 0; i < 5; ++i) {
        {
            std::lock_guard<std::mutex> lock(mtx);
            data_queue.push(i);
            std::cout << "Produced: " << i << std::endl;
        }
        cv.notify_one();
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
    
    {
        std::lock_guard<std::mutex> lock(mtx);
        finished = true;
    }
    cv.notify_all();
}

void consumer() {
    while (true) {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [] { return !data_queue.empty() || finished; });
        
        while (!data_queue.empty()) {
            int value = data_queue.front();
            data_queue.pop();
            lock.unlock();
            std::cout << "Consumed: " << value << std::endl;
            lock.lock();
        }
        
        if (finished && data_queue.empty()) {
            break;
        }
    }
}

int main() {
    std::thread prod(producer);
    std::thread cons(consumer);
    
    prod.join();
    cons.join();
    
    std::cout << "Done" << std::endl;
    return 0;
}
```

---

## 181. std::chrono::microseconds - 微秒时长

### 功能说明
`std::chrono::microseconds` 表示微秒（百万分之一秒）的时间长度。

### 使用场景
- 高精度计时
- 性能分析
- 实时系统

### 代码示例
```cpp
#include <iostream>
#include <chrono>
#include <thread>

using namespace std::chrono;

int main() {
    // 创建微秒时长
    microseconds us1(1000);
    microseconds us2 = 500us;  // C++14后缀
    
    std::cout << "us1: " << us1.count() << " microseconds" << std::endl;
    std::cout << "us2: " << us2.count() << " microseconds" << std::endl;
    
    // 转换
    std::cout << "us1 in milliseconds: " 
              << duration_cast<milliseconds>(us1).count() << std::endl;
    
    // 高精度计时
    auto start = steady_clock::now();
    std::this_thread::sleep_for(100us);
    auto elapsed = duration_cast<microseconds>(steady_clock::now() - start);
    std::cout << "Elapsed: " << elapsed.count() << " us" << std::endl;
    
    return 0;
}
```

---

## 182. std::uninitialized_copy_n - 未初始化复制n个元素

### 功能说明
`std::uninitialized_copy_n` 将n个元素复制到未初始化的内存区域。

### 使用场景
- 自定义容器实现
- 内存池管理
- 高性能复制

### 代码示例
```cpp
#include <iostream>
#include <memory>
#include <vector>

int main() {
    std::vector<int> source = {1, 2, 3, 4, 5};
    
    // 分配未初始化内存
    int* dest = static_cast<int*>(std::malloc(source.size() * sizeof(int)));
    
    // 复制到未初始化内存
    std::uninitialized_copy_n(source.begin(), source.size(), dest);
    
    std::cout << "Copied values: ";
    for (size_t i = 0; i < source.size(); ++i) {
        std::cout << dest[i] << " ";
    }
    std::cout << std::endl;
    
    // 手动析构（因为是在malloc内存上构造的）
    for (size_t i = 0; i < source.size(); ++i) {
        dest[i].~int();
    }
    std::free(dest);
    
    return 0;
}
```

---

## 183. std::transform - 变换元素范围

### 功能说明
`std::transform` 对范围内的每个元素应用操作，并将结果存储到另一个范围。

### 使用场景
- 数据转换
- 批量计算
- 字符串处理

### 代码示例
```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <cctype>

int main() {
    std::vector<int> numbers = {1, 2, 3, 4, 5};
    std::vector<int> squares;
    
    // 转换为平方
    std::transform(numbers.begin(), numbers.end(),
                   std::back_inserter(squares),
                   [](int x) { return x * x; });
    
    std::cout << "Squares: ";
    for (int x : squares) std::cout << x << " ";
    std::cout << std::endl;
    
    // 字符串转换
    std::string str = "Hello World";
    std::transform(str.begin(), str.end(), str.begin(), ::toupper);
    std::cout << "Uppercase: " << str << std::endl;
    
    // 二元变换
    std::vector<int> a = {1, 2, 3};
    std::vector<int> b = {10, 20, 30};
    std::vector<int> sums(a.size());
    
    std::transform(a.begin(), a.end(), b.begin(), sums.begin(),
                   std::plus<>());
    
    std::cout << "Sums: ";
    for (int x : sums) std::cout << x << " ";
    std::cout << std::endl;
    
    return 0;
}
```

---

## 184. std::thread::id - 线程ID类型

### 功能说明
`std::thread::id` 表示线程的唯一标识符。

### 使用场景
- 线程标识
- 调试和日志
- 线程本地存储关联

### 代码示例
```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <map>

std::mutex mtx;
std::map<std::thread::id, int> thread_data;

void worker(int value) {
    auto id = std::this_thread::get_id();
    
    {
        std::lock_guard<std::mutex> lock(mtx);
        thread_data[id] = value;
        std::cout << "Thread " << id << " stored value " << value << std::endl;
    }
    
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

int main() {
    std::thread t1(worker, 1);
    std::thread t2(worker, 2);
    
    std::cout << "Main thread ID: " << std::this_thread::get_id() << std::endl;
    std::cout << "Thread 1 ID: " << t1.get_id() << std::endl;
    std::cout << "Thread 2 ID: " << t2.get_id() << std::endl;
    
    t1.join();
    t2.join();
    
    std::cout << "\nThread data:" << std::endl;
    for (const auto& [id, value] : thread_data) {
        std::cout << "Thread " << id << ": " << value << std::endl;
    }
    
    return 0;
}
```

---

## 185. std::system_category - 系统错误类别

### 功能说明
`std::system_category` 返回系统错误类别的单例对象，用于解释系统错误码。

### 使用场景
- 错误处理
- 系统调用错误解释
- 跨平台错误代码

### 代码示例
```cpp
#include <iostream>
#include <system_error>
#include <cerrno>

int main() {
    const auto& category = std::system_category();
    
    // 解释系统错误码
    std::error_code ec(EACCES, category);
    std::cout << "Error code " << ec.value() << ": " << ec.message() << std::endl;
    
    ec.assign(ENOENT, category);
    std::cout << "Error code " << ec.value() << ": " << ec.message() << std::endl;
    
    // 从errno创建
    errno = EAGAIN;
    ec = std::error_code(errno, std::system_category());
    std::cout << "Current error: " << ec.message() << std::endl;
    
    return 0;
}
```

---

## 186. std::string_literals - 字符串字面量命名空间(C++14)

### 功能说明
`std::string_literals` 命名空间提供了字符串字面量后缀操作符，用于创建 `std::string` 和 `std::string_view`。

### 使用场景
- 方便的字符串创建
- 与string类的操作
- 模板编程

### 代码示例
```cpp
#include <iostream>
#include <string>
#include <string_view>

using namespace std::string_literals;
using namespace std::string_view_literals;

int main() {
    // 创建std::string
    auto str1 = "Hello"s;  // std::string
    auto str2 = "World"s;
    
    std::cout << "Type of str1: " << typeid(str1).name() << std::endl;
    std::cout << str1 + " " + str2 << std::endl;
    
    // 创建std::string_view
    auto sv1 = "Hello"sv;  // std::string_view
    std::cout << "Type of sv1: " << typeid(sv1).name() << std::endl;
    
    // 结合使用
    std::string combined = "Prefix: "s + "text"sv;
    std::cout << combined << std::endl;
    
    return 0;
}
```

---

## 187. std::strerror - 获取错误字符串

### 功能说明
`std::strerror` 返回描述错误码的字符串。

### 使用场景
- 系统错误诊断
- 调试输出
- 用户友好的错误信息

### 代码示例
```cpp
#include <iostream>
#include <cstring>
#include <cerrno>
#include <fstream>

int main() {
    // 直接查询错误码
    std::cout << "Error 0 (Success): " << std::strerror(0) << std::endl;
    std::cout << "Error ENOENT (2): " << std::strerror(ENOENT) << std::endl;
    std::cout << "Error EACCES (13): " << std::strerror(EACCES) << std::endl;
    
    // 实际错误场景
    errno = 0;
    std::ifstream file("/nonexistent/file.txt");
    if (!file) {
        std::cout << "\nFailed to open file: " << std::strerror(errno) << std::endl;
    }
    
    return 0;
}
```

---

## 188. std::set_union - 集合并集

### 功能说明
`std::set_union` 计算两个已排序范围的并集。

### 使用场景
- 集合操作
- 数据合并
- 去重组合

### 代码示例
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> set1 = {1, 2, 3, 5, 7};
    std::vector<int> set2 = {2, 4, 5, 6, 8};
    std::vector<int> result;
    
    std::set_union(set1.begin(), set1.end(),
                   set2.begin(), set2.end(),
                   std::back_inserter(result));
    
    std::cout << "Union: ";
    for (int x : result) std::cout << x << " ";
    std::cout << std::endl;
    
    // 检查是否有重复元素
    std::cout << "Set 1 is sorted: " 
              << std::is_sorted(set1.begin(), set1.end()) << std::endl;
    
    return 0;
}
```

---

## 189. std::set_difference - 集合差集

### 功能说明
`std::set_difference` 计算两个已排序范围的差集。

### 使用场景
- 集合操作
- 数据筛选
- 增量更新

### 代码示例
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> set1 = {1, 2, 3, 4, 5, 6};
    std::vector<int> set2 = {2, 4, 6, 8};
    std::vector<int> diff;
    
    // set1 - set2
    std::set_difference(set1.begin(), set1.end(),
                        set2.begin(), set2.end(),
                        std::back_inserter(diff));
    
    std::cout << "Difference (set1 - set2): ";
    for (int x : diff) std::cout << x << " ";
    std::cout << std::endl;
    
    // 双向差集（对称差）
    std::vector<int> sym_diff;
    std::set_symmetric_difference(set1.begin(), set1.end(),
                                  set2.begin(), set2.end(),
                                  std::back_inserter(sym_diff));
    
    std::cout << "Symmetric difference: ";
    for (int x : sym_diff) std::cout << x << " ";
    std::cout << std::endl;
    
    return 0;
}
```

---

## 190. std::remove_if - 条件移除元素

### 功能说明
`std::remove_if` 从范围内移除满足条件的元素（逻辑移除，需要配合erase使用）。

### 使用场景
- 条件删除
- 数据清理
- 过滤元素

### 代码示例
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    
    std::cout << "Original: ";
    for (int x : numbers) std::cout << x << " ";
    std::cout << std::endl;
    
    // 移除偶数（erase-remove惯用法）
    auto new_end = std::remove_if(numbers.begin(), numbers.end(),
                                  [](int x) { return x % 2 == 0; });
    numbers.erase(new_end, numbers.end());
    
    std::cout << "After removing evens: ";
    for (int x : numbers) std::cout << x << " ";
    std::cout << std::endl;
    
    // 另一种方法：使用std::erase_if (C++20)
    // std::erase_if(numbers, [](int x) { return x > 5; });
    
    return 0;
}
```

---

## 191. std::recursive_mutex - 递归互斥锁

### 功能说明
`std::recursive_mutex` 是递归互斥锁，允许同一线程多次加锁而不死锁。

### 使用场景
- 递归函数中的同步
- 复杂锁层次结构
- 回调函数中的锁定

### 代码示例
```cpp
#include <iostream>
#include <thread>
#include <recursive_mutex>

class RecursiveData {
    std::recursive_mutex mtx;
    int value = 0;
    
public:
    void increment() {
        std::lock_guard<std::recursive_mutex> lock(mtx);
        ++value;
    }
    
    void add(int n) {
        std::lock_guard<std::recursive_mutex> lock(mtx);
        for (int i = 0; i < n; ++i) {
            increment();  // 递归加锁
        }
    }
    
    int get() {
        std::lock_guard<std::recursive_mutex> lock(mtx);
        return value;
    }
};

int main() {
    RecursiveData data;
    
    std::thread t1([&data] {
        data.add(5);
        std::cout << "Thread 1: value = " << data.get() << std::endl;
    });
    
    std::thread t2([&data] {
        data.add(3);
        std::cout << "Thread 2: value = " << data.get() << std::endl;
    });
    
    t1.join();
    t2.join();
    
    std::cout << "Final value: " << data.get() << std::endl;
    
    return 0;
}
```

---

## 192. std::nullptr_t - nullptr类型

### 功能说明
`std::nullptr_t` 是 `nullptr` 的类型。

### 使用场景
- 函数重载区分
- 模板特化
- 类型特征

### 代码示例
```cpp
#include <iostream>
#include <type_traits>

void func(int) {
    std::cout << "Called func(int)" << std::endl;
}

void func(std::nullptr_t) {
    std::cout << "Called func(nullptr_t)" << std::endl;
}

void func(void*) {
    std::cout << "Called func(void*)" << std::endl;
}

template<typename T>
struct is_nullptr : std::false_type {};

template<>
struct is_nullptr<std::nullptr_t> : std::true_type {};

int main() {
    func(0);           // func(int)
    func(nullptr);     // func(nullptr_t)
    func((void*)0);    // func(void*)
    
    std::cout << "\nis_nullptr<int>: " << is_nullptr<int>::value << std::endl;
    std::cout << "is_nullptr<std::nullptr_t>: " << is_nullptr<std::nullptr_t>::value << std::endl;
    
    return 0;
}
```

---

## 193. std::none_of - 检查无元素满足条件

### 功能说明
`std::none_of` 检查范围内是否没有任何元素满足给定条件。

### 使用场景
- 验证所有元素都不满足条件
- 数据验证
- 安全检查

### 代码示例
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> numbers = {2, 4, 6, 8, 10};
    
    // 检查是否没有奇数
    bool no_odds = std::none_of(numbers.begin(), numbers.end(),
                                [](int x) { return x % 2 != 0; });
    
    std::cout << "No odd numbers: " << (no_odds ? "true" : "false") << std::endl;
    
    // 检查是否没有负数
    bool no_negatives = std::none_of(numbers.begin(), numbers.end(),
                                     [](int x) { return x < 0; });
    
    std::cout << "No negative numbers: " << (no_negatives ? "true" : "false") << std::endl;
    
    // 结合all_of使用
    bool all_even = std::all_of(numbers.begin(), numbers.end(),
                                [](int x) { return x % 2 == 0; });
    
    // 这两个条件是等价的
    std::cout << "All even == None odd: " << (all_even == no_odds) << std::endl;
    
    return 0;
}
```

---

## 194. std::memory_order_release - 释放内存序

### 功能说明
`std::memory_order_release` 是内存序标记，用于写操作，确保之前的读写操作不会被重排到后面。

### 使用场景
- 生产者-消费者同步
- 锁的自由实现
- 单例模式（双重检查锁定）

### 代码示例
```cpp
#include <iostream>
#include <atomic>
#include <thread>

std::atomic<int*> data(nullptr);
std::atomic<int> flag(0);

void producer() {
    int* p = new int(42);
    
    // 先写数据
    data.store(p, std::memory_order_relaxed);
    
    // 再设置标志（release语义）
    flag.store(1, std::memory_order_release);
}

void consumer() {
    // 等待标志（acquire语义）
    while (flag.load(std::memory_order_acquire) != 1) {
        // 自旋等待
    }
    
    // 保证能看到producer在release之前的所有写入
    int* p = data.load(std::memory_order_relaxed);
    std::cout << "Got value: " << *p << std::endl;
    
    delete p;
}

int main() {
    std::thread t1(producer);
    std::thread t2(consumer);
    
    t1.join();
    t2.join();
    
    return 0;
}
```

---

## 195. std::lower_bound - 下界查找

### 功能说明
`std::lower_bound` 在已排序范围内查找第一个不小于给定值的元素。

### 使用场景
- 二分查找
- 有序容器操作
- 范围查询

### 代码示例
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> sorted = {1, 3, 5, 7, 9, 11, 13, 15};
    
    // 查找 lower_bound
    auto it = std::lower_bound(sorted.begin(), sorted.end(), 7);
    if (it != sorted.end()) {
        std::cout << "Lower bound of 7: " << *it << " (index " 
                  << (it - sorted.begin()) << ")" << std::endl;
    }
    
    // 查找不存在的元素
    it = std::lower_bound(sorted.begin(), sorted.end(), 8);
    if (it != sorted.end()) {
        std::cout << "Lower bound of 8: " << *it << " (index " 
                  << (it - sorted.begin()) << ")" << std::endl;
    }
    
    // 插入位置
    int value = 6;
    it = std::lower_bound(sorted.begin(), sorted.end(), value);
    std::cout << "Insert " << value << " at position " 
              << (it - sorted.begin()) << std::endl;
    
    return 0;
}
```

---

## 196. std::logical_or - 逻辑或函数对象

### 功能说明
`std::logical_or` 是标准库提供的函数对象类，实现逻辑或操作。

### 使用场景
- 泛型算法参数
- 条件组合
- 谓词构建

### 代码示例
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::logical_or<bool> logical_or;
    
    std::cout << "true || false = " << logical_or(true, false) << std::endl;
    std::cout << "false || false = " << logical_or(false, false) << std::endl;
    
    // 结合transform使用
    std::vector<bool> a = {true, false, true, false};
    std::vector<bool> b = {false, true, true, false};
    std::vector<bool> result(a.size());
    
    std::transform(a.begin(), a.end(), b.begin(), result.begin(),
                   std::logical_or<>());
    
    std::cout << "\nLogical OR results: ";
    for (bool x : result) std::cout << x << " ";
    std::cout << std::endl;
    
    return 0;
}
```

---

## 197. std::is_trivially_copy_constructible_v - 检查平凡拷贝构造

### 功能说明
`std::is_trivially_copy_constructible_v` 检查类型是否具有平凡的拷贝构造函数。

### 使用场景
- 优化拷贝操作
- 确定是否可以使用memcpy
- 模板元编程

### 代码示例
```cpp
#include <iostream>
#include <type_traits>
#include <string>

struct Trivial {
    int x;
    double y;
};

struct NonTrivial {
    std::string s;
};

int main() {
    std::cout << "int: " << std::is_trivially_copy_constructible_v<int> << std::endl;
    std::cout << "Trivial: " << std::is_trivially_copy_constructible_v<Trivial> << std::endl;
    std::cout << "NonTrivial: " << std::is_trivially_copy_constructible_v<NonTrivial> << std::endl;
    std::cout << "std::string: " << std::is_trivially_copy_constructible_v<std::string> << std::endl;
    
    return 0;
}
```

---

## 198. std::is_enum_v - 检查枚举类型

### 功能说明
`std::is_enum_v` 检查类型是否为枚举类型。

### 使用场景
- 类型约束
- 枚举特化
- 序列化支持

### 代码示例
```cpp
#include <iostream>
#include <type_traits>

enum class Color { Red, Green, Blue };
enum Status { OK, Error };

class MyClass {};

int main() {
    std::cout << "int is enum: " << std::is_enum_v<int> << std::endl;
    std::cout << "Color is enum: " << std::is_enum_v<Color> << std::endl;
    std::cout << "Status is enum: " << std::is_enum_v<Status> << std::endl;
    std::cout << "MyClass is enum: " << std::is_enum_v<MyClass> << std::endl;
    
    return 0;
}
```

---

## 199. std::ios_base::openmode - 打开模式类型

### 功能说明
`std::ios_base::openmode` 是文件打开模式的类型。

### 使用场景
- 文件流操作
- 封装文件操作
- 配置打开模式

### 代码示例
```cpp
#include <iostream>
#include <fstream>

void open_file(const char* filename, std::ios_base::openmode mode) {
    std::fstream file(filename, mode);
    if (file.is_open()) {
        std::cout << "File opened successfully with mode" << std::endl;
        file.close();
    }
}

int main() {
    // 不同的打开模式
    open_file("test1.txt", std::ios::out);                    // 写入模式
    open_file("test2.txt", std::ios::in | std::ios::out);     // 读写模式
    open_file("test3.txt", std::ios::app);                    // 追加模式
    open_file("test4.txt", std::ios::binary | std::ios::out); // 二进制写入
    
    return 0;
}
```

---

## 200. std::ios_base::app - 追加模式标志

### 功能说明
`std::ios_base::app` 是以追加模式打开文件的标志，所有写入都在文件末尾。

### 使用场景
- 日志文件写入
- 追加数据到现有文件
- 防止数据覆盖

### 代码示例
```cpp
#include <iostream>
#include <fstream>

int main() {
    const char* filename = "log.txt";
    
    // 第一次写入
    {
        std::ofstream file(filename, std::ios::app);
        file << "Log entry 1" << std::endl;
    }
    
    // 第二次追加
    {
        std::ofstream file(filename, std::ios::app);
        file << "Log entry 2" << std::endl;
    }
    
    // 读取并显示
    {
        std::ifstream file(filename);
        std::cout << "Log file contents:" << std::endl;
        std::string line;
        while (std::getline(file, line)) {
            std::cout << line << std::endl;
        }
    }
    
    return 0;
}
```

---

*文档结束 - 共50个C++标准库组件详细分析*

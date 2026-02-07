# C++标准库组件分析 (101-150)

本文档详细分析50个C++标准库组件，包含功能说明、使用场景和完整代码示例。

---

## 101. std::replace - 替换范围内的元素

### 功能说明
`std::replace` 是 C++ 标准库 `<algorithm>` 头文件中的算法，用于将指定范围内的所有等于某个值的元素替换为新值。

```cpp
template<class ForwardIt, class T>
void replace(ForwardIt first, ForwardIt last, const T& old_value, const T& new_value);
```

### 使用场景
- 批量修改容器中特定值的数据
- 数据清洗和标准化处理
- 状态转换

### 代码示例

```cpp
#include <algorithm>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> data = {1, 2, 3, 2, 4, 2, 5};
    
    std::cout << "原始数据: ";
    for (int x : data) std::cout << x << " ";
    std::cout << "\n";
    
    std::replace(data.begin(), data.end(), 2, 99);
    
    std::cout << "替换后: ";
    for (int x : data) std::cout << x << " ";
    std::cout << "\n";
    
    return 0;
}
```

---

## 102. std::regex - 正则表达式库

### 功能说明
`std::regex` 是 C++11 引入的正则表达式库，位于 `<regex>` 头文件中。

### 使用场景
- 表单输入验证
- 日志文件解析
- 文本搜索和替换

### 代码示例

```cpp
#include <regex>
#include <string>
#include <iostream>

int main() {
    std::string email = "user@example.com";
    std::regex pattern(R"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})");
    
    if (std::regex_match(email, pattern)) {
        std::cout << "有效的邮箱\n";
    }
    
    return 0;
}
```

---

## 103. std::ios::in - 输入模式标志

### 功能说明
`std::ios::in` 是文件打开模式标志，用于指定以输入模式打开文件。

### 使用场景
- 显式指定只读模式
- 组合实现读写模式

### 代码示例

```cpp
#include <fstream>
#include <iostream>
#include <string>

int main() {
    std::ofstream out("test.txt");
    out << "Hello\nWorld";
    out.close();
    
    std::ifstream in("test.txt", std::ios::in);
    std::string line;
    while (std::getline(in, line)) {
        std::cout << line << "\n";
    }
    
    std::remove("test.txt");
    return 0;
}
```

---

## 104. std::hex - 十六进制格式操纵符

### 功能说明
`std::hex` 用于将整数以十六进制格式进行输入输出。

### 使用场景
- 内存地址显示
- 颜色值表示
- 二进制数据可视化

### 代码示例

```cpp
#include <iostream>
#include <iomanip>

int main() {
    int value = 255;
    
    std::cout << "十进制: " << value << "\n";
    std::cout << "十六进制: " << std::hex << value << "\n";
    std::cout << "带前缀: " << std::showbase << 255 << "\n";
    
    return 0;
}
```

---

## 105. std::exception - 标准异常基类

### 功能说明
`std::exception` 是所有标准异常的基类，提供 `what()` 虚函数。

### 使用场景
- 创建自定义异常
- 统一异常处理

### 代码示例

```cpp
#include <exception>
#include <iostream>
#include <string>

class MyException : public std::exception {
    std::string msg;
public:
    MyException(const std::string& m) : msg(m) {}
    const char* what() const noexcept override { return msg.c_str(); }
};

int main() {
    try {
        throw MyException("Custom error");
    } catch (const std::exception& e) {
        std::cout << "Exception: " << e.what() << "\n";
    }
    return 0;
}
```

---

## 106. std::conditional_t - 条件类型选择

### 功能说明
根据布尔条件在编译期选择两种类型之一。

### 使用场景
- 模板元编程
- 类型选择

### 代码示例

```cpp
#include <type_traits>
#include <iostream>

template<bool B>
using IntOrFloat = std::conditional_t<B, int, float>;

int main() {
    IntOrFloat<true> a = 10;
    IntOrFloat<false> b = 3.14f;
    
    std::cout << "a=" << a << ", b=" << b << "\n";
    return 0;
}
```

---

## 107. std::max_element - 查找最大元素

### 功能说明
返回指向范围内最大元素的迭代器。

### 代码示例

```cpp
#include <algorithm>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> v = {3, 1, 4, 1, 5, 9};
    auto it = std::max_element(v.begin(), v.end());
    std::cout << "Max: " << *it << " at position " << std::distance(v.begin(), it) << "\n";
    return 0;
}
```

---

## 108. std::istream - 输入流基类

### 功能说明
所有输入流的基类。

### 代码示例

```cpp
#include <iostream>
#include <sstream>

int main() {
    std::istringstream iss("10 20 30");
    int n;
    while (iss >> n) {
        std::cout << n << " ";
    }
    return 0;
}
```

---

## 109. std::isnan - 检查NaN

### 功能说明
检查浮点数是否为非数字。

### 代码示例

```cpp
#include <cmath>
#include <iostream>
#include <limits>

int main() {
    double nan = std::numeric_limits<double>::quiet_NaN();
    double normal = 3.14;
    
    std::cout << std::boolalpha;
    std::cout << "isnan(NaN): " << std::isnan(nan) << "\n";
    std::cout << "isnan(3.14): " << std::isnan(normal) << "\n";
    return 0;
}
```

---

## 110. std::iota - 填充递增序列

### 功能说明
用连续递增的值填充范围。

### 代码示例

```cpp
#include <numeric>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> v(5);
    std::iota(v.begin(), v.end(), 10);
    
    for (int x : v) std::cout << x << " ";
    return 0;
}
```

---

## 111. std::equal - 比较两个范围

### 功能说明
比较两个范围内的元素是否相等。

### 代码示例

```cpp
#include <algorithm>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> a = {1, 2, 3};
    std::vector<int> b = {1, 2, 3};
    std::vector<int> c = {1, 2, 4};
    
    std::cout << std::boolalpha;
    std::cout << "a==b: " << std::equal(a.begin(), a.end(), b.begin()) << "\n";
    std::cout << "a==c: " << std::equal(a.begin(), a.end(), c.begin()) << "\n";
    return 0;
}
```

---

## 112. std::distance - 计算迭代器距离

### 功能说明
计算两个迭代器之间的元素个数。

### 代码示例

```cpp
#include <iterator>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> v = {10, 20, 30, 40, 50};
    auto it = v.begin() + 3;
    
    std::cout << "Distance from begin: " << std::distance(v.begin(), it) << "\n";
    return 0;
}
```

---

## 113. std::count - 计数元素出现次数

### 功能说明
统计范围内等于特定值的元素个数。

### 代码示例

```cpp
#include <algorithm>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> v = {1, 2, 2, 3, 2, 4};
    auto cnt = std::count(v.begin(), v.end(), 2);
    std::cout << "Number 2 appears " << cnt << " times\n";
    return 0;
}
```

---

## 114. std::set - 有序唯一集合容器

### 功能说明
存储唯一元素的有序关联容器。

### 代码示例

```cpp
#include <set>
#include <iostream>

int main() {
    std::set<int> s = {3, 1, 4, 1, 5};
    
    std::cout << "Set: ";
    for (int x : s) std::cout << x << " ";
    std::cout << "\n";
    
    if (s.find(4) != s.end()) {
        std::cout << "Found 4\n";
    }
    return 0;
}
```

---

## 115. std::fixed - 定点数格式操纵符

### 功能说明
设置浮点数定点表示法。

### 代码示例

```cpp
#include <iostream>
#include <iomanip>

int main() {
    double pi = 3.14159;
    
    std::cout << "Default: " << pi << "\n";
    std::cout << "Fixed: " << std::fixed << pi << "\n";
    std::cout << "Precision 2: " << std::setprecision(2) << pi << "\n";
    return 0;
}
```

---

## 116. std::ceil - 向上取整

### 功能说明
返回不小于参数的最小整数。

### 代码示例

```cpp
#include <cmath>
#include <iostream>

int main() {
    std::cout << "ceil(2.3)=" << std::ceil(2.3) << "\n";
    std::cout << "ceil(2.9)=" << std::ceil(2.9) << "\n";
    std::cout << "ceil(-2.3)=" << std::ceil(-2.3) << "\n";
    return 0;
}
```

---

## 117. std::upper_bound - 上界查找

### 功能说明
返回指向第一个大于给定值的元素的迭代器。

### 代码示例

```cpp
#include <algorithm>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> v = {1, 3, 5, 7, 9};
    auto it = std::upper_bound(v.begin(), v.end(), 5);
    std::cout << "Upper bound of 5: " << *it << "\n";
    return 0;
}
```

---

## 118. std::system_error - 系统错误异常

### 功能说明
用于报告系统级错误。

### 代码示例

```cpp
#include <system_error>
#include <iostream>
#include <fstream>

int main() {
    try {
        std::ifstream f("nonexistent");
        if (!f) {
            throw std::system_error(
                std::make_error_code(std::errc::no_such_file_or_directory)
            );
        }
    } catch (const std::system_error& e) {
        std::cout << "Error: " << e.what() << "\n";
    }
    return 0;
}
```

---

## 119. std::floor - 向下取整

### 功能说明
返回不大于参数的最大整数。

### 代码示例

```cpp
#include <cmath>
#include <iostream>

int main() {
    std::cout << "floor(2.3)=" << std::floor(2.3) << "\n";
    std::cout << "floor(2.9)=" << std::floor(2.9) << "\n";
    std::cout << "floor(-2.3)=" << std::floor(-2.3) << "\n";
    return 0;
}
```

---

## 120. std::count_if - 条件计数

### 功能说明
统计满足谓词条件的元素个数。

### 代码示例

```cpp
#include <algorithm>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5, 6};
    auto even = std::count_if(v.begin(), v.end(), 
                              [](int x) { return x % 2 == 0; });
    std::cout << "Even numbers: " << even << "\n";
    return 0;
}
```

---

## 121. std::span - 连续序列视图(C++20)

### 功能说明
轻量级非拥有视图，提供对连续内存序列的安全访问。

### 代码示例

```cpp
#include <span>
#include <vector>
#include <iostream>

void print(std::span<const int> s) {
    for (int x : s) std::cout << x << " ";
    std::cout << "\n";
}

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5};
    print(v);
    
    int arr[] = {10, 20, 30};
    print(arr);
    return 0;
}
```

---

## 122. std::multiset - 有序可重复集合

### 功能说明
允许存储重复键值的有序关联容器。

### 代码示例

```cpp
#include <set>
#include <iostream>

int main() {
    std::multiset<int> ms = {3, 1, 4, 1, 5};
    
    for (int x : ms) std::cout << x << " ";
    std::cout << "\n";
    
    std::cout << "Count of 1: " << ms.count(1) << "\n";
    return 0;
}
```

---

## 123. std::make_move_iterator - 移动迭代器

### 功能说明
创建移动迭代器包装器。

### 代码示例

```cpp
#include <iterator>
#include <vector>
#include <string>
#include <iostream>

int main() {
    std::vector<std::string> src = {"Hello", "World"};
    std::vector<std::string> dst(
        std::make_move_iterator(src.begin()),
        std::make_move_iterator(src.end())
    );
    
    std::cout << "Destination: ";
    for (const auto& s : dst) std::cout << s << " ";
    return 0;
}
```

---

## 124. std::make_index_sequence - 创建索引序列

### 功能说明
创建编译期整数序列。

### 代码示例

```cpp
#include <utility>
#include <tuple>
#include <iostream>

template<typename Tuple, size_t... Is>
void print_impl(const Tuple& t, std::index_sequence<Is...>) {
    ((std::cout << std::get<Is>(t) << " "), ...);
}

template<typename Tuple>
void print_tuple(const Tuple& t) {
    print_impl(t, std::make_index_sequence<std::tuple_size_v<Tuple>>{});
}

int main() {
    auto t = std::make_tuple(1, 2.0, "hello");
    print_tuple(t);
    return 0;
}
```

---

## 125. std::isfinite - 检查有限数

### 功能说明
检查浮点数是否为有限值。

### 代码示例

```cpp
#include <cmath>
#include <iostream>
#include <limits>

int main() {
    double finite = 3.14;
    double inf = std::numeric_limits<double>::infinity();
    
    std::cout << std::boolalpha;
    std::cout << "isfinite(3.14): " << std::isfinite(finite) << "\n";
    std::cout << "isfinite(inf): " << std::isfinite(inf) << "\n";
    return 0;
}
```

---

## 126. std::ifstream - 输入文件流

### 功能说明
用于从文件读取数据的输入流类。

### 代码示例

```cpp
#include <fstream>
#include <iostream>
#include <string>

int main() {
    std::ofstream("test.txt") << "Hello\nWorld";
    
    std::ifstream in("test.txt");
    std::string line;
    while (std::getline(in, line)) {
        std::cout << line << "\n";
    }
    
    std::remove("test.txt");
    return 0;
}
```

---

## 127. std::errc::result_out_of_range - 结果超出范围错误

### 功能说明
表示数值转换结果超出范围的错误码。

### 代码示例

```cpp
#include <system_error>
#include <iostream>
#include <charconv>
#include <string>

int main() {
    std::string big = "99999999999999999999";
    int result;
    
    auto [ptr, ec] = std::from_chars(big.data(), big.data() + big.size(), result);
    
    if (ec == std::errc::result_out_of_range) {
        std::cout << "Value out of range\n";
    }
    return 0;
}
```

---

## 128. std::errc::invalid_argument - 无效参数错误

### 功能说明
表示无效参数的错误码。

### 代码示例

```cpp
#include <system_error>
#include <iostream>
#include <charconv>
#include <string>

int main() {
    std::string invalid = "abc";
    int result;
    
    auto [ptr, ec] = std::from_chars(invalid.data(), invalid.data() + invalid.size(), result);
    
    if (ec == std::errc::invalid_argument) {
        std::cout << "Invalid argument\n";
    }
    return 0;
}
```

---

## 129. std::end - 获取容器/数组尾后迭代器

### 功能说明
返回容器或数组的尾后迭代器。

### 代码示例

```cpp
#include <iterator>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> v = {1, 2, 3};
    
    for (auto it = std::begin(v); it != std::end(v); ++it) {
        std::cout << *it << " ";
    }
    return 0;
}
```

---

## 130. std::derived_from - 派生关系概念(C++20)

### 功能说明
检查一个类型是否派生自另一个类型。

### 代码示例

```cpp
#include <concepts>
#include <iostream>

class Base {};
class Derived : public Base {};

int main() {
    std::cout << std::boolalpha;
    std::cout << "Derived from Base: " 
              << std::derived_from<Derived, Base> << "\n";
    return 0;
}
```

---

## 131. std::true_type - true类型常量

### 功能说明
表示布尔值true的类型形式。

### 代码示例

```cpp
#include <type_traits>
#include <iostream>

template<typename T>
struct is_int : std::false_type {};

template<>
struct is_int<int> : std::true_type {};

int main() {
    std::cout << "is_int<int>: " << is_int<int>::value << "\n";
    std::cout << "is_int<double>: " << is_int<double>::value << "\n";
    return 0;
}
```

---

## 132. std::this_thread::get_id - 获取当前线程ID

### 功能说明
返回当前线程的唯一标识符。

### 代码示例

```cpp
#include <thread>
#include <iostream>

int main() {
    std::cout << "Main thread ID: " << std::this_thread::get_id() << "\n";
    
    std::thread t([]() {
        std::cout << "Worker thread ID: " << std::this_thread::get_id() << "\n";
    });
    
    t.join();
    return 0;
}
```

---

## 133. std::tan - 正切函数

### 功能说明
计算给定角度的正切值。

### 代码示例

```cpp
#include <cmath>
#include <iostream>

const double PI = 3.14159265359;

int main() {
    std::cout << "tan(0)=" << std::tan(0) << "\n";
    std::cout << "tan(45°)=" << std::tan(PI/4) << "\n";
    return 0;
}
```

---

## 134. std::string::traits_type::length - 字符特性长度

### 功能说明
计算以空字符结尾的字符数组长度。

### 代码示例

```cpp
#include <string>
#include <iostream>

int main() {
    using traits = std::string::traits_type;
    
    const char* str = "Hello";
    std::cout << "Length: " << traits::length(str) << "\n";
    return 0;
}
```

---

## 135. std::size - 获取容器大小(C++17)

### 功能说明
统一获取容器、数组或初始化列表的大小。

### 代码示例

```cpp
#include <iterator>
#include <vector>
#include <array>
#include <iostream>

int main() {
    std::vector<int> v = {1, 2, 3};
    int arr[] = {1, 2, 3, 4, 5};
    
    std::cout << "vector size: " << std::size(v) << "\n";
    std::cout << "array size: " << std::size(arr) << "\n";
    return 0;
}
```

---

## 136. std::setfill - 设置填充字符

### 功能说明
设置输出流中的填充字符。

### 代码示例

```cpp
#include <iostream>
#include <iomanip>

int main() {
    std::cout << "[" << std::setw(10) << 42 << "]\n";
    std::cout << "[" << std::setfill('0') << std::setw(10) << 42 << "]\n";
    return 0;
}
```

---

## 137. std::remove_reference_t - 移除引用类型

### 功能说明
移除类型的引用修饰符。

### 代码示例

```cpp
#include <type_traits>
#include <iostream>

int main() {
    using T1 = std::remove_reference_t<int&>;
    using T2 = std::remove_reference_t<int&&>;
    
    static_assert(std::is_same_v<T1, int>);
    static_assert(std::is_same_v<T2, int>);
    
    std::cout << "Reference removed\n";
    return 0;
}
```

---

## 138. std::remove_pointer_t - 移除指针类型

### 功能说明
移除类型的指针修饰符。

### 代码示例

```cpp
#include <type_traits>
#include <iostream>

int main() {
    using T1 = std::remove_pointer_t<int*>;
    using T2 = std::remove_pointer_t<int**>;
    
    static_assert(std::is_same_v<T1, int>);
    static_assert(std::is_same_v<T2, int*>);
    
    std::cout << "Pointer removed\n";
    return 0;
}
```

---

## 139. std::regex_replace - 正则替换

### 功能说明
使用正则表达式进行字符串替换。

### 代码示例

```cpp
#include <regex>
#include <string>
#include <iostream>

int main() {
    std::string text = "Hello World";
    std::regex pattern("World");
    
    std::string result = std::regex_replace(text, pattern, "Universe");
    std::cout << result << "\n";
    return 0;
}
```

---

## 140. std::modf - 分解浮点数

### 功能说明
将浮点数分解为整数部分和小数部分。

### 代码示例

```cpp
#include <cmath>
#include <iostream>

int main() {
    double value = 123.456;
    double intpart;
    
    double frac = std::modf(value, &intpart);
    std::cout << "Int: " << intpart << ", Frac: " << frac << "\n";
    return 0;
}
```

---

## 141. std::min_element - 查找最小元素

### 功能说明
返回指向范围内最小元素的迭代器。

### 代码示例

```cpp
#include <algorithm>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> v = {3, 1, 4, 1, 5};
    auto it = std::min_element(v.begin(), v.end());
    std::cout << "Min: " << *it << "\n";
    return 0;
}
```

---

## 142. std::memory_order_acquire - 获取内存序

### 功能说明
用于加载操作的同步内存顺序。

### 代码示例

```cpp
#include <atomic>
#include <thread>
#include <iostream>

std::atomic<int> data{0};
std::atomic<bool> ready{false};

void producer() {
    data.store(42, std::memory_order_relaxed);
    ready.store(true, std::memory_order_release);
}

void consumer() {
    while (!ready.load(std::memory_order_acquire));
    std::cout << "Data: " << data.load(std::memory_order_relaxed) << "\n";
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

## 143. std::is_pointer_v - 检查指针类型变量模板

### 功能说明
检查类型是否为指针类型。

### 代码示例

```cpp
#include <type_traits>
#include <iostream>

int main() {
    std::cout << std::boolalpha;
    std::cout << "is_pointer_v<int>: " << std::is_pointer_v<int> << "\n";
    std::cout << "is_pointer_v<int*>: " << std::is_pointer_v<int*> << "\n";
    return 0;
}
```

---

## 144. std::fstream - 文件流

### 功能说明
支持读写操作的文件流类。

### 代码示例

```cpp
#include <fstream>
#include <iostream>
#include <string>

int main() {
    // 写入
    std::fstream file("test.txt", std::ios::out);
    file << "Hello World";
    file.close();
    
    // 读取
    file.open("test.txt", std::ios::in);
    std::string content;
    file >> content;
    std::cout << content << "\n";
    
    std::remove("test.txt");
    return 0;
}
```

---

## 145. std::from_chars - 字符转数字(C++17)

### 功能说明
高效字符串转数字函数。

### 代码示例

```cpp
#include <charconv>
#include <iostream>
#include <string_view>

int main() {
    std::string_view str = "12345";
    int result;
    
    auto [ptr, ec] = std::from_chars(str.data(), str.data() + str.size(), result);
    
    if (ec == std::errc()) {
        std::cout << "Result: " << result << "\n";
    }
    return 0;
}
```

---

## 146. std::forward_iterator_tag - 前向迭代器标签

### 功能说明
表示前向迭代器的类别标签。

### 代码示例

```cpp
#include <iterator>
#include <vector>
#include <forward_list>
#include <iostream>

template<typename It>
void check_category() {
    using cat = typename std::iterator_traits<It>::iterator_category;
    if constexpr (std::is_same_v<cat, std::forward_iterator_tag>) {
        std::cout << "Forward iterator\n";
    }
}

int main() {
    check_category<std::forward_list<int>::iterator>();
    return 0;
}
```

---

## 147. std::find - 查找元素

### 功能说明
在范围内查找等于指定值的元素。

### 代码示例

```cpp
#include <algorithm>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5};
    auto it = std::find(v.begin(), v.end(), 3);
    
    if (it != v.end()) {
        std::cout << "Found at position " << std::distance(v.begin(), it) << "\n";
    }
    return 0;
}
```

---

## 148. std::bitset - 位集合

### 功能说明
固定大小位序列容器。

### 代码示例

```cpp
#include <bitset>
#include <iostream>

int main() {
    std::bitset<8> bits("10101010");
    
    std::cout << "Bits: " << bits << "\n";
    std::cout << "Count: " << bits.count() << "\n";
    std::cout << "Test bit 1: " << bits.test(1) << "\n";
    
    return 0;
}
```

---

## 149. std::weak_ptr - 弱智能指针

### 功能说明
不增加引用计数的弱引用智能指针。

### 代码示例

```cpp
#include <memory>
#include <iostream>

int main() {
    std::shared_ptr<int> sp = std::make_shared<int>(42);
    std::weak_ptr<int> wp = sp;
    
    if (auto locked = wp.lock()) {
        std::cout << "Value: " << *locked << "\n";
    }
    
    sp.reset();
    std::cout << "Expired: " << wp.expired() << "\n";
    
    return 0;
}
```

---

## 150. std::setprecision - 设置浮点精度

### 功能说明
设置浮点数的输出精度。

### 代码示例

```cpp
#include <iostream>
#include <iomanip>

int main() {
    double pi = 3.14159265359;
    
    std::cout << "Default: " << pi << "\n";
    std::cout << "Precision 3: " << std::setprecision(3) << pi << "\n";
    std::cout << "Fixed: " << std::fixed << std::setprecision(2) << pi << "\n";
    
    return 0;
}
```

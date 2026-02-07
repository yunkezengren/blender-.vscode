# C++标准库组件详细分析 (第351-403)

## 目录
- [351. std::nexttowardf](#351-stdnexttowardf)
- [352. std::nextafter](#352-stdnextafter)
- [353. std::multi_map](#353-stdmulti_map)
- [354. std::mt19937_64::min](#354-stdmt19937_64min)
- [355. std::mt19937_64::max](#355-stdmt19937_64max)
- [356. std::midpoint](#356-stdmidpoint)
- [357. std::make_unsigned_t](#357-stdmake_unsigned_t)
- [358. std::make_heap](#358-stdmake_heap)
- [359. std::logical_and](#359-stdlogical_and)
- [360. std::left](#360-stdleft)
- [361. std::lcm](#361-stdlcm)
- [362. std::isinf](#362-stdisinf)
- [363. std::isalpha](#363-stdisalpha)
- [364. std::is_standard_layout_v](#364-stdis_standard_layout_v)
- [365. std::is_layout_compatible](#365-stdis_layout_compatible)
- [366. std::is_invocable_v](#366-stdis_invocable_v)
- [367. std::is_default_constructible_v](#367-stdis_default_constructible_v)
- [368. std::is_constructible_v](#368-stdis_constructible_v)
- [369. std::is_const_v](#369-stdis_const_v)
- [370. std::is_bounded_array_v](#370-stdis_bounded_array_v)
- [371. std::ios_base::fmtflags](#371-stdios_basefmtflags)
- [372. std::ios_base::beg](#372-stdios_basebeg)
- [373. std::ios::trunc](#373-stdiostrunc)
- [374. std::integral_constant](#374-stdintegral_constant)
- [375. std::integer_sequence](#375-stdinteger_sequence)
- [376. std::input_iterator_tag](#376-stdinput_iterator_tag)
- [377. std::hypot](#377-stdhypot)
- [378. std::has_unique_object_representations_v](#378-stdhas_unique_object_representations_v)
- [379. std::gcd](#379-stdgcd)
- [380. std::for_each](#380-stdfor_each)
- [381. std::fminf](#381-stdfminf)
- [382. std::filesystem::recursive_directory_iterator](#382-stdfilesystemrecursive_directory_iterator)
- [383. std::filesystem::exists](#383-stdfilesystemexists)
- [384. std::filesystem::directory_iterator](#384-stdfilesystemdirectory_iterator)
- [385. std::filesystem](#385-stdfilesystem)
- [386. std::equal_to](#386-stdequal_to)
- [387. std::endian::native](#387-stdendinnative)
- [388. std::enable_if](#388-stdenable_if)
- [389. std::destroy_n](#389-stddestroy_n)
- [390. std::default_random_engine](#390-stddefault_random_engine)
- [391. std::copy_backward](#391-stdcopy_backward)
- [392. std::conj](#392-stdconj)
- [393. std::chrono::steady_clock::time_point](#393-stdchronosteady_clocktime_point)
- [394. std::chrono::seconds::period](#394-stdchronosecondsperiod)
- [395. std::chrono::high_resolution_clock::time_point](#395-stdchronohigh_resolution_clocktime_point)
- [396. std::chrono::high_resolution_clock](#396-stdchronohigh_resolution_clock)
- [397. std::chrono::duration](#397-stdchronoduration)
- [398. std::binary_search](#398-stdbinary_search)
- [399. std::atomic_thread_fence](#399-stdatomic_thread_fence)
- [400. std::atomic_size_t](#400-stdatomic_size_t)
- [401. std::allocator](#401-stdallocator)
- [402. std::aligned_alloc](#402-stdaligned_alloc)
- [403. std::addressof](#403-stdaddressof)

---

## 351. std::nexttowardf

### 功能说明
`std::nexttowardf` 返回从第一个参数 `from` 向第二个参数 `toward` 方向的下一个可表示的 `float` 值。如果 `from` 等于 `toward`，则返回 `toward`。

### 使用场景
1. 数值分析算法：精确控制浮点数步进
2. 浮点数比较：找到两个浮点数之间的下一个表示值
3. 边界测试：测试浮点数在边界条件下的行为

### 代码示例

```cpp
#include <iostream>
#include <cmath>

int main() {
    float from = 1.0f;
    float toward = 2.0f;
    float next = std::nexttowardf(from, toward);
    std::cout << "下一个值: " << next << std::endl;
    return 0;
}
```

---

## 352. std::nextafter

### 功能说明
`std::nextafter` 返回从 `from` 向 `to` 方向的下一个可表示的浮点值。有多个重载版本（float、double、long double）。

### 使用场景
1. 跨平台浮点运算：确保浮点数运算一致性
2. 高精度计算：精确控制浮点数的可表示值
3. 数值边界分析：确定浮点数的精度范围

### 代码示例

```cpp
#include <iostream>
#include <cmath>

int main() {
    double d1 = 1.0;
    double d_next = std::nextafter(d1, 2.0);
    std::cout << d1 << " -> " << d_next << std::endl;
    return 0;
}
```

---

## 353. std::multi_map

### 功能说明
**注意：C++标准库中没有 `std::multi_map`。** 用户可能指的是 `std::multimap`，这是一个允许键重复的关联容器。

### 使用场景
1. 多对一关系：一个键对应多个值
2. 重复键存储：存储具有相同标识符的多个记录
3. 范围查询：按键的范围查找所有相关值

### 代码示例

```cpp
#include <iostream>
#include <map>

int main() {
    std::multimap<int, std::string> mm;
    mm.insert({1, "A"});
    mm.insert({1, "B"});
    
    auto range = mm.equal_range(1);
    for (auto it = range.first; it != range.second; ++it) {
        std::cout << it->second << std::endl;
    }
    return 0;
}
```

---

## 354. std::mt19937_64::min

### 功能说明
`std::mt19937_64::min()` 返回 64位梅森旋转算法随机数生成器的最小可能输出值（总是0）。

### 使用场景
1. 随机数范围映射
2. 算法验证

### 代码示例

```cpp
#include <iostream>
#include <random>

int main() {
    std::cout << "min: " << std::mt19937_64::min() << std::endl;
    std::cout << "max: " << std::mt19937_64::max() << std::endl;
    return 0;
}
```

---

## 355. std::mt19937_64::max

### 功能说明
`std::mt19937_64::max()` 返回 64位梅森旋转算法随机数生成器的最大可能输出值（2^64 - 1）。

### 使用场景
1. 64位随机数生成
2. 加密相关应用
3. 科学模拟

### 代码示例

```cpp
#include <iostream>
#include <random>

int main() {
    std::mt19937_64 rng;
    std::cout << "max: " << std::mt19937_64::max() << std::endl;
    std::cout << "random: " << rng() << std::endl;
    return 0;
}
```

---

## 356. std::midpoint

### 功能说明
`std::midpoint` 是 C++20 引入的函数，计算两个值的中点，可避免溢出。

### 使用场景
1. 二分查找：安全地计算中间索引
2. 数值计算：避免大数相加溢出
3. 指针运算：找到两个指针之间的中点

### 代码示例

```cpp
#include <iostream>
#include <numeric>

int main() {
    std::cout << std::midpoint(10, 20) << std::endl;
    
    int arr[] = {0, 1, 2, 3, 4};
    int* mid = std::midpoint(&arr[0], &arr[4]);
    std::cout << "中点值: " << *mid << std::endl;
    return 0;
}
```

---

## 357. std::make_unsigned_t

### 功能说明
`std::make_unsigned_t` 是 C++14 引入的类型特性，将一个有符号整数类型转换为对应的无符号类型。

### 使用场景
1. 类型转换：泛型代码中的无符号转换
2. 位操作：无符号整数更安全

### 代码示例

```cpp
#include <iostream>
#include <type_traits>

int main() {
    using unsigned_int = std::make_unsigned_t<int>;
    std::cout << "int -> unsigned int" << std::endl;
    return 0;
}
```

---

## 358. std::make_heap

### 功能说明
`std::make_heap` 将范围内的元素重新排列为堆结构。默认创建最大堆。

### 使用场景
1. 优先队列：高效的最大/最小元素访问
2. 堆排序：排序算法的基础

### 代码示例

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> heap = {3, 1, 4, 1, 5};
    std::make_heap(heap.begin(), heap.end());
    std::cout << "堆顶: " << heap.front() << std::endl;
    return 0;
}
```

---

## 359. std::logical_and

### 功能说明
`std::logical_and` 是一个函数对象，执行逻辑与操作（`&&`）。

### 使用场景
1. 算法谓词：与 transform 等算法配合
2. 条件组合

### 代码示例

```cpp
#include <iostream>
#include <functional>

int main() {
    std::logical_and<bool> land;
    std::cout << land(true, true) << std::endl;
    std::cout << land(true, false) << std::endl;
    return 0;
}
```

---

## 360. std::left

### 功能说明
`std::left` 是 I/O 操纵符，设置输出流的文本对齐方式为左对齐。

### 使用场景
1. 表格格式化：左对齐数据表格
2. 日志输出：对齐日志字段

### 代码示例

```cpp
#include <iostream>
#include <iomanip>

int main() {
    std::cout << std::left;
    std::cout << std::setw(15) << "Name" << std::setw(10) << "Age" << std::endl;
    return 0;
}
```

---

## 361. std::lcm

### 功能说明
`std::lcm` 是 C++17 引入的函数，计算两个整数的最小公倍数。

### 使用场景
1. 分数运算：通分
2. 周期计算

### 代码示例

```cpp
#include <iostream>
#include <numeric>

int main() {
    std::cout << "lcm(4, 6) = " << std::lcm(4, 6) << std::endl;
    std::cout << "lcm(21, 6) = " << std::lcm(21, 6) << std::endl;
    return 0;
}
```

---

## 362. std::isinf

### 功能说明
`std::isinf` 检查浮点数是否为无穷大。

### 使用场景
1. 数值验证：检查计算结果是否溢出
2. 异常处理

### 代码示例

```cpp
#include <iostream>
#include <cmath>

int main() {
    std::cout << std::isinf(1.0) << std::endl;
    std::cout << std::isinf(INFINITY) << std::endl;
    return 0;
}
```

---

## 363. std::isalpha

### 功能说明
`std::isalpha` 检查字符是否为字母（a-z 或 A-Z）。

### 使用场景
1. 输入验证
2. 文本处理

### 代码示例

```cpp
#include <iostream>
#include <cctype>

int main() {
    std::cout << std::isalpha('A') << std::endl;
    std::cout << std::isalpha('5') << std::endl;
    return 0;
}
```

---

## 364. std::is_standard_layout_v

### 功能说明
`std::is_standard_layout_v` 是 C++17 引入的变量模板，检查类型是否是标准布局类型。

### 使用场景
1. C++与C交互
2. 内存映射文件

### 代码示例

```cpp
#include <iostream>
#include <type_traits>

struct Standard { int x; };
struct NonStandard { virtual void f() {} };

int main() {
    std::cout << std::is_standard_layout_v<Standard> << std::endl;
    std::cout << std::is_standard_layout_v<NonStandard> << std::endl;
    return 0;
}
```

---

## 365. std::is_layout_compatible

### 功能说明
`std::is_layout_compatible` 是 C++20 引入的类型特性，检查两种类型是否是布局兼容的。

### 代码示例

```cpp
#include <iostream>
#include <type_traits>

struct A { int x; float y; };
struct B { int a; float b; };

int main() {
    // C++20
    // std::cout << std::is_layout_compatible_v<A, B> << std::endl;
    return 0;
}
```

---

## 366. std::is_invocable_v

### 功能说明
`std::is_invocable_v` 是 C++17 引入的变量模板，检查类型是否可以用指定参数调用。

### 代码示例

```cpp
#include <iostream>
#include <type_traits>

void func(int) {}

int main() {
    std::cout << std::is_invocable_v<decltype(func), int> << std::endl;
    std::cout << std::is_invocable_v<decltype(func), char*> << std::endl;
    return 0;
}
```

---

## 367. std::is_default_constructible_v

### 功能说明
检查类型是否可默认构造。

### 代码示例

```cpp
#include <iostream>
#include <type_traits>

struct Default { Default() {} };
struct NoDefault { NoDefault(int) {} };

int main() {
    std::cout << std::is_default_constructible_v<Default> << std::endl;
    std::cout << std::is_default_constructible_v<NoDefault> << std::endl;
    return 0;
}
```

---

## 368. std::is_constructible_v

### 功能说明
检查类型是否能用指定参数构造。

### 代码示例

```cpp
#include <iostream>
#include <type_traits>

struct Test {
    Test() {}
    Test(int) {}
};

int main() {
    std::cout << std::is_constructible_v<Test> << std::endl;
    std::cout << std::is_constructible_v<Test, int> << std::endl;
    return 0;
}
```

---

## 369. std::is_const_v

### 功能说明
检查类型是否是 const 限定类型。

### 代码示例

```cpp
#include <iostream>
#include <type_traits>

int main() {
    std::cout << std::is_const_v<int> << std::endl;
    std::cout << std::is_const_v<const int> << std::endl;
    return 0;
}
```

---

## 370. std::is_bounded_array_v

### 功能说明
`std::is_bounded_array_v` 是 C++20 引入的变量模板，检查类型是否是定长数组类型。

### 代码示例

```cpp
#include <iostream>
#include <type_traits>

int main() {
    // C++20
    // std::cout << std::is_bounded_array_v<int[5]> << std::endl;
    // std::cout << std::is_bounded_array_v<int[]> << std::endl;
    return 0;
}
```

---

## 371. std::ios_base::fmtflags

### 功能说明
`std::ios_base::fmtflags` 是用于控制输入输出格式的位掩码类型。

### 使用场景
1. 格式控制：设置数字的进制、精度、宽度
2. 科学计算输出

### 代码示例

```cpp
#include <iostream>

int main() {
    int num = 255;
    std::cout.setf(std::ios::hex, std::ios::basefield);
    std::cout << num << std::endl;
    return 0;
}
```

---

## 372. std::ios_base::beg

### 功能说明
`std::ios_base::beg` 是文件流定位常量，表示相对于文件开头的位置。

### 代码示例

```cpp
#include <iostream>
#include <fstream>

int main() {
    std::ofstream f("test.txt");
    f << "Hello World";
    f.seekp(6, std::ios::beg);
    f << "C++";
    return 0;
}
```

---

## 373. std::ios::trunc

### 功能说明
`std::ios::trunc` 是文件打开模式标志，表示打开文件时截断内容。

### 代码示例

```cpp
#include <iostream>
#include <fstream>

int main() {
    std::ofstream f("file.txt", std::ios::trunc);
    f << "New content";
    return 0;
}
```

---

## 374. std::integral_constant

### 功能说明
`std::integral_constant` 是类型特性的基础模板，用于将编译期常量包装为类型。

### 代码示例

```cpp
#include <iostream>
#include <type_traits>

using five = std::integral_constant<int, 5>;

int main() {
    std::cout << five::value << std::endl;
    return 0;
}
```

---

## 375. std::integer_sequence

### 功能说明
`std::integer_sequence` 是 C++14 引入的模板，表示编译期整数序列。

### 代码示例

```cpp
#include <iostream>
#include <utility>

template<typename T, T... Is>
void print(std::integer_sequence<T, Is...>) {
    ((std::cout << Is << " "), ...);
}

int main() {
    print(std::make_integer_sequence<int, 5>{});
    return 0;
}
```

---

## 376. std::input_iterator_tag

### 功能说明
`std::input_iterator_tag` 用于标识输入迭代器类别。

### 代码示例

```cpp
#include <iostream>
#include <iterator>
#include <vector>

int main() {
    using category = std::iterator_traits<std::vector<int>::iterator>::iterator_category;
    std::cout << std::is_same_v<category, std::random_access_iterator_tag> << std::endl;
    return 0;
}
```

---

## 377. std::hypot

### 功能说明
`std::hypot` 计算斜边长度，即 sqrt(x² + y²)，防止溢出。

### 代码示例

```cpp
#include <iostream>
#include <cmath>

int main() {
    std::cout << std::hypot(3, 4) << std::endl;
    std::cout << std::hypot(1, 2, 2) << std::endl;  // C++17
    return 0;
}
```

---

## 378. std::has_unique_object_representations_v

### 功能说明
`std::has_unique_object_representations_v` 是 C++17 引入的变量模板，检查类型的每个位模式是否都对应唯一的值。

### 代码示例

```cpp
#include <iostream>
#include <type_traits>

struct Unique { int x; };

int main() {
    std::cout << std::has_unique_object_representations_v<Unique> << std::endl;
    return 0;
}
```

---

## 379. std::gcd

### 功能说明
`std::gcd` 是 C++17 引入的函数，计算两个整数的最大公约数。

### 代码示例

```cpp
#include <iostream>
#include <numeric>

int main() {
    std::cout << std::gcd(48, 18) << std::endl;
    std::cout << std::gcd(100, 35) << std::endl;
    return 0;
}
```

---

## 380. std::for_each

### 功能说明
`std::for_each` 对范围内的每个元素应用指定的函数。

### 代码示例

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {1, 2, 3};
    std::for_each(v.begin(), v.end(), [](int x) {
        std::cout << x << " ";
    });
    return 0;
}
```

---

## 381. std::fminf

### 功能说明
`std::fminf` 返回两个 float 值中的较小值，正确处理 NaN。

### 代码示例

```cpp
#include <iostream>
#include <cmath>

int main() {
    std::cout << std::fminf(3.0f, 5.0f) << std::endl;
    std::cout << std::fminf(NAN, 5.0f) << std::endl;
    return 0;
}
```

---

## 382. std::filesystem::recursive_directory_iterator

### 功能说明
C++17 提供的递归目录迭代器，遍历目录及其所有子目录。

### 代码示例

```cpp
#include <iostream>
#include <filesystem>
namespace fs = std::filesystem;

int main() {
    for (const auto& entry : fs::recursive_directory_iterator(".")) {
        std::cout << entry.path() << std::endl;
    }
    return 0;
}
```

---

## 383. std::filesystem::exists

### 功能说明
检查给定的文件系统路径是否存在。

### 代码示例

```cpp
#include <iostream>
#include <filesystem>
namespace fs = std::filesystem;

int main() {
    std::cout << fs::exists(".") << std::endl;
    std::cout << fs::exists("nonexistent") << std::endl;
    return 0;
}
```

---

## 384. std::filesystem::directory_iterator

### 功能说明
C++17 提供的目录迭代器，遍历目录中的直接子条目。

### 代码示例

```cpp
#include <iostream>
#include <filesystem>
namespace fs = std::filesystem;

int main() {
    for (const auto& entry : fs::directory_iterator(".")) {
        std::cout << entry.path().filename() << std::endl;
    }
    return 0;
}
```

---

## 385. std::filesystem

### 功能说明
C++17 引入的文件系统库命名空间。

### 代码示例

```cpp
#include <iostream>
#include <filesystem>
namespace fs = std::filesystem;

int main() {
    fs::path p = "/home/user/file.txt";
    std::cout << p.filename() << std::endl;
    std::cout << p.extension() << std::endl;
    return 0;
}
```

---

## 386. std::equal_to

### 功能说明
函数对象，执行相等比较操作（==）。

### 代码示例

```cpp
#include <iostream>
#include <functional>

int main() {
    std::equal_to<int> eq;
    std::cout << eq(5, 5) << std::endl;
    std::cout << eq(5, 3) << std::endl;
    return 0;
}
```

---

## 387. std::endian::native

### 功能说明
C++20 引入的枚举值，表示当前系统的字节序。

### 代码示例

```cpp
#include <iostream>
#include <bit>

int main() {
    #if __cplusplus >= 202002L
    if (std::endian::native == std::endian::little) {
        std::cout << "Little Endian" << std::endl;
    }
    #endif
    return 0;
}
```

---

## 388. std::enable_if

### 功能说明
SFINAE 技术的基础工具，用于条件性地启用或禁用模板。

### 代码示例

```cpp
#include <iostream>
#include <type_traits>

template<typename T>
std::enable_if_t<std::is_integral_v<T>, T> add(T a, T b) {
    return a + b;
}

int main() {
    std::cout << add(3, 4) << std::endl;
    return 0;
}
```

---

## 389. std::destroy_n

### 功能说明
C++17 引入的内存管理工具，销毁 n 个对象。

### 代码示例

```cpp
#include <iostream>
#include <memory>

struct Test { ~Test() { std::cout << "destroyed" << std::endl; } };

int main() {
    alignas(Test) char buffer[sizeof(Test) * 3];
    Test* ptr = reinterpret_cast<Test*>(buffer);
    
    new (ptr) Test();
    new (ptr + 1) Test();
    new (ptr + 2) Test();
    
    std::destroy_n(ptr, 3);
    return 0;
}
```

---

## 390. std::default_random_engine

### 功能说明
标准库的默认随机数引擎类型。

### 代码示例

```cpp
#include <iostream>
#include <random>

int main() {
    std::default_random_engine rng;
    std::cout << "min: " << rng.min() << std::endl;
    std::cout << "max: " << rng.max() << std::endl;
    std::cout << "random: " << rng() << std::endl;
    return 0;
}
```

---

## 391. std::copy_backward

### 功能说明
从后向前复制范围内的元素到另一个范围。

### 代码示例

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> src = {1, 2, 3, 4, 5};
    std::vector<int> dst(5);
    std::copy_backward(src.begin(), src.end(), dst.end());
    
    for (int x : dst) std::cout << x << " ";
    return 0;
}
```

---

## 392. std::conj

### 功能说明
计算复数的共轭复数。

### 代码示例

```cpp
#include <iostream>
#include <complex>

int main() {
    std::complex<double> z(3.0, 4.0);
    std::cout << "z = " << z << std::endl;
    std::cout << "conj(z) = " << std::conj(z) << std::endl;
    std::cout << "|z|^2 = " << std::norm(z) << std::endl;
    return 0;
}
```

---

## 393. std::chrono::steady_clock::time_point

### 功能说明
单调时钟的时间点类型，保证时间只向前推进。

### 代码示例

```cpp
#include <iostream>
#include <chrono>
#include <thread>

int main() {
    auto start = std::chrono::steady_clock::now();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    auto end = std::chrono::steady_clock::now();
    
    auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    std::cout << "Elapsed: " << ms.count() << " ms" << std::endl;
    return 0;
}
```

---

## 394. std::chrono::seconds::period

### 功能说明
表示秒的时间周期类型。

### 代码示例

```cpp
#include <iostream>
#include <chrono>

int main() {
    std::cout << "seconds::period::num = " << std::chrono::seconds::period::num << std::endl;
    std::cout << "seconds::period::den = " << std::chrono::seconds::period::den << std::endl;
    return 0;
}
```

---

## 395. std::chrono::high_resolution_clock::time_point

### 功能说明
高精度时钟的时间点类型。

### 代码示例

```cpp
#include <iostream>
#include <chrono>

int main() {
    auto start = std::chrono::high_resolution_clock::now();
    // ... some work ...
    auto end = std::chrono::high_resolution_clock::now();
    
    auto ns = std::chrono::duration_cast<std::chrono::nanoseconds>(end - start);
    std::cout << ns.count() << " ns" << std::endl;
    return 0;
}
```

---

## 396. std::chrono::high_resolution_clock

### 功能说明
系统上可提供的最高精度时钟。

### 代码示例

```cpp
#include <iostream>
#include <chrono>

int main() {
    std::cout << "is_steady: " << std::chrono::high_resolution_clock::is_steady << std::endl;
    
    auto now = std::chrono::high_resolution_clock::now();
    auto time = std::chrono::duration_cast<std::chrono::nanoseconds>(now.time_since_epoch());
    std::cout << "Time since epoch: " << time.count() << " ns" << std::endl;
    return 0;
}
```

---

## 397. std::chrono::duration

### 功能说明
表示时间间隔的模板类。

### 代码示例

```cpp
#include <iostream>
#include <chrono>

int main() {
    std::chrono::seconds s(5);
    std::chrono::milliseconds ms = s;
    std::chrono::microseconds us = s;
    
    std::cout << s.count() << " s" << std::endl;
    std::cout << ms.count() << " ms" << std::endl;
    std::cout << us.count() << " us" << std::endl;
    return 0;
}
```

---

## 398. std::binary_search

### 功能说明
在已排序的范围内二分查找特定值。

### 代码示例

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {1, 3, 5, 7, 9};
    
    std::cout << std::binary_search(v.begin(), v.end(), 5) << std::endl;
    std::cout << std::binary_search(v.begin(), v.end(), 4) << std::endl;
    return 0;
}
```

---

## 399. std::atomic_thread_fence

### 功能说明
建立内存同步顺序，提供内存屏障。

### 代码示例

```cpp
#include <iostream>
#include <atomic>

int data = 0;
std::atomic<int> flag{0};

void producer() {
    data = 42;
    std::atomic_thread_fence(std::memory_order_release);
    flag.store(1, std::memory_order_relaxed);
}

void consumer() {
    while (flag.load(std::memory_order_relaxed) == 0) {}
    std::atomic_thread_fence(std::memory_order_acquire);
    std::cout << data << std::endl;
}

int main() {
    producer();
    consumer();
    return 0;
}
```

---

## 400. std::atomic_size_t

### 功能说明
`size_t` 类型的原子类型别名。

### 代码示例

```cpp
#include <iostream>
#include <atomic>
#include <thread>

std::atomic_size_t counter{0};

void increment() {
    for (int i = 0; i < 1000; ++i) {
        counter.fetch_add(1, std::memory_order_relaxed);
    }
}

int main() {
    std::thread t1(increment);
    std::thread t2(increment);
    t1.join();
    t2.join();
    std::cout << counter << std::endl;
    return 0;
}
```

---

## 401. std::allocator

### 功能说明
标准库提供的默认内存分配器。

### 代码示例

```cpp
#include <iostream>
#include <memory>

int main() {
    std::allocator<int> alloc;
    int* p = alloc.allocate(5);
    
    for (int i = 0; i < 5; ++i) {
        alloc.construct(p + i, i);
    }
    
    for (int i = 0; i < 5; ++i) {
        std::cout << p[i] << " ";
    }
    
    for (int i = 0; i < 5; ++i) {
        alloc.destroy(p + i);
    }
    alloc.deallocate(p, 5);
    return 0;
}
```

---

## 402. std::aligned_alloc

### 功能说明
C++17 引入的内存分配函数，分配按指定边界对齐的内存。

### 代码示例

```cpp
#include <iostream>
#include <cstdlib>

int main() {
    void* ptr = std::aligned_alloc(64, 1024);
    std::cout << "Aligned address: " << ptr << std::endl;
    std::cout << "Is 64-byte aligned: " << ((reinterpret_cast<uintptr_t>(ptr) % 64) == 0) << std::endl;
    std::free(ptr);
    return 0;
}
```

---

## 403. std::addressof

### 功能说明
返回对象的真实地址，即使类型重载了 `operator&`。

### 代码示例

```cpp
#include <iostream>
#include <memory>

template<typename T>
class BadPtr {
    T* ptr_;
public:
    explicit BadPtr(T* p) : ptr_(p) {}
    BadPtr* operator&() { return this; }
};

int main() {
    int x = 42;
    BadPtr<int> p(&x);
    
    // 危险：返回 BadPtr* 而不是 int*
    // int* addr = &p;  // 错误！
    
    // 正确：获取真实地址
    BadPtr<int>* real_addr = std::addressof(p);
    std::cout << real_addr << std::endl;
    return 0;
}
```

---

**文档结束**

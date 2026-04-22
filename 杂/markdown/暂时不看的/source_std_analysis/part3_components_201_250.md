# C++标准库组件详细分析 (201-250)

本文档详细分析C++标准库的第201-250个组件，每个组件包含功能说明、使用场景和完整代码示例。

---

## 201. std::greater - 大于比较函数对象

### 功能说明
`std::greater`是一个函数对象（functor），用于比较两个值，当第一个值大于第二个值时返回`true`。它是`std::less`的相反操作，常用于排序算法（如`std::sort`）中实现降序排列。

### 使用场景
- 需要对容器进行降序排序
- 构建降序的`std::map`或`std::set`
- 自定义比较逻辑，如优先队列
- 配合STL算法使用

### 代码示例

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <functional>
#include <set>
#include <queue>

int main() {
    // 场景1: 使用std::greater进行降序排序
    std::vector<int> vec = {3, 1, 4, 1, 5, 9, 2, 6};
    
    std::cout << "Original: ";
    for (int x : vec) std::cout << x << " ";
    std::cout << "\n";
    
    // 降序排序
    std::sort(vec.begin(), vec.end(), std::greater<int>());
    
    std::cout << "Descending: ";
    for (int x : vec) std::cout << x << " ";
    std::cout << "\n\n";
    
    // 场景2: 创建降序排列的set
    std::set<int, std::greater<int>> desc_set = {1, 3, 5, 2, 4};
    std::cout << "Descending set: ";
    for (int x : desc_set) std::cout << x << " ";
    std::cout << "\n\n";
    
    // 场景3: 使用greater作为优先队列的比较器（最小堆）
    std::priority_queue<int, std::vector<int>, std::greater<int>> min_heap;
    min_heap.push(5);
    min_heap.push(1);
    min_heap.push(3);
    min_heap.push(2);
    
    std::cout << "Min heap (top is minimum): ";
    while (!min_heap.empty()) {
        std::cout << min_heap.top() << " ";
        min_heap.pop();
    }
    std::cout << "\n";
    
    return 0;
}
```

---

## 202. std::getline - 读取一行字符串

### 功能说明
`std::getline`是一个用于从输入流中读取整行文本的函数。它会读取字符直到遇到分隔符（默认为换行符`\n`），并将结果存储到`std::string`中。

### 使用场景
- 读取包含空格的整行文本
- 处理CSV文件或结构化文本
- 读取用户输入的句子或段落
- 逐行读取文件内容

### 代码示例

```cpp
#include <iostream>
#include <string>
#include <sstream>

int main() {
    // 场景1: 从标准输入读取一行
    std::cout << "Enter a line of text: ";
    std::string line;
    std::getline(std::cin, line);
    std::cout << "You entered: " << line << "\n\n";
    
    // 场景2: 使用自定义分隔符解析CSV
    std::string csv = "John,25,Engineer,New York";
    std::istringstream iss(csv);
    std::string token;
    
    std::cout << "CSV fields:\n";
    while (std::getline(iss, token, ',')) {
        std::cout << "  " << token << "\n";
    }
    
    return 0;
}
```

---

## 203. std::exp - 指数函数

### 功能说明
`std::exp`计算e（自然对数的底数，约2.71828）的x次幂（e^x）。支持`float`、`double`和`long double`类型。

### 使用场景
- 数学计算中的指数增长/衰减模型
- 概率统计中的正态分布计算
- 机器学习中的sigmoid激活函数
- 复利计算、人口增长模型

### 代码示例

```cpp
#include <iostream>
#include <cmath>

// Sigmoid激活函数
double sigmoid(double x) {
    return 1.0 / (1.0 + std::exp(-x));
}

int main() {
    std::cout << "Basic exp calculations:\n";
    std::cout << "exp(0) = " << std::exp(0.0) << "\n";
    std::cout << "exp(1) = " << std::exp(1.0) << " (e)\n";
    std::cout << "exp(2) = " << std::exp(2.0) << "\n";
    
    // Sigmoid函数
    std::cout << "\nSigmoid function:\n";
    for (double x = -3.0; x <= 3.0; x += 1.0) {
        std::cout << "sigmoid(" << x << ") = " << sigmoid(x) << "\n";
    }
    
    return 0;
}
```

---

## 204. std::erase_if - 条件擦除 (C++20)

### 功能说明
`std::erase_if`是C++20引入的便捷函数，用于从容器中删除满足特定条件的所有元素。它是对`erase-remove`惯用法的封装。

### 使用场景
- 简化容器中条件删除操作
- 替代传统的erase-remove惯用法
- 代码更清晰、更易读

### 代码示例

```cpp
#include <iostream>
#include <vector>
#include <string>

int main() {
    // 从vector中删除所有偶数
    std::vector<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    
    std::cout << "Original: ";
    for (int n : numbers) std::cout << n << " ";
    std::cout << "\n";
    
    // C++20: 使用erase_if删除偶数
    auto removed = std::erase_if(numbers, [](int n) { return n % 2 == 0; });
    
    std::cout << "After removing even numbers: ";
    for (int n : numbers) std::cout << n << " ";
    std::cout << "\nRemoved " << removed << " elements\n";
    
    return 0;
}
```

---

## 205. std::declval - 声明值工具

### 功能说明
`std::declval`用于在不构造对象的情况下获取某个类型的右值引用。主要用于SFINAE和类型特征的编写中。

### 使用场景
- 在decltype表达式中获取成员函数返回类型
- 编写自定义类型特征（type traits）
- 不需要默认构造函数就能进行类型推导

### 代码示例

```cpp
#include <iostream>
#include <type_traits>
#include <utility>

// 一个没有默认构造函数的类
struct NoDefault {
    int value;
    NoDefault(int v) : value(v) {}
    int getValue() const { return value; }
};

// 使用std::declval获取成员函数返回类型
template<typename T>
using get_value_return_type = decltype(std::declval<T>().getValue());

int main() {
    // 检查返回类型
    std::cout << "Return type of getValue(): "
              << typeid(get_value_return_type<NoDefault>).name() << "\n";
    
    return 0;
}
```

---

## 206. std::chrono::milliseconds - 毫秒时长

### 功能说明
`std::chrono::milliseconds`是`std::chrono::duration`的特化类型，表示以毫秒为单位的时间间隔。

### 使用场景
- 设置线程睡眠时间
- 测量代码执行时间
- 定时器和超时控制
- 动画和游戏中的时间步长

### 代码示例

```cpp
#include <iostream>
#include <chrono>
#include <thread>

int main() {
    using namespace std::chrono;
    
    // 基本毫秒时长操作
    milliseconds ms1(500);
    milliseconds ms2 = 1000ms;
    
    std::cout << "ms1: " << ms1.count() << " ms\n";
    std::cout << "ms2: " << ms2.count() << " ms\n";
    
    // 测量代码执行时间
    auto start = high_resolution_clock::now();
    std::this_thread::sleep_for(milliseconds(100));
    auto end = high_resolution_clock::now();
    
    milliseconds elapsed = duration_cast<milliseconds>(end - start);
    std::cout << "Elapsed: " << elapsed.count() << " ms\n";
    
    return 0;
}
```

---

## 207. std::chrono::high_resolution_clock::now - 获取高精度时间

### 功能说明
`std::chrono::high_resolution_clock::now()`返回当前时间点，使用系统提供的最高精度时钟。

### 使用场景
- 性能分析和代码优化
- 测量算法执行时间
- 高精度计时和定时器
- 游戏帧率计算

### 代码示例

```cpp
#include <iostream>
#include <chrono>
#include <vector>
#include <algorithm>

int main() {
    using namespace std::chrono;
    
    // 测量vector排序时间
    std::vector<int> data(10000);
    for (size_t i = 0; i < data.size(); ++i) {
        data[i] = data.size() - i;  // 降序排列
    }
    
    auto start = high_resolution_clock::now();
    std::sort(data.begin(), data.end());
    auto end = high_resolution_clock::now();
    
    auto duration = duration_cast<microseconds>(end - start);
    std::cout << "Sorting took: " << duration.count() << " microseconds\n";
    
    return 0;
}
```

---

## 208. std::arg - 复数幅角

### 功能说明
`std::arg`计算复数的幅角（argument/phase angle），即复数在复平面上与正实轴之间的夹角。

### 使用场景
- 信号处理中的相位分析
- 傅里叶变换和频域分析
- 复数运算和几何变换

### 代码示例

```cpp
#include <iostream>
#include <complex>
#include <cmath>

int main() {
    using namespace std::complex_literals;
    
    std::complex<double> z1(1.0, 0.0);
    std::complex<double> z2(0.0, 1.0);
    std::complex<double> z3(1.0, 1.0);
    
    std::cout << "Argument calculations:\n";
    std::cout << "arg(1+0i) = " << std::arg(z1) << " rad (0 degrees)\n";
    std::cout << "arg(0+1i) = " << std::arg(z2) << " rad (90 degrees)\n";
    std::cout << "arg(1+1i) = " << std::arg(z3) << " rad (45 degrees)\n";
    
    return 0;
}
```

---

## 209. std::stack - 栈容器适配器

### 功能说明
`std::stack`是一个容器适配器，提供LIFO（后进先出）数据结构。默认使用`std::deque`作为底层容器。

### 使用场景
- 函数调用栈模拟
- 表达式求值
- 括号匹配检查
- 撤销操作

### 代码示例

```cpp
#include <iostream>
#include <stack>
#include <string>

// 检查括号是否匹配
bool isValidParentheses(const std::string& s) {
    std::stack<char> stk;
    for (char c : s) {
        if (c == '(' || c == '[' || c == '{') {
            stk.push(c);
        } else {
            if (stk.empty()) return false;
            char top = stk.top();
            if ((c == ')' && top != '(') ||
                (c == ']' && top != '[') ||
                (c == '}' && top != '{')) {
                return false;
            }
            stk.pop();
        }
    }
    return stk.empty();
}

int main() {
    std::cout << "Parentheses validation:\n";
    std::cout << "()[]{}: " << (isValidParentheses("()[]{}") ? "Valid" : "Invalid") << "\n";
    std::cout << "([)]: " << (isValidParentheses("([)]") ? "Valid" : "Invalid") << "\n";
    std::cout << "{[]}: " << (isValidParentheses("{[]}") ? "Valid" : "Invalid") << "\n";
    
    return 0;
}
```

---

## 210. std::set_intersection - 集合交集

### 功能说明
`std::set_intersection`计算两个已排序范围的交集，并将结果输出到目标范围。

### 使用场景
- 查找两个数据集的共同元素
- 推荐系统的共同喜好分析
- 文本处理中的共同词汇

### 代码示例

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <iterator>

int main() {
    std::vector<int> set1 = {1, 2, 3, 4, 5, 6, 7};
    std::vector<int> set2 = {4, 5, 6, 7, 8, 9, 10};
    std::vector<int> intersection;
    
    std::set_intersection(set1.begin(), set1.end(),
                          set2.begin(), set2.end(),
                          std::back_inserter(intersection));
    
    std::cout << "Set 1: ";
    for (int x : set1) std::cout << x << " ";
    std::cout << "\n";
    
    std::cout << "Set 2: ";
    for (int x : set2) std::cout << x << " ";
    std::cout << "\n";
    
    std::cout << "Intersection: ";
    for (int x : intersection) std::cout << x << " ";
    std::cout << "\n";
    
    return 0;
}
```

---

## 211. std::regex_search - 正则搜索

### 功能说明
`std::regex_search`在字符串中搜索正则表达式模式，如果在字符串的任何位置找到匹配则返回`true`。

### 使用场景
- 文本搜索和提取
- 日志文件分析
- 数据验证和解析
- 从非结构化数据中提取信息

### 代码示例

```cpp
#include <iostream>
#include <string>
#include <regex>

int main() {
    std::string text = "The quick brown fox jumps over 13 lazy dogs.";
    std::regex word_regex("\\b\\w{5}\\b");
    
    std::smatch match;
    std::string::const_iterator search_start(text.cbegin());
    
    std::cout << "Text: " << text << "\n";
    std::cout << "Pattern: 5-letter words\n";
    std::cout << "Matches: ";
    
    while (std::regex_search(search_start, text.cend(), match, word_regex)) {
        std::cout << "\"" << match[0] << "\" ";
        search_start = match.suffix().first;
    }
    std::cout << "\n";
    
    return 0;
}
```

---

## 212. std::ref - 创建引用包装器

### 功能说明
`std::ref`创建一个`std::reference_wrapper`对象，用于将引用传递给期望值类型的模板函数。

### 使用场景
- 向std::thread传递引用参数
- 使用std::bind绑定引用参数
- 在容器中存储引用

### 代码示例

```cpp
#include <iostream>
#include <functional>
#include <vector>

void increment(int& value) {
    ++value;
}

int main() {
    // 使用ref在容器中存储引用
    int a = 10, b = 20, c = 30;
    std::vector<std::reference_wrapper<int>> refs = {std::ref(a), std::ref(b), std::ref(c)};
    
    std::cout << "Before: a=" << a << ", b=" << b << ", c=" << c << "\n";
    
    for (int& ref : refs) {
        ref *= 2;
    }
    
    std::cout << "After: a=" << a << ", b=" << b << ", c=" << c << "\n";
    
    return 0;
}
```

---

## 213. std::priority_queue - 优先队列

### 功能说明
`std::priority_queue`是一个容器适配器，提供常数时间访问最大（或最小）元素的能力。默认是大顶堆。

### 使用场景
- 任务调度（优先级队列）
- Dijkstra和A*算法
- 数据流的中位数查找
- Top K问题

### 代码示例

```cpp
#include <iostream>
#include <queue>
#include <vector>

int main() {
    // 大顶堆
    std::priority_queue<int> max_pq;
    max_pq.push(3);
    max_pq.push(1);
    max_pq.push(4);
    max_pq.push(1);
    max_pq.push(5);
    
    std::cout << "Max heap: ";
    while (!max_pq.empty()) {
        std::cout << max_pq.top() << " ";
        max_pq.pop();
    }
    std::cout << "\n";
    
    // 小顶堆
    std::priority_queue<int, std::vector<int>, std::greater<int>> min_pq;
    min_pq.push(3);
    min_pq.push(1);
    min_pq.push(4);
    
    std::cout << "Min heap: ";
    while (!min_pq.empty()) {
        std::cout << min_pq.top() << " ";
        min_pq.pop();
    }
    std::cout << "\n";
    
    return 0;
}
```

---

## 214. std::prev - 递减迭代器

### 功能说明
`std::prev`返回给定迭代器向前（向begin方向）移动n个位置后的迭代器。

### 使用场景
- 获取容器末尾元素之前的元素
- 反向遍历容器的一部分
- 在循环中获取前一个元素

### 代码示例

```cpp
#include <iostream>
#include <vector>
#include <iterator>

int main() {
    std::vector<int> vec = {10, 20, 30, 40, 50};
    
    auto it = vec.end();
    auto prev_it = std::prev(it);
    
    std::cout << "Last element: " << *prev_it << "\n";
    std::cout << "Second to last: " << *std::prev(vec.end(), 2) << "\n";
    
    return 0;
}
```

---

## 215. std::ofstream::out - 输出模式

### 功能说明
`std::ofstream::out`表示以输出（写入）模式打开文件。对于`std::ofstream`是默认的。

### 使用场景
- 显式指定文件打开模式
- 组合多个打开模式标志

### 代码示例

```cpp
#include <iostream>
#include <fstream>
#include <string>

int main() {
    std::string filename = "output.txt";
    
    // 默认模式（无需显式指定）
    std::ofstream ofs(filename);
    ofs << "Default mode works!\n";
    ofs.close();
    
    // 追加模式
    std::ofstream ofs_append(filename, std::ofstream::out | std::ofstream::app);
    ofs_append << "Appended line\n";
    ofs_append.close();
    
    std::cout << "File written successfully\n";
    
    // 清理
    std::remove(filename.c_str());
    
    return 0;
}
```

---

## 216. std::ofstream::binary - 二进制输出模式

### 功能说明
`std::ofstream::binary`表示以二进制模式打开文件。数据按原始字节写入，不会进行文本转换。

### 使用场景
- 写入二进制数据文件
- 保存结构体或对象到文件
- 跨平台数据交换

### 代码示例

```cpp
#include <iostream>
#include <fstream>
#include <cstring>

struct PlayerData {
    char name[32];
    int level;
    float health;
};

int main() {
    // 写入二进制数据
    {
        PlayerData player;
        std::strcpy(player.name, "Hero");
        player.level = 50;
        player.health = 100.0f;
        
        std::ofstream ofs("player.bin", std::ios::binary);
        ofs.write(reinterpret_cast<const char*>(&player), sizeof(PlayerData));
    }
    
    // 读取二进制数据
    {
        PlayerData loaded;
        std::ifstream ifs("player.bin", std::ios::binary);
        ifs.read(reinterpret_cast<char*>(&loaded), sizeof(PlayerData));
        
        std::cout << "Loaded player:\n";
        std::cout << "  Name: " << loaded.name << "\n";
        std::cout << "  Level: " << loaded.level << "\n";
        std::cout << "  Health: " << loaded.health << "\n";
    }
    
    // 清理
    std::remove("player.bin");
    
    return 0;
}
```

---

## 217. std::memory_order_acq_rel - 获取-释放内存序

### 功能说明
`std::memory_order_acq_rel`结合了获取和释放语义，用于读-修改-写原子操作。

### 使用场景
- 读-修改-写原子操作的同步
- 实现自旋锁
- 生产者-消费者模式

### 代码示例

```cpp
#include <iostream>
#include <atomic>
#include <thread>
#include <vector>

class SpinLock {
private:
    std::atomic<bool> locked{false};
public:
    void lock() {
        while (locked.exchange(true, std::memory_order_acq_rel)) {
            // 自旋等待
        }
    }
    void unlock() {
        locked.store(false, std::memory_order_release);
    }
};

int main() {
    SpinLock spinlock;
    int shared_data = 0;
    std::vector<std::thread> threads;
    
    for (int i = 0; i < 5; ++i) {
        threads.emplace_back([&]() {
            for (int j = 0; j < 1000; ++j) {
                spinlock.lock();
                ++shared_data;
                spinlock.unlock();
            }
        });
    }
    
    for (auto& t : threads) {
        t.join();
    }
    
    std::cout << "Final counter value: " << shared_data << " (expected: 5000)\n";
    
    return 0;
}
```

---

## 218. std::memchr - 内存中查找字符

### 功能说明
`std::memchr`在内存块中搜索指定字符的第一次出现。适用于原始字节数组。

### 使用场景
- 在二进制数据中查找特定字节
- 处理原始内存缓冲区
- 解析二进制文件格式

### 代码示例

```cpp
#include <iostream>
#include <cstring>

int main() {
    const char* text = "Hello, World!";
    size_t len = std::strlen(text);
    
    const void* result = std::memchr(text, 'W', len);
    if (result) {
        std::cout << "Found 'W' at position: "
                  << static_cast<const char*>(result) - text << "\n";
        std::cout << "Remaining string: " << static_cast<const char*>(result) << "\n";
    }
    
    return 0;
}
```

---

## 219. std::is_trivially_constructible_v - 检查平凡构造

### 功能说明
`std::is_trivially_constructible_v`用于检查一个类型是否可以平凡地（不产生副作用）用给定参数类型构造。

### 使用场景
- 优化内存布局和数据传输
- 确定类型是否可以直接内存拷贝
- 编写高性能序列化代码

### 代码示例

```cpp
#include <iostream>
#include <type_traits>
#include <string>

struct Point {
    int x;
    int y;
};

struct NonTrivial {
    int value;
    NonTrivial() : value(42) {}
};

int main() {
    std::cout << "is_trivially_constructible_v<int>: "
              << std::is_trivially_constructible_v<int> << "\n";
    std::cout << "is_trivially_constructible_v<Point>: "
              << std::is_trivially_constructible_v<Point> << "\n";
    std::cout << "is_trivially_constructible_v<NonTrivial>: "
              << std::is_trivially_constructible_v<NonTrivial> << "\n";
    std::cout << "is_trivially_constructible_v<std::string>: "
              << std::is_trivially_constructible_v<std::string> << "\n";
    
    return 0;
}
```

---

## 220. std::ios_base::in - 输入模式标志

### 功能说明
`std::ios_base::in`表示以输入（读取）模式打开文件。主要用于`std::ifstream`和`std::fstream`。

### 使用场景
- 显式指定文件读取模式
- 创建可读写的文件流
- 与其他打开模式组合使用

### 代码示例

```cpp
#include <iostream>
#include <fstream>
#include <string>

int main() {
    // 创建测试文件
    {
        std::ofstream ofs("test.txt");
        ofs << "Line 1\nLine 2\nLine 3\n";
    }
    
    // 读取文件
    std::ifstream ifs("test.txt", std::ios_base::in);
    std::string line;
    
    std::cout << "File content:\n";
    while (std::getline(ifs, line)) {
        std::cout << "  " << line << "\n";
    }
    
    ifs.close();
    std::remove("test.txt");
    
    return 0;
}
```

---

## 221. std::hash - 哈希函数对象

### 功能说明
`std::hash`为各种类型提供哈希函数，是无序关联容器的基础。

### 使用场景
- 自定义类型的哈希计算
- 创建无序容器
- 数据校验和

### 代码示例

```cpp
#include <iostream>
#include <functional>
#include <string>
#include <unordered_map>

int main() {
    std::cout << "Hash values:\n";
    std::cout << "hash<int>(42) = " << std::hash<int>{}(42) << "\n";
    std::cout << "hash<string>(\"hello\") = " << std::hash<std::string>{}("hello") << "\n";
    
    // 使用unordered_map
    std::unordered_map<std::string, int> scores;
    scores["Alice"] = 95;
    scores["Bob"] = 87;
    
    std::cout << "\nScores:\n";
    for (const auto& [name, score] : scores) {
        std::cout << "  " << name << ": " << score << "\n";
    }
    
    return 0;
}
```

---

## 222. std::forward_list - 前向链表

### 功能说明
`std::forward_list`是一个单向链表容器，只支持前向遍历，比`std::list`更节省内存。

### 使用场景
- 内存受限的环境
- 只需要前向遍历的算法
- 频繁的头部插入/删除

### 代码示例

```cpp
#include <iostream>
#include <forward_list>

int main() {
    std::forward_list<int> flist = {3, 1, 4, 1, 5};
    
    std::cout << "Initial: ";
    for (int x : flist) std::cout << x << " ";
    std::cout << "\n";
    
    // 在头部插入
    flist.push_front(0);
    std::cout << "After push_front(0): ";
    for (int x : flist) std::cout << x << " ";
    std::cout << "\n";
    
    // 在特定位置后插入
    auto it = flist.begin();
    flist.insert_after(it, 99);
    std::cout << "After insert_after(begin, 99): ";
    for (int x : flist) std::cout << x << " ";
    std::cout << "\n";
    
    // 排序和去重
    flist.sort();
    flist.unique();
    std::cout << "After sort and unique: ";
    for (int x : flist) std::cout << x << " ";
    std::cout << "\n";
    
    return 0;
}
```

---

## 223. std::fmod - 浮点取模

### 功能说明
`std::fmod`计算浮点数除法的余数。结果与`x`同号。

### 使用场景
- 角度归一化
- 浮点数循环计算
- 游戏开发中的环绕效果

### 代码示例

```cpp
#include <iostream>
#include <cmath>

// 将角度归一化到[0, 360)范围
double normalize_angle_360(double angle) {
    double result = std::fmod(angle, 360.0);
    if (result < 0) {
        result += 360.0;
    }
    return result;
}

int main() {
    std::cout << "fmod examples:\n";
    std::cout << "fmod(10.5, 3.0) = " << std::fmod(10.5, 3.0) << "\n";
    std::cout << "fmod(-10.5, 3.0) = " << std::fmod(-10.5, 3.0) << "\n";
    
    std::cout << "\nAngle normalization:\n";
    std::vector<double> angles = {370.0, -10.0, 720.0, -370.0};
    for (double angle : angles) {
        std::cout << angle << " -> " << normalize_angle_360(angle) << "\n";
    }
    
    return 0;
}
```

---

## 224. std::fill - 填充范围

### 功能说明
`std::fill`将给定值赋给范围内的每个元素。

### 使用场景
- 初始化容器为特定值
- 重置数据结构状态
- 初始化数组或缓冲区

### 代码示例

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> vec(10);
    
    std::cout << "Initial: ";
    for (int x : vec) std::cout << x << " ";
    std::cout << "\n";
    
    std::fill(vec.begin(), vec.end(), 42);
    std::cout << "After fill with 42: ";
    for (int x : vec) std::cout << x << " ";
    std::cout << "\n";
    
    // 部分填充
    std::fill(vec.begin() + 2, vec.begin() + 7, 0);
    std::cout << "After fill positions 2-6 with 0: ";
    for (int x : vec) std::cout << x << " ";
    std::cout << "\n";
    
    return 0;
}
```

---

## 225. std::fclose - 关闭C文件流

### 功能说明
`std::fclose`用于关闭文件流并刷新缓冲区，确保数据被写入文件。

### 使用场景
- 关闭C风格的FILE*文件句柄
- 确保数据完全写入磁盘
- 在C/C++混合代码中使用

### 代码示例

```cpp
#include <iostream>
#include <cstdio>

int main() {
    const char* filename = "c_style_file.txt";
    
    // 写入文件
    FILE* file = std::fopen(filename, "w");
    if (!file) {
        std::cerr << "Failed to open file\n";
        return 1;
    }
    
    std::fprintf(file, "Hello from C-style file I/O\n");
    std::fprintf(file, "Line 2: Writing data\n");
    
    // 关闭文件
    if (std::fclose(file) == 0) {
        std::cout << "File written and closed successfully\n";
    }
    
    // 读取文件
    file = std::fopen(filename, "r");
    if (file) {
        char buffer[256];
        std::cout << "\nFile content:\n";
        while (std::fgets(buffer, sizeof(buffer), file) != nullptr) {
            std::cout << "  " << buffer;
        }
        std::fclose(file);
    }
    
    std::remove(filename);
    return 0;
}
```

---

## 226. std::error_code - 错误码类

### 功能说明
`std::error_code`是一个轻量级的错误码类，用于报告系统级错误，包含错误值和错误类别。

### 使用场景
- 错误代码返回值替代异常
- 系统API错误处理
- 跨平台错误码转换

### 代码示例

```cpp
#include <iostream>
#include <system_error>
#include <fstream>

int main() {
    std::error_code ec;
    
    // 打开不存在的文件
    std::fstream file("nonexistent.txt");
    if (!file) {
        ec.assign(errno, std::generic_category());
        std::cout << "Error code: " << ec.value() << "\n";
        std::cout << "Error message: " << ec.message() << "\n";
        std::cout << "Error category: " << ec.category().name() << "\n";
    }
    
    return 0;
}
```

---

## 227. std::errc - 错误码枚举

### 功能说明
`std::errc`是一个枚举类，定义了标准的可移植错误条件。

### 使用场景
- 编写可移植的错误处理代码
- 将系统错误码转换为通用错误条件
- 检查特定类型的错误

### 代码示例

```cpp
#include <iostream>
#include <system_error>
#include <fstream>

int main() {
    // 从errc创建error_condition
    std::error_condition not_found = std::errc::no_such_file_or_directory;
    std::cout << "Condition: " << not_found.message() << "\n";
    
    // 检查文件错误
    std::fstream file("/nonexistent/path/file.txt");
    if (!file) {
        std::error_code ec(errno, std::generic_category());
        if (ec == std::errc::no_such_file_or_directory) {
            std::cout << "File not found!\n";
        } else if (ec == std::errc::permission_denied) {
            std::cout << "Permission denied!\n";
        }
    }
    
    return 0;
}
```

---

## 228. std::chrono::time_point - 时间点

### 功能说明
`std::chrono::time_point`表示一个特定的时间点，由时钟和持续时间组成。

### 使用场景
- 记录事件发生时间
- 计算时间间隔
- 实现超时和定时功能

### 代码示例

```cpp
#include <iostream>
#include <chrono>
#include <ctime>

int main() {
    using namespace std::chrono;
    
    // 获取当前时间点
    system_clock::time_point now = system_clock::now();
    
    // 转换为time_t
    std::time_t t = system_clock::to_time_t(now);
    std::cout << "Current time: " << std::ctime(&t);
    
    // 计算1小时后
    auto one_hour_later = now + hours(1);
    std::time_t t2 = system_clock::to_time_t(one_hour_later);
    std::cout << "One hour later: " << std::ctime(&t2);
    
    return 0;
}
```

---

## 229. std::chrono::duration_cast - 时长转换

### 功能说明
`std::chrono::duration_cast`用于在不同精度的时间单位之间进行显式转换。

### 使用场景
- 时间单位转换
- 将高精度时间转为低精度
- 格式化输出时间

### 代码示例

```cpp
#include <iostream>
#include <chrono>

int main() {
    using namespace std::chrono;
    
    // 创建纳秒时长
    nanoseconds ns(5500000000LL);  // 5.5秒
    
    // 转换为不同单位
    auto micros = duration_cast<microseconds>(ns);
    auto millis = duration_cast<milliseconds>(ns);
    auto secs = duration_cast<seconds>(ns);
    auto mins = duration_cast<minutes>(ns);
    
    std::cout << "5500000000 nanoseconds =\n";
    std::cout << "  " << micros.count() << " microseconds\n";
    std::cout << "  " << millis.count() << " milliseconds\n";
    std::cout << "  " << secs.count() << " seconds\n";
    std::cout << "  " << mins.count() << " minutes\n";
    
    return 0;
}
```

---

## 230. std::char_traits - 字符特性模板

### 功能说明
`std::char_traits`是一个特性类模板，定义了字符类型的基本操作。

### 使用场景
- 自定义字符串类
- 支持不同字符编码
- 自定义字符比较和复制行为

### 代码示例

```cpp
#include <iostream>
#include <string>

int main() {
    using traits = std::char_traits<char>;
    
    // 字符特性操作
    char str1[] = "Hello";
    char str2[] = "Hello";
    char str3[] = "World";
    
    std::cout << "Length of \"Hello\": " << traits::length(str1) << "\n";
    std::cout << "Compare str1 and str2: " << traits::compare(str1, str2, 5) << "\n";
    std::cout << "Compare str1 and str3: " << traits::compare(str1, str3, 5) << "\n";
    
    // 查找字符
    const char* found = traits::find(str1, 5, 'l');
    if (found) {
        std::cout << "Found 'l' at position: " << (found - str1) << "\n";
    }
    
    return 0;
}
```

---

## 231. std::bad_cast - 动态转换失败异常

### 功能说明
`std::bad_cast`是当`dynamic_cast`对引用类型失败时抛出的异常。

### 使用场景
- 处理动态类型转换失败
- 运行时类型检查
- 多态类型的安全转换

### 代码示例

```cpp
#include <iostream>
#include <typeinfo>

class Base {
public:
    virtual ~Base() = default;
};

class Derived : public Base {
public:
    void derivedOnly() {
        std::cout << "Derived class method\n";
    }
};

class Other : public Base {};

int main() {
    Base* base = new Other();
    
    try {
        // 尝试将Other*转换为Derived&
        Derived& derived = dynamic_cast<Derived&>(*base);
        derived.derivedOnly();
    } catch (const std::bad_cast& e) {
        std::cout << "bad_cast caught: " << e.what() << "\n";
    }
    
    delete base;
    return 0;
}
```

---

## 232. std::atan - 反正切函数

### 功能说明
`std::atan`计算反正切值，返回弧度。还有`atan2`版本可以正确处理象限。

### 使用场景
- 计算角度
- 坐标转换
- 游戏开发中的方向计算

### 代码示例

```cpp
#include <iostream>
#include <cmath>

int main() {
    std::cout << "atan examples:\n";
    std::cout << "atan(0) = " << std::atan(0.0) << " rad\n";
    std::cout << "atan(1) = " << std::atan(1.0) << " rad (45 degrees)\n";
    std::cout << "atan(infinity) = " << std::atan(1e308) << " rad (90 degrees)\n";
    
    // atan2示例
    std::cout << "\natan2 examples:\n";
    std::cout << "atan2(1, 1) = " << std::atan2(1.0, 1.0) << " rad (45 degrees)\n";
    std::cout << "atan2(1, -1) = " << std::atan2(1.0, -1.0) << " rad (135 degrees)\n";
    std::cout << "atan2(-1, -1) = " << std::atan2(-1.0, -1.0) << " rad (-135 degrees)\n";
    std::cout << "atan2(-1, 1) = " << std::atan2(-1.0, 1.0) << " rad (-45 degrees)\n";
    
    return 0;
}
```

---

## 233. std::as_const - 转为const引用 (C++17)

### 功能说明
`std::as_const`将对象转换为const引用，避免意外的修改。

### 使用场景
- 确保对象不被修改
- 调用重载函数时选择const版本
- 模板编程中的类型转换

### 代码示例

```cpp
#include <iostream>
#include <utility>

void process(int& x) {
    std::cout << "Non-const version: " << x << "\n";
    x *= 2;
}

void process(const int& x) {
    std::cout << "Const version: " << x << "\n";
}

int main() {
    int value = 42;
    
    std::cout << "Without as_const:\n";
    process(value);  // 调用非const版本
    std::cout << "Value after: " << value << "\n\n";
    
    value = 42;
    std::cout << "With as_const:\n";
    process(std::as_const(value));  // 强制调用const版本
    std::cout << "Value after: " << value << "\n";
    
    return 0;
}
```

---

## 234. std::vector::push_back - 向量尾部添加元素

### 功能说明
`std::vector::push_back`在vector的末尾添加一个元素。

### 使用场景
- 动态添加元素到容器
- 构建元素列表
- 数据收集

### 代码示例

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> vec;
    
    std::cout << "Adding elements with push_back:\n";
    vec.push_back(10);
    vec.push_back(20);
    vec.push_back(30);
    
    std::cout << "Vector contents: ";
    for (int x : vec) {
        std::cout << x << " ";
    }
    std::cout << "\n";
    std::cout << "Size: " << vec.size() << "\n";
    std::cout << "Capacity: " << vec.capacity() << "\n";
    
    return 0;
}
```

---

## 235. std::vector::erase - 向量删除元素

### 功能说明
`std::vector::erase`删除指定位置的元素或指定范围的元素。

### 使用场景
- 删除特定元素
- 批量删除元素
- 条件删除

### 代码示例

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> vec = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    
    std::cout << "Original: ";
    for (int x : vec) std::cout << x << " ";
    std::cout << "\n";
    
    // 删除单个元素
    vec.erase(vec.begin() + 3);
    std::cout << "After erase at position 3: ";
    for (int x : vec) std::cout << x << " ";
    std::cout << "\n";
    
    // 删除范围
    vec.erase(vec.begin() + 2, vec.begin() + 5);
    std::cout << "After erase range [2, 5): ";
    for (int x : vec) std::cout << x << " ";
    std::cout << "\n";
    
    return 0;
}
```

---

## 236. std::vector::empty - 检查向量是否为空

### 功能说明
`std::vector::empty`检查vector是否不包含任何元素。

### 使用场景
- 检查容器状态
- 避免访问空容器的操作
- 循环条件判断

### 代码示例

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> empty_vec;
    std::vector<int> non_empty_vec = {1, 2, 3};
    
    std::cout << "Empty vector:\n";
    std::cout << "  empty(): " << (empty_vec.empty() ? "true" : "false") << "\n";
    std::cout << "  size() == 0: " << (empty_vec.size() == 0 ? "true" : "false") << "\n";
    
    std::cout << "\nNon-empty vector:\n";
    std::cout << "  empty(): " << (non_empty_vec.empty() ? "true" : "false") << "\n";
    std::cout << "  size(): " << non_empty_vec.size() << "\n";
    
    // 安全访问
    if (!empty_vec.empty()) {
        std::cout << "First element: " << empty_vec[0] << "\n";
    } else {
        std::cout << "Vector is empty, safe to skip access\n";
    }
    
    return 0;
}
```

---

## 237. std::vector::emplace_back - 原地构造添加 (C++11)

### 功能说明
`std::vector::emplace_back`在vector末尾原地构造元素，避免不必要的拷贝或移动。

### 使用场景
- 添加复杂对象时提高性能
- 避免临时对象的创建
- 添加不可拷贝的对象

### 代码示例

```cpp
#include <iostream>
#include <vector>
#include <string>

struct Person {
    std::string name;
    int age;
    
    Person(std::string n, int a) : name(std::move(n)), age(a) {
        std::cout << "Constructor called for " << name << "\n";
    }
    
    Person(const Person& other) : name(other.name), age(other.age) {
        std::cout << "Copy constructor called for " << name << "\n";
    }
    
    Person(Person&& other) noexcept : name(std::move(other.name)), age(other.age) {
        std::cout << "Move constructor called for " << name << "\n";
    }
};

int main() {
    std::vector<Person> people;
    people.reserve(10);
    
    std::cout << "Using push_back:\n";
    people.push_back(Person("Alice", 30));  // 构造 + 移动
    
    std::cout << "\nUsing emplace_back:\n";
    people.emplace_back("Bob", 25);  // 只调用一次构造函数
    
    std::cout << "\nVector contents:\n";
    for (const auto& p : people) {
        std::cout << "  " << p.name << ", " << p.age << "\n";
    }
    
    return 0;
}
```

---

## 238. std::unordered_set::insert - 无序集合插入

### 功能说明
`std::unordered_set::insert`向无序集合中插入元素。

### 使用场景
- 添加唯一元素
- 构建去重集合
- 快速查找的数据结构

### 代码示例

```cpp
#include <iostream>
#include <unordered_set>
#include <string>

int main() {
    std::unordered_set<std::string> unique_names;
    
    // 插入元素
    auto result1 = unique_names.insert("Alice");
    std::cout << "Inserted Alice: " << (result1.second ? "success" : "already exists") << "\n";
    
    auto result2 = unique_names.insert("Bob");
    std::cout << "Inserted Bob: " << (result2.second ? "success" : "already exists") << "\n";
    
    auto result3 = unique_names.insert("Alice");
    std::cout << "Inserted Alice again: " << (result3.second ? "success" : "already exists") << "\n";
    
    std::cout << "\nSet contents: ";
    for (const auto& name : unique_names) {
        std::cout << name << " ";
    }
    std::cout << "\n";
    
    return 0;
}
```

---

## 239. std::unordered_set::find - 无序集合查找

### 功能说明
`std::unordered_set::find`查找集合中是否存在指定元素。

### 使用场景
- 检查元素是否存在
- 去重检查
- 成员资格测试

### 代码示例

```cpp
#include <iostream>
#include <unordered_set>
#include <string>

int main() {
    std::unordered_set<std::string> fruits = {"apple", "banana", "cherry", "date"};
    
    // 查找元素
    auto it1 = fruits.find("banana");
    if (it1 != fruits.end()) {
        std::cout << "Found: " << *it1 << "\n";
    }
    
    auto it2 = fruits.find("grape");
    if (it2 == fruits.end()) {
        std::cout << "grape not found in the set\n";
    }
    
    // 使用count检查存在性
    std::cout << "apple exists: " << (fruits.count("apple") > 0 ? "yes" : "no") << "\n";
    std::cout << "mango exists: " << (fruits.count("mango") > 0 ? "yes" : "no") << "\n";
    
    return 0;
}
```

---

## 240. std::unordered_set::erase - 无序集合删除

### 功能说明
`std::unordered_set::erase`从集合中删除指定元素。

### 使用场景
- 移除特定元素
- 批量删除
- 清理数据

### 代码示例

```cpp
#include <iostream>
#include <unordered_set>

int main() {
    std::unordered_set<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    
    std::cout << "Original: ";
    for (int x : numbers) std::cout << x << " ";
    std::cout << "\n";
    
    // 通过值删除
    size_t removed = numbers.erase(5);
    std::cout << "After erase(5), removed " << removed << " element(s)\n";
    
    // 通过迭代器删除
    auto it = numbers.find(7);
    if (it != numbers.end()) {
        numbers.erase(it);
        std::cout << "Erased element 7 using iterator\n";
    }
    
    std::cout << "Final set: ";
    for (int x : numbers) std::cout << x << " ";
    std::cout << "\n";
    
    return 0;
}
```

---

## 241. std::unordered_set::end - 无序集合尾后迭代器

### 功能说明
`std::unordered_set::end`返回指向集合最后一个元素之后位置的迭代器。

### 使用场景
- 标记查找失败
- 迭代器范围的上界
- 循环终止条件

### 代码示例

```cpp
#include <iostream>
#include <unordered_set>

int main() {
    std::unordered_set<int> numbers = {1, 2, 3, 4, 5};
    
    // 使用end()检查查找结果
    auto it = numbers.find(3);
    if (it != numbers.end()) {
        std::cout << "Found: " << *it << "\n";
    }
    
    it = numbers.find(10);
    if (it == numbers.end()) {
        std::cout << "10 not found (end() returned)\n";
    }
    
    // 遍历所有元素
    std::cout << "All elements: ";
    for (auto it = numbers.begin(); it != numbers.end(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << "\n";
    
    return 0;
}
```

---

## 242. std::type_info - 类型信息类

### 功能说明
`std::type_info`包含类型的信息，由`typeid`运算符返回。

### 使用场景
- 运行时类型识别
- 调试和日志
- 类型比较

### 代码示例

```cpp
#include <iostream>
#include <typeinfo>

class Base {
public:
    virtual ~Base() = default;
};

class Derived : public Base {};

int main() {
    // 基本类型信息
    std::cout << "Type information:\n";
    std::cout << "typeid(int).name(): " << typeid(int).name() << "\n";
    std::cout << "typeid(double).name(): " << typeid(double).name() << "\n";
    
    // 多态类型信息
    Base* base = new Derived();
    std::cout << "\ntypeid(*base).name(): " << typeid(*base).name() << "\n";
    std::cout << "typeid(base).name(): " << typeid(base).name() << "\n";
    
    // 类型比较
    if (typeid(*base) == typeid(Derived)) {
        std::cout << "base points to a Derived object\n";
    }
    
    delete base;
    return 0;
}
```

---

## 243. std::tuple_element_t - 获取tuple元素类型 (C++14)

### 功能说明
`std::tuple_element_t`获取tuple或pair中指定位置的元素类型。

### 使用场景
- 模板元编程
- 处理tuple元素类型
- 编写通用代码

### 代码示例

```cpp
#include <iostream>
#include <tuple>
#include <utility>
#include <type_traits>

int main() {
    using MyTuple = std::tuple<int, double, std::string>;
    
    // 获取tuple元素类型
    using FirstType = std::tuple_element_t<0, MyTuple>;
    using SecondType = std::tuple_element_t<1, MyTuple>;
    using ThirdType = std::tuple_element_t<2, MyTuple>;
    
    std::cout << "Tuple element types:\n";
    std::cout << "Element 0: " << typeid(FirstType).name() << "\n";
    std::cout << "Element 1: " << typeid(SecondType).name() << "\n";
    std::cout << "Element 2: " << typeid(ThirdType).name() << "\n";
    
    // 用于pair
    using MyPair = std::pair<int, std::string>;
    using PairFirst = std::tuple_element_t<0, MyPair>;
    using PairSecond = std::tuple_element_t<1, MyPair>;
    
    std::cout << "\nPair element types:\n";
    std::cout << "First: " << typeid(PairFirst).name() << "\n";
    std::cout << "Second: " << typeid(PairSecond).name() << "\n";
    
    return 0;
}
```

---

## 244. std::tm - 时间结构体

### 功能说明
`std::tm`是一个结构体，包含日历日期和时间的各个组成部分。

### 使用场景
- 日期时间分解
- 格式化时间输出
- 时间计算

### 代码示例

```cpp
#include <iostream>
#include <ctime>

int main() {
    std::time_t now = std::time(nullptr);
    std::tm* local_time = std::localtime(&now);
    
    std::cout << "Current time breakdown:\n";
    std::cout << "  Year: " << local_time->tm_year + 1900 << "\n";
    std::cout << "  Month: " << local_time->tm_mon + 1 << "\n";
    std::cout << "  Day: " << local_time->tm_mday << "\n";
    std::cout << "  Hour: " << local_time->tm_hour << "\n";
    std::cout << "  Minute: " << local_time->tm_min << "\n";
    std::cout << "  Second: " << local_time->tm_sec << "\n";
    std::cout << "  Day of week: " << local_time->tm_wday << " (0=Sunday)\n";
    std::cout << "  Day of year: " << local_time->tm_yday << "\n";
    
    return 0;
}
```

---

## 245. std::time_t - 时间类型

### 功能说明
`std::time_t`是表示时间点的算术类型，通常是整数类型。

### 使用场景
- 存储时间点
- 时间计算
- 系统时间操作

### 代码示例

```cpp
#include <iostream>
#include <ctime>

int main() {
    // 获取当前时间
    std::time_t now = std::time(nullptr);
    std::cout << "Current time_t: " << now << "\n";
    
    // 转换为可读格式
    std::cout << "As string: " << std::ctime(&now);
    
    // 时间计算
    std::time_t tomorrow = now + 24 * 60 * 60;  // 加1天
    std::cout << "Tomorrow: " << std::ctime(&tomorrow);
    
    // 计算时间差
    std::time_t past = now - 7 * 24 * 60 * 60;  // 1周前
    double diff = std::difftime(now, past);
    std::cout << "Difference: " << diff << " seconds (" << diff / 86400 << " days)\n";
    
    return 0;
}
```

---

## 246. std::time - 获取当前时间

### 功能说明
`std::time`获取当前日历时间。

### 使用场景
- 获取系统时间
- 时间戳生成
- 随机数种子

### 代码示例

```cpp
#include <iostream>
#include <ctime>
#include <cstdlib>

int main() {
    // 获取当前时间
    std::time_t now = std::time(nullptr);
    std::cout << "Current time: " << std::ctime(&now);
    
    // 使用time作为随机数种子
    std::srand(static_cast<unsigned>(std::time(nullptr)));
    std::cout << "Random number: " << std::rand() << "\n";
    
    // 获取特定时间点的time_t
    std::tm specific_time = {};
    specific_time.tm_year = 2024 - 1900;  // 年份从1900开始
    specific_time.tm_mon = 0;             // 一月
    specific_time.tm_mday = 1;            // 1日
    std::time_t specific = std::mktime(&specific_time);
    std::cout << "Specific time: " << std::ctime(&specific);
    
    return 0;
}
```

---

## 247. std::string_view::npos - string_view无效位置常量

### 功能说明
`std::string_view::npos`是一个静态成员常量，表示无效的位置或长度。

### 使用场景
- 检查查找操作是否成功
- 表示"直到末尾"
- 作为查找失败的返回值

### 代码示例

```cpp
#include <iostream>
#include <string_view>

int main() {
    std::string_view sv = "Hello, World!";
    
    // 查找子串
    auto pos = sv.find("World");
    if (pos != std::string_view::npos) {
        std::cout << "Found at position: " << pos << "\n";
    }
    
    // 查找不存在的子串
    pos = sv.find("xyz");
    if (pos == std::string_view::npos) {
        std::cout << "'xyz' not found (npos returned)\n";
    }
    
    // npos的值
    std::cout << "npos value: " << std::string_view::npos << "\n";
    std::cout << "npos as size_t max: " << static_cast<size_t>(-1) << "\n";
    
    return 0;
}
```

---

## 248. std::string::size_type - 字符串大小类型

### 功能说明
`std::string::size_type`是用于表示字符串大小和位置的无符号整数类型。

### 使用场景
- 字符串索引和大小
- 与字符串相关的循环变量
- 跨平台兼容性

### 代码示例

```cpp
#include <iostream>
#include <string>

int main() {
    std::string str = "Hello, World!";
    
    // 使用size_type
    std::string::size_type len = str.size();
    std::string::size_type pos = str.find("World");
    
    std::cout << "String length (size_type): " << len << "\n";
    std::cout << "Position of 'World': " << pos << "\n";
    
    // 类型信息
    std::cout << "\nsize_type is: " << typeid(std::string::size_type).name() << "\n";
    std::cout << "Same as std::size_t: " 
              << (std::is_same_v<std::string::size_type, std::size_t> ? "yes" : "no") << "\n";
    
    return 0;
}
```

---

## 249. std::streamoff - 流偏移类型

### 功能说明
`std::streamoff`是用于表示流中偏移量的有符号整数类型。

### 使用场景
- 文件定位操作
- 计算文件大小
- 随机访问文件

### 代码示例

```cpp
#include <iostream>
#include <fstream>
#include <string>

int main() {
    // 创建测试文件
    {
        std::ofstream ofs("test.txt");
        ofs << "Line 1\nLine 2\nLine 3\n";
    }
    
    std::ifstream ifs("test.txt");
    
    // 获取文件大小
    ifs.seekg(0, std::ios::end);
    std::streamoff file_size = ifs.tellg();
    std::cout << "File size: " << file_size << " bytes\n";
    
    // 定位到特定位置
    ifs.seekg(7, std::ios::beg);  // 从开头偏移7字节
    std::streamoff pos = ifs.tellg();
    std::cout << "Current position: " << pos << "\n";
    
    char ch;
    ifs.get(ch);
    std::cout << "Character at position " << pos << ": '" << ch << "'\n";
    
    ifs.close();
    std::remove("test.txt");
    
    return 0;
}
```

---

## 250. std::stoll - 字符串转long long

### 功能说明
`std::stoll`将字符串转换为`long long`类型。

### 使用场景
- 解析整数字符串
- 配置文件读取
- 用户输入处理
- 数据转换

### 代码示例

```cpp
#include <iostream>
#include <string>

int main() {
    // 基本转换
    std::string str1 = "123456789012345";
    long long val1 = std::stoll(str1);
    std::cout << "Converted: " << val1 << "\n";
    
    // 处理不同进制
    std::string hex = "FF";
    long long val2 = std::stoll(hex, nullptr, 16);
    std::cout << "Hex FF = " << val2 << " (decimal)\n";
    
    std::string binary = "1010";
    long long val3 = std::stoll(binary, nullptr, 2);
    std::cout << "Binary 1010 = " << val3 << " (decimal)\n";
    
    // 获取处理后的位置
    std::string str2 = "123abc";
    size_t pos;
    long long val4 = std::stoll(str2, &pos);
    std::cout << "Converted: " << val4 << ", processed " << pos << " characters\n";
    
    return 0;
}
```

---

## 总结

本文档涵盖了C++标准库的第201-250个组件，包括：

1. **比较与算法**：std::greater, std::set_intersection, std::fill
2. **字符串处理**：std::getline, std::regex_search, std::stoll
3. **容器操作**：std::stack, std::priority_queue, std::forward_list, std::vector操作
4. **数学计算**：std::exp, std::fmod, std::atan, std::arg
5. **时间与日期**：std::chrono组件, std::tm, std::time_t
6. **文件与IO**：std::ofstream模式, std::fclose, std::streamoff
7. **类型系统**：std::declval, std::is_trivially_constructible_v, std::type_info
8. **并发与内存**：std::memory_order_acq_rel, std::ref
9. **错误处理**：std::error_code, std::errc
10. **杂项工具**：std::hash, std::char_traits, std::memchr, std::as_const

每个组件都提供了完整的功能说明、使用场景和可编译运行的代码示例。

# C++标准库组件详解（第301-350个）- 完整版

本文档详细分析Blender代码库中使用的C++标准库组件（第301-350位），每个组件包含完整的功能说明、使用场景和代码示例。

---

## 301. std::asin - 反正弦函数

### 功能说明
`std::asin`是C++数学库中的反正弦函数（arcsine），用于计算一个数值的反正弦值，返回角度（以弧度为单位）。函数定义在头文件`<cmath>`中。

**函数原型**：
```cpp
double asin(double x);
float asinf(float x);
long double asinl(long double x);
```

**参数说明**：
- `x`：输入值，必须在`[-1.0, 1.0]`范围内

**返回值**：
- 返回`[-π/2, +π/2]`范围内的反正弦值（弧度）

### 代码示例

```cpp
#include <cmath>
#include <iostream>

int main() {
    double val = 0.5;
    double result = std::asin(val);
    std::cout << "asin(0.5) = " << result << " 弧度 (" 
              << result * 180.0 / M_PI << " 度)" << std::endl;
    return 0;
}
```

---

## 302. std::any - 任意类型容器

### 功能说明
C++17引入的类型安全容器，可存储任意类型的单个值。定义在`<any>`中。

### 代码示例

```cpp
#include <any>
#include <string>
#include <iostream>

int main() {
    std::any a = 42;
    std::cout << "整数: " << std::any_cast<int>(a) << std::endl;
    
    a = std::string("Hello");
    std::cout << "字符串: " << std::any_cast<std::string>(a) << std::endl;
    return 0;
}
```

---

## 303. std::adjacent_find - 查找相邻重复元素

### 功能说明
在范围内查找第一个满足条件的相邻元素对。

### 代码示例

```cpp
#include <algorithm>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> nums = {1, 2, 3, 3, 4, 5};
    auto it = std::adjacent_find(nums.begin(), nums.end());
    if (it != nums.end()) {
        std::cout << "相邻重复: " << *it << " 在位置 " 
                  << std::distance(nums.begin(), it) << std::endl;
    }
    return 0;
}
```

---

## 304. std::acos - 反余弦函数

### 功能说明
计算反余弦值，返回`[0, π]`范围内的弧度值。

### 代码示例

```cpp
#include <cmath>
#include <iostream>

int main() {
    std::cout << "acos(1.0) = " << std::acos(1.0) << " (0)" << std::endl;
    std::cout << "acos(0.0) = " << std::acos(0.0) << " (π/2)" << std::endl;
    std::cout << "acos(-1.0) = " << std::acos(-1.0) << " (π)" << std::endl;
    return 0;
}
```

---

## 305. std::void_t - void类型工具

### 功能说明
C++17元编程工具，用于SFINAE检测类型特征。

### 代码示例

```cpp
#include <type_traits>
#include <iostream>
#include <vector>

template<typename... Ts> using void_t = void;

template<typename, typename = void>
struct has_size : std::false_type {};

template<typename T>
struct has_size<T, void_t<decltype(std::declval<T>().size())>> 
    : std::true_type {};

int main() {
    std::cout << "vector有size(): " << has_size<std::vector<int>>::value << std::endl;
    std::cout << "int有size(): " << has_size<int>::value << std::endl;
    return 0;
}
```

---

## 306. std::vector::pop_back

### 功能说明
从vector末尾移除元素，时间复杂度O(1)。容器大小减1但容量不变。

**函数原型**：`void pop_back();`

### 使用场景
- 实现栈的出栈操作
- 撤销功能
- 批量处理尾部元素

### 代码示例

```cpp
#include <vector>
#include <iostream>
#include <string>

int main() {
    std::vector<std::string> history;
    history.push_back("Action 1");
    history.push_back("Action 2");
    history.push_back("Action 3");
    
    std::cout << "撤销前: " << history.size() << " 个操作" << std::endl;
    
    // 撤销最后一个操作
    if (!history.empty()) {
        std::cout << "撤销: " << history.back() << std::endl;
        history.pop_back();
    }
    
    std::cout << "撤销后: " << history.size() << " 个操作" << std::endl;
    
    // 使用vector作为栈
    std::vector<int> stack;
    stack.push_back(10);
    stack.push_back(20);
    stack.push_back(30);
    
    while (!stack.empty()) {
        std::cout << "弹出: " << stack.back() << std::endl;
        stack.pop_back();
    }
    
    return 0;
}
```

---

## 307. std::vector::insert

### 功能说明
在指定位置插入元素。可能移动后续所有元素，非尾部插入时间复杂度为O(n)。

**函数原型**：
```cpp
iterator insert(iterator position, const T& x);
iterator insert(iterator position, T&& x);
void insert(iterator position, size_type n, const T& x);
```

### 使用场景
- 有序插入保持排序
- 批量插入数据
- 在特定位置添加元素

### 代码示例

```cpp
#include <vector>
#include <iostream>
#include <algorithm>

int main() {
    std::vector<int> vec = {1, 3, 5, 7, 9};
    
    // 有序插入
    int value = 4;
    auto pos = std::lower_bound(vec.begin(), vec.end(), value);
    vec.insert(pos, value);
    
    std::cout << "插入4后: ";
    for (int n : vec) std::cout << n << " ";
    std::cout << std::endl;
    
    // 在指定位置插入
    vec.insert(vec.begin() + 2, 99);
    std::cout << "在位置2插入99: ";
    for (int n : vec) std::cout << n << " ";
    std::cout << std::endl;
    
    // 批量插入
    vec.insert(vec.end(), 3, 0);
    std::cout << "尾部插入3个0: ";
    for (int n : vec) std::cout << n << " ";
    std::cout << std::endl;
    
    return 0;
}
```

---

## 308. std::unordered_map::insert_or_assign

### 功能说明
C++17引入，插入新元素或更新已有元素的值。比`operator[]`更高效且类型安全。

**函数原型**：
```cpp
pair<iterator, bool> insert_or_assign(const key_type& k, M&& obj);
```

### 使用场景
- 缓存更新
- 配置管理
- 计数器累加

### 代码示例

```cpp
#include <unordered_map>
#include <iostream>
#include <string>

int main() {
    std::unordered_map<std::string, int> cache;
    
    // 插入新元素
    auto [it1, inserted1] = cache.insert_or_assign("key1", 100);
    std::cout << "插入 \"key1\": " << (inserted1 ? "新元素" : "已存在") << std::endl;
    
    // 更新已有元素
    auto [it2, inserted2] = cache.insert_or_assign("key1", 200);
    std::cout << "更新 \"key1\": " << (inserted2 ? "新元素" : "已存在") << std::endl;
    std::cout << "当前值: " << it2->second << std::endl;
    
    // 计数器示例
    std::unordered_map<std::string, int> wordCount;
    std::vector<std::string> words = {"apple", "banana", "apple", "cherry", "apple"};
    
    for (const auto& word : words) {
        auto [it, inserted] = wordCount.insert_or_assign(word, 1);
        if (!inserted) {
            it->second++;
        }
    }
    
    std::cout << "\n词频统计:" << std::endl;
    for (const auto& [word, count] : wordCount) {
        std::cout << word << ": " << count << std::endl;
    }
    
    return 0;
}
```

---

## 309. std::unordered_map::insert

### 功能说明
向哈希表插入新元素。如果键已存在，则插入失败，保持原值不变。

**函数原型**：
```cpp
pair<iterator, bool> insert(const value_type& value);
```

### 使用场景
- 去重集合
- 批量导入
- 首次初始化

### 代码示例

```cpp
#include <unordered_map>
#include <iostream>
#include <string>

int main() {
    std::unordered_map<int, std::string> users;
    
    // 插入成功
    auto result1 = users.insert({1, "Alice"});
    std::cout << "插入 ID 1: " << (result1.second ? "成功" : "失败") << std::endl;
    
    // 插入失败（键已存在）
    auto result2 = users.insert({1, "Bob"});
    std::cout << "插入 ID 1 再次: " << (result2.second ? "成功" : "失败") << std::endl;
    std::cout << "值保持为: " << result2.first->second << std::endl;
    
    // 批量插入
    std::vector<std::pair<int, std::string>> newUsers = {
        {2, "Charlie"},
        {3, "David"},
        {1, "Eve"}  // 这条会失败
    };
    
    for (const auto& user : newUsers) {
        auto result = users.insert(user);
        if (!result.second) {
            std::cout << "跳过重复 ID: " << user.first << std::endl;
        }
    }
    
    std::cout << "\n最终用户列表:" << std::endl;
    for (const auto& [id, name] : users) {
        std::cout << "  " << id << ": " << name << std::endl;
    }
    
    return 0;
}
```

---

## 310. std::unordered_map::find

### 功能说明
在哈希表中查找指定键。平均时间复杂度O(1)，最坏O(n)。

**函数原型**：
```cpp
iterator find(const key_type& key);
const_iterator find(const key_type& key) const;
```

### 使用场景
- 缓存查找
- 配置读取
- 存在性检查

### 代码示例

```cpp
#include <unordered_map>
#include <iostream>
#include <string>

int main() {
    std::unordered_map<std::string, double> prices;
    prices["apple"] = 5.5;
    prices["banana"] = 3.0;
    prices["cherry"] = 8.0;
    
    // 查找存在的键
    auto it = prices.find("banana");
    if (it != prices.end()) {
        std::cout << "香蕉价格: " << it->second << std::endl;
    }
    
    // 查找不存在的键
    auto not_found = prices.find("orange");
    if (not_found == prices.end()) {
        std::cout << "橙子未找到" << std::endl;
    }
    
    // C++17 if with initializer
    if (auto search = prices.find("apple"); search != prices.end()) {
        std::cout << "苹果价格: " << search->second << std::endl;
    }
    
    // 安全获取值
    std::string item = "grape";
    double price = 0.0;
    if (auto it = prices.find(item); it != prices.end()) {
        price = it->second;
    } else {
        price = -1.0;  // 未找到标记
    }
    std::cout << item << " 价格: " << (price > 0 ? std::to_string(price) : "未知") << std::endl;
    
    return 0;
}
```

---

## 311. std::unordered_map::erase

### 功能说明
从哈希表中删除元素，支持通过迭代器、键或范围删除。

**函数原型**：
```cpp
iterator erase(iterator position);
size_type erase(const key_type& key);
iterator erase(const_iterator first, const_iterator last);
```

### 使用场景
- 缓存淘汰
- 会话销毁
- 数据清理

### 代码示例

```cpp
#include <unordered_map>
#include <iostream>
#include <string>

int main() {
    std::unordered_map<int, std::string> sessions;
    sessions[1] = "User1";
    sessions[2] = "User2";
    sessions[3] = "User3";
    sessions[4] = "User4";
    
    std::cout << "初始会话数: " << sessions.size() << std::endl;
    
    // 通过键删除
    size_t removed = sessions.erase(2);
    std::cout << "删除会话 2: " << (removed > 0 ? "成功" : "失败") << std::endl;
    
    // 删除不存在的键
    removed = sessions.erase(99);
    std::cout << "删除会话 99: " << (removed > 0 ? "成功" : "失败") << std::endl;
    
    // 遍历删除（偶数ID）
    for (auto it = sessions.begin(); it != sessions.end(); ) {
        if (it->first % 2 == 0) {
            it = sessions.erase(it);  // erase返回下一个迭代器
        } else {
            ++it;
        }
    }
    
    std::cout << "删除偶数ID后剩余: " << sessions.size() << std::endl;
    for (const auto& [id, user] : sessions) {
        std::cout << "  " << id << ": " << user << std::endl;
    }
    
    // 清空
    sessions.clear();
    std::cout << "清空后: " << sessions.size() << std::endl;
    
    return 0;
}
```

---

## 312. std::unordered_map::empty

### 功能说明
检查容器是否为空，时间复杂度O(1)。

**函数原型**：`bool empty() const noexcept;`

### 使用场景
- 前置条件检查
- 循环条件
- 资源管理

### 代码示例

```cpp
#include <unordered_map>
#include <iostream>
#include <string>

void processIfNotEmpty(const std::unordered_map<std::string, int>& map) {
    if (map.empty()) {
        std::cout << "映射为空，跳过处理" << std::endl;
        return;
    }
    
    std::cout << "处理 " << map.size() << " 个元素:" << std::endl;
    for (const auto& [k, v] : map) {
        std::cout << "  " << k << " = " << v << std::endl;
    }
}

int main() {
    std::unordered_map<std::string, int> data;
    
    processIfNotEmpty(data);
    
    data["key1"] = 100;
    data["key2"] = 200;
    
    processIfNotEmpty(data);
    
    // 作为循环条件
    std::unordered_map<int, std::string> tasks;
    tasks[1] = "Task A";
    tasks[2] = "Task B";
    tasks[3] = "Task C";
    
    std::cout << "\n处理所有任务:" << std::endl;
    while (!tasks.empty()) {
        auto it = tasks.begin();
        std::cout << "处理: " << it->first << " - " << it->second << std::endl;
        tasks.erase(it);
    }
    
    std::cout << "所有任务完成" << std::endl;
    
    return 0;
}
```

---

## 313. std::unordered_map::contains

### 功能说明
C++20引入，检查容器是否包含指定键。比`find() != end()`更简洁。

**函数原型**：
```cpp
bool contains(const Key& key) const;
```

### 使用场景
- 存在性检查
- 白名单/黑名单验证
- 配置项检查

### 代码示例

```cpp
#include <unordered_map>
#include <iostream>
#include <string>

// C++17兼容版本
#if __cplusplus < 202002L
namespace std {
    template<typename K, typename V>
    bool contains(const std::unordered_map<K, V>& map, const K& key) {
        return map.find(key) != map.end();
    }
}
#endif

int main() {
    std::unordered_map<std::string, bool> permissions;
    permissions["read"] = true;
    permissions["write"] = true;
    
    // 检查权限
    if (permissions.contains("read")) {
        std::cout << "有读权限" << std::endl;
    }
    
    if (!permissions.contains("execute")) {
        std::cout << "无执行权限" << std::endl;
    }
    
    // 白名单检查
    std::unordered_map<std::string, int> whitelist;
    whitelist["admin"] = 1;
    whitelist["user"] = 2;
    whitelist["guest"] = 3;
    
    std::string username = "admin";
    if (whitelist.contains(username)) {
        std::cout << username << " 在白名单中，等级: " << whitelist[username] << std::endl;
    }
    
    // 配置默认值
    auto getConfig = [&permissions](const std::string& key, bool defaultVal) -> bool {
        if (permissions.contains(key)) {
            return permissions[key];
        }
        return defaultVal;
    };
    
    std::cout << "delete权限: " << (getConfig("delete", false) ? "允许" : "禁止") << std::endl;
    std::cout << "read权限: " << (getConfig("read", false) ? "允许" : "禁止") << std::endl;
    
    return 0;
}
```

---

## 314. std::uninitialized_move_n

### 功能说明
C++17引入，将n个元素从源范围移动到未初始化的目标内存。使用移动语义而非拷贝。

**函数原型**：
```cpp
pair<InputIt, ForwardIt> uninitialized_move_n(InputIt first, Size count,
                                               ForwardIt d_first);
```

### 使用场景
- vector扩容时移动元素
- 内存池管理
- 批量数据迁移

### 代码示例

```cpp
#include <memory>
#include <vector>
#include <iostream>
#include <string>

struct Resource {
    int id;
    std::string name;
    
    Resource(int i, std::string n) : id(i), name(std::move(n)) {
        std::cout << "构造 " << id << std::endl;
    }
    Resource(Resource&& other) noexcept : id(other.id), name(std::move(other.name)) {
        std::cout << "移动构造 " << id << std::endl;
    }
    ~Resource() { std::cout << "析构 " << id << std::endl; }
};

int main() {
    std::vector<Resource> source;
    source.emplace_back(1, "First");
    source.emplace_back(2, "Second");
    source.emplace_back(3, "Third");
    
    // 分配未初始化内存
    void* mem = ::operator new(sizeof(Resource) * 3);
    Resource* dest = static_cast<Resource*>(mem);
    
    std::cout << "\n执行uninitialized_move_n:" << std::endl;
    auto [src_end, dest_end] = std::uninitialized_move_n(
        source.begin(), 3, dest
    );
    
    std::cout << "\n验证结果:" << std::endl;
    for (int i = 0; i < 3; ++i) {
        std::cout << "dest[" << i << "]: " << dest[i].name << std::endl;
    }
    
    // 清理
    for (int i = 0; i < 3; ++i) {
        dest[i].~Resource();
    }
    ::operator delete(mem);
    
    return 0;
}
```

---

## 315. std::uninitialized_fill_n

### 功能说明
在未初始化的内存区域构造n个相同值的元素。

**函数原型**：
```cpp
ForwardIt uninitialized_fill_n(ForwardIt first, Size count, const T& value);
```

### 使用场景
- 内存池初始化
- 容器构造
- 批量对象创建

### 代码示例

```cpp
#include <memory>
#include <iostream>
#include <string>

class Widget {
public:
    int value;
    Widget(int v) : value(v) { std::cout << "构造 " << value << std::endl; }
    ~Widget() { std::cout << "析构 " << value << std::endl; }
};

int main() {
    // 分配未初始化内存
    void* mem = ::operator new(sizeof(Widget) * 5);
    Widget* widgets = static_cast<Widget*>(mem);
    
    std::cout << "填充5个Widget(值为42):" << std::endl;
    Widget prototype(42);
    std::uninitialized_fill_n(widgets, 5, prototype);
    
    std::cout << "\n验证:" << std::endl;
    for (int i = 0; i < 5; ++i) {
        std::cout << "widgets[" << i << "].value = " << widgets[i].value << std::endl;
    }
    
    // 清理
    std::cout << "\n析构:" << std::endl;
    for (int i = 0; i < 5; ++i) {
        widgets[i].~Widget();
    }
    ::operator delete(mem);
    
    return 0;
}
```

---

## 316. std::uninitialized_default_construct_n

### 功能说明
C++17引入，在未初始化内存上默认构造n个对象。

**函数原型**：
```cpp
ForwardIt uninitialized_default_construct_n(ForwardIt first, Size n);
```

### 使用场景
- 原始缓冲区分配
- 延迟初始化
- 高性能容器实现

### 代码示例

```cpp
#include <memory>
#include <iostream>
#include <string>

class Data {
public:
    int id;
    std::string info;
    Data() : id(-1), info("default") {
        std::cout << "默认构造 id=" << id << std::endl;
    }
    ~Data() { std::cout << "析构 id=" << id << std::endl; }
};

int main() {
    // 分配未初始化内存
    void* mem = ::operator new(sizeof(Data) * 3);
    Data* data = static_cast<Data*>(mem);
    
    std::cout << "默认构造3个Data对象:" << std::endl;
    std::uninitialized_default_construct_n(data, 3);
    
    std::cout << "\n初始值:" << std::endl;
    for (int i = 0; i < 3; ++i) {
        std::cout << "data[" << i << "]: id=" << data[i].id 
                  << ", info=" << data[i].info << std::endl;
    }
    
    // 修改值
    data[0].id = 100;
    data[0].info = "First";
    
    // 清理
    std::cout << "\n析构:" << std::endl;
    for (int i = 0; i < 3; ++i) {
        data[i].~Data();
    }
    ::operator delete(mem);
    
    return 0;
}
```

---

## 317. std::uniform_int_distribution

### 功能说明
生成指定范围内的均匀分布整数。

**类定义**：
```cpp
template<class IntType = int>
class uniform_int_distribution {
public:
    uniform_int_distribution(IntType a, IntType b);
    template<class URBG> result_type operator()(URBG& g);
};
```

### 使用场景
- 游戏随机数
- 测试数据生成
- 随机采样

### 代码示例

```cpp
#include <random>
#include <iostream>
#include <map>

int main() {
    std::random_device rd;
    std::mt19937 gen(rd());
    
    // 骰子 [1, 6]
    std::uniform_int_distribution<> dice(1, 6);
    
    std::cout << "投掷骰子10次:" << std::endl;
    for (int i = 0; i < 10; ++i) {
        std::cout << dice(gen) << " ";
    }
    std::cout << std::endl;
    
    // 统计分布
    std::map<int, int> freq;
    for (int i = 0; i < 1000; ++i) {
        freq[dice(gen)]++;
    }
    
    std::cout << "\n1000次统计:" << std::endl;
    for (int i = 1; i <= 6; ++i) {
        std::cout << i << ": " << freq[i] << " 次" << std::endl;
    }
    
    // 随机选择
    std::uniform_int_distribution<> coin(0, 1);
    std::cout << "\n抛硬币: " << (coin(gen) == 0 ? "正面" : "反面") << std::endl;
    
    return 0;
}
```

---

## 318. std::tolower

### 功能说明
将字符转换为小写形式。

**函数原型**：`int tolower(int ch);`

### 使用场景
- 不区分大小写比较
- 输入规范化
- 文件名处理

### 代码示例

```cpp
#include <cctype>
#include <iostream>
#include <string>
#include <algorithm>

std::string to_lower(const std::string& str) {
    std::string result = str;
    std::transform(result.begin(), result.end(), result.begin(),
        [](unsigned char c) { return std::tolower(c); });
    return result;
}

bool case_insensitive_equal(const std::string& a, const std::string& b) {
    if (a.length() != b.length()) return false;
    return std::equal(a.begin(), a.end(), b.begin(),
        [](char ca, char cb) {
            return std::tolower(static_cast<unsigned char>(ca)) == 
                   std::tolower(static_cast<unsigned char>(cb));
        });
}

int main() {
    std::string text = "Hello, WORLD! 123";
    std::cout << "原始: " << text << std::endl;
    std::cout << "小写: " << to_lower(text) << std::endl;
    
    std::cout << "\n比较测试:" << std::endl;
    std::cout << "\"Hello\" == \"hello\": " 
              << (case_insensitive_equal("Hello", "hello") ? "相等" : "不等") << std::endl;
    std::cout << "\"Apple\" == \"APPLE\": " 
              << (case_insensitive_equal("Apple", "APPLE") ? "相等" : "不等") << std::endl;
    
    // 命令解析
    std::string cmd = "QUIT";
    if (case_insensitive_equal(cmd, "quit")) {
        std::cout << "\n识别到退出命令" << std::endl;
    }
    
    return 0;
}
```

---

## 319. std::tmpnam

### 功能说明
生成临时文件名。存在竞争条件风险，不推荐使用。

**函数原型**：`char* tmpnam(char* filename);`

**安全替代**：使用`std::filesystem`或`std::tmpfile`

### 代码示例

```cpp
#include <cstdio>
#include <iostream>
#include <filesystem>
namespace fs = std::filesystem;

int main() {
    // 不推荐的方式
    char filename[L_tmpnam];
    if (std::tmpnam(filename) != nullptr) {
        std::cout << "生成的临时文件名: " << filename << std::endl;
    }
    
    // 推荐：使用std::tmpfile
    std::FILE* tmpfile = std::tmpfile();
    if (tmpfile) {
        std::fputs("写入临时文件\n", tmpfile);
        std::rewind(tmpfile);
        
        char buffer[100];
        if (std::fgets(buffer, sizeof(buffer), tmpfile)) {
            std::cout << "读取: " << buffer;
        }
        std::fclose(tmpfile);
    }
    
    // 最佳：使用filesystem
    fs::path temp_dir = fs::temp_directory_path();
    fs::path temp_file = temp_dir / "myapp_temp.txt";
    
    std::cout << "\n安全的临时文件路径: " << temp_file << std::endl;
    
    return 0;
}
```

---

## 320. std::this_thread::yield

### 功能说明
让出当前线程的CPU时间片。

**函数原型**：`void yield() noexcept;`

### 使用场景
- 自旋锁优化
- 协作式调度
- 负载均衡

### 代码示例

```cpp
#include <thread>
#include <atomic>
#include <iostream>
#include <chrono>

class SpinLock {
    std::atomic_flag flag_ = ATOMIC_FLAG_INIT;
public:
    void lock() {
        // 快速尝试几次
        for (int i = 0; i < 10; ++i) {
            if (!flag_.test_and_set(std::memory_order_acquire)) return;
        }
        // 失败后yield
        while (flag_.test_and_set(std::memory_order_acquire)) {
            std::this_thread::yield();
        }
    }
    void unlock() { flag_.clear(std::memory_order_release); }
};

int main() {
    SpinLock lock;
    int shared = 0;
    
    auto worker = [&]() {
        for (int i = 0; i < 1000; ++i) {
            lock.lock();
            ++shared;
            lock.unlock();
        }
    };
    
    std::thread t1(worker);
    std::thread t2(worker);
    
    t1.join();
    t2.join();
    
    std::cout << "最终结果: " << shared << std::endl;
    return 0;
}
```

---

## 321. std::this_thread::sleep_for

### 功能说明
让当前线程暂停指定时间。

**函数原型**：
```cpp
template<class Rep, class Period>
void sleep_for(const std::chrono::duration<Rep, Period>& sleep_duration);
```

### 使用场景
- 定时任务
- 节流控制
- 忙等待优化

### 代码示例

```cpp
#include <thread>
#include <chrono>
#include <iostream>

void countdown(int seconds) {
    for (int i = seconds; i > 0; --i) {
        std::cout << "倒计时: " << i << " 秒\r" << std::flush;
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
    std::cout << "\n发射!" << std::endl;
}

int main() {
    // 不同时间单位
    std::cout << "睡眠100毫秒..." << std::endl;
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    
    std::cout << "睡眠500微秒..." << std::endl;
    std::this_thread::sleep_for(std::chrono::microseconds(500));
    
    // 倒计时
    std::cout << "\n开始倒计时:" << std::endl;
    countdown(3);
    
    // 帧率限制
    auto frame_start = std::chrono::steady_clock::now();
    // 模拟渲染...
    std::this_thread::sleep_for(std::chrono::milliseconds(10));
    auto frame_end = std::chrono::steady_clock::now();
    
    auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(
        frame_end - frame_start);
    std::cout << "帧耗时: " << elapsed.count() << " ms" << std::endl;
    
    return 0;
}
```

---

## 322. std::terminate

### 功能说明
异常处理失败时终止程序。

**函数原型**：`[[noreturn]] void terminate() noexcept;`

### 使用场景
- 不可恢复错误
- 契约违反
- 调试辅助

### 代码示例

```cpp
#include <exception>
#include <iostream>
#include <cstdlib>

void custom_handler() {
    std::cerr << "程序异常终止!" << std::endl;
    std::abort();
}

void critical_operation(void* ptr) {
    if (ptr == nullptr) {
        std::cerr << "关键操作：空指针错误!" << std::endl;
        std::terminate();  // 无法恢复
    }
}

int main() {
    std::set_terminate(custom_handler);
    
    // 契约检查宏
    #define CONTRACT_CHECK(cond, msg) \
        do { \
            if (!(cond)) { \
                std::cerr << "契约违反: " << msg << std::endl; \
                std::terminate(); \
            } \
        } while(0)
    
    int* data = new int(42);
    CONTRACT_CHECK(data != nullptr, "内存分配失败");
    
    std::cout << "程序正常运行" << std::endl;
    
    delete data;
    return 0;
}
```

---

## 323. std::strncmp

### 功能说明
比较两个C字符串的前n个字符。

**函数原型**：`int strncmp(const char* str1, const char* str2, size_t num);`

### 使用场景
- 安全字符串比较
- 前缀匹配
- 固定长度字段

### 代码示例

```cpp
#include <cstring>
#include <iostream>
#include <string>

bool starts_with(const char* str, const char* prefix) {
    size_t len = std::strlen(prefix);
    return std::strncmp(str, prefix, len) == 0;
}

int main() {
    const char* str1 = "Hello, World!";
    const char* str2 = "Hello, Blender!";
    
    std::cout << "前5个字符比较: " << std::strncmp(str1, str2, 5) << std::endl;
    std::cout << "前13个字符比较: " << std::strncmp(str1, str2, 13) << std::endl;
    
    // 前缀匹配
    std::cout << "'Hello, World!'以'Hello'开头: " 
              << (starts_with(str1, "Hello") ? "是" : "否") << std::endl;
    
    // HTTP方法解析
    const char* request = "GET /index.html HTTP/1.1";
    if (std::strncmp(request, "GET ", 4) == 0) {
        std::cout << "HTTP方法: GET" << std::endl;
    }
    
    return 0;
}
```

---

## 324. std::strings

### 功能说明
非标准组件，可能是自定义类型或统计错误。以下是可能的自定义实现示例。

### 代码示例

```cpp
#include <vector>
#include <string>
#include <iostream>
#include <algorithm>

// 假设的strings实现
class strings {
    std::vector<std::string> data_;
public:
    void add(const std::string& s) { data_.push_back(s); }
    bool contains(const std::string& s) const {
        return std::find(data_.begin(), data_.end(), s) != data_.end();
    }
    std::string join(const std::string& sep) const {
        if (data_.empty()) return "";
        std::string result = data_[0];
        for (size_t i = 1; i < data_.size(); ++i) {
            result += sep + data_[i];
        }
        return result;
    }
};

int main() {
    strings file_types;
    file_types.add(".blend");
    file_types.add(".obj");
    file_types.add(".fbx");
    
    std::cout << "支持.blend: " << (file_types.contains(".blend") ? "是" : "否") << std::endl;
    
    return 0;
}
```

---

## 325. std::string_view:

### 功能说明
语法不完整，可能指`std::string_view::npos`，表示"未找到"的特殊值。

### 代码示例

```cpp
#include <string_view>
#include <iostream>

int main() {
    std::string_view sv = "Hello, World!";
    
    size_t pos = sv.find("World");
    if (pos != std::string_view::npos) {
        std::cout << "找到'World'在位置: " << pos << std::endl;
    }
    
    size_t not_found = sv.find("xyz");
    if (not_found == std::string_view::npos) {
        std::cout << "'xyz'未找到" << std::endl;
    }
    
    std::cout << "npos值: " << std::string_view::npos << std::endl;
    
    return 0;
}
```

---

## 326. std::strcmp

### 功能说明
C风格字符串比较，按字典序比较两个字符串。

**函数原型**：`int strcmp(const char* str1, const char* str2);`

### 代码示例

```cpp
#include <cstring>
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    const char* s1 = "apple";
    const char* s2 = "banana";
    
    std::cout << "strcmp(\"apple\", \"banana\") = " << std::strcmp(s1, s2) << std::endl;
    std::cout << "strcmp(\"apple\", \"apple\") = " << std::strcmp(s1, s1) << std::endl;
    std::cout << "strcmp(\"banana\", \"apple\") = " << std::strcmp(s2, s1) << std::endl;
    
    // 排序
    std::vector<const char*> fruits = {"cherry", "apple", "banana"};
    std::sort(fruits.begin(), fruits.end(),
        [](const char* a, const char* b) { return std::strcmp(a, b) < 0; });
    
    std::cout << "\n排序后: ";
    for (const char* f : fruits) std::cout << f << " ";
    std::cout << std::endl;
    
    return 0;
}
```

---

## 327. std::stol

### 功能说明
字符串转long类型。

**函数原型**：
```cpp
long stol(const string& str, size_t* idx = nullptr, int base = 10);
```

### 代码示例

```cpp
#include <string>
#include <iostream>

int main() {
    // 十进制
    std::string s1 = "12345";
    long val1 = std::stol(s1);
    std::cout << "\"" << s1 << "\" -> " << val1 << std::endl;
    
    // 十六进制
    std::string hex = "FF";
    long val_hex = std::stol(hex, nullptr, 16);
    std::cout << "\"FF\" (hex) -> " << val_hex << std::endl;
    
    // 二进制
    std::string bin = "1010";
    long val_bin = std::stol(bin, nullptr, 2);
    std::cout << "\"1010\" (bin) -> " << val_bin << std::endl;
    
    // 使用idx
    std::string mixed = "42abc";
    size_t pos;
    long val2 = std::stol(mixed, &pos);
    std::cout << "\"" << mixed << "\" 转换了 " << pos << " 个字符，值: " << val2 << std::endl;
    
    return 0;
}
```

---

## 328. std::stof

### 功能说明
字符串转float类型。

**函数原型**：
```cpp
float stof(const string& str, size_t* idx = nullptr);
```

### 代码示例

```cpp
#include <string>
#include <iostream>
#include <iomanip>

int main() {
    // 基本转换
    std::string s1 = "3.14159";
    float f1 = std::stof(s1);
    std::cout << std::fixed << std::setprecision(5);
    std::cout << "\"" << s1 << "\" -> " << f1 << std::endl;
    
    // 科学计数法
    std::string s2 = "1.23e-4";
    float f2 = std::stof(s2);
    std::cout << std::scientific;
    std::cout << "\"" << s2 << "\" -> " << f2 << std::endl;
    
    // 特殊值
    std::cout << std::fixed << "\"inf\" -> " << std::stof("inf") << std::endl;
    std::cout << "\"nan\" -> " << std::stof("nan") << std::endl;
    
    // 解析3D坐标
    std::string coords = "1.5 2.5 3.5";
    size_t idx = 0;
    float x = std::stof(coords, &idx);
    float y = std::stof(coords.substr(idx), &idx);
    float z = std::stof(coords.substr(idx));
    
    std::cout << std::fixed;
    std::cout << "\n坐标: (" << x << ", " << y << ", " << z << ")" << std::endl;
    
    return 0;
}
```

---

## 329. std::stack::emplace

### 功能说明
在栈顶原地构造元素，避免临时对象创建。

**函数原型**：
```cpp
template<class... Args>
void emplace(Args&&... args);
```

### 代码示例

```cpp
#include <stack>
#include <iostream>
#include <string>
#include <memory>

struct Task {
    int id;
    std::string name;
    int priority;
    
    Task(int i, std::string n, int p) 
        : id(i), name(std::move(n)), priority(p) {
        std::cout << "构造 Task(" << id << ", " << name << ")" << std::endl;
    }
};

int main() {
    std::stack<Task> tasks;
    
    // emplace直接构造
    tasks.emplace(1, "Task1", 5);
    tasks.emplace(2, "Task2", 3);
    
    std::cout << "\n处理任务:" << std::endl;
    while (!tasks.empty()) {
        std::cout << "处理: " << tasks.top().name 
                  << " (优先级: " << tasks.top().priority << ")" << std::endl;
        tasks.pop();
    }
    
    // unique_ptr示例
    std::stack<std::unique_ptr<Task>> ptr_stack;
    ptr_stack.emplace(std::make_unique<Task>(10, "Important", 9));
    
    auto task = std::move(ptr_stack.top());
    ptr_stack.pop();
    std::cout << "\n取出任务: " << task->name << std::endl;
    
    return 0;
}
```

---

## 330. std::stable_partition

### 功能说明
稳定分区，保持各组内元素相对顺序。

**函数原型**：
```cpp
BidirIt stable_partition(BidirIt first, BidirIt last, UnaryPredicate p);
```

### 代码示例

```cpp
#include <algorithm>
#include <vector>
#include <iostream>
#include <string>

struct File {
    std::string name;
    bool is_directory;
};

int main() {
    std::vector<File> files = {
        {"doc.txt", false},
        {"images", true},
        {"script.py", false},
        {"data", true},
        {"readme.md", false}
    };
    
    std::cout << "原始顺序:" << std::endl;
    for (const auto& f : files) {
        std::cout << (f.is_directory ? "[DIR] " : "[FILE] ") << f.name << std::endl;
    }
    
    // 稳定分区：目录在前
    auto mid = std::stable_partition(files.begin(), files.end(),
        [](const File& f) { return f.is_directory; });
    
    std::cout << "\n分区后:" << std::endl;
    std::cout << "--- 目录 ---" << std::endl;
    for (auto it = files.begin(); it != mid; ++it) {
        std::cout << it->name << std::endl;
    }
    std::cout << "--- 文件 ---" << std::endl;
    for (auto it = mid; it != files.end(); ++it) {
        std::cout << it->name << std::endl;
    }
    
    return 0;
}
```

---

## 331. std::sscanf

### 功能说明
C风格字符串格式化输入。

**函数原型**：`int sscanf(const char* str, const char* format, ...);`

### 代码示例

```cpp
#include <cstdio>
#include <iostream>
#include <string>

int main() {
    // 基本解析
    const char* data = "42 3.14 Hello";
    int i;
    double d;
    char s[100];
    
    std::sscanf(data, "%d %lf %s", &i, &d, s);
    std::cout << "整数: " << i << ", 浮点: " << d << ", 字符串: " << s << std::endl;
    
    // 解析日期
    const char* date = "2024-03-15";
    int year, month, day;
    std::sscanf(date, "%d-%d-%d", &year, &month, &day);
    std::cout << "日期: " << year << "年" << month << "月" << day << "日" << std::endl;
    
    // 解析顶点数据 (OBJ格式)
    const char* vertex = "v 1.0 2.0 3.0";
    char type;
    float x, y, z;
    std::sscanf(vertex, "%c %f %f %f", &type, &x, &y, &z);
    if (type == 'v') {
        std::cout << "顶点: (" << x << ", " << y << ", " << z << ")" << std::endl;
    }
    
    return 0;
}
```

---

## 332. std::smatch

### 功能说明
正则匹配结果容器。

**类型定义**：`using smatch = match_results<string::const_iterator>;`

### 代码示例

```cpp
#include <regex>
#include <string>
#include <iostream>

int main() {
    std::string text = "Email: john.doe@example.com";
    std::regex email_pattern(R"((\w+)\.(\w+)@(\w+)\.(\w+))");
    std::smatch match;
    
    if (std::regex_search(text, match, email_pattern)) {
        std::cout << "完整匹配: " << match[0] << std::endl;
        std::cout << "名: " << match[1] << std::endl;
        std::cout << "姓: " << match[2] << std::endl;
        std::cout << "域名: " << match[3] << std::endl;
        std::cout << "后缀: " << match[4] << std::endl;
    }
    
    // 提取所有匹配
    std::string log = "Error 404 at /page1, Error 500 at /page2";
    std::regex error_pattern(R"(Error (\d+) at (\S+))");
    std::sregex_iterator it(log.begin(), log.end(), error_pattern);
    std::sregex_iterator end;
    
    std::cout << "\n所有错误:" << std::endl;
    for (; it != end; ++it) {
        std::smatch m = *it;
        std::cout << "代码: " << m[1] << ", 路径: " << m[2] << std::endl;
    }
    
    return 0;
}
```

---

## 333. std::shuffle

### 功能说明
随机打乱范围内元素顺序。

**函数原型**：
```cpp
void shuffle(RandomIt first, RandomIt last, URBG&& g);
```

### 代码示例

```cpp
#include <algorithm>
#include <random>
#include <vector>
#include <iostream>
#include <chrono>

int main() {
    std::vector<int> deck;
    for (int i = 1; i <= 52; ++i) deck.push_back(i);
    
    std::random_device rd;
    std::mt19937 g(rd());
    
    std::cout << "洗牌前前10张: ";
    for (int i = 0; i < 10; ++i) std::cout << deck[i] << " ";
    std::cout << std::endl;
    
    // 洗牌
    std::shuffle(deck.begin(), deck.end(), g);
    
    std::cout << "洗牌后前10张: ";
    for (int i = 0; i < 10; ++i) std::cout << deck[i] << " ";
    std::cout << std::endl;
    
    // 打乱字符串
    std::string word = "HelloWorld";
    std::shuffle(word.begin(), word.end(), g);
    std::cout << "打乱后的字符串: " << word << std::endl;
    
    return 0;
}
```

---

## 334. std::showbase

### 功能说明
IO操纵符，显示进制前缀（0x表示十六进制，0表示八进制）。

**函数原型**：`ios_base& showbase(ios_base& str);`

### 代码示例

```cpp
#include <iostream>
#include <iomanip>

int main() {
    int num = 255;
    
    std::cout << "默认: " << num << std::endl;
    
    // 十六进制
    std::cout << "\n十六进制:" << std::endl;
    std::cout << std::hex << std::showbase;
    std::cout << "showbase: " << num << std::endl;
    std::cout << std::noshowbase;
    std::cout << "noshowbase: " << num << std::endl;
    
    // 八进制
    std::cout << "\n八进制:" << std::endl;
    std::cout << std::oct << std::showbase;
    std::cout << "showbase: " << num << std::endl;
    std::cout << std::noshowbase;
    std::cout << "noshowbase: " << num << std::endl;
    
    // 恢复十进制
    std::cout << std::dec << std::endl;
    
    return 0;
}
```

---

## 335. std::roundf

### 功能说明
float类型四舍五入到最接近的整数值。

**函数原型**：`float roundf(float x);`

### 代码示例

```cpp
#include <cmath>
#include <iostream>
#include <iomanip>

int main() {
    std::cout << std::fixed << std::setprecision(1);
    
    float values[] = {2.3f, 2.5f, 2.7f, -2.3f, -2.5f, -2.7f};
    
    std::cout << "四舍五入结果:" << std::endl;
    for (float v : values) {
        std::cout << "roundf(" << v << ") = " << std::roundf(v) << std::endl;
    }
    
    // 像素对齐
    float x = 10.7f, y = 20.3f;
    int pixel_x = static_cast<int>(std::roundf(x));
    int pixel_y = static_cast<int>(std::roundf(y));
    std::cout << "\n像素坐标: (" << pixel_x << ", " << pixel_y << ")" << std::endl;
    
    return 0;
}
```

---

## 336. std::rotl

### 功能说明
C++20引入，循环左移位操作。

**函数原型**：
```cpp
template<class T>
T rotl(T x, int s);
```

### 代码示例

```cpp
#include <bit>
#include <iostream>
#include <bitset>

int main() {
    unsigned int x = 0b00010010;  // 18
    
    std::cout << "原始: " << std::bitset<8>(x) << " (" << x << ")" << std::endl;
    
    // 循环左移2位
    auto rotated = std::rotl(x, 2);
    std::cout << "左移2位: " << std::bitset<8>(rotated) << " (" << rotated << ")" << std::endl;
    
    // 哈希计算
    unsigned int hash = 0x12345678;
    hash = std::rotl(hash, 13);
    std::cout << "\n哈希值: " << std::hex << hash << std::endl;
    
    return 0;
}
```

---

## 337. std::replace_if

### 功能说明
条件替换范围内元素。

**函数原型**：
```cpp
void replace_if(ForwardIt first, ForwardIt last, 
                UnaryPredicate p, const T& new_value);
```

### 代码示例

```cpp
#include <algorithm>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> nums = {1, -2, 3, -4, 5, -6};
    
    std::cout << "替换前: ";
    for (int n : nums) std::cout << n << " ";
    std::cout << std::endl;
    
    // 将所有负数替换为0
    std::replace_if(nums.begin(), nums.end(),
        [](int n) { return n < 0; }, 0);
    
    std::cout << "替换后: ";
    for (int n : nums) std::cout << n << " ";
    std::cout << std::endl;
    
    // 替换空字符串
    std::vector<std::string> names = {"Alice", "", "Bob", "", "Charlie"};
    std::replace_if(names.begin(), names.end(),
        [](const std::string& s) { return s.empty(); }, "Unknown");
    
    std::cout << "\n处理后: ";
    for (const auto& n : names) std::cout << n << " ";
    std::cout << std::endl;
    
    return 0;
}
```

---

## 338. std::remove_reference

### 功能说明
类型特征，移除引用。

**定义**：`template<class T> struct remove_reference;`

### 代码示例

```cpp
#include <type_traits>
#include <iostream>

int main() {
    // 移除左值引用
    static_assert(std::is_same_v<std::remove_reference_t<int&>, int>);
    
    // 移除右值引用
    static_assert(std::is_same_v<std::remove_reference_t<int&&>, int>);
    
    // 非引用保持不变
    static_assert(std::is_same_v<std::remove_reference_t<int>, int>);
    
    std::cout << "remove_reference_t<int&> is int: " 
              << std::is_same_v<std::remove_reference_t<int&>, int> << std::endl;
    
    return 0;
}
```

---

## 339. std::remove

### 功能说明
逻辑删除范围内指定值的元素（需配合erase使用）。

**函数原型**：
```cpp
ForwardIt remove(ForwardIt first, ForwardIt last, const T& value);
```

### 代码示例

```cpp
#include <algorithm>
#include <vector>
#include <iostream>
#include <string>

int main() {
    std::vector<int> nums = {1, 2, 3, 2, 4, 2, 5};
    
    std::cout << "删除前: ";
    for (int n : nums) std::cout << n << " ";
    std::cout << "(size=" << nums.size() << ")" << std::endl;
    
    // remove-erase惯用法
    auto new_end = std::remove(nums.begin(), nums.end(), 2);
    nums.erase(new_end, nums.end());
    
    std::cout << "删除所有2: ";
    for (int n : nums) std::cout << n << " ";
    std::cout << "(size=" << nums.size() << ")" << std::endl;
    
    // 删除空字符串
    std::vector<std::string> words = {"hello", "", "world", "", "!"};
    words.erase(
        std::remove_if(words.begin(), words.end(),
            [](const std::string& s) { return s.empty(); }),
        words.end()
    );
    
    std::cout << "\n删除空字符串后: ";
    for (const auto& w : words) std::cout << w << " ";
    std::cout << std::endl;
    
    return 0;
}
```

---

## 340. std::regex_match

### 功能说明
正则表达式完全匹配（整个字符串必须符合模式）。

**函数原型**：
```cpp
bool regex_match(const string& str, smatch& m, const regex& re);
```

### 代码示例

```cpp
#include <regex>
#include <string>
#include <iostream>

bool is_valid_email(const std::string& email) {
    std::regex pattern(R"(^[\w.-]+@[\w.-]+\.\w+$)");
    return std::regex_match(email, pattern);
}

bool is_valid_phone(const std::string& phone) {
    std::regex pattern(R"(^\d{3}-\d{3}-\d{4}$)");
    return std::regex_match(phone, pattern);
}

int main() {
    std::vector<std::string> emails = {
        "user@example.com",
        "invalid.email",
        "test@domain.org"
    };
    
    std::cout << "邮箱验证:" << std::endl;
    for (const auto& email : emails) {
        std::cout << email << " -> " 
                  << (is_valid_email(email) ? "有效" : "无效") << std::endl;
    }
    
    std::vector<std::string> phones = {
        "123-456-7890",
        "1234567890",
        "555-123-4567"
    };
    
    std::cout << "\n电话验证:" << std::endl;
    for (const auto& phone : phones) {
        std::cout << phone << " -> " 
                  << (is_valid_phone(phone) ? "有效" : "无效") << std::endl;
    }
    
    // 提取匹配组
    std::string date = "2024-03-15";
    std::regex date_pattern(R"((\d{4})-(\d{2})-(\d{2}))");
    std::smatch match;
    
    if (std::regex_match(date, match, date_pattern)) {
        std::cout << "\n日期解析:" << std::endl;
        std::cout << "年: " << match[1] << std::endl;
        std::cout << "月: " << match[2] << std::endl;
        std::cout << "日: " << match[3] << std::endl;
    }
    
    return 0;
}
```

---

## 341. std::random_device

### 功能说明
非确定性随机数生成器，提供真随机数种子。

**类定义**：提供硬件或系统熵源产生的随机数。

### 代码示例

```cpp
#include <random>
#include <iostream>

int main() {
    // 使用random_device作为种子
    std::random_device rd;
    
    std::cout << "随机种子值:" << std::endl;
    for (int i = 0; i < 5; ++i) {
        std::cout << rd() << " ";
    }
    std::cout << std::endl;
    
    // 创建高质量的随机数引擎
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dist(1, 100);
    
    std::cout << "\n随机数 [1-100]:" << std::endl;
    for (int i = 0; i < 10; ++i) {
        std::cout << dist(gen) << " ";
    }
    std::cout << std::endl;
    
    // 检查熵（某些平台可能返回0）
    std::cout << "\n熵值: " << rd.entropy() << std::endl;
    
    return 0;
}
```

---

## 342. std::random_access_iterator_tag

### 功能说明
随机访问迭代器标签，用于迭代器分类。

**定义**：`struct random_access_iterator_tag {};`

### 代码示例

```cpp
#include <iterator>
#include <type_traits>
#include <iostream>
#include <vector>
#include <list>

// 根据迭代器类型选择算法
template<typename Iter>
void process(Iter first, Iter last, std::random_access_iterator_tag) {
    std::cout << "使用随机访问迭代器，大小: " << (last - first) << std::endl;
}

template<typename Iter>
void process(Iter first, Iter last, std::bidirectional_iterator_tag) {
    std::cout << "使用双向迭代器" << std::endl;
}

template<typename Iter>
void process(Iter first, Iter last) {
    using category = typename std::iterator_traits<Iter>::iterator_category;
    process(first, last, category());
}

int main() {
    std::vector<int> vec = {1, 2, 3, 4, 5};
    std::list<int> lst = {1, 2, 3, 4, 5};
    
    std::cout << "vector: ";
    process(vec.begin(), vec.end());
    
    std::cout << "list: ";
    process(lst.begin(), lst.end());
    
    return 0;
}
```

---

## 343. std::rand

### 功能说明
C风格随机数生成。质量较低，建议使用C++11 `<random>`。

**函数原型**：`int rand();`

### 代码示例

```cpp
#include <cstdlib>
#include <ctime>
#include <iostream>

int main() {
    // 设置种子（只需一次）
    std::srand(std::time(nullptr));
    
    std::cout << "rand() 生成 [0, RAND_MAX]:" << std::endl;
    for (int i = 0; i < 5; ++i) {
        std::cout << std::rand() << " ";
    }
    std::cout << std::endl;
    
    // 生成 [0, 99]
    std::cout << "\n生成 [0, 99]:" << std::endl;
    for (int i = 0; i < 5; ++i) {
        std::cout << std::rand() % 100 << " ";
    }
    std::cout << std::endl;
    
    // 生成 [1, 6] (骰子)
    std::cout << "\n骰子 [1, 6]:" << std::endl;
    for (int i = 0; i < 10; ++i) {
        std::cout << (std::rand() % 6 + 1) << " ";
    }
    std::cout << std::endl;
    
    return 0;
}
```

---

## 344. std::push_heap

### 功能说明
将元素推入堆结构（需在已有堆的末尾添加元素后调用）。

**函数原型**：
```cpp
void push_heap(RandomIt first, RandomIt last);
```

### 代码示例

```cpp
#include <algorithm>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> heap;
    
    // 添加元素并维护堆
    auto push = [&](int val) {
        heap.push_back(val);
        std::push_heap(heap.begin(), heap.end());
        std::cout << "推入 " << val << ", 堆顶: " << heap.front() << std::endl;
    };
    
    push(3);
    push(1);
    push(4);
    push(1);
    push(5);
    push(9);
    
    std::cout << "\n堆内容: ";
    for (int n : heap) std::cout << n << " ";
    std::cout << std::endl;
    
    return 0;
}
```

---

## 345. std::pop_heap

### 功能说明
将堆顶元素移到末尾并调整堆（最大堆将最大值移到末尾）。

**函数原型**：
```cpp
void pop_heap(RandomIt first, RandomIt last);
```

### 代码示例

```cpp
#include <algorithm>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> heap = {9, 5, 4, 1, 1, 3};
    std::make_heap(heap.begin(), heap.end());
    
    std::cout << "初始堆: ";
    for (int n : heap) std::cout << n << " ";
    std::cout << "\n堆顶: " << heap.front() << std::endl;
    
    // 弹出堆顶
    std::pop_heap(heap.begin(), heap.end());
    int max_val = heap.back();
    heap.pop_back();
    
    std::cout << "弹出 " << max_val << ", 剩余: ";
    for (int n : heap) std::cout << n << " ";
    std::cout << "\n新堆顶: " << heap.front() << std::endl;
    
    // 堆排序
    std::vector<int> data = {3, 1, 4, 1, 5, 9, 2, 6};
    std::make_heap(data.begin(), data.end());
    
    std::cout << "\n堆排序: ";
    for (size_t i = data.size(); i > 0; --i) {
        std::pop_heap(data.begin(), data.begin() + i);
    }
    
    for (int n : data) std::cout << n << " ";
    std::cout << std::endl;
    
    return 0;
}
```

---

## 346. std::partial_sort

### 功能说明
部分排序，只保证前n个元素有序且是最小的n个。

**函数原型**：
```cpp
void partial_sort(RandomIt first, RandomIt middle, RandomIt last);
```

### 代码示例

```cpp
#include <algorithm>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> data = {9, 2, 7, 4, 5, 1, 8, 3, 6};
    
    std::cout << "原始: ";
    for (int n : data) std::cout << n << " ";
    std::cout << std::endl;
    
    // 只排序前3个最小的
    std::partial_sort(data.begin(), data.begin() + 3, data.end());
    
    std::cout << "部分排序(前3个): ";
    for (int n : data) std::cout << n << " ";
    std::cout << std::endl;
    
    std::cout << "\n前3个(已排序): ";
    for (int i = 0; i < 3; ++i) std::cout << data[i] << " ";
    std::cout << "\n其余(未排序): ";
    for (size_t i = 3; i < data.size(); ++i) std::cout << data[i] << " ";
    std::cout << std::endl;
    
    return 0;
}
```

---

## 347. std::out_of_range

### 功能说明
越界访问异常，继承自`std::logic_error`。

**类定义**：`class out_of_range : public logic_error;`

### 代码示例

```cpp
#include <stdexcept>
#include <vector>
#include <iostream>
#include <string>

int safe_at(const std::vector<int>& vec, size_t index, int default_val) {
    try {
        return vec.at(index);  // 会抛出out_of_range
    } catch (const std::out_of_range& e) {
        std::cerr << "越界访问: " << e.what() << std::endl;
        return default_val;
    }
}

int main() {
    std::vector<int> nums = {10, 20, 30};
    
    // 正常访问
    std::cout << "索引1: " << safe_at(nums, 1, -1) << std::endl;
    
    // 越界访问
    std::cout << "索引10: " << safe_at(nums, 10, -1) << std::endl;
    
    // 使用std::stoi可能抛出
    try {
        std::string str = "12345678901234567890";
        long val = std::stol(str);  // 可能out_of_range
    } catch (const std::out_of_range& e) {
        std::cout << "数值超出范围" << std::endl;
    }
    
    return 0;
}
```

---

## 348. std::nth_element

### 功能说明
快速选择算法，使第n元素处于正确位置（类似快速排序的partition）。

**函数原型**：
```cpp
void nth_element(RandomIt first, RandomIt nth, RandomIt last);
```

### 代码示例

```cpp
#include <algorithm>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> data = {9, 2, 7, 4, 5, 1, 8, 3, 6};
    
    std::cout << "原始: ";
    for (int n : data) std::cout << n << " ";
    std::cout << std::endl;
    
    // 找中位数（第5个元素，0索引为4）
    auto data_copy = data;
    std::nth_element(data_copy.begin(), data_copy.begin() + 4, data_copy.end());
    std::cout << "中位数(第5小): " << data_copy[4] << std::endl;
    
    // 找第3小的元素
    data_copy = data;
    std::nth_element(data_copy.begin(), data_copy.begin() + 2, data_copy.end());
    std::cout << "第3小: " << data_copy[2] << std::endl;
    
    // 找最大的元素
    data_copy = data;
    std::nth_element(data_copy.begin(), data_copy.end() - 1, data_copy.end());
    std::cout << "最大值: " << data_copy.back() << std::endl;
    
    std::cout << "\n注意：nth_element后元素顺序:\n左边 <= 第n元素 <= 右边" << std::endl;
    
    return 0;
}
```

---

## 349. std::norm

### 功能说明
计算复数模的平方（|z|²）。

**函数原型**：
```cpp
double norm(const complex<double>& z);
```

### 代码示例

```cpp
#include <complex>
#include <iostream>

int main() {
    std::complex<double> z(3.0, 4.0);  // 3 + 4i
    
    std::cout << "复数: " << z << std::endl;
    std::cout << "模: " << std::abs(z) << std::endl;
    std::cout << "模的平方 (norm): " << std::norm(z) << std::endl;
    
    // 验证: norm(z) = |z|² = 3² + 4² = 25
    std::cout << "验证: 3² + 4² = " << 3*3 + 4*4 << std::endl;
    
    // 信号处理应用
    std::complex<double> signal(1.0, 1.0);
    double power = std::norm(signal);
    std::cout << "\n信号功率: " << power << std::endl;
    
    return 0;
}
```

---

## 350. std::noopt

### 功能说明
非标准组件，可能是编译器特定扩展或统计错误。在Blender代码库中可能用于特定优化控制。

### 代码示例

由于此组件非标准，以下展示可能的编译器扩展用法：

```cpp
#include <iostream>

// 某些编译器可能使用__attribute__((noopt))或类似语法
// 这里展示常规优化控制方法

// 防止函数内联
[[gnu::noinline]]
void no_inline_function() {
    std::cout << "此函数不会被内联" << std::endl;
}

// 防止优化掉变量
volatile int prevent_optimization = 0;

int main() {
    // 使用volatile防止优化
    for (volatile int i = 0; i < 1000000; ++i) {
        prevent_optimization += i;
    }
    
    std::cout << "结果: " << prevent_optimization << std::endl;
    
    no_inline_function();
    
    return 0;
}
```

---

## 总结

本文档详细分析了Blender代码库中第301-350位的50个std::组件，每个组件都包含：

| 类别 | 组件数量 | 代表组件 |
|:---|:---:|:---|
| 数学函数 | 4 | asin, acos, norm, roundf |
| 容器操作 | 10 | vector::pop_back/insert, unordered_map方法 |
| 内存算法 | 3 | uninitialized_move_n, uninitialized_fill_n, uninitialized_default_construct_n |
| 字符串处理 | 5 | tolower, strcmp, strncmp, stol, stof |
| 随机数 | 3 | uniform_int_distribution, random_device, rand |
| 算法 | 6 | adjacent_find, stable_partition, shuffle, nth_element等 |
| 线程 | 2 | yield, sleep_for |
| 正则表达式 | 2 | smatch, regex_match |
| IO操纵符 | 1 | showbase |
| 类型特征 | 1 | remove_reference |
| 异常 | 1 | out_of_range |
| 其他 | 12 | void_t, any, terminate, tmpnam等 |

这些组件反映了Blender在处理3D图形、物理模拟、多线程渲染、内存管理等方面的需求。

---

**文档信息**
- **统计来源**：Blender代码库
- **分析范围**：第301-350个std::组件
- **文档版本**：2.0（完整版）
- **生成日期**：2026-02-07

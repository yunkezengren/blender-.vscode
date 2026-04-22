# Blender代码库中最常用的49个std::组件详解与示例

本文档详细介绍了Blender代码库中使用频率最高的49个C++标准库组件，每个组件都包含完整说明和实际代码示例。

---

## 1. std::string（使用5031次）

**说明**：标准字符串类，用于动态字符串存储和操作。

**示例**：
```cpp
#include <string>
#include <iostream>

int main() {
    std::string name = "Blender";
    name += " 3D";  // 字符串连接
    std::cout << "长度: " << name.length() << std::endl;  // 输出: 长度: 11
    
    if (name.find("3D") != std::string::npos) {
        std::cout << "找到了3D" << std::endl;
    }
    return 0;
}
```

---

## 2. std::optional（使用3220次）

**说明**：C++17引入的可选值类型，表示可能存在或不存在的值，避免使用nullptr或特殊值。

**示例**：
```cpp
#include <optional>
#include <string>

std::optional<std::string> findUser(int id) {
    if (id == 1) {
        return "Alice";
    }
    return std::nullopt;  // 表示无值
}

int main() {
    auto user = findUser(1);
    if (user.has_value()) {
        std::cout << "用户: " << user.value() << std::endl;
    }
    
    // 使用默认值
    auto user2 = findUser(999).value_or("未知用户");
    return 0;
}
```

---

## 3. std::nullopt（使用2383次）

**说明**：用于表示`std::optional`的空值状态，类似于nullptr但用于optional。

**示例**：
```cpp
#include <optional>

std::optional<int> divide(int a, int b) {
    if (b == 0) {
        return std::nullopt;  // 除数为0时返回空
    }
    return a / b;
}

int main() {
    auto result = divide(10, 0);
    if (result == std::nullopt) {
        std::cout << "除法错误" << std::endl;
    }
    return 0;
}
```

---

## 4. std::move（使用1705次）

**说明**：将对象转换为右值引用，启用移动语义，避免不必要的拷贝。

**示例**：
```cpp
#include <vector>
#include <string>

std::vector<std::string> createLargeVector() {
    std::vector<std::string> vec;
    vec.reserve(1000);
    for (int i = 0; i < 1000; ++i) {
        vec.push_back("Element " + std::to_string(i));
    }
    return std::move(vec);  // 移动而非拷贝
}

int main() {
    std::string str = "Hello";
    std::string new_str = std::move(str);  // str变为空，资源转移到new_str
    return 0;
}
```

---

## 5. std::unique_ptr（使用1353次）

**说明**：独占所有权的智能指针，自动管理动态内存，防止内存泄漏。

**示例**：
```cpp
#include <memory>

class Mesh {
public:
    Mesh() { std::cout << "Mesh创建" << std::endl; }
    ~Mesh() { std::cout << "Mesh销毁" << std::endl; }
    void render() { std::cout << "渲染Mesh" << std::endl; }
};

int main() {
    // 创建unique_ptr
    std::unique_ptr<Mesh> mesh = std::make_unique<Mesh>();
    mesh->render();
    
    // 转移所有权
    std::unique_ptr<Mesh> mesh2 = std::move(mesh);
    
    // 函数结束时自动释放内存，无需手动delete
    return 0;
}
```

---

## 6. std::max（使用1003次）

**说明**：返回两个值中较大者，可用于比较数值或自定义对象。

**示例**：
```cpp
#include <algorithm>

int main() {
    int a = 10, b = 20;
    int max_val = std::max(a, b);  // 返回20
    
    // 使用lambda比较
    std::string s1 = "apple", s2 = "banana";
    auto& longer = std::max(s1, s2, 
        [](const auto& x, const auto& y) { 
            return x.length() < y.length(); 
        });
    
    return 0;
}
```

---

## 7. std::min（使用736次）

**说明**：返回两个值中较小者，与std::max对应。

**示例**：
```cpp
#include <algorithm>
#include <iostream>

int main() {
    int width = 800, height = 600;
    int min_dimension = std::min(width, height);  // 返回600
    
    // 初始化列表版本
    int smallest = std::min({10, 5, 8, 3, 12});  // 返回3
    
    std::cout << "最小值: " << smallest << std::endl;
    return 0;
}
```

---

## 8. std::make_unique（使用716次）

**说明**：C++14引入的工厂函数，安全地创建unique_ptr，异常安全。

**示例**：
```cpp
#include <memory>
#include <vector>

class Node {
public:
    int value;
    Node(int v) : value(v) {}
};

int main() {
    // 推荐使用make_unique
    auto node = std::make_unique<Node>(42);
    
    // 对比：不推荐直接new
    // std::unique_ptr<Node> node2(new Node(42));  // 异常不安全
    
    // 数组版本
    auto buffer = std::make_unique<int[]>(100);
    buffer[0] = 1;
    
    return 0;
}
```

---

## 9. std::cout（使用690次）

**说明**：标准输出流对象，用于向控制台输出数据。

**示例**：
```cpp
#include <iostream>
#include <iomanip>

int main() {
    std::cout << "Blender 3D软件" << std::endl;
    
    // 格式化输出
    double pi = 3.14159265;
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Pi = " << pi << std::endl;  // Pi = 3.14
    
    // 多数据输出
    int vertices = 1000;
    std::cout << "顶点数: " << vertices << " 个" << std::endl;
    
    return 0;
}
```

---

## 10. std::array（使用653次）

**说明**：固定大小的数组容器，比C风格数组更安全，支持STL算法。

**示例**：
```cpp
#include <array>
#include <algorithm>

int main() {
    // 固定大小数组
    std::array<int, 5> numbers = {1, 2, 3, 4, 5};
    
    // 边界检查访问
    numbers.at(2) = 10;  // 安全访问，越界抛出异常
    
    // 迭代器支持
    std::sort(numbers.begin(), numbers.end());
    
    // 获取大小
    constexpr size_t size = numbers.size();  // 编译时常量
    
    return 0;
}
```

---

## 11. std::swap（使用417次）

**说明**：交换两个对象的值，可为自定义类型特化。

**示例**：
```cpp
#include <algorithm>
#include <string>

int main() {
    int a = 10, b = 20;
    std::swap(a, b);  // a=20, b=10
    
    std::string s1 = "Hello";
    std::string s2 = "World";
    std::swap(s1, s2);  // 高效交换字符串内容
    
    // 数组交换
    int arr1[] = {1, 2, 3};
    int arr2[] = {4, 5, 6};
    std::swap(arr1, arr2);  // 交换整个数组
    
    return 0;
}
```

---

## 12. std::endl（使用356次）

**说明**：输出换行符并刷新缓冲区，用于立即显示输出。

**示例**：
```cpp
#include <iostream>

int main() {
    std::cout << "正在处理...";
    std::cout.flush();  // 立即显示
    
    // 等同于endl但更高效的方式
    std::cout << "完成" << '\n';  // 仅换行，不刷新
    
    // 需要立即显示时使用endl
    std::cerr << "错误信息" << std::endl;  // 错误流立即刷新
    
    return 0;
}
```

---

## 13. std::vector（使用336次）

**说明**：动态数组容器，可自动扩展大小，最常用的序列容器。

**示例**：
```cpp
#include <vector>
#include <string>

int main() {
    std::vector<int> numbers;
    numbers.reserve(100);  // 预分配空间
    
    for (int i = 0; i < 10; ++i) {
        numbers.push_back(i * i);
    }
    
    // 范围for循环
    for (const auto& num : numbers) {
        std::cout << num << " ";
    }
    
    // 访问元素
    int first = numbers.front();
    int last = numbers.back();
    
    return 0;
}
```

---

## 14. std::shared_ptr（使用334次）

**说明**：共享所有权智能指针，通过引用计数管理资源生命周期。

**示例**：
```cpp
#include <memory>

class Texture {
public:
    std::string name;
    Texture(const std::string& n) : name(n) {
        std::cout << "Texture " << name << " 创建" << std::endl;
    }
    ~Texture() {
        std::cout << "Texture " << name << " 销毁" << std::endl;
    }
};

int main() {
    {
        std::shared_ptr<Texture> tex1 = std::make_shared<Texture>("diffuse");
        {
            std::shared_ptr<Texture> tex2 = tex1;  // 共享所有权
            std::cout << "引用计数: " << tex1.use_count() << std::endl;  // 2
        }  // tex2销毁，引用计数减1
        std::cout << "引用计数: " << tex1.use_count() << std::endl;  // 1
    }  // tex1销毁，Texture销毁
    
    return 0;
}
```

---

## 15. std::ostream（使用298次）

**说明**：输出流基类，用于自定义类型的输出操作。

**示例**：
```cpp
#include <iostream>

class Vector3 {
public:
    float x, y, z;
    Vector3(float x, float y, float z) : x(x), y(y), z(z) {}
    
    // 友元函数重载<<运算符
    friend std::ostream& operator<<(std::ostream& os, const Vector3& v) {
        os << "Vector3(" << v.x << ", " << v.y << ", " << v.z << ")";
        return os;
    }
};

int main() {
    Vector3 vec(1.0f, 2.0f, 3.0f);
    std::cout << vec << std::endl;  // Vector3(1, 2, 3)
    
    // 也可用于文件输出
    std::ofstream file("output.txt");
    file << vec << std::endl;
    
    return 0;
}
```

---

## 16. std::pair（使用294次）

**说明**：包含两个元素的简单元组类型，常用于返回两个值。

**示例**：
```cpp
#include <utility>
#include <map>

std::pair<int, std::string> getUser() {
    return {1, "Alice"};  // C++11列表初始化
}

int main() {
    auto [id, name] = getUser();  // C++17结构化绑定
    
    // 创建pair
    std::pair<std::string, int> person = std::make_pair("Bob", 25);
    
    // 在map中使用
    std::map<std::string, int> scores;
    scores.insert(std::make_pair("Alice", 95));
    
    return 0;
}
```

---

## 17. std::stringstream（使用265次）

**说明**：字符串流，允许像操作IO流一样处理字符串，用于格式化。

**示例**：
```cpp
#include <sstream>
#include <string>

int main() {
    // 构建字符串
    std::stringstream ss;
    ss << "用户: " << "Alice" << ", 分数: " << 95.5;
    std::string result = ss.str();
    
    // 解析字符串
    std::string data = "10 20.5 Hello";
    std::istringstream iss(data);
    int i;
    double d;
    std::string s;
    iss >> i >> d >> s;  // i=10, d=20.5, s="Hello"
    
    return 0;
}
```

---

## 18. std::numeric_limits（使用246次）

**说明**：提供数值类型的极限信息，如最大值、最小值、精度等。

**示例**：
```cpp
#include <limits>
#include <iostream>

int main() {
    // 获取整数极限
    int max_int = std::numeric_limits<int>::max();      // 2147483647
    int min_int = std::numeric_limits<int>::min();      // -2147483648
    
    // 获取浮点数极限
    float max_float = std::numeric_limits<float>::max();
    float epsilon = std::numeric_limits<float>::epsilon();  // 最小精度
    float inf = std::numeric_limits<float>::infinity();     // 无穷大
    
    // 检查是否有无穷大
    bool has_inf = std::numeric_limits<float>::has_infinity;
    
    // 用于比较浮点数
    float a = 0.1f + 0.2f;
    float b = 0.3f;
    if (std::abs(a - b) < std::numeric_limits<float>::epsilon()) {
        std::cout << "近似相等" << std::endl;
    }
    
    return 0;
}
```

---

## 19. std::get（使用237次）

**说明**：用于访问tuple、pair、variant、array等类型的元素。

**示例**：
```cpp
#include <tuple>
#include <array>
#include <utility>
#include <variant>

int main() {
    // 访问tuple
    std::tuple<int, std::string, double> person = {25, "Alice", 1.65};
    int age = std::get<0>(person);
    std::string name = std::get<1>(person);
    
    // 通过类型访问（类型唯一时）
    double height = std::get<double>(person);
    
    // 访问array
    std::array<int, 3> arr = {10, 20, 30};
    int second = std::get<1>(arr);  // 20
    
    // 访问pair
    std::pair<int, std::string> p = {1, "test"};
    auto first = std::get<0>(p);
    
    // C++14: std::get<I> 可用于获取variant的值
    std::variant<int, std::string> var = "hello";
    std::string val = std::get<std::string>(var);
    
    return 0;
}
```

---

## 20. std::clamp（使用227次）

**说明**：C++17引入，将值限制在指定范围内。

**示例**：
```cpp
#include <algorithm>

int main() {
    // 基本用法
    int value = 150;
    int clamped = std::clamp(value, 0, 100);  // 返回100
    
    // 颜色分量限制
    int red = 300;
    int green = -50;
    int blue = 128;
    
    red = std::clamp(red, 0, 255);      // 255
    green = std::clamp(green, 0, 255);  // 0
    blue = std::clamp(blue, 0, 255);    // 128
    
    // 浮点数版本
    double x = 2.5;
    double y = std::clamp(x, 0.0, 1.0);  // 1.0
    
    return 0;
}
```

---

## 21. std::make_shared（使用223次）

**说明**：工厂函数，安全高效地创建shared_ptr，一次性分配内存。

**示例**：
```cpp
#include <memory>

class Material {
public:
    std::string name;
    float roughness;
    Material(const std::string& n, float r) 
        : name(n), roughness(r) {}
};

int main() {
    // 推荐使用make_shared
    auto mat = std::make_shared<Material>("metal", 0.3f);
    
    // 更高效：只分配一次内存（对象+控制块）
    // 对比: shared_ptr<Material> mat(new Material("metal", 0.3f));
    // 后者分配两次内存
    
    // 创建数组（C++20起支持）
    // auto arr = std::make_shared<int[]>(100);
    
    return 0;
}
```

---

## 22. std::to_string（使用199次）

**说明**：将数值类型转换为字符串。

**示例**：
```cpp
#include <string>
#include <iostream>

int main() {
    // 各种数值转字符串
    std::string s1 = std::to_string(42);           // "42"
    std::string s2 = std::to_string(3.14159);      // "3.141590"
    std::string s3 = std::to_string(123456789L);   // "123456789"
    
    // 格式化编号
    for (int i = 0; i < 5; ++i) {
        std::string filename = "frame_" + std::to_string(i) + ".png";
        std::cout << filename << std::endl;
    }
    
    return 0;
}
```

---

## 23. std::is_same_v（使用194次）

**说明**：C++17变量模板，编译时检查两个类型是否相同。

**示例**：
```cpp
#include <type_traits>
#include <iostream>

int main() {
    // 检查类型
    static_assert(std::is_same_v<int, int>);           // true
    static_assert(!std::is_same_v<int, float>);        // false
    
    // 在模板中使用
    template<typename T>
    void process(T value) {
        if constexpr (std::is_same_v<T, int>) {
            std::cout << "整数处理" << std::endl;
        } else if constexpr (std::is_same_v<T, std::string>) {
            std::cout << "字符串处理" << std::endl;
        }
    }
    
    // 与decay配合使用
    static_assert(std::is_same_v<std::decay_t<const int&>, int>);
    
    return 0;
}
```

---

## 24. std::lock_guard（使用167次）

**说明**：互斥锁的RAII包装器，构造时加锁，析构时自动解锁。

**示例**：
```cpp
#include <mutex>
#include <thread>
#include <vector>

class Counter {
private:
    int count = 0;
    std::mutex mtx;
    
public:
    void increment() {
        std::lock_guard<std::mutex> lock(mtx);  // 自动加锁
        ++count;  // 临界区
        // 自动解锁
    }
    
    int get() {
        std::lock_guard<std::mutex> lock(mtx);
        return count;
    }
};

int main() {
    Counter counter;
    std::vector<std::thread> threads;
    
    for (int i = 0; i < 10; ++i) {
        threads.emplace_back([&counter]() {
            for (int j = 0; j < 100; ++j) {
                counter.increment();
            }
        });
    }
    
    for (auto& t : threads) t.join();
    std::cout << "Count: " << counter.get() << std::endl;  // 1000
    
    return 0;
}
```

---

## 25. std::forward（使用148次）

**说明**：完美转发，保持参数的值类别（左值/右值）。

**示例**：
```cpp
#include <utility>

class Widget {
public:
    Widget() { std::cout << "默认构造" << std::endl; }
    Widget(const Widget&) { std::cout << "拷贝构造" << std::endl; }
    Widget(Widget&&) { std::cout << "移动构造" << std::endl; }
};

// 通用引用+完美转发
template<typename T, typename Arg>
T create(Arg&& arg) {
    return T(std::forward<Arg>(arg));  // 保持原始值类别
}

int main() {
    Widget w;
    Widget w1 = create<Widget>(w);              // 拷贝构造（w是左值）
    Widget w2 = create<Widget>(Widget());       // 移动构造（临时对象是右值）
    
    return 0;
}
```

---

## 26. std::get_if（使用146次）

**说明**：C++17引入，安全访问variant的指针版本，不抛出异常。

**示例**：
```cpp
#include <variant>
#include <string>
#include <iostream>

using MyVariant = std::variant<int, std::string, double>;

int main() {
    MyVariant var = "Hello";
    
    // 安全获取指针
    if (auto* str = std::get_if<std::string>(&var)) {
        std::cout << "字符串值: " << *str << std::endl;
    } else if (auto* num = std::get_if<int>(&var)) {
        std::cout << "整数值: " << *num << std::endl;
    } else {
        std::cout << "其他类型" << std::endl;
    }
    
    // 获取不存在的类型返回nullptr
    auto* d = std::get_if<double>(&var);  // nullptr
    
    return 0;
}
```

---

## 27. std::scoped_lock（使用138次）

**说明**：C++17引入，可同时锁定多个互斥锁，避免死锁。

**示例**：
```cpp
#include <mutex>
#include <thread>

class BankAccount {
private:
    int balance = 1000;
    std::mutex mtx;
    
public:
    void transfer(BankAccount& to, int amount) {
        // 同时锁定两个账户的互斥锁，避免死锁
        std::scoped_lock lock(mtx, to.mtx);
        
        balance -= amount;
        to.balance += amount;
    }
    
    int getBalance() {
        std::scoped_lock lock(mtx);
        return balance;
    }
};

int main() {
    BankAccount alice, bob;
    
    std::thread t1([&]() { alice.transfer(bob, 100); });
    std::thread t2([&]() { bob.transfer(alice, 50); });
    
    t1.join();
    t2.join();
    
    return 0;
}
```

---

## 28. std::atomic（使用137次）

**说明**：提供原子操作，确保多线程环境下的线程安全。

**示例**：
```cpp
#include <atomic>
#include <thread>
#include <vector>
#include <iostream>

int main() {
    std::atomic<int> counter{0};
    std::atomic<bool> ready{false};
    
    std::vector<std::thread> threads;
    
    // 生产者线程
    threads.emplace_back([&]() {
        for (int i = 0; i < 1000; ++i) {
            counter.fetch_add(1, std::memory_order_relaxed);
        }
        ready.store(true, std::memory_order_release);
    });
    
    // 消费者线程
    threads.emplace_back([&]() {
        while (!ready.load(std::memory_order_acquire)) {
            // 等待ready变为true
        }
        std::cout << "Counter: " << counter.load() << std::endl;
    });
    
    for (auto& t : threads) t.join();
    
    return 0;
}
```

---

## 29. std::function（使用129次）

**说明**：通用多态函数包装器，可存储任何可调用对象。

**示例**：
```cpp
#include <functional>
#include <iostream>

void callback_function(int x) {
    std::cout << "回调: " << x << std::endl;
}

class Functor {
public:
    void operator()(int x) {
        std::cout << "仿函数: " << x << std::endl;
    }
};

int main() {
    // 存储普通函数
    std::function<void(int)> f1 = callback_function;
    
    // 存储lambda
    std::function<int(int, int)> f2 = [](int a, int b) { 
        return a + b; 
    };
    
    // 存储成员函数（需bind）
    Functor functor;
    std::function<void(int)> f3 = std::bind(&Functor::operator(), &functor, std::placeholders::_1);
    
    // 调用
    f1(42);
    std::cout << "和: " << f2(10, 20) << std::endl;
    
    // 检查是否为空
    if (f1) {
        f1(100);
    }
    
    return 0;
}
```

---

## 30. std::sort（使用108次）

**说明**：快速排序算法，平均时间复杂度O(n log n)。

**示例**：
```cpp
#include <algorithm>
#include <vector>
#include <string>

struct Person {
    std::string name;
    int age;
};

int main() {
    // 排序基本类型
    std::vector<int> nums = {3, 1, 4, 1, 5, 9, 2, 6};
    std::sort(nums.begin(), nums.end());  // 升序
    std::sort(nums.begin(), nums.end(), std::greater<int>());  // 降序
    
    // 排序自定义类型
    std::vector<Person> people = {
        {"Alice", 30}, {"Bob", 25}, {"Charlie", 35}
    };
    
    // 按年龄排序
    std::sort(people.begin(), people.end(), 
        [](const Person& a, const Person& b) {
            return a.age < b.age;
        });
    
    // 部分排序（保持相等元素相对顺序）
    std::stable_sort(people.begin(), people.end(),
        [](const Person& a, const Person& b) {
            return a.name < b.name;
        });
    
    return 0;
}
```

---

## 31. std::string_view（使用101次）

**说明**：C++17引入的字符串视图，只读引用，零拷贝。

**示例**：
```cpp
#include <string_view>
#include <string>
#include <iostream>

// 高效传递字符串，无需拷贝
void printString(std::string_view sv) {
    std::cout << "内容: " << sv << ", 长度: " << sv.length() << std::endl;
}

int main() {
    std::string str = "Hello World";
    const char* cstr = "C风格字符串";
    
    // 从不同来源创建
    printString(str);           // 从std::string
    printString(cstr);          // 从C字符串
    printString("字面量");       // 从字符串字面量
    printString(str.substr(0, 5));  // 子串，无拷贝！
    
    // 注意：string_view不拥有内存，使用时需确保原字符串有效
    std::string_view sv;
    {
        std::string temp = "temporary";
        sv = temp;  // 危险！temp将被销毁
    }
    // sv现在指向已释放的内存！
    
    return 0;
}
```

---

## 32. std::abs（使用98次）

**说明**：计算绝对值，支持整数和浮点数。

**示例**：
```cpp
#include <cstdlib>
#include <cmath>
#include <iostream>

int main() {
    // 整数绝对值
    int i = -42;
    int abs_i = std::abs(i);  // 42
    
    // 浮点数绝对值
    double d = -3.14;
    double abs_d = std::abs(d);  // 3.14
    
    // 长整型
    long l = -1000000L;
    long abs_l = std::abs(l);
    
    // 实际应用：计算距离
    int x1 = 10, y1 = 20;
    int x2 = 30, y2 = 50;
    int dx = std::abs(x2 - x1);
    int dy = std::abs(y2 - y1);
    
    std::cout << "曼哈顿距离: " << dx + dy << std::endl;
    
    return 0;
}
```

---

## 33. std::cerr（使用84次）

**说明**：标准错误输出流，通常不缓冲，立即输出。

**示例**：
```cpp
#include <iostream>
#include <fstream>

int main() {
    // 错误信息输出到stderr
    std::ifstream file("data.txt");
    if (!file.is_open()) {
        std::cerr << "错误: 无法打开文件 data.txt" << std::endl;
        return 1;
    }
    
    // 普通信息输出到stdout
    std::cout << "处理文件中..." << std::endl;
    
    // 警告信息也可以输出到stderr
    int lines = 0;
    std::string line;
    while (std::getline(file, line)) {
        if (line.empty()) {
            std::cerr << "警告: 发现空行，行号 " << lines + 1 << std::endl;
        }
        ++lines;
    }
    
    std::cout << "总共处理了 " << lines << " 行" << std::endl;
    
    return 0;
}
```

---

## 34. std::string::npos（使用81次）

**说明**：表示"未找到"或"无效位置"的特殊常量值。

**示例**：
```cpp
#include <string>
#include <iostream>

int main() {
    std::string text = "Hello, World!";
    
    // 查找子串
    size_t pos = text.find("World");
    if (pos != std::string::npos) {
        std::cout << "找到位置: " << pos << std::endl;
    }
    
    // 查找不存在的子串
    pos = text.find("xyz");
    if (pos == std::string::npos) {
        std::cout << "未找到子串" << std::endl;
    }
    
    // 其他返回npos的操作
    std::string str = "test";
    if (str.find('z') == std::string::npos) {
        std::cout << "字符'z'不存在" << std::endl;
    }
    
    // npos的值实际上是size_t的最大值
    std::cout << "npos = " << std::string::npos << std::endl;
    
    return 0;
}
```

---

## 35. std::memory_order_relaxed（使用77次）

**说明**：最宽松的原子内存序，仅保证原子性，不保证顺序。

**示例**：
```cpp
#include <atomic>
#include <thread>
#include <iostream>

int main() {
    std::atomic<int> counter{0};
    
    // 多线程增加计数器，无需同步顺序
    std::thread t1([&]() {
        for (int i = 0; i < 1000000; ++i) {
            counter.fetch_add(1, std::memory_order_relaxed);
        }
    });
    
    std::thread t2([&]() {
        for (int i = 0; i < 1000000; ++i) {
            counter.fetch_add(1, std::memory_order_relaxed);
        }
    });
    
    t1.join();
    t2.join();
    
    std::cout << "最终计数: " << counter.load() << std::endl;  // 2000000
    
    // 使用场景：单纯计数器，无需观察其他变量的值
    // 注意：relaxed不保证其他变量的可见性！
    
    return 0;
}
```

---

## 36. std::complex（使用76次）

**说明**：复数类型，支持复数运算，常用于信号处理、数学计算。

**示例**：
```cpp
#include <complex>
#include <iostream>

int main() {
    // 创建复数
    std::complex<double> c1(3.0, 4.0);  // 3 + 4i
    std::complex<double> c2(1.0, 2.0);  // 1 + 2i
    
    // 基本运算
    auto sum = c1 + c2;     // 4 + 6i
    auto diff = c1 - c2;    // 2 + 2i
    auto prod = c1 * c2;    // (3*1-4*2) + (3*2+4*1)i = -5 + 10i
    auto quot = c1 / c2;    // 复数除法
    
    // 获取实部和虚部
    double real = c1.real();  // 3.0
    double imag = c1.imag();  // 4.0
    
    // 计算模和辐角
    double magnitude = std::abs(c1);    // 5.0 (sqrt(3^2 + 4^2))
    double phase = std::arg(c1);        // 弧度制角度
    
    // 共轭复数
    auto conj = std::conj(c1);  // 3 - 4i
    
    std::cout << "c1 = " << c1 << ", |c1| = " << magnitude << std::endl;
    
    return 0;
}
```

---

## 37. std::variant（使用75次）

**说明**：C++17引入的类型安全联合体，可存储多种类型中的一种。

**示例**：
```cpp
#include <variant>
#include <string>
#include <iostream>

using Value = std::variant<int, double, std::string>;

void printValue(const Value& v) {
    // 使用visit访问variant
    std::visit([](const auto& val) {
        std::cout << val << std::endl;
    }, v);
}

int main() {
    // 存储不同类型
    Value v1 = 42;
    Value v2 = 3.14;
    Value v3 = std::string("Hello");
    
    // 类型检查
    if (std::holds_alternative<int>(v1)) {
        std::cout << "v1是整数" << std::endl;
    }
    
    // 获取值
    int i = std::get<int>(v1);
    
    // 安全获取（返回指针）
    if (auto* str = std::get_if<std::string>(&v3)) {
        std::cout << "字符串: " << *str << std::endl;
    }
    
    // 使用visit统一处理
    printValue(v1);
    printValue(v2);
    printValue(v3);
    
    return 0;
}
```

---

## 38. std::any_of（使用68次）

**说明**：检查范围内是否至少有一个元素满足条件。

**示例**：
```cpp
#include <algorithm>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> nums = {1, 3, 5, 7, 8, 9};
    
    // 检查是否有偶数
    bool has_even = std::any_of(nums.begin(), nums.end(),
        [](int n) { return n % 2 == 0; });
    
    if (has_even) {
        std::cout << "存在偶数" << std::endl;
    }
    
    // 检查字符串数组
    std::vector<std::string> files = {"data.txt", "image.png", "script.py"};
    bool has_image = std::any_of(files.begin(), files.end(),
        [](const std::string& f) { 
            return f.find(".png") != std::string::npos ||
                   f.find(".jpg") != std::string::npos; 
        });
    
    std::cout << "包含图片: " << (has_image ? "是" : "否") << std::endl;
    
    return 0;
}
```

---

## 39. std::byte（使用61次）

**说明**：C++17引入的字节类型，用于表示原始字节数据，类型安全。

**示例**：
```cpp
#include <cstddef>
#include <iostream>
#include <bitset>

int main() {
    // 创建byte
    std::byte b1{0x0F};  // 15
    std::byte b2{0xF0};  // 240
    
    // 位运算
    std::byte b3 = b1 | b2;   // 按位或: 0xFF
    std::byte b4 = b1 & b2;   // 按位与: 0x00
    std::byte b5 = b1 ^ b2;   // 按位异或: 0xFF
    std::byte b6 = ~b1;       // 按位非: 0xF0
    
    // 位移
    std::byte b7 = b1 << 2;   // 左移: 0x3C
    
    // 转换为整数（必须显式转换）
    int val = std::to_integer<int>(b1);
    std::cout << "b1的值: " << val << std::endl;
    
    // 处理二进制数据
    std::byte buffer[1024];
    // 读取文件到buffer...
    
    return 0;
}
```

---

## 40. std::decay_t（使用55次）

**说明**：移除类型的引用和cv限定符，数组退化为指针，用于类型萃取。

**示例**：
```cpp
#include <type_traits>
#include <iostream>

int main() {
    // 移除引用
    static_assert(std::is_same_v<std::decay_t<int&>, int>);
    static_assert(std::is_same_v<std::decay_t<const int&>, int>);
    
    // 移除cv限定符
    static_assert(std::is_same_v<std::decay_t<const int>, int>);
    static_assert(std::is_same_v<std::decay_t<volatile int>, int>);
    
    // 数组退化为指针
    static_assert(std::is_same_v<std::decay_t<int[5]>, int*>);
    static_assert(std::is_same_v<std::decay_t<int[]>, int*>);
    
    // 函数退化为指针
    static_assert(std::is_same_v<std::decay_t<void()>, void(*)()>);
    
    // 实际应用：模板中统一类型
    template<typename T>
    using CleanType = std::decay_t<T>;
    
    template<typename T>
    void store(T&& value) {
        CleanType<T> storage = std::forward<T>(value);
        // ...
    }
    
    return 0;
}
```

---

## 41. std::sqrt（使用52次）

**说明**：计算平方根，支持多种浮点类型。

**示例**：
```cpp
#include <cmath>
#include <iostream>

struct Vector2 {
    float x, y;
    
    float length() const {
        return std::sqrt(x * x + y * y);
    }
    
    Vector2 normalized() const {
        float len = length();
        if (len > 0) {
            return {x / len, y / len};
        }
        return {0, 0};
    }
};

int main() {
    // 基本用法
    double d = std::sqrt(16.0);  // 4.0
    float f = std::sqrt(2.0f);   // 约1.414
    
    // 向量长度计算
    Vector2 vec{3.0f, 4.0f};
    float len = vec.length();  // 5.0
    
    // 距离计算
    Vector2 a{1.0f, 2.0f};
    Vector2 b{4.0f, 6.0f};
    float dist = std::sqrt(
        std::pow(b.x - a.x, 2) + std::pow(b.y - a.y, 2)
    );  // 5.0
    
    std::cout << "向量长度: " << len << std::endl;
    
    return 0;
}
```

---

## 42. std::holds_alternative（使用50次）

**说明**：检查variant当前是否持有特定类型。

**示例**：
```cpp
#include <variant>
#include <string>
#include <iostream>

using ConfigValue = std::variant<int, double, bool, std::string>;

void printConfig(const std::string& key, const ConfigValue& value) {
    std::cout << key << " = ";
    
    if (std::holds_alternative<int>(value)) {
        std::cout << std::get<int>(value) << " (int)";
    } else if (std::holds_alternative<double>(value)) {
        std::cout << std::get<double>(value) << " (double)";
    } else if (std::holds_alternative<bool>(value)) {
        std::cout << (std::get<bool>(value) ? "true" : "false") << " (bool)";
    } else if (std::holds_alternative<std::string>(value)) {
        std::cout << std::get<std::string>(value) << " (string)";
    }
    
    std::cout << std::endl;
}

int main() {
    ConfigValue width = 1920;
    ConfigValue height = 1080.0;
    ConfigValue fullscreen = true;
    ConfigValue title = std::string("MyApp");
    
    printConfig("width", width);
    printConfig("height", height);
    printConfig("fullscreen", fullscreen);
    printConfig("title", title);
    
    return 0;
}
```

---

## 43. std::destroy_at（使用50次）

**说明**：C++17引入，在指定地址调用析构函数，用于手动内存管理。

**示例**：
```cpp
#include <memory>
#include <iostream>

class Resource {
public:
    int id;
    Resource(int i) : id(i) {
        std::cout << "Resource " << id << " 构造" << std::endl;
    }
    ~Resource() {
        std::cout << "Resource " << id << " 析构" << std::endl;
    }
};

int main() {
    // 分配原始内存
    void* memory = std::malloc(sizeof(Resource));
    
    // 在内存上构造对象（placement new）
    Resource* res = new (memory) Resource(42);
    
    // 使用对象
    std::cout << "ID: " << res->id << std::endl;
    
    // 显式调用析构函数
    std::destroy_at(res);
    
    // 释放内存（不调用析构函数）
    std::free(memory);
    
    // 另一个场景：数组销毁
    Resource* arr = static_cast<Resource*>(
        std::malloc(sizeof(Resource) * 3)
    );
    
    // 构造多个对象
    for (int i = 0; i < 3; ++i) {
        new (&arr[i]) Resource(i);
    }
    
    // 销毁所有对象
    for (int i = 0; i < 3; ++i) {
        std::destroy_at(&arr[i]);
    }
    
    std::free(arr);
    
    return 0;
}
```

---

## 44. std::unique_lock（使用42次）

**说明**：灵活的互斥锁包装器，支持延迟锁定、条件变量等。

**示例**：
```cpp
#include <mutex>
#include <condition_variable>
#include <queue>
#include <thread>

template<typename T>
class ThreadSafeQueue {
private:
    std::queue<T> queue_;
    std::mutex mtx_;
    std::condition_variable cv_;
    
public:
    void push(T value) {
        {
            std::unique_lock<std::mutex> lock(mtx_);
            queue_.push(std::move(value));
        }
        cv_.notify_one();
    }
    
    T pop() {
        std::unique_lock<std::mutex> lock(mtx_);
        
        // 等待直到队列非空
        cv_.wait(lock, [this] { return !queue_.empty(); });
        
        T value = std::move(queue_.front());
        queue_.pop();
        return value;
    }
    
    bool try_pop(T& value, std::chrono::milliseconds timeout) {
        std::unique_lock<std::mutex> lock(mtx_);
        
        // 带超时的等待
        if (cv_.wait_for(lock, timeout, 
            [this] { return !queue_.empty(); })) {
            value = std::move(queue_.front());
            queue_.pop();
            return true;
        }
        return false;
    }
};

int main() {
    ThreadSafeQueue<int> queue;
    
    std::thread producer([&]() {
        for (int i = 0; i < 10; ++i) {
            queue.push(i);
        }
    });
    
    std::thread consumer([&]() {
        for (int i = 0; i < 10; ++i) {
            int val = queue.pop();
            std::cout << "消费: " << val << std::endl;
        }
    });
    
    producer.join();
    consumer.join();
    
    return 0;
}
```

---

## 45. std::reference_wrapper（使用38次）

**说明**：可复制引用的包装器，可在容器中存储引用。

**示例**：
```cpp
#include <functional>
#include <vector>
#include <iostream>

int main() {
    int a = 10, b = 20, c = 30;
    
    // 无法直接存储引用
    // std::vector<int&> refs;  // 编译错误！
    
    // 使用reference_wrapper
    std::vector<std::reference_wrapper<int>> refs;
    refs.push_back(std::ref(a));
    refs.push_back(std::ref(b));
    refs.push_back(std::ref(c));
    
    // 修改原变量
    for (auto& ref : refs) {
        ref.get() *= 2;  // 通过get()访问
    }
    
    std::cout << "a=" << a << ", b=" << b << ", c=" << c << std::endl;
    // 输出: a=20, b=40, c=60
    
    // 与std::bind配合使用
    void process(int& x, int& y);
    auto bound = std::bind(process, std::ref(a), std::ref(b));
    // 调用bound()时，会修改a和b的值
    
    // 创建const引用包装
    std::reference_wrapper<const int> cref = std::cref(a);
    
    return 0;
}
```

---

## 46. std::all_of（使用34次）

**说明**：检查范围内所有元素是否都满足条件。

**示例**：
```cpp
#include <algorithm>
#include <vector>
#include <string>
#include <iostream>

int main() {
    // 检查所有元素是否为正数
    std::vector<int> nums = {1, 2, 3, 4, 5};
    bool all_positive = std::all_of(nums.begin(), nums.end(),
        [](int n) { return n > 0; });
    
    std::cout << "全部为正: " << (all_positive ? "是" : "否") << std::endl;
    
    // 检查字符串是否全为数字
    std::string str = "12345";
    bool all_digits = std::all_of(str.begin(), str.end(),
        [](char c) { return std::isdigit(c); });
    
    std::cout << "全是数字: " << (all_digits ? "是" : "否") << std::endl;
    
    // 检查数组是否已排序
    std::vector<int> sorted = {1, 2, 3, 4, 5};
    bool is_sorted = std::all_of(sorted.begin(), sorted.end() - 1,
        [](int a, int b) { return a <= b; });
    
    return 0;
}
```

---

## 47. std::mutex（使用33次）

**说明**：基本互斥锁，用于保护共享资源的访问。

**示例**：
```cpp
#include <mutex>
#include <thread>
#include <vector>
#include <iostream>

class ThreadSafeCounter {
private:
    int count_ = 0;
    std::mutex mtx_;
    
public:
    void increment() {
        mtx_.lock();
        ++count_;
        mtx_.unlock();
    }
    
    void decrement() {
        std::lock_guard<std::mutex> lock(mtx_);  // 更安全的RAII方式
        --count_;
    }
    
    int get() {
        std::lock_guard<std::mutex> lock(mtx_);
        return count_;
    }
    
    // 尝试锁定
    bool try_increment() {
        if (mtx_.try_lock()) {
            ++count_;
            mtx_.unlock();
            return true;
        }
        return false;
    }
};

int main() {
    ThreadSafeCounter counter;
    std::vector<std::thread> threads;
    
    for (int i = 0; i < 5; ++i) {
        threads.emplace_back([&counter]() {
            for (int j = 0; j < 1000; ++j) {
                counter.increment();
            }
        });
    }
    
    for (auto& t : threads) {
        t.join();
    }
    
    std::cout << "最终计数: " << counter.get() << std::endl;  // 5000
    
    return 0;
}
```

---

## 48. std::is_same（使用33次）

**说明**：类型特征，编译时检查两个类型是否相同。

**示例**：
```cpp
#include <type_traits>
#include <iostream>

// 模板类型检查
template<typename T>
void process(T value) {
    if constexpr (std::is_same<T, int>::value) {
        std::cout << "处理整数: " << value << std::endl;
    } else if constexpr (std::is_same<T, double>::value) {
        std::cout << "处理浮点数: " << value << std::endl;
    } else {
        std::cout << "处理其他类型" << std::endl;
    }
}

// 类型萃取
struct Vector3 {
    float x, y, z;
};

template<typename T>
struct is_vector3 : std::is_same<T, Vector3> {};

template<typename T>
constexpr bool is_vector3_v = is_vector3<T>::value;

int main() {
    // 基本类型检查
    static_assert(std::is_same<int, int>::value, "相同类型");
    static_assert(!std::is_same<int, float>::value, "不同类型");
    
    // 使用::value成员
    bool same = std::is_same<int, int>::value;  // true
    
    // C++17推荐使用is_same_v
    // bool same_v = std::is_same_v<int, int>;
    
    // 实际应用
    process(42);       // 处理整数
    process(3.14);     // 处理浮点数
    process("hello");  // 处理其他类型
    
    // 检查是否是Vector3
    static_assert(is_vector3_v<Vector3>);
    static_assert(!is_vector3_v<int>);
    
    return 0;
}
```

---

## 49. std::visit（使用32次）

**说明**：C++17引入，用于访问variant的值，替代复杂的if-else链。

**示例**：
```cpp
#include <variant>
#include <string>
#include <iostream>
#include <vector>

// 定义事件类型
struct MouseClick { int x, y; };
struct KeyPress { char key; };
struct Resize { int width, height; };

using Event = std::variant<MouseClick, KeyPress, Resize>;

// 处理函数对象
struct EventHandler {
    void operator()(const MouseClick& e) {
        std::cout << "鼠标点击: (" << e.x << ", " << e.y << ")" << std::endl;
    }
    
    void operator()(const KeyPress& e) {
        std::cout << "按键: " << e.key << std::endl;
    }
    
    void operator()(const Resize& e) {
        std::cout << "窗口调整: " << e.width << "x" << e.height << std::endl;
    }
};

// 使用lambda的重载访问
auto handleEvent = [](const auto& e) {
    using T = std::decay_t<decltype(e)>;
    if constexpr (std::is_same_v<T, MouseClick>) {
        std::cout << "处理鼠标事件" << std::endl;
    } else if constexpr (std::is_same_v<T, KeyPress>) {
        std::cout << "处理键盘事件" << std::endl;
    } else if constexpr (std::is_same_v<T, Resize>) {
        std::cout << "处理尺寸调整" << std::endl;
    }
};

int main() {
    std::vector<Event> events = {
        MouseClick{100, 200},
        KeyPress{'A'},
        Resize{1920, 1080}
    };
    
    // 使用函数对象处理
    for (const auto& event : events) {
        std::visit(EventHandler{}, event);
    }
    
    std::cout << "---" << std::endl;
    
    // 使用lambda处理
    for (const auto& event : events) {
        std::visit(handleEvent, event);
    }
    
    std::cout << "---" << std::endl;
    
    // 返回值的visit
    auto getTypeName = [](const auto& e) -> std::string {
        using T = std::decay_t<decltype(e)>;
        if constexpr (std::is_same_v<T, MouseClick>) return "MouseClick";
        if constexpr (std::is_same_v<T, KeyPress>) return "KeyPress";
        if constexpr (std::is_same_v<T, Resize>) return "Resize";
        return "Unknown";
    };
    
    for (const auto& event : events) {
        std::cout << "类型: " << std::visit(getTypeName, event) << std::endl;
    }
    
    return 0;
}
```

---

## 总结

这49个组件覆盖了Blender代码库的以下核心领域：

| 领域 | 主要组件 |
|:---|:---|
| **内存管理** | unique_ptr, shared_ptr, make_unique, make_shared, destroy_at |
| **字符串处理** | string, string_view, to_string, stringstream |
| **类型安全** | optional, nullopt, variant, visit, get, get_if |
| **并发编程** | mutex, lock_guard, scoped_lock, unique_lock, atomic |
| **模板元编程** | is_same_v, decay_t, is_same |
| **数值计算** | max, min, clamp, abs, sqrt, complex, numeric_limits |
| **算法** | sort, any_of, all_of, swap |
| **IO操作** | cout, cerr, endl, ostream |
| **工具函数** | move, forward, pair, tuple |

这些组件反映了现代C++（C++11/14/17）在大型项目中的最佳实践，包括RAII内存管理、类型安全、并发支持和性能优化。

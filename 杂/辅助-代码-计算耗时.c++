#include <chrono>
#include <iostream>

int main()
{
  system("chcp 65001");

  namespace c = std::chrono;
  auto start = c::steady_clock::now();

  auto duration = c::duration<double, std::milli>(c::steady_clock::now() - start);
  std::cout << "耗时 1: " << duration.count() << " ms \n";
  start = c::steady_clock::now();

  duration = c::duration<double, std::milli>(c::steady_clock::now() - start);
  std::cout << "耗时 2: " << duration.count() << " ms \n";

  duration = c::duration<double, std::milli>(c::steady_clock::now() - start);
  std::cout << "总耗时: " << duration.count() << " ms \n\n";

  // =====================================================================================================================
  // clang-format off
  // time_since_epoch: 从时钟纪元(1970年)到现在的距离
  std::chrono::steady_clock::duration start1 = std::chrono::steady_clock::now().time_since_epoch(); // 整数纳秒
  std::chrono::duration<double> start2 = std::chrono::steady_clock::now().time_since_epoch(); // 小数秒

  auto end = std::chrono::steady_clock::now().time_since_epoch();
  std::cout << "1: " << (end - start1).count() << " ns \n";  // 整数纳秒

  std::chrono::steady_clock::duration end2 = std::chrono::steady_clock::now().time_since_epoch();
  std::cout << "2: " << (end2 - start1).count() << " ns \n";  // 整数纳秒

  std::chrono::duration<double> end3 = std::chrono::steady_clock::now().time_since_epoch();
  std::cout << "3: " << (end3 - start1).count() << " ns \n";  //  小数纳秒
  std::cout << "3: " << (end3 - start2).count() << " s \n";   //  小数秒

  std::chrono::steady_clock::time_point start3 = std::chrono::high_resolution_clock::now();

  std::chrono::steady_clock::time_point end4 = std::chrono::high_resolution_clock::now();
  std::cout << "4: " << std::chrono::duration<double, std::milli>(end4 - start3).count()
            << " ms \n";  // 小数毫秒

  auto end5 = std::chrono::steady_clock::now();
  std::cout << "5: " << (end5 - start3).count() << " ns \n\n";  // 整数纳秒
  // clang-format on

  system("pause");
  return 0;
}

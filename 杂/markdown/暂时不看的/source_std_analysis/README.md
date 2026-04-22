# Blender 源码 std:: 使用分析报告

## 概览

- **分析时间**: $(date)
- **分析路径**: `source/blender/`
- **总匹配数**: 23,012 处
- **分析命令**: `grep -rn "std::" source/blender/`

## 目录结构

```
std_analysis/
├── README.md                    # 本报告
├── all_std_usages_raw.txt       # 原始匹配数据 (23,012 行)
├── std_components_freq.txt      # 按 std:: 组件统计
├── by_directory.txt             # 按目录统计
├── by_file.txt                  # 按文件统计
├── std_components_freq.csv      # 组件统计 CSV
├── by_directory.csv             # 目录统计 CSV
└── by_file.csv                  # 文件统计 CSV
```

## 使用方法

查看各统计文件了解详细分布：

```bash
# 查看最常用的 std:: 组件
cat std_components_freq.txt

# 查看各目录使用情况
cat by_directory.txt

# 查看使用最多的文件
cat by_file.txt
```

## 数据文件说明

| 文件 | 内容 | 行数 |
|------|------|------|
| `all_std_usages_raw.txt` | 原始匹配: 文件名:行号:代码 | 23,012 |
| `std_components_freq.txt` | 组件使用频率 | - |
| `by_directory.txt` | 目录使用统计 | - |
| `by_file.txt` | 文件使用统计 | - |

---

*由 OpenCode 自动生成*

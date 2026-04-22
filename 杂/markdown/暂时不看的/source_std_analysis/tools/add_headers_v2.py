#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加头文件信息到 std:: 组件统计 - 更新版
添加更多头文件映射
"""

import csv
import re
from collections import defaultdict

# C++ 标准库头文件映射表 - 扩展版
HEADER_MAP = {
    # ... (保留之前的所有映射)
}

def get_header(component_name):
    """获取组件对应的头文件 - 增强版"""
    # 移除 std:: 前缀
    if component_name.startswith('std::'):
        name = component_name[5:]
    else:
        name = component_name
    
    # 处理带 :: 的嵌套情况
    if '::' in name:
        # 获取第一部分
        base_name = name.split('::')[0]
        
        # 特殊情况处理
        if base_name == 'chrono':
            return '<chrono>'
        if base_name == 'ios':
            return '<ios>'
        if base_name == 'ios_base':
            return '<ios>'
        if base_name == 'filesystem':
            return '<filesystem>'
        if base_name == 'pmr':
            return '<memory_resource>'
        if base_name == 'this_thread':
            return '<thread>'
        if base_name == 'placeholders':
            return '<functional>'
        if base_name == 'regex_constants':
            return '<regex>'
        
        # 查找基础名称
        if base_name in HEADER_MAP:
            return HEADER_MAP[base_name]
        
        # 默认返回基础名称的头文件
        return f'<{base_name}>'
    
    # 查找完整名称
    return HEADER_MAP.get(name, '<unknown>')

def main():
    # 读取原始CSV
    components = []
    with open('E:/blender-git/blender/std_analysis/std_components_freq.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # 跳过标题行
        for row in reader:
            if len(row) >= 2:
                component = row[0].strip('"')
                count = int(row[1])
                components.append((component, count))
    
    print(f"读取到 {len(components)} 个组件")
    
    # 为每个组件添加头文件信息
    components_with_header = []
    header_to_components = defaultdict(list)
    
    for component, count in components:
        header = get_header(component)
        components_with_header.append((component, count, header))
        header_to_components[header].append((component, count))
    
    # 保存带头文件的CSV
    with open('E:/blender-git/blender/std_analysis/std_components_with_header.csv', 'w', encoding='utf-8') as f:
        f.write('Component,Count,Header\n')
        for component, count, header in components_with_header:
            f.write(f'"{component}",{count},{header}\n')
    
    print(f"已保存: std_components_with_header.csv")
    
    # 按头文件汇总
    header_summary = {}
    for header, comp_list in header_to_components.items():
        total_count = sum(count for _, count in comp_list)
        component_count = len(comp_list)
        header_summary[header] = {
            'total_count': total_count,
            'component_count': component_count,
            'components': comp_list
        }
    
    # 按使用次数排序
    sorted_headers = sorted(header_summary.items(), key=lambda x: x[1]['total_count'], reverse=True)
    
    # 保存头文件汇总CSV
    with open('E:/blender-git/blender/std_analysis/headers_summary.csv', 'w', encoding='utf-8') as f:
        f.write('Header,TotalUsage,ComponentCount\n')
        for header, info in sorted_headers:
            f.write(f'{header},{info["total_count"]},{info["component_count"]}\n')
    
    print(f"已保存: headers_summary.csv")
    
    # 保存详细映射
    with open('E:/blender-git/blender/std_analysis/headers_detail.txt', 'w', encoding='utf-8') as f:
        f.write("# Blender std:: 头文件使用详情\n\n")
        f.write(f"总组件数: {len(components)}\n")
        f.write(f"使用头文件数: {len(sorted_headers)}\n\n")
        
        f.write("## 头文件汇总 (按使用次数排序)\n\n")
        f.write("| 头文件 | 总使用次数 | 组件数 |\n")
        f.write("|--------|-----------|--------|\n")
        for header, info in sorted_headers[:50]:
            f.write(f"| {header} | {info['total_count']} | {info['component_count']} |\n")
        
        f.write("\n## 头文件详细内容\n")
        for header, info in sorted_headers:
            f.write(f"\n### {header} ({info['total_count']} 次)\n\n")
            f.write("| 组件 | 使用次数 |\n")
            f.write("|------|----------|\n")
            # 按使用次数排序
            sorted_comps = sorted(info['components'], key=lambda x: x[1], reverse=True)
            for comp, count in sorted_comps:
                f.write(f"| {comp} | {count} |\n")
    
    print(f"已保存: headers_detail.txt")
    
    # 显示统计摘要
    print(f"\n=== 统计摘要 ===")
    print(f"总组件数: {len(components)}")
    print(f"使用头文件数: {len(sorted_headers)}")
    print(f"\nTop 20 头文件:")
    for i, (header, info) in enumerate(sorted_headers[:20], 1):
        print(f"  {i:2d}. {header}: {info['total_count']} 次 ({info['component_count']} 个组件)")
    
    # 统计未知头文件
    unknown_components = [(comp, count) for comp, count in header_to_components.get('<unknown>', [])]
    if unknown_components:
        print(f"\n未知头文件组件数: {len(unknown_components)}")
        for comp, count in sorted(unknown_components, key=lambda x: x[1], reverse=True)[:20]:
            print(f"  - {comp}: {count}")

if __name__ == '__main__':
    main()

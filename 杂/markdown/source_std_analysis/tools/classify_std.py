#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能分类 std:: 组件 - 改进版
将 std::vector::iterator、std::vector::push_back 等归为 std::vector
"""

import re
from collections import defaultdict

def get_parent_component(full_name):
    """获取父级组件名称"""
    # 移除 std:: 前缀
    if full_name.startswith('std::'):
        name = full_name[5:]
    else:
        name = full_name
    
    # ========== 第一层分类 ==========
    # 本身就是顶层组件的
    top_level_components = {
        'string', 'optional', 'nullopt', 'move', 'unique_ptr', 'shared_ptr', 'weak_ptr',
        'array', 'vector', 'deque', 'list', 'forward_list',
        'set', 'multiset', 'map', 'multimap',
        'unordered_set', 'unordered_multiset', 'unordered_map', 'unordered_multimap',
        'queue', 'priority_queue', 'stack',
        'string_view', 'variant', 'any', 'function', 'tuple', 'pair',
        'ostream', 'istream', 'iostream', 'stringstream', 'istringstream', 'ostringstream',
        'cout', 'cerr', 'clog', 'cin', 'wcin', 'wcout', 'wcerr', 'wclog',
        'ifstream', 'ofstream', 'fstream', 'wifstream', 'wofstream', 'wfstream',
        'endl', 'ends', 'flush', 'ws', 'boolalpha', 'noboolalpha',
        'mutex', 'recursive_mutex', 'timed_mutex', 'recursive_timed_mutex',
        'lock_guard', 'unique_lock', 'scoped_lock', 'shared_lock',
        'condition_variable', 'condition_variable_any',
        'thread', 'jthread',
        'future', 'promise', 'packaged_task',
        'atomic', 'atomic_flag',
        'memory_order_relaxed', 'memory_order_consume', 'memory_order_acquire',
        'memory_order_release', 'memory_order_acq_rel', 'memory_order_seq_cst',
        'byte', 'size_t', 'ptrdiff_t', 'max_align_t', 'nullptr_t', 'nullptr',
        'initializer_list', 'source_location',
        'complex', 'valarray', 'slice', 'gslice', 'slice_array',
        'regex', 'smatch', 'cmatch', 'wsmatch', 'wcmatch',
        'error_code', 'error_condition', 'error_category', 'system_error',
        'runtime_error', 'logic_error', 'exception', 'bad_alloc', 'bad_cast',
        'bad_typeid', 'bad_exception', 'bad_optional_access', 'bad_variant_access',
        'bad_any_cast', 'bad_function_call', 'bad_weak_ptr',
        'invalid_argument', 'domain_error', 'length_error', 'out_of_range',
        'range_error', 'overflow_error', 'underflow_error',
        'locale', 'ctype', 'codecvt', 'collate', 'messages', 'moneypunct',
        'money_get', 'money_put', 'numpunct', 'num_get', 'num_put', 'time_get',
        'time_put', 'time_get_byname', 'time_put_byname',
        'random_device', 'mt19937', 'mt19937_64', 'minstd_rand', 'minstd_rand0',
        'uniform_int_distribution', 'uniform_real_distribution',
        'normal_distribution', 'bernoulli_distribution', 'binomial_distribution',
        'geometric_distribution', 'exponential_distribution', 'weibull_distribution',
        'gamma_distribution', 'lognormal_distribution', 'chi_squared_distribution',
        'cauchy_distribution', 'fisher_f_distribution', 'student_t_distribution',
        'discrete_distribution', 'piecewise_constant_distribution', 'piecewise_linear_distribution',
        'seed_seq', 'linear_congruential_engine', 'mersenne_twister_engine',
        'subtract_with_carry_engine', 'discard_block_engine', 'independent_bits_engine',
        'shuffle_order_engine',
        'filesystem::path', 'filesystem::directory_entry', 'filesystem::directory_iterator',
        'filesystem::recursive_directory_iterator', 'filesystem::file_status',
        'filesystem::space_info', 'filesystem::file_type', 'filesystem::perms',
        'filesystem::perm_options', 'filesystem::copy_options', 'filesystem::directory_options',
    }
    
    if name in top_level_components:
        return f'std::{name}'
    
    # ========== 第二层：双冒号分隔 ==========
    if '::' in name:
        parts = name.split('::')
        parent = parts[0]
        
        # ========== chrono 时间库 ==========
        if parent == 'chrono':
            if len(parts) >= 2:
                chrono_child = parts[1]
                # 时间段类型
                duration_types = ['seconds', 'milliseconds', 'microseconds', 'nanoseconds', 
                                 'hours', 'minutes', 'days', 'weeks', 'years', 'months']
                if chrono_child in duration_types:
                    return 'std::chrono::duration'
                # 时钟类型
                clock_types = ['system_clock', 'steady_clock', 'high_resolution_clock', 'file_clock',
                              'utc_clock', 'tai_clock', 'gps_clock']
                if chrono_child in clock_types:
                    return 'std::chrono::clock'
                # 时间点
                if chrono_child == 'time_point':
                    return 'std::chrono::time_point'
                # duration 本身
                if chrono_child == 'duration':
                    return 'std::chrono::duration'
                # 其他 chrono 组件
                return f'std::chrono::{chrono_child}'
            return 'std::chrono'
        
        # ========== atomic 原子操作 ==========
        if parent == 'atomic':
            return 'std::atomic'
        
        # ========== memory_order ==========
        if parent == 'memory_order':
            return 'std::memory_order'
        
        # ========== memory ==========
        if parent == 'memory':
            return 'std::memory'
        
        # ========== ios/io manipulators ==========
        if parent in ['ios', 'ios_base']:
            return 'std::ios'
        
        # ========== errc 错误码 ==========
        if parent == 'errc':
            return 'std::errc'
        
        # ========== compare 比较 ==========
        if parent == 'compare':
            return 'std::compare'
        
        # ========== limits ==========
        if parent == 'numeric_limits':
            return 'std::numeric_limits'
        
        # ========== ratio ==========
        if parent == 'ratio':
            return 'std::ratio'
        
        # ========== filesystem ==========
        if parent == 'filesystem':
            return 'std::filesystem'
        
        # ========== pmr 多态内存资源 ==========
        if parent == 'pmr':
            return 'std::pmr'
        
        # ========== placeholders ==========
        if parent == 'placeholders':
            return 'std::placeholders'
        
        # ========== cv_status ==========
        if parent == 'cv_status':
            return 'std::cv_status'
        
        # ========== future_status ==========
        if parent == 'future_status':
            return 'std::future_status'
        
        # ========== launch ==========
        if parent == 'launch':
            return 'std::launch'
        
        # ========== allocator_arg_t ==========
        if parent == 'allocator_arg':
            return 'std::allocator_arg'
        
        # ========== piecewise_construct_t ==========
        if parent == 'piecewise_construct':
            return 'std::piecewise_construct'
        
        # ========== in_place ==========
        if parent.startswith('in_place'):
            return 'std::in_place'
        
        # ========== defer_lock_t ==========
        if parent in ['defer_lock', 'try_to_lock', 'adopt_lock']:
            return 'std::lock_tags'
        
        # ========== seekdir ==========
        if parent in ['seekdir', 'beg', 'end', 'cur']:
            return 'std::seekdir'
        
        # ========== openmode ==========
        if parent in ['openmode', 'app', 'ate', 'binary', 'in', 'out', 'trunc']:
            return 'std::openmode'
        
        # ========== iostate ==========
        if parent in ['iostate', 'goodbit', 'badbit', 'eofbit', 'failbit']:
            return 'std::iostate'
        
        # ========== fmtflags ==========
        if parent in ['fmtflags', 'boolalpha', 'dec', 'fixed', 'hex', 'internal', 'left',
                     'oct', 'right', 'scientific', 'showbase', 'showpoint', 'showpos',
                     'skipws', 'unitbuf', 'uppercase', 'adjustfield', 'basefield', 'floatfield']:
            return 'std::fmtflags'
        
        # ========== float_denorm_style ==========
        if parent in ['float_denorm_style', 'denorm_indeterminate', 'denorm_absent', 'denorm_present']:
            return 'std::float_denorm_style'
        
        # ========== float_round_style ==========
        if parent in ['float_round_style', 'round_indeterminate', 'round_toward_zero',
                     'round_to_nearest', 'round_toward_infinity', 'round_toward_neg_infinity']:
            return 'std::float_round_style'
        
        # ========== 容器类成员 ==========
        containers = {
            'vector', 'string', 'array', 'deque', 'list', 'forward_list',
            'set', 'multiset', 'map', 'multimap',
            'unordered_set', 'unordered_multiset', 'unordered_map', 'unordered_multimap',
            'queue', 'priority_queue', 'stack',
            'shared_ptr', 'unique_ptr', 'weak_ptr',
            'string_view', 'optional', 'variant', 'any',
            'function', 'tuple', 'pair',
            'istream', 'ostream', 'iostream', 'stringstream', 'istringstream', 'ostringstream',
            'ifstream', 'ofstream', 'fstream',
            'thread', 'mutex', 'recursive_mutex', 'timed_mutex', 'recursive_timed_mutex',
            'lock_guard', 'unique_lock', 'scoped_lock', 'shared_lock',
            'condition_variable', 'condition_variable_any',
            'future', 'promise', 'packaged_task',
            'allocator', 'allocator_traits',
            'iterator', 'reverse_iterator', 'move_iterator', 'back_insert_iterator',
            'front_insert_iterator', 'insert_iterator', 'istream_iterator', 'ostream_iterator',
            'istreambuf_iterator', 'ostreambuf_iterator',
            'bitset', 'valarray',
            'regex', 'smatch', 'cmatch', 'ssub_match', 'csub_match', 'wsmatch', 'wcmatch',
            'locale', 'ctype', 'codecvt', 'collate',
            'random_device', 'mt19937', 'mt19937_64', 'uniform_int_distribution',
            'uniform_real_distribution', 'normal_distribution', 'bernoulli_distribution',
            'binomial_distribution', 'geometric_distribution',
            'seed_seq', 'linear_congruential_engine', 'mersenne_twister_engine',
            'complex', 'valarray',
            'error_code', 'error_condition', 'error_category', 'system_error',
        }
        
        if parent in containers:
            return f'std::{parent}'
        
        # 返回第一级 + 第二级（保留结构）
        if len(parts) >= 2:
            return f'std::{parent}::{parts[1]}'
        return f'std::{parent}'
    
    # ========== 第三层：单层级的 ==========
    # 算法（需要提前处理）
    algorithms = [
        'sort', 'stable_sort', 'partial_sort', 'partial_sort_copy', 'is_sorted', 'is_sorted_until',
        'nth_element', 'lower_bound', 'upper_bound', 'equal_range', 'binary_search',
        'find', 'find_if', 'find_if_not', 'find_end', 'find_first_of', 'adjacent_find',
        'count', 'count_if', 'mismatch', 'equal', 'is_permutation', 'search', 'search_n',
        'copy', 'copy_if', 'copy_n', 'copy_backward', 'move_backward',
        'swap_ranges', 'iter_swap', 'transform', 'replace', 'replace_if',
        'replace_copy', 'replace_copy_if', 'fill', 'fill_n', 'generate', 'generate_n',
        'remove', 'remove_if', 'remove_copy', 'remove_copy_if', 'unique', 'unique_copy',
        'reverse', 'reverse_copy', 'rotate', 'rotate_copy', 'shuffle', 'sample',
        'partition', 'stable_partition', 'partition_copy', 'partition_point',
        'is_partitioned', 'merge', 'inplace_merge', 'includes', 'set_union',
        'set_intersection', 'set_difference', 'set_symmetric_difference',
        'push_heap', 'pop_heap', 'make_heap', 'sort_heap', 'is_heap', 'is_heap_until',
        'max', 'min', 'minmax', 'min_element', 'max_element', 'minmax_element',
        'clamp', 'lexicographical_compare', 'next_permutation', 'prev_permutation',
        'all_of', 'any_of', 'none_of', 'for_each', 'for_each_n',
        'accumulate', 'reduce', 'inner_product', 'transform_reduce',
        'partial_sum', 'exclusive_scan', 'inclusive_scan', 'transform_exclusive_scan',
        'transform_inclusive_scan', 'adjacent_difference', 'iota',
        'gcd', 'lcm', 'midpoint', 'lerp',
        'destroy', 'destroy_at', 'destroy_n', 'construct_at',
        'uninitialized_copy', 'uninitialized_copy_n', 'uninitialized_fill', 'uninitialized_fill_n',
        'uninitialized_move', 'uninitialized_move_n', 'uninitialized_default_construct',
        'uninitialized_default_construct_n', 'uninitialized_value_construct', 'uninitialized_value_construct_n',
        'uninitialized_relocate', 'uninitialized_relocate_n', 'relocate', 'relocate_at',
        'copy_n', 'copy_if', 'move', 'swap'
    ]
    if name in algorithms:
        return 'std::algorithms'
    
    # 数学函数
    math_funcs = [
        'abs', 'fabs', 'fmod', 'remainder', 'remquo', 'fma', 'fmax', 'fmin', 'fdim',
        'exp', 'exp2', 'expm1', 'log', 'log2', 'log10', 'log1p',
        'pow', 'sqrt', 'cbrt', 'hypot',
        'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'atan2',
        'sinh', 'cosh', 'tanh', 'asinh', 'acosh', 'atanh',
        'ceil', 'floor', 'trunc', 'round', 'lround', 'llround', 'nearbyint', 'rint', 'lrint', 'llrint',
        'isfinite', 'isinf', 'isnan', 'isnormal', 'signbit',
        'isgreater', 'isgreaterequal', 'isless', 'islessequal', 'islessgreater', 'isunordered',
        'erf', 'erfc', 'tgamma', 'lgamma',
        'copysign', 'nan', 'nextafter', 'nexttoward',
        'fpclassify', 'scalbn', 'scalbln', 'ilogb', 'logb', 'modf', 'frexp', 'ldexp',
        'assoc_laguerre', 'assoc_legendre', 'beta', 'comp_ellint_1', 'comp_ellint_2', 'comp_ellint_3',
        'cyl_bessel_i', 'cyl_bessel_j', 'cyl_bessel_k', 'cyl_neumann',
        'ellint_1', 'ellint_2', 'ellint_3', 'expint', 'hermite', 'legendre', 'laguerre',
        'riemann_zeta', 'sph_bessel', 'sph_legendre', 'sph_neumann',
        'riemann_zeta', 'hermite', 'legendre', 'laguerre', 'expint'
    ]
    if name in math_funcs:
        return 'std::math'
    
    # C 库兼容函数
    c_funcs = [
        'memcpy', 'memmove', 'memset', 'memcmp', 'memchr', 'strcpy', 'strncpy', 'strcat',
        'strncat', 'strcmp', 'strncmp', 'strcoll', 'strxfrm', 'strchr', 'strrchr',
        'strspn', 'strcspn', 'strpbrk', 'strstr', 'strtok', 'strlen', 'strerror',
        'strtoul', 'strtoull', 'strtof', 'strtod', 'strtold', 'strtoimax', 'strtoumax',
        'atoi', 'atol', 'atoll', 'atof', 'mblen', 'mbtowc', 'wctomb', 'mbstowcs', 'wcstombs',
        'qsort', 'bsearch', 'rand', 'srand', 'malloc', 'calloc', 'realloc', 'free',
        'exit', 'abort', 'atexit', 'system', 'getenv', 'clock', 'time', 'difftime',
        'mktime', 'asctime', 'ctime', 'gmtime', 'localtime', 'strftime', 'wcsftime',
        'remove', 'rename', 'tmpfile', 'tmpnam', 'fopen', 'freopen', 'fclose',
        'fflush', 'fwide', 'setbuf', 'setvbuf', 'fprintf', 'fscanf', 'printf', 'scanf',
        'sprintf', 'sscanf', 'vprintf', 'vfprintf', 'vsprintf', 'vsnprintf', 'snprintf',
        'fgetc', 'fgets', 'fputc', 'fputs', 'getc', 'getchar', 'gets', 'putc', 'putchar',
        'puts', 'ungetc', 'fgetwc', 'fgetws', 'fputwc', 'fputws', 'getwc', 'getwchar',
        'putwc', 'putwchar', 'ungetwc', 'fgetpos', 'fsetpos', 'fseek', 'ftell', 'rewind',
        'clearerr', 'feof', 'ferror', 'perror', 'fwprintf', 'fwscanf', 'wprintf', 'wscanf',
        'swprintf', 'swscanf', 'vwprintf', 'vfwprintf', 'vswprintf', 'aligned_alloc',
        'quick_exit', 'at_quick_exit', 'getenv_s', 'system_s',
        'bsearch_s', 'qsort_s', 'fopen_s', 'freopen_s', 'tmpfile_s', 'tmpnam_s',
        'snprintf_s', 'sprintf_s', 'sscanf_s', 'vfprintf_s', 'vfscanf_s', 'vprintf_s',
        'vscanf_s', 'vsnprintf_s', 'vsprintf_s', 'vsscanf_s', 'fscanf_s', 'scanf_s',
        'fprintf_s', 'printf_s', 'gets_s', 'wcstombs_s', 'mbstowcs_s', 'mbsrtowcs_s',
        'wcsrtombs_s', 'wcrtomb_s', 'mbrtowc_s', 'memcpy_s', 'memmove_s', 'strcpy_s',
        'strncpy_s', 'strcat_s', 'strncat_s', 'strerror_s', 'strnlen_s', 'ctime_s',
        'gmtime_s', 'localtime_s', 'asctime_s', 'wctomb_s', 'mbstowcs_s',
        'aligned_alloc', '_Exit', 'quick_exit', 'at_quick_exit', 'getenv_s'
    ]
    if name in c_funcs:
        return 'std::c_compat'
    
    # 字符分类
    ctypes = [
        'isalnum', 'isalpha', 'isblank', 'iscntrl', 'isdigit', 'isgraph', 'islower',
        'isprint', 'ispunct', 'isspace', 'isupper', 'isxdigit', 'tolower', 'toupper',
        'iswalnum', 'iswalpha', 'iswblank', 'iswcntrl', 'iswdigit', 'iswgraph', 'iswlower',
        'iswprint', 'iswpunct', 'iswspace', 'iswupper', 'iswxdigit', 'towlower', 'towupper',
        'iswctype', 'wctype'
    ]
    if name in ctypes:
        return 'std::ctype'
    
    # IO manipulators
    io_manipulators = [
        'hex', 'oct', 'dec', 'hexfloat', 'defaultfloat', 'scientific', 'fixed',
        'setw', 'setprecision', 'setfill', 'setbase', 'setiosflags', 'resetiosflags',
        'boolalpha', 'noboolalpha', 'showbase', 'noshowbase', 'showpoint', 'noshowpoint',
        'showpos', 'noshowpos', 'skipws', 'noskipws', 'uppercase', 'nouppercase',
        'unitbuf', 'nounitbuf', 'internal', 'left', 'right', 'ws', 'ends', 'flush',
        'put_money', 'get_money', 'put_time', 'get_time', 'quoted'
    ]
    if name in io_manipulators:
        return 'std::io_manipulators'
    
    # 类型萃取 traits
    type_traits = [
        'is_same', 'is_same_v', 'is_void', 'is_void_v', 'is_integral', 'is_integral_v',
        'is_floating_point', 'is_floating_point_v', 'is_array', 'is_array_v',
        'is_pointer', 'is_pointer_v', 'is_reference', 'is_reference_v',
        'is_lvalue_reference', 'is_lvalue_reference_v', 'is_rvalue_reference', 'is_rvalue_reference_v',
        'is_const', 'is_const_v', 'is_volatile', 'is_volatile_v',
        'is_trivial', 'is_trivial_v', 'is_trivially_copyable', 'is_trivially_copyable_v',
        'is_trivially_constructible', 'is_trivially_constructible_v',
        'is_trivially_default_constructible', 'is_trivially_default_constructible_v',
        'is_trivially_copy_constructible', 'is_trivially_copy_constructible_v',
        'is_trivially_move_constructible', 'is_trivially_move_constructible_v',
        'is_trivially_assignable', 'is_trivially_assignable_v',
        'is_trivially_copy_assignable', 'is_trivially_copy_assignable_v',
        'is_trivially_move_assignable', 'is_trivially_move_assignable_v',
        'is_trivially_destructible', 'is_trivially_destructible_v',
        'is_standard_layout', 'is_standard_layout_v', 'is_pod', 'is_pod_v',
        'is_literal_type', 'is_literal_type_v', 'is_empty', 'is_empty_v',
        'is_polymorphic', 'is_polymorphic_v', 'is_abstract', 'is_abstract_v',
        'is_final', 'is_final_v', 'is_aggregate', 'is_aggregate_v',
        'is_signed', 'is_signed_v', 'is_unsigned', 'is_unsigned_v',
        'is_constructible', 'is_constructible_v', 'is_default_constructible', 'is_default_constructible_v',
        'is_copy_constructible', 'is_copy_constructible_v', 'is_move_constructible', 'is_move_constructible_v',
        'is_assignable', 'is_assignable_v', 'is_copy_assignable', 'is_copy_assignable_v',
        'is_move_assignable', 'is_move_assignable_v', 'is_destructible', 'is_destructible_v',
        'is_swappable', 'is_swappable_v', 'is_swappable_with', 'is_swappable_with_v',
        'is_nothrow_constructible', 'is_nothrow_constructible_v',
        'is_nothrow_default_constructible', 'is_nothrow_default_constructible_v',
        'is_nothrow_copy_constructible', 'is_nothrow_copy_constructible_v',
        'is_nothrow_move_constructible', 'is_nothrow_move_constructible_v',
        'is_nothrow_assignable', 'is_nothrow_assignable_v',
        'is_nothrow_copy_assignable', 'is_nothrow_copy_assignable_v',
        'is_nothrow_move_assignable', 'is_nothrow_move_assignable_v',
        'is_nothrow_destructible', 'is_nothrow_destructible_v',
        'is_nothrow_swappable', 'is_nothrow_swappable_v',
        'is_invocable', 'is_invocable_v', 'is_invocable_r', 'is_invocable_r_v',
        'is_base_of', 'is_base_of_v', 'is_convertible', 'is_convertible_v',
        'enable_if', 'enable_if_t', 'conditional', 'conditional_t',
        'common_type', 'common_type_t', 'underlying_type', 'underlying_type_t',
        'result_of', 'result_of_t', 'invoke_result', 'invoke_result_t',
        'void_t', 'conjunction', 'conjunction_v', 'disjunction', 'disjunction_v',
        'negation', 'negation_v', 'bool_constant',
        'integral_constant', 'true_type', 'false_type',
        'is_enum', 'is_enum_v', 'is_class', 'is_class_v', 'is_union', 'is_union_v',
        'is_function', 'is_function_v', 'is_object', 'is_object_v', 'is_scalar', 'is_scalar_v',
        'is_arithmetic', 'is_arithmetic_v', 'is_fundamental', 'is_fundamental_v',
        'is_compound', 'is_compound_v', 'is_member_pointer', 'is_member_pointer_v',
        'is_member_object_pointer', 'is_member_object_pointer_v',
        'is_member_function_pointer', 'is_member_function_pointer_v',
        'alignment_of', 'alignment_of_v', 'rank', 'rank_v', 'extent', 'extent_v',
        'remove_cv', 'remove_cv_t', 'remove_const', 'remove_const_t',
        'remove_volatile', 'remove_volatile_t', 'add_cv', 'add_cv_t',
        'add_const', 'add_const_t', 'add_volatile', 'add_volatile_t',
        'remove_reference', 'remove_reference_t', 'add_lvalue_reference', 'add_lvalue_reference_t',
        'add_rvalue_reference', 'add_rvalue_reference_t', 'remove_pointer', 'remove_pointer_t',
        'add_pointer', 'add_pointer_t', 'make_signed', 'make_signed_t',
        'make_unsigned', 'make_unsigned_t', 'remove_extent', 'remove_extent_t',
        'remove_all_extents', 'remove_all_extents_t', 'decay', 'decay_t',
        'is_bind_expression', 'is_bind_expression_v', 'is_placeholder', 'is_placeholder_v',
        'aligned_storage', 'aligned_storage_t', 'aligned_union', 'aligned_union_t',
        'tuple_size', 'tuple_size_v', 'tuple_element', 'tuple_element_t',
        'variant_size', 'variant_size_v', 'variant_alternative', 'variant_alternative_t',
        'index_sequence', 'make_index_sequence', 'index_sequence_for'
    ]
    if name in type_traits:
        return 'std::type_traits'
    
    # 函数和绑定
    functional = [
        'bind', 'mem_fn', 'not_fn', 'invoke', 'invoke_r',
        'reference_wrapper', 'ref', 'cref', 'unwrap_reference', 'unwrap_ref_decay'
    ]
    if name in functional:
        return 'std::functional'
    
    # 辅助函数
    utility_funcs = [
        'forward', 'move', 'move_if_noexcept', 'swap', 'exchange', 'as_const',
        'to_underlying', 'cmp_equal', 'cmp_not_equal', 'cmp_less', 'cmp_greater',
        'cmp_less_equal', 'cmp_greater_equal', 'in_range',
        'declval', 'decltype', 'sizeof', 'offsetof', 'typeid', 'addressof'
    ]
    if name in utility_funcs:
        return 'std::utility'
    
    # 内存操作
    memory_funcs = [
        'addressof', 'align', 'assume_aligned', 'make_unique', 'make_shared',
        'allocate_shared', 'static_pointer_cast', 'dynamic_pointer_cast', 'const_pointer_cast',
        'reinterpret_pointer_cast', 'get_deleter', 'get', 'get_if', 'holds_alternative',
        'visit', 'monostate', 'valueless_by_exception', 'destroy_at', 'construct_at',
        'uninitialized_default_construct', 'uninitialized_value_construct',
        'uninitialized_copy', 'uninitialized_move', 'uninitialized_fill',
        'destroy', 'destroy_n', 'destroy_at', 'construct_at', 'raw_storage_iterator'
    ]
    if name in memory_funcs:
        return 'std::memory'
    
    # 迭代器工具
    iterator_tools = [
        'advance', 'distance', 'next', 'prev', 'begin', 'end', 'cbegin', 'cend',
        'rbegin', 'rend', 'crbegin', 'crend', 'size', 'ssize', 'empty', 'data',
        'front', 'back', 'front_insert_iterator', 'back_insert_iterator',
        'insert_iterator', 'make_move_iterator'
    ]
    if name in iterator_tools:
        return 'std::iterator'
    
    # 字符串转换
    string_conv = [
        'to_string', 'to_wstring', 'stoi', 'stol', 'stoll', 'stoul', 'stoull',
        'stof', 'stod', 'stold'
    ]
    if name in string_conv:
        return 'std::string_conversion'
    
    # 作用域守卫
    scope_guards = [
        'scope_exit', 'scope_fail', 'scope_success', 'make_scope_exit',
        'uncaught_exceptions'
    ]
    if name in scope_guards:
        return 'std::scope_guards'
    
    # 同步原语
    sync_primitives = [
        'barrier', 'latch', 'semaphore', 'binary_semaphore', 'counting_semaphore',
        'binary_semaphore', 'counting_semaphore', 'notify_all_at_thread_exit'
    ]
    if name in sync_primitives:
        return 'std::sync_primitives'
    
    # 默认返回
    return f'std::{name}'

def main():
    # 读取原始数据
    components = []
    with open('E:/blender-git/blender/std_analysis/std_components_freq.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # 解析 "5031 std::string" 格式
            match = re.match(r'^\s*(\d+)\s+(.+)$', line)
            if match:
                count = int(match.group(1))
                component = match.group(2).strip()
                components.append((component, count))
    
    print(f"读取到 {len(components)} 个组件")
    
    # 分类统计
    classified = defaultdict(int)
    detailed_mapping = defaultdict(list)  # 记录每个分类包含的原始组件
    
    for component, count in components:
        parent = get_parent_component(component)
        classified[parent] += count
        detailed_mapping[parent].append((component, count))
    
    # 按数量排序
    sorted_classified = sorted(classified.items(), key=lambda x: x[1], reverse=True)
    
    # 保存分类结果 - 汇总版
    with open('E:/blender-git/blender/std_analysis/std_classified.txt', 'w', encoding='utf-8') as f:
        f.write("# Blender std:: 组件智能分类统计\n\n")
        f.write(f"总组件数: {len(components)}\n")
        f.write(f"分类后类别数: {len(classified)}\n\n")
        f.write("| 分类 | 使用次数 |\n")
        f.write("|------|----------|\n")
        for parent, count in sorted_classified:
            f.write(f"| {parent} | {count} |\n")
    
    # 保存CSV
    with open('E:/blender-git/blender/std_analysis/std_classified.csv', 'w', encoding='utf-8') as f:
        f.write("Category,Count\n")
        for parent, count in sorted_classified:
            f.write(f'"{parent}",{count}\n')
    
    # 保存详细映射关系
    with open('E:/blender-git/blender/std_analysis/std_classified_detail.txt', 'w', encoding='utf-8') as f:
        f.write("# Blender std:: 组件分类详细映射\n\n")
        for parent, count in sorted_classified:
            f.write(f"\n## {parent} (总计: {count})\n\n")
            f.write("| 原始组件 | 使用次数 |\n")
            f.write("|----------|----------|\n")
            # 按使用次数排序
            sorted_details = sorted(detailed_mapping[parent], key=lambda x: x[1], reverse=True)
            for comp, cnt in sorted_details:
                f.write(f"| {comp} | {cnt} |\n")
    
    print(f"\n分类完成!")
    print(f"- 分类后类别数: {len(classified)}")
    print(f"- 原始组件数: {len(components)}")
    print(f"\nTop 30 分类:")
    for i, (parent, count) in enumerate(sorted_classified[:30], 1):
        print(f"  {i:2d}. {parent}: {count}")
    
    # 输出一些有趣的统计
    print(f"\n=== 分类概览 ===")
    
    # 计算各大类总数
    categories = {
        '容器类': ['std::vector', 'std::string', 'std::array', 'std::map', 'std::unordered_map', 
                   'std::set', 'std::unordered_set', 'std::deque', 'std::list', 'std::forward_list',
                   'std::queue', 'std::stack', 'std::priority_queue'],
        '智能指针': ['std::unique_ptr', 'std::shared_ptr', 'std::weak_ptr'],
        '算法': ['std::algorithms'],
        '类型萃取': ['std::type_traits'],
        '数学函数': ['std::math'],
        'IO流': ['std::iostream', 'std::istream', 'std::ostream', 'std::stringstream'],
        'IO操作符': ['std::io_manipulators', 'std::ios'],
        '并发': ['std::thread', 'std::mutex', 'std::atomic', 'std::condition_variable', 
                'std::future', 'std::promise'],
        '字符串': ['std::string_view', 'std::string_conversion'],
        '内存': ['std::memory', 'std::make_unique', 'std::make_shared'],
        '时间': ['std::chrono::duration', 'std::chrono::clock', 'std::chrono::time_point'],
        '异常': ['std::exception', 'std::runtime_error', 'std::logic_error'],
        '函数式': ['std::function', 'std::functional', 'std::bind'],
        '迭代器': ['std::iterator'],
        '实用工具': ['std::optional', 'std::variant', 'std::any', 'std::tuple', 'std::pair'],
        'C兼容': ['std::c_compat'],
    }
    
    for cat_name, cat_items in categories.items():
        total = sum(classified.get(item, 0) for item in cat_items)
        if total > 0:
            print(f"  {cat_name}: {total}")

if __name__ == '__main__':
    main()

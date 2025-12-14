# Blender Development Guide for Agentic Coding Agents

## Build Commands

### Primary Build System
- **Build**: 编译的话, 一定要在文件夹 E:/blender-git/blender_ninja_lite_debug/ 中执行: rebuild -j8,一定要这样
- **Test**: `make test` or `ctest . --output-on-failure`
- **Single test**: `ctest -R <test_name> --output-on-failure`
- **Format code**: `make format PATHS="path/to/files"`
- **Configure**: `make config` (Linux/macOS) or uses Visual Studio (Windows)

### Build Variants
- **Debug build**: `make debug`
- **Release build**: `make release` 
- **Lite build**: `make lite` (faster, fewer features)
- **Developer build**: `make developer` (recommended for development)

### Code Quality Checks
- **Lint/Format**: `make format` (uses clang-format + autopep8)
- **Static analysis**: `make check_cppcheck`, `make check_clang_array`
- **License check**: `make check_licenses`
- **Spelling check**: `make check_spelling_c`, `make check_spelling_py`


## Markdown 文档结构模板

### 1. 文档头部格式
```markdown
# [文档标题]

## 目录

- [概述](#概述)
- [核心组件分析](#核心组件分析)
  - [1. 组件名称](#1-组件名称)
  - [2. 组件名称](#2-组件名称)
- [核心函数解析](#核心函数解析)
  - [1. 函数名称](#1-函数名称)
  - [2. 函数名称](#2-函数名称)
- [实现细节](#实现细节)
- [总结](#总结)
```

### 2. 章节格式规范
- **二级标题后必须添加目录链接**: `## 章节名称  [[⬆](#目录)]`
- **三级标题**: `### 1. 编号 + 标题`
- **四级标题**: `#### 2.1 编号 + 标题`

### 3. 代码块引用格式
- **每个涉及代码的地方都必须标注位置**: 
 **定义位置**: `文件路径:行号范围`

**示例**:
**定义位置**: `draw_manager_text.cc:54-69`
```cpp
struct Example {
    int member;
};
```

## Code Style Guidelines

### C++ Code Style
- **Formatting**: Uses clang-format with `.clang-format` config
- **Line limit**: 99 characters maximum
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Memory**: Use MEM_* functions from guardedalloc (MEM_mallocN, MEM_callocN, MEM_freeN)
- **Headers**: SPDX license headers required on all files
- **Includes**: Use angle brackets for system headers, quotes for local headers
- **Error handling**: Return error codes, use BLI_assert() for developer checks

### Python Code Style
- **Formatting**: autopep8 compliance via `make check_pep8`
- **Type checking**: mypy enabled in some areas
- **Imports**: Group imports (standard library, third-party, local Blender imports)

### CMake Style
- **File lists**: Use `CMakeLists.txt` file lists for consistency
- **Naming**: UPPERCASE for variables/caches, PascalCase for targets
- **Checking**: `make check_cmake` validates file list consistency

### General Principles
- **No exceptions**: Blender doesn't use C++ exceptions
- **Minimal dependencies**: Prefer existing Blender libraries over external ones
- **Cross-platform**: Code must work on Linux, Windows, macOS
- **Documentation**: Comment public APIs, especially DNA/structures
- **Testing**: Add unit tests in `tests/` directory when adding new functionality

## Testing
- Unit tests use GTest framework in `tests/` directory  
- Python tests in `tests/python/`
- Use `make test` to run full test suite
- Single test: `ctest -R <test_pattern> --output-on-failure`
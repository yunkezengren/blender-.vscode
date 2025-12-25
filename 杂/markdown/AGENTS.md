# AGENTS.md - Blender Development Guide

This file provides essential information for agentic coding agents working in the Blender codebase.

## Build Commands

### Building Blender
- **Unix/Linux/macOS**: `make [target]` (e.g., `make release`, `make developer`, `make debug`)
- **Windows**: `make.bat [target]` (e.g., `make.bat release`, `make.bat developer`, `make.bat debug`)
- **Build directory**: E:/blender-git/blender_ninja_lite_debug/
- **Build**: 编译的话, 一定要在文件夹 E:/blender-git/blender_ninja_lite_debug/ 中执行: rebuild -j8,一定要这样
- **Configure**: `make config` or manually with cmake
- **Clean**: `make clean` (after setting target)

### Common Build Targets
- `release` - Full build matching blender.org releases
- `developer` - Faster builds with error checking and tests (recommended)
- `debug` - Debuggable unoptimized build
- `lite` - Smaller binary with fewer features
- `ninja` - Use Ninja build system for faster compilation

## Testing Commands

### Running Tests
- **Run all tests**: `make test` or `ctest --output-on-failure` (from build directory)
- **Run single test**: `ctest -R <test_pattern>` (e.g., `ctest -R compositor_cpu_file_output`)
- **Update failing tests**: `BLENDER_TEST_UPDATE=1 ctest -R <test_pattern>`
- **Note**: Tests require `WITH_GTESTS=ON` during CMake configuration

### Python Tests
- Located in `tests/python/`
- Use unittest framework
- Run from build directory with Blender binary

## Code Style Guidelines

### C/C++ Code
- **Indentation**: 2 spaces (no tabs)
- **Line length**: 99 characters max
- **Formatting**: Run `make format` (uses clang-format per `.clang-format` config)
- **Headers**: Must include SPDX license header:
  ```c
  /* SPDX-FileCopyrightText: YYYY Blender Authors
   *
   * SPDX-License-Identifier: GPL-2.0-or-later */
  ```
- **Includes**: Use `"local.h"` for project headers, `<system.h>` for system headers
- **Naming**:
  - Functions: `snake_case` (e.g., `BLI_strdup`)
  - Classes: `PascalCase` (e.g., `VectorSet`)
  - Macros: `UPPER_CASE` (e.g., `MEM_mallocN`)
- **Documentation**: Doxygen style with `\param`, `\retval`, `\return` tags
- **Error handling**: Return `nullptr` or `false` on failure; use `BLI_assert()` for invariants
- **Memory**: Use Blender's memory macros: `MEM_mallocN`, `MEM_freeN`, `MEM_callocN`
- **String handling**: Use BLI string functions: `BLI_strdup`, `BLI_strncpy`
- **Attributes**: Use `ATTR_NONNULL`, `ATTR_MALLOC`, `ATTR_WARN_UNUSED_RESULT` where appropriate

### Python Code
- **Indentation**: 4 spaces
- **Line length**: 120 characters max
- **Formatting**: autopep8 (runs automatically with `make format`)
- **Style**: Follow PEP8 with Blender conventions
- **Quotes**: Single quotes for enums, double quotes for strings
  ```python
  bpy.context.scene.render.image_settings.file_format = 'PNG'
  bpy.context.scene.render.filepath = "//render_out"
  ```
- **Imports**: Explicit imports only (no `import *`)
- **Class names**: `PascalCase` (e.g., `ViewLayerTesting`)
- **Functions/variables**: `snake_case` (e.g., `do_scene_write_read`)

## Linting and Static Analysis

### Available Checks
- **Format code**: `make format PATHS="source/path"`
- **Cppcheck**: `make check_cppcheck`
- **Clang-tidy**: Enable with `WITH_CLANG_TIDY=ON` in CMake
- **Mypy**: `make check_mypy`
- **Spelling**: `make check_spelling_c`, `make check_spelling_py`
- **Licenses**: `make check_licenses` (verifies SPDX headers)
- **Struct comments**: `make check_struct_comments`
- **CMake consistency**: `make check_cmake`
- **Descriptions**: `make check_descriptions`

## Important File Locations

- **CMakeLists.txt**: Build configuration
- **.clang-format**: C/C++ formatting rules
- **.clang-tidy**: Static analysis checks
- **.editorconfig**: Editor-agnostic formatting settings
- **tools/check_source/**: Static checking scripts
- **tests/python/**: Python integration tests
- **tests/gtests/**: C++ unit tests (require `WITH_GTESTS=ON`)

## Key Conventions

1. **Always format code before committing**: `make format`
2. **Add SPDX license headers** to all new files
3. **Use Blender's utilities** instead of standard C/C++ when available (e.g., BLI, MEM)
4. **Run tests** before submitting: `make test`
5. **Check for warnings** - build with developer warnings enabled
6. **Document public APIs** with Doxygen comments
7. **Follow existing patterns** in the module you're working on
8. **Python scripts** must follow PEP8 and use proper Blender API conventions

## Platform-Specific Notes

- **Windows**: Use `make.bat` instead of `make`, requires Visual Studio or Clang
- **macOS**: Xcode or Clang required
- **Linux**: GCC 11+ or Clang 8+ required
- **ARM64**: Clang is default compiler on Windows ARM64

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build System

Blender uses CMake with convenience wrappers for common build configurations.

### Windows Build Commands
在文件夹 E:/blender-git/blender_ninja_lite_debug/ 中执行: rebuild -j8 或 powershell -Command "& .\rebuild.cmd"
```bash
# Basic build (uses MSBuild or Ninja)
make.bat

# # Build with specific configuration
# make.bat lite          # Minimal build, faster compilation
# make.bat full          # All features enabled
# make.bat debug         # Debug build
# make.bat release       # Release build matching blender.org releases
# make.bat developer     # Developer mode with faster builds and tests

# Build with Ninja (faster)
make.bat ninja

# Run tests
make.bat test

# Update source and libraries
make.bat update

# Format code
make.bat format
```

### Build Directory Structure

- Out-of-source builds are required (in-source builds are blocked)
- Default build directory: `../build_<platform>` (e.g., `../build_linux`, `../build_windows`)
- Build variants append suffixes: `../build_linux_debug`, `../build_linux_lite`, etc.
- Built binary location:
  - Linux/Windows: `<build_dir>/bin/blender`
  - macOS: `<build_dir>/bin/Blender.app/Contents/MacOS/Blender`

### CMake Configuration

- Main CMakeLists.txt: `CMakeLists.txt`
- Config presets: `build_files/cmake/config/`
  - `blender_lite.cmake` - Minimal features
  - `blender_full.cmake` - All features
  - `blender_release.cmake` - Release configuration
  - `blender_developer.cmake` - Developer mode
  - `bpy_module.cmake` - Python module
  - `blender_headless.cmake` - No GUI
  - `cycles_standalone.cmake` - Cycles only

## Codebase Architecture

### Top-Level Directory Structure

- **`source/blender/`** - Core Blender C/C++ code
- **`intern/`** - Internal libraries (Cycles, Ghost, etc.)
- **`extern/`** - External dependencies bundled with Blender
- **`scripts/`** - Python scripts (addons, modules, presets)
- **`release/`** - Release files (datafiles, icons, startup files)
- **`tests/`** - Test suite (Python tests, gtests, performance tests)
- **`build_files/`** - Build system files (CMake, platform-specific)
- **`doc/`** - Documentation generation scripts
- **`tools/`** - Development utilities (code checking, formatting)

### Core Source Modules (`source/blender/`)

Key architectural modules:

- **`blenkernel/`** - Core kernel, main data structures and operations
- **`blenlib/`** - Low-level utilities (math, strings, data structures)
- **`blenloader/`** - .blend file loading/saving
- **`makesdna/`** - DNA system (file format definitions, serialization)
- **`makesrna/`** - RNA system (runtime type introspection, Python API)
- **`depsgraph/`** - Dependency graph (evaluation order, updates)
- **`editors/`** - Editor modules (3D view, outliner, properties, etc.)
- **`windowmanager/`** - Window management, event system, operators
- **`gpu/`** - GPU abstraction layer
- **`draw/`** - Drawing/rendering pipeline
- **`render/`** - Render engines (Eevee, Workbench)
- **`compositor/`** - Compositor nodes
- **`nodes/`** - Node system (geometry nodes, shader nodes)
- **`geometry/`** - Geometry processing
- **`bmesh/`** - BMesh (mesh editing data structure)
- **`modifiers/`** - Mesh/object modifiers
- **`animrig/`** - Animation rigging system
- **`sequencer/`** - Video sequence editor
- **`python/`** - Python integration (bpy module)
- **`io/`** - Import/export (Alembic, USD, glTF, etc.)

### Internal Libraries (`intern/`)

- **`cycles/`** - Cycles render engine (standalone)
- **`ghost/`** - Platform abstraction (windowing, OpenGL context)
- **`guardedalloc/`** - Memory allocation tracking
- **`libmv/`** - Motion tracking library
- **`opensubdiv/`** - OpenSubdiv integration
- **`openvdb/`** - OpenVDB integration
- **`mantaflow/`** - Fluid simulation
- **`rigidbody/`** - Rigid body physics (Bullet wrapper)

### Python Scripts (`scripts/`)

- **`startup/`** - Startup scripts, UI definitions, app templates
- **`modules/`** - Python modules (bpy_extras, etc.)
- **`addons_core/`** - Core addons shipped with Blender
- **`presets/`** - User presets
- **`templates_py/`** - Python script templates

### DNA/RNA System

Blender's core architecture uses two key systems:

- **DNA (makesdna)**: Defines C structs for .blend file format. Changes to DNA structs require versioning code in `blenloader/` to maintain backward compatibility.
- **RNA (makesrna)**: Runtime type system providing introspection, Python API access, and UI generation. RNA wraps DNA structs and adds properties, functions, and metadata.

When modifying data structures:
1. Update DNA struct in `makesdna/DNA_*.h`
2. Add RNA properties in `makesrna/intern/rna_*.cc`
3. Add versioning code in `blenloader/intern/versioning_*.cc` if needed
4. Update relevant kernel code in `blenkernel/intern/`

## Testing

### Running Tests

```bash
# Run all tests
make test              # Linux/macOS
make.bat test          # Windows

# Run specific test categories
cd <build_dir>
ctest -R <pattern>     # Run tests matching pattern
ctest -L <label>       # Run tests with specific label

# Python tests
<blender_bin> --background --python tests/python/<test_file>.py

# GTests (C++ unit tests)
<build_dir>/bin/blender_test --gtest_filter=<pattern>
```

### Test Locations

- **`tests/python/`** - Python-based tests (operators, modifiers, etc.)
- **`tests/gtests/`** - C++ unit tests (GTest framework)
- **`source/blender/*/tests/`** - Module-specific tests
- **`tests/performance/`** - Performance benchmarks

## Code Style and Formatting

### Formatting Tools

```bash
# Format C/C++ and Python code
make format                    # Format all code
make format PATHS="<paths>"    # Format specific paths

# Check code style
make check_pep8                # Python PEP8 compliance
make check_mypy                # Python type checking
make check_cppcheck            # C/C++ static analysis
make check_spelling_c          # Spell check C/C++
make check_spelling_py         # Spell check Python
```

### Style Configuration

- **C/C++**: `.clang-format` (clang-format configuration)
- **Python**: `pyproject.toml` (autopep8 configuration, max line length 120)
- **Editor**: `.editorconfig` (basic editor settings)

### Code Conventions

- C/C++ files use lowercase with underscores: `BKE_mesh.h`, `mesh_convert.cc`
- Python follows PEP8 with 120 character line limit
- All files must have SPDX license headers
- DNA structs use specific naming: `typedef struct StructName { ... } StructName;`
- RNA properties follow naming conventions for Python API exposure

## Development Workflow

### Making Changes to Core Data Structures

1. Modify DNA struct in `makesdna/DNA_*.h`
2. Update RNA in `makesrna/intern/rna_*.cc`
3. Implement functionality in `blenkernel/intern/`
4. Add UI in `editors/*/` or Python in `scripts/`
5. Add versioning code if DNA changed
6. Write tests in `tests/` or module-specific `tests/`
7. Format code with `make format`

### Adding New Operators

Operators are in `source/blender/editors/*/`:
1. Define operator in C: `*_ops.cc` (e.g., `mesh_ops.cc`)
2. Register in module's `*_ops.cc` file
3. Add RNA properties for operator parameters
4. Implement `exec`, `invoke`, `modal` callbacks as needed
5. Add to UI in Python (`scripts/startup/bl_ui/`)

### Working with Geometry Nodes

Geometry nodes are in `source/blender/nodes/geometry/`:
- Each node is typically one file: `nodes/geometry/nodes/node_geo_*.cc`
- Node registration in `nodes/geometry/register_geometry_nodes.cc`
- Node evaluation uses lazy function system
- Field system for attribute operations

### Python API (bpy)

- Python integration: `source/blender/python/`
- bpy module structure mirrors RNA
- Extending bpy: Add RNA properties/functions, they auto-expose to Python
- Python addons: `scripts/addons_core/` (core) or user addons directory

## Platform-Specific Notes

### Windows

- Requires Visual Studio 2019 or 2022
- Libraries in `lib/windows_x64/` (auto-downloaded by build system)
- Use `make.bat` wrapper, not `make` directly
- Supports both MSBuild and Ninja generators

### Linux

- Requires GCC or Clang
- Libraries in `lib/linux_x64/` or system libraries
- Use `make` wrapper (GNUmakefile)
- Supports Make and Ninja generators

### macOS

- Requires Xcode command line tools
- Libraries in `lib/macos_arm64/` or `lib/macos_x64/`
- Universal binaries supported
- Use `make` wrapper

## Important Constraints

### File Format Compatibility

- .blend files must maintain backward compatibility
- DNA changes require versioning code in `blenloader/intern/versioning_*.cc`
- Test file loading with older .blend files after DNA changes

### Performance Considerations

- Blender handles large datasets (millions of polygons, thousands of objects)
- Avoid O(n²) algorithms in hot paths
- Use multi-threading where appropriate (BLI_task, threading utilities in blenlib)
- GPU operations should minimize CPU-GPU transfers

### Memory Management

- Use `MEM_*` functions from `guardedalloc` for tracked allocations
- DNA structs use specific allocation patterns
- Be careful with ownership and lifetime of data blocks

## Additional Resources

- Build instructions: https://developer.blender.org/docs/handbook/building_blender/
- Developer docs: https://developer.blender.org/docs/
- Code layout: https://developer.blender.org/docs/features/code_layout/
- Python API: https://docs.blender.org/api/current/

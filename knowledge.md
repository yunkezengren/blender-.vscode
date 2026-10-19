# Blender Project Knowledge

## Markdown Mermaid 配色约定

2026-10-17：本项目 VS Code Markdown 预览中，用户确认以下调整后颜色正常显示：将 Mermaid 的 `classDef` + `class` 绑定改为对每个节点直接使用 `style`。这是当前项目已验证可用的写法；未确定原先不显示颜色的插件或渲染器根因，不应推断所有 VS Code 都不支持 `classDef`。

后续编写项目 Markdown 图时优先使用直接节点样式，例如：

```mermaid
flowchart LR
    A["输入"] --> B["处理"] --> C["结果"]
    style A fill:#DBEAFE,stroke:#2563EB,color:#1E3A8A,stroke-width:2px
    style B fill:#FEF3C7,stroke:#D97706,color:#78350F,stroke-width:2px
    style C fill:#DCFCE7,stroke:#16A34A,color:#14532D,stroke-width:2px
    linkStyle default stroke:#64748B,stroke-width:2px
```

配色：蓝色表示入口/输入，金色表示计算/核心步骤，紫色表示构建/后续阅读，绿色表示完成/结果，灰色虚线表示可选内容。节点同时设置 `fill`、`stroke`、`color`，保证文字对比度。说明参考 `.markdown/重复区域-源码阅读/重复区域-源码阅读路径.md`。这是一项文档编写约定，无需添加不存在的 VS Code 配置项到 `settings.json`。

## What This Is
Blender — the free/open-source 3D creation suite (modeling, rigging, animation, simulation, rendering, compositing, motion tracking, video editing). Licensed GPL-2.0-or-later. Written in C, C++, and Python. Built with CMake. C++20 standard.

## Key Directories
- `source/blender/` — Main Blender application modules:
  - `blenkernel/` — Core data structures & scene management
  - `blenlib/` — Low-level utility library (BLI_*)
  - `editors/` — UI/editors (SpaceType handlers)
  - `gpu/` — GPU draw manager & backends (OpenGL, Vulkan, Metal)
  - `nodes/` — Node tree system (compositor, shader, geometry nodes)
  - `compositor/` — Compositor engine
  - `draw/` — Draw manager (viewport rendering)
  - `windowmanager/` — Window manager, operators, events
  - `makesdna/` — DNA (Data Nature Architecture) — .blend file serialization
  - `makesrna/` — RNA (data API / property system)
  - `python/` — Python API bindings (bpy)
  - `render/` — Render engine integration
  - `depsgraph/` — Dependency graph evaluation
  - `imbuf/` — Image buffer handling
  - `bmesh/` — BMesh mesh data structure
  - `modifiers/` — Modifier stack
  - `io/` — Import/export (Alembic, USD, FBX, OBJ, etc.)
  - `sequencer/` — Video sequencer
  - `geometry/` — Geometry nodes utilities
  - `functions/` — Multi-function infrastructure
  - `simulation/` — Simulation system
  - `asset_system/` — Asset system
  - `animrig/` — Animation rigging
  - `freestyle/` — Freestyle edge rendering
- `source/creator/` — Blender `main()` entry point
- `intern/` — Internal libraries (bundled, not part of Blender API):
  - `cycles/` — Cycles render engine
  - `guardedalloc/` — Memory allocator (MEM_*)
  - `ghost/` — OS windowing/input abstraction
  - `libmv/` — Motion tracking (LibMV)
  - `mantaflow/` — Fluid simulation
  - `openvdb/` — OpenVDB integration
  - `eigen/` — Eigen3 (linear algebra)
  - `sky/` — Sky model (Nishita)
  - `atomic/` — Atomic operations
  - `clog/` — Logging library
- `extern/` — External bundled libraries (audaspace, bullet, draco, gflags, glog, etc.)
- `scripts/` — Python scripts (addons, presets, startup, modules)
- `tests/` — Test suite (GTest C++ tests + Python tests)
- `build_files/` — CMake build system helpers, Windows build scripts
- `release/` — Release assets (icons, datafiles, startup.blend)
- `doc/` — Documentation (Python API, doxygen, blender file format)
- `tools/` — Dev/maintenance scripts (code checking, formatting, utils)
- `lib/` — Pre-compiled dependencies (platform-specific, from SVN/git-lfs)

## Build Commands

### Windows (this platform)
```bat
make.bat                        :: Build with MSVC (auto-detected)
make.bat ninja                  :: Build with Ninja generator
make.bat debug                  :: Debug build
make.bat full                   :: All dependencies enabled
make.bat lite                   :: Minimal build
make.bat release                :: Release build
make.bat developer              :: Developer config (tests + error checking)
make.bat update                 :: Update source + libraries
make.bat test                   :: Run tests via ctest
```
Build output goes to `../build_windows_*` by default.

### Killing a running instance before building (Windows)
A build fails with `LNK1168: cannot open bin\blender.exe for writing` when an instance is
running. Kill **only the instance holding that build directory's binary**, never every Blender
process — the user may have other sessions open (other worktrees, a second build dir, an
unsaved scene):

```powershell
# Preferred: kill only the process whose image path matches this build directory.
Get-Process blender -ErrorAction SilentlyContinue |
  Where-Object { $_.Path -like 'E:\blender-git\blender_ninja_lite_debug\*' } |
  Stop-Process -Force

# Equivalent via taskkill (filter by image path):
taskkill /F /FI "IMAGENAME eq blender.exe" /FI "PID eq <pid>"
```

Avoid a blanket `taskkill /F /IM blender.exe`: it terminates unrelated sessions and can lose
the user's unsaved work.

### Linux/macOS (via GNUmakefile)
```bash
make                            :: Build (auto-detects)
make debug                      :: Debug build
make full                       :: All dependencies
make lite                       :: Minimal build
make release                    :: Release build
make developer                  :: Developer config
make ninja                      :: Use Ninja
make update                     :: Update repo + libs
make test                       :: Run tests
```

### Manual CMake (any platform)
```bash
mkdir build && cd build
cmake ../blender                :: Configure
cmake --build . --target install :: Build
ctest                           :: Test
```
**Out-of-source builds only** — CMake will error on in-source builds.

## Test & Lint Commands
- `make test` or `ctest` — Run test suite (requires `WITH_GTESTS=ON`)
- `make check_cppcheck` — Static analysis with cppcheck
- `make check_clang_array` — Clang array bounds checking
- `make check_licenses` — SPDX license header verification
- `make check_pep8` — Python PEP8 checking
- `make check_mypy` — Python type checking
- `make check_cmake` — CMake file consistency
- `make check_spelling_c` / `check_spelling_py` — Spell checking
- `make format` — Auto-format with clang-format + autopep8

## Conventions & Gotchas

### Code Style
- **C/C++ indent**: 2 spaces (no tabs), max line 99 chars
- **Python indent**: 4 spaces, max line 120 chars
- **clang-format**: Project has `.clang-format`; use `make format` or `tools/utils_maintenance/clang_format_paths.py`
- **autopep8**: For Python; `tools/utils_maintenance/autopep8_format_paths.py`
- **Braces**: Opening brace on new line for functions; same line for control statements (unless multi-line condition, then next line)
- **Naming**: `snake_case` for functions/variables; `CamelCase` for types; `UPPER_CASE` for macros; BLI_*, MEM_*, GPU_* prefixes for library APIs
- **Header extension**: `.hh` for C++ headers, `.h` for C headers
- **Namespaces**: Closing brace comment `// namespace foo`

### C++ Standard
- **C++20 required** (no downgrading allowed)
- C11 with GNU extensions for C code

### Compiler Requirements
- GCC ≥ 14.0.0
- Clang ≥ 17.0
- MSVC ≥ 2019 (16.9.16)

### Build Gotchas
- **Out-of-source builds mandatory** — never build in source tree
- **Git LFS** required — `startup.blend` and other datafiles tracked via LFS; run `make update` or `git lfs pull` if startup.blend < 1KB
- **Pre-compiled libs** in `lib/` directory (platform-specific); auto-detected by CMake
- **Python ≥ 3.13** required for building
- On Windows, use `make.bat` not `make` (GNUmakefile will error on Windows)

### Architecture Notes
- **DNA** (`makesdna/`) defines all serializable data structures — changing struct order breaks .blend file compatibility
- **RNA** (`makesrna/`) exposes DNA as a runtime API — used by Python API, animation, UI
- **BKE** (`blenkernel/`) — "Blender Kernel" — core logic layer
- **BLI** (`blenlib/`) — "Blender Library" — containers, math, algorithms, file ops
- **GHOST** (`intern/ghost/`) — OS abstraction layer for windows/input
- **GPU backends**: OpenGL, Vulkan, Metal (platform-dependent availability)
- **WM** (`windowmanager/`) — handles operators, events, keymaps
- **ED** (`editors/`) — each editor (3D viewport, node editor, etc.) is a "space type"

### Python API
- Embedded CPython; `scripts/` contains startup, addons, modules
- `bpy` module generated via RNA
- Python API stability: only `bpy` namespace is public; `bpy.types`, `bpy.ops`, `bpy.data`

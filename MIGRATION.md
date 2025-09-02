# PyCAM GTK 2 → GTK 4 Migration

PyCAM has been successfully migrated from GTK 2 to GTK 4. This document tracks the completed work and remaining tasks.

Remember the following:

* Always use `.venv/bin/python` as the python interpreter
* The GUI entrypoint is the module `pycam.run_gui`
* Always use a timeout when running the GUI
* Log to the local `tmp` folder
* Ensure that any edits to `.ui` files are valid XML
* When any `.ui` files change, ensure they all pass validation (`validate_ui_files.sh`)

## Migration Status: ✅ CORE FUNCTIONALITY COMPLETE

### ✅ Major Systems Migrated
- **Core UI Infrastructure** - GTK 4 windows, menus, dialogs working
- **Plugin System** - All core plugins (Models, Tools, Processes, Bounds, Tasks) functional
- **File System** - Model loading, FilenameDialog, file operations working
- **UI Files** - All 44 UI files load successfully with GTK 4
- **Menu & Action System** - Complete MenuManager with GMenu/GSimpleAction
- **OpenGL Visualization** - Core OpenGL infrastructure migrated to GLArea

### ✅ UI File Fixes Completed (Phase 13)
- **All UI Files Compatible**: 44/44 UI files now load without errors
- **GTK 3→4 Property Migration**: Removed all deprecated properties
- **Widget Updates**: GtkRadioButton→GtkCheckButton, removed packing tags, fixed stock properties
- **Structural Fixes**: Fixed XML structure, child elements, internal dialogs

### ✅ Core User Workflows Working
- ✅ Application launch with workspace loading
- ✅ Model import and file selection (STL, etc.)
- ✅ Basic 3D visualization framework
- ✅ Plugin tab management and UI

## 🚧 Remaining GTK 4 Migration Tasks

Based on current plugin errors when running `.venv/bin/python -m pycam.run_gui`:

### High Priority: Core Plugin Fixes

#### Task 1: Signal Migration Issues
**Problem**: Multiple plugins using deprecated GTK 3 signals
- `delete-event` → `close-request` (ParallelProcessing, Fonts, MemoryAnalyzer)
- `focus-in-event` → `focus-enter` (ModelScaling, ModelPosition) 
- `button-press-event` → `button-pressed` (Log)
- `key-press-event` → `key-pressed` (GtkConsole)

**Files to Fix**:
```
pycam/Plugins/ParallelProcessing.py
pycam/Plugins/Fonts.py  
pycam/Plugins/MemoryAnalyzer.py
pycam/Plugins/ModelScaling.py
pycam/Plugins/ModelPosition.py
pycam/Plugins/Log.py
pycam/Plugins/GtkConsole.py
```

#### Task 2: Container Method Migration
**Problem**: GTK 4 container API changes
- `container.add()` → `container.append()` (ToolpathCrop)
- `container.remove()` → PopoverMenu specific removal methods (OpenGLWindow)

**Files to Fix**:
```
pycam/Plugins/ToolpathCrop.py
pycam/Plugins/OpenGLWindow.py
```

#### Task 3: Image Widget API Changes  
**Problem**: GTK 4 Image widget changes
- `Image.get_pixbuf()` → new GTK 4 texture/paintable API (ModelExtrusion)

**Files to Fix**:
```
pycam/Plugins/ModelExtrusion.py
```

### Medium Priority: Dependency Chain Recovery

#### Task 4: OpenGL Plugin Chain
**Problem**: OpenGL plugins disabled due to OpenGLWindow dependency failure
- Fix OpenGLWindow first (Task 2 issue)
- This will enable: OpenGLViewGrid, OpenGLViewDimension, OpenGLViewToolpath, OpenGLViewBounds
- Secondary: ToolpathSimulation (depends on OpenGLViewToolpath)

#### Task 5: Model Support Chain
**Problem**: ModelSupportGrid disabled due to ModelSupport dependency
- Need to identify and fix ModelSupport plugin issues
- This will restore 3D model support functionality

### Low Priority: Enhanced Features

#### Task 6: Advanced UI Polish
- Fix any remaining GTK builder warnings
- Optimize 3D visualization performance  
- Test complete CAM workflows (model → toolpath → export)

#### Task 7: Modern GTK 4 Features
- Implement GTK 4 native styling
- Add adaptive layouts for different screen sizes
- Utilize GTK 4 performance optimizations

## Implementation Strategy

### Quick Wins (1-2 hours each)
1. **Signal Migration** - Search/replace deprecated signals in plugin files
2. **Container Methods** - Update add()/remove() calls to append()/etc.
3. **Image API** - Migrate pixbuf usage to new paintable system

### Critical Path (OpenGL Recovery)
1. Fix OpenGLWindow container issues → enables 4+ OpenGL plugins
2. Fix ModelSupport plugin → enables ModelSupportGrid
3. Test complete 3D visualization workflow

## Technical Changes Summary

### Completed API Migrations
| GTK 2/3 Component | GTK 4 Replacement | Status |
|-------------------|-------------------|--------|
| `GtkAction` | `GSimpleAction` | ✅ Complete |
| `UIManager` | `GMenu` | ✅ Complete |
| `delete-event` | `close-request` | 🔄 Needs plugin fixes |
| `gtk.gtkgl` | `Gtk.GLArea` | ✅ Complete |
| `GtkWindow` | `GtkApplicationWindow` | ✅ Complete |
| Stock icons | Named icons | ✅ Complete |
| UI File Properties | GTK 4 properties | ✅ Complete |

### Current Plugin Status
- **✅ Working**: Core plugins (16), basic functionality
- **🚧 Fixable**: 13 plugins with known GTK 4 API issues  
- **📋 Blocked**: 6 plugins waiting for dependency fixes

## How to Test

```bash
# Run PyCAM with current GTK 4 support
.venv/bin/python -m pycam.run_gui

# Expected: Application launches, core tabs visible, file operations work
# Issues: "Skipping problematic plugin" messages for specific GTK 4 incompatibilities
```

## Success Metrics

**Current Status**: ✅ Core migration complete, application functional
**Remaining Work**: Fix specific plugin GTK 4 compatibility issues
**Timeline**: Most issues are straightforward API updates (1-4 hours each)

---

*Last Updated: 2025-09-02 - Core GTK 4 migration complete, focusing on plugin compatibility*

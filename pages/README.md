# Pages 目录结构说明

本目录采用**混合方案**组织 Page Object 模式的页面对象。

## 📁 目录结构

```
pages/
├── base_page.py              # 基础页面类（所有页面继承）
│
├── components/               # 可复用组件
│   └── __init__.py          # 未来可添加：header.py, modal.py 等
│
├── common/                   # 通用页面（不属于特定业务模块）
│   ├── __init__.py
│   ├── login/               # 登录模块
│   │   └── login_page.py
│   └── search_page.py       # 搜索页面
│
└── modules/                  # 业务模块
    ├── __init__.py
    │
    ├── blood/               # 血常规模块
    │   ├── __init__.py
    │   └── blood_entry_page.py    # 血常规录入页
    │   # 未来可扩展：
    │   # ├── blood_history_page.py  # 历史记录页
    │   # └── blood_report_page.py   # 报告查看页
    │
    └── mar/                 # 用药记录模块
        ├── __init__.py
        └── mar_page.py      # 用药记录页
```

## 📖 使用指南

### 导入规则

```python
# 基础类
from pages.base_page import BasePage

# 通用页面
from pages.common.login.login_page import LoginPage
from pages.common.search_page import SearchPage

# 业务模块页面
from pages.modules.blood.blood_entry_page import BloodEntryPage
from pages.modules.mar.mar_page import MarPage

# 组件（未来）
# from pages.components.header import HeaderComponent
```

### 命名规范

1. **文件命名**：小写+下划线，描述页面功能
   - `blood_entry_page.py` - 血常规录入页
   - `blood_history_page.py` - 血常规历史页

2. **类命名**：大驼峰，后缀 `Page` 或 `Component`
   - `BloodEntryPage` - 页面类
   - `HeaderComponent` - 组件类

3. **模块目录**：小写，描述业务领域
   - `blood/` - 血常规模块
   - `urine/` - 尿常规模块

## 🔧 扩展指南

### 添加新的业务模块

例如：添加"尿常规"模块

```bash
# 1. 创建模块目录
mkdir -p pages/modules/urine

# 2. 创建 __init__.py
touch pages/modules/urine/__init__.py

# 3. 创建页面文件
# pages/modules/urine/urine_entry_page.py
```

```python
# pages/modules/urine/urine_entry_page.py
from pages.base_page import BasePage

class UrineEntryPage(BasePage):
    """尿常规录入页面"""
    pass
```

### 添加可复用组件

例如：添加"日期选择器"组件

```python
# pages/components/date_picker.py
from pages.base_page import BasePage

class DatePickerComponent(BasePage):
    """日期选择器组件（多模块共用）"""

    DATE_INPUT = "#date"
    CALENDAR_ICON = ".calendar-icon"

    def select_date(self, date: str):
        self.fill(self.DATE_INPUT, date)
```

### 添加通用页面

例如：添加"首页"

```python
# pages/common/home_page.py
from pages.base_page import BasePage

class HomePage(BasePage):
    """首页"""
    pass
```

## 🎯 设计原则

### 1. **components/** - 放什么？
- 多个页面共用的 UI 组件
- 不是完整页面，而是页面的一部分
- 例如：头部、侧边栏、弹窗、表单字段

### 2. **common/** - 放什么？
- 通用的完整页面
- 不属于特定业务模块
- 例如：登录、首页、搜索、个人设置

### 3. **modules/** - 放什么？
- 业务模块的页面
- 按业务功能分组
- 每个模块独立发展，互不影响

### 4. 如何处理跨模块功能？

如果某个功能在多个模块中使用：

```
❌ 不推荐：放在某个模块内
pages/modules/blood/result_analysis_page.py

✅ 推荐：提取到 common 或新建独立模块
pages/common/result_analysis_page.py
# 或者
pages/modules/analysis/result_analysis_page.py
```

### 5. 避免循环依赖

```python
# ✅ 正确：子模块依赖 base 和 components
from pages.base_page import BasePage
from pages.components.date_picker import DatePickerComponent

# ❌ 错误：模块之间互相导入
from pages.modules.blood.blood_page import BloodPage  # 在 mar_page.py 中
```

## 🔄 重构历史

- **2025-12-25**：重构为混合方案
  - 创建 `components/`, `common/`, `modules/` 目录
  - 移动 `login/` → `common/login/`
  - 移动 `search_page.py` → `common/search_page.py`
  - 移动 `blood/` → `modules/blood/`
  - 移动 `mar/` → `modules/mar/`
  - 重命名 `blood_page.py` → `blood_entry_page.py`
  - 重命名类 `BloodPage` → `BloodEntryPage`

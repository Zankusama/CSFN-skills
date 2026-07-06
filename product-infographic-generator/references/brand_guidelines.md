# 蔡氏福宁品牌设计规范

## 1. 品牌色系（严禁偏离）

### 主品牌色

**PANTONE 1645C 亮橙红**

| 用途 | 色值 | 说明 |
|------|------|------|
| 主品牌色 | `#E85A24` | 严禁使用 `#87032` 等错误色值 |
| 品牌深色 | `#C24518` | 用于hover状态、深色背景 |
| 品牌浅色 | `#F07846` | 用于渐变、浅色背景 |
| 品牌柔和色 | `#F5A080` | 用于图标、装饰元素 |
| 品牌极浅色 | `#FEF0EC` | 用于浅底块背景 |

### 文字色系

| 用途 | 色值 | 说明 |
|------|------|------|
| 主文字色 | `#2a2018` | 暖墨色，用于标题和正文 |
| 次要文字色 | `#6b5e54` | 用于副标题、说明文字 |
| 浅色文字 | `#a89888` | 用于禁用状态、占位符 |

### 背景色系

| 用途 | 色值 | 说明 |
|------|------|------|
| 宣纸白 | `#faf8f2` | 页面主背景 |
| 暖宣纸白 | `#f5f0e6` | 卡片背景、浅底块 |

### 辅助色系（全部暖调，禁用冷色）

| 用途 | 色值 | 说明 |
|------|------|------|
| 暖金色 | `#d4a648` | 装饰线条、图标 |
| 暖绿色 | `#7a9a5b` | 成功状态、positive标识 |
| 暖青色 | `#5ba4a4` | 信息状态、链接 |
| 边框色 | `#e0d5c0` | 卡片边框 |
| 分割线色 | `#e8e0d0` | 分割线 |

### 竞品配色（暖调区分，禁用冷蓝/冷绿）

| 品牌 | 主色 | 浅底色 | 说明 |
|------|------|--------|------|
| 蔡氏福宁 | `#E85A24` | `#FEF0EC` | 品牌橙红 |
| 花王 | `#5a7a5a` | `#e8f0e8` | 暖墨绿（禁用冷蓝） |
| 珍视明 | `#6b8e6b` | `#e8f0e8` | 暖橄榄绿（禁用冷绿） |
| 海氏海诺 | `#8b6f47` | `#f0e8d8` | 暖棕色（禁用冷灰） |

## 2. Logo使用规范

### 标准Logo文件

**文件路径**：`/Users/zankus/标准文件/设计标准文件/蔡氏福宁无底色 logo.png`

**特性**：白色透明底，适合深色或彩色背景

### Logo嵌入方案

#### 方案A：绝对路径（推荐）

```html
<img src="/Users/zankus/标准文件/设计标准文件/蔡氏福宁无底色 logo.png" alt="蔡氏福宁" class="header-logo" />
```

**优点**：路径固定，不会出错
**缺点**：文件路径较长

#### 方案B：相对路径（备用）

1. 复制logo到HTML同目录：
   ```bash
   cp /Users/zankus/标准文件/设计标准文件/蔡氏福宁无底色\ logo.png ./logo.png
   ```

2. HTML中引用：
   ```html
   <img src="logo.png" alt="蔡氏福宁" class="header-logo" />
   ```

**优点**：路径简洁
**缺点**：需要额外复制文件

### Logo样式规范

**头部Logo**：
- 位置：右上角
- 高度：40px
- 透明度：0.9
- 鼠标悬停：透明度1.0

**底部Logo**：
- 位置：居中
- 高度：30px
- 透明度：0.7

**CSS示例**：
```css
.header-logo {
  position: absolute;
  right: 40px;
  top: 50%;
  transform: translateY(-50%);
  height: 40px;
  opacity: 0.9;
}

.footer-logo {
  height: 30px;
  opacity: 0.7;
}
```

## 3. 设计风格规范

### 整体风格

**宣纸风 + 暖调 + 中国风元素**

### 字体规范

| 用途 | 字体 | 备用字体 |
|------|------|----------|
| 标题 | Noto Serif SC | "Songti SC", "SimSun", serif |
| 正文 | Noto Sans SC | "PingFang SC", "Microsoft YaHei", sans-serif |
| 代码 | Monaco | "Menlo", "Consolas", monospace |

**CSS示例**：
```css
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&family=Noto+Serif+SC:wght@400;600;700&display=swap');

h1, h2, h3 {
  font-family: 'Noto Serif SC', serif;
}

body, p, div {
  font-family: 'Noto Sans SC', sans-serif;
}
```

### 排版规范

| 元素 | 规范 |
|------|------|
| 页面宽度 | 1200px居中 |
| 卡片圆角 | 6px |
| 卡片边框 | `1px solid #d8cfc4` |
| 卡片阴影 | `0 2px 8px rgba(42,32,24,0.08)` |
| Section标题 | 左侧4px竖线 + 深色文字 |
| 板块间距 | 60px |
| 卡片间距 | 20px |

### 中国风元素

- **宣纸纹理背景**：`#faf8f2`
- **金色装饰线条**：`#d4a648`
- **传统色彩**：朱红、石青、石绿（全部暖调化）
- **竖排文字**：必要时可使用竖排（如"新品上市"标签）

## 4. 内容规范（严禁瞎编）

### 必须从brief中提取

- **产品定位、卖点、参数** → 从brief"产品层"提取
- **竞品信息** → 从brief"市场层"提取
- **人群场景** → 从brief"利益层"提取
- **口播文案** → 从brief"心智层"提取

### 禁止行为

❌ **编造brief中不存在的信息**
- 错误示例："药店渠道"、"下沉市场"（这些内容你从没说过）

❌ **使用拼音代替中文品牌名**
- 错误示例："CAISHIFUNING"
- 正确示例："蔡氏福宁"

❌ **主观评判竞品优劣**
- 错误示例："花王品质最好"、"海氏海诺最差"
- 正确做法：只做客观参数对比

❌ **使用冷色调**
- 错误示例：冷蓝色 `#4a90d9`、冷绿色 `#2ecc71`
- 正确做法：全部使用暖色调

## 5. HTML模板结构

### 产品一页纸结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>{产品名} - 产品一页纸</title>
  <style>
    /* CSS变量定义 */
    :root {
      --brand: #E85A24;
      /* ... 其他变量 ... */
    }
    
    /* 基础样式 */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Noto Sans SC', sans-serif; background: var(--paper); color: var(--ink); }
    
    /* 头部样式 */
    .header { background: linear-gradient(135deg, var(--brand) 0%, var(--brand-dark) 100%); }
    
    /* Section标题样式 */
    .section-title { border-left: 4px solid var(--brand); }
    
    /* 卡片样式 */
    .card { background: white; border: 1px solid #d8cfc4; border-radius: 6px; box-shadow: 0 2px 8px rgba(42,32,24,0.08); }
  </style>
</head>
<body>
  <!-- 头部 -->
  <div class="header">
    <h1>{产品口号}</h1>
    <img src="logo.png" alt="蔡氏福宁" class="header-logo" />
  </div>
  
  <!-- 内容板块 -->
  <div class="section">
    <h2 class="section-title">板块标题</h2>
    <div class="card">卡片内容</div>
  </div>
  
  <!-- 底部 -->
  <div class="footer">
    <img src="logo.png" alt="蔡氏福宁" class="footer-logo" />
  </div>
</body>
</html>
```

### 竞品对比结构

与产品一页纸结构基本一致，但增加：
- 竞品配色区分（各竞品用不同暖色调）
- 对比表格（多维度横向对比）
- 客观描述（不做主观评判）

## 6. 常见问题

### Q1: 品牌色显示不正确怎么办？

**检查清单**：
1. 确认色值是否为 `#E85A24`（不是 `#87032`）
2. 确认CSS变量名是否为 `--brand`
3. 确认是否有其他样式覆盖

### Q2: Logo无法显示怎么办？

**解决方案**：
1. 检查文件路径是否正确
2. 尝试方案A（绝对路径）
3. 尝试方案B（相对路径，需复制logo文件）

### Q3: 配色不协调怎么办？

**检查清单**：
1. 确认没有使用冷色调（蓝、冷绿、冷灰）
2. 确认所有辅助色都在暖色相环内
3. 参考"竞品配色"表格使用正确的暖调色值

### Q4: 内容不准确怎么办？

**解决方案**：
1. 所有内容必须从brief中提取
2. 如果brief中没有相关信息，询问用户
3. 严禁编造信息

## 7. 更新日志

- **2026-07-03**: 初始版本，基于蔡氏福宁蒸汽眼罩信息图项目整理

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_infographic.py — 蔡氏福宁产品信息图生成器

读取 markdown 中间文件，解析结构，填充 HTML 模板，输出信息图。
用法：
  python3 generate_infographic.py <brief_md> <输出目录>

依赖：
  - assets/product-one-pager-template.html
  - assets/competitor-comparison-template.html
  - assets/logo.png (由调用方复制到输出目录)

设计原则：
  - 所有内容严格来自 markdown（防编造/防上下文污染）
  - 动态板块（SKU/场景/FAQ/参数/雷达维度）按实际数量生成
  - 占位符一一对应，无残留
"""
import os
import re
import sys
import json


def parse_md(path):
    """解析 markdown 为嵌套字典 {h2: {h3: {key: val/list}}}"""
    with open(path, encoding='utf-8') as f:
        lines = f.read().split('\n')
    data = {}
    cur_h2 = None
    cur_h3 = None
    for line in lines:
        if line.startswith('## '):
            cur_h2 = line[3:].strip()
            data[cur_h2] = {}
            cur_h3 = None
        elif line.startswith('### '):
            cur_h3 = line[4:].strip()
            if cur_h2 is not None:
                data[cur_h2][cur_h3] = {}
        elif line.startswith('- '):
            content = line[2:].strip()
            if '：' in content:
                k, v = content.split('：', 1)
                k, v = k.strip(), v.strip()
            else:
                k, v = None, content
            if cur_h2 is not None and cur_h3 is not None:
                d = data[cur_h2][cur_h3]
                if k:
                    d[k] = v
                else:
                    d.setdefault('_bullets', []).append(v)
            elif cur_h2 is not None:
                d = data[cur_h2]
                if k:
                    if k in d:
                        if not isinstance(d[k], list):
                            d[k] = [d[k]]
                        d[k].append(v)
                    else:
                        d[k] = v
                else:
                    d.setdefault('_bullets', []).append(v)
        elif line.strip() and not line.startswith('#'):
            txt = line.strip()
            if cur_h2 is not None and cur_h3 is not None:
                d = data[cur_h2][cur_h3]
                d['_text'] = (d.get('_text', '') + '\n' + txt).strip()
            elif cur_h2 is not None:
                d = data[cur_h2]
                d['_text'] = (d.get('_text', '') + '\n' + txt).strip()
    return data


def find_h2(data, prefix):
    for k in data:
        if k.startswith(prefix):
            return k
    return None


def bullet_list(items):
    return '\n'.join(f'    <li>{x}</li>' for x in items)


def fill_one_pager(template, md_path):
    d = parse_md(md_path)
    name_h2 = find_h2(d, '产品名称')
    slogan_h2 = find_h2(d, '产品口号')
    pod_h2 = find_h2(d, '核心卖点')
    spec_h2 = find_h2(d, '产品规格')
    usage_h2 = find_h2(d, '使用方法')
    suit_h2 = find_h2(d, '适用人群')
    forbid_h2 = find_h2(d, '禁忌人群')
    warn_h2 = find_h2(d, '注意事项')
    sku_h2 = find_h2(d, '产品系列')
    scene_h2 = find_h2(d, '使用场景')
    copy_h2 = find_h2(d, '口播文案')
    faq_h2 = find_h2(d, '常见问题')

    rep = {}
    rep['{产品名}'] = d.get(name_h2, {}).get('_text', '') or d.get(name_h2, {}).get('', '')
    # 产品名称可能是 h2 下的 _text 或 h2 本身的键
    if not rep['{产品名}']:
        # h2 key 就是 "产品名称"，内容在 _text
        rep['{产品名}'] = d.get(name_h2, {}).get('_text', '')
    rep['{产品口号}'] = d.get(slogan_h2, {}).get('_text', '')

    # POD
    pod_sec = d.get(pod_h2, {})
    for i in range(1, 5):
        # h3 形如 "POD1" / "POD1 xxx"
        h3 = None
        for k in pod_sec:
            if k.startswith(f'POD{i}'):
                h3 = k
                break
        pd = pod_sec.get(h3, {}) if h3 else {}
        rep[f'{{POD{i}标题}}'] = pd.get('标题', '')
        rep[f'{{POD{i}特征}}'] = pd.get('特征', '')
        rep[f'{{POD{i}优势}}'] = pd.get('优势', '')
        rep[f'{{POD{i}利益}}'] = pd.get('利益', '')
        rep[f'{{POD{i}vs竞品}}'] = pd.get('vs竞品', '')

    # 列表类
    rep['{规格列表}'] = bullet_list(d.get(spec_h2, {}).get('_bullets', []))
    rep['{使用方法列表}'] = bullet_list(d.get(usage_h2, {}).get('_bullets', []))
    rep['{适用人群列表}'] = bullet_list(d.get(suit_h2, {}).get('_bullets', []))
    rep['{禁忌人群列表}'] = bullet_list(d.get(forbid_h2, {}).get('_bullets', []))
    rep['{注意事项列表}'] = bullet_list(d.get(warn_h2, {}).get('_bullets', []))

    # SKU
    if sku_h2:
        sku_sec = d.get(sku_h2, {})
        # 提取区分维度
        m = re.search(r'SKU区分维度[:：]\s*(.+)', sku_h2)
        rep['{SKU区分维度}'] = m.group(1).strip() if m else '产品系列'
        for i in range(1, 6):
            h3 = None
            for k in sku_sec:
                if k.startswith(f'SKU{i}'):
                    h3 = k
                    break
            sd = sku_sec.get(h3, {}) if h3 else {}
            rep[f'{{SKU{i}名称}}'] = sd.get('名称', '')
            rep[f'{{SKU{i}描述}}'] = sd.get('描述', '')
    else:
        rep['{SKU区分维度}'] = '产品系列'
        for i in range(1, 6):
            rep[f'{{SKU{i}名称}}'] = ''
            rep[f'{{SKU{i}描述}}'] = ''

    # 场景
    if scene_h2:
        scene_sec = d.get(scene_h2, {})
        for i in range(1, 6):
            h3 = None
            for k in scene_sec:
                if k.startswith(f'场景{i}'):
                    h3 = k
                    break
            sd = scene_sec.get(h3, {}) if h3 else {}
            rep[f'{{场景{i}图标}}'] = sd.get('图标', '•')
            rep[f'{{场景{i}标题}}'] = sd.get('标题', '')
            rep[f'{{场景{i}描述}}'] = sd.get('描述', '')
    else:
        for i in range(1, 6):
            rep[f'{{场景{i}图标}}'] = '•'
            rep[f'{{场景{i}标题}}'] = ''
            rep[f'{{场景{i}描述}}'] = ''

    # 口播
    rep['{口播文案}'] = d.get(copy_h2, {}).get('_text', '')

    # FAQ
    if faq_h2:
        faq_sec = d.get(faq_h2, {})
        for i in range(1, 9):
            h3 = None
            for k in faq_sec:
                if k.startswith(f'FAQ{i}'):
                    h3 = k
                    break
            fd = faq_sec.get(h3, {}) if h3 else {}
            rep[f'{{Q{i}}}'] = fd.get('Q', '')
            rep[f'{{A{i}}}'] = fd.get('A', '')
    else:
        for i in range(1, 9):
            rep[f'{{Q{i}}}'] = ''
            rep[f'{{A{i}}}'] = ''

    out = template
    for k, v in rep.items():
        out = out.replace(k, str(v))
    return out


def fill_competitor(template, md_path):
    d = parse_md(md_path)
    pos_h2 = find_h2(d, '竞品定位')
    dim_h2 = find_h2(d, '核心参数维度')
    radar_dim_h2 = find_h2(d, '雷达图维度')
    radar_score_h2 = find_h2(d, '雷达图打分')
    concl_h2 = find_h2(d, '核心结论')

    rep = {}

    # 竞品定位
    pos_sec = d.get(pos_h2, {})
    brand_order = ['蔡氏福宁', '珍视明', '花王', '海氏海诺']
    brand_display = {
        '蔡氏福宁': '蔡氏福宁',
        '珍视明': '珍视明',
        '花王': '花王（美舒律）',
        '海氏海诺': '海氏海诺',
    }
    # 竞品1/2/3 = 后三个
    comp_short = brand_order[1:]  # 珍视明, 花王, 海氏海诺
    for i, b in enumerate(brand_order, 1):
        # 找 h3 以 b 开头
        h3 = None
        for k in pos_sec:
            if k.startswith(b):
                h3 = k
                break
        pd = pos_sec.get(h3, {}) if h3 else {}
        if i == 1:
            rep['{品牌名}'] = brand_display.get(b, b)
            rep['{品牌定位描述}'] = pd.get('定位', '') + '；' + pd.get('核心', '')
        else:
            rep[f'{{竞品{i-1}名称}}'] = brand_display.get(b, b)
            rep[f'{{竞品{i-1}定位描述}}'] = pd.get('定位', '') + '；' + pd.get('核心', '')

    rep['{产品名称}'] = '蔡氏福宁·蒸汽眼罩'  # 由调用方覆盖

    # 核心参数维度 → 参数卡片区
    dim_sec = d.get(dim_h2, {})
    dims = []
    for k in dim_sec:
        if k.startswith('维度'):
            m = re.search(r'维度\d+[：:]\s*(.+)', k)
            dim_name = m.group(1).strip() if m else k
            dims.append((k, dim_name, dim_sec[k]))
    # 构建参数卡片：每品牌一张，每行一个维度
    cards = []
    for bi, b in enumerate(brand_order):
        cls = 'brand' if bi == 0 else f'c{bi}'
        marker = '●' if bi == 0 else '○'
        rows = []
        for (_, dim_name, dim_content) in dims:
            val = dim_content.get(b, '')
            if not val:
                # 尝试从 bullets 找
                for bl in dim_content.get('_bullets', []):
                    if bl.startswith(b):
                        val = bl.split('：', 1)[1] if '：' in bl else bl
                        break
            rows.append(f'      <div class="param-row"><span class="param-label">{dim_name}</span><span class="param-val">{val}</span></div>')
        card = f'    <div class="param-card {cls}">\n      <h4>{marker} {brand_display.get(b, b)}</h4>\n' + '\n'.join(rows) + '\n    </div>'
        cards.append(card)
    rep['{参数卡片区}'] = '\n'.join(cards)

    # 维度对比区（左/右）：展示全部核心参数维度简要对比
    dim_cards = []
    for idx, (_, dim_name, dim_content) in enumerate(dims, 1):
        parts = []
        for b in brand_order:
            val = dim_content.get(b, '')
            if not val:
                for bl in dim_content.get('_bullets', []):
                    if bl.startswith(b):
                        val = bl.split('：', 1)[1] if '：' in bl else bl
                        break
            cls = 'b-brand' if b == '蔡氏福宁' else f'b-c{brand_order.index(b)}'
            parts.append(f'<span class="{cls}">{brand_display.get(b, b)}</span>：{val}')
        p = '；'.join(parts)
        dim_cards.append(f'      <div class="dim-card">\n        <h4>{"①②③④⑤⑥⑦⑧"[idx-1]} {dim_name}</h4>\n        <p>{p}</p>\n      </div>')
    mid = (len(dim_cards) + 1) // 2
    rep['{维度对比区-左}'] = '\n'.join(dim_cards[:mid])
    rep['{维度对比区-右}'] = '\n'.join(dim_cards[mid:])

    # 雷达图：维度 + 打分
    radar_dims = []
    rsec = d.get(radar_dim_h2, {})
    # 雷达图维度可能是 _bullets 列表 "1. xxx"
    bullets = rsec.get('_bullets', [])
    for bl in bullets:
        m = re.sub(r'^\d+[.、]\s*', '', bl).strip()
        if m:
            radar_dims.append(m)
    # 若 bullets 空，尝试从 _text
    if not radar_dims and '_text' in rsec:
        for line in rsec['_text'].split('\n'):
            m = re.sub(r'^\d+[.、]\s*', '', line).strip()
            if m:
                radar_dims.append(m)

    rep['{雷达标签}'] = json.dumps(radar_dims, ensure_ascii=False)

    # 打分
    ssec = d.get(radar_score_h2, {})
    score_text = ssec.get('_text', '')
    # 解析 "- 品牌：[...]"
    score_map = {}
    for line in score_text.split('\n'):
        line = line.strip()
        m = re.match(r'-\s*(.+?)[：:]\s*\[(.+?)\]', line)
        if m:
            brand = m.group(1).strip()
            arr = [float(x) for x in m.group(2).split(',')]
            score_map[brand] = arr
    rep['{雷达数据-品牌}'] = json.dumps(score_map.get('蔡氏福宁', []), ensure_ascii=False)
    rep['{雷达数据-竞品1}'] = json.dumps(score_map.get('珍视明', []), ensure_ascii=False)
    rep['{雷达数据-竞品2}'] = json.dumps(score_map.get('花王', []), ensure_ascii=False)
    rep['{雷达数据-竞品3}'] = json.dumps(score_map.get('海氏海诺', []), ensure_ascii=False)

    # 核心结论
    rep['{核心结论内容}'] = d.get(concl_h2, {}).get('_text', '')

    out = template
    for k, v in rep.items():
        out = out.replace(k, str(v))
    return out


def main():
    if len(sys.argv) < 2:
        print("用法: python3 generate_infographic.py <输出目录>")
        sys.exit(1)
    out_dir = sys.argv[1]
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets = os.path.join(skill_dir, 'assets')

    one_tpl = open(os.path.join(assets, 'product-one-pager-template.html'), encoding='utf-8').read()
    comp_tpl = open(os.path.join(assets, 'competitor-comparison-template.html'), encoding='utf-8').read()

    import glob
    one_mds = glob.glob(os.path.join(out_dir, '*_信息图内容.md'))
    comp_mds = glob.glob(os.path.join(out_dir, '*_竞品对比内容.md'))

    for one_md in one_mds:
        base = os.path.basename(one_md).replace('_信息图内容.md', '')
        html = fill_one_pager(one_tpl, one_md)
        # 从 markdown 提取产品名兜底
        d = parse_md(one_md)
        nm = find_h2(d, '产品名称')
        pname = d.get(nm, {}).get('_text', '') if nm else ''
        if pname:
            html = html.replace('{产品名}', pname)
        with open(os.path.join(out_dir, f'{base}-产品一页纸.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ 产品一页纸生成完成: {base}-产品一页纸.html")

    for comp_md in comp_mds:
        base = os.path.basename(comp_md).replace('_竞品对比内容.md', '')
        html = fill_competitor(comp_tpl, comp_md)
        d = parse_md(comp_md)
        nm = find_h2(d, '产品名称')
        pname = d.get(nm, {}).get('_text', '') if nm else ''
        if pname:
            html = html.replace('{产品名称}', pname)
        # 竞品名兜底（通用）
        pos_h2 = find_h2(d, '竞品定位')
        if pos_h2:
            pos_sec = d.get(pos_h2, {})
            brands = [k for k in pos_sec if k.startswith(('蔡氏福宁', '珍视明', '花王', '海氏海诺', '守', '真', '元', '气'))]
        with open(os.path.join(out_dir, f'{base}-竞品对比.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ 竞品对比生成完成: {base}-竞品对比.html")


if __name__ == '__main__':
    main()

"""
🧠 Mind Map Generator - مولّد الخرائط الذهنية v2.0
يستخدم D3.js مباشرة - أكثر استقراراً
"""
import json
import re
from typing import Dict, Any


class MindMapGenerator:
    """مولّد الخرائط الذهنية بـ D3.js"""

    MAP_STYLES = {
        "colorful": {
            "name": "🎨 ملوّن",
            "description": "ألوان زاهية متنوعة",
            "colors": ["#FF6B6B", "#4ECDC4", "#45B7D1",
                       "#FFA07A", "#98D8C8", "#F7DC6F",
                       "#BB8FCE", "#85C1E2"]
        },
        "ocean": {
            "name": "🌊 محيط",
            "description": "درجات الأزرق",
            "colors": ["#1A5490", "#2E86AB", "#3FA7D6",
                       "#59C9E5", "#7BD3EA", "#A8DADC",
                       "#457B9D", "#1D3557"]
        },
        "sunset": {
            "name": "🌅 غروب",
            "description": "ألوان دافئة",
            "colors": ["#F94144", "#F3722C", "#F8961E",
                       "#F9844A", "#F9C74F", "#90BE6D",
                       "#43AA8B", "#577590"]
        },
        "forest": {
            "name": "🌲 غابة",
            "description": "درجات الأخضر",
            "colors": ["#1B4332", "#2D6A4F", "#40916C",
                       "#52B788", "#74C69D", "#95D5B2",
                       "#B7E4C7", "#D8F3DC"]
        },
        "professional": {
            "name": "💼 احترافي",
            "description": "ألوان رسمية",
            "colors": ["#003049", "#264653", "#2A9D8F",
                       "#457B9D", "#1D3557", "#6C757D",
                       "#495057", "#343A40"]
        },
        "neon": {
            "name": "💫 نيون",
            "description": "ألوان زاهية على خلفية داكنة",
            "colors": ["#FF00FF", "#00FFFF", "#FFFF00",
                       "#FF6B6B", "#4ECDC4", "#95E1D3",
                       "#FCE38A", "#F38181"]
        }
    }

    DEPTH_LEVELS = {
        "simple":   {"name": "🟢 بسيط",  "depth": 2, "branches": 4},
        "medium":   {"name": "🟡 متوسط", "depth": 3, "branches": 5},
        "detailed": {"name": "🔴 مفصل", "depth": 4, "branches": 7},
    }

    def __init__(self, ai_engine):
        self.ai = ai_engine

    # ─────────────────────────────────────────
    def generate(
        self,
        text: str,
        depth_level: str = "medium",
        style: str = "colorful"
    ) -> Dict[str, Any]:
        """توليد خريطة ذهنية"""

        if not text or len(text.strip()) < 50:
            return {
                'success': False,
                'data': {},
                'markdown': '',
                'error': 'النص قصير جداً!'
            }

        depth_info = self.DEPTH_LEVELS.get(depth_level, self.DEPTH_LEVELS['medium'])

        max_chars = 4000
        text_to_use = text[:max_chars] + "..." if len(text) > max_chars else text

        prompt = self._build_prompt(text_to_use, depth_info)

        try:
            response = self.ai.answer_question(context="", question=prompt)
            data = self._parse_response(response)

            if not data:
                simple_prompt = self._build_simple_prompt(text_to_use)
                response2 = self.ai.answer_question(context="", question=simple_prompt)
                data = self._parse_response(response2)

            if not data:
                data = self._create_fallback_map(text_to_use)

            markdown = self._convert_to_markdown(data)

            return {
                'success': True,
                'data': data,
                'markdown': markdown,
                'style': style,
                'error': None
            }

        except Exception as e:
            return {
                'success': False,
                'data': {},
                'markdown': '',
                'error': f'خطأ: {str(e)}'
            }

    # ─────────────────────────────────────────
    def _build_prompt(self, text: str, depth_info: dict) -> str:
        depth = depth_info['depth']
        branches = depth_info['branches']

        return f"""أنت خبير في تنظيم المعلومات.

المحتوى:
\"\"\"
{text}
\"\"\"

اعمل خريطة ذهنية للمحتوى.

التعليمات:
- استخرج الموضوع الرئيسي (العنوان)
- اعمل {branches} فروع رئيسية على الأكثر
- كل فرع له {depth} مستويات تفرع
- العناوين قصيرة (كلمة لـ 4 كلمات)
- ركّز على الأفكار المهمة

الرد JSON فقط:
{{
  "title": "الموضوع الرئيسي",
  "children": [
    {{
      "title": "الفرع الأول",
      "children": [
        {{
          "title": "تفصيل 1",
          "children": [
            {{"title": "نقطة فرعية", "children": []}}
          ]
        }},
        {{"title": "تفصيل 2", "children": []}}
      ]
    }},
    {{
      "title": "الفرع الثاني",
      "children": [
        {{"title": "تفصيل", "children": []}}
      ]
    }}
  ]
}}

مهم:
- ارجع JSON فقط
- العناوين بالعربي
- كلام قصير ومركز
- كل عنصر له children (لو فاضي اكتب [])"""

    def _build_simple_prompt(self, text: str) -> str:
        return f"""اعمل خريطة ذهنية من النص ده.

النص: {text[:2000]}

JSON فقط:
{{
  "title": "العنوان",
  "children": [
    {{"title": "فرع 1", "children": [{{"title": "نقطة", "children": []}}]}},
    {{"title": "فرع 2", "children": [{{"title": "نقطة", "children": []}}]}}
  ]
}}"""

    # ─────────────────────────────────────────
    def _parse_response(self, response: str) -> Dict:
        if not response:
            return {}

        # محاولة 1: JSON مباشر
        try:
            data = json.loads(response.strip())
            if self._validate_map(data):
                return self._ensure_children(data)
        except json.JSONDecodeError:
            pass

        # محاولة 2: استخراج JSON
        try:
            pattern = r'\{[\s\S]*"title"[\s\S]*\}'
            matches = re.findall(pattern, response)
            for match in matches:
                try:
                    data = json.loads(match)
                    if self._validate_map(data):
                        return self._ensure_children(data)
                except Exception:
                    continue
        except Exception:
            pass

        # محاولة 3: تنظيف backticks
        try:
            cleaned = response.strip()
            cleaned = re.sub(r'^```(?:json)?\s*', '', cleaned)
            cleaned = re.sub(r'\s*```$', '', cleaned)
            data = json.loads(cleaned)
            if self._validate_map(data):
                return self._ensure_children(data)
        except Exception:
            pass

        return {}

    def _validate_map(self, data: Any) -> bool:
        if not isinstance(data, dict):
            return False
        if 'title' not in data:
            return False
        return True

    def _ensure_children(self, node: Dict) -> Dict:
        """التأكد إن كل node عنده children list"""
        if 'children' not in node or not isinstance(node.get('children'), list):
            node['children'] = []
        for child in node['children']:
            if isinstance(child, dict):
                self._ensure_children(child)
        return node

    def _create_fallback_map(self, text: str) -> Dict:
        sentences = re.split(r'[.!?؟،\n]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10][:6]

        children = []
        for i, sent in enumerate(sentences[:5], 1):
            short = sent[:50] + "..." if len(sent) > 50 else sent
            children.append({
                "title": f"نقطة {i}",
                "children": [{"title": short, "children": []}]
            })

        return {
            "title": "الموضوع الرئيسي",
            "children": children
        }

    # ─────────────────────────────────────────
    def _convert_to_markdown(self, data: Dict, level: int = 0) -> str:
        if not data:
            return ""

        result = ""
        title = data.get('title', '').strip()

        if title:
            if level == 0:
                result += f"# {title}\n\n"
            else:
                indent = "  " * (level - 1)
                result += f"{indent}- {title}\n"

        children = data.get('children', [])
        for child in children:
            result += self._convert_to_markdown(child, level + 1)

        return result

    # ─────────────────────────────────────────
    def render_d3_mindmap(
        self,
        data: Dict,
        style: str = "colorful",
        height: int = 600
    ) -> str:
        """
        توليد HTML تفاعلي بـ D3.js (أكثر استقراراً من Markmap)
        """
        colors_data = self.MAP_STYLES.get(style, self.MAP_STYLES['colorful'])
        colors = colors_data['colors']

        # تحويل البيانات لـ JSON آمن
        data_json = json.dumps(data, ensure_ascii=False)
        colors_json = json.dumps(colors)

        # تحديد لون الخلفية حسب الستايل
        bg_color = "#1a1a2e" if style == "neon" else "#ffffff"
        text_color = "#ffffff" if style == "neon" else "#2c3e50"

        html = """<!DOCTYPE html>
<html dir="ltr">
<head>
<meta charset="UTF-8">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: 'Cairo', 'Segoe UI', Tahoma, sans-serif;
    background: """ + bg_color + """;
    overflow: hidden;
}
#mindmap-container {
    width: 100%;
    height: """ + str(height) + """px;
    position: relative;
    background: """ + bg_color + """;
    border-radius: 15px;
    overflow: hidden;
}
#mindmap-svg {
    width: 100%;
    height: 100%;
    cursor: grab;
}
#mindmap-svg:active { cursor: grabbing; }

.node circle {
    cursor: pointer;
    stroke: #fff;
    stroke-width: 2.5px;
    transition: all 0.3s ease;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
}
.node:hover circle {
    stroke-width: 4px;
    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
}
.node text {
    font-family: 'Cairo', sans-serif;
    font-size: 14px;
    font-weight: 600;
    fill: """ + text_color + """;
    pointer-events: none;
    user-select: none;
}
.node.collapsed circle {
    fill: #ddd !important;
}
.link {
    fill: none;
    stroke-opacity: 0.5;
    stroke-width: 2.5px;
    transition: stroke-opacity 0.3s;
}
.link:hover { stroke-opacity: 0.9; stroke-width: 3.5px; }

.controls {
    position: absolute;
    top: 15px;
    left: 15px;
    z-index: 100;
    display: flex;
    gap: 8px;
    background: rgba(255,255,255,0.95);
    padding: 8px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
.ctrl-btn {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 14px;
    cursor: pointer;
    font-size: 13px;
    font-weight: 600;
    font-family: 'Cairo', sans-serif;
    transition: all 0.3s;
}
.ctrl-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(102, 126, 234, 0.4);
}
.info-badge {
    position: absolute;
    bottom: 15px;
    right: 15px;
    background: rgba(0,0,0,0.75);
    color: white;
    padding: 8px 14px;
    border-radius: 10px;
    font-size: 12px;
    font-family: 'Cairo', sans-serif;
    z-index: 100;
    direction: rtl;
}
.title-banner {
    position: absolute;
    top: 15px;
    right: 15px;
    background: linear-gradient(135deg, #11998e, #38ef7d);
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
    font-family: 'Cairo', sans-serif;
    z-index: 100;
    box-shadow: 0 4px 15px rgba(17, 153, 142, 0.4);
}
</style>
<script src="https://d3js.org/d3.v7.min.js"></script>
</head>
<body>
<div id="mindmap-container">
    <div class="controls">
        <button class="ctrl-btn" onclick="zoomIn()">🔍+</button>
        <button class="ctrl-btn" onclick="zoomOut()">🔍−</button>
        <button class="ctrl-btn" onclick="resetZoom()">🎯 احتواء</button>
        <button class="ctrl-btn" onclick="expandAll()">📂 افتح الكل</button>
        <button class="ctrl-btn" onclick="collapseAll()">📁 اطوي الكل</button>
        <button class="ctrl-btn" onclick="downloadSVG()">📥 SVG</button>
    </div>

    <div class="title-banner">🧠 خريطة ذهنية تفاعلية</div>

    <svg id="mindmap-svg"></svg>

    <div class="info-badge">
        💡 اسحب للتحريك | اسكرول للتكبير | اضغط على نود للطي
    </div>
</div>

<script>
(function() {
    const treeData = __DATA_PLACEHOLDER__;
    const colors = __COLORS_PLACEHOLDER__;

    const container = document.getElementById('mindmap-container');
    const width = container.clientWidth;
    const height = """ + str(height) + """;

    let i = 0;
    const duration = 500;
    let root;

    // إعداد التخطيط الشجري
    const tree = d3.tree().nodeSize([45, 220]);

    // إعداد SVG
    const svg = d3.select("#mindmap-svg")
        .attr("viewBox", [0, 0, width, height])
        .attr("preserveAspectRatio", "xMidYMid meet");

    // إعداد الـ zoom
    const zoom = d3.zoom()
        .scaleExtent([0.1, 4])
        .on("zoom", (event) => {
            g.attr("transform", event.transform);
        });

    svg.call(zoom);

    // المجموعة الرئيسية
    const g = svg.append("g")
        .attr("transform", `translate(${width / 4}, ${height / 2})`);

    // تحضير البيانات
    root = d3.hierarchy(treeData, d => d.children);
    root.x0 = 0;
    root.y0 = 0;

    // طي العقد العميقة في البداية
    if (root.children) {
        root.children.forEach(collapseAtDepth);
    }

    function collapseAtDepth(d) {
        if (d.depth >= 2 && d.children) {
            d._children = d.children;
            d._children.forEach(collapseAtDepth);
            d.children = null;
        } else if (d.children) {
            d.children.forEach(collapseAtDepth);
        }
    }

    update(root);

    function update(source) {
        const treeData = tree(root);
        const nodes = treeData.descendants();
        const links = treeData.descendants().slice(1);

        // تحديث المواقع
        nodes.forEach(d => { d.y = d.depth * 200; });

        // ─── العقد ───
        const node = g.selectAll('g.node')
            .data(nodes, d => d.id || (d.id = ++i));

        const nodeEnter = node.enter().append('g')
            .attr('class', 'node')
            .attr("transform", d => `translate(${source.y0},${source.x0})`)
            .on('click', click);

        // الدوائر
        nodeEnter.append('circle')
            .attr('r', 1e-6)
            .style("fill", d => {
                if (d.depth === 0) return colors[0];
                return colors[d.depth % colors.length];
            });

        // النصوص
        nodeEnter.append('text')
            .attr("dy", ".35em")
            .attr("x", d => d.children || d._children ? -15 : 15)
            .attr("text-anchor", d => d.children || d._children ? "end" : "start")
            .text(d => d.data.title)
            .style("opacity", 0)
            .style("direction", "rtl");

        // التحديث
        const nodeUpdate = nodeEnter.merge(node);

        nodeUpdate.transition()
            .duration(duration)
            .attr("transform", d => `translate(${d.y},${d.x})`);

        nodeUpdate.select('circle')
            .attr('r', d => {
                if (d.depth === 0) return 12;
                if (d.depth === 1) return 9;
                return 7;
            })
            .style("fill", d => {
                if (d._children) return "#95a5a6";
                if (d.depth === 0) return colors[0];
                return colors[d.depth % colors.length];
            })
            .attr('class', d => d._children ? 'collapsed' : '');

        nodeUpdate.select('text')
            .transition()
            .duration(duration)
            .style("opacity", 1);

        // الإزالة
        const nodeExit = node.exit().transition()
            .duration(duration)
            .attr("transform", d => `translate(${source.y},${source.x})`)
            .remove();

        nodeExit.select('circle').attr('r', 1e-6);
        nodeExit.select('text').style('opacity', 0);

        // ─── الروابط ───
        const link = g.selectAll('path.link')
            .data(links, d => d.id);

        const linkEnter = link.enter().insert('path', "g")
            .attr("class", "link")
            .attr('d', d => {
                const o = {x: source.x0, y: source.y0};
                return diagonal(o, o);
            })
            .style("stroke", d => colors[d.depth % colors.length]);

        const linkUpdate = linkEnter.merge(link);

        linkUpdate.transition()
            .duration(duration)
            .attr('d', d => diagonal(d, d.parent));

        link.exit().transition()
            .duration(duration)
            .attr('d', d => {
                const o = {x: source.x, y: source.y};
                return diagonal(o, o);
            })
            .remove();

        // حفظ المواقع القديمة
        nodes.forEach(d => {
            d.x0 = d.x;
            d.y0 = d.y;
        });
    }

    // رسم الروابط المنحنية
    function diagonal(s, d) {
        return `M ${s.y} ${s.x}
                C ${(s.y + d.y) / 2} ${s.x},
                  ${(s.y + d.y) / 2} ${d.x},
                  ${d.y} ${d.x}`;
    }

    // الضغط للطي/الفتح
    function click(event, d) {
        if (d.children) {
            d._children = d.children;
            d.children = null;
        } else {
            d.children = d._children;
            d._children = null;
        }
        update(d);
    }

    // ─── الوظائف العامة ───
    window.zoomIn = function() {
        svg.transition().call(zoom.scaleBy, 1.3);
    };

    window.zoomOut = function() {
        svg.transition().call(zoom.scaleBy, 0.7);
    };

    window.resetZoom = function() {
        svg.transition().duration(500).call(
            zoom.transform,
            d3.zoomIdentity.translate(width / 4, height / 2).scale(0.85)
        );
    };

    window.expandAll = function() {
        root.each(d => {
            if (d._children) {
                d.children = d._children;
                d._children = null;
            }
        });
        update(root);
    };

    window.collapseAll = function() {
        root.each(d => {
            if (d.depth > 0 && d.children) {
                d._children = d.children;
                d.children = null;
            }
        });
        update(root);
    };

    window.downloadSVG = function() {
        const svgEl = document.getElementById('mindmap-svg');
        const serializer = new XMLSerializer();
        let source = serializer.serializeToString(svgEl);

        if (!source.match(/^<svg[^>]+xmlns="http\\:\\/\\/www\\.w3\\.org\\/2000\\/svg"/)) {
            source = source.replace(/^<svg/, '<svg xmlns="http://www.w3.org/2000/svg"');
        }

        const blob = new Blob([source], {type: 'image/svg+xml;charset=utf-8'});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'mindmap.svg';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    // تطبيق zoom افتراضي
    setTimeout(() => {
        resetZoom();
    }, 300);

})();
</script>
</body>
</html>"""

        # استبدال البيانات
        html = html.replace('__DATA_PLACEHOLDER__', data_json)
        html = html.replace('__COLORS_PLACEHOLDER__', colors_json)

        return html

    # ─────────────────────────────────────────
    def get_stats(self, data: Dict) -> Dict:
        stats = {
            'total_nodes': 0,
            'max_depth': 0,
            'branches': 0
        }

        def count_nodes(node, depth=0):
            stats['total_nodes'] += 1
            stats['max_depth'] = max(stats['max_depth'], depth)
            children = node.get('children', [])
            if depth == 1:
                stats['branches'] += 1
            for child in children:
                count_nodes(child, depth + 1)

        if data:
            count_nodes(data)

        return stats
"""
🧠 صفحة الخرائط الذهنية - شجرة تفاعلية بـ D3.js
"""
import streamlit as st
import streamlit.components.v1 as components
import json
from utils.plan_limits import check_plan_limit, increment_usage
from modules.auth.outputs_manager import (
    save_output, get_cached_output, save_lesson_output,
    get_lesson_output_cached, is_lesson_from_library, get_current_lesson_id
)


def render_mindmap_page(ai):
    if not st.session_state.extracted_text:
        st.warning("⚠️ ارفع ملف أو اختار درس من الفصول")
        return

    st.markdown("## 🧠 الخرائط الذهنية")

    col1, col2 = st.columns(2)
    with col1:
        depth_level = st.selectbox(
            "مستوى التفصيل:",
            options=["simple", "normal", "detailed"],
            format_func=lambda x: {"simple":"🟢 بسيط","normal":"🟡 متوسط","detailed":"🔴 مفصل"}[x],
            index=1, key="mm_depth"
        )
    with col2:
        map_style = st.selectbox(
            "🎨 ستايل الألوان:",
            options=["default", "colorful", "dark", "minimal"],
            index=0, key="mm_style"
        )

    can_do, msg = check_plan_limit("mindmaps")
    if not can_do:
        st.error(msg)
        if st.button("💎 اترقى لباقة أعلى", key="upgrade_mindmap"):
            st.session_state['current_page'] = 'subscriptions'
            st.rerun()
        return
    else:
        st.caption(msg)

    cached = get_cached_mindmap({'depth': depth_level, 'style': map_style})
    if cached:
        st.session_state.mindmap_data = cached
        st.success("⚡ الخريطة جاهزة من الكاش!")

    if st.button("🧠 ولّد الخريطة", use_container_width=True, type="primary", key="mm_gen"):
        if cached:
            st.rerun()
        else:
            with st.spinner("⏳ جاري توليد الخريطة الذهنية..."):
                try:
                    from utils.mindmap_generator import MindMapGenerator
                    mm_gen = MindMapGenerator(ai)
                    
                    try:
                        result = mm_gen.generate(st.session_state.extracted_text)
                    except TypeError:
                        try:
                            result = mm_gen.generate(text=st.session_state.extracted_text)
                        except Exception:
                            result = None
                    
                    if result and result.get('success'):
                        st.session_state.mindmap_data = result['data']
                        st.session_state.mindmap_markdown = result.get('markdown', '')
                        st.session_state.stats['mindmaps_made'] += 1
                        increment_usage('mindmaps')
                        save_mindmap_to_cache(result['data'], {'depth': depth_level, 'style': map_style})
                        st.success("✅ تم توليد الخريطة!")
                        st.rerun()
                    else:
                        st.error("❌ جرب تاني")
                except Exception as e:
                    st.error(f"❌ حصل خطأ: {str(e)}")

    if st.session_state.get('mindmap_data'):
        render_d3_mindmap(map_style)


def render_d3_mindmap(map_style="default"):
    """عرض الخريطة الذهنية بـ D3.js - شجرة تفاعلية"""
    st.markdown("---")
    st.markdown("### 🧠 خريطتك الذهنية التفاعلية")
    
    data = st.session_state.mindmap_data
    
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except:
            st.error("❌ خطأ في تنسيق البيانات")
            return
    
    if not isinstance(data, dict):
        st.error("❌ البيانات مش صحيحة")
        return
    
    # الألوان
    color_schemes = {
        "default": ["#667eea", "#764ba2", "#3498db", "#e74c3c", "#f39c12"],
        "colorful": ["#ff6b6b", "#4ecdc4", "#ffe66d", "#a8e6cf", "#ff8b94"],
        "dark": ["#00d9ff", "#00ff88", "#ff00aa", "#ffaa00", "#aa00ff"],
        "minimal": ["#2c3e50", "#34495e", "#7f8c8d", "#95a5a6", "#bdc3c7"]
    }
    
    colors = color_schemes.get(map_style, color_schemes["default"])
    bg_color = "#1a1a2e" if map_style == "dark" else "#ffffff"
    text_color = "#ffffff" if map_style == "dark" else "#2c3e50"
    
    data_json = json.dumps(data, ensure_ascii=False)
    colors_json = json.dumps(colors)
    
    html_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
        font-family: 'Cairo', 'Arial', sans-serif;
        background: BG_COLOR_HERE;
        overflow: hidden;
    }
    #mindmap-svg {
        width: 100%;
        height: 700px;
        background: BG_COLOR_HERE;
        cursor: grab;
    }
    #mindmap-svg:active { cursor: grabbing; }
    
    .node circle {
        stroke: white;
        stroke-width: 3px;
        cursor: pointer;
    }
    
    .node text {
        font: 14px 'Cairo', sans-serif;
        font-weight: 600;
        fill: TEXT_COLOR_HERE;
        pointer-events: none;
    }
    
    .link {
        fill: none;
        stroke: LINK_COLOR_HERE;
        stroke-width: 2px;
        stroke-opacity: 0.6;
    }
    
    .controls {
        position: absolute;
        top: 10px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 10;
    }
    
    .controls button {
        background: LINK_COLOR_HERE;
        color: white;
        border: none;
        padding: 8px 16px;
        margin: 0 5px;
        border-radius: 20px;
        cursor: pointer;
        font-family: 'Cairo', sans-serif;
        font-weight: 600;
        font-size: 13px;
    }
    
    .controls button:hover {
        opacity: 0.8;
    }
</style>
</head>
<body>
<div class="controls">
    <button onclick="resetView()">🔄 إعادة تعيين</button>
    <button onclick="expandAll()">📂 فتح الكل</button>
    <button onclick="collapseAll()">📁 غلق الكل</button>
</div>
<svg id="mindmap-svg"></svg>

<script>
const treeData = DATA_HERE;
const nodeColors = COLORS_HERE;

const width = window.innerWidth;
const height = 700;
const margin = {top: 20, right: 90, bottom: 20, left: 90};

const svg = d3.select("#mindmap-svg")
    .attr("width", width)
    .attr("height", height);

const g = svg.append("g")
    .attr("transform", "translate(" + (width - margin.right) + "," + (height/2) + ")");

let i = 0;
const duration = 500;

const tree = d3.tree().size([height - 40, width - 300]);

let root = d3.hierarchy(treeData, function(d) { return d.children; });
root.x0 = 0;
root.y0 = 0;

// طي كل الفروع بعد المستوى الأول
if (root.children) {
    root.children.forEach(collapse);
}

update(root);

function collapse(d) {
    if (d.children) {
        d._children = d.children;
        d._children.forEach(collapse);
        d.children = null;
    }
}

function expand(d) {
    if (d._children) {
        d.children = d._children;
        d.children.forEach(expand);
        d._children = null;
    }
}

function update(source) {
    const treeData = tree(root);
    const nodes = treeData.descendants();
    const links = treeData.descendants().slice(1);
    
    nodes.forEach(function(d) { d.y = d.depth * 180; });
    
    // === Nodes ===
    const node = g.selectAll('g.node')
        .data(nodes, function(d) { return d.id || (d.id = ++i); });
    
    const nodeEnter = node.enter().append('g')
        .attr('class', 'node')
        .attr("transform", function(d) {
            return "translate(" + (-source.y0) + "," + source.x0 + ")";
        })
        .on('click', click);
    
    nodeEnter.append('circle')
        .attr('class', 'node')
        .attr('r', 1e-6)
        .style("fill", function(d) {
            return d._children ? nodeColors[d.depth % nodeColors.length] : nodeColors[d.depth % nodeColors.length];
        });
    
    nodeEnter.append('text')
        .attr("dy", ".35em")
        .attr("x", function(d) {
            return d.children || d._children ? -13 : 13;
        })
        .attr("text-anchor", function(d) {
            return d.children || d._children ? "end" : "start";
        })
        .text(function(d) { return d.data.title; });
    
    // Update
    const nodeUpdate = nodeEnter.merge(node);
    
    nodeUpdate.transition()
        .duration(duration)
        .attr("transform", function(d) {
            return "translate(" + (-d.y) + "," + d.x + ")";
        });
    
    nodeUpdate.select('circle.node')
        .attr('r', function(d) {
            return d.depth === 0 ? 15 : 10;
        })
        .style("fill", function(d) {
            return nodeColors[d.depth % nodeColors.length];
        })
        .attr('cursor', 'pointer');
    
    // Exit
    const nodeExit = node.exit().transition()
        .duration(duration)
        .attr("transform", function(d) {
            return "translate(" + (-source.y) + "," + source.x + ")";
        })
        .remove();
    
    nodeExit.select('circle').attr('r', 1e-6);
    nodeExit.select('text').style('fill-opacity', 1e-6);
    
    // === Links ===
    const link = g.selectAll('path.link')
        .data(links, function(d) { return d.id; });
    
    const linkEnter = link.enter().insert('path', "g")
        .attr("class", "link")
        .attr('d', function(d) {
            const o = {x: source.x0, y: source.y0};
            return diagonal(o, o);
        });
    
    const linkUpdate = linkEnter.merge(link);
    
    linkUpdate.transition()
        .duration(duration)
        .attr('d', function(d) { return diagonal(d, d.parent); });
    
    link.exit().transition()
        .duration(duration)
        .attr('d', function(d) {
            const o = {x: source.x, y: source.y};
            return diagonal(o, o);
        })
        .remove();
    
    nodes.forEach(function(d) {
        d.x0 = d.x;
        d.y0 = d.y;
    });
    
    function diagonal(s, d) {
        return "M " + (-s.y) + " " + s.x +
               " C " + (-(s.y + d.y) / 2) + " " + s.x + "," +
               " " + (-(s.y + d.y) / 2) + " " + d.x + "," +
               " " + (-d.y) + " " + d.x;
    }
}

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

// Zoom
const zoom = d3.zoom()
    .scaleExtent([0.3, 3])
    .on("zoom", function(event) {
        g.attr("transform", event.transform);
    });

svg.call(zoom);

// Controls
window.resetView = function() {
    svg.transition().duration(500).call(
        zoom.transform,
        d3.zoomIdentity.translate(width - margin.right, height/2)
    );
};

window.expandAll = function() {
    root.each(function(d) {
        if (d._children) {
            d.children = d._children;
            d._children = null;
        }
    });
    update(root);
};

window.collapseAll = function() {
    root.each(function(d) {
        if (d.children && d.depth > 0) {
            d._children = d.children;
            d.children = null;
        }
    });
    update(root);
};

// Initial position
svg.call(
    zoom.transform,
    d3.zoomIdentity.translate(width - margin.right, height/2)
);
</script>
</body>
</html>
"""
    
    # استبدال المتغيرات
    html_code = html_code.replace("DATA_HERE", data_json)
    html_code = html_code.replace("COLORS_HERE", colors_json)
    html_code = html_code.replace("BG_COLOR_HERE", bg_color)
    html_code = html_code.replace("TEXT_COLOR_HERE", text_color)
    html_code = html_code.replace("LINK_COLOR_HERE", colors[0])
    
    components.html(html_code, height=720, scrolling=False)
    
    # أزرار التصدير
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        json_text = json.dumps(data, ensure_ascii=False, indent=2)
        st.download_button(
            "⬇️ تنزيل JSON",
            data=json_text,
            file_name="mindmap.json",
            mime="application/json",
            use_container_width=True,
            key="download_mm_json"
        )
    
    with col2:
        text_version = convert_to_text(data)
        st.download_button(
            "📝 تنزيل نصي",
            data=text_version,
            file_name="mindmap.txt",
            mime="text/plain",
            use_container_width=True,
            key="download_mm_txt"
        )


def convert_to_text(node, level=0):
    """تحويل الشجرة لنص"""
    if not isinstance(node, dict):
        return str(node)
    
    result = "  " * level + f"{'#' * (level + 1)} {node.get('title', '')}\n"
    for child in node.get('children', []):
        result += convert_to_text(child, level + 1)
    return result


def get_cached_mindmap(settings):
    is_from_library = is_lesson_from_library()
    if is_from_library:
        lesson_id = get_current_lesson_id()
        return get_lesson_output_cached(lesson_id=lesson_id, output_type='mindmap', settings=settings)
    else:
        current_file_id = st.session_state.get('current_file_id')
        if current_file_id:
            return get_cached_output(file_id=current_file_id, output_type='mindmap', settings=settings)
    return None


def save_mindmap_to_cache(content, settings):
    is_from_library = is_lesson_from_library()
    if is_from_library:
        lesson_id = get_current_lesson_id()
        save_lesson_output(lesson_id=lesson_id, output_type='mindmap', content=content, settings=settings)
    else:
        current_file_id = st.session_state.get('current_file_id')
        if current_file_id:
            save_output(file_id=current_file_id, output_type='mindmap', content=content, settings=settings)
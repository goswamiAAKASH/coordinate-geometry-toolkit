import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import io
import json
import inspect
import math
from typing import Any
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import csv
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    # Using absolute imports with the path fix above
    from coordinate_geometry_toolkit.point import Point
    from coordinate_geometry_toolkit.line import Line
    from coordinate_geometry_toolkit.circle import Circle
    from coordinate_geometry_toolkit.vector import Vector
    from coordinate_geometry_toolkit.triangle import Triangle
    from coordinate_geometry_toolkit.rectangle import Rectangle
    from coordinate_geometry_toolkit.square import Square
    from coordinate_geometry_toolkit.polygon import Polygon
    from coordinate_geometry_toolkit.ellipse import Ellipse
    from coordinate_geometry_toolkit.hyperbola import Hyperbola
    from coordinate_geometry_toolkit.parabola import Parabola
except Exception as e:
    st.error(f"Could not import modules: {str(e)}")
    # Provide a minimal fallback so the rest of the script doesn't crash during inspection.
    Point = Line = Circle = Vector = Triangle = Rectangle = Square = Polygon = Ellipse = Hyperbola = Parabola = object

# Utilities

COLOR_CYCLE = plt.rcParams['axes.prop_cycle'].by_key()['color']

def new_color(idx: int) -> str:
    return COLOR_CYCLE[idx % len(COLOR_CYCLE)]

def uid() -> str:
    import time, random
    return f"s{int(time.time()*1000)}_{random.randint(0,9999)}"

# Store shapes as dicts: {id, type, obj, name, color}
if 'shapes' not in st.session_state:
    st.session_state.shapes = []
if 'last_color_index' not in st.session_state:
    st.session_state.last_color_index = 0

# Core helpers 

def add_shape(shape_type: str, obj: Any, name: str = None):
    st.session_state.last_color_index += 1
    entry = {
        'id': uid(),
        'type': shape_type,
        'obj': obj,
        'name': name or f"{shape_type}_{len(st.session_state.shapes)+1}",
        'color': new_color(st.session_state.last_color_index)
    }
    st.session_state.shapes.append(entry)
    return entry

def undo_last():
    if st.session_state.shapes:
        return st.session_state.shapes.pop()
    return None

def clear_shapes():
    st.session_state.shapes = []
    st.session_state.last_color_index = 0

# Calculate bounding box from shapes using best-effort
def compute_bbox(margin=1.0):
    xs, ys = [], []
    for s in st.session_state.shapes:
        t = s['type']
        o = s['obj']
        try:
            if t == 'Point':
                xs.append(o.x); ys.append(o.y)
            elif t == 'Line':
                xs.extend([o.p1.x, o.p2.x]); ys.extend([o.p1.y, o.p2.y])
            elif t == 'Circle':
                xs.extend([o.center.x - o.radius, o.center.x + o.radius]); ys.extend([o.center.y - o.radius, o.center.y + o.radius])
            elif t == 'Vector':
                xs.extend([0, o._x]); ys.extend([0, o._y])
            elif t in ('Triangle','Polygon'):
                pts = getattr(o, 'vertices', None) or [o.p1, o.p2, getattr(o,'p3',None)]
                for p in pts:
                    if p is not None:
                        xs.append(p.x); ys.append(p.y)
            elif t in ('Rectangle','Square'):
                p1, p2 = o.p1, o.p2
                xs.extend([p1.x, p2.x]); ys.extend([p1.y, p2.y])
            elif t == 'Ellipse':
                xs.extend([o.center.x - o.a, o.center.x + o.a]); ys.extend([o.center.y - o.b, o.center.y + o.b])
            elif t == 'Hyperbola':
                xs.extend([o.center.x - o.a*5, o.center.x + o.a*5]); ys.extend([o.center.y - o.b*5, o.center.y + o.b*5])
            elif t == 'Parabola':
                pts = []
                try:
                    pts = o.generate_points(n=200)
                except Exception:
                    pass
                for p in pts:
                    xs.append(p.x); ys.append(p.y)
        except Exception:
            # ignore shape if attributes not as expected
            pass
    if not xs or not ys:
        return (-5 - margin, 5 + margin, -5 - margin, 5 + margin)
    xmin, xmax = min(xs) - margin, max(xs) + margin
    ymin, ymax = min(ys) - margin, max(ys) + margin
    # make square limits for neat view
    mx = max(xmax - xmin, ymax - ymin)
    cx = (xmin + xmax) / 2
    cy = (ymin + ymax) / 2
    return (cx - mx/2, cx + mx/2, cy - mx/2, cy + mx/2)

# ---------- Plotting ----------

def plot_all(show_grid=True, show_axes=True, annotate=True):
    fig, ax = plt.subplots(figsize=(7,7))
    ax.set_aspect('equal')
    ax.tick_params(axis='both', which='major', labelsize=9, pad=6)

    if show_grid:
        ax.grid(True, linestyle='--', alpha=0.4)

    # draw axes as thin lines if requested
    for spine in ['top','right']:
        ax.spines[spine].set_visible(False)
    if show_axes:
        ax.axhline(0, color='#666666', linewidth=1, alpha=0.7, zorder=0)
        ax.axvline(0, color='#666666', linewidth=1, alpha=0.7, zorder=0)

    labels = []
    for s in st.session_state.shapes:
        t = s['type']; o = s['obj']; color = s['color']; name = s['name']
        try:
            if t == 'Point':
                ax.plot(o.x, o.y, 'o', color=color, markersize=8)
                if annotate: ax.annotate(name + f" ({o.x:.2f},{o.y:.2f})", (o.x, o.y), textcoords='offset points', xytext=(4,4), fontsize=8)
                labels.append(name)

            elif t == 'Line':
                x1, y1 = o.p1.x, o.p1.y
                x2, y2 = o.p2.x, o.p2.y
                ax.plot([x1, x2], [y1, y2], '-', linewidth=2, color=color)
                if annotate: ax.annotate(name, ((x1+x2)/2, (y1+y2)/2), fontsize=8)

            elif t == 'Circle':
                circ = plt.Circle((o.center.x, o.center.y), o.radius, fill=False, linewidth=2, color=color)
                ax.add_artist(circ)
                if annotate: ax.annotate(name + f" (r={o.radius:.2f})", (o.center.x + o.radius, o.center.y), fontsize=8)

            elif t == 'Vector':
                ax.quiver(0,0, o._x, o._y, angles='xy', scale_units='xy', scale=1, color=color)
                if annotate: ax.annotate(name, (o._x, o._y), fontsize=8)

            elif t in ('Triangle','Polygon'):
                pts = getattr(o, 'vertices', None)
                if pts is None:
                    pts = [o.p1, o.p2, getattr(o,'p3',None)]
                xs = [p.x for p in pts] + [pts[0].x]
                ys = [p.y for p in pts] + [pts[0].y]
                ax.plot(xs, ys, '-', linewidth=2, color=color)
                if annotate: ax.annotate(name, (xs[0], ys[0]), fontsize=8)

            elif t in ('Rectangle','Square'):
                p1, p2 = o.p1, o.p2
                p3 = Point(p1.x, p2.y)
                p4 = Point(p2.x, p1.y)
                pts = [p1,p3,p2,p4]
                xs = [p.x for p in pts] + [pts[0].x]
                ys = [p.y for p in pts] + [pts[0].y]
                ax.plot(xs, ys, '-', linewidth=2, color=color)
                if annotate: ax.annotate(name, (p1.x, p1.y), fontsize=8)

            elif t == 'Ellipse':
                tvals = np.linspace(0, 2*np.pi, 200)
                x = o.center.x + o.a * np.cos(tvals)
                y = o.center.y + o.b * np.sin(tvals)
                ax.plot(x, y, '-', linewidth=2, color=color)
                if annotate: ax.annotate(name, (o.center.x + o.a, o.center.y), fontsize=8)

            elif t == 'Hyperbola':
                tvals = np.linspace(0.5, 3.0, 200)
                x1 = o.center.x + o.a*np.cosh(tvals)
                y1 = o.center.y + o.b*np.sinh(tvals)
                x2 = o.center.x - o.a*np.cosh(tvals)
                y2 = o.center.y - o.b*np.sinh(tvals)
                ax.plot(x1, y1, '-', linewidth=2, color=color)
                ax.plot(x2, y2, '-', linewidth=2, color=color)

            elif t == 'Parabola':
                pts = []
                try:
                    pts = o.generate_points(n=400)
                except Exception:
                    # fall back to sampling around vertex and focus if available
                    try:
                        v = o.vertex
                        f = o.focus
                        p = v.x
                        tvals = np.linspace(-5,5,200)
                        xs = [p + tv for tv in tvals]
                        ys = [o.value_at(xi) for xi in xs]
                        ax.plot(xs, ys, '-', linewidth=2, color=color)
                    except Exception:
                        pass
                if pts:
                    xs = [p.x for p in pts]
                    ys = [p.y for p in pts]
                    ax.plot(xs, ys, '-', linewidth=2, color=color)

        except Exception:
            # if plotting of a shape fails, continue with others
            continue

    xmin, xmax, ymin, ymax = compute_bbox(margin=1.0)
    ax.set_xlim(xmin, xmax); ax.set_ylim(ymin, ymax)
    ax.set_xlabel('X'); ax.set_ylabel('Y')
    ax.set_title('Geometry Toolkit — Visualization')
    fig.tight_layout()
    return fig

# ---------- UI: Sidebar controls ----------

st.set_page_config(page_title="Geometry Toolkit", layout='wide', page_icon="📐")

# Enhanced CSS for UI with 60-30-10 color rule and improved visibility (google se liya)
st.markdown(
    """
    <style>
    /* Global styles */
    body {
        background-color: #2E2E2E; /* Dominant dark grey */
        color: #F5F5F5; /* High-contrast white text */
        font-family: 'Roboto', sans-serif;
        margin: 0;
        padding: 0;
    }

    /* Main content and sidebar */
    .main-header, .sidebar-section, .shape-card, .info-box, .method-section, .success-box, .error-box, .metric-card, .summary-section {
        background-color: #F5F5F5; /* Light grey/white background */
        color: #2E2E2E; /* Dark text for readability */
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .main-header h1, .sidebar-section h3, .sidebar-section h4, .shape-card h3, .method-section h3, .summary-section h2 {
        color: #2E2E2E; /* Ensure headers are dark */
        text-align: center;
        margin-bottom: 0.5rem;
    }

    .main-header p, .shape-card p, .method-section p, .summary-section p {
        color: #4A4A4A; /* Medium grey for secondary text */
        text-align: center;
        font-size: 1rem;
    }

    /* Input fields */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #FFFFFF; /* White for inputs */
        color: #2E2E2E; /* Dark text */
        border: 1px solid #C5FF3E; /* Accent border */
        border-radius: 8px;
        padding: 0.75rem;
        font-size: 1rem;
        width: 100%;
        box-sizing: border-box;
    }

    /* Buttons */
    .stButton button {
        background-color: #C5FF3E; /* Accent yellow-green */
        color: #2E2E2E; /* Dark text on button */
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        transition: background-color 0.2s ease;
    }

    .stButton button:hover {
        background-color: #A3FF12; /* Darker accent on hover */
        color: #2E2E2E; /* Ensure text remains visible */
    }

    /* Selectbox */
    .stSelectbox select {
        background-color: #FFFFFF;
        color: #2E2E2E;
        border: 1px solid #C5FF3E;
        border-radius: 8px;
        padding: 0.75rem;
        font-size: 1rem;
    }

    /* Responsive columns */
    .stColumns {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
    }

    /* Shape history alignment */
    .stColumns .stButton {
        margin-top: 0.5rem;
    }

    /* Summary section */
    .summary-section ul {
        list-style-type: disc;
        padding-left: 2rem;
    }
    .summary-section li {
        margin-bottom: 0.5rem;
        color: #2E2E2E;
    }

    /* Ensure text visibility */
    .stMarkdown strong, .stMarkdown em, .stMarkdown p, .stMarkdown li {
        color: #2E2E2E; /* Dark text for all markdown */
    }

    /* Sidebar fix */
    .css-1v3fvcr {
        background-color: #2E2E2E !important;
        color: #F5F5F5 !important; /* Ensure sidebar text is visible */
        padding: 1rem;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .stColumns {
            flex-direction: column;
        }
        .stButton button {
            padding: 0.5rem 1rem;
        }
        .summary-section {
            padding: 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main header
st.markdown("""
<div class="main-header">
    <h1>Geometry Toolkit</h1>
    <p>Interactive Coordinate Geometry Visualization</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div class="sidebar-section">
    <h3>Controls</h3>
</div>
""", unsafe_allow_html=True)

# Quick controls
st.sidebar.markdown("""
<div class="sidebar-section">
    <h4>Quick Actions</h4>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button('Clear All', help="Remove all shapes"):
        clear_shapes()
        st.rerun()

with col2:
    if st.button('Undo', help="Remove last shape"):
        undo_last()
        st.rerun()

# Download Shapes
with st.sidebar.expander('Download Shapes'):
    if st.button('Download shapes (JSON)'):
        buf = io.BytesIO()
        serial = [{'id': s['id'], 'type': s['type'], 'name': s['name']} for s in st.session_state.shapes]
        buf.write(json.dumps(serial, indent=2).encode())
        buf.seek(0)
        st.download_button('Download JSON (summary)', buf, file_name='shapes_summary.json')

# Export visualizations and results
with st.sidebar.expander('Export Reports'):
    export_type = st.selectbox('Export as', ['PDF', 'CSV'])
    if st.button('Export'):
        if export_type == 'PDF':
            pdf_buffer = io.BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            story.append(Paragraph("Geometry Toolkit Report", styles['Heading1']))
            story.append(Spacer(1, 12))
            
            # Add visualization
            fig = plot_all(show_grid=True, show_axes=True, annotate=True)
            img_buffer = io.BytesIO()
            fig.savefig(img_buffer, format='PNG', dpi=100)
            img_buffer.seek(0)
            story.append(Image(img_buffer, width=400, height=400))
            story.append(Spacer(1, 12))
            
            # Add shape summary
            story.append(Paragraph("Shape Summary", styles['Heading2']))
            for s in st.session_state.shapes:
                story.append(Paragraph(f"{s['name']} ({s['type']}): {str(s['obj'])}", styles['Normal']))
            story.append(Spacer(1, 12))
            
            doc.build(story)
            pdf_buffer.seek(0)
            st.download_button('Download PDF Report', pdf_buffer, file_name='geometry_report.pdf')
        elif export_type == 'CSV':
            csv_buffer = io.StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow(['Name', 'Type', 'Details'])
            for s in st.session_state.shapes:
                writer.writerow([s['name'], s['type'], str(s['obj'])])
            csv_buffer.seek(0)
            st.download_button('Download CSV Report', data=csv_buffer.getvalue(), file_name='geometry_report.csv', mime='text/csv')

# Visualization toggles
st.sidebar.markdown("""
<div class="sidebar-section">
    <h4>Display Options</h4>
</div>
""", unsafe_allow_html=True)

show_grid = st.sidebar.checkbox('Show grid', True, help="Display grid lines on the plot")
show_axes = st.sidebar.checkbox('Show axes (x=0,y=0)', True, help="Show coordinate axes")
annotate = st.sidebar.checkbox('Show labels & annotations', True, help="Display shape names and coordinates")

# ---------- Main layout ----------

left, right = st.columns([2,3])

with left:
    st.markdown("""
    <div class="shape-card">
        <h3>Create Shapes</h3>
        <p>Select a shape type and provide the required parameters to add it to your diagram.</p>
    </div>
    """, unsafe_allow_html=True)
    
    shape_choice = st.selectbox('Choose shape', ['Point','Line','Circle','Triangle','Rectangle','Square','Vector','Polygon','Ellipse','Hyperbola','Parabola'], help="Select the type of geometric shape to create")

    with st.form('create_shape'):
        name = st.text_input('Optional name', placeholder="e.g., Point A, Center, Vertex")
        if shape_choice == 'Point':
            x = st.number_input('X', value=0.0, format='%f')
            y = st.number_input('Y', value=0.0, format='%f')
            if st.form_submit_button('Add Point'):
                add_shape('Point', Point(x,y), name=name or None)
                st.success('Point added successfully!')

        elif shape_choice == 'Line':
            st.markdown('Two points (A and B)')
            x1 = st.number_input('Ax', value=-1.0, key='ax')
            y1 = st.number_input('Ay', value=0.0, key='ay')
            x2 = st.number_input('Bx', value=1.0, key='bx')
            y2 = st.number_input('By', value=0.0, key='by')
            if st.form_submit_button('Add Line'):
                add_shape('Line', Line(Point(x1,y1), Point(x2,y2)), name=name or None)
                st.success('Line added successfully!')

        elif shape_choice == 'Circle':
            cx = st.number_input('Center X', value=0.0)
            cy = st.number_input('Center Y', value=0.0)
            r = st.number_input('Radius', value=1.0, min_value=0.0)
            if st.form_submit_button('Add Circle'):
                add_shape('Circle', Circle(Point(cx,cy), r), name=name or None)
                st.success('Circle added successfully!')

        elif shape_choice == 'Triangle':
            st.markdown('Three vertices')
            tx1 = st.number_input('X1', value=0.0, key='t1x')
            ty1 = st.number_input('Y1', value=0.0, key='t1y')
            tx2 = st.number_input('X2', value=1.0, key='t2x')
            ty2 = st.number_input('Y2', value=0.0, key='t2y')
            tx3 = st.number_input('X3', value=0.0, key='t3x')
            ty3 = st.number_input('Y3', value=1.0, key='t3y')
            if st.form_submit_button('Add Triangle'):
                add_shape('Triangle', Triangle(Point(tx1,ty1), Point(tx2,ty2), Point(tx3,ty3)), name=name or None)
                st.success('Triangle added')

        elif shape_choice == 'Rectangle':
            rx1 = st.number_input('Corner 1 X', value=-1.0, key='rx1')
            ry1 = st.number_input('Corner 1 Y', value=-1.0, key='ry1')
            rx2 = st.number_input('Corner 2 X', value=1.0, key='rx2')
            ry2 = st.number_input('Corner 2 Y', value=1.0, key='ry2')
            if st.form_submit_button('Add Rectangle'):
                add_shape('Rectangle', Rectangle(Point(rx1,ry1), Point(rx2,ry2)), name=name or None)
                st.success('Rectangle added')

        elif shape_choice == 'Square':
            sx1 = st.number_input('Corner 1 X', value=-1.0, key='sx1')
            sy1 = st.number_input('Corner 1 Y', value=-1.0, key='sy1')
            sx2 = st.number_input('Corner 2 X', value=1.0, key='sx2')
            sy2 = st.number_input('Corner 2 Y', value=1.0, key='sy2')
            if st.form_submit_button('Add Square'):
                add_shape('Square', Square(Point(sx1,sy1), Point(sx2,sy2)), name=name or None)
                st.success('Square added')

        elif shape_choice == 'Vector':
            vx = st.number_input('X component', value=1.0)
            vy = st.number_input('Y component', value=1.0)
            if st.form_submit_button('Add Vector'):
                add_shape('Vector', Vector(vx,vy), name=name or None)
                st.success('Vector added')

        elif shape_choice == 'Polygon':
            n = st.number_input('Number of vertices', min_value=3, value=3, step=1)
            pts = []
            for i in range(n):
                cx, cy = st.columns(2)
                with cx:
                    px = st.number_input(f'X{i+1}', value=float(np.cos(2*np.pi*i/n)), key=f'poly_x_{i}')
                with cy:
                    py = st.number_input(f'Y{i+1}', value=float(np.sin(2*np.pi*i/n)), key=f'poly_y_{i}')
                pts.append(Point(px, py))
            if st.form_submit_button('Add Polygon'):
                add_shape('Polygon', Polygon(pts), name=name or None)
                st.success('Polygon added')

        elif shape_choice == 'Ellipse':
            ecx = st.number_input('Center X', value=0.0)
            ecy = st.number_input('Center Y', value=0.0)
            a = st.number_input('Semi-major a', value=2.0, min_value=0.0)
            b = st.number_input('Semi-minor b', value=1.0, min_value=0.0)
            if st.form_submit_button('Add Ellipse'):
                add_shape('Ellipse', Ellipse(Point(ecx,ecy), a, b), name=name or None)
                st.success('Ellipse added')

        elif shape_choice == 'Hyperbola':
            hcx = st.number_input('Center X', value=0.0)
            hcy = st.number_input('Center Y', value=0.0)
            a = st.number_input('Transverse a', value=2.0, min_value=0.0)
            b = st.number_input('Conjugate b', value=1.0, min_value=0.0)
            if st.form_submit_button('Add Hyperbola'):
                add_shape('Hyperbola', Hyperbola(Point(hcx,hcy), a, b), name=name or None)
                st.success('Hyperbola added')

        elif shape_choice == 'Parabola':
            pvx = st.number_input('Vertex X', value=0.0)
            pvy = st.number_input('Vertex Y', value=0.0)
            pfx = st.number_input('Focus X', value=0.0)
            pfy = st.number_input('Focus Y', value=1.0)
            if st.form_submit_button('Add Parabola'):
                add_shape('Parabola', Parabola(Point(pvx,pvy), Point(pfx,pfy)), name=name or None)
                st.success('Parabola added')

with right:
    st.markdown("""
    <div class="shape-card">
        <h3>Visualization & History</h3>
        <p>View your geometric shapes and manage your diagram.</p>
    </div>
    """, unsafe_allow_html=True)
    
    fig = plot_all(show_grid=show_grid, show_axes=show_axes, annotate=annotate)
    st.pyplot(fig)

    # Export plot
    st.markdown("---")
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150)
    buf.seek(0)
    st.download_button('Download plot as PNG', buf, file_name='geometry_plot.png', help="Save your diagram as a high-quality image")

    # Shape history
    st.markdown("""
    <div class="shape-card">
        <h4>Shape History</h4>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.shapes:
        for i, s in enumerate(reversed(st.session_state.shapes)):
            actual_idx = len(st.session_state.shapes) - 1 - i
            cols = st.columns([6,1])
            with cols[0]:
                st.markdown(f"""
                <div class="info-box">
                    <strong>{actual_idx+1}. {s['name']}</strong> — <em>{s['type']}</em>
                </div>
                """, unsafe_allow_html=True)
            with cols[1]:
                if st.button('Delete', key=f"del_{s['id']}", help="Delete this shape"):
                    try:
                        del st.session_state.shapes[actual_idx]
                    except Exception:
                        pass
                    st.rerun()
    else:
        st.markdown("""
        <div class="info-box">
            <strong>No shapes yet.</strong> Use the form on the left to create shapes and start building your diagram!
        </div>
        """, unsafe_allow_html=True)

# ---------- Method explorer (dynamic) ----------

st.markdown('---')
st.markdown("""
<div class="method-section">
    <h3>Method Explorer</h3>
    <p>Explore methods defined in your geometry classes. Results will be added to your diagram.</p>
</div>
""", unsafe_allow_html=True)

if not st.session_state.shapes:
    st.markdown("""
    <div class="info-box">
        <strong>No shapes available.</strong> Add at least one shape to use the method explorer.
    </div>
    """, unsafe_allow_html=True)
else:
    # Curated method list that matches your class source code
    CLASS_METHODS = {
        'Point': [
            ('distance_from_origin', []),
            ('distance_bw_two_points', ['point']),
            ('midpoint', ['point']),
            ('reflection_of_point_about_X_Axis', []),
            ('reflection_of_point_about_Y_Axis', []),
            ('reflection_of_point_about_Origin', []),
            ('translate_point', ['float','float']),
            ('quadrant_of_a_point', []),
            ('midpoint_with_origin', []),
            ('slope_between_two_points', ['point']),
            ('to_vector', []),
        ],
        'Line': [
            ('length_of_the_line_segment', []),
            ('slope', []),
            ('equation', []),
            ('is_horizontal', []),
            ('is_vertical', []),
            ('midpoint_line_segment', []),
            ('is_Parallel', ['line']),
            ('is_perpendicular', ['line']),
            ('distance_from_point', ['point']),
            ('angle_bw_two_line', ['line']),
            ('intersection_with_another_line', ['line']),
            ('angle_between_two_lines', ['line']),
        ],
        'Circle': [
            ('area', []),
            ('perimeter', []),
            ('diameter', []),
            ('is_point_on_circle', ['point']),
            ('cir_from_diameter', ['point','point']),
            ('generate_points', ['int']),
            ('equation_of_chord', ['point','point']),
        ],
        'Vector': [
            ('magnitude', []),
            ('dot', ['vector']),
            ('cross', ['vector']),
            ('angle_with', ['vector']),
            ('angle_between', ['vector']),
            ('unit_vector', []),
            ('projection_on', ['vector']),
            ('is_parallel', ['vector']),
            ('is_perpendicular', ['vector']),
            ('scale', ['float']),
            ('is_collinear', ['vector']),
            ('angle_with_x_axis', []),
            ('angle_with_y_axis', []),
            ('reflect_x_axis', []),
            ('reflect_y_axis', []),
            ('reflect_origin', []),
            ('translate', ['float','float']),
            ('rotate', ['float']),
            ('rotate_about_point', ['float','point']),
            ('to_point', []),
            ('to_polar', []),
        ],
        'Triangle': [
            ('area', []), ('perimeter', []), ('Centroid', []), ('type_of_triangle', []),
            ('is_right_angle_triangle', []), ('is_collinear', []), ('is_Valid_Triangle', []),
            ('angle_of_triangle', []), ('Incenter', []), ('circumcenter', []), ('orthocenter', []),
            ('circumradius', []), ('inradius', []),
        ],
        'Rectangle': [
            ('area', []), ('perimeter', []), ('diagonal_length', []),
            ('is_point_inside', ['point']), ('is_point_on_boundary', ['point']),
        ],
        'Square': [
            ('area', []), ('perimeter', []), ('diagonal_length', []),
            ('is_point_inside', ['point']), ('is_point_on_boundary', ['point']),
        ],
        'Polygon': [
            ('perimeter', []), ('area', []), ('centroid', []), ('is_point_inside', ['point']),
        ],
        'Ellipse': [
            ('eccentricity', []), ('equation', []), ('foci', []), ('vertices', []), ('co_vertices', []),
            ('major_axis_length', []), ('minor_axis_length', []), ('area', []), ('perimeter', []),
            ('point_on_ellipse', ['point']), ('is_point_inside', ['point']), ('distance_to_focus', ['point']),
            ('generate_points', ['int']), ('axis_of_symmetry', []), ('latus_rectum_length', []), ('directrix', []),
            ('focus_point', []), ('co_focus_point', []), ('reflection_of_ellipse_about_X_axis', []), ('reflection_of_ellipse_about_Y_axis', []),
        ],
        'Hyperbola': [
            ('equation', []), ('foci', []), ('vertices', []), ('asymptotes', []), ('eccentricity', []),
            ('transverse_axis_length', []), ('conjugate_axis_length', []), ('point_on_hyperbola', ['point']),
            ('is_between_branches', ['point']), ('distance_to_focus', ['point']), ('generate_points', ['int']),
            ('is_point_on_hyperbola', ['point']),
        ],
        'Parabola': [
            ('equation', []), ('focus_point', []), ('directrix', []), ('latus_rectum_length', []),
            ('axis_of_symmetry', []), ('vertex_form_of_parabola', []), ('point_on_parabola', ['point']),
            ('distance_to_focus', ['point']), ('distance_to_directrix', ['point']), ('is_point_inside', ['point']),
            ('generate_points', ['int']), ('is_point_on_parabola', ['point']), ('focus_directrix_property', ['point']),
        ],
    }

    idx = st.number_input('Choose shape index (1 = first added)', min_value=1, max_value=len(st.session_state.shapes), value=1)
    entry = st.session_state.shapes[idx-1]
    s_obj = entry['obj']
    s_type = entry['type']
    st.markdown(f"**Selected:** {entry['name']} ({s_type})")

    methods = CLASS_METHODS.get(s_type, [])
    if not methods:
        st.warning('No curated methods for this shape type.')
    else:
        method_labels = [m[0] for m in methods]
        chosen = st.selectbox('Choose a method to call', method_labels)
        args_spec = dict(methods)[chosen]

        args = []
        # Build inputs per spec
        for i, kind in enumerate(args_spec):
            if kind == 'point':
                cx, cy = st.columns(2)
                with cx:
                    x = st.number_input(f'arg{i+1} (Point x)', value=0.0, key=f'{chosen}_px_{i}')
                with cy:
                    y = st.number_input(f'arg{i+1} (Point y)', value=0.0, key=f'{chosen}_py_{i}')
                args.append(Point(x, y))
            elif kind == 'line':
                st.markdown(f'arg{i+1} (Line)')
                lx1 = st.number_input(f'Line{i+1} A x', value=0.0, key=f'{chosen}_l{i}_ax')
                ly1 = st.number_input(f'Line{i+1} A y', value=0.0, key=f'{chosen}_l{i}_ay')
                lx2 = st.number_input(f'Line{i+1} B x', value=1.0, key=f'{chosen}_l{i}_bx')
                ly2 = st.number_input(f'Line{i+1} B y', value=0.0, key=f'{chosen}_l{i}_by')
                args.append(Line(Point(lx1,ly1), Point(lx2,ly2)))
            elif kind == 'vector':
                vx = st.number_input(f'arg{i+1} Vector x', value=1.0, key=f'{chosen}_vx_{i}')
                vy = st.number_input(f'arg{i+1} Vector y', value=1.0, key=f'{chosen}_vy_{i}')
                args.append(Vector(vx, vy))
            elif kind == 'int':
                ival = st.number_input(f'arg{i+1} (int)', value=100, step=1, key=f'{chosen}_int_{i}')
                args.append(int(ival))
            elif kind == 'float':
                fval = st.number_input(f'arg{i+1} (float)', value=0.0, key=f'{chosen}_float_{i}')
                args.append(float(fval))

        if st.button('Run Method', type="primary"):
            try:
                func = getattr(s_obj, chosen)
                res = func(*args)
                # Integrate results directly into the main diagram instead of separate mini plots
                if isinstance(res, Point):
                    add_shape('Point', res, name=f'{chosen} result')
                    st.markdown("""
                    <div class="success-box">
                        <strong>Point added to the diagram!</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    st.rerun()
                elif isinstance(res, (list, tuple)) and res and isinstance(res[0], Point):
                    pts = list(res)
                    if len(pts) == 1:
                        add_shape('Point', pts[0], name=f'{chosen} result')
                    elif len(pts) == 2:
                        add_shape('Point', pts[0], name=f'{chosen} result P1')
                        add_shape('Point', pts[1], name=f'{chosen} result P2')
                        # also draw a line if meaningful
                        try:
                            add_shape('Line', Line(pts[0], pts[1]), name=f'{chosen} segment')
                        except Exception:
                            pass
                    else:
                        add_shape('Polygon', Polygon(pts), name=f'{chosen} path')
                    st.markdown("""
                    <div class="success-box">
                        <strong>Result added to the diagram!</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    st.rerun()
                elif isinstance(res, (Circle, Ellipse, Hyperbola, Parabola, Line, Triangle, Rectangle, Square, Polygon, Vector)):
                    type_map = {
                        Circle: 'Circle', Ellipse: 'Ellipse', Hyperbola: 'Hyperbola', Parabola: 'Parabola',
                        Line: 'Line', Triangle: 'Triangle', Rectangle: 'Rectangle', Square: 'Square', Polygon: 'Polygon', Vector: 'Vector'
                    }
                    tname = next((v for k,v in type_map.items() if isinstance(res, k)), 'Shape')
                    add_shape(tname, res, name=f'{chosen} result')
                    st.markdown(f"""
                    <div class="success-box">
                        <strong>{tname} added to the diagram!</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    st.rerun()
                else:
                    st.markdown(f"""
                    <div class="metric-card">
                        <strong>Method Result:</strong> {res}
                    </div>
                    """, unsafe_allow_html=True)
                    try:
                        # Numeric → show metric and mini bar
                        if isinstance(res, (int, float)):
                            st.metric(label='Value', value=res)
                            fign, axn = plt.subplots(figsize=(3.5, 0.6))
                            axn.barh(["result"], [float(res)])
                            axn.set_yticks([])
                            axn.set_xlim(left=min(0.0, float(res)))
                            for spine in ["top","right","left"]:
                                axn.spines[spine].set_visible(False)
                            st.pyplot(fign)
                        # Dict of numeric → bar chart
                        elif isinstance(res, dict) and all(isinstance(v, (int, float)) for v in res.values()):
                            labels = list(res.keys())
                            values = [float(res[k]) for k in labels]
                            figd, axd = plt.subplots(figsize=(4.5, 2.5))
                            axd.bar(labels, values)
                            axd.set_title('Values')
                            st.pyplot(figd)
                        # Tuple/list of numerics → line
                        elif isinstance(res, (list, tuple)) and res and all(isinstance(v, (int, float)) for v in res):
                            figl, axl = plt.subplots(figsize=(4.5, 2.2))
                            axl.plot(list(range(len(res))), list(map(float, res)), marker='o')
                            axl.set_title('Sequence')
                            st.pyplot(figl)
                        # Bool → simple status
                        elif isinstance(res, bool):
                            status = "True" if res else "False"
                            st.markdown(f"""
                            <div class="success-box">
                                <strong>{status}</strong>
                            </div>
                            """, unsafe_allow_html=True)
                    except Exception:
                        pass
            except Exception as e:
                st.markdown(f"""
                <div class="error-box">
                    <strong>Error calling method:</strong> {e}
                </div>
                """, unsafe_allow_html=True)

# ---------- Educational help ----------

st.markdown('---')
st.markdown("""
<div class="method-section">
    <h3>Study Corner</h3>
    <p>Explore geometric concepts and practice problems.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <h4>Key Features:</h4>
    <ul>
        <li><strong>Shapes & Conics</strong> — Create points, lines, circles, parabolas, and more to visualize problems.</li>
        <li><strong>Locus Problems</strong> — Generate parametric points (e.g., midpoints of moving segments).</li>
        <li><strong>Method Explorer</strong> — Calculate coordinates, intersections, and slopes interactively.</li>
    </ul>
    
    <h4>Example Problem:</h4>
    <p><em>Find the equation of a circle passing through points (1,0), (0,1), and (-1,0).</em></p>
    <p><strong>Steps:</strong> Add the three points → compute perpendicular bisectors → find their intersection → create a circle with the center and radius.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <strong>Want more?</strong> Request additional problems with solutions and one-click setups for topics like circles, parabolas, conics, triangle centers, locus, or transformations.
</div>
""", unsafe_allow_html=True)

# ---------- Summary Display (Disabled Upload, Kept Download Reference) ----------

st.markdown("""
<div class="summary-section">
    <h2>Shape Summary</h2>
    <p>Download a JSON summary of your shapes using the 'Download Shapes' option in the sidebar.</p>
</div>
""", unsafe_allow_html=True)

# ---------- End ----------

st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(90deg, #4a5568 0%, #2d3748 100%); color: white; border-radius: 10px; margin-top: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <h3>Built for Learning</h3>
    <p>Create clear diagrams, explore methods, and practice problems. Request custom features anytime!</p>
</div>
""", unsafe_allow_html=True)
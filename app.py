import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="🎨 Tablero de Dibujo Completo")
st.title("🖌️ Tablero para Dibujo Avanzado")

# Propiedades en el sidebar
with st.sidebar:
    st.subheader("Propiedades del Tablero")
    
    drawing_mode = st.selectbox(
        "🛠️ Herramienta de Dibujo:",
        ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
    )

    stroke_width = st.slider("✏️ Grosor del trazo", 1, 30, 15)
    stroke_color = st.color_picker("🎨 Color del trazo", "#FFFFFF")
    fill_color_hex = st.color_picker("🧯 Color de relleno (formas)", "#FFA500")
    bg_color = st.color_picker("🖼️ Color de fondo", "#000000")
    realtime_update = st.checkbox("🔄 Actualización en tiempo real", True)

# Convertir el color de relleno a formato RGBA con opacidad fija
fill_color_rgba = fill_color_hex.lstrip("#")
r, g, b = tuple(int(fill_color_rgba[i:i+2], 16) for i in (0, 2, 4))
fill_color = f"rgba({r}, {g}, {b}, 0.3)"  # Opacidad del 30%

# Canvas principal
canvas_result = st_canvas(
    fill_color=fill_color,  # Color de relleno
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=400,
    width=600,
    drawing_mode=drawing_mode,
    update_streamlit=realtime_update,
    key="canvas",
)

# Mostrar data del dibujo (opcional)
if canvas_result.json_data is not None:
    st.subheader("📦 Datos JSON del dibujo:")
    st.json(canvas_result.json_data)

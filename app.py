import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
import os

st.set_page_config(page_title="🎨 Tablero de Dibujo Total")
st.title("🖌️ Tablero de Dibujo Interactivo")

# Sidebar: Configuración del canvas
with st.sidebar:
    st.subheader("🎛️ Propiedades del Tablero")

    drawing_mode = st.selectbox(
        "🛠️ Herramienta de Dibujo:",
        ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
    )

    stroke_width = st.slider("✏️ Grosor del trazo", 1, 30, 15)
    stroke_color = st.color_picker("🎨 Color del trazo", "#FFFFFF")
    fill_color_hex = st.color_picker("🧯 Color de relleno (formas)", "#FFA500")
    bg_color = st.color_picker("🖼️ Color de fondo", "#000000")
    realtime_update = st.checkbox("🔄 Actualización en tiempo real", True)

    st.markdown("---")
    bg_image_file = st.file_uploader("📂 Cargar imagen de fondo", type=["png", "jpg", "jpeg"])
    clear_canvas = st.button("🧹 Limpiar el Canvas")
    save_canvas = st.button("💾 Guardar como PNG")

# Convertir color de relleno a formato RGBA
fill_color_rgba = fill_color_hex.lstrip("#")
r, g, b = tuple(int(fill_color_rgba[i:i+2], 16) for i in (0, 2, 4))
fill_color = f"rgba({r}, {g}, {b}, 0.3)"  # Opacidad al 30%

# Procesar imagen de fondo
bg_image = None
if bg_image_file:
    bg_image = Image.open(bg_image_file)

# Si se presiona "limpiar", forzamos el canvas a recargarse usando una clave diferente
canvas_key = "canvas_reset" if clear_canvas else "canvas_active"

# Mostrar el canvas
canvas_result = st_canvas(
    fill_color=fill_color,
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=None if bg_image else bg_color,
    background_image=bg_image,
    height=400,
    width=600,
    drawing_mode=drawing_mode,
    update_streamlit=realtime_update,
    key=canvas_key,
)

# Guardar como PNG si se presionó el botón
if save_canvas and canvas_result.image_data is not None:
    st.success("✅ Imagen guardada como 'mi_dibujo.png'")
    img = Image.fromarray(canvas_result.image_data.astype("uint8"), mode="RGBA")
    img.save("mi_dibujo.png")
    # También mostrar la imagen en pantalla y permitir descarga
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button(
        label="⬇️ Descargar imagen",
        data=byte_im,
        file_name="mi_dibujo.png",
        mime="image/png"
    )
    st.image(img, caption="Tu dibujo guardado", use_column_width=True)

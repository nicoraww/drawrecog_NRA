import os
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import io
import base64
import openai

# --- Función para codificar imagen como base64 ---
def encode_image(image: Image.Image) -> str:
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# --- Configuración inicial ---
st.set_page_config(page_title="🎨 Tablero Inteligente")
st.title("🧠 Tablero de Dibujo con Inteligencia Artificial")

# --- Sidebar: Configuración del tablero ---
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

    st.markdown("---")
    api_key = st.text_input("🔑 Ingresa tu API Key de OpenAI", type="password")
    analyze_button = st.button("🧠 Analizar dibujo con GPT")

# --- Preparar colores ---
fill_color_rgba = fill_color_hex.lstrip("#")
r, g, b = tuple(int(fill_color_rgba[i:i+2], 16) for i in (0, 2, 4))
fill_color = f"rgba({r}, {g}, {b}, 0.3)"

# --- Imagen de fondo ---
bg_image = Image.open(bg_image_file) if bg_image_file else None

# --- Canvas ---
canvas_key = "canvas_reset" if clear_canvas else "canvas_active"
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

# --- Guardar como PNG ---
if save_canvas and canvas_result.image_data is not None:
    img = Image.fromarray(canvas_result.image_data.astype("uint8"), mode="RGBA")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button("⬇️ Descargar imagen", byte_im, file_name="mi_dibujo.png", mime="image/png")
    st.image(img, caption="Tu dibujo guardado", use_column_width=True)

# --- Analizar con GPT ---
if analyze_button:
    if not api_key:
        st.warning("⚠️ Por favor, ingresa tu clave API.")
    elif canvas_result.image_data is None:
        st.warning("⚠️ Dibuja algo antes de analizar.")
    else:
        with st.spinner("Analizando tu dibujo con GPT-4o..."):

            try:
                # Convertir imagen
                image_data = Image.fromarray(canvas_result.image_data.astype("uint8"), mode="RGBA")
                base64_img = encode_image(image_data)

                # Crear mensaje para GPT
                prompt = (
                    "A partir de esta imagen dibujada, crea una historia corta en español. "
                    "Incluye personajes, un lugar, una pequeña aventura, y un final imaginativo. "
                    "Sé creativo, visual y algo fantástico."
                )

                # Llamada a OpenAI
                os.environ["OPENAI_API_KEY"] = api_key
                openai.api_key = api_key
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{base64_img}",
                                    },
                                },
                            ],
                        }
                    ],
                    max_tokens=700,
                )

                story = response.choices[0].message.content
                st.success("✨ ¡Aquí está tu historia!")
                st.markdown(story)

            except Exception as e:
                st.error(f"Ocurrió un error al analizar la imagen: {e}")

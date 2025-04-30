import os
import streamlit as st
import base64
from openai import OpenAI
import openai
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas

# Función para codificar imagen en base64
def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image
    except FileNotFoundError:
        return "Error: La imagen no se encontró en la ruta especificada."

# Configuración de página
st.set_page_config(page_title='Tablero Inteligente')
st.title('🧠 Tablero Inteligente que Interpreta Dibujos')

# Configuración en la barra lateral
with st.sidebar:
    st.subheader("🖌️ Propiedades del Tablero")
    drawing_mode = st.selectbox(
        "Herramienta de Dibujo:",
        ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
    )
    stroke_width = st.slider('Grosor del trazo', 1, 30, 15)
    stroke_color = st.color_picker("Color del trazo", "#FFFFFF")
    bg_color = st.color_picker("Color de fondo", "#000000")
    st.markdown("---")
    api_key = st.text_input('🔑 Ingresa tu Clave de OpenAI', type="password")

st.subheader("🎨 Dibuja en el panel y genera una historia con tu arte")

# Crear el componente de canvas
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=300,
    width=500,
    drawing_mode=drawing_mode,
    key="canvas"
)

# Botón para analizar
analyze_button = st.button("📖 Analiza y cuenta una historia")

# Acción del botón
if canvas_result.image_data is not None and api_key and analyze_button:
    with st.spinner("Analizando tu dibujo..."):
        try:
            # Convertir y guardar imagen
            input_numpy_array = np.array(canvas_result.image_data)
            input_image = Image.fromarray(input_numpy_array.astype('uint8'), 'RGBA')
            input_image.save('img.png')

            # Codificar imagen en base64
            base64_image = encode_image_to_base64("img.png")

            # Prompt para GPT
            prompt_text = (
                "A partir de esta imagen dibujada, crea una historia corta en español, "
                "con personajes, un lugar y una pequeña aventura basada en lo que ves en el dibujo. "
                "Sé creativo y visual."
            )

            # Llamada a la API
            os.environ["OPENAI_API_KEY"] = api_key
            openai.api_key = api_key

            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt_text},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}",
                                },
                            },
                        ],
                    }
                ],
                max_tokens=600,
            )

            # Mostrar respuesta
            historia = response.choices[0].message.content
            st.success("✨ ¡Aquí está la historia generada!")
            st.markdown(historia)

        except Exception as e:
            st.error(f"Ocurrió un error al analizar la imagen: {e}")
else:
    if analyze_button:
        if not api_key:
            st.warning("⚠️ Por favor, ingresa tu API Key.")
        elif canvas_result.image_data is None:
            st.warning("⚠️ Dibuja algo antes de analizar.")

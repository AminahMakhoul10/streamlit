import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np


# Tentar carregar o modelo
try:
    model = load_model('modelo_cachorro_gato.keras')
    st.write("Modelo carregado com sucesso!")
except Exception as e:
    st.write(f"Erro ao carregar o modelo: {e}")

# Interface do Usuário
st.title("Classificador de Gatos e Cachorros")
st.write("Faça upload de uma imagem de um gato ou cachorro para classificação.")

# Upload da imagem
uploaded_file = st.file_uploader("Escolha uma imagem...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Carregar e exibir a imagem
    img = image.load_img(uploaded_file, target_size=(128, 128))  # Ajuste o tamanho se necessário
    st.image(img, caption="Imagem Carregada", use_container_width=True)

    # Pré-processamento da imagem
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Adicionar dimensão batch
    img_array /= 255.0  # Normalizar os valores dos pixels

    # Fazer predição
    prediction = model.predict(img_array)
    if prediction[0][0] > 0.5:  # Se a probabilidade for maior que 0.5, é cachorro
        st.write("**Resultado: Cachorro 🐶**")
    else:
        st.write("**Resultado: Gato 🐱**")

    # Exibir confiança da predição
    confidence = prediction[0][0] if prediction[0][0] > 0.5 else 1 - prediction[0][0]
    st.write(f"Confiança da predição: {confidence * 100:.2f}%")
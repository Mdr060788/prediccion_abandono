import streamlit as st
import numpy as np
from flask import Flask, request, jsonify, render_template, url_for
import pickle
from PIL import Image
#from sklearn import svm



# Path del modelo preentrenado
MODEL_PATH = '/home/mauro/Mis_proyectos_jupyter/Proyects/Codigos/abandono_cliente/pickle_model.pkl'


# Se recibe la imagen y el modelo, devuelve la predicción
def model_prediction(x_in, model):

    x = np.asarray(x_in).reshape(1,-1)
    preds=model.predict(x)

    return preds
    
#Funcion de clasificador
def classify(num):
    if num == 1:
        st.markdown("<h3 style='color: red;'>Cliente perdido 😞</h3>", unsafe_allow_html=True)
    else: 
        st.markdown("<h3 style='color: green;'>Cliente existente 😀</h3>", unsafe_allow_html=True)

    

def main():   
    model=''

    # Se carga el modelo
    if model=='':
        with open(MODEL_PATH, 'rb') as file:
            model = pickle.load(file)
    
    # Título
    html_temp = """
    <h1 style="color:#181082;text-align:center;">SISTEMA DE PREDICCIÓN DE ABANDONO </h1>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)

    #Reporte PBI
    st.components.v1.html(
    """
    <iframe title="customers_bank" width="700" height="400" src="https://app.powerbi.com/view?r=eyJrIjoiYjJhNGI3OGYtYTI0MC00ZmU4LWE5N2QtZjQ4ODI3YmQ2ZTFhIiwidCI6ImRmODY3OWNkLWE4MGUtNDVkOC05OWFjLWM4M2VkN2ZmOTVhMCJ9&pageName=ReportSection7c53cbaed9a20303b3eb" frameborder="0" allowFullScreen="true"></iframe>
    """,
    width=1000, height=400)


    # Mostrar campos del predictor    

    st.subheader('Modifique los valores para predecir si el cliente abandonará o no la empresa')
    # Lectura de datos
    
    # Diccionario que mapea los valores del selectbox a valores numéricos
    gender_map = {"Male (Masculino)": 1, 
                  "Female (Femenino)": 0
                 }

    # Crear selectbox para género y convertir a valor numérico
    gen = st.selectbox("Gender (Género):", options=
                       [
                        "Male (Masculino)", 
                        "Female (Femenino)"
                       ]
                      )
    gen_val = gender_map[gen]

    income_map = {
                'Unknown (Desconocido)':0,
                'Less than $40K (< 40k/año)':1,
                '$40K - $60K':2,
                '$60K - $80K':3,
                '$80K - $120K':4,
                '$120K +':5
                 }
    income = st.selectbox(
        'Income Category (Categoría de ingresos):', options=
                        [
                        'Unknown (Desconocido)',
                        'Less than $40K (< 40k/año)',
                        '$40K - $60K',
                        '$60K - $80K',
                        '$80K - $120K',
                        '$120K +'
                        ]
                        )
    income_val = income_map[income]

    # Definir los sliders 
    d_c = st.slider("Dependent count (Personas dependientes):", min_value=0, max_value=10, value=0, step=1, format="%d")
    m_o_b = st.slider("Months on book (Meses en la empresa):", min_value=0, max_value=60, value=0, step=1, format="%d")
    t_r_c = st.slider("Total Relationship Count (Cantidad de productos que el cliente utiliza):", min_value=1, max_value=6, value=0, step=1, format="%d")
    m_i_12_m = st.slider("Months Inactive 12 mon (Meses inactivos en el ultimo año):", min_value=0, max_value=12, value=0, step=1, format="%d")
    c_c_12_m = st.slider("Contacts Count 12 mon (Cantidad de contactos que el cliente ha tenido en los últimos 12 meses.):", min_value=0, max_value=5, value=0, step=1, format="%d")
    t_t_c = st.slider("Total Trans Ct (Cantidad de transacciones realizadas en los últimos 12 meses.):", min_value=0, max_value=200, value=0, step=1, format="%d")
    t_c_c_q4 = st.slider("Total Ct Chng Q4 Q1 (Cambio porcentual en la cantidad total de transacciones realizadas en el cuarto trimestre con respecto al primer trimestre.):", min_value=0.0, max_value=400.0, step=1.0, value=0.0, format="%.2f %%")
    t_t_a = st.slider("Total Trans Amt (Monto total de transacciones realizadas en los últimos 12 meses.):", min_value=0, max_value=20000, value=0, step=1, format="%d U$S")
    t_a_c_q4 = st.slider("Total Amt Chng Q4 Q1 (Cambio porcentual en el monto de transacciones realizadas en el cuarto trimestre con respecto al primer trimestre.):", min_value=0.0, max_value=400.0, step=1.0, value=0.0, format="%.2f %%")

    # El botón predicción se usa para iniciar el procesamiento
    if st.button("Hacer predicción :"): 

        x_in =[     
                np.int_(gen_val),
                np.int_(income_val),
                np.int_(d_c),
                np.int_(m_o_b),
                np.int_(t_r_c),
                np.int_(m_i_12_m),
                np.int_(c_c_12_m),
                np.float_(t_a_c_q4),
                np.float_(t_t_a),
                np.float_(t_t_c),
                np.float_(t_c_c_q4),
              ]

        predictS = model_prediction(x_in, model)
        result = classify(predictS[0])

if __name__ == '__main__':
    main()

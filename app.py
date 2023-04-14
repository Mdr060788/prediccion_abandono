import streamlit as st
import numpy as np
import pandas as pd
import pickle
from PIL import Image

# Path del modelo preentrenado
MODEL_PATH = '/home/mauro/Mis_proyectos_jupyter/Proyects/Codigos/abandono_cliente/pickle_model.pkl'

# Se recibe la entrada y el modelo, devuelve la predicción
def model_prediction(x_in, model):
    x = np.asarray(x_in).reshape(1,-1)
    y_pred = model.predict(x)[0]
    return y_pred

def model_prediction_lot(X_lot, model):
    X = np.asarray(X_lot).reshape(len(X_lot), -1)
    y_preds = model.predict(X)
    return y_preds
   
#Funcion de clasificador
def classify(y_pred):
    if y_pred == 1:
        st.markdown("<h3 style='color: red;'>Cliente perdido 😞</h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='color: green;'>Cliente existente 😀</h3>", unsafe_allow_html=True)

def classify2(y_preds):
    labels = []
    for y in y_preds:
        if y == 1:
            labels.append("Perdido 😞")
        else:
            labels.append("Existente 😀")
    return labels

def download_link(df, file_name, file_type):
    if file_type == 'csv':
        df.to_csv(file_name, index=False)
    elif file_type == 'xlsx':
        df.to_excel(file_name, index=False)
    with open(file_name, 'rb') as f:
        file_bytes = f.read()
        st.download_button(label='Descargar ' + file_type.upper(), data=file_bytes, file_name=file_name, mime=file_type)

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

    #Reportes
    report_type = st.selectbox('Seleccione un reporte', ['', 'Power BI', 'Looker Studio'], index=0)

    if report_type == 'Power BI':
        st.markdown(
            """
            <div style="position: relative; overflow: hidden; padding-top: 75%; height: 0;">
                <iframe src="https://app.powerbi.com/view?r=eyJrIjoiNDI2M2Q0MGYtMWJmMy00MzAxLWI4OTMtM2Y3OTM0NGM0ZjUyIiwidCI6ImRmODY3OWNkLWE4MGUtNDVkOC05OWFjLWM4M2VkN2ZmOTVhMCJ9" 
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;"></iframe>
            </div>
            """,
            unsafe_allow_html=True
        )
    if report_type == 'Looker Studio':
        st.markdown(
            """
            <div style="position: relative; overflow: hidden; padding-top: 75%; height: 0;">
                <iframe src="https://lookerstudio.google.com/embed/reporting/ddbf619f-01d4-4203-8373-c7b62c489124/page/RyiMD" 
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;"></iframe>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.subheader('Seleccione de que forma será la entrada de datos')
    opt_pred = st.selectbox("Entrada", ["", "Un cliente", "Lote de clientes"], index=0)
 
    if opt_pred == "Un cliente":
        # Mostrar campos del predictor    
        st.subheader('Modifique los valores para predecir si el cliente abandonará o no la empresa')
       
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
        m_i_12_m = st.slider("Months Inactive 12 mon (Meses inactivos en el ultimo año):", min_value=0, max_value=6, value=0, step=1, format="%d")
        c_c_12_m = st.slider("Contacts Count 12 mon (Cantidad de contactos que el cliente ha tenido en los últimos 12 meses.):", min_value=0, max_value=5, value=0, step=1, format="%d")
        t_t_c = st.slider("Total Trans Ct (Cantidad de transacciones realizadas en los últimos 12 meses.):", min_value=0, max_value=200, value=0, step=1, format="%d")
        t_c_c_q4 = st.slider("Total Ct Chng Q4 Q1 (Cambio porcentual en la cantidad total de transacciones realizadas en el cuarto trimestre con respecto al primer trimestre.):", min_value=0.000, max_value=400.0, step=0.1, value=0.0, format="%.2f %%")
        t_t_a = st.slider("Total Trans Amt (Monto total de transacciones realizadas en los últimos 12 meses.):", min_value=0, max_value=20000, value=0, step=1, format="%d U$S")
        t_a_c_q4 = st.slider("Total Amt Chng Q4 Q1 (Cambio porcentual en el monto de transacciones realizadas en el cuarto trimestre con respecto al primer trimestre.):", min_value=0.000, max_value=400.0, step=0.1, value=0.0, format="%.2f %%")

        # El botón predicción se usa para iniciar el procesamiento
        if st.button("Hacer predicción :"):

            # Atención con el orden de entrada al modelo, la forma correcta es:                
            #Gender	
            #Income_Category	
            #Dependent_count	
            #Months_on_book	
            #Total_Relationship_Count	
            #Months_Inactive_12_mon	
            #Contacts_Count_12_mon	
            #Total_Amt_Chng_Q4_Q1	
            #Total_Trans_Amt	
            #Total_Trans_Ct	
            #Total_Ct_Chng_Q4_Q1

            x_in =[    
                    np.int_(gen_val),
                    np.int_(income_val),
                    np.int_(d_c),
                    np.int_(m_o_b),
                    np.int_(t_r_c),
                    np.int_(m_i_12_m),
                    np.int_(c_c_12_m),
                    np.float_(t_a_c_q4)/100,
                    np.float_(t_t_a),
                    np.float_(t_t_c),
                    np.float_(t_c_c_q4)/100,
                ]
            #st.write(x_in)
            
            #Relizar prediccion
            predictS = model_prediction(x_in, model)
            result = classify(predictS)
            return result
        
    if opt_pred == "Lote de clientes":
        uploaded_file = st.file_uploader("Cargar archivo CSV", type="csv")
        if uploaded_file is not None:
            # Transformación de datos
            df = pd.read_csv(uploaded_file)
            st.write(df)

            # Convertir las columnas:

            data = {'gender': df['Género'].replace({'F': 0, 'M': 1}).astype(int),
                    'Income_Category': df['Cat. Ingresos'].replace({
                                                    'Unknown':0,
                                                    'Less than $40K':1,
                                                    '$40K - $60K':2,
                                                    '$60K - $80K':3,
                                                    '$80K - $120K':4,
                                                    '$120K +':5
                                                    }).astype(int),
                    'Dependent_count': df['Nº Depend.'],
                    'Months_on_book': df['Antigüedad'],
                    'Total_Relationship_Count': df['Ct. Prod.'],
                    'Months_Inactive_12_mon': df['Meses inact.'],
                    'Contacts_Count_12_mon': df['Contactos'],
                    'Total_Trans_Ct': df['Ct Trans.'],
                    'Total_Ct_Chng_Q4_Q1': df['% var ct tr Q4/Q3'].str.strip().str.replace('%', '').str.replace(',', '.').astype(float),
                    'Total_Trans_Amt': df['$ Tot. Trans.'].str.replace('$', '').astype(int),
                    'Total_Amt_Chng_Q4_Q1': df['% var $ tr Q4/Q3'].str.strip().str.replace('%', '').str.replace(',', '.').astype(float)
                    }
            
            #dff = pd.DataFrame(data)
            #st.write(dff)

            if st.button('Predecir lote'):

                X_lot = np.array([data['gender'],
                            data['Income_Category'],
                            data['Dependent_count'],
                            data['Months_on_book'],
                            data['Total_Relationship_Count'],
                            data['Months_Inactive_12_mon'],
                            data['Contacts_Count_12_mon'],
                            data['Total_Amt_Chng_Q4_Q1'],
                            data['Total_Trans_Amt'],
                            data['Total_Trans_Ct'],
                            data['Total_Ct_Chng_Q4_Q1']]).T
               
                st.write(X_lot)

                # Hacer la predicción
                st.spinner('Realizando predicciones...')
                y_predictS = model_prediction_lot(X_lot, model)
                labels = classify2(y_predictS)


                # Mostrar resultados
                st.success('👇 Resultados de la predicción 👇')
                df.insert(0, 'Predicción', labels)
                st.write(df)

                # Calcular perdidos
                total = len(df)
                estado_perdido = "Perdido 😞"
                perdidos = len(df[df['Predicción'] == estado_perdido])
                porcentaje_perdidos = (perdidos / total) * 100

                # Porcentaje_perdidos
                st.subheader(f"El número de clientes considerados perdidos es de {perdidos} y representan el {porcentaje_perdidos:.1f} % de los {total}")

                # Agregar botón de descarga de CSV
                download_link(df, 'data.csv', 'csv')

                # Agregar botón de descarga de Excel
                #download_link(df, 'data.xlsx', 'xlsx')

if __name__ == '__main__':
    main()
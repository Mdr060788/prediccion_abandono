# Streamlit: App ML para predicción de abandono + Reportes en Power BI y Looker Studio
![App](https://github.com/Mdr060788/prediccion_abandono/blob/main/assets/logo.jpeg)

Este proyecto está creado a partir de un notebook donde se entrena un modelo de clasificación, con los datos públicos del dataset "BankChurner" de Kaggle,
para predecir el abandono de clientes. 
Luego de limpiar y preparar los datos, se entrenó y seleccionó un modelo de clasificación binaria de regresión logística. La base para el notebook fué tomada 
de un proyecto sobre el stroke de Jordi Olle. 
Finalizado el proceso, guardé el modelo entrenado en un archivo de formato pkl. 
El siguiente paso fue crear una aplicación que pudiera tomar los datos del usuario y hacer la predicción. 
Utilicé la biblioteca Streamlit, en el proyecto he integrado dos repotes con dos herramientas de análisis, Power Bi y Looker Studio.

![App](https://github.com/Mdr060788/prediccion_abandono/blob/main/assets/reportes.gif)

Supongamos que el usuario observará un caso en particular, basándose en su reporte con datos actualizados y nunca vistos por el modelo predictivo (esa es la idea).
Ingresará todas esas características en los comandos de la interfaz y podrá hacer la predicción de forma unitaria.

![App](https://github.com/Mdr060788/prediccion_abandono/blob/main/assets/linea.jpg)

Ahora imaginemos que ya no queremos predecir uno por uno porque es una tarea bastante pesada, sino que queremos analizar un conjunto de clientes con ciertas características.
Un lote de clientes. En este caso por ejemplo, podríamos filtrar en el reporte los clientes que hace 6 meses no operan en la empresa, y luego exportar el listado…
A continuación, seleccionamos la opción de entrada de datos con “Lote de clientes”, y subimos nuestro archivo CSV.
Aparecerá una vista previa del listado que hemos cargado. Le damos al botón predecir...

![App](https://github.com/Mdr060788/prediccion_abandono/blob/main/assets/prediccion.gif)

Y saldrá el listado donde la primera columna será el resultado de cada predicción, además, tendremos un mensaje con la cantidad de clientes en condición de 
“Perdidos”, el % que representan del total, y la posibilidad poder exportar nuestro listado para tomar medidas estratégicas y recuperarlos nuevamente.

Si quiere ver el artículo completo: https://medium.com/@maurodanielrossi/app-web-ml-streamlit-power-bi-looker-s-5659aafe36f9

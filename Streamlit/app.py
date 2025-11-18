import streamlit as st
import pandas as pd
import io
import sys
import os
import matplotlib.pyplot as plt
import seaborn as sns

RUTA_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if RUTA_BASE not in sys.path:
    sys.path.append(RUTA_BASE)


from src.eda.ProcesadorEDA import ProcesadorEDA

# ----------------------------------------------------------
# CONFIG GENERAL
# ----------------------------------------------------------
st.set_page_config(
    page_title="Proyecto Premier League",
    page_icon="⚽",
    layout="wide"
)

ruta_limpio = "src/data/processed/premier_clean.csv"

# ----------------------------------------------------------
# ESTADO: para saber qué botón se presionó
# ----------------------------------------------------------
if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"

# ----------------------------------------------------------
# MENÚ LATERAL CON BOTONES
# ----------------------------------------------------------
st.sidebar.title("Menú principal")

if st.sidebar.button("🏠 Inicio"):
    st.session_state.pagina = "Inicio"

if st.sidebar.button("📂 Ver Dataset"):
    st.session_state.pagina = "Dataset"

if st.sidebar.button("📊 Gráficos"):
    st.session_state.pagina = "Graficos"

# ----------------------------------------------------------
# CONTENIDO DE CADA SECCIÓN
# ----------------------------------------------------------

# 🌸 PORTADA
if st.session_state.pagina == "Inicio":
    st.title("⚽ Proyecto de Análisis de Datos – Premier League")
    st.markdown("""
    ### **Curso:** Programación II – Big Data  
    ### **Estudiantes:** Evelyn & Compañero  
    ---
    """)

# 📂 DATASET
elif st.session_state.pagina == "Dataset":
    st.header("📂 Dataset Limpio")

    # Cargar usando ProcesadorEDA
    if os.path.exists(ruta_limpio):
        df_raw = pd.read_csv(ruta_limpio)
        eda = ProcesadorEDA(df_raw, ruta_limpio)

        # Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "👁 Vista previa",
            "ℹ Información",
            "📊 Estadísticas",
            "🔢 Categóricas",
            "🧮 Correlación"
        ])

        # ---------- TAB 1: Vista previa ----------
        with tab1:
            st.subheader("Vista previa")
            st.dataframe(eda.df)
            st.write(f"**Filas:** {eda.df.shape[0]}")
            st.write(f"**Columnas:** {eda.df.shape[1]}")

        # ---------- TAB 2: Información ----------
        with tab2:
            st.subheader("Información del dataset")

            buffer = io.StringIO()
            eda.df.info(buf=buffer)
            st.text(buffer.getvalue())

        # ---------- TAB 3: Estadísticas ----------
        with tab3:
            st.subheader("Estadísticas")
            resumen = eda.resumen_descriptivo()
            st.dataframe(resumen)

        # ---------- TAB 4: Categóricas ----------
        with tab4:
            st.subheader("Valores categóricos")
            cols_cat = eda.df.select_dtypes(include=["object"]).columns
            for col in cols_cat:
                st.markdown(f"### {col}")
                st.write(eda.df[col].value_counts())

        # ---------- TAB 5: Correlación ----------
        with tab5:
            st.subheader("Matriz de correlación")

            corr = eda.matriz_correlacion()

            # Mostrar tabla
            st.dataframe(corr)

            # ---------------------
            # Heatmap gráfico
            # ---------------------

            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
            st.pyplot(fig)

    else:
        st.error("No se encontró el archivo.")

# 📊 GRÁFICOS
elif st.session_state.pagina == "Graficos":
    st.header("📊 Visualización de Datos")

    if not os.path.exists(ruta_limpio):
        st.error("⚠️ No se encontró el archivo limpio.")
    else:
        df = pd.read_csv(ruta_limpio)

        tabA, tabB, tabC = st.tabs([
            "📈 Histogramas",
            "📉 Líneas",
            "🎯 Comparaciones"
        ])

        with tabA:
            col = st.selectbox(
                "Selecciona columna numérica:",
                df.select_dtypes(include=['int64','float64']).columns
            )
            st.bar_chart(df[col])

        with tabB:
            col = st.selectbox(
                "Selecciona variable para línea:",
                df.select_dtypes(include=['int64','float64']).columns,
                key="linea"
            )
            st.line_chart(df[col])

        with tabC:
            col1 = st.selectbox(
                "Columna 1:",
                df.select_dtypes(include=['int64','float64']).columns,
                key="c1"
            )
            col2 = st.selectbox(
                "Columna 2:",
                df.select_dtypes(include=['int64','float64']).columns,
                key="c2"
            )
            st.scatter_chart(df[[col1, col2]])

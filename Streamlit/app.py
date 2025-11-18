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
from visualizacion.visualizador import Visualizador


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
    st.title("⚽ Proyecto 2 Programación - Análisis de la Premier League")
    st.markdown("""
    ### **Curso:** Programación II – Big Data  
    ### **Estudiantes:** Evelyn Calderón / Steven Vindas
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
    st.header("📊 Visualización del Proyecto")

    if not os.path.exists(ruta_limpio):
        st.error("No se encontró el archivo limpio.")
    else:
        df = pd.read_csv(ruta_limpio)

        from visualizacion.visualizador import Visualizador
        viz = Visualizador(df)

        # Tabs de la clase Visualizador
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "👟 Top goleadores",
            "👟 Top asistidores",
            "👟 Goles por país (equipo)",
            "👟 Distribución de edades",
            "👟 Amarillas por equipo",
            "👟 Goles por posición"
        ])

        import matplotlib.pyplot as plt

        # 1) TOP GOLEADORES
        with tab1:
            datos = df.nlargest(10, "Goals")
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(datos["Player"], datos["Goals"])
            ax.set_title("Top 10 Goleadores")
            ax.invert_yaxis()
            st.pyplot(fig)

        # 2) TOP ASISTIDORES
        with tab2:
            datos = df.nlargest(10, "Assists")
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(datos["Player"], datos["Assists"], marker="o")
            plt.xticks(rotation=45, ha="right")
            ax.set_title("Top 10 Asistidores")
            st.pyplot(fig)

        # 3) GOLES POR PAÍS EN EQUIPO
        with tab3:
            equipo = st.selectbox("Selecciona un equipo:", df["Team"].unique())
            datos = df[df["Team"] == equipo]

            if datos.empty:
                st.warning("No hay datos para este equipo.")
            else:
                goles_por_pais = datos.groupby("Nation")["Goals"].sum()
                fig, ax = plt.subplots(figsize=(8, 8))
                ax.pie(goles_por_pais, labels=goles_por_pais.index, autopct="%1.1f%%")
                ax.set_title(f"Goles por nacionalidad en {equipo}")
                st.pyplot(fig)

        # 4) DISTRIBUCIÓN DE EDADES
        with tab4:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(df["Age"], bins=15)
            ax.set_title("Distribución de edades en la Premier League")
            st.pyplot(fig)

        # 5) AMARILLAS POR EQUIPO
        with tab5:
            datos = df.groupby("Team")["Yellow_Cards"].sum().sort_values()
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.barh(datos.index, datos.values)
            ax.set_title("Tarjetas Amarillas por Equipo")
            st.pyplot(fig)

        # 6) GOLES POR POSICIÓN
        with tab6:
            datos = df.groupby("Position")["Goals"].sum().sort_values(ascending=False).head(10)
            fig, ax = plt.subplots(figsize=(10, 6))
            datos.plot(kind="bar", ax=ax)
            ax.set_title("Top Posiciones con Más Goles")
            plt.xticks(rotation=45)
            st.pyplot(fig)

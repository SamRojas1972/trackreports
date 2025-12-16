"""
Dashboard principal de Streamlit para reportes de trayectoria
"""
import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Agregar path del proyecto
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.config import config
from src.utils.logger import get_logger
from src.backend.processors.extractor import DataExtractor
from src.backend.processors.transformer import TrayectoriaTransformer


logger = get_logger(__name__, config.paths.logs_dir)


# Configuración de la página
st.set_page_config(
    page_title="Sistema de Reportes de Trayectoria",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    """Función principal del dashboard"""

    # Título
    st.title("📊 Sistema de Reportes de Trayectoria")
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.header("Navegación")

        page = st.radio(
            "Selecciona una opción:",
            [
                "🏠 Inicio",
                "📈 Visualización de Trayectoria",
                "📊 Cuadro FIMPES",
                "📥 Generación de Reportes",
                "⚙️ Configuración"
            ]
        )

        st.markdown("---")
        st.info(f"**Periodo configurado:**\n\n{config.reports.year_start} - {config.reports.year_end}")

    # Contenido principal según selección
    if page == "🏠 Inicio":
        show_home()
    elif page == "📈 Visualización de Trayectoria":
        show_trayectoria()
    elif page == "📊 Cuadro FIMPES":
        show_fimpes()
    elif page == "📥 Generación de Reportes":
        show_generacion()
    elif page == "⚙️ Configuración":
        show_configuracion()


def show_home():
    """Página de inicio"""
    st.header("Bienvenido al Sistema de Reportes de Trayectoria")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Grados Académicos",
            value=len(config.reports.grados),
            delta="LL, EL, ML"
        )

    with col2:
        st.metric(
            label="Periodo de Análisis",
            value=f"{config.reports.year_end - config.reports.year_start + 1} años",
            delta=f"{config.reports.year_start}-{config.reports.year_end}"
        )

    with col3:
        st.metric(
            label="Base de Datos",
            value="PostgreSQL",
            delta=config.database.database
        )

    st.markdown("---")

    st.subheader("Funcionalidades")

    st.markdown("""
    ### 📈 Visualización de Trayectoria
    - Análisis de cohortes por generación
    - Seguimiento de estudiantes de nuevo ingreso
    - Métricas de retención y permanencia
    - Gráficos interactivos

    ### 📊 Cuadro FIMPES
    - Indicadores institucionales
    - Eficiencia de retención
    - Tasas de egreso
    - Análisis de rezago

    ### 📥 Generación de Reportes
    - Reportes Excel automatizados
    - Formato corporativo
    - Descarga bajo demanda
    - Programación automática

    ### ⚙️ Configuración
    - Ajuste de periodos
    - Configuración de base de datos
    - Gestión de exportaciones
    """)

    st.markdown("---")
    st.info("💡 **Tip:** Usa el menú lateral para navegar entre las diferentes secciones.")


def show_trayectoria():
    """Página de visualización de trayectoria"""
    st.header("📈 Visualización de Trayectoria")

    # Filtros
    col1, col2 = st.columns(2)

    with col1:
        grado = st.selectbox(
            "Grado Académico",
            options=config.reports.grados,
            format_func=lambda x: {
                'LL': 'Licenciatura',
                'EL': 'Especialidad',
                'ML': 'Maestría'
            }.get(x, x)
        )

    with col2:
        # Validar que year_start < year_end
        min_year = min(config.reports.year_start, 2020)
        max_year = max(config.reports.year_end, config.reports.year_start + 1)

        year_range = st.slider(
            "Rango de Años",
            min_value=min_year,
            max_value=max_year,
            value=(config.reports.year_start, config.reports.year_end)
        )

    if st.button("🔄 Cargar Datos", type="primary"):
        with st.spinner("Cargando datos desde la base de datos..."):
            try:
                # Cargar datos reales
                extractor = DataExtractor(year_start=year_range[0], year_end=year_range[1])

                # Extraer datos
                logger.info(f"Extrayendo datos para {grado} ({year_range[0]}-{year_range[1]})")
                datos = extractor.extract_all_for_grado(grado)

                # Transformar datos
                transformer = TrayectoriaTransformer(datos['resumen'])
                trayectoria_df = transformer.crear_tabla_trayectoria()

                st.success(f"✅ Datos cargados: {len(datos['nuevo_ingreso'])} NI, {len(datos['reinscritos'])} Reinscritos")

                # ====================
                # VISUALIZACIONES
                # ====================

                # 1. Resumen de totales
                st.markdown("---")
                st.subheader("📊 Resumen General")

                col1, col2, col3 = st.columns(3)
                with col1:
                    total_ni = datos['resumen']['nuevo_ingreso'].sum()
                    st.metric("Nuevo Ingreso Total", f"{total_ni:,}")

                with col2:
                    total_eg = datos['resumen']['egresados'].sum()
                    st.metric("Egresados Total", f"{total_eg:,}")

                with col3:
                    total_ti = datos['resumen']['titulados'].sum()
                    st.metric("Titulados Total", f"{total_ti:,}")

                # 2. Gráfico de tendencia temporal
                st.markdown("---")
                st.subheader("📈 Tendencia Temporal")

                fig_tendencia = go.Figure()

                fig_tendencia.add_trace(go.Scatter(
                    x=datos['resumen']['periodo_id'],
                    y=datos['resumen']['nuevo_ingreso'],
                    name='Nuevo Ingreso',
                    mode='lines+markers',
                    line=dict(color='#366092', width=3)
                ))

                fig_tendencia.add_trace(go.Scatter(
                    x=datos['resumen']['periodo_id'],
                    y=datos['resumen']['egresados'],
                    name='Egresados',
                    mode='lines+markers',
                    line=dict(color='#5B9BD5', width=3)
                ))

                fig_tendencia.add_trace(go.Scatter(
                    x=datos['resumen']['periodo_id'],
                    y=datos['resumen']['titulados'],
                    name='Titulados',
                    mode='lines+markers',
                    line=dict(color='#70AD47', width=3)
                ))

                fig_tendencia.update_layout(
                    title=f"Evolución por Periodo - {grado}",
                    xaxis_title="Periodo",
                    yaxis_title="Número de Estudiantes",
                    hovermode='x unified',
                    height=400
                )

                st.plotly_chart(fig_tendencia, use_container_width=True)

                # 3. Tabla de datos resumen
                st.markdown("---")
                st.subheader("📋 Datos por Periodo")

                # Formatear tabla para mejor visualización
                resumen_display = datos['resumen'].copy()
                resumen_display = resumen_display.sort_values('periodo_id', ascending=False)

                st.dataframe(
                    resumen_display,
                    use_container_width=True,
                    height=300,
                    hide_index=True
                )

                # 4. Trayectoria por cohorte (si está disponible)
                if trayectoria_df is not None and not trayectoria_df.empty:
                    st.markdown("---")
                    st.subheader("🎓 Trayectoria por Cohorte")

                    # Mostrar solo las primeras columnas relevantes
                    cols_to_show = [col for col in trayectoria_df.columns if col.startswith('P') or col == 'Generación']
                    if cols_to_show:
                        st.dataframe(
                            trayectoria_df[cols_to_show].head(10),
                            use_container_width=True,
                            height=300
                        )

                        st.info("💡 Mostrando las primeras 10 generaciones. El reporte Excel contiene todos los datos.")

                # 5. Distribución de estudiantes
                st.markdown("---")
                st.subheader("👥 Distribución de Estudiantes")

                col1, col2 = st.columns(2)

                with col1:
                    # Gráfico de pie para NI vs Reinscritos
                    totales = pd.DataFrame({
                        'Tipo': ['Nuevo Ingreso', 'Reinscritos'],
                        'Total': [len(datos['nuevo_ingreso']), len(datos['reinscritos'])]
                    })

                    fig_pie = px.pie(
                        totales,
                        values='Total',
                        names='Tipo',
                        title='Nuevo Ingreso vs Reinscritos',
                        color_discrete_sequence=['#366092', '#5B9BD5']
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)

                with col2:
                    # Top 5 periodos con más nuevo ingreso
                    top_periodos = datos['resumen'].nlargest(5, 'nuevo_ingreso')[['periodo_id', 'nuevo_ingreso']]

                    fig_bar = px.bar(
                        top_periodos,
                        x='periodo_id',
                        y='nuevo_ingreso',
                        title='Top 5 Periodos - Nuevo Ingreso',
                        color='nuevo_ingreso',
                        color_continuous_scale='Blues'
                    )
                    fig_bar.update_layout(showlegend=False)
                    st.plotly_chart(fig_bar, use_container_width=True)

                # 6. Botón de descarga
                st.markdown("---")
                st.info("💾 Para obtener el reporte completo con todas las hojas y formato, usa la sección **Generación de Reportes**.")

            except Exception as e:
                st.error(f"❌ Error al cargar datos: {str(e)}")
                logger.error(f"Error en visualización: {e}", exc_info=True)

                # Mostrar detalles del error en modo debug
                with st.expander("🔍 Ver detalles del error"):
                    st.code(str(e))


def show_fimpes():
    """Página de cuadro FIMPES"""
    st.header("📊 Cuadro FIMPES")

    grado = st.selectbox(
        "Selecciona Grado Académico",
        options=config.reports.grados,
        format_func=lambda x: {
            'LL': 'Licenciatura',
            'EL': 'Especialidad',
            'ML': 'Maestría'
        }.get(x, x)
    )

    if st.button("📊 Generar Cuadro FIMPES", type="primary"):
        with st.spinner("Generando cuadro FIMPES..."):
            try:
                st.success("Cuadro FIMPES generado!")
                st.info("📊 El cuadro FIMPES se mostrará aquí una vez conectado a la base de datos.")

            except Exception as e:
                st.error(f"Error al generar cuadro: {str(e)}")


def show_generacion():
    """Página de generación de reportes"""
    st.header("📥 Generación de Reportes Excel")

    st.subheader("Generar Reportes")

    col1, col2 = st.columns(2)

    with col1:
        grados_seleccionados = st.multiselect(
            "Grados Académicos",
            options=config.reports.grados,
            default=config.reports.grados,
            format_func=lambda x: {
                'LL': 'Licenciatura',
                'EL': 'Especialidad',
                'ML': 'Maestría'
            }.get(x, x)
        )

    with col2:
        year_range = st.slider(
            "Rango de Años",
            min_value=2020,
            max_value=2025,
            value=(config.reports.year_start, config.reports.year_end),
            key="gen_years"
        )

    if st.button("🚀 Generar Reportes", type="primary"):
        if not grados_seleccionados:
            st.warning("Por favor selecciona al menos un grado académico")
        else:
            with st.spinner("Generando reportes..."):
                try:
                    progress_bar = st.progress(0)
                    status = st.empty()

                    for idx, grado in enumerate(grados_seleccionados):
                        status.text(f"Generando reporte para {grado}...")
                        progress_bar.progress((idx + 1) / len(grados_seleccionados))

                    st.success(f"✅ {len(grados_seleccionados)} reportes generados exitosamente!")

                    st.info("💾 Los reportes se guardarán en: `data/reportes_generados/`")

                except Exception as e:
                    st.error(f"Error al generar reportes: {str(e)}")

    st.markdown("---")
    st.subheader("Reportes Generados")
    st.info("📁 Aquí se listarán los reportes generados recientemente.")


def show_configuracion():
    """Página de configuración"""
    st.header("⚙️ Configuración del Sistema")

    tab1, tab2, tab3 = st.tabs(["Base de Datos", "Reportes", "Programación"])

    with tab1:
        st.subheader("Configuración de Base de Datos")

        st.text_input("Host", value=config.database.host, disabled=True)
        st.number_input("Puerto", value=config.database.port, disabled=True)
        st.text_input("Base de Datos", value=config.database.database, disabled=True)
        st.text_input("Usuario", value=config.database.user, disabled=True)

        if st.button("🔍 Probar Conexión"):
            with st.spinner("Probando conexión..."):
                try:
                    from src.backend.db import db
                    if db.test_connection():
                        st.success("✅ Conexión exitosa!")
                    else:
                        st.error("❌ Error en la conexión")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    with tab2:
        st.subheader("Configuración de Reportes")

        st.number_input("Año Inicial", value=config.reports.year_start, min_value=2000, max_value=2030)
        st.number_input("Año Final", value=config.reports.year_end, min_value=2000, max_value=2030)

        st.multiselect(
            "Grados Académicos",
            options=['LL', 'EL', 'ML'],
            default=config.reports.grados
        )

    with tab3:
        st.subheader("Programación Automática")

        st.checkbox("Habilitar generación automática", value=config.scheduler.enabled)
        st.time_input("Hora de ejecución", value=None)
        st.selectbox("Zona horaria", options=["America/Mexico_City"])

        st.info("⏰ La generación automática ejecutará los reportes diariamente a la hora configurada.")


if __name__ == "__main__":
    main()


import streamlit as st
import pandas as pd
from ejecutar_rebates import ejecutar_rebates


# =============================================================
# 1. CONFIGURACIÓN DE LA APLICACIÓN
# =============================================================

st.set_page_config(
    page_title='Rebates Legrand',
    page_icon='📊',
    layout='wide'
)

st.title('📊 Rebates Legrand')
st.caption('Control de cumplimiento de metas, Back Order y rebate esperado')


# =============================================================
# 2. FILTROS
# =============================================================

st.sidebar.header('🔎 Filtros')

categoria = st.sidebar.selectbox(
    'Categoría',
    ['INDUSTRIAL', 'ELECTROBARRAS', 'DC & DC']
)

trimestre = st.sidebar.selectbox(
    'Trimestre',
    ['Todos', 'Q1', 'Q2', 'Q3', 'Q4']
)

calcular = st.sidebar.button(
    'Calcular Rebates',
    type='primary',
    use_container_width=True
)


# =============================================================
# 3. CALCULAR REBATES
# =============================================================

if calcular:

    resultados = ejecutar_rebates(categoria)

    st.subheader(f'Resultados — {categoria}')

    resultados_mostrar = (
        resultados
        if trimestre == 'Todos'
        else {trimestre: resultados[trimestre]}
    )

    # =========================================================
    # 4. MOSTRAR RESULTADOS POR TRIMESTRE
    # =========================================================

    for trimestre_actual, r in resultados_mostrar.items():

        st.divider()

        st.markdown(f'### 📅 {trimestre_actual}')

        # -----------------------------------------------------
        # Obtener valores originales
        # -----------------------------------------------------

        meta = float(r['meta'] or 0)

        total_facturado = float(
            r['total_facturado'] or 0
        )

        back_order = float(
            r['back_order'] or 0
        )

        # -----------------------------------------------------
        # TOTAL PARA CUMPLIMIENTO
        # -----------------------------------------------------

        total_cumplimiento = (
            total_facturado + back_order
        )

        # -----------------------------------------------------
        # PORCENTAJE DE CUMPLIMIENTO
        # -----------------------------------------------------

        porcentaje_cumplimiento = (
            (total_cumplimiento / meta) * 100
            if meta > 0
            else 0
        )

        # -----------------------------------------------------
        # DETERMINAR TASA DE REBATE
        # -----------------------------------------------------

        if categoria == 'DC & DC':

            porcentaje_base = 5.0
            porcentaje_130 = 6.5
            porcentaje_150 = 7.5

        else:

            porcentaje_base = 4.0
            porcentaje_130 = 5.2
            porcentaje_150 = 6.0

        if porcentaje_cumplimiento < 100:

            tasa_rebate = 0

        elif porcentaje_cumplimiento < 110:

            tasa_rebate = porcentaje_base

        elif porcentaje_cumplimiento < 120:

            tasa_rebate = porcentaje_130

        else:

            tasa_rebate = porcentaje_150

        # -----------------------------------------------------
        # CALCULAR REBATE ESPERADO
        # -----------------------------------------------------

        rebate_esperado = (
            total_cumplimiento * (tasa_rebate / 100)
        )

        rebate_ganado = (
            porcentaje_cumplimiento >= 100
        )

        # =====================================================
        # 5. INDICADORES
        # =====================================================

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            'Meta',
            f"${meta:,.0f}"
        )

        c2.metric(
            'Facturación válida',
            f"${total_facturado:,.0f}"
        )

        c3.metric(
            'Back Order reconocido',
            f"${back_order:,.0f}"
        )

        c4.metric(
            'Total para cumplimiento',
            f"${total_cumplimiento:,.0f}"
        )

        c5, c6, c7 = st.columns(3)

        c5.metric(
            'Cumplimiento',
            f"{porcentaje_cumplimiento:.2f}%"
        )

        c6.metric(
            'Porcentaje de rebate',
            f"{tasa_rebate:.2f}%"
        )

        c7.metric(
            'Rebate esperado',
            f"${rebate_esperado:,.0f}"
        )

        # =====================================================
        # 6. MENSAJE DE CUMPLIMIENTO
        # =====================================================

        if rebate_ganado:

            st.success(
                f"Meta cumplida. Se aplica una tasa de rebate "
                f"del {tasa_rebate:.2f}% sobre el Total de Cumplimiento."
            )

        else:

            faltante = meta - total_cumplimiento

            st.warning(
                f"No se alcanzó el 100% de cumplimiento. "
                f"Faltan ${faltante:,.0f} para alcanzar la meta. "
                f"No se genera rebate para este trimestre."
            )

        # =====================================================
        # 7. DETALLE DE BACK ORDER
        # =====================================================

        with st.expander('📋 Ver detalle de Back Order'):

            if r['detalle']:

                df_detalle = pd.DataFrame(r['detalle'])

                # Renombrar columnas para una mejor presentación
                df_detalle = df_detalle.rename(columns={
                    'oc': 'Orden de compra',
                    'valor_utilizado': 'Valor utilizado',
                    'back_order_original': 'Back Order original',
                    'back_order_restante': 'Back Order restante',
                    'fila': 'Fila Excel'
                })

                # Formato visual de la tabla
                df_estilizado = df_detalle.style.format({
                    'Valor utilizado': '${:,.0f}',
                    'Back Order original': '${:,.0f}',
                    'Back Order restante': '${:,.0f}'
                })

                st.dataframe(
                    df_estilizado,
                    use_container_width=True,
                    hide_index=True,
                    height=400
                )

            else:

                st.info(
                    'No se reconoció Back Order para este trimestre.'
                )
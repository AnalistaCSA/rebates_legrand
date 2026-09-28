import streamlit as st
import pandas as pd
from ejecutar_rebates import ejecutar_rebates

st.set_page_config(page_title='Rebates Legrand', page_icon='📊', layout='wide')
st.title('📊 Rebates Legrand')
st.caption('Control de cumplimiento de metas, Back Order y rebate esperado')

st.sidebar.header('🔎 Filtros')
categoria = st.sidebar.selectbox('Categoría', ['INDUSTRIAL', 'ELECTROBARRAS', 'DC & DC'])
trimestre = st.sidebar.selectbox('Trimestre', ['Todos', 'Q1', 'Q2', 'Q3', 'Q4'])
calcular = st.sidebar.button('Calcular Rebates', type='primary', use_container_width=True)

if calcular:
    resultados = ejecutar_rebates(categoria)
    st.subheader(f'Resultados — {categoria}')
    resultados_mostrar = resultados if trimestre == 'Todos' else {trimestre: resultados[trimestre]}

    for trimestre_actual, r in resultados_mostrar.items():
        st.divider()
        st.markdown(f'### 📅 {trimestre_actual}')

        c1, c2, c3, c4 = st.columns(4)
        c1.metric('Meta', f"${r['meta']:,.0f}")
        c2.metric('Facturación válida', f"${r['total_facturado']:,.0f}")
        c3.metric('Back Order reconocido', f"${r['back_order']:,.0f}")
        c4.metric('Total para cumplimiento', f"${r['total_cumplimiento']:,.0f}")

        c5, c6, c7 = st.columns(3)
        c5.metric('Cumplimiento', f"{r['porcentaje_cumplimiento']:.2f}%")
        c6.metric('Porcentaje de rebate', f"{r['tasa_rebate']:.2f}%")
        c7.metric('Rebate esperado', f"${r['rebate_esperado']:,.0f}")

        if r['rebate_ganado']:
            st.success(f"Meta cumplida. Se aplica una tasa de rebate del {r['tasa_rebate']:.2f}% sobre el Total de Cumplimiento.")
        else:
            st.warning('No se alcanzó el 100% de cumplimiento. No se genera rebate para este trimestre.')

        with st.expander('📋 Ver detalle de Back Order'):
            if r['detalle']:
                st.dataframe(pd.DataFrame(r['detalle']), use_container_width=True, hide_index=True)
            else:
                st.info('No se reconoció Back Order para este trimestre.')

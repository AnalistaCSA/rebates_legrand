from calculo_rebates import calcular_rebates
from metas_ln import *

TASAS = {
    'DC & DC': {100: 0.05, 110: 0.065, 120: 0.075},
    'INDUSTRIAL': {100: 0.04, 110: 0.052, 120: 0.06},
    'ELECTROBARRAS': {100: 0.04, 110: 0.052, 120: 0.06},
}


def determinar_tasa(cumplimiento, categoria):
    """Retorna porcentaje de rebate según el cumplimiento de la meta."""
    if cumplimiento < 100:
        return 0.0
    tasas = TASAS[categoria]
    if cumplimiento >= 120:
        return tasas[120]
    if cumplimiento >= 110:
        return tasas[110]
    return tasas[100]


def ejecutar_rebates(categoria):
    # Crédito de BO pendiente de descontar de facturas futuras por OC.
    compras_usadas = {}
    resultados = {}

    metas = {
        'INDUSTRIAL': {
            'Q1': meta_q1_industrial, 'Q2': meta_q2_industrial,
            'Q3': meta_q3_industrial, 'Q4': meta_q4_industrial,
        },
        'ELECTROBARRAS': {
            'Q1': meta_q1_electrobarras, 'Q2': meta_q2_electrobarras,
            'Q3': meta_q3_electrobarras, 'Q4': meta_q4_electrobarras,
        },
        'DC & DC': {
            'Q1': meta_q1_dc_y_dc, 'Q2': meta_q2_dc_y_dc,
            'Q3': meta_q3_dc_y_dc, 'Q4': meta_q4_dc_y_dc,
        },
    }

    for trimestre in ['Q1', 'Q2', 'Q3', 'Q4']:
        meta = metas[categoria][trimestre]
        total_facturado, total_back_order, total_cumplimiento, detalle = calcular_rebates(
            trimestre, categoria, meta, compras_usadas
        )

        cumplimiento = (total_cumplimiento / meta * 100) if meta else 0
        tasa = determinar_tasa(cumplimiento, categoria)
        rebate_esperado = total_cumplimiento * tasa

        resultados[trimestre] = {
            'meta': meta,
            'total_facturado': total_facturado,
            'back_order': total_back_order,
            'total_cumplimiento': total_cumplimiento,
            'porcentaje_cumplimiento': cumplimiento,
            'tasa_rebate': tasa * 100,
            'rebate_ganado': tasa > 0,
            'rebate_esperado': rebate_esperado,
            'detalle': detalle,
        }

    return resultados

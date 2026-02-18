# -*- coding: utf-8 -*-
"""
Key Functions on Bloomberg
"""
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

# -------------------------------
# BASE DE CONOCIMIENTO BLOOMBERG
# -------------------------------
FUNCTION_KB = {

    "XLTP": {
        "purpose": "Exportar datos de Bloomberg a Excel usando plantillas y enlaces dinámicos.",
        "universe": "Multi-asset en mercados organizados y OTC.",
        "output": "Excel con campos y universos enlazados dinámicamente.",
        "assumptions": "Campos y parámetros correctos; datos actualizados.",
        "not_applicable": [
            "No es herramienta de análisis",
            "No sirve para pricing ni riesgo",
            "No valida supuestos automáticamente"
        ],
        "chart": None
    },

    "NIA": {
        "purpose": "Construir y comparar curvas de crédito y greenium por emisor.",
        "universe": "Bonos corporativos OTC del mismo emisor.",
        "output": "Curvas de spread interpoladas por vencimiento.",
        "assumptions": "Comparabilidad crediticia, liquidez suficiente, correcta clasificación ESG.",
        "not_applicable": [
            "Emisores con un solo bono",
            "Bonos ilíquidos o sin precios",
            "Estructuras project finance o private debt"
        ],
        "chart": "credit_curve"
    },

    "BVAL": {
        "purpose": "Obtener precios de cierre confiables.",
        "universe": "Bonos y préstamos OTC.",
        "output": "Precio end-of-day estimado.",
        "assumptions": "Modelos + transacciones reales.",
        "not_applicable": [
            "Ejecución de trading",
            "Instrumentos altamente idiosincráticos",
            "Private deals sin referencias"
        ],
        "chart": "price_compare"
    },

    "BGN": {
        "purpose": "Mostrar precios promedio del mercado en tiempo real.",
        "universe": "Bonos OTC.",
        "output": "Precio consenso del mercado.",
        "assumptions": "Cotizaciones indicativas de dealers.",
        "not_applicable": [
            "Mercados estresados",
            "Bonos sin quotes activas"
        ],
        "chart": "price_compare"
    },

    "MIPD": {
        "purpose": "Evaluar probabilidad de default implícita.",
        "universe": "Renta fija en mercados organizados y OTC.",
        "output": "Curvas de PD por horizonte temporal.",
        "assumptions": "Recovery estándar y spreads representativos.",
        "not_applicable": [
            "Private debt sin precios",
            "Project finance",
            "Estructuras con garantías complejas"
        ],
        "chart": "pd_curve"
    },
    
    "BOB": {
    "purpose": "Resumir noticias, research y datos clave de un activo o mercado (Best of Bloomberg).",
    "universe": "Multi-activo: acciones, bonos, FX y commodities en mercados organizados y OTC.",
    "output": "Resumen curado de titulares, métricas y gráficos; se interpreta como una visión rápida de contexto y catalizadores.",
    "assumptions": "La selección algorítmica/editorial prioriza la información más relevante para el activo.",
    "not_applicable": [
        "Análisis profundo de valuación",
        "Decisiones de trading táctico",
        "Mercados con baja cobertura informativa"
    ],
    "chart": None
    },
    
    "BT": {
    "purpose": "Analizar, cotizar y negociar bonos mediante la plataforma Bond Trader.",
    "universe": "Bonos soberanos y corporativos, principalmente en mercado OTC.",
    "output": "Precios, yields, spreads y profundidad de mercado; se interpretan como niveles ejecutables o indicativos.",
    "assumptions": "Las cotizaciones reflejan condiciones reales de liquidez y crédito en el momento.",
    "not_applicable": [
        "Bonos ilíquidos o sin quotes",
        "Análisis puramente teórico",
        "Private debt"
    ],
    "chart": "price_compare"
    },
    
    "BI": {
    "purpose": "Proveer research fundamental, estimaciones y análisis sectorial (Bloomberg Intelligence).",
    "universe": "Multi-activo: equity, crédito y macro en mercados organizados y OTC.",
    "output": "Reportes, modelos, previsiones y KPIs; se interpretan como análisis propietario para apoyar decisiones de inversión.",
    "assumptions": "Los modelos y supuestos de analistas reflejan escenarios razonables de mercado y fundamentales.",
    "not_applicable": [
        "Trading intradía",
        "Ejecución directa",
        "Mercados sin cobertura de analistas"
    ],
    "chart": None
    },
    
    "ECFC": {
    "purpose": "Analizar y comparar estructuras de capital y métricas financieras históricas y proyectadas.",
    "universe": "Emisores corporativos (equity y crédito) en mercados organizados y deuda OTC.",
    "output": "Tablas y gráficos de deuda, EBITDA, leverage y cobertura; se interpretan para evaluar solvencia y riesgo crediticio.",
    "assumptions": "Los estados financieros reportados y ajustes estándar reflejan adecuadamente la realidad económica del emisor.",
    "not_applicable": [
        "Entidades financieras",
        "Startups sin históricos",
        "Estructuras project finance"
    ],
    "chart": None
    },
    
    "RELS": {
    "purpose": "Mostrar valores relativos y comparables entre compañías o instrumentos similares.",
    "universe": "Equity y crédito corporativo en mercados organizados y OTC.",
    "output": "Ratios comparativos (P/E, EV/EBITDA, spreads, etc.); se interpretan como señales de sobre o infravaloración relativa.",
    "assumptions": "El peer group seleccionado es homogéneo y comparable en riesgo y modelo de negocio.",
    "not_applicable": [
        "Empresas sin peers claros",
        "Sectores altamente heterogéneos",
        "Análisis absoluto de valuación"
    ],
    "chart": None
    },
    
    "HDS": {
    "purpose": "Proporcionar análisis detallado de la estructura y métricas de deuda histórica del emisor.",
    "universe": "Emisores corporativos con deuda en mercado OTC (bonos y préstamos).",
    "output": "Calendario de vencimientos y composición de deuda; se interpreta para analizar refinanciación y liquidez.",
    "assumptions": "La información de deuda reportada está completa y correctamente clasificada.",
    "not_applicable": [
        "Emisores sin deuda pública",
        "Private debt no reportado",
        "Análisis equity puro"
    ],
    "chart": None
    },
    
    "CACS": {
    "purpose": "Analizar cláusulas de acción colectiva (Collective Action Clauses) en bonos soberanos.",
    "universe": "Bonos soberanos emitidos en mercados internacionales (OTC).",
    "output": "Detalle de umbrales de votación y términos de reestructuración; se interpreta para evaluar riesgo legal en defaults.",
    "assumptions": "La documentación legal está correctamente cargada y estandarizada en Bloomberg.",
    "not_applicable": [
        "Bonos corporativos",
        "Bonos domésticos sin CACs",
        "Análisis de pricing directo"
    ],
    "chart": None
    },
    
    "PORT": {
    "purpose": "Analizar y atribuir el desempeño de portafolios frente a benchmarks.",
    "universe": "Portafolios multi-activo (acciones, bonos, ETFs) en mercados organizados y OTC.",
    "output": "Retornos, alpha, beta, tracking error y attribution; se interpreta para evaluar generación de valor y riesgo relativo.",
    "assumptions": "Las posiciones cargadas y el benchmark seleccionado reflejan correctamente la estrategia evaluada.",
    "not_applicable": [
        "Instrumentos individuales",
        "Portafolios incompletos o mal cargados",
        "Análisis intradía"
    ],
    "chart": None
    },
    
    "MODL": {
    "purpose": "Construir y analizar modelos financieros con métricas sectoriales integradas.",
    "universe": "Acciones corporativas en mercados organizados.",
    "output": "Proyecciones financieras y KPIs sectoriales; se interpretan para valoración y análisis prospectivo.",
    "assumptions": "Supuestos de crecimiento, márgenes y drivers sectoriales consistentes con el escenario base.",
    "not_applicable": [
        "Bonos y renta fija",
        "Trading táctico",
        "Empresas sin cobertura sectorial"
    ],
    "chart": None
    },
    
    "FA": {
    "purpose": "Extraer estados financieros ajustados por Bloomberg para análisis y modelaje.",
    "universe": "Compañías listadas (equity) con reporting financiero estandarizado.",
    "output": "Estados financieros históricos y ratios calculados; base limpia para valoración.",
    "assumptions": "Los ajustes estandarizados de Bloomberg reflejan adecuadamente la comparabilidad entre compañías.",
    "not_applicable": [
        "Empresas privadas",
        "Estados financieros no estandarizados",
        "Análisis de mercado en tiempo real"
    ],
    "chart": None
    },
    
    "RRG": {
    "purpose": "Analizar fortaleza relativa y momentum frente a un benchmark.",
    "universe": "Acciones e índices en mercados organizados.",
    "output": "Gráfico en cuadrantes (Leading, Improving, Weakening, Lagging); se interpreta para rotación táctica.",
    "assumptions": "Las métricas de fuerza relativa y momentum capturan correctamente la dinámica comparativa.",
    "not_applicable": [
        "Bonos y renta fija",
        "Horizontes de muy largo plazo",
        "Mercados ilíquidos"
    ],
    "chart": None
    },
    
    "GF": {
    "purpose": "Graficar series históricas de métricas fundamentales.",
    "universe": "Acciones de compañías listadas en mercados organizados.",
    "output": "Gráficos temporales de fundamentales históricos y estimados; se interpretan para detectar tendencias.",
    "assumptions": "Datos históricos y estimaciones futuras correctamente ajustados y alineados metodológicamente.",
    "not_applicable": [
        "Bonos y crédito",
        "Empresas sin históricos suficientes",
        "Análisis puramente transversal"
    ],
    "chart": None
    },
    
    "FIT": {
    "purpose": "Analizar y comparar curvas de tasas y su evolución temporal.",
    "universe": "Renta fija y derivados de tasas en mercados organizados y OTC.",
    "output": "Curvas, spreads y cambios por tramo; se interpretan para evaluar pendiente y expectativas.",
    "assumptions": "Precios y cotizaciones reflejan condiciones reales de mercado.",
    "not_applicable": [
        "Bonos corporativos específicos",
        "Private debt",
        "Análisis de crédito idiosincrático"
    ],
    "chart": "credit_curve"
    },
    
    "SOVR": {
    "purpose": "Analizar riesgo soberano y métricas fiscales de países.",
    "universe": "Bonos soberanos (OTC) y análisis macro-país.",
    "output": "Deuda/PIB, déficit, spreads y ratings; se interpretan para evaluar riesgo país.",
    "assumptions": "Las cifras fiscales y macroeconómicas son comparables y están actualizadas.",
    "not_applicable": [
        "Empresas corporativas",
        "Análisis microeconómico",
        "Trading intradía"
    ],
    "chart": None
    },
    
    "BTMM": {
    "purpose": "Monitorear tasas de mercado monetario y curvas de corto plazo.",
    "universe": "Money market y tasas en mercados organizados y OTC.",
    "output": "Niveles actuales de tasas, forwards y spreads; referencia para fondeo y liquidez.",
    "assumptions": "Cotizaciones interbancarias reflejan condiciones vigentes de liquidez.",
    "not_applicable": [
        "Bonos de largo plazo",
        "Análisis de equity",
        "Estrategias estructurales"
    ],
    "chart": None
    },
    
    "RATC": {
    "purpose": "Analizar cambios históricos y actuales en calificaciones crediticias.",
    "universe": "Emisores corporativos y soberanos en mercados organizados y OTC.",
    "output": "Historial de upgrades, downgrades y outlooks; señal de evolución del riesgo crediticio.",
    "assumptions": "Las acciones de rating reflejan adecuadamente la percepción de riesgo de las agencias.",
    "not_applicable": [
        "Instrumentos sin rating",
        "Private debt",
        "Trading táctico de corto plazo"
    ],
    "chart": None
    },
    
    "CRPR": {
    "purpose": "Analizar desempeño agregado y métricas del mercado de crédito corporativo.",
    "universe": "Bonos corporativos investment grade y high yield en mercado OTC.",
    "output": "Spreads promedio, retornos y estadísticas de mercado; barómetro del riesgo crediticio.",
    "assumptions": "Índices y universos representan adecuadamente el mercado subyacente.",
    "not_applicable": [
        "Análisis de bonos individuales",
        "Valoración de emisores específicos",
        "Private debt sin índices públicos"
    ],
    "chart": "credit_market"
    },
    
    "RRG": {
    "purpose": "Analizar momentum y fortaleza relativa entre activos o sectores.",
    "universe": "Acciones e índices en mercados organizados.",
    "output": "Gráfico en cuadrantes; señal de liderazgo y rotación relativa.",
    "assumptions": "Las métricas de momentum capturan correctamente la dinámica comparativa.",
    "not_applicable": [
        "Análisis fundamental de largo plazo",
        "Instrumentos ilíquidos",
        "Mercados privados"
    ],
    "chart": "rrg_quadrant"
    },
    
    "CHRT": {
    "purpose": "Realizar análisis técnico y visualización avanzada de precios.",
    "universe": "Multi-activo en mercados organizados y OTC.",
    "output": "Gráficos con indicadores técnicos; identificación de tendencias y niveles clave.",
    "assumptions": "Series de precios correctamente ajustadas por eventos corporativos.",
    "not_applicable": [
        "Valoración fundamental",
        "Análisis crediticio",
        "Instrumentos sin historial de precios"
    ],
    "chart": "technical_price"
    },
    
    "TOP": {
    "purpose": "Centralizar noticias macro, geopolíticas y corporativas relevantes.",
    "universe": "Multi-activo en mercados organizados y OTC.",
    "output": "Feed curado de titulares; radar de riesgos y catalizadores inmediatos.",
    "assumptions": "La priorización editorial resalta la información más relevante.",
    "not_applicable": [
        "Análisis cuantitativo",
        "Modelización financiera",
        "Valoración de instrumentos"
    ],
    "chart": None
    },
    
    "W": {
    "purpose": "Crear paneles personalizados de monitoreo y seguimiento.",
    "universe": "Principalmente acciones en mercados organizados; multi-activo soportado.",
    "output": "Tablas dinámicas con precios, ratios y noticias; dashboard operativo.",
    "assumptions": "Campos y universos seleccionados representan el set de análisis.",
    "not_applicable": [
        "Análisis profundo de un solo emisor",
        "Modelos financieros detallados",
        "Pricing de instrumentos complejos"
    ],
    "chart": None
    },
    
    "EQS": {
    "purpose": "Filtrar acciones según criterios fundamentales y de mercado.",
    "universe": "Acciones listadas en mercados organizados globales.",
    "output": "Listado de compañías que cumplen filtros; universo candidato.",
    "assumptions": "Datos financieros y estimaciones están actualizados.",
    "not_applicable": [
        "Valoración final de inversión",
        "Análisis crediticio",
        "Instrumentos privados"
    ],
    "chart": None
    } 
        

}

# -------------------------------
# CONFIGURACIÓN GENERAL
# -------------------------------
st.set_page_config(
    page_title="Bloomberg Terminal Simulator",
    layout="wide"
)

# -------------------------------
# ESTILOS BLOOMBERG
# -------------------------------
st.markdown("""
<style>
body { background-color: #000000; color: white; }
.stApp { background-color: #000000; }
h1, h2, h3, h4 { color: #ffffff; }
.command { color: #FFD700; font-weight: bold; }
.positive { color: #00FF7F; }
.negative { color: #FF4C4C; }
.reference { color: #4DA6FF; }
.inactive { color: #A9A9A9; }
.top-bar { background-color: #8B0000; padding: 10px; font-weight: bold; }
.panel { border: 1px solid #333333; padding: 10px; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------
st.markdown(
    '<div class="top-bar">FUNCTION: SIMULATOR | CONTEXT: EDUCATIONAL MODE</div>',
    unsafe_allow_html=True
)

# -------------------------------
# INPUT DE COMANDO
# -------------------------------
st.markdown("### 💻 Bloomberg Command Line")

command = st.text_input(
    label="Enter command (example: IBM US NIA <GO>)",
    value=""
)

execute = st.button("EXECUTE <GO>")

# -------------------------------
# PARSER
# -------------------------------
def parse_command(cmd):
    parts = cmd.replace("<GO>", "").strip().split()
    if len(parts) == 1:
        return None, parts[0]
    return " ".join(parts[:-1]), parts[-1]

# -------------------------------
# EJECUCIÓN PRINCIPAL
# -------------------------------
if execute and command:

    context, function = parse_command(command.upper())

    st.markdown("### 📊 Terminal Output")
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    # FUNCIÓN GLOBAL
    if context is None:
        st.markdown(f"**Function Executed:** <span class='command'>{function}</span>", unsafe_allow_html=True)
        st.markdown("**Context:** GLOBAL", unsafe_allow_html=True)

    # FUNCIÓN CON CONTEXTO
    else:
        st.markdown(f"**Context:** <span class='reference'>{context}</span>", unsafe_allow_html=True)
        st.markdown(f"**Function:** <span class='command'>{function}</span>", unsafe_allow_html=True)

        if function in FUNCTION_KB:

            kb = FUNCTION_KB[function]

            st.markdown("#### 🟨 Function Logic Breakdown")

            st.markdown(f"""
            <span class='command'>¿Para qué sirve?</span><br>
            <span class='reference'>{kb['purpose']}</span><br><br>

            <span class='command'>¿Para qué instrumento / emisor / mercado está diseñada?</span><br>
            <span class='reference'>{kb['universe']}</span><br><br>

            <span class='command'>¿Qué output entrega y cómo interpretarlo?</span><br>
            <span class='reference'>{kb['output']}</span><br><br>

            <span class='command'>¿Qué supuestos asume?</span><br>
            <span class='negative'>{kb['assumptions']}</span>
            """, unsafe_allow_html=True)

            st.markdown("#### 🚨 When NOT to use this function")
            for item in kb["not_applicable"]:
                st.markdown(f"<span class='negative'>⚠ {item}</span>", unsafe_allow_html=True)

            # GRÁFICOS
            if kb["chart"] == "credit_curve":
                x = np.array([1, 3, 5, 7, 10])
                y = np.array([120, 140, 160, 180, 200])
                fig, ax = plt.subplots()
                ax.plot(x, y, linestyle="--")
                st.pyplot(fig)

            elif kb["chart"] == "price_compare":
                d = np.arange(1, 11)
                fig, ax = plt.subplots()
                ax.plot(d, 100 + np.random.normal(0, 0.2, 10))
                st.pyplot(fig)

            elif kb["chart"] == "pd_curve":
                h = np.array([1, 2, 3, 5, 7, 10])
                pdv = np.array([0.5, 1.2, 2.5, 4.0, 6.5, 9.0])
                fig, ax = plt.subplots()
                ax.plot(h, pdv)
                st.pyplot(fig)
            elif kb["chart"] == "credit_market":
                t = np.arange(2018, 2026)
                spreads = np.array([90, 110, 180, 140, 160, 155, 150, 145])
                fig, ax = plt.subplots()
                ax.plot(t, spreads)
                ax.set_title("Corporate Credit Spread Index (bps)")
                st.pyplot(fig)
            
            elif kb["chart"] == "rrg_quadrant":
                fig, ax = plt.subplots()
                ax.axhline(0)
                ax.axvline(0)
                ax.scatter([1, -1, -0.5, 0.8], [1, 0.5, -1, -0.8])
                ax.set_title("Relative Rotation Graph (Pedagogical)")
                st.pyplot(fig)
            
            elif kb["chart"] == "technical_price":
                p = np.cumsum(np.random.normal(0, 1, 100)) + 100
                fig, ax = plt.subplots()
                ax.plot(p)
                ax.set_title("Price Chart with Trend (Mock)")
                st.pyplot(fig)


        else:
            st.markdown("<span class='inactive'>Function recognized but not documented.</span>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.markdown("## 🧭 Bloomberg Workflow")
st.sidebar.markdown("""
1. Define **context**  
2. Select **function**  
3. Execute `<GO>`  
4. Review **assumptions**  
5. Validate with another function  
""")

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("""
---
### 🧠 Key Learning
> Bloomberg is not a menu — it is a **contextual language**.
""")



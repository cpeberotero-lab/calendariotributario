import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ==========================================
# 1. CONFIGURACIÓN Y UTILIDADES
# ==========================================
st.set_page_config(page_title="Hub Tributario 2026", layout="wide", page_icon="🏢")

# Festivos Colombia 2026 (Simplificado para cálculo de días hábiles)
HOLIDAYS_2026 = [
    "2026-01-01", "2026-01-12", "2026-03-23", "2026-04-02", "2026-04-03", 
    "2026-05-01", "2026-05-18", "2026-06-08", "2026-06-15", "2026-06-29", 
    "2026-07-20", "2026-08-07", "2026-08-17", "2026-10-12", "2026-11-02", 
    "2026-11-16", "2026-12-08", "2026-12-25"
]

def get_business_days(start_date_str, num_days=10):
    """Genera días hábiles saltando fines de semana y festivos."""
    start_date = pd.to_datetime(start_date_str)
    dates = []
    current_date = start_date
    while len(dates) < num_days:
        if current_date.weekday() >= 5 or current_date.strftime("%Y-%m-%d") in HOLIDAYS_2026:
            current_date += timedelta(days=1)
            continue
        dates.append(current_date)
        current_date += timedelta(days=1)
    return dates

# ==========================================
# 2. LÓGICA NACIONAL (DIAN)
# ==========================================
def get_national_calendar(last_digit, last_two_digits):
    calendar = []
    
    # Reglas Generales (1 dígito) - Fechas de inicio base extraídas del PDF
    rules = [
        {"impuesto": "Retención en la Fuente (DIAN)", "periodo": "Enero", "start": "2026-02-10"},
        {"impuesto": "Retención en la Fuente (DIAN)", "periodo": "Febrero", "start": "2026-03-10"},
        {"impuesto": "IVA Bimestral (DIAN)", "periodo": "Bimestre 1", "start": "2026-03-10"},
        {"impuesto": "Renta Personas Jurídicas (DIAN)", "periodo": "1ra Cuota", "start": "2026-05-11"},
    ]
    
    # Mapeo DIAN: Si NIT termina en 1, es el día 0 de la secuencia.
    digit_map = {1:0, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 0:9}
    idx = digit_map[int(last_digit)]
    
    for rule in rules:
        dates = get_business_days(rule['start'], num_days=10)
        # Verificamos que el índice no exceda la lista de fechas generadas
        if idx < len(dates):
            calendar.append({
                "Jurisdicción": "🇨🇴 Nacional",
                "Impuesto": rule['impuesto'],
                "Periodo": rule['periodo'],
                "Fecha": dates[idx],
                "Detalle": "Regla General"
            })
        
    return calendar

# ==========================================
# 3. LÓGICA DEPARTAMENTAL (ATLÁNTICO)
# ==========================================
def get_atlantico_calendar():
    # Basado en la Resolución 000476 de 2025
    calendar = []
    
    # [cite_start]Impuesto de Registro [cite: 491, 492]
    fechas_registro = [
        ("Enero", "2026-02-16"), ("Febrero", "2026-03-16"), ("Marzo", "2026-04-15"),
        ("Abril", "2026-05-15"), ("Mayo", "2026-06-16"), ("Junio", "2026-07-15")
    ]
    for per, fecha in fechas_registro:
        calendar.append({
            "Jurisdicción": "🌊 Atlántico",
            "Impuesto": "Impuesto de Registro",
            "Periodo": per,
            "Fecha": pd.to_datetime(fecha),
            "Detalle": "Fecha Fija"
        })

    # [cite_start]Tasa de Seguridad y Convivencia [cite: 509, 511]
    fechas_seguridad = [
        ("Enero", "2026-02-18"), ("Febrero", "2026-03-18"), ("Marzo", "2026-04-20")
    ]
    for per, fecha in fechas_seguridad:
        calendar.append({
            "Jurisdicción": "🌊 Atlántico",
            "Impuesto": "Tasa Seguridad y Convivencia",
            "Periodo": per,
            "Fecha": pd.to_datetime(fecha),
            "Detalle": "Fecha Fija"
        })

    # [cite_start]Estampillas Departamentales (Anual) [cite: 522]
    calendar.append({
        "Jurisdicción": "🌊 Atlántico",
        "Impuesto": "Estampillas Departamentales",
        "Periodo": "Anual 2026",
        "Fecha": pd.to_datetime("2027-01-31"),
        "Detalle": "Declaración Consolidada"
    })
    
    return calendar

# ==========================================
# 4. LÓGICA DISTRITAL (BARRANQUILLA)
# ==========================================
def get_barranquilla_calendar(last_digit):
    # Basado en Resolución DSH 003 de 2025
    calendar = []
    digit = int(last_digit)
    
    # [cite_start]--- A. ICA ANUAL [cite: 582] ---
    # Tabla: 0->15 Feb, 9->16 Feb...
    ica_map = {
        0: "2027-02-15", 9: "2027-02-16", 8: "2027-02-17", 7: "2027-02-18",
        6: "2027-02-19", 5: "2027-02-22", 4: "2027-02-23", 3: "2027-02-24",
        2: "2027-02-25", 1: "2027-02-26"
    }
    calendar.append({
        "Jurisdicción": "🏙️ Barranquilla",
        "Impuesto": "ICA (Industria y Comercio)",
        "Periodo": "Anual 2026",
        "Fecha": pd.to_datetime(ica_map.get(digit, "2027-02-28")), # Fallback seguro
        "Detalle": "Régimen Común"
    })
    
    # [cite_start]--- B. PREDIAL UNIFICADO [cite: 614, 615, 616] ---
    predial_fechas = [
        ("Con Descuento 10%", "2026-03-27"),
        ("Con Descuento 5%", "2026-05-29"),
        ("Sin Descuento (Límite)", "2026-06-30")
    ]
    for desc, fecha in predial_fechas:
        calendar.append({
            "Jurisdicción": "🏙️ Barranquilla",
            "Impuesto": "Impuesto Predial",
            "Periodo": "Vigencia 2026",
            "Fecha": pd.to_datetime(fecha),
            "Detalle": desc
        })

    # [cite_start]--- C. RETE-ICA BIMESTRAL (Ejemplo Demo) [cite: 595] ---
    # Lógica simplificada basada en tabla source 595 para primer bimestre
    if digit in [0, 9]:
        f_mar = "2026-03-13" if digit == 0 else "2026-03-16"
    elif digit == 8: f_mar = "2026-03-17"
    elif digit == 7: f_mar = "2026-03-18"
    elif digit in [6, 5, 4]: f_mar = "2026-03-20" 
    elif digit in [3, 2]: f_mar = "2026-03-25"
    else: f_mar = "2026-03-27" # Digito 1

    calendar.append({
        "Jurisdicción": "🏙️ Barranquilla",
        "Impuesto": "Rete-ICA Bimestral",
        "Periodo": "Ene-Feb",
        "Fecha": pd.to_datetime(f_mar),
        "Detalle": "Agentes Retenedores"
    })
    
    return calendar

# ==========================================
# 5. INTERFAZ PRINCIPAL
# ==========================================

st.title("🗓️ Hub Tributario: Nacional, Atlántico y Barranquilla")
st.markdown("""
Consulta unificada de obligaciones tributarias para 2026. 
Normativa: **DIAN**, **Gobernación del Atlántico** [Res. 000476/25] y **Alcaldía de Barranquilla** [Res. DSH 003/25].
""")

# --- FILTROS ---
col1, col2 = st.columns([1, 2])
with col1:
    nit_input = st.text_input("NIT (Sin dígito de verificación)", placeholder="Ej: 800123456")

with col2:
    jurisdicciones = st.multiselect(
        "Seleccione Jurisdicciones:",
        ["Nacional (DIAN)", "Atlántico (Gobernación)", "Barranquilla (Distrito)"],
        default=["Nacional (DIAN)", "Atlántico (Gobernación)", "Barranquilla (Distrito)"]
    )

if nit_input and nit_input.isdigit():
    last_digit = int(nit_input[-1])
    last_two = nit_input[-2:]
    
    full_calendar = []
    
    # --- CONSTRUCCIÓN DE DATOS ---
    if "Nacional (DIAN)" in jurisdicciones:
        full_calendar.extend(get_national_calendar(last_digit, last_two))
        
    if "Atlántico (Gobernación)" in jurisdicciones:
        full_calendar.extend(get_atlantico_calendar())
        
    if "Barranquilla (Distrito)" in jurisdicciones:
        full_calendar.extend(get_barranquilla_calendar(last_digit))
    
    # --- VISUALIZACIÓN ---
    if full_calendar:
        df = pd.DataFrame(full_calendar)
        df = df.sort_values(by="Fecha")
        
        st.divider()
        st.subheader(f"Resultados para NIT terminado en {last_digit}")
        
        # Iterar filas para crear tarjetas
        for i, row in df.iterrows():
            fecha_dt = row['Fecha']
            dias_restantes = (fecha_dt - datetime.now()).days + 1
            
            # Colores por jurisdicción
            color_border = "#ccc"
            if "Nacional" in row['Jurisdicción']: color_border = "#003366" # Azul oscuro DIAN
            elif "Atlántico" in row['Jurisdicción']: color_border = "#FF9900" # Naranja Gob
            elif "Barranquilla" in row['Jurisdicción']: color_border = "#009933" # Verde Bquilla
            
            # Semáforo de tiempo
            estado_icon = "🟢"
            if dias_restantes < 0: estado_icon = "🔴 Vencido"
            elif dias_restantes < 15: estado_icon = "🟠 Próximo"
            
            st.markdown(f"""
            <div style="
                background-color: white; 
                padding: 15px; 
                border-radius: 8px; 
                border-left: 6px solid {color_border};
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin-bottom: 10px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:bold; color:{color_border};">{row['Jurisdicción']}</span>
                    <span style="background-color:#eee; padding:2px 8px; border-radius:4px; font-size:0.9em;">
                        {estado_icon} ({dias_restantes} días)
                    </span>
                </div>
                <h3 style="margin:5px 0 0 0; font-size:18px;">{row['Impuesto']}</h3>
                <p style="margin:0; color:#555;">{row['Periodo']} - <i>{row['Detalle']}</i></p>
                <hr style="margin:8px 0;">
                <div style="font-size:16px; font-weight:bold;">
                    📅 Vence: {fecha_dt.strftime('%d de %B, %Y')}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    else:
        st.info("Selecciona al menos una jurisdicción para ver los resultados.")

elif nit_input:
    st.error("El NIT debe ser numérico.")

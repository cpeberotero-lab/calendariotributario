import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ==========================================
# 1. CONFIGURACIÓN Y MOTOR DE FECHAS
# ==========================================

st.set_page_config(page_title="Agenda Tributaria 2026", layout="wide", page_icon="🗓️")

# Definimos los días festivos clave de Colombia 2026 para que el cálculo sea preciso
# (Lista simplificada para el cálculo de días hábiles bancarios)
HOLIDAYS_2026 = [
    "2026-01-01", "2026-01-12", "2026-03-23", "2026-04-02", "2026-04-03", 
    "2026-05-01", "2026-05-18", "2026-06-08", "2026-06-15", "2026-06-29", 
    "2026-07-20", "2026-08-07", "2026-08-17", "2026-10-12", "2026-11-02", 
    "2026-11-16", "2026-12-08", "2026-12-25"
]

def get_business_days(start_date_str, num_days=10):
    """
    Genera una lista de 'num_days' días hábiles a partir de una fecha de inicio.
    Salta fines de semana y festivos definidos.
    """
    start_date = pd.to_datetime(start_date_str)
    dates = []
    current_date = start_date
    
    while len(dates) < num_days:
        # Si es sábado (5) o domingo (6) o festivo, avanzar
        if current_date.weekday() >= 5 or current_date.strftime("%Y-%m-%d") in HOLIDAYS_2026:
            current_date += timedelta(days=1)
            continue
        dates.append(current_date)
        current_date += timedelta(days=1)
        
    return dates

# ==========================================
# 2. GENERADOR DE CALENDARIO COMPLETO (BASE DE DATOS)
# ==========================================
# Aquí definimos SOLO la fecha de inicio del Dígito 1 para cada obligación.
# El sistema calculará el resto (Dígitos 2,3...0) automáticamente.

CALENDAR_RULES = [
    # --- RETENCIÓN EN LA FUENTE (Mensual) ---
    {"impuesto": "Retención en la Fuente", "periodo": "Enero", "start": "2026-02-10"},
    {"impuesto": "Retención en la Fuente", "periodo": "Febrero", "start": "2026-03-10"},
    {"impuesto": "Retención en la Fuente", "periodo": "Marzo", "start": "2026-04-07"}, # Ajustado por Semana Santa
    {"impuesto": "Retención en la Fuente", "periodo": "Abril", "start": "2026-05-11"},
    {"impuesto": "Retención en la Fuente", "periodo": "Mayo", "start": "2026-06-09"}, # Festivo el 8
    {"impuesto": "Retención en la Fuente", "periodo": "Junio", "start": "2026-07-07"},
    {"impuesto": "Retención en la Fuente", "periodo": "Julio", "start": "2026-08-11"}, # Festivo el 7
    {"impuesto": "Retención en la Fuente", "periodo": "Agosto", "start": "2026-09-08"},
    {"impuesto": "Retención en la Fuente", "periodo": "Septiembre", "start": "2026-10-06"},
    {"impuesto": "Retención en la Fuente", "periodo": "Octubre", "start": "2026-11-10"},
    {"impuesto": "Retención en la Fuente", "periodo": "Noviembre", "start": "2026-12-10"},
    {"impuesto": "Retención en la Fuente", "periodo": "Diciembre", "start": "2027-01-13"},

    # --- IVA BIMESTRAL ---
    {"impuesto": "IVA Bimestral", "periodo": "Bimestre 1 (Ene-Feb)", "start": "2026-03-10"},
    {"impuesto": "IVA Bimestral", "periodo": "Bimestre 2 (Mar-Abr)", "start": "2026-05-11"},
    {"impuesto": "IVA Bimestral", "periodo": "Bimestre 3 (May-Jun)", "start": "2026-07-07"},
    {"impuesto": "IVA Bimestral", "periodo": "Bimestre 4 (Jul-Ago)", "start": "2026-09-08"},
    {"impuesto": "IVA Bimestral", "periodo": "Bimestre 5 (Sep-Oct)", "start": "2026-11-10"},
    {"impuesto": "IVA Bimestral", "periodo": "Bimestre 6 (Nov-Dic)", "start": "2027-01-13"},

    # --- RENTA PERSONAS JURÍDICAS ---
    {"impuesto": "Renta Personas Jurídicas", "periodo": "1ra Cuota / Declaración", "start": "2026-05-11"},
    {"impuesto": "Renta Personas Jurídicas", "periodo": "2da Cuota", "start": "2026-07-07"},
    
    # --- RENTA GRANDES CONTRIBUYENTES ---
    {"impuesto": "Renta Grandes Contribuyentes", "periodo": "1ra Cuota", "start": "2026-02-10"},
    {"impuesto": "Renta Grandes Contribuyentes", "periodo": "2da Cuota / Declaración", "start": "2026-04-07"},
    {"impuesto": "Renta Grandes Contribuyentes", "periodo": "3ra Cuota", "start": "2026-06-09"},
]

def generate_full_calendar(nit_last_digit):
    """
    Crea la lista personalizada de fechas para un NIT específico.
    """
    my_calendar = []
    
    # 1. Procesar impuestos de 1 dígito (Regla general: 1 al 0)
    # El orden de vencimiento estándar DIAN es: 1, 2, 3, 4, 5, 6, 7, 8, 9, 0
    # Si mi NIT termina en 1, me toca el día 0. Si termina en 0, me toca el día 9.
    
    digit_map = {1:0, 2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:7, 9:8, 0:9}
    day_index = digit_map[nit_last_digit]
    
    for rule in CALENDAR_RULES:
        dates = get_business_days(rule['start'], num_days=10)
        due_date = dates[day_index]
        
        my_calendar.append({
            "Impuesto": rule['impuesto'],
            "Periodo": rule['periodo'],
            "Fecha": due_date,
            "Categoria": "General / PJ / GC"
        })
        
    return pd.DataFrame(my_calendar)

def generate_natural_person_calendar(nit_last_two):
    """
    Genera fechas para Renta Personas Naturales (Regla de 2 dígitos)
    Inicio aprox: 11 Agosto 2026. Avanza 1 día por cada par de dígitos.
    """
    start_date_pn = "2026-08-11"
    # Generamos suficientes días hábiles para cubrir del 01 al 00 (50 días hábiles)
    dates_pn = get_business_days(start_date_pn, num_days=60)
    
    # NIT 01-02 -> Día 0
    # NIT 99-00 -> Día 49
    # Convertir NIT '00' a 100 para la matemática
    val = int(nit_last_two)
    if val == 0: val = 100
    
    # Índice: (Valor - 1) dividido en 2 (división entera)
    # Ej: 01 -> (1-1)//2 = 0. 02 -> (2-1)//2 = 0.
    day_index = (val - 1) // 2
    
    if day_index < len(dates_pn):
        due_date = dates_pn[day_index]
        return [{
            "Impuesto": "Renta Personas Naturales", 
            "Periodo": "Declaración Anual", 
            "Fecha": due_date,
            "Categoria": "Solo Personas Naturales"
        }]
    return []

# ==========================================
# 3. INTERFAZ DE USUARIO (UI)
# ==========================================

st.title("🗓️ Planificador Fiscal Anual 2026")
st.markdown("""
Esta herramienta proyecta **todas las obligaciones del año** para tu NIT, 
calculando los días hábiles automáticamente según el calendario DIAN.
""")

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    nit_input = st.text_input("Ingresa tu NIT completo (Sin dígito de verificación)", placeholder="Ej: 900123456")

if nit_input and nit_input.isdigit():
    # --- LÓGICA DE CÁLCULO ---
    last_digit = int(nit_input[-1])
    last_two = nit_input[-2:]
    
    # 1. Generar calendario general (IVA, Rete, Renta PJ)
    df_general = generate_full_calendar(last_digit)
    
    # 2. Generar fecha de Persona Natural (Si aplica)
    pn_data = generate_natural_person_calendar(last_two)
    df_pn = pd.DataFrame(pn_data)
    
    # 3. Unir todo
    df_final = pd.concat([df_general, df_pn], ignore_index=True)
    df_final = df_final.sort_values(by="Fecha")
    
    # --- VISUALIZACIÓN ---
    st.divider()
    st.subheader(f"📅 Calendario Completo para NIT terminado en {last_digit}")
    
    # Crear pestañas para mejor organización
    tab1, tab2 = st.tabs(["📋 Lista Cronológica", "📊 Vista por Impuesto"])
    
    with tab1:
        # Iterar para mostrar como lista bonita
        for i, row in df_final.iterrows():
            fecha_str = row['Fecha'].strftime("%Y-%m-%d")
            mes_str = row['Fecha'].strftime("%B")
            dia_str = row['Fecha'].strftime("%d")
            
            # Estilo condicional para fechas pasadas
            color = "#0056b3" # Azul default
            if row['Fecha'] < pd.Timestamp.now():
                color = "#6c757d" # Gris (pasado)
            
            with st.container():
                c1, c2 = st.columns([1, 4])
                with c1:
                    st.markdown(f"""
                    <div style="text-align:center; background-color:{color}; color:white; border-radius:5px; padding:5px;">
                        <span style="font-size:12px">{row['Fecha'].strftime('%b').upper()}</span><br>
                        <span style="font-size:24px; font-weight:bold">{dia_str}</span>
                    </div>
                    """, unsafe_allow_html=True)
                with c2:
                    st.markdown(f"**{row['Impuesto']}**")
                    st.caption(f"{row['Periodo']} - ({row['Categoria']})")
                st.write("") # Espacio
                
    with tab2:
        # Tabla dinámica filtrable
        st.dataframe(
            df_final[['Fecha', 'Impuesto', 'Periodo', 'Categoria']].style.format({"Fecha": lambda t: t.strftime("%Y-%m-%d")}),
            use_container_width=True,
            hide_index=True
        )

elif nit_input:
    st.error("El NIT debe contener solo números.")

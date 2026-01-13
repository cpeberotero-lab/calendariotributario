import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 1. BASE DE DATOS DE VENCIMIENTOS (Extracto del PDF)
# ==========================================
# Aquí he digitalizado los patrones encontrados en el PDF adjunto.
# La lógica es: NIT termina en X -> Vence el día Y.

DB_CALENDARIO = []

def agregar_vencimiento(impuesto, periodo, fecha_base_inicio, dias_habiles_consecutivos):
    """
    Función auxiliar para generar fechas masivamente siguiendo el patrón de la DIAN:
    Los vencimientos suelen arrancar en una fecha y seguir días hábiles sucesivos
    para los dígitos 1, 2, 3, 4, 5, 6, 7, 8, 9, 0.
    """
    # Esta lista simula los días exactos extraídos del PDF para el patrón estándar
    # Ejemplo basado en Retefuente Enero (Vence Febrero) : 
    # Dígitos 1-0 corresponden a días 10, 11, 12, 13, 16, 17, 18, 19, 20, 24.
    
    digitos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    
    # Mapeo manual de las fechas extraídas del PDF para los ejemplos:
    
    if periodo == "Enero (Decl. Feb)": # Fuente: PDF Pág 1 
        fechas = ["2026-02-10", "2026-02-11", "2026-02-12", "2026-02-13", "2026-02-16", 
                  "2026-02-17", "2026-02-18", "2026-02-19", "2026-02-20", "2026-02-24"]
                  
    elif periodo == "Febrero (Decl. Mar)": # Fuente: PDF Pág 1 
        fechas = ["2026-03-10", "2026-03-11", "2026-03-12", "2026-03-13", "2026-03-16", 
                  "2026-03-17", "2026-03-18", "2026-03-19", "2026-03-20", "2026-03-24"]
                  
    elif periodo == "Bimestre 1 (Decl. Mar)": # IVA - Fuente: PDF Pág 1 
        fechas = ["2026-03-10", "2026-03-11", "2026-03-12", "2026-03-13", "2026-03-16", 
                  "2026-03-17", "2026-03-18", "2026-03-19", "2026-03-20", "2026-03-24"]

    elif periodo == "Cuota 1 (Mayo)": # Renta PJ - Fuente: PDF Pág 1 
        # Dígitos 1 al 0
        fechas = ["2026-05-11", "2026-05-12", "2026-05-13", "2026-05-14", "2026-05-15", 
                  "2026-05-18", "2026-05-19", "2026-05-20", "2026-05-21", "2026-05-22"]
    else:
        fechas = []

    for d, f in zip(digitos, fechas):
        DB_CALENDARIO.append({
            "Impuesto": impuesto,
            "Periodo": periodo,
            "Ultimo_Digito": d,
            "Fecha_Limite": f
        })

# --- CARGA DE DATOS ---
# Retención en la fuente 
agregar_vencimiento("Retención en la Fuente", "Enero (Decl. Feb)", "", [])
agregar_vencimiento("Retención en la Fuente", "Febrero (Decl. Mar)", "", [])

# IVA Bimestral 
agregar_vencimiento("IVA Bimestral", "Bimestre 1 (Decl. Mar)", "", [])

# Renta Personas Jurídicas 
agregar_vencimiento("Renta Personas Jurídicas", "Cuota 1 (Mayo)", "", [])

# ==========================================
# 2. INTERFAZ Y LÓGICA (STREAMLIT)
# ==========================================

st.set_page_config(page_title="Calendario Tributario 2026", layout="centered", page_icon="📅")

# Estilos CSS para simular la estética DIAN/Corporativa
st.markdown("""
    <style>
    .stApp { background-color: #f5f7f9; }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        border-left: 5px solid #0056b3;
    }
    .big-font { font-size: 18px !important; font-weight: bold; color: #333; }
    .date-font { font-size: 16px; color: #0056b3; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🇨🇴 Calendario Tributario Inteligente 2026")
st.markdown("Digita tu NIT para conocer tus próximas obligaciones basadas en el **Calendario DIAN 2026**.")

# --- INPUT DEL USUARIO ---
col1, col2 = st.columns([2, 1])
with col1:
    nit = st.text_input("Ingrese su NIT (Sin dígito de verificación):", max_chars=12, placeholder="Ej: 900123456")
with col2:
    tipo_usuario = st.selectbox("Tipo de Contribuyente", ["Persona Jurídica", "Persona Natural"])

# --- PROCESAMIENTO ---
if nit and nit.isdigit():
    digito = int(nit[-1])
    
    st.divider()
    st.subheader(f"Obligaciones para NIT terminado en: {digito}")
    
    # Filtrar Base de Datos
    df = pd.DataFrame(DB_CALENDARIO)
    mis_obligaciones = df[df['Ultimo_Digito'] == digito].copy()
    
    # Convertir a datetime para ordenar cronológicamente
    mis_obligaciones['Fecha_DT'] = pd.to_datetime(mis_obligaciones['Fecha_Limite'])
    mis_obligaciones = mis_obligaciones.sort_values(by='Fecha_DT')
    
    # Filtrar fechas pasadas (opcional, aquí mostramos todas las del 2026 cargadas)
    # mis_obligaciones = mis_obligaciones[mis_obligaciones['Fecha_DT'] >= datetime.now()]

    if not mis_obligaciones.empty:
        for index, row in mis_obligaciones.iterrows():
            
            # Calcular días restantes
            hoy = datetime.now()
            delta = row['Fecha_DT'] - hoy
            dias_restantes = delta.days + 1
            
            # Definir color del estado
            estado = "🟢 A tiempo"
            if dias_restantes < 0:
                estado = "🔴 Vencido"
            elif dias_restantes <= 5:
                estado = "🟠 Urgente"
            
            # Renderizar tarjeta
            st.markdown(f"""
            <div class="card">
                <div class="big-font">{row['Impuesto']}</div>
                <div>Periodo: {row['Periodo']}</div>
                <hr style="margin: 5px 0;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div class="date-font">📅 Vence: {row['Fecha_Limite']}</div>
                    <div style="background-color: #eee; padding: 5px 10px; border-radius: 5px;">
                        {estado} ({dias_restantes} días)
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    else:
        st.info("No se encontraron obligaciones cargadas para este perfil en la versión demo.")

elif nit and not nit.isdigit():
    st.error("El NIT debe contener solo números.")

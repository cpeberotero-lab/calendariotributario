import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 1. BASE DE DATOS UNIFICADA
# ==========================================
# Estructura: 
# - 'criterio': '1D' (Último dígito) o '2D' (Últimos dos dígitos)
# - 'digito': El número (0-9 para 1D, 00-99 para 2D)
# - 'categoria': A quién le aplica (GC = Grandes Contribuyentes, PJ = Personas Jurídicas, PN = Personas Naturales, General = Todos)

DB_CALENDARIO = []

def agregar_vencimiento_1d(impuesto, categoria, periodo, fecha_base, dias_consecutivos=True):
    """
    Genera fechas para impuestos basados en 1 solo dígito (IVA, Rete, Renta PJ/GC)
    Patrón típico DIAN: 1, 2, 3, 4, 5, 6, 7, 8, 9, 0
    """
    # Fechas simuladas basadas en el PDF (Simplificado para el demo)
    # En producción, aquí irían las fechas exactas del calendario.
    fechas_ejemplo = pd.date_range(start=fecha_base, periods=10, freq='B') # 'B' son días hábiles aprox
    
    digitos_orden = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    
    for d, f in zip(digitos_orden, fechas_ejemplo):
        DB_CALENDARIO.append({
            "Impuesto": impuesto,
            "Categoria": categoria,
            "Periodo": periodo,
            "Criterio": "1D",
            "Valor_Criterio": str(d), # Guardamos como string para comparar fácil
            "Fecha_Limite": f.strftime("%Y-%m-%d")
        })

def agregar_vencimiento_2d_pn(impuesto, categoria, periodo, fecha_base):
    """
    Genera fechas para Renta Personas Naturales (Basado en 2 últimos dígitos) 
    Patrón: 01-02, 03-04, ... 99-00
    """
    # Simulamos el calendario de Ago-Oct para PN
    fechas_ejemplo = pd.date_range(start=fecha_base, periods=50, freq='B') 
    
    contador_fecha = 0
    for i in range(1, 101): # Del 01 al 100 (donde 100 representa 00)
        # Formatear el dígito a 2 caracteres (ej. '01', '09', '99', '00')
        val_str = f"{i:02d}" if i < 100 else "00"
        
        # Cada fecha aplica para 2 números consecutivos (ej. 01 y 02 el mismo día)
        fecha = fechas_ejemplo[contador_fecha // 2]
        
        DB_CALENDARIO.append({
            "Impuesto": impuesto,
            "Categoria": categoria,
            "Periodo": periodo,
            "Criterio": "2D",
            "Valor_Criterio": val_str,
            "Fecha_Limite": fecha.strftime("%Y-%m-%d")
        })
        contador_fecha += 1

# --- CARGA DE DATOS DEMO ---

# 1. Renta Grandes Contribuyentes (Usa 1 dígito - Ver PDF source: 10)
agregar_vencimiento_1d("Renta - Grandes Contribuyentes", "Solo Grandes Contribuyentes", "Pago 2a Cuota", "2026-04-10")

# 2. Renta Personas Jurídicas (Usa 1 dígito - Ver PDF source: 20)
agregar_vencimiento_1d("Renta - Personas Jurídicas", "Personas Jurídicas", "Decl. y Pago 1a Cuota", "2026-05-11")

# 3. IVA Bimestral (Usa 1 dígito - General)
agregar_vencimiento_1d("IVA Bimestral", "Régimen Común / GC", "Periodo Ene-Feb", "2026-03-10")

# 4. Retención en la Fuente (Usa 1 dígito - General)
agregar_vencimiento_1d("Retención en la Fuente", "Agentes Retenedores", "Mensual - Enero", "2026-02-10")

# 5. Renta Personas Naturales (Usa 2 dígitos - Ver PDF source: 35)
# Esto demostrará la lógica inteligente cuando metas un NIT largo.
agregar_vencimiento_2d_pn("Renta - Personas Naturales", "Personas Naturales", "Declaración de Renta", "2026-08-11")


# ==========================================
# 2. INTERFAZ MEJORADA
# ==========================================

st.set_page_config(page_title="Calendario Tributario 2026", layout="centered", page_icon="🇨🇴")

st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .card {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        border-left: 6px solid #ccc;
    }
    .card-GC { border-left-color: #6f42c1; } /* Morado para Grandes Contribuyentes */
    .card-PJ { border-left-color: #0d6efd; } /* Azul para Personas Jurídicas */
    .card-PN { border-left-color: #198754; } /* Verde para Personas Naturales */
    
    .badge {
        display: inline-block;
        padding: 0.25em 0.4em;
        font-size: 75%;
        font-weight: 700;
        color: #fff;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 0.25rem;
    }
    .bg-GC { background-color: #6f42c1; }
    .bg-PJ { background-color: #0d6efd; }
    .bg-PN { background-color: #198754; }
    .bg-GEN { background-color: #6c757d; }
    </style>
""", unsafe_allow_html=True)

st.title("🔎 Agenda Tributaria Unificada")
st.markdown("Ingresa el NIT completo. El sistema detectará automáticamente todas las posibles obligaciones según el último o los dos últimos dígitos.")

# Solo un input
nit_input = st.text_input("Ingrese NIT (sin dígito de verificación):", placeholder="Ej: 800123456")

if nit_input and nit_input.isdigit():
    # --- LÓGICA DE EXTRACCIÓN ---
    last_1 = nit_input[-1]       # Último dígito (Ej. 6)
    last_2 = nit_input[-2:]      # Últimos dos (Ej. 56)
    
    st.info(f"Analizando para NIT terminado en **{last_1}** (Regla general) y **{last_2}** (Regla Personas Naturales).")
    
    # --- FILTRADO INTELIGENTE ---
    df = pd.DataFrame(DB_CALENDARIO)
    
    # Buscamos coincidencias: 
    # 1. Que el criterio sea '1D' y coincida con last_1
    # 2. O que el criterio sea '2D' y coincida con last_2
    
    mask_1d = (df['Criterio'] == '1D') & (df['Valor_Criterio'] == last_1)
    mask_2d = (df['Criterio'] == '2D') & (df['Valor_Criterio'] == last_2)
    
    resultados = df[mask_1d | mask_2d].copy()
    
    # Ordenar por fecha
    resultados['Fecha_DT'] = pd.to_datetime(resultados['Fecha_Limite'])
    resultados = resultados.sort_values(by='Fecha_DT')
    
    st.divider()
    
    if not resultados.empty:
        for _, row in resultados.iterrows():
            # Determinar estilo según categoría
            css_class = "card"
            badge_class = "bg-GEN"
            if "Grandes" in row['Categoria']: 
                css_class += " card-GC"
                badge_class = "bg-GC"
            elif "Jurídicas" in row['Categoria']: 
                css_class += " card-PJ"
                badge_class = "bg-PJ"
            elif "Naturales" in row['Categoria']: 
                css_class += " card-PN"
                badge_class = "bg-PN"
            
            # HTML Card
            st.markdown(f"""
            <div class="{css_class}">
                <div style="display:flex; justify-content:space-between;">
                    <span class="badge {badge_class}">{row['Categoria']}</span>
                    <small>Regla: {row['Valor_Criterio']}</small>
                </div>
                <h4 style="margin: 5px 0;">{row['Impuesto']}</h4>
                <div>Periodo: {row['Periodo']}</div>
                <hr style="margin: 5px 0; border-top: 1px dashed #eee;">
                <strong>📅 Fecha Límite: {row['Fecha_Limite']}</strong>
            </div>
            """, unsafe_allow_html=True)
            
    else:
        st.warning("No se encontraron fechas exactas en la base de datos demo para este NIT.")

elif nit_input:
    st.error("Por favor ingrese solo números.")

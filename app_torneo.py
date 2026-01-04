import streamlit as st
import pandas as pd

st.set_page_config(page_title="🏆 Torneo Pro", layout="wide")
st.title("⚽ Sistema de Gestión de Campeonatos")

archivo_excel = "testv2.xlsx" 

try:
    # 1. Leer las pestañas con los nombres reales de tu archivo
    df_equipos = pd.read_excel(archivo_excel, sheet_name="EQUIPOS")
    df_partidos = pd.read_excel(archivo_excel, sheet_name="PARTIDOS")
    df_jugadores = pd.read_excel(archivo_excel, sheet_name="JUGADORES")
    df_goles = pd.read_excel(archivo_excel, sheet_name="GOLES")

    # --- TABLA DE POSICIONES ---
    # Usamos los nombres de columna exactos de tu Excel: ID_Equipo (Key)
    posiciones = df_equipos[['ID_Equipo (Key)', 'Nombre', 'Grupo']].copy()
    posiciones.columns = ['ID', 'Nombre', 'Grupo']
    posiciones[['PJ', 'PG', 'PE', 'PP', 'GF', 'GC', 'PTS']] = 0

    for _, p in df_partidos.iterrows():
        # Verificamos si hay goles anotados y si el estado es 'Finalizado' (opcional)
        if pd.notnull(p['Goles_E1']) and pd.notnull(p['Goles_E2']):
            e1, e2 = p['ID_Equipo_1'], p['ID_Equipo_2']
            g1, g2 = int(p['Goles_E1']), int(p['Goles_E2'])

            # Actualizar estadísticas
            for eq, gf, gc in [(e1, g1, g2), (e2, g2, g1)]:
                posiciones.loc[posiciones['ID'] == eq, 'PJ'] += 1
                posiciones.loc[posiciones['ID'] == eq, 'GF'] += gf
                posiciones.loc[posiciones['ID'] == eq, 'GC'] += gc

            if g1 > g2:
                posiciones.loc[posiciones['ID'] == e1, 'PG'] += 1
                posiciones.loc[posiciones['ID'] == e1, 'PTS'] += 3
                posiciones.loc[posiciones['ID'] == e2, 'PP'] += 1
            elif g2 > g1:
                posiciones.loc[posiciones['ID'] == e2, 'PG'] += 1
                posiciones.loc[posiciones['ID'] == e2, 'PTS'] += 3
                posiciones.loc[posiciones['ID'] == e1, 'PP'] += 1
            else:
                posiciones.loc[posiciones['ID'] == e1, 'PE'] += 1
                posiciones.loc[posiciones['ID'] == e2, 'PE'] += 1
                posiciones.loc[posiciones['ID'] == e1, 'PTS'] += 1
                posiciones.loc[posiciones['ID'] == e2, 'PTS'] += 1

    posiciones['DG'] = posiciones['GF'] - posiciones['GC']
    posiciones = posiciones.sort_values(by=['PTS', 'DG'], ascending=False)

    # --- INTERFAZ ---
    tab1, tab2 = st.tabs(["📊 Posiciones", "📅 Partidos"])
    with tab1:
        st.subheader("Tabla General")
        st.dataframe(posiciones, use_container_width=True, hide_index=True)
    with tab2:
        st.subheader("Resultados Registrados")
        st.dataframe(df_partidos, use_container_width=True)

except Exception as e:
    st.error(f"Error detectado: {e}")
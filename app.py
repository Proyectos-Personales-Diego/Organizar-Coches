import streamlit as st

st.set_page_config(page_title="Organizador de Coches", page_icon="🚗", layout="centered")

st.title("🚗 Coches para el Finde")

# Inicializar base de datos temporal en memoria
if 'coches' not in st.session_state:
    st.session_state.coches = {}

# Formulario para crear un coche nuevo
with st.expander("➕ Ofrecer mi coche", expanded=False):
    with st.form("form_crear"):
        conductor = st.text_input("Tu Nombre (Conductor)")
        plazas = st.number_input("Plazas libres (sin contarte a ti)", min_value=1, max_value=8, value=4)
        if st.form_submit_button("Crear Coche"):
            if conductor:
                st.session_state.coches[conductor] = {"plazas": plazas, "pasajeros": []}
                st.success(f"Coche de {conductor} creado correctamente.")
                st.rerun()

st.divider()

# Listar coches y gestionar los pasajeros
if not st.session_state.coches:
    st.info("Aún no hay coches disponibles. ¡Anímate a llevar el tuyo!")
else:
    for conductor, info in list(st.session_state.coches.items()):
        plazas_totales = info["plazas"]
        pasajeros = info["pasajeros"]
        huecos_libres = plazas_totales - len(pasajeros)
        
        st.markdown(f"**🚙 Coche de {conductor}** — {huecos_libres} huecos libres de {plazas_totales}")
        
        if pasajeros:
            st.write(f"👥 Pasajeros: {', '.join(pasajeros)}")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if huecos_libres > 0:
                with st.form(key=f"subir_{conductor}"):
                    nuevo = st.text_input("Tu nombre", key=f"in_{conductor}", placeholder="Escribe tu nombre")
                    if st.form_submit_button("Me subo"):
                        if nuevo and nuevo not in pasajeros:
                            st.session_state.coches[conductor]["pasajeros"].append(nuevo)
                            st.rerun()
        with col2:
            if st.button("🗑️ Borrar", key=f"del_{conductor}"):
                del st.session_state.coches[conductor]
                st.rerun()
        st.divider()
import streamlit as st

st.set_page_config(page_title="Organizador de Coches", page_icon="🚗", layout="centered")

st.title("🚗 Coches para el Finde")

# --- MAGIA PARA COMPARTIR ESTADO ENTRE USUARIOS ---
@st.cache_resource
def get_base_datos():
    return {} # Devuelve un diccionario que será el mismo para todos

# Llamamos a la base de datos global
coches_db = get_base_datos()
# --------------------------------------------------

# Formulario para crear un coche nuevo
with st.expander("➕ Ofrecer mi coche", expanded=False):
    with st.form("form_crear"):
        conductor = st.text_input("Tu Nombre (Conductor)")
        plazas = st.number_input("Plazas libres (sin contarte a ti)", min_value=1, max_value=8, value=4)
        if st.form_submit_button("Crear Coche"):
            if conductor:
                # OJO: Ahora guardamos en coches_db, no en session_state
                coches_db[conductor] = {"plazas": plazas, "pasajeros": []}
                st.success(f"Coche de {conductor} creado correctamente.")
                st.rerun()

st.divider()

# Listar coches y gestionar pasajeros
if not coches_db:
    st.info("Aún no hay coches disponibles. ¡Anímate a llevar el tuyo!")
else:
    for conductor, info in list(coches_db.items()):
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
                            coches_db[conductor]["pasajeros"].append(nuevo)
                            st.rerun()
        with col2:
            if st.button("🗑️ Borrar", key=f"del_{conductor}"):
                del coches_db[conductor]
                st.rerun()
        st.divider()
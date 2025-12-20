import streamlit as st

def show_login_form(auth_controller):
    """Display login form with email"""
    
    st.markdown("""
    <style>
    .auth-container {
        max-width: 450px;
        margin: 40px auto;
        padding: 40px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        color: white;
    }
    .auth-header {
        text-align: center;
        margin-bottom: 30px;
    }
    .auth-tabs {
        display: flex;
        margin-bottom: 25px;
        border-bottom: 1px solid rgba(255,255,255,0.3);
    }
    .auth-form {
        background: rgba(255,255,255,0.1);
        padding: 25px;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    .stTextInput>div>div>input, .stTextInput>div>div>input:focus {
        background: rgba(255,255,255,0.9);
        border: 1px solid rgba(255,255,255,0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
    if 'auth_tab' not in st.session_state:
        st.session_state.auth_tab = 'login'
    
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="auth-header">
        <h2 style="margin:0; color: white;">🔐 SISTEM BANJIR</h2>
        <p style="margin:10px 0 0 0; opacity:0.9;">Masuk atau daftar untuk mengakses sistem</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Login", use_container_width=True, 
                    type="primary" if st.session_state.auth_tab == 'login' else "secondary"):
            st.session_state.auth_tab = 'login'
            st.rerun()
    with col2:
        if st.button("📝 Daftar", use_container_width=True,
                    type="primary" if st.session_state.auth_tab == 'register' else "secondary"):
            st.session_state.auth_tab = 'register'
            st.rerun()
    
    st.markdown('<div class="auth-form">', unsafe_allow_html=True)
    
    if st.session_state.auth_tab == 'login':
        _show_login_tab(auth_controller)
    else:
        _show_register_tab(auth_controller)
    
    st.markdown('</div>', unsafe_allow_html=True)  
    st.markdown('</div>', unsafe_allow_html=True)  

def _show_login_tab(auth_controller):
    """Show login tab content"""
    st.markdown('<h3 style="text-align:center; color:white; margin-bottom:25px;">Masuk ke Akun</h3>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        email = st.text_input(
            "Email Address",
            placeholder="contoh@email.com",
            help="Masukkan alamat email yang terdaftar"
        )
        
        password = st.text_input(
            "Password", 
            type="password",
            placeholder="Masukkan password",
            help="Masukkan password akun Anda"
        )
        
        col1, col2 = st.columns([1, 2])
        with col1:
            remember_me = st.checkbox("Ingat saya")
        
        login_button = st.form_submit_button(
            "Login ke Sistem", 
            use_container_width=True,
            type="primary"
        )
        
        if login_button:
            if not email or not password:
                st.error("❌ Email dan password harus diisi!")
            else:
                with st.spinner("Memverifikasi..."):
                    success, result = auth_controller.login(email, password)
                    
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_data = result
                        st.success(f"✅ Login berhasil! Selamat datang {result['full_name']}")
                        st.rerun()
                    else:
                        st.error(f"❌ {result}")

def _show_register_tab(auth_controller):
    """Show register tab content"""
    st.markdown('<h3 style="text-align:center; color:white; margin-bottom:25px;">Buat Akun Baru</h3>', unsafe_allow_html=True)
    
    with st.form("register_form"):
        full_name = st.text_input(
            "Nama Lengkap",
            placeholder="Masukkan nama lengkap",
            help="Nama lengkap Anda"
        )
        
        email = st.text_input(
            "Email Address",
            placeholder="contoh@email.com",
            help="Gunakan email yang valid"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Minimal 6 karakter",
                help="Password minimal 6 karakter"
            )
        
        with col2:
            confirm_password = st.text_input(
                "Konfirmasi Password",
                type="password", 
                placeholder="Ulangi password",
                help="Harus sama dengan password"
            )
        
        agree_terms = st.checkbox("Saya menyetujui syarat dan ketentuan")
        
        register_button = st.form_submit_button(
            "Daftar Akun Baru",
            use_container_width=True,
            type="primary"
        )
        
        if register_button:
            if not all([full_name, email, password, confirm_password]):
                st.error("❌ Semua field harus diisi!")
            elif not agree_terms:
                st.error("❌ Anda harus menyetujui syarat dan ketentuan!")
            else:
                with st.spinner("Mendaftarkan akun..."):
                    success, message = auth_controller.register(
                        email, password, full_name, confirm_password
                    )
                    
                    if success:
                        st.success(f"✅ {message}")
                        st.session_state.auth_tab = 'login'
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")

def show_logout_section():
    """Display logout section in sidebar"""
    if st.session_state.get('logged_in'):
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**👋 Halo, {st.session_state.user_data['full_name']}**")
        st.sidebar.markdown(f"*{st.session_state.user_data['email']}*")
        
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_data = None
            st.session_state.current_page = "Home"
            st.rerun()

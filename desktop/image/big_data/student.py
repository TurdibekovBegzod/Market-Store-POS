import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import hashlib
import json
import os

st.set_page_config(page_title="EduPredict - Aqlli Ta'lim Tizimi", layout="wide")

# ============================================
# 1. FOYDALANUVCHILAR BAZASI (Database)
# ============================================

# Parolni xeshlash funksiyasi
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Foydalanuvchilar ma'lumotlari (real loyihada bu ma'lumotlar bazasida saqlanadi)
USERS_DB = {
    # Direktor
    "director": {
        "password": hash_password("director123"),
        "role": "director",
        "name": "Direktor Abdullayev",
        "school_id": 1
    },
    
    # O'qituvchilar
    "teacher_ali": {
        "password": hash_password("teacher123"),
        "role": "teacher",
        "name": "Aliyev Alisher",
        "class": "8-A",
        "subject": "matematika",
        "school_id": 1
    },
    "teacher_nilufar": {
        "password": hash_password("teacher123"),
        "role": "teacher",
        "name": "Karimova Nilufar",
        "class": "9-B",
        "subject": "matematika",
        "school_id": 1
    },
    
    # Ota-onalar
    "parent_ali": {
        "password": hash_password("parent123"),
        "role": "parent",
        "name": "Aliyev Bobur",
        "child_name": "Aliyev Ali",
        "child_id": 1,
        "school_id": 1
    },
    "parent_lola": {
        "password": hash_password("parent123"),
        "role": "parent",
        "name": "Karimova Lola",
        "child_name": "Karimova Malika",
        "child_id": 2,
        "school_id": 1
    },
    
    # Talabalar
    "student_ali": {
        "password": hash_password("student123"),
        "role": "student",
        "name": "Aliyev Ali",
        "class": "8-A",
        "student_id": 1,
        "school_id": 1
    },
    "student_malika": {
        "password": hash_password("student123"),
        "role": "student",
        "name": "Karimova Malika",
        "class": "9-B",
        "student_id": 2,
        "school_id": 1
    },
    "student_jasur": {
        "password": hash_password("student123"),
        "role": "student",
        "name": "Rahimov Jasur",
        "class": "8-A",
        "student_id": 3,
        "school_id": 1
    }
}

# ============================================
# 2. MA'LUMOTLAR BAZASI (Data)
# ============================================

@st.cache_data
def load_students_data():
    """Talabalar ma'lumotlarini yuklash"""
    return pd.read_csv('D://9_smester//big_data//StudentsPerformance.csv')

@st.cache_data
def load_attendance_data():
    """Davomat ma'lumotlarini yaratish (real loyihada alohida fayldan o'qiladi)"""
    np.random.seed(42)
    students = load_students_data()
    attendance = pd.DataFrame({
        'student_id': range(1, len(students) + 1),
        'attendance_rate': np.random.uniform(70, 100, len(students)),
        'homework_completion': np.random.uniform(50, 100, len(students)),
        'participation_score': np.random.uniform(40, 100, len(students))
    })
    return attendance

def get_student_by_class(df, class_name):
    """Sinf bo'yicha talabalarni olish"""
    # Bu yerda haqiqiy ma'lumotlarda class ustuni bo'lishi kerak
    # Hozircha namuna sifatida
    return df.head(10)  # Vaqtinchalik

def get_student_by_id(student_id):
    """ID bo'yicha talaba ma'lumotlarini olish"""
    df = load_students_data()
    if student_id <= len(df):
        return df.iloc[student_id - 1]
    return None

# ============================================
# 3. LOGIN QISMI
# ============================================

def login():
    """Login formasi"""
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 30px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }
    .login-title {
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.image("https://img.icons8.com/color/96/000000/education--v1.png", width=100)
        st.markdown("<h1 style='text-align: center;'>📚 EduPredict</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Aqlli Ta'lim Prognoz Tizimi</p>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        username = st.text_input("👤 Login", placeholder="Loginingizni kiriting")
        password = st.text_input("🔒 Parol", type="password", placeholder="Parolingizni kiriting")
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            login_btn = st.button("🚪 Kirish", use_container_width=True)
        
        if login_btn:
            if username in USERS_DB:
                if USERS_DB[username]["password"] == hash_password(password):
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = username
                    st.session_state["user_info"] = USERS_DB[username]
                    st.rerun()
                else:
                    st.error("❌ Parol xato!")
            else:
                st.error("❌ Bunday foydalanuvchi topilmadi!")
        
        st.markdown("---")
        st.markdown("""
        <p style='text-align: center; font-size: 12px; color: gray;'>
        Demo hisoblar:<br>
        Direktor: director / director123<br>
        O'qituvchi: teacher_ali / teacher123<br>
        Ota-ona: parent_ali / parent123<br>
        Talaba: student_ali / student123
        </p>
        """, unsafe_allow_html=True)

def logout():
    """Chiqish funksiyasi"""
    if st.sidebar.button("🚪 Chiqish", use_container_width=True):
        for key in ["logged_in", "user", "user_info"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# ============================================
# 4. MODELLARNI O'RGATISH FUNKSIYALARI
# ============================================

@st.cache_resource
def train_model():
    """Baholarni prognoz qilish modelini o'rgatish"""
    df = load_students_data()
    
    categorical_cols = ['gender', 'race/ethnicity', 'parental level of education', 'lunch', 'test preparation course']
    df_encoded = df.copy()
    
    for col in categorical_cols:
        le = LabelEncoder()
        df_encoded[col] = le.fit_transform(df_encoded[col])
    
    feature_cols = categorical_cols
    X = df_encoded[feature_cols]
    y = df_encoded['math score']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    model = XGBRegressor(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)
    
    return model, scaler, df_encoded, feature_cols

# ============================================
# 5. FOYDALANUVCHI INTERFEYSLARI
# ============================================

def director_dashboard(user_info):
    """Direktor dashboardi"""
    st.markdown(f"## 🏫 Direktor Dashboardi")
    st.markdown(f"### 👋 Assalomu alaykum, {user_info['name']}!")
    
    df = load_students_data()
    
    # Umumiy statistika
    st.markdown("---")
    st.subheader("📊 Umumiy statistika")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📚 Jami talabalar", len(df))
    with col2:
        st.metric("📖 O'rtacha matematika", f"{df['math score'].mean():.1f}")
    with col3:
        st.metric("📖 O'rtacha o'qish", f"{df['reading score'].mean():.1f}")
    with col4:
        st.metric("✍️ O'rtacha yozuv", f"{df['writing score'].mean():.1f}")
    
    # Barcha talabalar jadvali
    st.markdown("---")
    st.subheader("👨‍🎓 Barcha talabalar ro'yxati")
    st.dataframe(df, use_container_width=True)
    
    # Sinflar reytingi
    st.markdown("---")
    st.subheader("🏆 Sinflar reytingi")
    
    # Vaqtinchalik sinf reytingi
    classes = ['8-A', '8-B', '9-A', '9-B', '10-A', '10-B']
    scores = [82.5, 78.3, 85.1, 74.2, 88.4, 79.6]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['gold' if i==0 else 'silver' if i==1 else 'bronze' if i==2 else 'skyblue' for i in range(len(scores))]
    ax.bar(classes, scores, color=colors)
    ax.set_ylabel('O\'rtacha ball')
    ax.set_title('Sinflar reytingi')
    ax.axhline(y=80, color='red', linestyle='--', label='Maqsad (80 ball)')
    ax.legend()
    st.pyplot(fig)
    
    # Xavf zonasidagi talabalar
    st.markdown("---")
    st.subheader("⚠️ Xavf zonasidagi talabalar (60 balldan past)")
    
    model, scaler, df_encoded, feature_cols = train_model()
    X = df_encoded[feature_cols]
    X_scaled = scaler.transform(X)
    predictions = model.predict(X_scaled)
    
    df['prognoz'] = predictions
    at_risk = df[df['prognoz'] < 60]
    
    if len(at_risk) > 0:
        st.warning(f"⚠️ {len(at_risk)} nafar talaba xavf zonasida!")
        st.dataframe(at_risk[['math score', 'reading score', 'writing score', 'prognoz']], use_container_width=True)
    else:
        st.success("✅ Xavf zonasida talabalar yo'q!")

def teacher_dashboard(user_info):
    """O'qituvchi dashboardi"""
    st.markdown(f"## 📚 O'qituvchi Dashboardi")
    st.markdown(f"### 👋 Assalomu alaykum, {user_info['name']}!")
    st.markdown(f"### 🏫 Sinf: {user_info['class']} | 📖 Fan: {user_info['subject'].capitalize()}")
    
    df = load_students_data()
    
    # O'z sinfidagi talabalarni ko'rsatish
    st.markdown("---")
    st.subheader(f"👨‍🎓 {user_info['class']} sinfidagi talabalar")
    
    # Vaqtinchalik sinf ma'lumotlari
    class_students = df.head(15).copy()
    class_students['Sinf'] = user_info['class']
    class_students['Ism'] = [f"Talaba {i+1}" for i in range(len(class_students))]
    
    st.dataframe(class_students[['Ism', 'math score', 'reading score', 'writing score']], use_container_width=True)
    
    # Modelni o'rgatish va prognoz
    st.markdown("---")
    st.subheader("🔮 Talaba baholarini prognoz qilish")
    
    model, scaler, df_encoded, feature_cols = train_model()
    X = df_encoded[feature_cols]
    X_scaled = scaler.transform(X)
    predictions = model.predict(X_scaled)
    
    df['prognoz'] = predictions
    
    # Har bir talaba uchun prognoz
    for idx, row in class_students.head(5).iterrows():
        with st.container():
            col1, col2, col3 = st.columns([2,1,2])
            with col1:
                st.write(f"**{row['Ism']}**")
            with col2:
                st.write(f"Hozirgi: {row['math score']:.0f}")
            with col3:
                prog = predictions[idx]
                if prog > row['math score']:
                    st.success(f"Prognoz: {prog:.0f} ↑")
                elif prog < row['math score']:
                    st.warning(f"Prognoz: {prog:.0f} ↓")
                else:
                    st.info(f"Prognoz: {prog:.0f} →")
    
    # Erta ogohlantirish
    st.markdown("---")
    st.subheader("🚨 Erta ogohlantirish")
    
    at_risk = df[df['prognoz'] < 60].head(5)
    if len(at_risk) > 0:
        st.warning("Quyidagi talabalar yordamga muhtoj:")
        for idx, row in at_risk.iterrows():
            st.write(f"- Talaba {idx+1}: matematika prognozi {row['prognoz']:.0f} ball")
    else:
        st.success("✅ Xavf zonasida talabalar yo'q!")

def parent_dashboard(user_info):
    """Ota-ona dashboardi"""
    st.markdown(f"## 👪 Ota-ona Dashboardi")
    st.markdown(f"### 👋 Assalomu alaykum, {user_info['name']}!")
    st.markdown(f"### 👶 Farzandingiz: {user_info['child_name']}")
    
    df = load_students_data()
    child_id = user_info['child_id']
    
    if child_id <= len(df):
        child_data = df.iloc[child_id - 1]
        
        # Farzand haqida ma'lumot
        st.markdown("---")
        st.subheader(f"📊 {user_info['child_name']}ning natijalari")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📐 Matematika", f"{child_data['math score']}")
        with col2:
            st.metric("📖 O'qish", f"{child_data['reading score']}")
        with col3:
            st.metric("✍️ Yozuv", f"{child_data['writing score']}")
        
        # Prognoz
        st.markdown("---")
        st.subheader("🔮 Prognoz")
        
        model, scaler, df_encoded, feature_cols = train_model()
        X = df_encoded[feature_cols]
        X_scaled = scaler.transform(X)
        predictions = model.predict(X_scaled)
        
        prediction = predictions[child_id - 1]
        
        col1, col2 = st.columns(2)
        with col1:
            if prediction >= 80:
                st.success(f"🎯 Matematika prognozi: {prediction:.0f} ball")
            elif prediction >= 60:
                st.warning(f"🎯 Matematika prognozi: {prediction:.0f} ball")
            else:
                st.error(f"🎯 Matematika prognozi: {prediction:.0f} ball")
        
        with col2:
            if prediction > child_data['math score']:
                st.info(f"📈 O'sish: +{prediction - child_data['math score']:.0f} ball")
            elif prediction < child_data['math score']:
                st.warning(f"📉 Pasayish: {prediction - child_data['math score']:.0f} ball")
            else:
                st.info("📊 O'zgarish yo'q")
        
        # Tavsiyalar
        st.markdown("---")
        st.subheader("💡 Tavsiyalar")
        
        if prediction < 60:
            st.error("""
            ⚠️ **Farzandingiz yordamga muhtoj!**
            - Har kuni 30 daqiqa matematikaga vaqt ajrating
            - Maktabda qo'shimcha darslarga yoziling
            - Onlayn testlarni yechishni tavsiya qilamiz
            """)
        elif prediction < 75:
            st.warning("""
            📚 **O'rtacha natija, yaxshilash mumkin!**
            - Qiyin mavzularni aniqlang
            - Haftada 2 marta repetitor bilan shug'ullaning
            """)
        else:
            st.success("""
            🎉 **Farzandingiz yaxshi natija ko'rsatmoqda!**
            - Yuqori darajani saqlab qolish uchun davom eting
            - Olimpiadalarda qatnashishni tavsiya qilamiz
            """)
        
        # Vizualizatsiya
        fig, ax = plt.subplots(figsize=(10, 5))
        subjects = ['Matematika', 'O\'qish', 'Yozuv', 'Prognoz']
        values = [child_data['math score'], child_data['reading score'], child_data['writing score'], prediction]
        colors = ['#3498db', '#2ecc71', '#e74c3c', '#9b59b6']
        ax.bar(subjects, values, color=colors)
        ax.set_ylabel('Ball')
        ax.set_title(f"{user_info['child_name']}ning natijalari")
        ax.axhline(y=60, color='red', linestyle='--', label='Chegara (60 ball)')
        ax.legend()
        st.pyplot(fig)
        
    else:
        st.error("❌ Farzandingiz haqida ma'lumot topilmadi!")

def student_dashboard(user_info):
    """Talaba dashboardi"""
    st.markdown(f"## 🎓 Talaba Dashboardi")
    st.markdown(f"### 👋 Assalomu alaykum, {user_info['name']}!")
    st.markdown(f"### 🏫 Sinf: {user_info['class']}")
    
    df = load_students_data()
    student_id = user_info['student_id']
    
    if student_id <= len(df):
        student_data = df.iloc[student_id - 1]
        
        # Natijalar
        st.markdown("---")
        st.subheader("📊 Sizning natijalaringiz")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📐 Matematika", f"{student_data['math score']}")
        with col2:
            st.metric("📖 O'qish", f"{student_data['reading score']}")
        with col3:
            st.metric("✍️ Yozuv", f"{student_data['writing score']}")
        
        # O'rtacha ball
        avg = (student_data['math score'] + student_data['reading score'] + student_data['writing score']) / 3
        st.metric("📊 Umumiy o'rtacha", f"{avg:.1f}")
        
        # Prognoz
        st.markdown("---")
        st.subheader("🔮 Kelajak prognozi")
        
        model, scaler, df_encoded, feature_cols = train_model()
        X = df_encoded[feature_cols]
        X_scaled = scaler.transform(X)
        predictions = model.predict(X_scaled)
        
        prediction = predictions[student_id - 1]
        
        if prediction >= 80:
            st.success(f"🎯 Matematika prognozi: {prediction:.0f} ball - Yaxshi natija!")
        elif prediction >= 60:
            st.warning(f"🎯 Matematika prognozi: {prediction:.0f} ball - Yaxshilash mumkin")
        else:
            st.error(f"🎯 Matematika prognozi: {prediction:.0f} ball - Ko'proq harakat kerak")
        
        # Qaysi fan kuchli/qaysi fan kuchsiz?
        st.markdown("---")
        st.subheader("📈 Sizning SWOT tahlilingiz")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**💪 Kuchli tomonlaringiz:**")
            scores = {
                'Matematika': student_data['math score'],
                'O\'qish': student_data['reading score'],
                'Yozuv': student_data['writing score']
            }
            best_subject = max(scores, key=scores.get)
            if scores[best_subject] >= 80:
                st.success(f"✅ {best_subject} - bu sizning kuchli tomoningiz!")
            else:
                st.info(f"📚 {best_subject} da eng yaxshi natijaga egasiz")
        
        with col2:
            st.markdown("**📈 Rivojlanish kerak bo'lgan joylar:**")
            worst_subject = min(scores, key=scores.get)
            if scores[worst_subject] < 60:
                st.warning(f"⚠️ {worst_subject} - bu fanga ko'proq e'tibor bering!")
            else:
                st.info(f"📚 {worst_subject} ni yanada yaxshilashingiz mumkin")
        
        # Motivatsiya
        st.markdown("---")
        st.subheader("🏆 Motivatsiya")
        
        if avg >= 85:
            st.balloons()
            st.success("🎉 Ajoyib! Siz a'lo talabasiz! Olimpiadalarda qatnashing!")
        elif avg >= 70:
            st.info("👍 Yaxshi! Yuqori natija uchun yana 15 ball kerak. Davom eting!")
        elif avg >= 60:
            st.warning("💪 Taslim bo'lmang! Har kuni 30 daqiqa ko'proq o'qing!")
        else:
            st.error("📚 Hali vaqt bor! O'qituvchingizdan yordam so'rang va ko'proq mashq qiling!")
        
        # Kunlik topshiriq
        st.markdown("---")
        st.subheader("📝 Bugungi topshiriq")
        
        import random
        tasks = [
            "10 ta kasrlar bilan bog'liq misol yeching",
            "Onlayn testda qatnashing (20 daqiqa)",
            "Qiyin mavzuni aniqlang va uni o'rganing",
            "Sinfdoshingizga bir mavzuni tushuntirib bering",
            "5 ta yangi so'zni o'rganing va ular bilan gap tuzing"
        ]
        st.write(f"✅ {random.choice(tasks)}")
        
    else:
        st.error("❌ Ma'lumotlar topilmadi!")

# ============================================
# 6. ASOSIY DASTUR
# ============================================

def main():
    """Asosiy dastur"""
    
    # Login tekshiruvi
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        login()
        return
    
    user_info = st.session_state["user_info"]
    
    # Sidebar - foydalanuvchi ma'lumotlari
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/education--v1.png", width=60)
        st.markdown(f"### 👤 {user_info['name']}")
        st.markdown(f"**Rol:** {user_info['role'].capitalize()}")
        
        st.markdown("---")
        
        # Foydalanuvchi rolga qarab menu
        if user_info['role'] == "director":
            st.markdown("### 📋 Menu")
            st.markdown("- 🏫 Bosh sahifa")
            st.markdown("- 📊 Statistika")
            st.markdown("- 👨‍🎓 Talabalar")
            st.markdown("- 🏆 Reyting")
        
        elif user_info['role'] == "teacher":
            st.markdown("### 📋 Menu")
            st.markdown("- 📚 Sinfim")
            st.markdown("- 🔮 Prognoz")
            st.markdown("- 🚨 Ogohlantirish")
        
        elif user_info['role'] == "parent":
            st.markdown("### 📋 Menu")
            st.markdown("- 👶 Farzandim")
            st.markdown("- 🔮 Prognoz")
            st.markdown("- 💡 Tavsiyalar")
        
        else:  # student
            st.markdown("### 📋 Menu")
            st.markdown("- 📊 Natijalarim")
            st.markdown("- 🔮 Prognoz")
            st.markdown("- 🏆 Motivatsiya")
        
        st.markdown("---")
        logout()
    
    # Rolga qarab dashboard
    if user_info['role'] == "director":
        director_dashboard(user_info)
    elif user_info['role'] == "teacher":
        teacher_dashboard(user_info)
    elif user_info['role'] == "parent":
        parent_dashboard(user_info)
    else:  # student
        student_dashboard(user_info)

if __name__ == "__main__":
    main()
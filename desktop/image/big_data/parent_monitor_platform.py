import hashlib
from datetime import date, timedelta

import numpy as np
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Ota-Onalar Nazorat Platformasi",
    page_icon="📘",
    layout="wide",
)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


PARENT_ACCOUNTS = {
    "aziza": {
        "password": hash_password("aziza123"),
        "parent_name": "Aziza Rahimova",
        "student_id": 1,
    },
    "dilshod": {
        "password": hash_password("dilshod123"),
        "parent_name": "Dilshod Karimov",
        "student_id": 2,
    },
    "malika": {
        "password": hash_password("malika123"),
        "parent_name": "Malika Tursunova",
        "student_id": 3,
    },
}


@st.cache_data
def load_students() -> pd.DataFrame:
    raw = pd.read_csv("StudentsPerformance.csv").copy()
    raw = raw.rename(
        columns={
            "math score": "Matematika",
            "reading score": "O'qish",
            "writing score": "Yozuv",
            "parental level of education": "Ota-ona_ta'limi",
            "test preparation course": "Tayyorlov",
        }
    )

    names = [
        "Ali Rahimov",
        "Madina Karimova",
        "Jasur Tursunov",
        "Sevinch Aliyeva",
        "Bekzod Ergashev",
        "Mohira Rasulova",
        "Asilbek Qodirov",
        "Nilufar Qobilova",
        "Samandar Jo'rayev",
        "Shahnoza Eshonova",
        "Zafar Ismoilov",
        "Diyora Usmonova",
    ]
    classes = ["5-A", "5-B", "6-A", "6-B", "7-A", "7-B"] * 2
    raw = raw.head(len(names)).copy()
    raw["student_id"] = np.arange(1, len(raw) + 1)
    raw["FISH"] = names
    raw["Sinf"] = classes[: len(raw)]

    attendance = [97, 88, 91, 84, 95, 79, 93, 90, 86, 98, 82, 89]
    homework = [100, 72, 90, 68, 94, 63, 88, 85, 74, 97, 70, 80]
    focus = [5, 3, 4, 3, 5, 2, 4, 4, 3, 5, 3, 4]
    absenteeism = [0, 3, 1, 4, 0, 5, 1, 2, 3, 0, 4, 2]
    raw["Davomat"] = attendance[: len(raw)]
    raw["Vazifa_bajarilishi"] = homework[: len(raw)]
    raw["Diqqat_darajasi"] = focus[: len(raw)]
    raw["Qoldirilgan_kunlar"] = absenteeism[: len(raw)]
    raw["Umumiy_baho"] = raw[["Matematika", "O'qish", "Yozuv"]].mean(axis=1).round(1)
    return raw


@st.cache_data
def build_weekly_activity() -> pd.DataFrame:
    days = pd.date_range(date.today() - timedelta(days=6), date.today(), freq="D")
    rows = []
    study_templates = {
        1: [2.0, 2.5, 1.5, 2.5, 3.0, 1.0, 2.0],
        2: [1.0, 1.0, 1.5, 1.0, 2.0, 0.5, 1.0],
        3: [1.5, 2.0, 2.0, 1.5, 2.0, 1.0, 1.5],
    }
    for student_id, template in study_templates.items():
        for day, hours in zip(days, template):
            rows.append(
                {
                    "student_id": student_id,
                    "Sana": day,
                    "O'qish_soati": hours,
                }
            )
    return pd.DataFrame(rows)


@st.cache_data
def get_teacher_notes() -> pd.DataFrame:
    return pd.DataFrame(
        [
            [1, "Sinfda faol, matematika fanidan kuchli.", "Matematika"],
            [1, "Uyga vazifani doim o'z vaqtida topshiradi.", "Sinf rahbari"],
            [2, "O'qish fanida ko'proq mashq kerak.", "Ona tili"],
            [2, "Davomat pasaygan, oilaviy nazoratni kuchaytirish foydali.", "Sinf rahbari"],
            [3, "Yozuv bo'yicha yaxshi o'sish ko'rsatmoqda.", "Ona tili"],
        ],
        columns=["student_id", "Izoh", "Muallif"],
    )


@st.cache_data
def get_tasks() -> pd.DataFrame:
    return pd.DataFrame(
        [
            [1, "Matematika testini yechish", "2026-04-08", "Yuqori", "Jarayonda"],
            [1, "Kitobdan 10 bet o'qish", "2026-04-07", "O'rta", "Bajarilgan"],
            [2, "Ona tili diktanti", "2026-04-07", "Yuqori", "Kutilmoqda"],
            [2, "Haftalik davomatni yaxshilash", "2026-04-12", "Yuqori", "Jarayonda"],
            [3, "Insho yozish", "2026-04-09", "O'rta", "Jarayonda"],
        ],
        columns=["student_id", "Topshiriq", "Muddat", "Muhimlik", "Holat"],
    )


def authenticate(username: str, password: str):
    account = PARENT_ACCOUNTS.get(username)
    if not account:
        return None
    if account["password"] != hash_password(password):
        return None
    return account


def login_page():
    st.title("📘 Ota-onalar uchun nazorat platformasi")
    st.write("Farzandingizning bahosi, davomat va vazifalarini bir joyda kuzatib boring.")

    left, center, right = st.columns([1, 1.2, 1])
    with center:
        with st.form("login_form"):
            username = st.text_input("Login")
            password = st.text_input("Parol", type="password")
            submitted = st.form_submit_button("Kirish", use_container_width=True)

        st.caption("Demo loginlar: `aziza / aziza123`, `dilshod / dilshod123`, `malika / malika123`")

        if submitted:
            account = authenticate(username.strip(), password)
            if account:
                st.session_state["account"] = account
                st.success("Muvaffaqiyatli kirildi.")
                st.rerun()
            st.error("Login yoki parol noto'g'ri.")


def get_risk_level(student: pd.Series) -> str:
    if student["Davomat"] < 85 or student["Vazifa_bajarilishi"] < 70:
        return "Yuqori ehtiyot"
    if student["Umumiy_baho"] < 75:
        return "O'rta ehtiyot"
    return "Barqaror"


def get_recommendations(student: pd.Series) -> list[str]:
    recommendations = []
    if student["Davomat"] < 90:
        recommendations.append("Davomatni tiklash uchun ertalabki tartibni qat'iylashtiring.")
    if student["Matematika"] < 70:
        recommendations.append("Har kuni 20 daqiqa matematika mashqi tashkil qiling.")
    if student["O'qish"] < 70:
        recommendations.append("Birgalikda ovoz chiqarib o'qish mashg'ulotini yo'lga qo'ying.")
    if student["Vazifa_bajarilishi"] < 80:
        recommendations.append("Uy vazifasi uchun alohida vaqt va tinch joy belgilang.")
    if not recommendations:
        recommendations.append("Hozirgi sur'at yaxshi, shu tartibni davom ettirish kifoya.")
    return recommendations


def dashboard():
    students = load_students()
    weekly = build_weekly_activity()
    notes = get_teacher_notes()
    tasks = get_tasks()

    account = st.session_state["account"]
    student = students.loc[students["student_id"] == account["student_id"]].iloc[0]
    student_weekly = weekly[weekly["student_id"] == student["student_id"]]
    student_notes = notes[notes["student_id"] == student["student_id"]]
    student_tasks = tasks[tasks["student_id"] == student["student_id"]]

    with st.sidebar:
        st.header("Hisob")
        st.write(account["parent_name"])
        st.write(f"Farzand: {student['FISH']}")
        st.write(f"Sinf: {student['Sinf']}")
        if st.button("Chiqish", use_container_width=True):
            st.session_state.pop("account", None)
            st.rerun()

    st.title(f"Assalomu alaykum, {account['parent_name']}")
    st.subheader(f"{student['FISH']} bo'yicha qisqa holat")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Umumiy o'rtacha", f"{student['Umumiy_baho']:.1f}")
    col2.metric("Davomat", f"{student['Davomat']}%")
    col3.metric("Vazifa bajarilishi", f"{student['Vazifa_bajarilishi']}%")
    col4.metric("Xavf holati", get_risk_level(student))

    left, right = st.columns([1.3, 1])

    with left:
        st.markdown("### Fanlar kesimida natijalar")
        scores = pd.DataFrame(
            {
                "Fan": ["Matematika", "O'qish", "Yozuv"],
                "Ball": [student["Matematika"], student["O'qish"], student["Yozuv"]],
            }
        ).set_index("Fan")
        st.bar_chart(scores)

        st.markdown("### Haftalik o'qish vaqti")
        chart_data = student_weekly.set_index("Sana")[["O'qish_soati"]]
        st.line_chart(chart_data)

    with right:
        st.markdown("### Tezkor signal")
        risk_messages = []
        if student["Davomat"] < 90:
            risk_messages.append("Davomat pasaygan, maktab bilan aloqani kuchaytirish kerak.")
        if student["Vazifa_bajarilishi"] < 80:
            risk_messages.append("Uy vazifalarini bajarish muntazam emas.")
        if student["Diqqat_darajasi"] <= 3:
            risk_messages.append("Darsdagi diqqat darajasi pastlashgan.")
        if not risk_messages:
            risk_messages.append("Jiddiy xavf ko'rinmadi, natijalar barqaror.")

        for item in risk_messages:
            st.info(item)

        st.markdown("### Tavsiyalar")
        for recommendation in get_recommendations(student):
            st.write(f"- {recommendation}")

    st.markdown("### O'qituvchi izohlari")
    if student_notes.empty:
        st.write("Hozircha izoh yo'q.")
    else:
        for _, row in student_notes.iterrows():
            st.write(f"• {row['Izoh']} — {row['Muallif']}")

    st.markdown("### Topshiriqlar")
    if student_tasks.empty:
        st.write("Faol topshiriq yo'q.")
    else:
        st.dataframe(student_tasks.drop(columns=["student_id"]), use_container_width=True, hide_index=True)

    st.markdown("### Batafsil ma'lumot")
    detail_cols = st.columns(3)
    parent_education = student["Ota-ona_ta'limi"]
    detail_cols[0].write(f"Ota-onaning ta'lim darajasi: {parent_education}")
    detail_cols[1].write(f"Tayyorlov kursi: {student['Tayyorlov']}")
    detail_cols[2].write(f"Qoldirilgan kunlar: {student['Qoldirilgan_kunlar']}")


def main():
    if "account" not in st.session_state:
        login_page()
    else:
        dashboard()


if __name__ == "__main__":
    main()

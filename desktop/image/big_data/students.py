import pandas as pd
import numpy as np
import random

# ============================================
# 1. MUMKIN BO'LGAN QIYMATLAR
# ============================================

genders = ['male', 'female']
race_groups = ['group A', 'group B', 'group C', 'group D', 'group E']
education_levels = [
    "some high school",
    "high school",
    "some college",
    "associate's degree",
    "bachelor's degree",
    "master's degree"
]
lunch_types = ['free/reduced', 'standard']
prep_courses = ['none', 'completed']

# ============================================
# 2. REALISTIC BAHOLAR YARATISH FUNKSIYASI
# ============================================

def generate_realistic_score(gender, race, education, lunch, prep_course):
    """Realistik baho yaratish (0-100 oralig'ida)"""
    
    # Bazaviy ball (50)
    base_score = 50
    
    # Jins ta'siri (minimal farq)
    if gender == 'female':
        base_score += 2  # Qizlar biroz yuqori
    
    # Ijtimoiy guruh ta'siri
    race_effect = {
        'group A': 5,
        'group B': 3,
        'group C': 0,
        'group D': -2,
        'group E': -4
    }
    base_score += race_effect.get(race, 0)
    
    # Ota-ona ta'limi ta'siri
    education_effect = {
        "some high school": -8,
        "high school": -4,
        "some college": 0,
        "associate's degree": 4,
        "bachelor's degree": 8,
        "master's degree": 12
    }
    base_score += education_effect.get(education, 0)
    
    # Ovqatlanish turi ta'siri
    if lunch == 'standard':
        base_score += 5
    else:
        base_score -= 3
    
    # Test tayyorlov kursi ta'siri
    if prep_course == 'completed':
        base_score += 10
    
    # Tasodifiy tebranish (-8 dan +8 gacha)
    random_variation = random.randint(-8, 8)
    
    # Yakuniy ball (0-100 oralig'ida cheklash)
    final_score = max(0, min(100, base_score + random_variation))
    
    return int(final_score)

# ============================================
# 3. 1000 TALABA MA'LUMOTLARINI YARATISH
# ============================================

np.random.seed(42)  # Natijalarni takrorlanadigan qilish uchun
random.seed(42)

data = []

for i in range(1000):
    # Tasodifiy tanlash
    gender = random.choice(genders)
    race = random.choice(race_groups)
    education = random.choice(education_levels)
    lunch = random.choice(lunch_types)
    prep = random.choice(prep_courses)
    
    # Har bir fan uchun ball yaratish (ular bir-biriga bog'liq)
    math_base = generate_realistic_score(gender, race, education, lunch, prep)
    reading_base = generate_realistic_score(gender, race, education, lunch, prep)
    writing_base = generate_realistic_score(gender, race, education, lunch, prep)
    
    # Fanlar orasidagi korrelyatsiyani yaratish
    # Matematika va o'qish o'rtasida bog'liqlik
    reading_base = int(reading_base * 0.8 + math_base * 0.2)
    writing_base = int(writing_base * 0.7 + math_base * 0.3 + reading_base * 0.1)
    
    # Chegaralarni tekshirish
    reading_score = max(0, min(100, reading_base))
    writing_score = max(0, min(100, writing_base))
    
    data.append({
        'gender': gender,
        'race/ethnicity': race,
        'parental level of education': education,
        'lunch': lunch,
        'test preparation course': prep,
        'math score': math_base,
        'reading score': reading_score,
        'writing score': writing_score
    })

# ============================================
# 4. DATAFRAME YARATISH
# ============================================

df = pd.DataFrame(data)

# ============================================
# 5. STATISTIK TEKSHIRISH
# ============================================

print("=" * 60)
print("MA'LUMOTLAR STATISTIKASI")
print("=" * 60)

print("\n📊 Umumiy statistika:")
print(df.describe())

print("\n📊 Har bir ustundagi qiymatlar taqsimoti:")
for col in df.columns:
    if df[col].dtype == 'object':
        print(f"\n{col}:")
        print(df[col].value_counts())

print("\n📊 Korrelyatsiya matritsasi:")
print(df[['math score', 'reading score', 'writing score']].corr())

# ============================================
# 6. CSV FAYLGA SAQLASH
# ============================================

df.to_csv('StudentsPerformance.csv', index=False)
print("\n✅ students.csv fayli yaratildi!")
print(f"📁 Jami qatorlar: {len(df)}")
print(f"📁 Jami ustunlar: {len(df.columns)}")
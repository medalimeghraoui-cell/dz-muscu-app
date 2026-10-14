import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="DZ Muscu App",
    page_icon="💪",
    layout="centered"
)

# App Title
st.title("💪 تطبيق بناء العضلات والتغذية الاقتصادية الجزائري")
st.caption("مخصص لميزانية 20,000 دج شهرياً ولتطوير الهرمونات البنائية")

# Sidebar navigation
page = st.sidebar.selectbox("اختر الشاشة", ["🏋️‍♂️ جدول التمارين", "🥗 برنامج التغذية", "📊 القياسات ونسبة الدهون"])

# 1. WORKOUT HUB
if page == "🏋️‍♂️ جدول التمارين":
    st.header("🏋️‍♂️ برنامج التدريب (3 أيام - Full Body)")
    st.info("💡 نصيحة التدرج التدريجي: إذا تمكنت من إنهاء كامل التكرارات في الطقم الأخير بنجاح، أضف +2.5 كغ في الحصة القادمة!")
    
    day = st.selectbox("اختر اليوم التدريبي", ["اليوم الأول (دفع وصدر)", "اليوم الثاني (سحب وظهر)", "اليوم الثالث (شامل ومكثف)"])
    
    if day == "اليوم الأول (دفع وصدر)":
        st.subheader("📋 حصة الأحد / السبت")
        st.markdown("- **السكوات بالبار (Barbell Squat):** 3 مجموعات × 8-10 تكرارات")
        st.markdown("- **ضغط صدر مستوي بالبار (Bench Press):** 4 مجموعات × 8-12 تكرار")
        st.markdown("- **ضغط أكتاف بالدمبلز جالس:** 3 مجموعات × 10 تكرارات")
        st.markdown("- **سحب ظهر عمودي (Lat Pulldown):** 3 مجموعات × 10-12 تكرار")
        st.markdown("- **ترايسبس خلفي بالكابل:** 3 مجموعات × 12 تكرار")
        
    elif day == "اليوم الثاني (سحب وظهر)":
        st.subheader("📋 حصة الثلاثاء / الإثنين")
        st.markdown("- **الرفعة الميتة (Deadlift):** 3 مجموعات × 8 تكرارات")
        st.markdown("- **تجديف بالبار للظهر (Barbell Row):** 4 مجموعات × 8-10 تكرارات")
        st.markdown("- **تجميع صدر مائل بالدمبلز:** 3 مجموعات × 10-12 تكرار")
        st.markdown("- **رفرفة أكتاف جانبي:** 4 مجموعات × 12-15 تكرار")
        st.markdown("- **تبادل بايسبس بالدمبلز:** 3 مجموعات × 12 تكرار")
        
    elif day == "اليوم الثالث (شامل ومكثف)":
        st.subheader("📋 حصة الخميس / الأربعاء")
        st.markdown("- **ضغط أرجل على الجهاز (Leg Press):** 4 مجموعات × 10-12 تكرار")
        st.markdown("- **غطس المتوازي (Dips):** 3 مجموعات × 10 تكرارات")
        st.markdown("- **سحب أرضي للظهر (Seated Cable Row):** 3 مجموعات × 10 تكرارات")
        st.markdown("- **ضغط أكتاف بالبار واقف:** 3 مجموعات × 8 تكرارات")
        st.markdown("- **تمرين بطن + بلانك:** 3 مجموعات حتى التعب")

# 2. DIET LEDGER
elif page == "🥗 برنامج التغذية":
    st.header("🥗 جدول الوجبات الاقتصادية (20,000 دج/شهر)")
    
    st.subheader("🍳 الوجبة 1: الفطور")
    st.markdown("**المكونات:** 3 بيضات كاملة مسلوقة + 60 غرام شوفان مطبوخ بالماء ونصف موزة.")
    st.caption("🎯 الهدف: تحفيز التستوستيرون صباحاً عبر الكوليسترول الصحي بصفار البيض.")
    
    st.subheader("🍛 الوجبة 2: الغداء")
    st.markdown("**المكونات:** 150 غرام أرز أو معكرونة + 150 غرام كبدة دجاج مطبوخة بالثوم والبصل + سلطة خضراء.")
    st.caption("🎯 الهدف: خفض الكورتيزول بفضل الأليسين في الثوم والبصل وتوفير زنك وحديد مكثف.")
    
    st.subheader("🌌 الوجبة 3: المسائية المدمجة (بعد التمرين وقبل النوم)")
    st.markdown("**المكونات:** 1 علبة تونة بالماء (أو 3 بيضات مسلوقة) + 2 علب جبن طبيعي (ريجيم) + 150 غرام بطاطا مسلوقة + حفنة كاوكاو محمص بدون ملح.")
    st.warning("⚠️ حظر برمي: تم استبعاد السكريات السريعة تماماً لحماية هرمون النمو (GH) ليلاً من الكبح!")

# 3. METRICS TRACKER
elif page == "📊 القياسات ونسبة الدهون":
    st.header("📊 تتبع القياسات الحيوية ونسبة الدهون")
    st.subheader("معادلة البحرية الأمريكية (US Navy Formula)")
    
    gender = st.radio("الجنس", ["ذكر", "أنثى"])
    height = st.number_input("الطول (سم)", min_value=120.0, max_value=220.0, value=175.0, step=0.5)
    weight = st.number_input("الوزن الحالي (كغ)", min_value=40.0, max_value=200.0, value=75.0, step=0.1)
    neck = st.number_input("محيط الرقبة (سم)", min_value=20.0, max_value=60.0, value=38.0, step=0.1)
    waist = st.number_input("محيط الخصر عند السرة (سم)", min_value=40.0, max_value=150.0, value=85.0, step=0.1)
    
    if gender == "أنثى":
        hip = st.number_input("محيط الورك (سم) - للإناث فقط", min_value=40.0, max_value=150.0, value=90.0, step=0.1)
        
    if st.button("احسب النتائج البيولوجية"):
        # BMI Calculation
        bmi = weight / ((height / 100) ** 2)
        st.metric("مؤشر كتلة الجسم (BMI)", f"{bmi:.1f}")
        
        # Body Fat Calculation based on US Navy Formula
        try:
            if gender == "ذكر":
                bf = 86.010 * np.log10(waist - neck) - 70.041 * np.log10(height) + 36.76
            else:
                bf = 163.205 * np.log10(waist + hip - neck) - 97.684 * np.log10(height) - 78.387
                
            if np.isnan(bf) or np.isinf(bf) or bf <= 0:
                st.error("الرجاء التحقق من القياسات المدخلة.")
            else:
                st.metric("نسبة الدهون التقريبية في الجسم", f"{bf:.1f} %")
                
                # Lean Body Mass
                fat_mass = weight * (bf / 100)
                lbm = weight - fat_mass
                st.metric("الكتلة العضلية الصافية (LBM)", f"{lbm:.1f} كغ")
        except:
            st.error("حدث خطأ في الحساب الرياضي، تأكد من منطقية الفروق بين القياسات.")

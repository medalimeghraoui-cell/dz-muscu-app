import streamlit as st
import pandas as pd
import datetime
import math

# إعدادات الصفحة الأساسية المتوافقة مع الهاتف
st.set_page_config(page_title="DZ Muscu App v2.5", page_icon="🏋️‍♂️", layout="centered")

# عنوان التطبيق الرئيسي
st.title("🏋️‍♂️ تطبيق بناء العضلات والقياسات الحيوية")
st.write("برنامج 3 أيام مخصص بميزانية اقتصادية مع تتبع الأداء والوزن")

# تهيئة مخزن البيانات في الجلسة إذا لم يكن موجوداً
if "workout_logs" not in st.session_state:
    st.session_state.workout_logs = pd.DataFrame(columns=["التاريخ", "اليوم", "التمرين", "الوزن (كغ)", "العدّات"])

# إنشاء التبويبات (Tabs)
tab1, tab2, tab3, tab4 = st.tabs(["💪 جدول التمارين والتتبع", "🥗 البرنامج الغذائي الكامل", "📏 القياسات ونسبة الدهون", "📈 سجل التطور التاريخي"])

# ==================== التبويب الأول: جدول التمارين والتتبع ====================
with tab1:
    st.header("🏋️‍♂️ سجل تمرينك اليوم وتحدى نفسك")
    
    selected_day = st.selectbox("اختر الحصة التدريبية اليوم:", ["اليوم الأول (دفع وصدر)", "اليوم الثاني (سحب وظهر)", "اليوم الثالث (شامل مكثف)"])
    
    # تعريف التمارين الكاملة (15 تمرين) مع روابط صور تخطيطية منسجمة
    exercises_data = {
        "اليوم الأول (دفع وصدر)": [
            {"name": "السكوات بالبار (Barbell Squat)", "img": "https://fitnessprogramer.com/wp-content/uploads/2021/02/BARBELL-SQUAT.gif", "desc": "3 مجموعات × 8-10 تكرارات (أرجل)"},
            {"name": "ضغط صدر مستوي بالبار (Bench Press)", "img": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Bench-Press.gif", "desc": "4 مجموعات × 8-12 تكرار (صدر)"},
            {"name": "ضغط أكتاف بالدمبلز جالس (Dumbbell Shoulder Press)", "img": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Seated-Dumbbell-Press.gif", "desc": "3 مجموعات × 10 تكرارات (كتف أمامي)"},
            {"name": "سحب ظهر عمودي (Lat Pulldown)", "img": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Lat-Pulldown.gif", "desc": "3 مجموعات × 10-12 تكرار (عضلات الظهر العريضة)"},
            {"name": "ترايسبس خلفي بالكابل (Triceps Pushdown)", "img": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Pushdown.gif", "desc": "3 مجموعات × 12 تكرار (ذراع خلفي)"}
        ],
        "اليوم الثاني (سحب وظهر)": [
            {"name": "الرفعة الميتة (Deadlift)", "img": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Deadlift.gif", "desc": "3 مجموعات × 8 تكرارات (أرجل خلفية وأسفل الظهر)"},
            {"name": "تجديف بالبار للظهر (Barbell Row)", "img": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Row.gif", "desc": "4 مجموعات × 8-10 تكرارات (سمك الظهر)"},
            {"name": "تجميع صدر مائل بالدمبلز (Incline Dumbbell Fly)", "img": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Incline-Dumbbell-Fly.gif", "desc": "3 مجموعات × 10-12 تكرار (الصدر العلوي)"},
            {"name": "رفرفة أكتاف جانبي بالدمبلز (Lateral Raise)", "img": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Lateral-Raise.gif", "desc": "4 مجموعات × 12-15 تكرار (عرض الأكتاف)"},
            {"name": "تبادل بايسبس بالدمبلز (Dumbbell Biceps Curl)", "img": "https://fitnessprogramer.com/wp-content/uploads/2021/03/Dumbbell-Curl.gif", "desc": "3 مجموعات × 12 تكرار (ذراع أمامي)"}
        ],
        "اليوم الثالث (شامل مكثف)": [
            {"name": "ضغط أرجل على الجهاز (Leg Press)", "img": "https://fitnessprogramer.com/wp-content/uploads/2015/11/Leg-Press.gif", "desc": "4 مجموعات × 10-12 تكرار (أرجل)"},
            {"name": "غطس المتوازي (Dips)", "img": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dips.gif", "desc": "3 مجموعات × 10 تكرارات (أسفل الصدر والترايسبس)"},
            {"name": "سحب أرضي للظهر (Seated Cable Row)", "img": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Seated-Cable-Row.gif", "desc": "3 مجموعات × 10 تكرارات (منتصف الظهر)"},
            {"name": "ضغط أكتاف بالبار واقف (Military Press)", "img": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Military-Press.gif", "desc": "3 مجموعات × 8 تكرارات (أكتاف وقوة عامة)"},
            {"name": "تمرين بطن (Crunches)", "img": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Crunch.gif", "desc": "3 مجموعات حتى التعب"}
        ]
    }
    
    st.info("💡 نصيحة الزيادة التدريجية: إذا أكملت عَدّاتك الحالية بسهولة، أضف 2.5 كغ في الحصة القادمة!")
    
    current_logs = []
    
    for ex in exercises_data[selected_day]:
        st.subheader(ex["name"])
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(ex["img"], caption=ex["desc"], use_container_width=True)
            
        with col2:
            weight = st.number_input(f"الوزن (كغ) - {ex['name']}", min_value=0.0, max_value=300.0, step=2.5, key=f"w_{ex['name']}")
            reps = st.number_input(f"عدد العدّات الحقيقية - {ex['name']}", min_value=0, max_value=50, step=1, key=f"r_{ex['name']}")
            current_logs.append({"التمرين": ex["name"], "الوزن (كغ)": weight, "العدّات": reps})
        st.markdown("---")
        
    if st.button("💾 حفظ حصة اليوم وتخزين البيانات", type="primary"):
        new_records = []
        today_date = datetime.date.today().strftime("%Y-%m-%d")
        for log in current_logs:
            if log["العدّات"] > 0:
                new_records.append({
                    "التاريخ": today_date,
                    "اليوم": selected_day,
                    "التمرين": log["التمرين"],
                    "الوزن (كغ)": log["الوزن (كغ)"],
                    "العدّات": log["العدّات"]
                })
        if new_records:
            st.session_state.workout_logs = pd.concat([st.session_state.workout_logs, pd.DataFrame(new_records)], ignore_index=True)
            st.success("✅ تم حفظ البيانات بنجاح! انتقل لتبويب سجل التطور لمشاهدة النتائج.")
        else:
            st.warning("⚠️ يرجى إدخال عدد اللفات (العدّات) على الأقل لتسجيل التمرين.")

# ==================== التبويب الثاني: البرنامج الغذائي الكامل ====================
with tab2:
    st.header("🥗 البرنامج الغذائي الاقتصادي الكامل المحفز للهرمونات")
    st.write("**الميزانية المستهدفة:** 20,000 دج شهرياً (حوالي 660 دج يومياً) لتوفير 140 غرام بروتين")
    
    st.markdown("### 🍳 الوجبة الأولى: الفطور (وجبة شحن التستوستيرون الصباحية)")
    st.markdown("""
    * **3 بيضات كاملة** مسلوقة أو مقلية بمسحة زيت زيتون (كوليسترول صحي لإنتاج هرمون التذكورة).
    * **60 غرام شوفان** مطبوخ بالماء أو حليب قليل الدسم.
    * **نصف موزة** أو 3 حبات تمر للطاقة.
    """)
    
    st.markdown("### 🍗 الوجبة الثانية: الغداء (وجبة بناء العضلات والتركيز)")
    st.markdown("""
    * **150 غرام كبدة دجاج** (أو صدور دجاج) مطبوخة مع البصل والثوم (الثوم يخفض الكورتيزول الهادم).
    * **150 غرام أرز أبيض أو معكرونة** مسلوقة كمصدر أساسي ومستدام للطاقة.
    * **طبق سلطة خضراء** خفيف (طماطم، خيار أو خس).
    """)
    
    st.error("🌌 الوجبة الثالثة المدمجة: وجبة ما بعد التمرين وقبل النوم مباشرة")
    st.markdown("""
    * **1 علبة تونة بالماء** (مصفاة جيداً) أو **3 بيضات مسلوقة** (بياض فقط لتقليل الدهون ليلاً).
    * **2 علب جبن طبيعي (ناتير / جبن ريجيم)** (يوفر بروتين الكازين بطيء الامتصاص لتغذية العضلات طوال 8 ساعات نوم).
    * **150 إلى 200 غرام بطاطا مسلوقة** أو مشوية (كربوهيدرات معقدة تمنحك استرخاءً وتساعد على النوم العميق).
    * **حفنة صغيرة من الفول السوداني (كاوكاو محمص بدون ملح)** (مصدر دهون صحية ومغنيسيوم لتنظيم جودة النوم وتحفيز هرمون النمو GH).
    """)
    
    st.warning("🚫 تحذير مبرمج هرمونياً: لا تقم بإدخال أي سكريات بسيطة (حلويات، عصائر مصنعة) في هذه الوجبة المسائية لتفادي كبح هرمون النمو ليلاً.")

# ==================== التبويب الثالث: القياسات ونسبة الدهون ====================
with tab3:
    st.header("📏 حاسبة نسبة الدهون والكتلة العضلية (US Navy Formula)")
    
    gender = st.radio("الجنس:", ["ذكر", "أنثى"], horizontal=True)
    height_cm = st.number_input("الطول (سم):", min_value=120.0, max_value=230.0, value=175.0)
    weight_kg = st.number_input("الوزن الحالي (كغ):", min_value=30.0, max_value=200.0, value=75.0)
    neck_cm = st.number_input("محيط الرقبة (سم):", min_value=20.0, max_value=60.0, value=38.0)
    waist_cm = st.number_input("محيط الخصر عند السرة (سم):", min_value=40.0, max_value=150.0, value=85.0)
    
    if st.button("📊 احسب نسب الجسم الحالية"):
        bmi = weight_kg / ((height_cm / 100) ** 2)
        try:
            if gender == "ذكر":
                body_fat = 86.010 * math.log10(waist_cm - neck_cm) - 70.041 * math.log10(height_cm) + 36.76
            else:
                hip_cm = st.number_input("محيط الورك (سم) للإناث:", min_value=40.0, max_value=150.0, value=90.0)
                body_fat = 163.205 * math.log10(waist_cm + hip_cm - neck_cm) - 97.684 * math.log10(height_cm) - 78.387
            
            fat_mass = weight_kg * (body_fat / 100)
            lean_mass = weight_kg - fat_mass
            
            st.metric(label="📉 نسبة الدهون المقدرة:", value=f"{body_fat:.1f} %")
            st.metric(label="💪 الكتلة العضلية والصافية (LBM):", value=f"{lean_mass:.1f} كغ")
            st.metric(label="⚖️ مؤشر كتلة الجسم (BMI):", value=f"{bmi:.1f}")
        except ValueError:
            st.error("❌ يرجى التحقق من صحة القياسات المدخلة (محيط الخصر يجب أن يكون أكبر من محيط الرقبة).")

# ==================== التبويب الرابع: سجل التطور التاريخي ====================
with tab4:
    st.header("📈 جدول تتبع النتائج ومراقبة الأداء الأسبوعي")
    
    if not st.session_state.workout_logs.empty:
        st.dataframe(st.session_state.workout_logs, use_container_width=True)
        if st.button("🗑️ مسح السجل وإعادة تعيين التتبع"):
            st.session_state.workout_logs = pd.DataFrame(columns=["التاريخ", "اليوم", "التمرين", "الوزن (كغ)", "العدّات"])
            st.rerun()
    else:
        st.info("📭 السجل فارغ حالياً. قم بتسجيل تمارينك من التبويب الأول لتظهر لك الرسوم البيانية والجداول هنا.")

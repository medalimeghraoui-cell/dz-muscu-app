import streamlit as st
import pandas as pd
import datetime
import math

# إعدادات شاشة التطبيق المتوافقة مع الهواتف الذكية
st.set_page_config(page_title="DZ Muscu App v2.0", page_icon="🏋️‍♂️", layout="centered")

# تعديل الواجهة البرمجية لتصبح باللون الداكن العصري (Premium Dark Mode) عبر CSS
st.markdown("""
<style>
    .stApp {
        background-color: #121212;
        color: #FFFFFF;
    }
    div.stTabs [data-baseweb="tab-list"] {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 5px;
    }
    div.stTabs [data-baseweb="tab"] {
        color: #BBBBBB;
        font-weight: bold;
    }
    div.stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #4CAF50;
    }
    .card {
        background-color: #1E1E1E;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #2D2D2D;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    h3 {
        color: #4CAF50 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏋️‍♂️ تطبيق DZ Muscu App v2.0")
st.write("برنامج 3 أيام بميزانية اقتصادية 20,000 دج مع تتبع كامل للأوزان والوجبات والنسب الحيوية")

# تهيئة مخزن البيانات في الجلسة لتتبع أداء الحصص
if "workout_logs" not in st.session_state:
    st.session_state.workout_logs = pd.DataFrame(columns=["التاريخ", "الحصة", "التمرين", "الوزن (كغ)", "العدّات"])

# إنشاء التبويبات الأربعة للتطبيق
tab1, tab2, tab3, tab4 = st.tabs(["💪 التمارين والتتبع", "🥗 التغذية الكاملة", "📏 نسب الجسم والدهون", "📈 سجل التطور"])

# ==================== التبويب الأول: التمارين والتتبع ====================
with tab1:
    st.header("🏋️‍♂️ سجل أدائك التدريبي اليوم")
    seance = st.selectbox("اختر الحصة الحالية:", ["اليوم الأول (دفع وصدر)", "اليوم الثاني (سحب وظهر)", "اليوم الثالث (شامل مكثف)"])
    
    # قائمة الـ 15 تمريناً كاملة ومنسجمة بدون أي نقص
    exercises = {
        "اليوم الأول (دفع وصدر)": [
            {"name": "السكوات بالبار (Barbell Squat)", "desc": "3 مجموعات × 8-10 تكرارات (أرجل)"},
            {"name": "ضغط صدر مستوي بالبار (Bench Press)", "desc": "4 مجموعات × 8-12 تكرار (صدر)"},
            {"name": "ضغط أكتاف بالدمبلز جالس (Shoulder Press)", "desc": "3 مجموعات × 10 تكرارات (كتف أمامي)"},
            {"name": "سحب ظهر عمودي (Lat Pulldown)", "desc": "3 مجموعات × 10-12 تكرار (ظهر عريض)"},
            {"name": "تمرين ترايسبس خلفي بالكابل (Pushdown)", "desc": "3 مجموعات × 12 تكرار (ذراع خلفي)"}
        ],
        "اليوم الثاني (سحب وظهر)": [
            {"name": "الرفعة الميتة (Deadlift)", "desc": "3 مجموعات × 8 تكرارات (أرجل خلفية وأسفل الظهر)"},
            {"name": "تجديف بالبار للظهر (Barbell Row)", "desc": "4 مجموعات × 8-10 تكرارات (سمك الظهر)"},
            {"name": "تجميع صدر مائل بالدمبلز (Incline Fly)", "desc": "3 مجموعات × 10-12 تكرار (صدر علوي)"},
            {"name": "رفرفة أكتاف جانبي بالدمبلز (Lateral Raise)", "desc": "4 مجموعات × 12-15 تكرار (عرض الأكتاف)"},
            {"name": "تبادل بايسبس بالدمبلز (Biceps Curl)", "desc": "3 مجموعات × 12 تكرار (ذراع أمامي)"}
        ],
        "اليوم الثالث (شامل مكثف)": [
            {"name": "ضغط أرجل على الجهاز (Leg Press)", "desc": "4 مجموعات × 10-12 تكرار (أرجل)"},
            {"name": "غطس المتوازي (Dips)", "desc": "3 مجموعات × 10 تكرارات (أسفل الصدر والترايسبس)"},
            {"name": "سحب أرضي للظهر (Seated Cable Row)", "desc": "3 مجموعات × 10 تكرارات (منتصف الظهر)"},
            {"name": "ضغط أكتاف بالبار واقف (Military Press)", "desc": "3 مجموعات × 8 تكرارات (أكتاف وقوة عامة)"},
            {"name": "تمرين بطن (Crunches) + بلانك", "desc": "3 مجموعات حتى التعب"}
        ]
    }
    
    current_inputs = []
    st.info("💡 لتطبيق الزيادة التدريجية: عند إكمال التكرارات المستهدفة بسهولة، أضف 2.5 كغ في الحصة القادمة.")
    
    for ex in exercises[seance]:
        st.markdown(f"<div class='card'><h4>{ex['name']}</h4><p style='color: #AAA; margin:0;'>{ex['desc']}</p></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            w = st.number_input(f"الوزن (كغ) - {ex['name']}", min_value=0.0, max_value=300.0, step=2.5, key=f"w_{ex['name']}")
        with col2:
            r = st.number_input(f"عدد العدّات - {ex['name']}", min_value=0, max_value=50, step=1, key=f"r_{ex['name']}")
        current_inputs.append({"التمرين": ex["name"], "الوزن (كغ)": w, "العدّات": r})
        st.markdown("---")
        
    if st.button("💾 حفظ حصة اليوم وتخزين البيانات", type="primary"):
        records = []
        today = datetime.date.today().strftime("%Y-%m-%d")
        for log in current_inputs:
            if log["العدّات"] > 0:
                records.append({
                    "التاريخ": today,
                    "الحصة": seance,
                    "التمرين": log["التمرين"],
                    "الوزن (كغ)": log["الوزن (كغ)"],
                    "العدّات": log["العدّات"]
                })
        if records:
            st.session_state.workout_logs = pd.concat([st.session_state.workout_logs, pd.DataFrame(records)], ignore_index=True)
            st.success("✅ تم حفظ الحصة بنجاح في سجل التطور الخاص بك!")
        else:
            st.warning("⚠️ يرجى إدخال عدد العدّات لتسجيل التمرين بنجاح.")

# ==================== التبويب الثاني: التغذية الكاملة ====================
with tab2:
    st.header("🥗 البرنامج الغذائي الاقتصادي الشامل (20,000 دج/شهر)")
    
    st.markdown("""
    <div class='card'>
        <h3>🍳 الوجبة 1: الفطور</h3>
        <p>• 3 بيضات كاملة مسلوقة أو مقلية بمسحة زيت زيتون.</p>
        <p>• 60-80 غرام شوفان مطبوخ بالماء مع نصف موزة.</p>
        <p style='color: #4CAF50;'>💡 الهدف الهرموني: الكوليسترول الصحي في صفار البيض يحفز تصنيع هرمون التستوستيرون صباحاً.</p>
    </div>
    <div class='card'>
        <h3>🍗 الوجبة 2: الغداء</h3>
        <p>• 150-200 غرام كبدة دجاج مطبوخة بالثوم والبصل العطري.</p>
        <p>• 150 غرام أرز مسلوق أو معكرونة + طبق سلطة خضراء خفيف.</p>
        <p style='color: #4CAF50;'>💡 الهدف الهرموني: كبدة الدجاج توفر الزنك والحديد، بينما يعمل الثوم والبصل على خفض الكورتيزول.</p>
    </div>
    <div class='card'>
        <h3>🌌 الوجبة 3: الوجبة الليلية الضخمة المدمجة (بعد التمرين وقبل النوم مباشرة)</h3>
        <p>• 1 علبة تونة بالماء (مصفاة جيدا) أو 3 بيضات مسلوقة (بياض فقط).</p>
        <p>• 2 علب جبن طبيعي ناتير (Natur'a / جبن ريجيم لتدفق أحماض الكازين ببطء طوال 8 ساعات نوم).</p>
        <p>• 150-200 غرام بطاطا مسلوقة أو مشوية لإعادة شحن مخازن الجليكوجين وضمان النوم العميق.</p>
        <p>• حفنة صغيرة من الفول السوداني (كاوكاو محمص بدون ملح) لتوفير المغنيسيوم والدهون الصحية.</p>
        <p style='color: #FF9800;'>⚠️ تنبيه هرموني: الوجبة خالية تماماً من السكريات البسيطة لضمان ذروة إفراز هرمون النمو (GH) ليلاً.</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== التبويب الثالث: نسب الجسم والدهون ====================
with tab3:
    st.header("📏 حاسبة نسبة الدهون والكتلة الصافية (US Navy Formula)")
    height = st.number_input("الطول (سم):", min_value=120.0, max_value=230.0, value=175.0)
    weight = st.number_input("الوزن الإجمالي (كغ):", min_value=30.0, max_value=200.0, value=75.0)
    neck = st.number_input("محيط الرقبة (سم):", min_value=20.0, max_value=60.0, value=38.0)
    waist = st.number_input("محيط الخصر عند السرة (سم):", min_value=40.0, max_value=150.0, value=85.0)
    
    if st.button("📊 احسب مكونات الجسم الحالية"):
        bmi = weight / ((height / 100) ** 2)
        if waist > neck:
            bf = 86.010 * math.log10(waist - neck) - 70.041 * math.log10(height) + 36.76
            fat_m = weight * (bf / 100)
            lean_m = weight - fat_m
            st.success(f"📉 نسبة الدهون المقدرة للجسم: {bf:.1f} %")
            st.success(f"💪 الكتلة العضلية الصافية المحسوبة: {lean_m:.1f} كغ")
            st.success(f"⚖️ مؤشر كتلة الجسم العام (BMI): {bmi:.1f}")
        else:
            st.error("❌ خطأ قياسي: يجب أن يكون محيط الخصر أكبر من محيط الرقبة لحساب المعادلة.")

# ==================== التبويب الرابع: سجل التطور ====================
with tab4:
    st.header("📈 جدول مراقبة الأداء والتطور التاريخي")
    if not st.session_state.workout_logs.empty:
        st.dataframe(st.session_state.workout_logs, use_container_width=True)
        if st.button("🗑️ مسح السجل وإعادة التصفير"):
            st.session_state.workout_logs = pd.DataFrame(columns=["التاريخ", "الحصة", "التمرين", "الوزن (كغ)", "العدّات"])
            st.rerun()
    else:
        st.info("المذكرة فارغة حالياً. بمجرد تسجيل وتخزين أول تمرين من التبويب الأول، ستظهر النتائج والتوثيقات هنا.")

import streamlit as st
import pandas as pd
import datetime

# إعدادات الصفحة الأساسية المتوافقة مع الهاتف
st.set_page_config(page_title="DZ Muscu App v2.0", page_icon="🏋️‍♂️", layout="centered")

# عنوان التطبيق الرئيسي
st.title("🏋️‍♂️ تطبيق بناء العضلات والقياسات الحيوية")
st.write("برنامج 3 أيام مخصص بميزانية اقتصادية مع تتبع الأداء والوزن")

# تهيئة مخزن البيانات في الجلسة إذا لم يكن موجوداً
if "workout_logs" not in st.session_state:
    st.session_state.workout_logs = pd.DataFrame(columns=["التاريخ", "اليوم", "التمرين", "الوزن (كغ)", "العدّات"])

# إنشاء التبويبات (Tabs)
tab1, tab2, tab3, tab4 = st.tabs(["💪 جدول التمارين والتتبع", "🥗 التغذية الهرمونية", "📏 القياسات ونسبة الدهون", "📈 سجل التطور التاريخي"])

# ==================== التبويب الأول: جدول التمارين والتتبع ====================
with tab1:
    st.header("🏋️‍♂️ سجل تمرينك اليوم وتحدى نفسك")
    
    selected_day = st.selectbox("اختر الحصة التدريبية اليوم:", ["اليوم الأول (دفع وصدر)", "اليوم الثاني (سحب وظهر)", "اليوم الثالث (شامل مكثف)"])
    
    # تعريف التمارين والصور المرتبطة بها
    exercises_data = {
        "اليوم الأول (دفع وصدر)": [
            {"name": "السكوات بالبار (Barbell Squat)", "img": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?w=500", "desc": "3 مجموعات × 8-10 تكرارات (أرجل)"},
            {"name": "ضغط صدر مستوي بالبار (Bench Press)", "img": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=500", "desc": "4 مجموعات × 8-12 تكرار (صدر)"},
            {"name": "ضغط أكتاف بالدمبلز جالس", "img": "https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?w=500", "desc": "3 مجموعات × 10 تكرارات (كتف أمامي)"}
        ],
        "اليوم الثاني (سحب وظهر)": [
            {"name": "الرفعة الميتة (Deadlift)", "img": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=500", "desc": "3 مجموعات × 8 تكرارات (أرجل خلفية وأسفل الظهر)"},
            {"name": "تجديف بالبار للظهر (Barbell Row)", "img": "https://images.unsplash.com/photo-1605296867304-46d5465a25f1?w=500", "desc": "4 مجموعات × 8-10 تكرارات (سمك الظهر)"},
            {"name": "رفرفة أكتاف جانبي بالدمبلز", "img": "https://images.unsplash.com/photo-1593079831268-3381b0db4a77?w=500", "desc": "4 مجموعات × 12-15 تكرار (عرض الأكتاف)"}
        ],
        "اليوم الثالث (شامل مكثف)": [
            {"name": "ضغط أرجل على الجهاز (Leg Press)", "img": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=500", "desc": "4 مجموعات × 10-12 تكرار (أرجل)"},
            {"name": "غطس المتوازي (Dips)", "img": "https://images.unsplash.com/photo-1598971639058-fab3c3109a00?w=500", "desc": "3 مجموعات × 10 تكرارات (أسفل الصدر والترايسبس)"},
            {"name": "سحب أرضي للظهر (Seated Cable Row)", "img": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=500", "desc": "3 مجموعات × 10 تكرارات (منتصف الظهر)"}
        ]
    }
    
    st.info("💡 نصيحة الزيادة التدريجية: إذا أكملت عَدّاتك الحالية بسهولة، أضف 2.5 كغ في الحصة القادمة!")
    
    current_logs = []
    
    # عرض التمارين وإتاحة حقول تسجيل الوزن والعدّات
    for ex in exercises_data[selected_day]:
        st.subheader(ex["name"])
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(ex["img"], caption=ex["desc"], use_container_width=True)
            
        with col2:
            weight = st.number_input(f"الوزن (كغ) - {ex['name']}", min_value=0.0, max_value=300.0, step=2.5, key=f"w_{ex['name']}")
            reps = st.number_input(f"عدد اللفات الحقيقية - {ex['name']}", min_value=0, max_value=50, step=1, key=f"r_{ex['name']}")
            current_logs.append({"التمرين": ex["name"], "الوزن (كغ)": weight, "العدّات": reps})
        st.markdown("---")
        
    if st.button("💾 حفظ حصة اليوم وتخزين البيانات", type="primary"):
        new_records = []
        today_date = datetime.date.today().strftime("%Y-%m-%d")
        for log in current_logs:
            if log["العدّات"] > 0:  # حفظ التمارين التي تم لعبها فقط
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

# ==================== التبويب الثاني: التغذية الهرمونية ====================
with tab2:
    st.header("🥗 نظام غذائي محفز للهرمونات ومدروس الميزانية")
    st.write("**الميزانية المستهدفة:** 20,000 دج شهرياً (حوالي 660 دج يومياً)")
    
    st.success("🌌 الوجبة الليلية الضخمة والمدمجة (بعد التمرين وقبل النوم مباشرة)")
    st.markdown("""
    * **علبة تونة بالماء** (مصفاة جيدا) أو **3 بيضات مسلوقة** (بياض فقط لتقليل الدهون ليلاً).
    * **2 علب جبن طبيعي ناتير** (بروتين كازين بطيء الامتصاص لمد العضلات طوال 8 ساعات نوم).
    * **150-200 غرام بطاطا مسلوقة** (كربوهيدرات نظيفة تمنحك استرخاءً وتساعد على النوم العميق).
    * **حفنة كاوكاو محمص بدون ملح** (دهون صحية ومغنيسيوم لتنظيم جودة النوم وتحفيز هرمون النمو GH).
    """)
    st.warning("🚫 تحذير مبرمج: لا تقم بإدخال أي سكريات بسيطة (حلويات، عصائر مصنعة) في هذه الوجبة لتفادي كبح هرمون النمو ليلاً.")

# ==================== التبويب الثالث: القياسات ونسبة الدهون ====================
with tab3:
    st.header("📏 حاسبة نسبة الدهون والكتلة العضلية (US Navy Formula)")
    
    gender = st.radio("الجنس:", ["ذكر", "أنثى"], horizontal=True)
    height_cm = st.number_input("الطول (سم):", min_value=120.0, max_value=230.0, value=175.0)
    weight_kg = st.number_input("الوزن الحالي (كغ):", min_value=30.0, max_value=200.0, value=75.0)
    neck_cm = st.number_input("محيط الرقبة (سم):", min_value=20.0, max_value=60.0, value=38.0)
    waist_cm = st.number_input("محيط الخصر عند السرة (سم):", min_value=40.0, max_value=150.0, value=85.0)
    
    if st.button("📊 احسب نسب الجسم الحالية"):
        import math
        # حساب مؤشر كتلة الجسم
        bmi = weight_kg / ((height_cm / 100) ** 2)
        
        # حساب نسبة الدهون بناءً على معادلة البحرية الأمريكية للذكور والإناث
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
        
        # خيار لحذف البيانات وإعادة التصفير
        if st.button("🗑️ مسح السجل وإعادة تعيين التتبع"):
            st.session_state.workout_logs = pd.DataFrame(columns=["التاريخ", "اليوم", "التمرين", "الوزن (كغ)", "العدّات"])
            st.rerun()
    else:
        st.info("📭 السجل فارغ حالياً. قم بتسجيل تمارينك من التبويب الأول لتظهر لك الرسوم البيانية والجداول هنا.")
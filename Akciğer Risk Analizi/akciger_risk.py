import streamlit as st
import pandas as pd

def calculate_pack_years(daily_cigarettes, smoking_years):
    """Paket-yıl hesaplaması"""
    if daily_cigarettes == 0:
        return 0
    packs_per_day = daily_cigarettes / 20
    return packs_per_day * smoking_years

def calculate_base_risk_score(daily_cigarettes, smoking_years):
    """Temel risk skoru hesaplama"""
    base_score = 0
    
   
    pack_years = calculate_pack_years(daily_cigarettes, smoking_years)
    
    if pack_years > 30:
        base_score += 30
    elif pack_years > 20:
        base_score += 20
    elif pack_years > 10:
        base_score += 15
    elif pack_years > 5:
        base_score += 10
    elif pack_years > 0:
        base_score += 5
    else:
        base_score = 0  
    
    return base_score

def calculate_environmental_risk(work_environment, genetic_history):
    """Çevresel risk hesaplama"""
    env_score = 0
    
   
    work_risk = {
        'Ofis': 0,
        'Tozlu Ortam': 10,
        'Kimyasal Ortam': 15,
        'Maden/Ocak': 20,
        'Diğer': 5
    }
    env_score += work_risk.get(work_environment, 0)
    
 
    genetic_risk = {
        'Yok': 0,
        '2. Derece Akraba': 10,
        '1. Derece Akraba': 15
    }
    env_score += genetic_risk.get(genetic_history, 0)
    
    return env_score

def calculate_protective_factors(exercise, diet, age):
    """Koruyucu faktörler"""
    protective_score = 0
    

    exercise_bonus = {
        'Hiç': 0,
        'Haftada 1-2 Gün': -5,
        'Haftada 3+ Gün': -10
    }
    protective_score += exercise_bonus.get(exercise, 0)
    
   
    diet_bonus = {
        'Kötü': 0,
        'Orta': -4,
        'İyi': -8
    }
    protective_score += diet_bonus.get(diet, 0)
    
 
    if age < 40:
        protective_score -= 5
    
    return protective_score

def categorize_risk(total_score):
    """Risk kategorizasyonu"""
    if total_score <= 20:
        return "DÜŞÜK RİSK", "🟢", "low"
    elif total_score <= 40:
        return "ORTA RİSK", "🟡", "medium"
    elif total_score <= 60:
        return "YÜKSEK RİSK", "🟠", "high"
    else:
        return "ÇOK YÜKSEK RİSK", "🔴", "very_high"

def generate_recommendations(risk_category, user_data):
    """Kişiselleştirilmiş öneriler"""
    recommendations = []
    
    if risk_category in ["YÜKSEK RİSK", "ÇOK YÜKSEK RİSK"]:
        recommendations.extend([
            "🚨 **ACİL:** Göğüs hastalıkları uzmanına başvurun",
            "📅 **Tarama:** Yıllık düşük doz akciğer tomografisi önerilir",
            "🚭 **Bırakma:** Sigarayı bırakma programına katılın"
        ])
    elif risk_category == "ORTA RİSK":
        recommendations.extend([
            "⚠️ **Takip:** Düzenli sağlık kontrolleri yaptırın",
            "📉 **Azaltma:** Sigara sayısını kademeli olarak azaltın",
            "🏃 **Spor:** Düzenli egzersiz programı başlatın"
        ])
    else:
        recommendations.extend([
            "✅ **Koruma:** Mevcut sağlıklı alışkanlıklarınızı sürdürün",
            "🔍 **Önlem:** Düzenli check-up yaptırın",
            "💪 **Spor:** Aktif yaşam tarzını devam ettirin"
        ])
    
 
    if user_data['daily_cigarettes'] > 10:
        recommendations.append("📉 **Hedef:** Sigara sayısını günde 10'un altına indirin")
    elif user_data['daily_cigarettes'] > 0:
        recommendations.append("🎯 **Hedef:** Tamamen bırakmak için plan yapın")
 
    if user_data['exercise'] == 'Hiç':
        recommendations.append("🏃 **Spor:** Haftada 3 gün 30 dakika yürüyüş yapın")
    elif user_data['exercise'] == 'Haftada 1-2 Gün':
        recommendations.append("💪 **Geliştirme:** Egzersizi haftada 3 güne çıkarın")
    
  
    if user_data['diet'] == 'Kötü':
        recommendations.append("🥗 **Beslenme:** Antioksidan bakımından zengin besinler tüketin")
    
    return recommendations

def calculate_bmi(weight, height):
    """BMI hesaplama"""
    if height > 0:
        return weight / ((height / 100) ** 2)
    return 0

def main():
    st.set_page_config(
        page_title="Akciğer Risk Analizi", 
        page_icon="🩺",
        layout="centered"
    )
    
  
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .risk-low { color: green; font-weight: bold; font-size: 1.5rem; }
    .risk-medium { color: orange; font-weight: bold; font-size: 1.5rem; }
    .risk-high { color: red; font-weight: bold; font-size: 1.5rem; }
    .risk-very-high { color: darkred; font-weight: bold; font-size: 1.5rem; }
    .recommendation-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid #1f77b4;
        color: #000000 !important;  /* SİYAH RENK EKLENDİ */
    }
    .recommendation-box p {
        color: #000000 !important;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-header">🩺 Akciğer Sağlığı Risk Analiz Aracı</div>', unsafe_allow_html=True)
    st.markdown("Kişisel risk faktörlerinize göre akciğer sağlığınızı değerlendirin")
    
    with st.form("risk_analysis"):
        st.subheader("📊 Kişisel Bilgiler")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Yaşınız", min_value=18, max_value=100, value=35)
            gender = st.selectbox("Cinsiyetiniz", ["Erkek", "Kadın", "Diğer"])
            
        with col2:
            height = st.number_input("Boyunuz (cm)", min_value=100, max_value=220, value=170)
            weight = st.number_input("Kilonuz (kg)", min_value=30, max_value=200, value=70)
        
    
        bmi = calculate_bmi(weight, height)
        if bmi > 0:
            st.write(f"**Vücut Kitle İndeksi:** {bmi:.1f}")
        
        st.subheader("🚬 Sigara Alışkanlıkları")
        
        col3, col4 = st.columns(2)
        
        with col3:
            daily_cigarettes = st.slider("Günlük sigara sayısı", 0, 80, 10)
            smoking_years = st.slider("Kaç yıldır sigara içiyorsunuz", 0, 60, 5)
        
        with col4:
            cigarette_type = st.selectbox(
                "Sigara türü", 
                ["Light", "Normal", "Puro", "Nargile", "Elektronik Sigara", "İçmiyorum"]
            )
            inhalation = st.selectbox(
                "İçe çekme derinliği",
                ["İçmiyorum", "Yüzeysel", "Orta", "Derin"]
            )
        
        st.subheader("🏭 Çevresel Faktörler")
        
        col5, col6 = st.columns(2)
        
        with col5:
            work_environment = st.selectbox(
                "İş ortamınız",
                ["Ofis", "Tozlu Ortam", "Kimyasal Ortam", "Maden/Ocak", "Diğer"]
            )
        
        with col6:
            genetic_history = st.selectbox(
                "Ailede akciğer kanseri öyküsü",
                ["Yok", "2. Derece Akraba", "1. Derece Akraba"]
            )
        
        st.subheader("💪 Yaşam Tarzı")
        
        col7, col8 = st.columns(2)
        
        with col7:
            exercise = st.selectbox(
                "Egzersiz sıklığı",
                ["Hiç", "Haftada 1-2 Gün", "Haftada 3+ Gün"]
            )
        
        with col8:
            diet = st.selectbox(
                "Beslenme kalitesi",
                ["Kötü", "Orta", "İyi"]
            )
        
        submitted = st.form_submit_button("🔍 Risk Analizi Yap")
        
        if submitted:
          
            user_data = {
                'daily_cigarettes': daily_cigarettes,
                'exercise': exercise,
                'diet': diet,
                'work_environment': work_environment,
                'genetic_history': genetic_history,
                'age': age
            }
            
           
            base_risk = calculate_base_risk_score(daily_cigarettes, smoking_years)
            env_risk = calculate_environmental_risk(work_environment, genetic_history)
            protective = calculate_protective_factors(exercise, diet, age)
            
            total_score = base_risk + env_risk + protective
            total_score = max(0, min(100, total_score)) 
            
            risk_category, risk_emoji, risk_class = categorize_risk(total_score)
            pack_years = calculate_pack_years(daily_cigarettes, smoking_years)
            
         
            st.success("✅ Analiz tamamlandı!")
            
          
            st.markdown(f"<div class='risk-{risk_class}'>{risk_emoji} {risk_category}</div>", unsafe_allow_html=True)
            
           
            st.progress(total_score / 100)
            st.write(f"**Risk Skoru:** {total_score}/100")
            
           
            st.subheader("📈 Detaylı Risk Analizi")
            
            col9, col10, col11 = st.columns(3)
            
            with col9:
                st.metric("Paket-Yıl", f"{pack_years:.1f}")
            
            with col10:
                st.metric("Temel Risk", f"{base_risk}p")
            
            with col11:
                st.metric("Koruyucu Faktörler", f"{protective}p")
            
           
            with st.expander("🔍 Risk Detayları"):
                st.write(f"**Paket-Yıl Hesaplaması:** {pack_years:.1f}")
                st.write(f"**İş Ortamı Risk Puanı:** {env_risk}p")
                st.write(f"**Koruyucu Faktörler:** {protective}p")
                st.write(f"**Toplam Risk Skoru:** {total_score}p")
                
                if daily_cigarettes > 0:
                    monthly_cost = (daily_cigarettes / 20) * 100 * 30  
                    st.write(f"**Aylık Sigara Maliyeti:** ~{monthly_cost:.0f} TL")
            
           
            st.subheader("💡 Kişiselleştirilmiş Öneriler")
            
            recommendations = generate_recommendations(risk_category, user_data)
            
            
            for i, recommendation in enumerate(recommendations, 1):
               
                if "🚨" in recommendation or "ACİL" in recommendation:
                    st.error(f"{i}. {recommendation}")
                elif "⚠️" in recommendation:
                    st.warning(f"{i}. {recommendation}")
                elif "✅" in recommendation:
                    st.success(f"{i}. {recommendation}")
                else:
                    st.info(f"{i}. {recommendation}")
            
            st.info("""
            **💡 Önemli Not:** Bu analiz sadece bilgilendirme amaçlıdır. 
            Kesin teşhis için lütfen bir sağlık uzmanına başvurun.
            """)

if __name__ == "__main__":

    main()

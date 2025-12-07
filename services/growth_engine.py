import numpy as np

# ==========================================
# 🌱 GROWTH STANDARDS DATABASE (Reference)
# ==========================================
# Ideal Growth Curves (Logistic/Linear Approximations)
# Format: {HST (Day): {Height_cm, Leaves, Stem_mm}}
GROWTH_STANDARDS = {
    "Cabai Merah": {
        "phase_switch": 35, # HST enters Generative
        "targets": {
            10: {"height": 10, "leaves": 5, "stem": 2},
            20: {"height": 25, "leaves": 12, "stem": 4},
            30: {"height": 45, "leaves": 30, "stem": 6},
            40: {"height": 60, "leaves": 80, "stem": 8},
            60: {"height": 90, "leaves": 150, "stem": 12},
            90: {"height": 120, "leaves": 200, "stem": 15}
        }
    },
    "Melon (Premium)": {
        "phase_switch": 25,
        "targets": {
            10: {"height": 15, "leaves": 4, "stem": 3},
            20: {"height": 50, "leaves": 15, "stem": 6},
            30: {"height": 120, "leaves": 25, "stem": 8},
            40: {"height": 180, "leaves": 35, "stem": 10}, # Topping usually at 25-30 leaves
            60: {"height": 200, "leaves": 35, "stem": 12}
        }
    }
}

def get_ideal_value(crop, hst, metric):
    """Interpolate ideal value closest to HST"""
    standards = GROWTH_STANDARDS.get(crop, {}).get("targets", {})
    days = sorted(standards.keys())
    
    if not days: return 0
    
    # Logic Simple: Find closest days (Prev & Next)
    prev_day = days[0]
    next_day = days[-1]
    
    for d in days:
        if d <= hst: prev_day = d
        if d >= hst: 
            next_day = d
            break
            
    val_prev = standards[prev_day].get(metric, 0)
    val_next = standards[next_day].get(metric, 0)
    
    if prev_day == next_day:
        return val_prev
        
    # Linear Interpolation
    slope = (val_next - val_prev) / (next_day - prev_day)
    interpolated = val_prev + slope * (hst - prev_day)
    return interpolated

def evaluate_growth(crop, hst, height, stem, leaf_color_idx):
    feedback = []
    status = "Normal"
    score = 100
    
    # 1. Height Check
    ideal_h = get_ideal_value(crop, hst, "height")
    if ideal_h > 0:
        dev_h = (height - ideal_h) / ideal_h
        if dev_h < -0.25:
            feedback.append("⚠️ **Kerdil (Stunted):** Tinggi tanaman di bawah standar (-{:.0f}%). Cek kecukupan air dan Nitrogen.".format(abs(dev_h)*100))
            status = "Perlu Perhatian"
            score -= 20
        elif dev_h > 0.30:
            feedback.append("⚠️ **Etiolasi (Kutilang):** Tanaman terlalu tinggi dan kurus. Kemungkinan kurang sinar matahari.")
            status = "Warning"
            score -= 15
        else:
            feedback.append("✅ Tinggi tanaman optimal sesuai umur.")

    # 2. Stem Check (Kekokohan)
    ideal_s = get_ideal_value(crop, hst, "stem")
    if ideal_s > 0 and stem > 0:
        dev_s = (stem - ideal_s) / ideal_s
        if dev_s < -0.20:
             feedback.append("⚠️ **Batang Kecil:** Batang kurang kokoh. Pertimbangkan penambahan Kalium (K) dan Kalsium (Ca).")
             score -= 10
        elif dev_s > 0.20:
             feedback.append("✅ **Batang Kokoh:** Perkembangan vegetatif sangat baik.")
             score += 5

    # 3. Leaf Color (Nitrogen Indicator)
    # Scale 1 (Pale Yellow) to 4 (Dark Green)
    if leaf_color_idx == 1:
        feedback.append("🍂 **Klorosis (Kuning):** Defisiensi Nitrogen parah atau pH tanah bermasalah. Segera aplikasi pupuk daun N tinggi.")
        status = "Kritis"
        score -= 30
    elif leaf_color_idx == 2:
        feedback.append("🍃 **Hijau Muda:** Indikasi kurang Nitrogen. Naikkan dosis pupuk N (Urea/AB Mix).")
        score -= 10
    elif leaf_color_idx == 4:
        feedback.append("🌿 **Hijau Gelap:** Kadar N sangat cukup (mungkin berlebih). Hati-hati serangan hama penghisap.")
    
    return status, score, feedback

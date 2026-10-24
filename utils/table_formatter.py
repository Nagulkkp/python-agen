"""
utils/table_formatter.py
========================
Human-Centric Deterministic Formatter & Hybrid Presentation Engine for HIMES AI.
Transforms raw MSSQL query result rows into clean, status-driven action cards
with collapsible detailed breakdowns for Standard Users, while retaining full
uncollapsed technical tables with query diagnostics for Developer Mode.

Universal Multilingual Support: Natively supports Tamil, Arabic, Hindi, Malayalam,
Telugu, Russian, French, Spanish, Tagalog, German, and English, plus universal fallback.
Zero LLM Token Consumption: All grouping, aggregation, panic threshold checks,
and Markdown/HTML rendering are processed deterministically in Python.
"""

import re
import json
from typing import List, Dict, Any, Optional

try:
    from valkey_himes_manager import valkey_manager
except Exception:
    valkey_manager = None


# -----------------------------------------------------------------------------
# UNIVERSAL LOCALIZED STRINGS & STATUS LABELS
# -----------------------------------------------------------------------------
LOCALIZED_CONTENT: Dict[str, Dict[str, str]] = {
    "ar": {
        "empty": "ℹ️ **تنبيه:** لم يتم العثور على أي سجلات مطابقة في قاعدة البيانات",
        "unbilled_title": "### ⚠️ ملخص الفحوصات والخدمات غير المفوترة",
        "unbilled_desc": "> **الحالة:** يوجد **{unbilled}** من أصل **{total}** خدمات/فحوصات لم يتم فوترتها بعد.",
        "billed_title": "### ✅ ملخص الخدمات والفحوصات المفوترة",
        "billed_desc": "> **الحالة:** تم فوترة واعتماد جميع الخدمات البالغ عددها **{total}** بنجاح.",
        "summary_btn": "📌 انقر لعرض جدول التفاصيل الكاملة ({count} بند)",
        "footer": "> ℹ️ تم استرداد هذه المعلومات مباشرة من قاعدة البيانات بصيغة مؤمنة (0 Tokens).",
        "unbilled_tag": "⚠️ غير مفوتر",
        "billed_tag": "✅ مفوتر"
    },
    "ta": {
        "empty": "ℹ️ **தகவல்:** நேரலை தரவுத்தளத்தில் பதிவுகள் எதுவும் கிடைக்கவில்லை",
        "unbilled_title": "### ⚠️ பில் செய்யப்படாத சேவைகள் விபரம் (Pending Unbilled Services)",
        "unbilled_desc": "> **நிலை:** மொத்தம் உள்ள **{total}** சேவைகளில் **{unbilled} சேவைகள்** இன்னும் பில் செய்யப்படவில்லை (Unbilled).",
        "billed_title": "### ✅ பதிவு செய்யப்பட்ட சேவைகள் விபரம் (All Billed)",
        "billed_desc": "> **நிலை:** அனைத்து **{total}** சேவைகளும் வெற்றிகரமாக பில் செய்யப்பட்டுள்ளன.",
        "summary_btn": "📌 முழு விபரங்களையும் அட்டவணையாக பார்க்க கிளிக் செய்யவும் ({count} items)",
        "footer": "> ℹ️ இந்தத் தகவல் நேரலை தரவுத்தளத்தில் இருந்து துல்லியமாகப் பெறப்பட்டு வழங்கப்பட்டுள்ளது (0 Tokens).",
        "unbilled_tag": "⚠️ பில் ஆகவில்லை",
        "billed_tag": "✅ பில் ஆனது"
    },
    "tanglish": {
        "empty": "ℹ️ **Status:** Database-la matching records ethuvum kidaikala",
        "unbilled_title": "### ⚠️ Innum Bill Aagatha Services (Pending Unbilled Services)",
        "unbilled_desc": "> **Status:** Motha **{total}** services-la **{unbilled} services** innum bill aagala (Pending).",
        "billed_title": "### ✅ Record Aana Services Breakdown (All Billed)",
        "billed_desc": "> **Status:** Motha **{total}** services-um bill aagi finalize aagirukku.",
        "summary_btn": "📌 Muzhu details table-ah paaka click pannunga ({count} items)",
        "footer": "> ℹ️ Intha details live hospital database-la irunthu direct-ah edukapattathu (0 Tokens).",
        "unbilled_tag": "⚠️ Bill Aagala",
        "billed_tag": "✅ Billed"
    },
    "hi": {
        "empty": "ℹ️ **सूचना:** अस्पताल डेटाबेस में कोई संबंधित रिकॉर्ड नहीं मिला",
        "unbilled_title": "### ⚠️ अनबिल्ड सेवाओं का विवरण (Pending Unbilled Services)",
        "unbilled_desc": "> **स्थिति:** कुल **{total}** सेवाओं में से **{unbilled} सेवाएं** अभी तक बिल नहीं की गई हैं (Unbilled)।",
        "billed_title": "### ✅ सभी सेवाएं सफलतापूर्वक बिल की गई हैं (All Billed)",
        "billed_desc": "> **स्थिति:** सभी **{total}** सेवाएं सफलतापूर्वक बिल और अंतिम रूप दी गई हैं।",
        "summary_btn": "📌 पूर्ण विवरण तालिका देखने के लिए क्लिक करें ({count} वस्तुएं)",
        "footer": "> ℹ️ यह जानकारी सीधे अस्पताल डेटाबेस से सत्यापित की गई है (0 Tokens)।",
        "unbilled_tag": "⚠️ अनबिल्ड",
        "billed_tag": "✅ बिल हुआ"
    },
    "ml": {
        "empty": "ℹ️ **വിവരം:** ഡാറ്റാബേസിൽ അനുയോജ്യമായ രേഖകൾ ഒന്നും കണ്ടെത്തിയില്ല",
        "unbilled_title": "### ⚠️ ബിൽ ചെയ്യാത്ത സേവനങ്ങളുടെ വിവരം (Pending Unbilled Services)",
        "unbilled_desc": "> **നില:** ആകെ **{total}** സേവനങ്ങളിൽ **{unbilled} എണ്ണം** ഇതുവരെ ബിൽ ചെയ്തിട്ടില്ല.",
        "billed_title": "### ✅ എല്ലാ സേവനങ്ങളും ബിൽ ചെയ്തു (All Billed)",
        "billed_desc": "> **നില:** രേഖപ്പെടുത്തിയ എല്ലാ **{total}** സേവനങ്ങളും ബിൽ ചെയ്തുകഴിഞ്ഞു.",
        "summary_btn": "📌 വിശദമായ പട്ടിക കാണുന്നതിന് ക്ലിക്ക് ചെയ്യുക ({count} എണ്ണം)",
        "footer": "> ℹ️ ഈ വിവരങ്ങൾ ഡാറ്റാബേസിൽ നിന്ന് നേരിട്ട് പരിശോധിച്ചതാണ് (0 Tokens).",
        "unbilled_tag": "⚠️ ബിൽ ചെയ്തിട്ടില്ല",
        "billed_tag": "✅ ബിൽ ചെയ്തു"
    },
    "te": {
        "empty": "ℹ️ **సమాచారం:** డేటాబేస్‌లో సరిపోలే రికార్డులు కనుగొనబడలేదు",
        "unbilled_title": "### ⚠️ బిల్ చేయని సేవల వివరాలు (Pending Unbilled Services)",
        "unbilled_desc": "> **స్థితి:** మొత్తం **{total}** సేవలలో **{unbilled} సేవలు** ఇంకా బిల్ చేయబడలేదు.",
        "billed_title": "### ✅ అన్ని సేవలు బిల్ చేయబడ్డాయి (All Billed)",
        "billed_desc": "> **స్థితి:** మొత్తం **{total}** సేవలు విజయవంతంగా బిల్ చేయబడ్డాయి.",
        "summary_btn": "📌 పూర్తి వివరాల పట్టికను చూడటానికి క్లిక్ చేయండి ({count} అంశాలు)",
        "footer": "> ℹ️ ఈ సమాచారం నేరుగా డేటాబేస్ నుండి ధృవీకరించబడింది (0 Tokens).",
        "unbilled_tag": "⚠️ బిల్ చేయలేదు",
        "billed_tag": "✅ బిల్ చేయబడింది"
    },
    "ru": {
        "empty": "ℹ️ **Уведомление:** Соответствующих записей в базе данных не найдено",
        "unbilled_title": "### ⚠️ Сводка по неоплаченным услугам (Pending Unbilled Services)",
        "unbilled_desc": "> **Статус:** Из **{total}** зарегистрированных услуг **{unbilled}** еще не оплачены/не выставлены.",
        "billed_title": "### ✅ Все услуги успешно оплачены и оформлены (All Billed)",
        "billed_desc": "> **Статус:** Все **{total}** оказанные услуги успешно оплачены.",
        "summary_btn": "📌 Нажмите, чтобы просмотреть полную таблицу ({count} поз.)",
        "footer": "> ℹ️ Информация получена напрямую из базы данных больницы (0 Tokens).",
        "unbilled_tag": "⚠️ Не оплачено",
        "billed_tag": "✅ Оплачено"
    },
    "fr": {
        "empty": "ℹ️ **Avis :** Aucun enregistrement correspondant trouvé dans la base de données",
        "unbilled_title": "### ⚠️ Récapitulatif des prestations non facturées (Pending Unbilled)",
        "unbilled_desc": "> **Statut :** **{unbilled}** sur **{total}** prestations enregistrées ne sont pas encore facturées.",
        "billed_title": "### ✅ Toutes les prestations sont facturées et validées (All Billed)",
        "billed_desc": "> **Statut :** L'ensemble des **{total}** prestations enregistrées sont facturées.",
        "summary_btn": "📌 Cliquez pour afficher le tableau détaillé complet ({count} éléments)",
        "footer": "> ℹ️ Informations vérifiées extraites directement de la base de données (0 Tokens).",
        "unbilled_tag": "⚠️ Non facturé",
        "billed_tag": "✅ Facturé"
    },
    "es": {
        "empty": "ℹ️ **Aviso:** No se encontraron registros coincidentes en la base de datos",
        "unbilled_title": "### ⚠️ Resumen de servicios pendientes de facturación (Pending Unbilled)",
        "unbilled_desc": "> **Estado:** **{unbilled}** de **{total}** servicios registrados están pendientes de facturar.",
        "billed_title": "### ✅ Todos los servicios han sido facturados y finalizados (All Billed)",
        "billed_desc": "> **Estado:** Todos los **{total}** servicios registrados han sido facturados.",
        "summary_btn": "📌 Haga clic para ver la tabla detallada completa ({count} elementos)",
        "footer": "> ℹ️ Información verificada obtenida directamente de la base de datos (0 Tokens).",
        "unbilled_tag": "⚠️ Pendiente",
        "billed_tag": "✅ Facturado"
    },
    "tl": {
        "empty": "ℹ️ **Abiso:** Walang natagpuang tala sa database",
        "unbilled_title": "### ⚠️ Buod ng mga Hindi pa Nasingil na Serbisyo (Pending Unbilled)",
        "unbilled_desc": "> **Katayuan:** **{unbilled}** sa **{total}** na naitalang serbisyo ay hindi pa sisingilin.",
        "billed_title": "### ✅ Lahat ng Serbisyo ay Nasingil Na (All Billed)",
        "billed_desc": "> **Katayuan:** Ang lahat ng **{total}** na serbisyo ay matagumpay na nasingil.",
        "summary_btn": "📌 I-click upang makita ang buong talaan ({count} aytem)",
        "footer": "> ℹ️ Ang impormasyong ito ay direktang nakuha mula sa database (0 Tokens).",
        "unbilled_tag": "⚠️ Hindi pa Bayad",
        "billed_tag": "✅ Bayad Na"
    },
    "de": {
        "empty": "ℹ️ **Hinweis:** Keine passenden Einträge in der Datenbank gefunden",
        "unbilled_title": "### ⚠️ Übersicht der nicht abgerechneten Leistungen (Pending Unbilled)",
        "unbilled_desc": "> **Status:** **{unbilled}** von **{total}** erfassten Leistungen sind noch nicht abgerechnet.",
        "billed_title": "### ✅ Alle Leistungen wurden abgerechnet (All Billed)",
        "billed_desc": "> **Status:** Alle **{total}** erfassten Leistungen sind vollständig abgerechnet.",
        "summary_btn": "📌 Klicken Sie hier für die vollständige Aufschlüsselung ({count} Positionen)",
        "footer": "> ℹ️ Verifizierte Daten direkt aus der Krankenhausdatenbank abgerufen (0 Tokens).",
        "unbilled_tag": "⚠️ Nicht abgerechnet",
        "billed_tag": "✅ Abgerechnet"
    },
    "kn": {
        "empty": "ℹ️ **ಮಾಹಿತಿ:** ಡೇಟಾಬೇಸ್‌ನಲ್ಲಿ ಹೊಂದಾಣಿಕೆಯಾಗುವ ದಾಖಲೆಗಳು ಕಂಡುಬಂದಿಲ್ಲ",
        "unbilled_title": "### ⚠️ ಬಿಲ್ ಮಾಡದ ಸೇವೆಗಳ ವಿವರ (Pending Unbilled Services)",
        "unbilled_desc": "> **ಸ್ಥಿತಿ:** ಒಟ್ಟು **{total}** ಸೇವೆಗಳಲ್ಲಿ **{unbilled} ಸೇವೆಗಳು** ಇನ್ನೂ ಬಿಲ್ ಮಾಡಲಾಗಿಲ್ಲ.",
        "billed_title": "### ✅ ಎಲ್ಲಾ ಸೇವೆಗಳು ಬಿಲ್ ಮಾಡಲಾಗಿದೆ (All Billed)",
        "billed_desc": "> **ಸ್ಥಿತಿ:** ಎಲ್ಲಾ **{total}** ಸೇವೆಗಳನ್ನು ಯಶಸ್ವಿಯಾಗಿ ಬಿಲ್ ಮಾಡಲಾಗಿದೆ.",
        "summary_btn": "📌 ಸಂಪೂರ್ಣ ವಿವರಗಳ ಕೋಷ್ಟಕವನ್ನು ವೀಕ್ಷಿಸಲು ಕ್ಲಿಕ್ ಮಾಡಿ ({count} ಐಟಂಗಳು)",
        "footer": "> ℹ️ ಈ ಮಾಹಿತಿಯನ್ನು ನೇರವಾಗಿ ಡೇಟಾಬೇಸ್‌ನಿಂದ ಪಡೆಯಲಾಗಿದೆ (0 Tokens).",
        "unbilled_tag": "⚠️ ಬಿಲ್ ಮಾಡಲಾಗಿಲ್ಲ",
        "billed_tag": "✅ ಬಿಲ್ ಮಾಡಲಾಗಿದೆ"
    },
    "bn": {
        "empty": "ℹ️ **তথ্য:** ডাটাবেসে কোনো সংশ্লিষ্ট রেকর্ড পাওয়া যায়নি",
        "unbilled_title": "### ⚠️ অবিল করা সেবাসমূহের বিবরণ (Pending Unbilled Services)",
        "unbilled_desc": "> **অবস্থা:** মোট **{total}** টি সেবার মধ্যে **{unbilled} টি সেবা** এখনও বিল করা হয়নি।",
        "billed_title": "### ✅ সমস্ত সেবা সফলভাবে বিল করা হয়েছে (All Billed)",
        "billed_desc": "> **অবস্থা:** সমস্ত **{total}** টি সেবা বিল এবং চূড়ান্ত করা হয়েছে।",
        "summary_btn": "📌 সম্পূর্ণ বিবরণ সারণী দেখতে ক্লিক করুন ({count} আইটেম)",
        "footer": "> ℹ️ এই তথ্যটি সরাসরি ডাটাবেস থেকে প্রাপ্ত (0 Tokens)।",
        "unbilled_tag": "⚠️ অবিল করা",
        "billed_tag": "✅ বিল করা হয়েছে"
    },
    "zh": {
        "empty": "ℹ️ **通知：** 数据库中未找到匹配的记录",
        "unbilled_title": "### ⚠️ 未开票诊疗与检查服务明细 (Pending Unbilled Services)",
        "unbilled_desc": "> **状态：** 在记录的 **{total}** 项服务中，有 **{unbilled} 项** 尚未开票结算。",
        "billed_title": "### ✅ 所有就诊服务均已完成开票结算 (All Billed)",
        "billed_desc": "> **状态：** 全部 **{total}** 项服务均已成功开票。",
        "summary_btn": "📌 点击查看完整数据明细表（共 {count} 项）",
        "footer": "> ℹ️ 数据直接从医院实时数据库安全调取（0 Tokens）。",
        "unbilled_tag": "⚠️ 未开票",
        "billed_tag": "✅ 已开票"
    },
    "ja": {
        "empty": "ℹ️ **通知：** 該当するデータがデータベースに見つかりませんでした",
        "unbilled_title": "### ⚠️ 未請求の診療・検査サマリー (Pending Unbilled Services)",
        "unbilled_desc": "> **ステータス:** 登録された **{total}** 件のサービスのうち **{unbilled} 件** が未請求です。",
        "billed_title": "### ✅ すべての診療サービスが請求済みです (All Billed)",
        "billed_desc": "> **ステータス:** 登録された全 **{total}** 件のサービスが請求済みです。",
        "summary_btn": "📌 詳細内訳テーブルを表示するにはクリックしてください ({count} 件)",
        "footer": "> ℹ️ 病院データベースから直接取得された確認済みデータです (0 Tokens)。",
        "unbilled_tag": "⚠️ 未請求",
        "billed_tag": "✅ 請求済み"
    },
    "it": {
        "empty": "ℹ️ **Avviso:** Nessun record corrispondente trovato nel database",
        "unbilled_title": "### ⚠️ Riepilogo prestazioni non fatturate (Pending Unbilled)",
        "unbilled_desc": "> **Stato:** **{unbilled}** su **{total}** prestazioni registrate non sono ancora state fatturate.",
        "billed_title": "### ✅ Tutte le prestazioni sono state fatturate (All Billed)",
        "billed_desc": "> **Stato:** Tutte le **{total}** prestazioni registrate sono state fatturate con successo.",
        "summary_btn": "📌 Fare clic per visualizzare la tabella dettagliata ({count} voci)",
        "footer": "> ℹ️ Informazioni verificate estratte direttamente dal database dell'ospedale (0 Tokens).",
        "unbilled_tag": "⚠️ Non fatturato",
        "billed_tag": "✅ Fatturato"
    },
    "pt": {
        "empty": "ℹ️ **Aviso:** Nenhum registro correspondente encontrado no banco de dados",
        "unbilled_title": "### ⚠️ Resumo de serviços não faturados (Pending Unbilled)",
        "unbilled_desc": "> **Status:** **{unbilled}** de **{total}** serviços registrados ainda não foram faturados.",
        "billed_title": "### ✅ Todos os serviços foram faturados e concluídos (All Billed)",
        "billed_desc": "> **Status:** Todos os **{total}** serviços registrados foram faturados.",
        "summary_btn": "📌 Clique para ver a tabela detalhada ({count} itens)",
        "footer": "> ℹ️ Informações verificadas extraídas diretamente do banco de dados (0 Tokens).",
        "unbilled_tag": "⚠️ Não faturado",
        "billed_tag": "✅ Faturado"
    },
    "tr": {
        "empty": "ℹ️ **Bilgi:** Veritabanında eşleşen kayıt bulunamadı",
        "unbilled_title": "### ⚠️ Faturalandırılmamış Hizmetler Özeti (Pending Unbilled)",
        "unbilled_desc": "> **Durum:** Kayıtlı **{total}** hizmetten **{unbilled} tanesi** henüz faturalandırılmadı.",
        "billed_title": "### ✅ Tüm Hizmetler Başarıyla Faturalandırıldı (All Billed)",
        "billed_desc": "> **Durum:** Kayıtlı **{total}** hizmetin tamamı faturalandırıldı.",
        "summary_btn": "📌 Detaylı tabloyu görüntülemek için tıklayın ({count} kalem)",
        "footer": "> ℹ️ Bu bilgiler doğrudan hastane veritabanından alınmıştır (0 Tokens).",
        "unbilled_tag": "⚠️ Faturalanmadı",
        "billed_tag": "✅ Faturalandı"
    },
    "id": {
        "empty": "ℹ️ **Pemberitahuan:** Tidak ada catatan yang cocok ditemukan di database",
        "unbilled_title": "### ⚠️ Ringkasan Layanan yang Belum Ditagih (Pending Unbilled)",
        "unbilled_desc": "> **Status:** **{unbilled}** dari **{total}** layanan yang tercatat belum ditagihkan.",
        "billed_title": "### ✅ Semua Layanan Telah Berhasil Ditagih (All Billed)",
        "billed_desc": "> **Status:** Semua **{total}** layanan yang tercatat telah ditagih.",
        "summary_btn": "📌 Klik untuk melihat tabel rincian lengkap ({count} item)",
        "footer": "> ℹ️ Informasi diverifikasi langsung dari database rumah sakit (0 Tokens).",
        "unbilled_tag": "⚠️ Belum Ditagih",
        "billed_tag": "✅ Sudah Ditagih"
    },
    "en": {
        "empty": "ℹ️ **Notice:** No matching records found in the database",
        "unbilled_title": "### ⚠️ Pending Unbilled Services Summary",
        "unbilled_desc": "> **Status:** **{unbilled}** of **{total}** recorded services are currently unbilled.",
        "billed_title": "### ✅ Patient Services & Procedures Overview (All Billed)",
        "billed_desc": "> **Status:** All **{total}** recorded services are billed and finalized.",
        "summary_btn": "📌 Click to view full breakdown table ({count} items)",
        "footer": "> ℹ️ Live verified clinical & billing facts retrieved directly from the hospital database (0 Tokens).",
        "unbilled_tag": "⚠️ Unbilled",
        "billed_tag": "✅ Billed"
    }
}


def detect_language(text: Optional[str]) -> str:
    """
    Detects user language from prompt or context text across any world language.
    Supports Unicode script blocks and transliterated romanized dialects with universal fallback.
    """
    if not text:
        return "en"
    
    # 1. Arabic / Urdu / Persian script range: \u0600-\u06FF
    if re.search(r"[\u0600-\u06FF]", text):
        return "ar"
    
    # 2. Tamil script range: \u0B80-\u0BFF
    if re.search(r"[\u0B80-\u0BFF]", text):
        return "ta"

    # 3. Hindi / Devanagari script: \u0900-\u097F
    if re.search(r"[\u0900-\u097F]", text):
        return "hi"

    # 4. Malayalam script: \u0D00-\u0D7F
    if re.search(r"[\u0D00-\u0D7F]", text):
        return "ml"

    # 5. Telugu script: \u0C00-\u0C7F
    if re.search(r"[\u0C00-\u0C7F]", text):
        return "te"

    # 6. Kannada script: \u0C80-\u0CFF
    if re.search(r"[\u0C80-\u0CFF]", text):
        return "kn"

    # 7. Bengali script: \u0980-\u09FF
    if re.search(r"[\u0980-\u09FF]", text):
        return "bn"

    # 8. Russian / Cyrillic script: \u0400-\u04FF
    if re.search(r"[\u0400-\u04FF]", text):
        return "ru"

    # 9. Japanese scripts (Hiragana/Katakana): \u3040-\u30FF
    if re.search(r"[\u3040-\u30FF]", text):
        return "ja"

    # 10. Chinese / Han characters: \u4E00-\u9FFF
    if re.search(r"[\u4E00-\u9FFF]", text):
        return "zh"

    # 11. Korean Hangul: \uAC00-\uD7AF
    if re.search(r"[\uAC00-\uD7AF]", text):
        return "ko"

    lower = text.lower()

    # 12. French
    if any(re.search(rf"\b{w}\b", lower) for w in ["est-ce", "pour", "factur", "facturé", "non-facturé", "combien", "montrer", "veuillez", "prestations"]):
        return "fr"

    # 13. Portuguese
    if any(re.search(rf"\b{w}\b", lower) for w in ["quais", "são", "sao", "não", "nao", "faturado", "faturados", "faturação", "serviços", "servicos", "exames", "para o"]):
        return "pt"

    # 14. Spanish
    if any(re.search(rf"\b{w}\b", lower) for w in ["cuáles", "cuales", "facturado", "facturados", "pendiente", "servicios", "favor", "pruebas", "para el", "no facturados"]):
        return "es"

    # 15. Italian
    if any(re.search(rf"\b{w}\b", lower) for w in ["quali", "fatturato", "fatturati", "servizi", "paziente", "mostra", "esami"]):
        return "it"

    # 16. Turkish
    if any(re.search(rf"\b{w}\b", lower) for w in ["lütfen", "hasta", "hizmet", "hizmetler", "fatura", "faturalanmamış", "ödenmemiş"]):
        return "tr"

    # 17. Indonesian / Malay
    if any(re.search(rf"\b{w}\b", lower) for w in ["tagihan", "layanan", "pasien", "belum", "ditagih", "tampilkan"]):
        return "id"

    # 18. Tanglish structural linguistic morphemes and common words
    if re.search(r"(-ku\b|-la\b|-oda\b|\biruk|\benna\b|\bkaattu\b|\bsollu\b|\bnethu\b|\binaiku\b|\bpaaru\b|\bkodu\b|\bpanren\b|\bpannu\b|\bathanala\b|\bantha\b|\bintha\b|\byaar\b|\byaaravathu\b|\bpanniruk|\bpotruk)", lower):
        return "tanglish"

    # Default for Latin / unclassified queries
    return "en"


def categorize_row(row: Dict[str, Any]) -> str:
    """
    Categorizes a clinical or financial row into natural hospital departments:
    - Laboratory
    - Radiology
    - Pharmacy
    - Bed & Accommodation
    - Consultation & Clinical Procedures
    """
    cpt = str(row.get("CPT_Code") or row.get("cpt_code") or row.get("CPT") or "").strip()
    desc = str(
        row.get("Service_Description") or 
        row.get("Test_Name") or 
        row.get("Item_Description") or 
        row.get("Drug_Brand_Name") or 
        row.get("Drug_Generic_Name") or 
        row.get("Description") or 
        row.get("Service_Name") or 
        ""
    ).lower()

    # 1. Pharmacy / Medications
    has_pharm_cols = any(k in row for k in ["Drug_Brand_Name", "Drug_Generic_Name", "Dosage", "Duration_In_Days"])
    pharm_keywords = [
        "mg", "ml", "tablet", "syrup", "capsule", "injection", "inj", "drops", 
        "cream", "ointment", "pharma", "rx", "dose", "antibiotic", "suspension", "paracetamol", "amoxicillin"
    ]
    if has_pharm_cols or any(w in desc for w in pharm_keywords):
        return "Pharmacy"

    # 2. Radiology & Imaging (CPT 70000-79999 or keywords)
    rad_keywords = [
        "x-ray", "xray", "mri", "ct scan", "ultrasound", "usg", "radiology", 
        "doppler", "echocardiogram", "echo", "mammography", "sonography", "radiograph"
    ]
    if (cpt.isdigit() and 70000 <= int(cpt) <= 79999) or any(w in desc for w in rad_keywords):
        return "Radiology"

    # 3. Laboratory & Investigations (CPT 80000-89999 or keywords)
    lab_keywords = [
        "lab", "culture", "cbc", "blood", "panel", "screen", "profile", "assay", 
        "smear", "test", "biochemistry", "hematology", "urinalysis", "urine", 
        "pathology", "potassium", "sodium", "calcium", "glucose", "hemoglobin", 
        "platelet", "troponin", "creatinine", "lipid", "hba1c", "cochlear"
    ]
    if (cpt.isdigit() and 80000 <= int(cpt) <= 89999) or any(w in desc for w in lab_keywords):
        return "Laboratory"

    # 4. Bed & Room Accommodation
    bed_keywords = [
        "bed", "room", "icu", "ward", "admission", "nursing", "stay", "accommodation", "daycare"
    ]
    if any(w in desc for w in bed_keywords):
        return "Bed & Accommodation"

    # 5. Consultations & Clinical Procedures (CPT 90000-99999 or default)
    return "Consultation & Clinical Procedures"


def is_row_unbilled(row: Dict[str, Any]) -> bool:
    """Checks if a service/item row is unbilled or pending."""
    if "Is_Service_Billed" in row:
        val = str(row["Is_Service_Billed"]).strip().upper()
        if val in ["N", "NO", "0", "FALSE"]:
            return True
        if val in ["Y", "YES", "1", "TRUE"]:
            return False

    if "Is_Bill_Finalized" in row:
        val = str(row["Is_Bill_Finalized"]).strip().upper()
        if val not in ["C", "FINALIZED", "Y", "TRUE"]:
            return True
        return False

    return False


def evaluate_panic_alerts(query_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Checks numeric test results against Valkey panic thresholds."""
    if not valkey_manager:
        return []
    
    alerts = []
    for row in query_results:
        analyte = (
            row.get("Test_Name") or 
            row.get("Item_Description") or 
            row.get("Service_Description") or 
            row.get("Analyte") or 
            ""
        )
        val_str = str(row.get("Result_Value") or row.get("Numeric_Value") or row.get("Value") or "").strip()
        if not analyte or not val_str:
            continue
            
        num_match = re.search(r"[-+]?\d*\.?\d+", val_str)
        if num_match:
            try:
                num_val = float(num_match.group(0))
                panic_eval = valkey_manager.evaluate_panic_value(str(analyte), num_val)
                if panic_eval and panic_eval.get("is_panic"):
                    alerts.append(panic_eval)
            except Exception:
                pass
    return alerts


def is_clinical_service_dataset(rows: List[Dict[str, Any]]) -> bool:
    """Checks if the result rows actually represent clinical services or encounter orders."""
    if not rows or not isinstance(rows[0], dict):
        return False
    service_cols = {
        "cpt_code", "cpt", "service_description", "service_name", "test_name",
        "drug_brand_name", "drug_generic_name", "item_description", "is_service_billed", 
        "patient_visit_services_serial_no", "service_ussdb_serial_no", "analyte"
    }
    sample = rows[0]
    keys_lower = {k.lower() for k in sample.keys()}
    return bool(keys_lower.intersection(service_cols))


def format_user_friendly_response(
    query_results: List[Dict[str, Any]], 
    query_context: Optional[Dict[str, Any]] = None, 
    mode: str = "user"
) -> str:
    """
    Main Entry Point: Transforms raw database query results into an intuitive, 
    human-readable card presentation in ANY world language.

    Args:
        query_results: List of dictionary records returned by MSSQL.
        query_context: Metadata including user_query, mrn, visit_no, executed_sql, etc.
        mode: 'user' (clean cards + collapsible details) or 'developer' (uncollapsed diagnostic view).

    Returns:
        Formatted Markdown / HTML string with 0 additional LLM token cost.
    """
    context = query_context or {}
    user_query = context.get("user_query", "")
    lang = context.get("lang") or detect_language(user_query)
    mrn = context.get("mrn") or ""
    visit_no = context.get("visit_no") or ""
    executed_sql = context.get("executed_sql") or ""

    loc = LOCALIZED_CONTENT.get(lang, LOCALIZED_CONTENT["en"])

    # 1. Handle Empty Results
    if not query_results:
        id_str = f" (`{mrn}`)" if mrn else ""
        visit_str = f" (Visit: `{visit_no}`)" if visit_no else ""
        empty_msg = f"{loc['empty']}{id_str}{visit_str}."
        if executed_sql:
            empty_msg += (
                f"\n\n<details>\n"
                f"<summary>🔍 <b>View Generated SQL Query</b></summary>\n\n"
                f"```sql\n{executed_sql.strip()}\n```\n"
                f"</details>"
            )
        return empty_msg

    # 1.5 Route Non-Clinical Queries to Generic Formatter
    # Prevents patient/doctor/visit/setting queries from falsely displaying as "Consultation & Clinical Procedures" and "Billed"
    if not is_clinical_service_dataset(query_results):
        latency_ms = context.get("latency_ms", 0)
        return format_generic_query_result(
            rows=query_results,
            executed_sql=executed_sql,
            latency_ms=latency_ms,
            mode=mode
        )

    # 2. Metric Aggregations & Department Grouping
    total_count = len(query_results)
    unbilled_count = 0
    billed_count = 0
    total_amount = 0.0
    has_amount = False

    groups: Dict[str, List[Dict[str, Any]]] = {
        "Laboratory": [],
        "Radiology": [],
        "Pharmacy": [],
        "Bed & Accommodation": [],
        "Consultation & Clinical Procedures": []
    }

    for row in query_results:
        cat = categorize_row(row)
        groups[cat].append(row)

        if is_row_unbilled(row):
            unbilled_count += 1
        else:
            billed_count += 1

        for amt_col in ["Service_Net_Amount", "Bill_Net_Value", "Service_Gross_Amount", "Amount", "Net_Value", "Total_Amount"]:
            if amt_col in row and row[amt_col] is not None:
                try:
                    total_amount += float(str(row[amt_col]).replace(",", "").strip())
                    has_amount = True
                    break
                except Exception:
                    pass

    panic_alerts = evaluate_panic_alerts(query_results)

    # -------------------------------------------------------------------------
    # VIEW MODE A: DEVELOPER VIEW (Uncollapsed full table + SQL diagnostics)
    # -------------------------------------------------------------------------
    if mode == "developer":
        dev_lines = []
        dev_lines.append(f"### 💻 Developer Diagnostics & Technical Data View")
        latency_str = f" | **DB Latency:** `{context['latency_ms']} ms`" if context.get("latency_ms") is not None else ""
        dev_lines.append(f"• **Record Count:** `{total_count}` rows | **Unbilled:** `{unbilled_count}` | **Billed:** `{billed_count}`{latency_str}")
        if mrn or visit_no:
            dev_lines.append(f"• **Context Keys:** MRN: `{mrn or 'N/A'}` | Visit: `{visit_no or 'N/A'}`")
        if executed_sql:
            dev_lines.append(f"\n**Executed MSSQL Query:**\n```sql\n{executed_sql.strip()}\n```")

        cols = list(query_results[0].keys())
        header_row = "| " + " | ".join(cols) + " |"
        sep_row = "| " + " | ".join([":---" for _ in cols]) + " |"
        data_rows = []
        for r in query_results:
            row_str = "| " + " | ".join([str(r.get(c, "-")).replace("\n", " ") for c in cols]) + " |"
            data_rows.append(row_str)
            
        dev_lines.append(f"\n**Full Dataset Output ({total_count} rows):**\n")
        dev_lines.append(header_row)
        dev_lines.append(sep_row)
        dev_lines.extend(data_rows)
        dev_lines.append(f"\n*(⚡ Executed on MSSQL with 0 LLM Presentation Tokens | Cached in Valkey 5m)*")
        return "\n".join(dev_lines)

    # -------------------------------------------------------------------------
    # VIEW MODE B: USER VIEW (Human-Centric Status Card + Collapsible Details)
    # -------------------------------------------------------------------------
    card_sections = []

    # 1. Top Status Indicator
    if panic_alerts:
        alert_text = "\n".join([f"- {a['alert_banner']}" for a in panic_alerts])
        card_sections.append(f"### 🚨 CRITICAL CLINICAL ALERTS DETECTED\n{alert_text}\n")
    elif unbilled_count > 0:
        card_sections.append(
            f"{loc['unbilled_title']}\n"
            f"{loc['unbilled_desc'].format(unbilled=unbilled_count, total=total_count)}"
        )
    else:
        card_sections.append(
            f"{loc['billed_title']}\n"
            f"{loc['billed_desc'].format(total=total_count)}"
        )

    # 2. Patient / Visit Header Metadata
    meta_badges = []
    if mrn:
        meta_badges.append(f"**MRN:** `{mrn}`")
    if visit_no:
        meta_badges.append(f"**Visit No:** `{visit_no}`")
    if has_amount:
        meta_badges.append(f"**Total Amount:** `AED {total_amount:,.2f}`")
    if meta_badges:
        card_sections.append("• " + " | ".join(meta_badges) + "\n")

    # 3. Department / Category Bulleted Breakdown
    category_bullets = []
    category_icons = {
        "Laboratory": "🔬",
        "Radiology": "🩻",
        "Pharmacy": "💊",
        "Bed & Accommodation": "🛏️",
        "Consultation & Clinical Procedures": "👨‍⚕️"
    }

    for cat_name, cat_rows in groups.items():
        if not cat_rows:
            continue
        c_count = len(cat_rows)
        c_unbilled = sum(1 for r in cat_rows if is_row_unbilled(r))
        icon = category_icons.get(cat_name, "📋")
        
        status_desc = f"({c_unbilled} {loc['unbilled_tag']})" if c_unbilled > 0 else f"({loc['billed_tag']})"
        category_bullets.append(f"• {icon} **{cat_name}:** {c_count} items {status_desc}")

    if category_bullets:
        card_sections.append("**Department Summary:**\n" + "\n".join(category_bullets) + "\n")

    # 4. Collapsible Detailed Breakdown Table
    summary_btn_label = loc["summary_btn"].format(count=total_count)

    table_header = "| CPT / Code | Description | Department | Qty | Status |\n| :--- | :--- | :--- | :--- | :--- |"
    table_rows = []
    for r in query_results:
        cpt = r.get("CPT_Code") or r.get("Service_Internal_Code") or r.get("cpt_code") or "-"
        desc = (
            r.get("Service_Description") or 
            r.get("Test_Name") or 
            r.get("Drug_Brand_Name") or 
            r.get("Description") or 
            r.get("Item_Description") or 
            "Medical Service"
        )
        dept = categorize_row(r)
        qty = r.get("Service_Quantity") or r.get("Quantity") or 1
        if "Is_Service_Billed" in r or "Is_Bill_Finalized" in r:
            unb = is_row_unbilled(r)
            status_label = loc["unbilled_tag"] if unb else loc["billed_tag"]
        else:
            status_label = "📋 Active"
        table_rows.append(f"| {cpt} | {desc} | {dept} | {qty} | {status_label} |")

    collapsible_table = (
        f"<details>\n"
        f"<summary><b>{summary_btn_label}</b></summary>\n\n"
        f"{table_header}\n"
        + "\n".join(table_rows) + "\n\n"
        f"</details>"
    )
    card_sections.append(collapsible_table)

    # 5. Expandable / Collapsible Generated SQL Query View for Standard Users
    if executed_sql:
        sql_toggle = (
            f"\n<details>\n"
            f"<summary>🔍 <b>View Generated SQL Query</b></summary>\n\n"
            f"```sql\n{executed_sql.strip()}\n```\n"
            f"</details>"
        )
        card_sections.append(sql_toggle)

    # 6. Localized Footer
    card_sections.append(f"\n{loc['footer']}")

    return "\n".join(card_sections)


# -----------------------------------------------------------------------------
# GENERIC QUERY RESULT FORMATTER (for direct SELECT queries via chat input)
# Produces clean readable markdown tables with collapsible large result sets.
# Does NOT assume patient/billing data — works for ANY table/query result.
# -----------------------------------------------------------------------------

def format_generic_query_result(
    rows: List[Dict[str, Any]],
    executed_sql: str = "",
    latency_ms: float = 0,
    mode: str = "user",
    display_limit: int = 20
) -> str:
    """
    Format raw SQL query results into a clean, readable markdown table.
    - Shows up to `display_limit` rows by default.
    - If total rows > display_limit, remaining rows appear in a collapsible <details> accordion.
    - In developer mode, also shows the executed SQL and latency.
    """
    if not rows:
        result = f"ℹ️ Query returned **0 rows** (`{latency_ms} ms`)\n\n"
        if mode == "developer" and executed_sql:
            result += f"```sql\n{executed_sql.strip()}\n```"
        return result

    total = len(rows)
    cols = list(rows[0].keys())

    def _cell(value) -> str:
        """Sanitize a cell value for markdown table."""
        s = str(value) if value is not None else "—"
        return s.replace("\n", " ").replace("\r", "").replace("|", "\\|")[:200]

    def _build_md_table(data_rows: List[Dict]) -> str:
        header = "| " + " | ".join(cols) + " |"
        sep = "| " + " | ".join([":---"] * len(cols)) + " |"
        lines = [header, sep]
        for r in data_rows:
            cells = [_cell(r.get(c)) for c in cols]
            lines.append("| " + " | ".join(cells) + " |")
        return "\n".join(lines)

    display_rows = rows[:display_limit]
    overflow_rows = rows[display_limit:]

    # Primary visible table
    primary_table = _build_md_table(display_rows)

    # Summary line
    if total == 1:
        count_label = "**1 row** returned"
    else:
        count_label = f"**{total} rows** returned"

    header_line = f"📊 {count_label} (`{latency_ms} ms`)"

    parts = [header_line, "", primary_table]

    # If there are overflow rows, put them in a collapsible accordion
    if overflow_rows:
        overflow_table = _build_md_table(overflow_rows)
        collapsible = (
            f"\n<details>\n"
            f"<summary><b>📋 Show remaining {len(overflow_rows)} rows "
            f"(rows {display_limit + 1}–{total})</b></summary>\n\n"
            f"{overflow_table}\n\n"
            f"</details>"
        )
        parts.append(collapsible)

    # Developer mode: append the executed SQL
    if mode == "developer" and executed_sql:
        parts.append(
            f"\n<details>\n"
            f"<summary>🔍 <b>View Executed SQL</b></summary>\n\n"
            f"```sql\n{executed_sql.strip()}\n```\n"
            f"*(⚡ Live MSSQL | 0 LLM Tokens)*\n\n"
            f"</details>"
        )

    return "\n".join(parts)

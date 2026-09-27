<div align="center">

<img src="app/logo AIN.png" alt="AIN Logo" width="140"/>

# 👁️ AIN | عين

### نظام ذكاء اصطناعي عربي لرصد الرسائل الخطرة الموجّهة للأطفال

مبني على نموذج **[MARBERTv2](https://huggingface.co/UBC-NLP/MARBERTv2)** المضبوط (Fine-tuned) لتصنيف الرسائل العربية إلى **آمنة** أو **خطرة**، مع منظومة كاملة لرصد الخطورة، تنبيه أولياء الأمور فورًا، ومتابعة الحوادث عبر لوحة تحكم.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Transformers](https://img.shields.io/badge/🤗%20Transformers-MARBERTv2-yellow)](https://huggingface.co/UBC-NLP/MARBERTv2)
[![n8n](https://img.shields.io/badge/n8n-Automation-EA4B71?logo=n8n&logoColor=white)](https://n8n.io/)

</div>

---

## 📖 فكرة المشروع

**AIN (عين)** نظام يراقب رسائل المحادثات النصية العربية (شات، ألعاب، منصات تعليمية...) ويحلّل كل رسالة عبر نموذج MARBERTv2 المدرّب خصيصًا لكشف المحتوى الخطر الموجّه للأطفال (استغلال، تحرّش، ألفاظ مسيئة...). عند اكتشاف رسالة عالية الخطورة، يسجّل النظام تنبيهًا ويرسله تلقائيًا لولي الأمر عبر أتمتة **n8n**، مع إمكانية متابعة كل الحوادث من لوحة تحكم مخصّصة.

> الاسم "عين" يعبّر عن فكرة المشروع: عين ساهرة ترصد الخطر وتنبّه قبل تفاقمه.

### أداء النموذج

| المقياس | القيمة |
|---|---|
| الدقة (Accuracy) | **91.4%** |
| استرجاع الرسائل الخطرة (Risk Recall) | **94%** |
| حجم بيانات التدريب | **+22,000** رسالة عربية مصنّفة |

---

## ✨ كيف يعمل النظام

1. **رسالة تدخل النظام** (من واجهة Streamlit التجريبية أو أي تطبيق خارجي عبر الـ API).
2. **`ain/model/inference.py`** يمرّر النص على MARBERTv2 ويرجّع درجة خطورة (`risk_score`) ودرجة أمان (`safe_score`).
3. **`ain/Risk/Engine.py`** يحوّل درجة الخطورة إلى مستوى (`SAFE` 🟢 / `LOW` 🟡 / `MEDIUM` 🟠 / `HIGH` 🔴).
4. تُخزَّن كل رسالة في قاعدة البيانات، وإذا كان المستوى **HIGH** يُنشأ تنبيه عبر **`ain/alerts/service.py`**.
5. إذا كان ولي الأمر مسجَّلًا (وخارج فترة التهدئة الافتراضية 5 دقائق لنفس المحادثة)، يُرسَل التنبيه تلقائيًا إلى **n8n** (`ain/notifications/n8n.py`) عبر Webhook، ليصل بريد إلكتروني لولي الأمر.
6. يمكن متابعة كل الرسائل والتنبيهات ومراجعتها/تجاهلها من **لوحة التحكم**.

---

## 🏗️ هيكل المشروع

```
AIN/
├── ain/                        # المنطق الأساسي (Core)
│   ├── Risk/Engine.py          # تحويل risk_score إلى مستوى خطورة (SAFE/LOW/MEDIUM/HIGH)
│   ├── alerts/
│   │   ├── rules.py            # قواعد إنشاء التنبيه (HIGH فقط)
│   │   └── service.py          # إنشاء التنبيهات + التهدئة (Cooldown) + الإرسال لـ n8n
│   ├── database/
│   │   ├── database.py         # اتصال SQLAlchemy (SQLite افتراضيًا / PostgreSQL اختياريًا)
│   │   ├── models.py           # جداول: Parent, Message, Alert, Feedback
│   │   └── repository.py       # عمليات CRUD
│   ├── model/
│   │   ├── loader.py           # تحميل MARBERTv2 من Hugging Face
│   │   └── inference.py        # تشغيل الاستدلال (Inference) على النصوص
│   └── notifications/n8n.py    # إرسال التنبيهات/الملاحظات إلى n8n عبر Webhook
│
├── api/                         # واجهة FastAPI
│   ├── main.py                  # نقطة الدخول + تسجيل الراوترات
│   ├── schemas.py                # نماذج Pydantic للطلبات والاستجابات
│   └── routes/
│       ├── analyze.py            # POST /api/v1/analyze
│       ├── parents.py            # POST /api/v1/parents
│       ├── dashboard.py          # GET /api/v1/dashboard/summary, /alerts...
│       └── feedback.py           # POST /api/v1/feedback
│
├── app/                          # واجهة Streamlit
│   ├── Home.py                   # الصفحة الرئيسية
│   ├── pages/
│   │   ├── live_demo.py          # تجربة حيّة: شات + مقياس خطورة لحظي
│   │   ├── Dashboard.py          # لوحة تحكم: إحصائيات، رسوم بيانية، إدارة التنبيهات
│   │   ├── parent_setup.py       # تسجيل بريد ولي الأمر لجلسة/محادثة معيّنة
│   │   └── feedback.py           # إرسال اقتراحات/ملاحظات/بلاغات
│   ├── components/                # sidebar.py, risk_meter.py
│   └── services/api_client.py     # عميل HTTP للتواصل مع FastAPI
│
├── n8n/                           # سير عمل الأتمتة (Workflows) الجاهزة للاستيراد
│   ├── AIN.json                   # سير إرسال تنبيهات الخطورة لولي الأمر
│   └── FeedBack-AIN.json          # سير معالجة الاقتراحات/الملاحظات
│
├── notebooks/AIN_Training.ipynb   # تجهيز البيانات وتدريب/تقييم MARBERTv2
├── Data/
│   ├── All_data.csv               # +22K رسالة عربية (Feature, Target: Safe/risky)
│   └── Arabic_offensive_comment_detection_annotation_4000_selected.xlsx
├── tests/                         # اختبارات Pytest (alerts, api, database, feedback, n8n)
├── .devcontainer/devcontainer.json
└── requirements.txt
```

---

## 🚀 التشغيل محليًا

### المتطلبات

- Python 3.11
- (اختياري) GPU لتسريع الاستدلال — يعمل على CPU افتراضيًا
- حساب n8n (سحابي أو ذاتي الاستضافة) إذا أردت تفعيل إرسال التنبيهات فعليًا

### 1. الاستنساخ وتثبيت الاعتماديات

```bash
git clone https://github.com/HamzehAlshraah/AIN.git
cd AIN

python -m venv venv
source venv/bin/activate      # على Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. إعداد متغيرات البيئة

أنشئ ملف `.env` في جذر المشروع:

```env
# قاعدة البيانات (اختياري — الافتراضي SQLite محلي: ain.db)
DATABASE_URL=postgresql://user:password@localhost:5432/ain

# روابط Webhook الخاصة بسير عمل n8n (اختياري لتفعيل الإشعارات الفعلية)
N8N_WEBHOOK_URL=https://your-n8n-instance/webhook/ain-alert
N8N_FEEDBACK_WEBHOOK_URL=https://your-n8n-instance/webhook/ain-feedback

# عنوان الـ API الذي تتصل به واجهة Streamlit
API_BASE_URL=http://localhost:8000
```

> النموذج نفسه لا يحتاج إعدادًا إضافيًا؛ يُحمَّل تلقائيًا من Hugging Face (`HazmehAlshraah/marbert-risk-model`) عند أول استدعاء لتحليل رسالة.

### 3. تشغيل الـ API (FastAPI)

```bash
uvicorn api.main:app --reload --port 8000
```

توثيق تفاعلي تلقائي متاح على: `http://localhost:8000/docs`

### 4. تشغيل واجهة Streamlit

```bash
streamlit run app/Home.py
```

ستُفتح على `http://localhost:8501`، وتتضمن: الصفحة الرئيسية، التجربة الحيّة، تسجيل ولي الأمر، لوحة التحكم، والاقتراحات/الملاحظات.

### 5. (اختياري) استيراد سير عمل n8n

استورد `n8n/AIN.json` و `n8n/FeedBack-AIN.json` إلى نسخة n8n الخاصة بك، فعِّل السير، وانسخ روابط الـ Webhook إلى ملف `.env`.

### 6. تشغيل الاختبارات

```bash
pytest
```

---

## 🔌 نقاط الـ API الرئيسية

| Method | Endpoint | الوصف |
|---|---|---|
| `GET` | `/health` | فحص حالة الخدمة |
| `POST` | `/api/v1/analyze` | تحليل رسالة وإرجاع درجة/مستوى الخطورة |
| `POST` | `/api/v1/parents` | تسجيل ولي أمر لمحادثة معيّنة |
| `GET` | `/api/v1/dashboard/summary` | ملخص إحصائي (رسائل، أحداث خطورة، أعلى درجة) |
| `GET` | `/api/v1/alerts` | قائمة كل التنبيهات |
| `GET` | `/api/v1/alerts/{id}` | تفاصيل تنبيه محدد |
| `PATCH` | `/api/v1/alerts/{id}` | تحديث حالة التنبيه (`NEW` / `REVIEWED` / `DISMISSED`) |
| `GET` | `/api/v1/conversations/{id}/messages` | كل رسائل محادثة معيّنة |
| `POST` | `/api/v1/feedback` | إرسال اقتراح/ملاحظة/بلاغ (بحد أقصى كل 10 دقائق لكل محادثة) |

---

## 🧠 عن النموذج

النموذج المستخدم مضبوط (Fine-tuned) فوق **[MARBERTv2](https://huggingface.co/UBC-NLP/MARBERTv2)** من فريق UBC-NLP، وهو من أقوى نماذج BERT للعربية الفصحى واللهجات. تم تدريبه على أكثر من 22 ألف رسالة عربية مصنّفة (`Data/All_data.csv`) للتمييز بين رسالة **آمنة (Safe)** و**خطرة (risky)**، وتفاصيل التدريب والتقييم موثّقة في `notebooks/AIN_Training.ipynb`. النموذج النهائي مستضاف ويُحمَّل مباشرة من Hugging Face.

مستويات الخطورة المستخدمة في الإنتاج (`ain/Risk/Engine.py`):

| المستوى | النطاق |
|---|---|
| 🟢 SAFE | أقل من 0.30 |
| 🟡 LOW | 0.30 – 0.50 |
| 🟠 MEDIUM | 0.50 – 0.75 |
| 🔴 HIGH (يُطلق تنبيهًا) | 0.75 فأعلى |

---

## 🤝 المساهمة

1. Fork للمستودع.
2. فرع جديد: `git checkout -b feature/amazing-feature`
3. `git commit -m "إضافة ميزة جديدة"`
4. `git push origin feature/amazing-feature`
5. فتح Pull Request.

يمكنك أيضًا استخدام صفحة **الاقتراحات والملاحظات** داخل التطبيق نفسه لإرسال أفكار أو بلاغات مباشرة.

---

## ⚖️ إخلاء مسؤولية

AIN أداة مساعدة لرصد المحتوى الخطر، وليست بديلًا عن الإشراف الأبوي المباشر أو التبليغ للجهات المختصة بحماية الطفل عند الحاجة. يُنصح باستخدامها كطبقة حماية إضافية ضمن منظومة أوسع للأمان الرقمي للأطفال.

---

## 👤 التواصل

**Hamzeh Alshraah** — [@HamzehAlshraah](https://github.com/HamzehAlshraah)

<div align="center">

إذا أعجبك المشروع لا تنسَ ترك ⭐ على المستودع!

</div>

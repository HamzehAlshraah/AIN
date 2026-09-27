# 👁️ عين (AIN)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ainchild.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Model](https://img.shields.io/badge/Model-MARBERTv2-orange)
![API](https://img.shields.io/badge/API-FastAPI-009688)
![Database](https://img.shields.io/badge/Database-Supabase%20%2F%20PostgreSQL-3ECF8E)

> **AIN (عين)** هو نظام ذكاء اصطناعي يهدف إلى المساعدة في حماية الأطفال والمراهقين من المحتوى العربي الخطِر من خلال تحليل الرسائل، تقدير مستوى الخطورة، وتوليد تنبيهات لولي الأمر عند اكتشاف محتوى عالي الخطورة.

## 🌐 تجربة النظام مباشرة

### 👁️ AIN | Streamlit

يمكن تجربة الواجهة مباشرة من خلال:

**[🚀 فتح تطبيق عين (AIN)](https://ainchild.streamlit.app/)**

---

## 🎯 فكرة المشروع

يعتمد **AIN** على نموذج اللغة العربي **MARBERTv2** لتحليل الرسائل العربية وتصنيفها إلى:

* 🟢 **Safe** — رسالة آمنة
* 🔴 **Risky** — رسالة تحتوي على محتوى مقلق أو خطِر

بعد التصنيف، يقوم النظام بتحويل درجة الخطورة إلى مستوى واضح يساعد في تحديد الإجراء المناسب.

الهدف من النظام هو المساعدة في اكتشاف أنماط مثل:

* التنمر الإلكتروني
* الإساءة اللفظية
* خطاب الكراهية
* المحتوى العدائي أو المسيء
* الرسائل التي قد تشكل خطرًا على الطفل أو المراهق

---

## ✨ أهم مميزات AIN

### 🤖 تحليل الرسائل باستخدام الذكاء الاصطناعي

يستخدم المشروع **MARBERTv2**، وهو نموذج متخصص في معالجة اللغة العربية، لتحليل محتوى الرسائل.

### 📊 Risk Score

كل رسالة تحصل على:

* `risk_score`
* `safe_score`
* `label`
* `severity`
* `should_alert`

وبذلك لا يكتفي النظام بقول إن الرسالة خطرة أو آمنة، بل يعطي **درجة ومستوى للخطورة**.

### 🚦 مستويات الخطورة

| المستوى   |   `risk_score` | الإجراء           |
| --------- | -------------: | ----------------- |
| 🟢 SAFE   |  أقل من `0.30` | لا يوجد تنبيه     |
| 🟡 LOW    | `0.30 – <0.50` | مراقبة            |
| 🟠 MEDIUM | `0.50 – <0.75` | مستوى خطورة متوسط |
| 🔴 HIGH   |       `≥ 0.75` | إنشاء تنبيه       |

---

## 🚨 نظام التنبيهات

عند وصول الرسالة إلى مستوى **HIGH**، يقوم النظام بإنشاء Alert.

إذا كان ولي الأمر مسجلاً، يتم إرسال بيانات التنبيه إلى **n8n** عبر Webhook، ليتم تنفيذ عملية الإشعار، مثل إرسال بريد إلكتروني إلى ولي الأمر.

```text
Message
   │
   ▼
MARBERTv2
   │
   ▼
Risk Score
   │
   ▼
Risk Engine
   │
   ├── SAFE / LOW / MEDIUM
   │
   └── HIGH
         │
         ▼
       Alert
         │
         ▼
        n8n
         │
         ▼
 Parent Notification
```

---

## ⏱️ Feedback Cooldown

يحتوي النظام أيضًا على نظام **Feedback Cooldown** لمنع إرسال عدد كبير من الملاحظات المتكررة خلال فترة زمنية قصيرة.

يتم تطبيق فترة التهدئة على مستوى المستخدم وفق آلية التعريف المستخدمة في النظام، بدل الاعتماد على جلسة محادثة مؤقتة فقط.

---

## 👨‍👩‍👧 Parent Setup

يوفر النظام صفحة مخصصة لتسجيل ولي الأمر.

يمكن لولي الأمر إدخال:

* البريد الإلكتروني
* الاسم بشكل اختياري

ثم يتم ربط بيانات ولي الأمر بالمحادثة/المستخدم وفق آلية النظام، حتى يتمكن النظام من إرسال التنبيهات عند اكتشاف حالات عالية الخطورة.

---

## 💬 Live Demo

تتيح واجهة **Live Demo** تجربة النظام بشكل مباشر.

يمكن إرسال رسالة عربية ومشاهدة نتيجة التحليل، بما في ذلك:

```text
Label
Risk Score
Safe Score
Severity
Alert Status
```

وهذا يسمح بعرض طريقة عمل نموذج الذكاء الاصطناعي بشكل تفاعلي.

---

## 📊 Dashboard

يحتوي النظام على لوحة تحكم لمتابعة حالة النظام والرسائل والتنبيهات.

يمكن من خلالها متابعة معلومات مثل:

* عدد الرسائل التي تم تحليلها
* عدد حالات الخطورة
* الحالات عالية الخطورة
* أعلى Risk Score
* التنبيهات
* حالة التنبيه

كما تم تحسين طريقة جلب بيانات الـ Dashboard لتقليل عدد طلبات الـ API وتحسين الأداء.

---

## 🧠 النموذج المستخدم

### MARBERTv2

النموذج الأساسي:

**UBC-NLP/MARBERTv2**

وهو نموذج مبني لمعالجة اللغة العربية ويُستخدم في المشروع لتحليل وتصنيف الرسائل.

النموذج المدرّب للمشروع:

**HazmehAlshraah/marbert-risk-model**

ويتم تحميل النموذج عند الحاجة واستخدامه لتحليل الرسائل العربية.

### نتائج النموذج

| Metric         | Result |
| -------------- | -----: |
| Accuracy       |  91.3% |
| Recall – Risky |    95% |
| F1 – Safe      |   0.91 |
| F1 – Risky     |   0.91 |

> تم الحصول على هذه النتائج على مجموعة اختبار مستقلة، وهي تعكس أداء النموذج على بيانات التقييم المستخدمة في المشروع.

---

## 📚 البيانات المستخدمة

تم دمج عدة مصادر للبيانات العربية بهدف تدريب نموذج قادر على التعامل مع أنواع مختلفة من المحتوى الخطِر.

من المصادر المستخدمة:

* **ArbCyD** — بيانات التنمر الإلكتروني العربي
* **Arabic Offensive Comment Detection**
* **Egyptian Arabic Hate Speech**

تم توحيد التصنيفات إلى فئتين رئيسيتين:

```text
Safe
Risky
```

ثم استخدام البيانات في عملية تدريب وتقييم النموذج.

---

# 🏗️ Architecture

يتكون النظام من عدة أجزاء رئيسية:

```text
                    ┌──────────────────┐
                    │    Streamlit     │
                    │   User Interface │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │      FastAPI     │
                    │       API        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    MARBERTv2     │
                    │   NLP Model      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Risk Engine    │
                    └────────┬─────────┘
                             │
                    ┌────────┴─────────┐
                    ▼                  ▼
             ┌─────────────┐    ┌─────────────┐
             │  Database   │    │    Alert    │
             │ PostgreSQL  │    │   System    │
             └─────────────┘    └──────┬──────┘
                                       │
                                       ▼
                                    ┌──────┐
                                    │ n8n  │
                                    └──┬───┘
                                       │
                                       ▼
                                Parent Notification
```

---

# 📁 Project Structure

```text
AIN/
│
├── ain/
│   ├── model/
│   │   └── MARBERT model loading & inference
│   │
│   ├── Risk/
│   │   └── Engine.py
│   │
│   ├── alerts/
│   │   └── Alert logic & cooldown
│   │
│   ├── database/
│   │   └── SQLAlchemy models & repositories
│   │
│   └── notifications/
│       └── n8n integration
│
├── api/
│   ├── main.py
│   ├── schemas.py
│   └── routes/
│       ├── analyze.py
│       ├── parents.py
│       ├── dashboard.py
│       ├── alerts.py
│       └── feedback.py
│
├── app/
│   ├── Home.py
│   │
│   ├── pages/
│   │   ├── live_demo.py
│   │   ├── dashboard.py
│   │   ├── parent_setup.py
│   │   └── feedback.py
│   │
│   ├── components/
│   │   ├── sidebar.py
│   │   └── risk_indicator.py
│   │
│   └── services/
│       └── api_client.py
│
├── Data/
│   └── Training datasets
│
├── notebooks/
│   └── AIN_Training.ipynb
│
├── tests/
│   └── Automated tests
│
├── .devcontainer/
│   └── Codespaces configuration
│
├── requirements.txt
└── README.md
```

---

# ⚙️ Technologies

| Technology                | الاستخدام                     |
| ------------------------- | ----------------------------- |
| **Python**                | لغة البرمجة الأساسية          |
| **MARBERTv2**             | تحليل وتصنيف النصوص العربية   |
| **PyTorch**               | تشغيل النموذج                 |
| **Transformers**          | تحميل وتشغيل MARBERTv2        |
| **FastAPI**               | Backend API                   |
| **Pydantic**              | API schemas & validation      |
| **SQLAlchemy**            | التعامل مع قاعدة البيانات     |
| **PostgreSQL / Supabase** | تخزين البيانات                |
| **Streamlit**             | واجهة المستخدم والـ Dashboard |
| **n8n**                   | أتمتة إرسال التنبيهات         |
| **pytest**                | اختبار النظام                 |
| **GitHub Codespaces**     | بيئة التطوير                  |

---

# 🚀 تشغيل المشروع محليًا

## 1. Clone

```bash
git clone https://github.com/HamzehAlshraah/AIN.git
cd AIN
```

## 2. إنشاء البيئة الافتراضية

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

## 3. تثبيت المتطلبات

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

أنشئ ملف `.env` في جذر المشروع.

مثال:

```env
API_BASE_URL=http://localhost:8000
N8N_WEBHOOK_URL=your_n8n_webhook_url

DATABASE_URL=your_database_url
```

> لا تقم برفع ملف `.env` أو أي مفاتيح سرية إلى GitHub.

---

# ▶️ تشغيل الـ Backend

```bash
uvicorn api.main:app --reload --port 8000
```

بعد التشغيل يمكن الوصول إلى:

```text
http://localhost:8000
```

وتوثيق الـ API:

```text
http://localhost:8000/docs
```

---

# ▶️ تشغيل Streamlit

في Terminal آخر:

```bash
streamlit run app/Home.py
```

سيعمل التطبيق عادةً على:

```text
http://localhost:8501
```

### النسخة المنشورة

يمكن تجربة النسخة المنشورة مباشرة:

**https://ainchild.streamlit.app/**

---

# ☁️ GitHub Codespaces

تم إعداد المشروع للعمل داخل **GitHub Codespaces** باستخدام:

```text
.devcontainer/
```

ويتم تجهيز بيئة التطوير والمكتبات المطلوبة تلقائيًا.

---

# 🔌 API

جميع API endpoints تستخدم:

```text
/api/v1
```

مع استثناء:

```text
/health
```

### أهم endpoints

| Method | Endpoint                    | الوظيفة            |
| ------ | --------------------------- | ------------------ |
| GET    | `/health`                   | فحص حالة API       |
| POST   | `/api/v1/analyze`           | تحليل رسالة        |
| POST   | `/api/v1/parents`           | تسجيل ولي الأمر    |
| GET    | `/api/v1/dashboard/summary` | إحصائيات Dashboard |
| GET    | `/api/v1/alerts`            | عرض التنبيهات      |
| PATCH  | `/api/v1/alerts/{id}`       | تحديث حالة التنبيه |
| POST   | `/api/v1/feedback`          | إرسال Feedback     |

---

# 🧪 Testing

يستخدم المشروع **pytest** لاختبار مكونات النظام.

لتشغيل الاختبارات:

```bash
pytest tests/ -v
```

وتشمل الاختبارات أجزاء مثل:

* API
* Database
* Alert system
* Risk logic
* Feedback
* Cooldown
* Notifications

---

# 🔄 Workflow

الـ workflow الأساسي للنظام:

```text
User Message
     │
     ▼
Streamlit
     │
     ▼
FastAPI
     │
     ▼
MARBERTv2
     │
     ▼
Classification
     │
     ▼
Risk Score
     │
     ▼
Risk Engine
     │
     ├───────────────┐
     │               │
     ▼               ▼
Normal          High Risk
                     │
                     ▼
                   Alert
                     │
                     ▼
                    n8n
                     │
                     ▼
             Parent Notification
```

---

# 🔒 Privacy & Safety

AIN يتعامل مع بيانات مرتبطة بسلامة الأطفال، لذلك يجب التعامل مع البيانات بحذر.

في بيئة الإنتاج يجب:

* حماية بيانات المستخدمين.
* عدم تخزين بيانات حساسة دون حاجة.
* حماية مفاتيح API وWebhooks.
* عدم رفع ملفات `.env` إلى GitHub.
* تحديد صلاحيات الوصول إلى Dashboard.
* توضيح للمستخدمين ما الذي تتم مراقبته وكيف تتم معالجة البيانات.

---

# ⚠️ Disclaimer

AIN هو **نظام مساعد للكشف عن المحتوى المقلق** وليس نظامًا قادرًا على تحديد الخطر بشكل مثالي.

قد تحدث:

* False Positives
* False Negatives

لذلك لا يجب الاعتماد على النظام وحده في القرارات المتعلقة بسلامة الطفل، ويجب أن يبقى الإشراف البشري والتواصل الأسري جزءًا أساسيًا من عملية الحماية.

---

# 🎓 Project Purpose

تم تطوير **AIN** كمشروع في مجال:

* Artificial Intelligence
* Natural Language Processing
* Arabic NLP
* Machine Learning
* Child Digital Safety
* Real-Time Risk Detection
* Automated Notifications

ويجمع المشروع بين **Machine Learning Model + Backend API + Database + Web Interface + Automation Workflow** في نظام واحد متكامل.

---

## 👁️ AIN

**عين — لأن حماية الطفل تبدأ من الانتباه.**

🚀 **[تجربة AIN مباشرة على Streamlit](https://ainchild.streamlit.app/)**

💻 **[GitHub Repository](https://github.com/HamzehAlshraah/AIN)**

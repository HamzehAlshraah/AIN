<div align="center">

# 👁️ AIN | عين

### نظام ذكاء اصطناعي لكشف الرسائل الخطرة الموجّهة للأطفال باللغة العربية

مبني على نموذج **MARBERTv2** لفهم اللهجات والفصحى العربية، لحماية الأطفال من الاستغلال والتحرش والمحتوى الخطر أثناء المحادثات الرقمية.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Transformers](https://img.shields.io/badge/🤗%20Transformers-MARBERTv2-yellow)](https://huggingface.co/UBC-NLP/MARBERTv2)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#-الترخيص)

</div>

---

## 📖 نظرة عامة

**AIN (عين)** هو نظام ذكاء اصطناعي مخصّص للغة العربية، يهدف إلى رصد وكشف الرسائل الخطرة أو المشبوهة الموجّهة للأطفال في بيئات المحادثة الرقمية (تطبيقات الدردشة، الألعاب، المنصات التعليمية، إلخ).

يعتمد المشروع على نموذج **[MARBERTv2](https://huggingface.co/UBC-NLP/MARBERTv2)**، وهو نموذج BERT مدرّب خصيصًا على اللهجات العربية المختلفة والفصحى، مما يمنحه قدرة أفضل على فهم السياق العربي مقارنة بالنماذج متعددة اللغات التقليدية.

> ⚠️ الاسم "عين" (AIN) يرمز إلى فكرة المشروع: **عين ساهرة** ترصد المحتوى الخطر وتنبّه قبل وقوع الضرر.

---

## ✨ أبرز الميزات

- 🧠 **تصنيف النصوص العربية** باستخدام نموذج MARBERTv2 المُدرّب مسبقًا (Fine-tuned) على بيانات مخصّصة لكشف الرسائل الخطرة.
- 💬 **واجهة تجريبية تفاعلية** مبنية بـ Streamlit لتجربة النموذج مباشرة عبر محادثة حية.
- ⚙️ **خدمة API** مبنية بـ FastAPI لإتاحة النموذج كخدمة قابلة للتكامل مع تطبيقات أخرى.
- 🗄️ **دعم قواعد بيانات متعددة**: PostgreSQL و MongoDB لتخزين المحادثات والنتائج.
- 🔄 **معالجة غير متزامنة** للمهام الثقيلة باستخدام Celery و Redis (مع لوحة مراقبة Flower).
- 📓 **دفتر تدريب (Notebook)** موثّق يشرح خطوات تجهيز البيانات وتدريب وتقييم النموذج.

---

## 🏗️ التقنيات المستخدمة

| الفئة | التقنيات |
|---|---|
| النموذج / معالجة اللغة | `transformers`, `torch`, MARBERTv2 |
| الواجهة الخلفية (API) | `FastAPI`, `uvicorn`, `pydantic` |
| الواجهة التفاعلية | `streamlit` |
| قواعد البيانات | `PostgreSQL` (`psycopg2-binary`, `SQLAlchemy`), `MongoDB` (`motor`, `pymongo`) |
| المهام غير المتزامنة | `celery`, `redis`, `flower` |
| أدوات مساعدة | `langchain`, `openai`, `gspread`, `google-auth`, `python-dotenv` |

---

## 📂 هيكل المشروع

```
AIN/
├── .devcontainer/          # إعدادات بيئة التطوير (Dev Container)
├── Data/                   # مجموعات البيانات المستخدمة في التدريب والتقييم
├── AIN.ipynb               # دفتر تدريب وتقييم النموذج
├── streamlit_chat_app.py   # واجهة الدردشة التجريبية (Streamlit)
├── requirements.txt        # الاعتماديات المطلوبة للمشروع
└── README.md
```

---

## 🚀 التثبيت والتشغيل

### المتطلبات الأساسية

- Python 3.10 أو أحدث
- (اختياري) وصول إلى GPU لتسريع الاستدلال/التدريب
- حسابات/مفاتيح خدمات خارجية إن استُخدمت (مثل OpenAI) — تُضاف في ملف `.env`

### 1. استنساخ المستودع

```bash
git clone https://github.com/HamzehAlshraah/AIN.git
cd AIN
```

### 2. إنشاء بيئة افتراضية وتثبيت الاعتماديات

```bash
python -m venv venv
source venv/bin/activate      # على Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 3. إعداد متغيرات البيئة

أنشئ ملف `.env` في جذر المشروع وأضف المتغيرات اللازمة (مثل مفاتيح API وروابط قواعد البيانات):

```env
OPENAI_API_KEY=your_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/ain
MONGODB_URI=mongodb://localhost:27017/ain
```

### 4. تشغيل واجهة التجربة (Streamlit)

```bash
streamlit run streamlit_chat_app.py
```

### 5. استكشاف التدريب والتقييم

افتح دفتر `AIN.ipynb` عبر Jupyter أو Google Colab لاستعراض خطوات تجهيز البيانات، ضبط النموذج (Fine-tuning)، وتقييم الأداء.

```bash
jupyter notebook AIN.ipynb
```

---

## 🧠 عن النموذج: MARBERTv2

[MARBERTv2](https://huggingface.co/UBC-NLP/MARBERTv2) هو نموذج BERT من تطوير فريق UBC-NLP، مدرّب على كميات ضخمة من النصوص العربية الفصحى واللهجات، مما يجعله مناسبًا لمهام معالجة اللغة الطبيعية في السياق العربي مثل:

- تصنيف النصوص (Text Classification)
- كشف المحتوى الضار (Harmful Content Detection)
- تحليل المشاعر (Sentiment Analysis)

في هذا المشروع، تم ضبط النموذج (Fine-tuning) على بيانات مخصّصة لتمييز الرسائل الخطرة الموجّهة للأطفال عن الرسائل العادية.

---

## 🤝 المساهمة

المساهمات مرحّب بها لتطوير المشروع وتحسين دقته! يمكنك:

1. عمل Fork للمستودع.
2. إنشاء فرع جديد للميزة أو الإصلاح: `git checkout -b feature/amazing-feature`
3. حفظ التعديلات: `git commit -m 'إضافة ميزة جديدة'`
4. رفع الفرع: `git push origin feature/amazing-feature`
5. فتح Pull Request.

---

## ⚖️ إخلاء مسؤولية

هذا المشروع أداة مساعدة لرصد المحتوى الخطر، وليس بديلًا عن الإشراف الأبوي أو الجهات المختصة بحماية الطفل. يُنصح باستخدامه كطبقة حماية إضافية ضمن منظومة أوسع للأمان الرقمي للأطفال.

---

## 📄 الترخيص

هذا المشروع مرخّص بموجب [رخصة MIT](LICENSE) ما لم يُذكر خلاف ذلك.

---

## 👤 التواصل

**Hamzeh Alshraah**
GitHub: [@HamzehAlshraah](https://github.com/HamzehAlshraah)

---

<div align="center">

إذا أعجبك المشروع، لا تنسَ ترك ⭐ على المستودع!

</div>

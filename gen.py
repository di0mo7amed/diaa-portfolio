#!/usr/bin/env python3
"""Builds Diaa Mohammed's portfolio: English at the root, Arabic in /ar/.
   Edit the CONTENT section, then run:  python3 gen.py
   Output: ./site (upload this folder) and ./preview (used for the Claude preview)."""
import os, re, shutil, html

ROOT = os.path.dirname(os.path.abspath(__file__))
e = html.escape

# =========================== CONTENT ===========================
IMG = "https://framerusercontent.com/images/"
LOGO = IMG + "ZfnO7ta8aoFz20nDWkANMwvxi4Q.svg"
HERO = IMG + "nM1lDMjBbvvURGFVf5IMB4aZT8.png?scale-down-to=1600"
PORTRAIT = IMG + "9MXsp1yQQX8ctlfxudylN9onQ.png?scale-down-to=1200"
ME = "img/me.webp"  # high-res portrait shipped with the site
EMAIL = "dioo.zone@gmail.com"
BEHANCE = "https://www.behance.net/diaamohammed4"
INSTAGRAM = "https://instagram.com/dio.zone"
LINKEDIN = "https://www.linkedin.com/in/diaamu/"
CV = "https://drive.google.com/file/d/1cXgFfKuSHwqX7aolbv007TA7rz6kGjKG/view?usp=sharing"
TALLY = "https://tally.so/embed/BzeA0e?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1"
TALLY_PAGE = "https://tally.so/r/BzeA0e"

# Images: the hosted site loads full-quality files from Framer's CDN; the Claude preview uses small local copies in img/.
_MODE = {"preview": False, "pre": ""}
def pic(local, remote):
    if _MODE["preview"] and os.path.exists(os.path.join(ROOT, "img", local)):
        return _MODE["pre"] + "img/" + local
    return remote
def jpg(i, w=1024): return pic(f"post-{i}.webp", f"{IMG}{i}.jpg?scale-down-to={w}")
COVERS = {"hbbah": "7rVuSUwD8Q0lEVl7BzpSvbpgXU", "avenue": "EOjMDlGAq5kJv7k4tFHrlmlY", "watsio": "FPgJVWIGSlZmTsytmdNiUvXlWm0",
          "2care": "eyxrTUyCrrMIKVJdlmLfokbUziw", "sahlcart": "0jPCQTkadPMl3ewAYEFtZhoTo", "growvo": "4uBjl1WcxwWH6CFIuK0e7GkLamE",
          "holidaytime": "Z5GxoPsLdD5LgMgCqdak56QYHA", "toycastle": "FOlgOmZRAOpESUq1O4JUtjeB5s"}
def cover_(slug, w=1024):
    if _MODE["preview"] and os.path.exists(os.path.join(ROOT, "img", f"{slug}.webp")): return _MODE["pre"] + f"img/{slug}.webp"
    return img_url(COVER_URL.get(slug, ""), w)
def hero_img(): return pic("portrait.webp", HERO)
def plus(n): return n[:-1] + '<span class="plus">+</span>' if n.endswith('+') else n

# Every text is (English, Arabic)
NAME = ("Diaa Mohammed", "ضيَــاء مُحمد")
NAME_LINES = (("Diaa", "Mohammed"), ("ضيَــاء", "مُحمد"))
TAGLINE = ("Design colors life.", "التصميمُ يلوِّن الحياة.")
TAGLINE_MARK = ('Design <span class="mark-draw">colors</span> life.', 'التصميمُ <span class="mark-draw">يلوِّن</span> الحياة.')
TAGLINE_HTML = ('Design <span class="red">colors</span> life.', 'التصميمُ <span class="red">يلوِّن</span> الحياة.')
LEAD = ("I design visual identities and ad campaigns that give your brand a voice of its own, and a presence people remember.",
        "أصمّم هويات بصرية وحملات إعلانية تمنح علامتك صوتًا يميّزها، وحضورًا يبقى في الذهن.")

HOME_STATS = [("15+", ("Projects delivered", "مشروع منفَّذ")), ("3+", ("Years of experience", "سنوات خبرة")),
              ("4+", ("Countries designed for", "دول صممت لها")), ("20+", ("Brands", "علامة تجارية"))]

SERVICES = [("Branding", "الهويات البصرية"), ("Campaigns", "الحملات الإعلانية"), ("Social Media", "السوشيال ميديا"), ("Art Direction", "التوجيه الفني")]

PROCESS = [
    (("Listen", "الإنصات"), ("Every project starts with understanding the brand, its audience and the goal behind the brief. Good design starts with good questions.",
                            "يبدأ كل مشروع بفهم العلامة وجمهورها والهدف من ورائها. التصميم الجيد يبدأ بأسئلة جيدة.")),
    (("Direction", "الاتجاه"), ("We explore several creative routes, test them against the goal, and commit to the one that says the most.",
                               "نستكشف أكثر من اتجاه إبداعي، نختبرها أمام الهدف، ثم نختار الاتجاه الأقوى.")),
    (("Craft", "الصناعة"), ("The idea becomes a system: logo, color, type, layouts and templates that hold together everywhere the brand appears.",
                           "تتحول الفكرة إلى منظومة: شعار، ألوان، خطوط، وقوالب متّسقة في كل مكان تظهر فيه العلامة.")),
    (("Deliver", "التسليم"), ("Clean files, a clear guide, and support while the work goes live.",
                             "ملفات مرتبة، ودليل واضح، ومتابعة حتى ينطلق العمل.")),
]

# TODO(Diaa): review these answers
FAQ = [
    (("What kind of projects do you take on?", "ما نوع المشاريع التي تعمل عليها؟"),
     ("Visual identities (logo, color and type systems, brand guidelines) and ad campaigns and social content, mostly for restaurants, retail and service brands.",
      "الهويات البصرية المتكاملة (الشعار، نظام الألوان والخطوط، ودليل العلامة) والحملات الإعلانية ومحتوى السوشيال ميديا، خاصة لقطاعات المطاعم والتجزئة والخدمات.")),
    (("Do you work with agencies or directly with brands?", "هل تعمل مع الوكالات أم مع العلامات مباشرة؟"),
     ("Both. I work directly with brands, and with agencies and studios as part of their team.",
      "الاثنين. أعمل مع العلامات التجارية مباشرة، ومع الوكالات والاستوديوهات كجزء من فريقها.")),
    (("How do you start a project?", "كيف تبدأ أي مشروع؟"),
     ("By listening. I learn the brand, its audience and its goal before designing anything, then set a visual direction and move to execution.",
      "بالإنصات. أفهم العلامة وجمهورها وهدفها قبل أي تصميم، ثم أضع الاتجاه البصري وأنتقل للتنفيذ.")),
    (("Which markets and languages do you work in?", "في أي أسواق ولغات تعمل؟"),
     ("Egypt, Saudi Arabia, Kuwait and the UAE, in Arabic and English. My work has reached over 50 countries.",
      "مصر والسعودية والكويت والإمارات، بالعربية والإنجليزية، وامتدّ أثر أعمالي إلى أكثر من خمسين دولة.")),
    (("How do we start working together?", "كيف نبدأ العمل معًا؟"),
     ("Fill in the contact form or email me with a short brief, and I'll reply to agree on scope and timeline.",
      "املأ نموذج التواصل أو راسلني بنبذة عن مشروعك، وسأرد عليك لنتفق على التفاصيل والجدول الزمني.")),
    (("How long does a project usually take?", "كم يستغرق المشروع عادةً؟"),
     ("It depends on scope. A campaign takes less time than a full identity. We agree on the timeline before we start.",
      "يختلف حسب الحجم؛ الحملة تأخذ وقتًا أقل من هوية كاملة. نتفق على المدة قبل البدء.")),
]

STORY = [
    ("Before I knew what I did had a name, design was my first language.", "قبل أن أعرف أن لِما أفعله اسمًا، كان التصميم لغتي الأولى."),
    ("As a child, talking wasn't my easiest way through. Among my mother's notebooks I found planners she had filled with magazine cut-outs: pictures and colors arranged with care. That was the first thing that pulled me in: taking scattered things and arranging them until they said something. That's where I learned that shape and color can say what words can't.",
     "في طفولة لم يكن الكلام فيها طريقي الأسهل، وجدت بين دفاتر أمي أجندات ملأتها بقصاصات من المجلات؛ صور وألوان مرتَّبة بعناية. كان ذلك أول ما استهواني: أن آخذ أشياء متفرّقة وأعيد ترتيبها حتى تقول شيئًا. هناك تعلّمت أن ما يعجز عنه القول قد يقوله الشكل واللون."),
    ("I started on an old, modest computer, teaching myself step by step. Over time that quiet curiosity became a craft: turning an abstract idea into something people can see and feel, and giving a brand an identity and a voice that don't get lost.",
     "بدأت على حاسوب قديم متواضع، أعلّم نفسي بنفسي، خطوة تتبعها خطوة. ومع الوقت تحوّل ذلك الفضول الصامت إلى حرفة: أن أحوّل فكرة مجرّدة إلى شيء يراه الناس ويشعرون به، وأن أمنح العلامة هوية وصوتًا لا يضيعان وسط ما حولهما."),
    ("“Design colors life” isn't a slogan I picked. It's what I lived. Color, to me, isn't decoration. It's meaning and spirit added to the ordinary so it leaves a mark.",
     "«التصميم يلوّن الحياة» ليس شعارًا اخترته؛ هي ما عشته. اللون عندي ليس زينة، بل معنى و روح تُضاف إلى ما هو عادي فيصير له أثر يبقى."),
    ("Today, at nineteen, I'm an independent designer in visual identity and advertising, working with brands and agencies across Egypt and the Gulf, with work that has reached more than fifty countries. What matters to me in every project hasn't changed since those notebooks: listen well, then give the idea the shape that makes it seen, and felt.",
     "اليوم، وأنا في التاسعة عشرة، أعمل مصمّمًا مستقلًّا في الهوية البصرية والحملات الإعلانية، مع علامات ووكالات في مصر والخليج، وامتدّ أثر أعمالي إلى أكثر من خمسين دولة. لكن ما يهمّني في كل مشروع لم يتغيّر منذ تلك الدفاتر: أن أنصِت جيدًا، ثم أمنح الفكرة شكلها الذي يجعلها تُرى، وتُحَسّ."),
]
ABOUT_STATS = [("1.6K+", ("Appreciations from designers", "إعجاب من مصمّمين")), ("50+", ("Countries reached", "دولة حول العالم")),
               ("920K+", ("Behance reach", "وصول أعمالي على Behance"))]
JOBS = [
    (("Aug 2025 – Jun 2026", "أغسطس ٢٠٢٥ – يونيو ٢٠٢٦"), "Hbbah Studio", ("Brand & Social Designer · Saudi Arabia", "مصمم هويات ومحتوى سوشيال · السعودية"),
     ("Full identities and social content for Saudi clients across restaurants, retail and services: from logo, color and type to brand guidelines. I also direct product and food photography to keep every touchpoint consistent.",
      "أصمّم هويات متكاملة ومحتوى سوشيال لعملاء في السعودية عبر قطاعات المطاعم والتجزئة والخدمات: من الشعار ونظام الألوان والخطوط إلى دليل العلامة، وأتولّى توجيه تصوير المنتجات والأطعمة.")),
    (("2024 – Now", "٢٠٢٤ – الآن"), ("Independent Brand Designer", "مصمم هويات مستقل"), ("Remote · Egypt, KSA, Kuwait, UAE", "عن بُعد · مصر، السعودية، الكويت، الإمارات"),
     ("End-to-end identity projects from strategy to application, specialised in restaurants and services.",
      "مشاريع هوية كاملة من الاستراتيجية حتى التطبيق، بتخصّص في قطاع المطاعم والخدمات.")),
]
VOLUNTEER = [
    (("2025", "٢٠٢٥"), "STAI", ("Volunteer Social Media Designer", "مصمم سوشيال ميديا متطوّع"),
     ("Led a visual redesign of the student initiative and built banners, posts and templates for online events.", "قُدت إعادة تصميم بصرية للمبادرة الطلابية، وأنشأت بانرات ومنشورات وقوالب للفعاليات الإلكترونية.")),
    (("Dec 2024 – 2025", "ديسمبر ٢٠٢٤ – ٢٠٢٥"), "Skills Area", ("Brand Designer", "مصمم علامة بصرية"),
     ("Designed consistent visuals for educational posts and helped define the academy's first identity.", "صمّمت محتوى بصريًا متّسقًا للمنشورات التعليمية، وساهمت في تحديد ملامح الهوية البصرية الأولى للأكاديمية.")),
    (("Feb – Dec 2023", "فبراير – ديسمبر ٢٠٢٣"), "Sunrise Academy", ("Identity & Visual Content Designer", "مصمم هويات ومحتوى بصري"),
     ("Directed the visual style of educational events with a consistent identity across platforms.", "وجّهت الأسلوب البصري للفعاليات التعليمية، وقدّمت هوية متّسقة عبر المنصّات.")),
    (("Feb – Jun 2023", "فبراير – يونيو ٢٠٢٣"), ("SBS – Youth Helping Youth", "SBS – شباب بتساعد شباب"), ("Identity & Visual Content Designer", "مصمم هويات ومحتوى بصري"),
     ("Campaigns and social content for young audiences, plus print matching the initiative's identity.", "طوّرت حملات ومحتوى سوشيال موجّه للشباب، وصمّمت مطبوعات متّسقة مع هوية المبادرة.")),
]
TOOLS = [("Photoshop", "Adobe"), ("Illustrator", "Adobe"), ("After Effects", "Adobe"), ("Audition", "Adobe"), ("Media Encoder", "Adobe"),
         ("Figma", "Design"), ("Framer", "Web"), ("Canva", "Design"), ("CapCut", "Video")]

HB_POSTS = ["jI3pMKerNpIp8q6kO3SEBfvhSug", "fR1tu968lLq8Nz3x15oB3Pfg", "Y2D0KlalLyqLPe0AeE7b2loTA"]
HB_CAR = ["Nh2AcXQ2AGDG4QVpbP3JusQ6WU", "Z1FV065smOUHyfgl33fOByPMPCE", "ZtdfHDq8Dymv4GS8HMgcSg1SU", "OTluSAu9bBihwDUGUfmx2JC0Eg8",
    "2xBJnU9rr9A0EIxSXH3eJ5X4xg0", "8xaAG4uxeQz6dGNEMO6G6q42Cu8", "HnhvIFuox4axlW1Jpb5qX42N0g", "ctePNEhG45v29GKSR15lSTYc", "901TYnFPH6cGT1baVTI9uaCFQ",
    "74xfAl675DxsNuniGcV9mpmzM", "ytjIsR3ePn96KjDs0ONjMlbePqA", "hZY1y3P4OrNHpLQrGYwgrNymE0", "ttXugJj8ZtWYTFPowq0xC9GQt4", "vE81sBE7ES9y4FZ7mLALwMx9M",
    "10cT1w5tOyu3SEygYCSJlqEM4I", "CLPoucfzk4zwWAvHVIxWWWuk3so", "NQianXPAPIcY7sToTlaPOwhjN1c", "WVxhcc26gEYChcUyiN6w7X87ZSE", "eXTViTVRPXkRin9EySu2XuM",
    "noNOTbH36Bru8jNSQGB1FgmqUc", "pcFpPmNfcvLxhZUTNb6hps5u6g", "lS38GTAhZQCOX0WgVp6uFCFOnKw", "kmuAneRHI82Ms77zlhlOO0gSgo", "j9anewUwbHHjz43uc81lm2eOyAE",
    "8HVd9ovVjUvQcpfka9NA8px34L0", "LaWlkSvgSkBoc7EFGxTN7HGfPDI", "6DiiL47hDuejQ0JGH2eY40ookQ"]

# Case study for Hbbah. TODO(Diaa): everything below marked SAMPLE is placeholder text.
HBBAH = dict(
    desc=("A content system for a Saudi growth firm that helps companies redesign their revenue model. We made finance feel clear, confident and human.",
          "نظام محتوى لشركة سعودية في تطوير الأعمال تساعد الشركات على إعادة تصميم نموذجها الربحي. جعلنا عالم الأرقام يبدو واضحًا وواثقًا وقريبًا من الناس."),
    meta=[(("Services", "الخدمات"), ("Art Direction, Social Content", "توجيه فني، محتوى سوشيال")), (("Client", "العميل"), ("Hbbah", "هبَّة")),
          (("Country", "الدولة"), ("Saudi Arabia", "السعودية")), (("Duration", "المدة"), ("Jan – Feb 2026", "يناير – فبراير ٢٠٢٦")),
          (("Role", "دوري"), ("Lead Designer", "المصمم الرئيسي"))],
    overview_lede=("Hbbah turns messy revenue into a growth system. <em>Their feed needed to say that in three seconds.</em>",
                   "هبَّة تحوّل الإيرادات المبعثرة إلى منظومة نمو. <em>وكان على حسابهم أن يقول ذلك في ثلاث ثوانٍ.</em>"),
    overview=[("Hbbah works with founders and finance teams across the Gulf. Their expertise is deep, but their social presence looked like every other consultancy: stock photos, dense text and charts nobody stops for.",
               "تعمل هبَّة مع المؤسسين وفرق المالية في الخليج. خبرتهم عميقة، لكن حضورهم على السوشيال كان يشبه أي شركة استشارات: صور جاهزة، نصوص كثيفة، ورسوم بيانية لا يتوقف عندها أحد."),
              ("We built a visual language and a set of reusable templates so the team could publish every week without losing the brand.",
               "بنينا لغة بصرية ومجموعة قوالب قابلة لإعادة الاستخدام تتيح للفريق النشر أسبوعيًا دون أن تضيع هوية العلامة.")],
    challenge_lede=("How do you make revenue strategy exciting <em>without making it look cheap?</em>", "كيف تجعل استراتيجية الإيرادات ممتعة <em>دون أن تفقد جديتها؟</em>"),
    goals=[("Explain complex financial ideas at a glance", "شرح الأفكار المالية المعقّدة من نظرة واحدة"),
           ("Build trust with decision makers, not just likes", "بناء الثقة مع صنّاع القرار، لا الإعجابات فقط"),
           ("Give the in-house team templates they can reuse", "منح الفريق الداخلي قوالب يعيد استخدامها")],
    limits=[("No photography budget", "لا توجد ميزانية للتصوير"), ("Bilingual posts, Arabic first", "منشورات بلغتين، والعربية أولًا"),
            ("Weekly publishing from week two", "نشر أسبوعي بدءًا من الأسبوع الثاني")],
    idea_lede=("The idea: numbers as characters. <em>Every post gives one figure its own stage.</em>", "الفكرة: الأرقام كأبطال. <em>كل منشور يمنح رقمًا واحدًا مسرحه الخاص.</em>"),
    words=[("Confident", "واثق"), ("Clear", "واضح"), ("Momentum", "زخم"), ("Gulf-modern", "خليجي معاصر")],
    palette=[("#0E2A47", "#fff"), ("#1FB57A", "#fff"), ("#F2C14E", "#0E0E0E"), ("#F5F3EE", "#0E0E0E")],
    dirs=[(("Ledger", "الدفتر"), ("Grid paper and handwritten notes. Warm, but it read as an accounting firm.", "ورق مربعات وملاحظات بخط اليد. دافئ، لكنه بدا كمكتب محاسبة."), False, "#E4E2DC"),
          (("Big Number", "الرقم الكبير"), ("One oversized figure per post, framed by a short line of insight. Fast to read and easy to template.", "رقم واحد ضخم في كل منشور مع جملة قصيرة. سريع القراءة وسهل التحويل إلى قالب."), True, "#C9CFF2"),
          (("Motion", "الحركة"), ("Arrows and growth curves everywhere. Energetic, but too close to trading ads.", "أسهم ومنحنيات نمو في كل مكان. حيوي، لكنه اقترب من إعلانات التداول."), False, "#D5EBDD")],
    solution_lede=("Three post types and a carousel system, <em>all built on one grid.</em>", "ثلاثة أنواع من المنشورات ونظام كاروسل، <em>كلها على شبكة واحدة.</em>"),
    results=[(("Engagement", "التفاعل"), "+212%", ("Engagement rate in the first three months", "زيادة في معدل التفاعل خلال أول ثلاثة أشهر")),
             (("Saves", "الحفظ"), "4.6×", ("More saves per post than the old feed", "حفظ أكثر لكل منشور مقارنة بالسابق")),
             (("Leads", "العملاء"), "38", ("Inbound leads that came from social", "عميل محتمل جاء من السوشيال"))],
    quote=("“For the first time, our feed sounds like us. Clients quote our posts back to us in meetings.”", "«لأول مرة يشبهنا حسابنا. عملاؤنا يقتبسون منشوراتنا في الاجتماعات.»"),
    quote_by=("Founder, Hbbah", "المؤسس، هبَّة"),
    team=[(("Lead Designer", "المصمم الرئيسي"), ("Diaa Mohammed", "ضياء محمد"), True), (("Creative Director", "المدير الإبداعي"), ("Team member", "اسم عضو الفريق"), False),
          (("Copywriter", "كاتب المحتوى"), ("Team member", "اسم عضو الفريق"), False), (("Motion Designer", "مصمم موشن"), ("Team member", "اسم عضو الفريق"), False),
          (("Account Manager", "مدير الحساب"), ("Team member", "اسم عضو الفريق"), False)],
    deliverables=[("Visual language", "لغة بصرية"), ("Post templates", "قوالب المنشورات"), ("Carousel system", "نظام الكاروسل"), ("Usage guide", "دليل الاستخدام")],
)

# slug, name, field, year, category, tone, cover image id (or None), case study (or None)
PROJECTS = [
    ("hbbah", ("Hbbah", "هبَّة"), ("Business Growth", "تطوير الأعمال"), "2026", "social", "#C9CFF2", HB_POSTS[0], HBBAH),
    ("avenue", ("Avenue", "اڤينيو"), ("Marketing", "التسويق"), "2025", "social", "#F0D9C4", None, None),
    ("watsio", ("Watsio", "واتسيو"), ("SaaS", "SaaS"), "2025", "social", "#CFE7D8", None, None),
    ("2care", ("2Care", "تو كير"), ("Beauty", "تجميل"), "2025", "social", "#EBD3DC", None, None),
    ("sahlcart", ("Sahl Cart", "سهل كارت"), ("E-commerce", "متاجر إلكترونية"), "2025", "social", "#D6DCEB", None, None),
    ("growvo", ("Growvo", "جروڤو"), ("Marketing", "التسويق"), "2024", "social", "#E8E3C6", None, None),
    ("holidaytime", ("Holiday Time", "هوليداي تايم"), ("Travel", "سياحة"), "2024", "social", "#C9E2EC", None, None),
    ("toycastle", ("Toy Castle", "قلعة الألعاب"), ("Kids' Toys", "ألعاب الأطفال"), "2024", "social", "#F2DCC0", None, None),
]

# Swatch card per project (concept 5): strong chip colour + catalogue code
SWATCH = {"hbbah": ("#EB4B36", "DM-001", ("Coral", "مرجاني")), "avenue": ("#F26B3A", "DM-002", ("Apricot", "مشمشي")),
          "watsio": ("#F2552C", "DM-003", ("Signal", "إشارة")), "2care": ("#E8473F", "DM-004", ("Rose Red", "وردي أحمر")),
          "sahlcart": ("#F07A45", "DM-005", ("Clay", "طيني")), "growvo": ("#E5412D", "DM-006", ("Ember", "جمر")),
          "holidaytime": ("#F0603A", "DM-007", ("Sunset", "غروب")), "toycastle": ("#F28C38", "DM-008", ("Marigold", "قطيفة"))}

# Listen tool (concept 3): words a visitor can pick
LISTEN_WORDS = [("bold", ("Bold", "جريئة")), ("calm", ("Calm", "هادئة")), ("warm", ("Warm", "دافئة")), ("luxe", ("Luxe", "فاخرة")),
                ("playful", ("Playful", "مرحة")), ("clean", ("Clean", "نظيفة")), ("rooted", ("Rooted", "أصيلة")), ("tech", ("Techy", "تقنية"))]

# Filter tags per project (edit freely): social, campaigns, art, branding
TAGS = {"hbbah": "social campaigns art", "avenue": "social campaigns", "watsio": "social campaigns", "2care": "social art",
        "sahlcart": "social campaigns", "growvo": "social art", "holidaytime": "social campaigns", "toycastle": "social campaigns"}
FILTERS = [("all", ("All work", "كل الأعمال")), ("social", ("Social Media", "السوشيال ميديا")), ("campaigns", ("Campaigns", "الحملات الإعلانية")),
           ("art", ("Art Direction", "التوجيه الفني")), ("branding", ("Branding", "الهويات البصرية"))]
# Who you've worked with (credibility strip). TODO(Diaa): add or reorder names
CLIENTS = ["Hbbah Studio", "Hbbah", "Avenue", "Watsio", "2Care", "Sahl Cart", "Growvo", "Holiday Time", "Toy Castle", "Skills Area", "Sunrise Academy", "SBS", "STAI"]

UI = {
    "work": ("Work", "أعمالي"), "about": ("About", "من أنا"), "contact": ("Contact", "تواصل"), "home": ("Home", "الرئيسية"),
    "start": ("Start a project", "ابدأ مشروعك"), "cairo": ("Cairo, Egypt", "القاهرة، مصر"), "available": ("Available for work", "متاح للعمل"),
    "services": ("Services", "الخدمات"), "based": ("Based in", "المقر"), "selected": ("Selected work", "أعمال مختارة"),
    "all_work": ("All work", "كل الأعمال"), "numbers": ("In numbers", "بالأرقام"), "process": ("Process", "طريقة العمل"),
    "how": ("How I work", "كيف أعمل"), "faq": ("Questions", "أسئلة شائعة"), "faq_h": ("Good to know", "قبل أن نبدأ"),
    "ready": ("Ready to build your brand?", "جاهز لنبني علامتك معًا؟"), "lets": ("Let's talk", "لنتحدث"),
    "email": ("Email", "البريد"), "social": ("Social", "حسابات"), "rights": ("All rights reserved.", "جميع الحقوق محفوظة."),
    "local": ("Local time", "التوقيت المحلي"), "filter_all": ("All", "الكل"), "social_cat": ("Social Media", "سوشيال ميديا"),
    "branding_cat": ("Branding", "هويات بصرية"), "work_intro": ("I treat every campaign as a complete system: it starts with understanding the brand and its goal, and ends with considered designs that keep its character clear in people's minds. A selection of projects where I tried to balance idea, taste and impact.",
                                                            "أتعامل مع كل حملة باعتبارها منظومة متكاملة، تبدأ من فهم العلامة وهدفها، وتنتهي بتصاميم مدروسة تحافظ على شخصيتها وتتركها واضحة في ذهن من يراها. مجموعة مختارة حاولت فيها أن أوازن بين الفكرة والذوق والأثر."),
    "branding_more": ("Branding projects live on Behance", "مشاريع الهويات البصرية على Behance"),
    "story": ("My story with design", "حكايتي مع التصميم"), "exp": ("Experience", "الخبرة"), "vol": ("Volunteering", "التطوع والمشاركة"),
    "tools": ("Tools", "الأدوات"), "cv": ("Download CV", "السيرة الذاتية"), "stats": ("Stats", "إحصائيات"),
    "contact_h": ("Let's talk.", "يسعدني تواصلك."), "contact_intro": ("Tell me about your brand or your campaign, and I'll get back to you soon.", "احكيلي عن علامتك أو حملتك، وهرد عليك في أقرب وقت."),
    "copy": ("Copy email", "نسخ البريد"), "copied": ("Copied", "تم النسخ"), "form_alt": ("Form not showing?", "النموذج مش ظاهر؟"),
    "form_open": ("Open it in a new tab", "افتحه في صفحة مستقلة"), "back": ("All work", "كل الأعمال"), "info": ("Services & Info", "الخدمات والتفاصيل"),
    "overview": ("Overview", "نظرة عامة"), "challenge": ("Challenge", "التحدي"), "thinking": ("Creative thinking", "التفكير الإبداعي"),
    "solution": ("Solution", "الحل"), "results": ("Results", "النتائج"), "credits": ("Credits", "فريق العمل"),
    "goals": ("Goals", "الأهداف"), "limits": ("Constraints", "القيود"), "moodboard": ("Moodboard", "لوحة الإلهام"),
    "routes": ("Routes we explored", "اتجاهات جرّبناها"), "chosen": ("Chosen", "المختار"), "explored": ("Explored", "تجربة"),
    "posts": ("Posts", "المنشورات"), "carousels": ("Carousels", "الكاروسلز"), "carousel": ("Carousel", "كاروسل"), "slides": ("slides", "شرائح"),
    "deliv": ("Deliverables", "المخرجات"), "next": ("Next project", "المشروع التالي"), "soon": ("Full case study coming soon.", "دراسة الحالة الكاملة قريبًا."),
    "behance": ("View on Behance", "شاهد على Behance"), "close": ("Close", "إغلاق"), "prev": ("Prev", "السابق"), "nextb": ("Next", "التالي"),
    "lang": ("عربي", "English"), "lang_label": ("النسخة العربية", "English version"), "lang_word": ("العربية", "English"),
    "day": ("Daylight · dim the lights?", "نهار · نطفي النور؟"), "night": ("Lights low · switch on?", "الأضواء خافتة · نشغّلها؟"),
    "light_btn": ("Switch light", "بدّل الإضاءة"), "notebook": ("From the notebooks", "من الدفاتر"),
    "page01": ("Page 01 — scattered things, until they say something", "صفحة ٠١ — أشياء متفرّقة، حتى تقول شيئًا"),
    "arrange": ("Arrange", "رتّب"), "scatter": ("Scatter", "بعثر"), "drag_hint": ("Drag the cut-outs around, or let me arrange them.", "حرّك القصاصات بنفسك، أو دعني أرتّبها."),
    "color_hint": ("Move to color", "حرّك لتلوّن"), "view": ("View", "شوف"),
    "listen_lbl": ("Try it", "جرّبها"), "listen_h": ("Before I design, I listen.", "قبل أن أصمّم، أُنصت."),
    "listen_p": ("Pick up to three words that sound like your brand, and watch it take shape.", "اختر حتى ثلاث كلمات تشبه علامتك، وشاهدها تأخذ شكلها."),
    "brand_name": ("Your brand name", "اسم علامتك"), "brand_ph": ("Your Brand", "علامتك"),
    "specimen": ("Brand specimen", "عيّنة العلامة"), "send_brief": ("Send this as a brief", "أرسلها كبداية للمشروع"),
    "reset": ("Reset", "من جديد"), "brief_h": ("Your brief so far", "بداية مشروعك"),
    "brief_p": ("Paste this into the form so I start from what you picked.", "الصقها في النموذج لأبدأ مما اخترته."),
    "copy_brief": ("Copy brief", "انسخ"), "tear": ("Take my email", "خذ بريدي"), "torn": ("Copied", "اتنسخ"),
    "lost_h": ("Lost between the notebooks.", "ضاعت بين الدفاتر."), "lost_p": ("This page slipped out of the agenda. Let's go back to the work.", "هذه الصفحة سقطت من الأجندة. لنرجع للأعمال."),
    "back_home": ("Back home", "للرئيسية"), "see_work": ("See my work", "شوف أعمالي"),
    "clients": ("Worked with", "اشتغلت مع"), "menu": ("Menu", "القائمة"), "list": ("List", "قائمة"), "grid_v": ("Grid", "شبكة"),
    "summary": ("In short", "باختصار"), "role": ("My role", "دوري"), "deliv_s": ("Deliverables", "المخرجات"), "result": ("Key result", "أهم نتيجة"),
    "on_behance": ("Branding projects on Behance", "مشاريع الهويات على Behance"), "behance_tag": ("Opens Behance ↗", "يفتح Behance ↗"), "est": ("Est. 2026 — Cairo", "تأسست ٢٠٢٦ — القاهرة"), "city": ("Cairo", "القاهرة"), "swatches": ("Colour index", "فهرس الألوان"),
}


# ======================= EDITABLE CONTENT (content/*.json) =======================
# Everything below is loaded from content/site.json and content/projects/*.json.
# Those files are what the /admin dashboard edits, so edit them there (or by hand).
import json, glob
def _t(d):
    if isinstance(d, dict): return (d.get("en", "") or "", d.get("ar", "") or d.get("en", "") or "")
    return (d or "", d or "")
_S = json.load(open(os.path.join(ROOT, "content", "site.json"), encoding="utf-8"))
LEAD = _t(_S["lead"]); EMAIL = _S["email"]; INSTAGRAM = _S["instagram"]; BEHANCE = _S["behance"]; LINKEDIN = _S["linkedin"]; CV = _S["cv"]
TALLY = f"https://tally.so/embed/{_S['tally']}?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1"; TALLY_PAGE = f"https://tally.so/r/{_S['tally']}"
HOME_STATS = [(str(x["value"]), _t(x["label"])) for x in _S["home_stats"]]
ABOUT_STATS = [(str(x["value"]), _t(x["label"])) for x in _S["about_stats"]]
CLIENTS = [x["name"] for x in _S.get("clients", [])]
PROCESS = [(_t(x["title"]), _t(x["text"])) for x in _S["process"]]
FAQ = [(_t(x["q"]), _t(x["a"])) for x in _S["faq"]]
STORY = [_t(x) for x in _S["story"]]
JOBS = [(_t(x["when"]), _t(x["title"]), _t(x["role"]), _t(x["text"])) for x in _S["jobs"]]
VOLUNTEER = [(_t(x["when"]), _t(x["title"]), _t(x["role"]), _t(x["text"])) for x in _S["volunteer"]]
TOOLS = [(x["name"], x.get("kind", "")) for x in _S["tools"]]
_P = [json.load(open(f, encoding="utf-8")) for f in glob.glob(os.path.join(ROOT, "content", "projects", "*.json"))]
_P = [x for x in _P if not x.get("hidden")]
_P.sort(key=lambda x: (x.get("order", 999), x["slug"]))
PROJECTS = [(x["slug"], _t(x["name"]), _t(x["field"]), str(x.get("year", "")), x.get("category", "social"), None, x.get("cover", ""), x.get("case") or None) for x in _P]
TAGS = {x["slug"]: " ".join(x.get("tags") or ["social"]) for x in _P}
COVER_URL = {x["slug"]: x.get("cover", "") for x in _P}

def img_url(u, w=1024):
    """Framer CDN links get resized; uploaded files (/img/uploads/...) are made relative; preview uses local copies when present."""
    if not u: return None
    m = re.search(r"framerusercontent\.com/images/([A-Za-z0-9]+)", u)
    if m and _MODE["preview"]:
        for cand in (f"post-{m.group(1)}.webp",):
            if os.path.exists(os.path.join(ROOT, "img", cand)): return _MODE["pre"] + "img/" + cand
    if m: return u.split("?")[0] + f"?scale-down-to={w}"
    if u.startswith("/"): return _MODE["pre"] + u.lstrip("/")
    return u

# =========================== TEMPLATE ===========================
class Ctx:
    def __init__(s, lang, preview): s.lang, s.preview, s.i = lang, preview, (0 if lang == "en" else 1)
    def t(s, pair): return pair[s.i] if isinstance(pair, tuple) else pair
    def u(s, key): return UI[key][s.i]
    @property
    def pre(s): return "" if s.lang == "en" else "../"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;700&display=swap">')

def ph(src, cap, cls="r45", tone=None, eager=False, extra=""):
    st = f' style="--tone:{tone}"' if tone else ""
    im = f'<img src="{src}" alt="" decoding="async"{"" if eager else " loading=lazy"}>' if src else ""
    return f'<div class="ph {cls}"{st} data-cap="{e(cap)}"{extra}>{im}</div>'

def _logo_parts():
    svg = open(os.path.join(ROOT, "img", "logo.svg"), encoding="utf-8").read()
    return re.findall(r'<path class="cls-1" d="([^"]+)"', svg)
_LP = None
def face(cls=""):
    """Inline logo with separate eyes/brows so they can move (follow cursor, raise, wink)."""
    global _LP
    if _LP is None: _LP = _logo_parts()
    main, mouth, eyeL, eyeR, browR, browL = _LP
    return (f'<svg class="face {cls}" viewBox="0 0 1121.98 1367.44" aria-hidden="true"><path d="{main}"/><path d="{mouth}"/>'
            f'<g class="brows"><path d="{browL}"/><path d="{browR}"/></g><g class="eyes"><path class="eye l" d="{eyeL}"/><path class="eye r" d="{eyeR}"/></g></svg>')

SIG = f'<span class="sig" role="img" aria-label="{NAME[1]}"></span>'
SIG_RED = f'<span class="sig sig-red" role="img" aria-label="{NAME[1]}"></span>'

LIGHT_JS = ("<script>(function(){var h=12,m=null;try{h=+new Intl.DateTimeFormat('en-GB',{hour:'numeric',hourCycle:'h23',timeZone:'Africa/Cairo'}).format(new Date())}catch(e){}"
            "try{m=localStorage.getItem('dm-light')}catch(e){}var d=document.documentElement;d.setAttribute('data-light',m||(h>=6&&h<18?'day':'night'));"
            "try{if(sessionStorage.getItem('dm-wipe')){d.classList.add('wipe-in')}}catch(e){}})()</script>")

def header(c, active, fname):
    links = [("index.html", "home"), ("work.html", "work"), ("about.html", "about"), ("contact.html", "contact")]
    nav = "".join(f'<a href="{h}"{" aria-current=page" if k == active else ""}>{c.u(k)}</a>' for h, k in links)
    other = f'ar/{fname}' if c.lang == "en" else f'../{fname}'
    return f'''<header class="hdr"><div class="wrap grid">
<a class="brand" href="index.html" aria-label="{c.t(NAME)}">{face("face-sm")}<span>{c.t(NAME)}</span></a>
<nav aria-label="Main" id="main-nav">{nav}</nav>
<div class="right"><a class="cta-top ul" href="contact.html" data-cta>{c.u("start")}</a><button class="clock-pill" type="button" aria-label="{c.u("light_btn")}"><i class="orb" aria-hidden="true"></i><span class="clk-time"><span data-clock>--:--</span> {c.u("city")}</span><span class="clk-msg"><span class="lt-day">{c.u("day")}</span><span class="lt-night">{c.u("night")}</span></span></button><a class="lang" href="{other}" hreflang="{"ar" if c.lang == "en" else "en"}" aria-label="{c.u("lang_label")}" data-word="{c.u("lang_word")}">{c.u("lang")}</a><button class="menu-btn" type="button" aria-expanded="false" aria-controls="main-nav" aria-label="{c.u("menu")}"><span></span><span></span></button></div>
</div></header>'''

def footer(c):
    strips = f'<button type="button" class="strip-t" data-copy="{EMAIL}" data-torn="{c.u("torn")}"><span>{EMAIL}</span></button>'
    return f'''<footer class="ftr"><div class="wrap">
<div class="ftr-top">{face("face-lg")}{SIG if c.lang == "ar" else ""}</div>
<span class="lbl" style="display:block">{c.u("ready")}</span>
<a class="ftr-big" href="contact.html" data-cta>{c.u("lets")} <span class="arrow">↗</span></a>
<div class="grid">
  <div class="c1"><span class="lbl">{c.u("based")}</span><p>{c.u("cairo")}</p></div>
  <div class="c2"><span class="lbl">{c.u("email")}</span><div class="strips">{strips}</div></div>
  <div class="c3"><span class="lbl">{c.u("social")}</span><ul><li><a class="ul" href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a></li><li><a class="ul" href="{BEHANCE}" target="_blank" rel="noopener">Behance</a></li><li><a class="ul" href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a></li></ul></div>
  <div class="c4"><span class="lbl">{c.u("local")}</span><p><span data-clock>--:--</span> · {c.u("city")}</p></div>
</div>
<div class="ftr-bottom"><span>© 2026 {c.t(NAME)}. {c.u("rights")}</span><span>{c.t(TAGLINE_HTML)}</span></div>
</div></footer>
<div class="cursor" aria-hidden="true"><span></span></div>'''

def page(c, fname, title, active, body, extra_end=""):
    inner = (f'{header(c, active, fname)}\n<main>\n{body}\n</main>\n{footer(c)}\n{extra_end}'
             f'<script src="{c.pre}assets/main.js" charset="utf-8"></script>\n<script src="{c.pre}assets/play.js" charset="utf-8"></script>')
    head = (f'<title>{e(title)}</title>\n<meta name="description" content="{e(c.t(LEAD))}">\n'
            f'<meta property="og:image" content="{IMG}9MXsp1yQQX8ctlfxudylN9onQ.png"><link rel="icon" href="{c.pre}img/logo.svg">\n'
            f'<link rel="alternate" hreflang="en" href="{c.pre}{fname}"><link rel="alternate" hreflang="ar" href="{c.pre}ar/{fname}">\n'
            f'{FONTS}\n<link rel="stylesheet" href="{c.pre}assets/style.css">\n<link rel="stylesheet" href="{c.pre}assets/play.css">\n{LIGHT_JS}')
    if c.preview and c.lang == "en" and fname == "index.html":
        return (f'<meta name="claude:viewport-fit-sides" content="cover">\n{head}\n'
                '<script>document.documentElement.lang="en";document.documentElement.dir="ltr";</script>\n' + inner + "\n")
    d = "rtl" if c.lang == "ar" else "ltr"
    return (f'<!doctype html>\n<html lang="{c.lang}" dir="{d}">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'{head}\n</head>\n<body>\n{inner}\n</body>\n</html>\n')

def chip(slug, c, small=False):
    col, code, nm = SWATCH[slug]
    return f'<span class="chip-sw{" sm" if small else ""}"><i style="background:{col}"></i><span>{code}<br><b>{c.t(nm)}</b></span></span>'

# Scattered positions on the desk: (x, y, rotation) as fractions of the free space
SCATTER = [(0.02, 0.10, -6), (0.31, 0.00, 4), (0.60, 0.14, -3), (0.98, 0.03, 7), (0.10, 0.95, 5), (0.40, 0.72, -8), (0.70, 1.00, 3), (0.92, 0.64, -5)]

def desk(c):
    cuts = ""
    for i, p in enumerate(PROJECTS):
        slug, name, field = p[0], p[1], p[2]
        x, y, r = SCATTER[i] if i < len(SCATTER) else (((i * 37) % 97) / 100, ((i * 53) % 89) / 100, (i * 7) % 13 - 6)
        cuts += (f'<a class="cut" href="project-{slug}.html" data-tags="{TAGS[slug]}" data-x="{x}" data-y="{y}" data-r="{r}" data-cursor="{c.u("view")}" draggable="false">'
                 f'<span class="tape" aria-hidden="true"></span>{ph(cover_(slug), c.t(name), "r45 mono")}'
                 f'<span class="cap"><span class="idx">({i+1:02d})</span> <b>{c.t(name)}</b> <span>{c.t(field)}</span></span></a>')
    # branding lives on Behance for now: a clearly-labelled card that only shows under the Branding filter
    cuts += (f'<a class="cut cut-out" href="{BEHANCE}/projects" target="_blank" rel="noopener" data-tags="branding" data-x="0.5" data-y="0.4" data-r="-2" data-cursor="Behance ↗" draggable="false" hidden>'
             f'<span class="tape" aria-hidden="true"></span><span class="ph r45 be-card"><b>Bē</b><span>{c.u("on_behance")}</span></span>'
             f'<span class="cap"><span class="idx">↗</span> <b>Behance</b> <span>{c.u("behance_tag")}</span></span></a>')
    filt = "".join(f'<button type="button" class="{"on" if k == "all" else ""}" data-f="{k}" aria-pressed="{"true" if k == "all" else "false"}">{c.t(t)}<span class="idx">({i:02d})</span></button>' for i, (k, t) in enumerate(FILTERS))
    return f'''<section class="desk-sec" id="works"><div class="wrap">
  <div class="ghost ghost-filter" role="group" aria-label="{c.u("work")}">{filt}</div>
  <div class="desk-bar"><span class="lbl">{c.u("page01")}</span>
    <span class="desk-actions"><span class="lbl hint">{c.u("drag_hint")}</span><button class="btn" type="button" data-arrange data-a="{c.u("arrange")}" data-s="{c.u("scatter")}">{c.u("scatter")}</button></span></div>
  <div class="desk" data-desk>{cuts}</div>
  <p style="margin-top:40px"><a class="btn" href="work.html">{c.u("all_work")} <span class="arrow">↗</span></a></p>
</div></section>'''

def clients_strip(c):
    names = "".join(f"<span>{n}</span>" for n in CLIENTS)
    return f'''<section class="clients" aria-label="{c.u("clients")}"><div class="wrap"><span class="lbl">{c.u("clients")}</span></div>
<div class="marquee"><div class="track">{names}</div><div class="track" aria-hidden="true">{names}</div></div></section>'''

def listen(c):
    words = "".join(f'<button type="button" class="word" data-trait="{k}" aria-pressed="false">{c.t(w)}</button>' for k, w in LISTEN_WORDS)
    return f'''<section class="sec listen" id="listen"><div class="wrap">
  <div class="sec-head"><span class="lbl">({c.u("listen_lbl")})</span><h2>{c.u("listen_h")}</h2></div>
  <div class="grid listen-grid">
    <div class="listen-ctl">
      <p class="listen-p">{c.u("listen_p")}</p>
      <div class="words" role="group">{words}</div>
      <label class="lbl" for="brand-name">{c.u("brand_name")}</label>
      <input id="brand-name" class="brand-input" type="text" maxlength="22" placeholder="{c.u("brand_ph")}" autocomplete="off">
      <p class="listen-note" aria-live="polite"></p>
      <p class="listen-actions"><a class="btn solid" href="contact.html" data-brief data-cta>{c.u("send_brief")} <span class="arrow">↗</span></a><button class="btn" type="button" data-reset>{c.u("reset")}</button></p>
    </div>
    <figure class="specimen" data-specimen data-ph="{c.u("brand_ph")}">
      <figcaption class="lbl">{c.u("specimen")}</figcaption>
      <span class="sp-shape" aria-hidden="true"></span>
      <span class="sp-name">{c.u("brand_ph")}</span>
      <span class="sp-line">{c.u("est")}</span>
      <span class="sp-words"></span>
      <span class="sp-pal" aria-hidden="true"><i></i><i></i><i></i></span>
    </figure>
  </div>
</div></section>'''

def home(c):
    stats = "".join(f'<div class="num"><span class="k">{c.t(l)}</span><b>{plus(n)}</b></div>' for n, l in HOME_STATS)
    ghost = "".join(f'<a href="work.html" class="{"on" if i == 0 else ""}">{c.t(s)}<span class="idx">({i+1:02d})</span></a>' for i, s in enumerate(SERVICES))
    steps = "".join(f'<div class="step rv"><span class="big idx">{i+1}</span><h3>{c.t(h)}</h3><p>{c.t(d)}</p></div>' for i, (h, d) in enumerate(PROCESS))
    faq = "".join(f'<details><summary><span class="idx">{i+1:02d}</span><span>{c.t(q)}</span><span class="pm" aria-hidden="true">+</span></summary><p>{c.t(a)}</p></details>' for i, (q, a) in enumerate(FAQ))
    nl = NAME_LINES[c.i]
    hero_name = (f'<h1 class="hero-name hero-sig" aria-label="{c.t(NAME)}"><span class="sig sig-hero"></span></h1>' if c.lang == "ar"
                 else f'<h1 class="hero-name" aria-label="{c.t(NAME)}"><span>{nl[0]}</span><span>{nl[1]}</span></h1>')
    svc = "<br>".join(c.t(s) for s in SERVICES)
    me = c.pre + ME
    return f'''<section class="hero">
<div class="wrap grid hero-top">
  <div class="avail"><i></i>{c.u("available")}</div>
  <div class="lead-wrap"><p class="lead">{c.t(LEAD)}</p>
  <p class="hero-ctas"><a class="btn solid" href="#works">{c.u("see_work")} <span class="down">↓</span></a><a class="btn" href="contact.html" data-cta>{c.u("start")} <span class="arrow">↗</span></a></p></div>
</div>
<div class="hero-stage">
  <div class="hero-photo lens" data-lens data-cursor="{c.u("color_hint")}"><img class="base" src="{me}" alt="{c.t(NAME)}"><img class="top" src="{me}" alt="" aria-hidden="true"><span class="lens-hint lbl">{c.u("color_hint")} ●</span></div>
  {hero_name}
</div>
</section>
<section class="wrap grid tagline-row">
  <span class="lbl">(©2026)</span>
  <p class="t">{c.t(TAGLINE_MARK)}</p>
  <p class="loc"><span class="lbl">{c.u("based")}</span><br>{c.u("cairo")}</p>
</section>
{desk(c)}
<section class="sec-tight proof"><div class="wrap nums rv"><span class="lbl">{c.u("numbers")}</span><div class="row">{stats}</div></div></section>
{clients_strip(c)}
<section class="sec"><div class="wrap">
  <div class="sec-head"><span class="lbl">{c.u("process")}</span><h2>{c.u("how")}</h2></div>
  <div class="steps">{steps}</div>
</div></section>
{listen(c)}
<section class="sec" style="padding-top:0"><div class="wrap">
  <div class="sec-head"><span class="lbl">{c.u("faq")}</span><h2>{c.u("faq_h")}</h2></div>
  <div class="grid"><div class="faq">{faq}</div></div>
</div></section>'''

def work(c):
    rows, cards = "", ""
    for i, p in enumerate(PROJECTS):
        slug, name, field, year, cat = p[0], p[1], p[2], p[3], p[4]
        rows += (f'<a class="wrow" data-cat="{cat}" href="project-{slug}.html" data-cursor="{c.u("view")}"><span class="idx">({i+1:02d})</span><h3>{c.t(name)}</h3>'
                 f'<span class="f">{c.t(field)}</span><span class="y">{year}</span><span class="go arrow">↗</span></a>')
        cards += (f'<a class="gcard" data-cat="{cat}" href="project-{slug}.html" data-cursor="{c.u("view")}">{ph(cover_(slug), c.t(name), "r45 mono")}'
                  f'<span class="gmeta"><span class="idx">({i+1:02d})</span><b>{c.t(name)}</b><span>{c.t(field)} · {year}</span></span></a>')
    rows += (f'<a class="wrow" data-cat="branding" href="{BEHANCE}/projects" target="_blank" rel="noopener"><span class="idx">(→)</span><h3>{c.u("branding_cat")}</h3>'
             f'<span class="f">{c.u("branding_more")}</span><span class="y">{c.u("behance_tag")}</span><span class="go arrow">↗</span></a>')
    cards += (f'<a class="gcard" data-cat="branding" href="{BEHANCE}/projects" target="_blank" rel="noopener"><span class="ph r45 be-card"><b>Bē</b><span>{c.u("on_behance")}</span></span>'
              f'<span class="gmeta"><span class="idx">↗</span><b>{c.u("branding_cat")}</b><span>{c.u("behance_tag")}</span></span></a>')
    return f'''<section class="phead"><div class="wrap grid">
  <h1>{c.u("work")}</h1>
  <p class="intro">{c.u("work_intro")}</p>
</div></section>
<section class="wrap" style="padding-bottom:120px">
  <div class="work-tools">
    <div class="filters" role="group">
      <button type="button" data-filter="all" aria-pressed="true">{c.u("filter_all")}</button>
      <button type="button" data-filter="social" aria-pressed="false">{c.u("social_cat")}</button>
      <button type="button" data-filter="branding" aria-pressed="false">{c.u("branding_cat")}</button>
    </div>
    <div class="view-toggle" role="group"><button type="button" data-view="list" aria-pressed="true">☰ {c.u("list")}</button><button type="button" data-view="grid" aria-pressed="false">▦ {c.u("grid_v")}</button></div>
  </div>
  <div class="windex">{rows}</div>
  <div class="wgrid" hidden>{cards}</div>
</section>'''

def lost(c):
    return f'''<section class="lost wrap"><div class="lost-n" aria-hidden="true">4<span class="cut lost-cut"><span class="tape"></span>{ph(cover_("hbbah"), "", "r45 mono")}</span>4</div>
<h1>{c.u("lost_h")}</h1><p>{c.u("lost_p")}</p><p><a class="btn solid" href="index.html">{c.u("back_home")} <span class="arrow">↗</span></a> <a class="btn" href="work.html">{c.u("all_work")}</a></p></section>'''

def about(c):
    story = STORY
    QUOTE_MARKS = "“«" + chr(34)
    def pcls(n, t): return "first" if n == 0 else ("q" if c.t(t)[:1] in QUOTE_MARKS else "")
    txt = "".join(f'<p class="{pcls(n, t)}">{c.t(t)}</p>' for n, t in enumerate(story)) + (SIG_RED if c.lang == "ar" else "")
    txt += f'<p style="display:flex;gap:16px;flex-wrap:wrap"><a class="btn solid" href="{CV}" target="_blank" rel="noopener">{c.u("cv")} <span class="arrow">↗</span></a><a class="ul" href="{BEHANCE}" target="_blank" rel="noopener">Behance</a><a class="ul" href="https://www.linkedin.com/in/diaamohammed/" target="_blank" rel="noopener">LinkedIn</a></p>'
    def rows(items):
        return "".join(f'<div class="trow rv"><span class="when">{c.t(w)}</span><h3>{c.t(t)}<small>{c.t(r)}</small></h3><p>{c.t(d)}</p></div>' for w, t, r, d in items)
    stats = "".join(f'<div class="num"><span class="k">{c.t(l)}</span><b>{plus(n)}</b></div>' for n, l in ABOUT_STATS)
    tools = "".join(f'<div>{n}<span>{k}</span></div>' for n, k in TOOLS)
    return f'''<section class="phead"><div class="wrap grid"><span class="lbl">{c.u("about")}</span><h1>{c.u("story")}</h1></div></section>
<section class="wrap grid about-hero">{ph(c.pre + "img/me.webp", c.t(NAME), "r45 lens-auto", eager=True)}<div class="txt">{txt}</div></section>
<section class="sec"><div class="wrap nums rv"><span class="lbl">{c.u("stats")}</span><div class="row three">{stats}</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="sec-head"><span class="lbl">(01)</span><h2>{c.u("exp")}</h2></div><div class="table">{rows(JOBS)}</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="sec-head"><span class="lbl">(02)</span><h2>{c.u("vol")}</h2></div><div class="table">{rows(VOLUNTEER)}</div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="sec-head"><span class="lbl">(03)</span><h2>{c.u("tools")}</h2></div><div class="grid"><div class="tools">{tools}</div></div></div></section>'''

def contact(c):
    return f'''<section class="phead"><div class="wrap grid"><span class="lbl">{c.u("contact")}</span><h1>{c.u("contact_h")}</h1><p class="intro">{c.u("contact_intro")}</p></div></section>
<section class="wrap grid contact" style="padding-bottom:120px;row-gap:40px">
  <div class="left">
    <div class="brief" hidden><span class="lbl">{c.u("brief_h")}</span><p class="brief-txt" id="brief-txt"></p><p class="lbl">{c.u("brief_p")}</p><button class="btn solid" type="button" data-copy-brief data-done="{c.u("copied")}">{c.u("copy_brief")}</button></div>
    <div><span class="lbl">{c.u("email")}</span><p class="email" id="mail">{EMAIL}</p><button class="btn" type="button" style="margin-top:12px" data-copy="{EMAIL}" data-target="mail" data-done="{c.u("copied")}">{c.u("copy")}</button></div>
    <div><span class="lbl">{c.u("based")}</span><p>{c.u("cairo")} · <span data-clock>--:--</span></p></div>
    <div><span class="lbl">{c.u("social")}</span><p style="display:flex;gap:16px;flex-wrap:wrap"><a class="ul" href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a><a class="ul" href="{BEHANCE}" target="_blank" rel="noopener">Behance</a><a class="ul" href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a></p></div>
  </div>
  <div class="form"><iframe src="{TALLY}" title="Contact form" loading="lazy"></iframe>
    <p class="lbl" style="text-align:center;padding-top:8px">{c.u("form_alt")} <a class="ul" href="{TALLY_PAGE}" target="_blank" rel="noopener">{c.u("form_open")}</a></p></div>
</section>'''

def project(c, idx):
    slug, name, field, year, cat, tone, cover, cs = PROJECTS[idx]
    nxt = PROJECTS[(idx + 1) % len(PROJECTS)]
    T = lambda v: c.t(_t(v)) if v is not None else ""
    lede = lambda a, b: f'<p class="lede">{T(cs.get(a))} <em>{T(cs.get(b))}</em></p>' if T(cs.get(a)) else ""
    summary_html = ""
    if cs:
        parts = []
        if T(cs.get("role")): parts.append(f'<div><dt class="lbl">{c.u("role")}</dt><dd>{T(cs.get("role"))}</dd></div>')
        if cs.get("deliverables"): parts.append(f'<div><dt class="lbl">{c.u("deliv_s")}</dt><dd>{" · ".join(T(d) for d in cs["deliverables"][:3])}</dd></div>')
        if cs.get("results"):
            r0 = cs["results"][0]; parts.append(f'<div class="hl"><dt class="lbl">{c.u("result")}</dt><dd><b>{r0.get("value","")}</b> {T(r0.get("text"))}</dd></div>')
        if parts: summary_html = f'<dl class="tldr">{"".join(parts)}</dl>'
    head = f'''<div class="progress" aria-hidden="true"></div>
<section class="cs-head"><div class="wrap grid">
  <a class="back" href="work.html"><span class="arrow" style="transform:scaleX(-1)">→</span>{c.u("back")}</a>
  <div class="t"><span class="lbl">{c.t(field)} · {year}</span><h1>{c.t(name)}</h1></div>
  <span class="n idx">({idx+1:02d})</span>
  {f'<p class="desc">{T(cs.get("description"))}</p>' if cs and T(cs.get("description")) else ''}
  {summary_html}
</div></section>'''
    if cs:
        meta = "".join(f'<div class="m"><span class="lbl">{c.t(lbl)}</span>{T(cs.get(k))}</div>' for k, lbl in
                       [("services", ("Services", "الخدمات")), ("client", ("Client", "العميل")), ("country", ("Country", "الدولة")), ("duration", ("Duration", "المدة"))] if T(cs.get(k)))
    else:
        meta = (f'<div class="m"><span class="lbl">{c.u("services")}</span>{c.u("social_cat")}</div><div class="m"><span class="lbl">{c.t(("Client","العميل"))}</span>{c.t(name)}</div>'
                f'<div class="m"><span class="lbl">{c.t(("Year","السنة"))}</span>{year}</div>')
    head += f'<section class="wrap grid cs-meta"><span class="lbl h">{c.u("info")}</span>{meta}</section>'
    nxt_html = f'<a class="next" href="project-{nxt[0]}.html"><span class="lbl"><span>{c.u("next")}</span><span>{c.t(nxt[2])}</span></span><h2>{c.t(nxt[1])} <span class="arrow">↗</span></h2></a>'
    if not cs:
        return head + f'''<section class="wrap">{ph(cover_(slug, 2048), c.t(name), "r21 cs-cover", eager=True)}
<div class="soon"><p style="font-size:clamp(1.4rem,2.6vw,2.2rem);letter-spacing:-.02em">{c.u("soon")}</p><a class="btn" href="{BEHANCE}" target="_blank" rel="noopener">{c.u("behance")} <span class="arrow">↗</span></a></div>
{nxt_html}</section>''', ""

    chapters = []
    def chap(key, inner):
        if not inner.strip(): return
        i = len(chapters) + 1
        chapters.append(f'<section class="chap wrap" id="{key}"><div class="side"><span class="idx">({i:02d})</span><h2>{c.u(key)}</h2></div><div class="main">{inner}</div></section>')
    tones = ["#DCE0F5", "#F3E8C3", "#D5EBDD", "#EBD3DC", "#E4E2DC", "#D6DCEB"]
    posts_l = cs.get("posts") or []
    cars = [x.get("slides") or [] for x in (cs.get("carousels") or []) if x.get("slides")]
    cover = ph(cover_(slug, 2048), "Cover", "r21 cs-cover", eager=True)
    trio = "".join(ph(img_url(u), f"Post {n+1}", "r45", tones[n]) for n, u in enumerate(posts_l[:3]))
    ov = "".join(f"<p>{T(x)}</p>" for x in cs.get("overview") or [])
    chap("overview", lede("overview_lede", "overview_soft") + (f'<div class="body"><div class="cols">{ov}</div></div>' if ov else ""))
    li = lambda xs: "".join(f'<li><span class="idx">{n+1:02d}</span>{T(x)}</li>' for n, x in enumerate(xs))
    kv = ""
    if cs.get("goals") or cs.get("limits"):
        kv = '<div class="kv">' + (f'<div><span class="lbl">{c.u("goals")}</span><ul>{li(cs["goals"])}</ul></div>' if cs.get("goals") else "") + (f'<div><span class="lbl">{c.u("limits")}</span><ul>{li(cs["limits"])}</ul></div>' if cs.get("limits") else "") + '</div>'
    chap("challenge", lede("challenge_lede", "challenge_soft") + kv)
    words = "".join(f"<span>{T(w)}</span>" for w in cs.get("keywords") or [])
    mood_imgs = [m for m in (cs.get("moodboard") or []) if m]
    mood = "".join(ph(img_url(u), f'{c.u("moodboard")} {n+1}', "abcde"[n % 5], tones[n % 6]) for n, u in enumerate(mood_imgs[:5]))
    def fg(hexc):
        h = hexc.lstrip("#"); 
        try: r, g_, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        except Exception: return "#0E0E0E"
        return "#0E0E0E" if (r * 299 + g_ * 587 + b * 114) / 1000 > 150 else "#FFFFFF"
    pal = "".join(f'<div style="background:{x["color"]};color:{fg(x["color"])};border:1px solid var(--line)">{x["color"]}</div>' for x in cs.get("palette") or [] if x.get("color"))
    routes = cs.get("routes") or []
    dirs = "".join(f'<article class="dir{" pick" if r.get("chosen") else ""}"><div class="top"><span>{chr(65+n)} · {T(r.get("title"))}</span><span class="st">{c.u("chosen") if r.get("chosen") else c.u("explored")}</span></div>{ph(img_url(r.get("image")), f"Route {chr(65+n)}", "r45", tones[n % 6])}<p>{T(r.get("text"))}</p></article>' for n, r in enumerate(routes))
    chap("thinking", lede("idea_lede", "idea_soft") + (f'<div class="words">{words}</div>' if words else "") + (f'<div class="mood">{mood}</div>' if mood else "") + (f'<div class="pal">{pal}</div>' if pal else "")
         + (f'<p class="lbl" style="margin-top:64px">{c.u("routes")}</p><div class="dirs" style="margin-top:16px">{dirs}</div>' if dirs else ""))
    btn = lambda u, cap, n: f'<button type="button" data-lb="{img_url(u, 2048)}" data-cap="{cap}" aria-label="{cap}">{ph(img_url(u), cap, "r45", tones[n % 6])}</button>'
    posts = "".join(btn(u, f"Post {n+1}", n) for n, u in enumerate(posts_l))
    sets = "".join(f'<div class="set"><div class="h"><span>{c.u("carousel")} {k:02d}</span><span>{len(part)} {c.u("slides")}</span></div><div class="strip">' + "".join(btn(u, f"Carousel {k} · {n+1}", n) for n, u in enumerate(part)) + '</div></div>' for k, part in enumerate(cars, 1))
    n_slides = sum(len(x) for x in cars)
    tabs = ""
    if posts and sets:
        tabs = (f'<div class="tabs" role="tablist"><button role="tab" type="button" data-tab="t-posts" aria-selected="true">{c.u("posts")}<sup>{len(posts_l)}</sup></button><button role="tab" type="button" data-tab="t-car" aria-selected="false">{c.u("carousels")}<sup>{n_slides}</sup></button></div>'
                f'<div id="t-posts" class="gal">{posts}</div><div id="t-car" hidden>{sets}</div>')
    elif posts: tabs = f'<div class="gal" style="margin-top:40px">{posts}</div>'
    elif sets: tabs = f'<div style="margin-top:40px">{sets}</div>'
    chap("solution", lede("solution_lede", "solution_soft") + tabs)
    res = "".join(f'<div class="num"><span class="k">{T(r.get("label"))}</span><b>{r.get("value","")}</b><p>{T(r.get("text"))}</p></div>' for r in cs.get("results") or [])
    quote = f'<div class="quote"><p>{T(cs.get("quote"))}</p><span class="who">{T(cs.get("quote_by"))}</span></div>' if T(cs.get("quote")) else ""
    chap("results", (f'<div class="nums" style="display:block"><div class="row three">{res}</div></div>' if res else "") + quote)
    team = "".join(f'<div class="r{" me" if m.get("me") else ""}"><span class="role">{T(m.get("role"))}</span><span class="name">{T(m.get("name"))}</span></div>' for m in cs.get("team") or [])
    deliv = "".join(f"<span>{T(d)}</span>" for d in cs.get("deliverables") or [])
    chap("credits", (f'<div class="credits">{team}</div>' if team else "") + (f'<p class="lbl" style="margin-top:44px">{c.u("deliv")}</p><div class="deliv" style="margin-top:10px">{deliv}</div>' if deliv else ""))
    lb = f'<div class="lb" id="lb" hidden role="dialog" aria-modal="true" aria-label="Viewer"><button class="x" type="button">{c.u("close")} ✕</button><div class="ph"><img alt=""></div><div class="ui"><button class="prev" type="button">{c.u("prev")}</button><span class="cnt"></span><button class="nxt" type="button">{c.u("nextb")}</button></div></div>\n' if (posts or sets) else ""
    body = head + f'<section class="wrap">{cover}' + (f'<div class="cs-trio">{trio}</div>' if trio else "") + '</section>' + "".join(chapters) + f'<div class="wrap">{nxt_html}</div>'
    return body, lb

# =========================== BUILD ===========================
def build(out, preview):
    shutil.rmtree(out, ignore_errors=True)
    for lang in ("en", "ar"):
        c = Ctx(lang, preview)
        _MODE["preview"], _MODE["pre"] = preview, c.pre
        d = out if lang == "en" else os.path.join(out, "ar")
        os.makedirs(d, exist_ok=True)
        N = c.t(NAME)
        pages = {"index.html": (N if not (preview and lang == "en") else "Diaa Mohammed Portfolio", "home", home(c), ""),
                 "work.html": (f"{c.u('work')} — {N}", "work", work(c), ""),
                 "about.html": (f"{c.u('about')} — {N}", "about", about(c), ""),
                 "contact.html": (f"{c.u('contact')} — {N}", "contact", contact(c), "")}
        pages["404.html"] = (f"404 — {N}", "", lost(c), "")
        for i, p in enumerate(PROJECTS):
            body, lb = project(c, i)
            pages[f"project-{p[0]}.html"] = (f"{c.t(p[1])} — {N}", "work", body, lb)
        for fn, (title, act, body, end) in pages.items():
            with open(os.path.join(d, fn), "w", encoding="utf-8") as f:
                f.write(page(c, fn, title, act, body, end))
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(out, "assets"))
    os.makedirs(os.path.join(out, "img"), exist_ok=True)
    for f in os.listdir(os.path.join(ROOT, "img")):
        if os.path.isdir(os.path.join(ROOT, "img", f)): continue
        if preview or f in ("logo.svg", "me.webp", "signature.png"):
            shutil.copy(os.path.join(ROOT, "img", f), os.path.join(out, "img", f))
    up = os.path.join(ROOT, "img", "uploads")
    if os.path.isdir(up): shutil.copytree(up, os.path.join(out, "img", "uploads"), dirs_exist_ok=True)
    if os.path.isdir(os.path.join(ROOT, "admin")): shutil.copytree(os.path.join(ROOT, "admin"), os.path.join(out, "admin"))
    if os.path.isdir(os.path.join(ROOT, "fonts")):
        shutil.copytree(os.path.join(ROOT, "fonts"), os.path.join(out, "fonts"))

if __name__ == "__main__":
    build(os.path.join(ROOT, "site"), False)
    build(os.path.join(ROOT, "preview"), True)
    print("built site/ and preview/")

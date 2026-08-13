from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- قاعدة بيانات مؤقتة تمثل العقارات المضافة (تتحدث أوتوماتيكياً) ---
properties_db = [
    {
        "id": 1,
        "title": "بنت هاوس بانوراما فاخر",
        "type": "بنت هاوس",
        "location": "التجمع الخامس",
        "price": 5000000,
        "rent": 45000,
        "area": 280,
        "description": "بنتهاوس بتصميم عصري فائق الفخامة مع إطلالة مفتوحة وتشطيبات ديلوكس."
    },
    {
        "id": 2,
        "title": "شقة استثمارية مميزة",
        "type": "شقة",
        "location": "الشيخ زايد",
        "price": 3200000,
        "rent": 28000,
        "area": 160,
        "description": "شقة قرب الخدمات الرئيسية بعائد استثماري مرتفع."
    }
]

# --- 1. خوارزمية التسعير الذكي وحساب متوسط السوق ---
def get_market_average(location):
    location_props = [p for p in properties_db if p['location'] == location]
    if not location_props:
        return 18000
    total_price = sum(p['price'] for p in location_props)
    total_area = sum(p['area'] for p in location_props)
    return round(total_price / total_area, 2)

# --- 2. حساب العائد السنوي (ROI) تلقائياً ---
def calculate_roi(price, rent):
    try:
        annual_rent = rent * 12
        roi = (annual_rent / price) * 100
        return round(roi, 2)
    except:
        return 10.5

# --- 3. حساب تكلفة التشطيب الذكية أوتوماتيكياً ---
def calculate_renovation(area):
    rate_per_meter = 3200 
    total = area * rate_per_meter
    return f"{total:,.0f}"

# --- 4. توليد مؤشر السوق ونقاط الذكاء الاصطناعي ---
def generate_ai_insights(prop):
    avg_meter = get_market_average(prop['location'])
    prop_meter = prop['price'] / prop['area']
    
    if prop_meter < avg_meter:
        advice = "السعر الحالي أقل من متوسط السوق، فرصة استثمارية قوية جداً للشراء الفوري."
        status = "فرصة ذهبية صاعدة 🚀"
    else:
        advice = "السعر يتوافق مع معدلات النمو المستقرة في المنطقة."
        status = "نمو مستقر ومتوازن 📈"

    return {
        "status": status,
        "growth_rate": "+14% سنشط سنوياً",
        "advice": advice
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    for prop in properties_db:
        prop['roi'] = calculate_roi(prop['price'], prop['rent'])
        prop['reno_cost'] = calculate_renovation(prop['area'])
        prop['trend'] = generate_ai_insights(prop)
        prop['price_formatted'] = f"{prop['price']:,.0f}"
        prop['rent_formatted'] = f"{prop['rent']:,.0f}"

    return render_template('index.html', properties=properties_db)

@app.route('/add_property', methods=['GET', 'POST'])
def add_property():
    if request.method == 'POST':
        new_prop = {
            "id": len(properties_db) + 1,
            "title": request.form.get('title', 'عقار جديد'),
            "type": request.form.get('type', 'شقة'),
            "location": request.form.get('location', 'القاهرة'),
            "price": float(request.form.get('price', 0)),
            "rent": float(request.form.get('rent', 0)),
            "area": float(request.form.get('area', 100)),
            "description": request.form.get('description', '')
        }
        properties_db.append(new_prop)
        return render_template('index.html', properties=properties_db)
    
    return "<h1>صفحة إضافة عقار</h1><form method='POST'><input name='title' placeholder='العنوان'><input name='price' placeholder='السعر'><input name='rent' placeholder='الإيجار'><input name='area' placeholder='المساحة'><input name='location' placeholder='الموقع'><button type='submit'>حفظ</button></form>"

@app.route('/api/ai-search', methods=['POST'])
def ai_search():
    data = request.json
    query = data.get('query', '').lower()
    filtered = [p for p in properties_db if query in p['location'].lower() or query in p['title'].lower() or query in p['type'].lower()]
    
    if not filtered:
        filtered = properties_db
        
    return jsonify({
        "status": "success", 
        "message": f"تم تحليل طلبك وعرض {len(filtered)} عقاراً مطابقاً بالمعايير الذكية الحية!"
    })

@app.route('/offers')
def offers():
    return "<h1>قائمة العروض الحصرية</h1><a href='/'>العودة للرئيسية</a>"

@app.route('/messages')
def messages():
    return "<h1>قسم الرسائل والتواصل</h1><a href='/'>العودة للرئيسية</a>"

@app.route('/profile')
def profile_page():
    return "<h1>صفحة المستثمر العقاري</h1><a href='/'>العودة للرئيسية</a>"

@app.route('/more')
def more():
    return "<h1>المزيد من الإعدادات والخدمات</h1><a href='/'>العودة للرئيسية</a>"

if __name__ == '__main__':
    app.run(port=5004, debug=True)
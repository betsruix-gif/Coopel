from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta_coopel_2024_segura'
app.config["MONGO_URI"] = "mongodb+srv://Admin:admin123456@cluster0.3wpkqiz.mongodb.net/coopel"
app.config['UPLOAD_FOLDER'] = 'static/img'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'avif'}

mongo = PyMongo(app)

departamentos = [
    {
        "id": "electronica", 
        "nombre": "Electronica", 
        "icono": "📱", 
        "color": "#667eea",
        "descripcion": "Los mejores productos electrónicos"
    },
    {
        "id": "jugueteria", 
        "nombre": "Juguetería", 
        "icono": "🎮", 
        "color": "#38a169",
        "descripcion": "Juguetes para todas las edades"
    },
    {
        "id": "hogar", 
        "nombre": "Hogar", 
        "icono": "🏠", 
        "color": "#9f7aea",
        "descripcion": "Todo para tu hogar"
    }
]

productos_db = {
    "electronica": [
        {
            "id": "tv_sony_1",
            "nombre": "Pantalla Sony 50'' 4K Smart TV",
            "precio": 15000.00,
            "marca": "Sony",
            "imagen": "sony4k.webp",  
            "descripcion": "Pantalla LED 4K Ultra HD con Android TV, 50 pulgadas, sonido surround",
            "especificaciones": ["4K Ultra HD", "Smart TV", "Android TV", "50 Pulgadas"]
        },
        {
            "id": "laptop_gamer",
            "nombre": "Laptop Gamer ASUS ROG",
            "precio": 25000.00,
            "marca": "ASUS",
            "imagen": "Laptop.avif",  
            "descripcion": "Laptop gaming con RTX 4060, Intel i7, 16GB RAM, 1TB SSD",
            "especificaciones": ["RTX 4060", "Intel i7", "16GB RAM", "1TB SSD"]
        }
    ],
    "jugueteria": [
        {
            "id": "lego_starwars",
            "nombre": "Set LEGO Star Wars Millennium Falcon",
            "precio": 3500.00,
            "marca": "LEGO",
            "imagen": "LEGO.webp", 
            "descripcion": "Set de construcción LEGO Star Wars con 1354 piezas",
            "especificaciones": ["1354 piezas", "Edad 16+", "Coleccionable"]
        },
        {
            "id": "muneca_barbie",
            "nombre": "Muñeca Barbie Dreamhouse",
            "precio": 1200.00,
            "marca": "Barbie",
            "imagen": "barbie.webp",  
            "descripcion": "Casa de sueños Barbie con 3 pisos y accesorios",
            "especificaciones": ["3 pisos", "Incluye accesorios", "Edad 3+"]
        }
    ],
    "hogar": [
        {
            "id": "sarten_induccion",
            "nombre": "Juego de Sartenes de Inducción",
            "precio": 800.00,
            "marca": "T-fal",
            "imagen": "sarten.jpg",  
            "descripcion": "Juego de 5 sartenes antiadherentes para inducción",
            "especificaciones": ["5 piezas", "Antiaderente", "Para inducción"]
        },
        {
            "id": "cortinas_blackout",
            "nombre": "Cortinas Blackout Termicas",
            "precio": 650.00,
            "marca": "Home Comfort",
            "imagen": "cortina.jpg",  
            "descripcion": "Cortinas blackout térmicas y aislantes 140x240 cm",
            "especificaciones": ["140x240 cm", "Térmicas", "Aislamiento acústico"]
        }
    ]
}

def get_image_path(depto_id, imagen_nombre):
    """Obtiene la ruta completa de la imagen"""
    return f"img/productos/{depto_id}/{imagen_nombre}"

@app.route('/')
def index():
    if 'usuario' in session:
        return redirect(url_for('bienvenida'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if email == "admin@coopel.com" and password == "123456":
            session['usuario'] = {
                'id': '1',
                'nombre': 'Usuario Demo',
                'email': email
            }
            session['carrito'] = []
            return redirect(url_for('bienvenida'))
        else:
            return render_template('login.html', error="Credenciales incorrectas")
    
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        session['usuario'] = {
            'id': '2',
            'nombre': f"{request.form['nombres']} {request.form['apellidos']}",
            'email': request.form['email']
        }
        session['carrito'] = []
        return redirect(url_for('bienvenida'))
    
    return render_template('registro.html')

@app.route('/bienvenida')
def bienvenida():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('bienvenida.html', usuario=session['usuario'])

@app.route('/departamentos')
def departamentos_view():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('departamentos.html', departamentos=departamentos)

@app.route('/productos/<depto_id>')
def productos(depto_id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    depto = next((d for d in departamentos if d['id'] == depto_id), None)
    if not depto:
        return "Departamento no encontrado", 404
    
    productos_depto = productos_db.get(depto_id, [])
    
    for producto in productos_depto:
        producto['imagen_path'] = get_image_path(depto_id, producto['imagen'])
    
    return render_template('productos.html', 
                         productos=productos_depto, 
                         departamento=depto)

@app.route('/producto/<depto_id>/<producto_id>')
def producto_detalle(depto_id, producto_id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    productos_depto = productos_db.get(depto_id, [])
    producto = next((p for p in productos_depto if p['id'] == producto_id), None)
    
    if not producto:
        return "Producto no encontrado", 404
    
    producto['imagen_path'] = get_image_path(depto_id, producto['imagen'])
    depto = next((d for d in departamentos if d['id'] == depto_id), None)
    
    return render_template('producto_detalle.html', 
                         producto=producto, 
                         departamento=depto)

@app.route('/agregar_carrito', methods=['POST'])
def agregar_carrito():
    if 'usuario' not in session:
        return jsonify({'success': False, 'message': 'Debe iniciar sesión'})
    
    depto_id = request.form['depto_id']
    producto_id = request.form['producto_id']
    cantidad = int(request.form.get('cantidad', 1))
    
    productos_depto = productos_db.get(depto_id, [])
    producto = next((p for p in productos_depto if p['id'] == producto_id), None)
    
    if not producto:
        return jsonify({'success': False, 'message': 'Producto no encontrado'})
    
    if 'carrito' not in session:
        session['carrito'] = []
    
    carrito_item = next((item for item in session['carrito'] 
                        if item['producto_id'] == producto_id and item['depto_id'] == depto_id), None)
    
    if carrito_item:
        carrito_item['cantidad'] += cantidad
    else:
        session['carrito'].append({
            'producto_id': producto_id,
            'depto_id': depto_id,
            'nombre': producto['nombre'],
            'precio': producto['precio'],
            'imagen': producto['imagen'],
            'imagen_path': get_image_path(depto_id, producto['imagen']),
            'cantidad': cantidad,
            'marca': producto.get('marca', '')
        })
    
    session.modified = True
    
    return jsonify({
        'success': True, 
        'carrito_count': len(session['carrito']),
        'message': f'{producto["nombre"]} agregado al carrito'
    })

@app.route('/carrito')
def carrito():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    carrito = session.get('carrito', [])
    total = sum(item['precio'] * item['cantidad'] for item in carrito)
    
    return render_template('carrito.html', carrito=carrito, total=total)

@app.route('/actualizar_carrito', methods=['POST'])
def actualizar_carrito():
    if 'usuario' not in session:
        return jsonify({'success': False})
    
    producto_id = request.form['producto_id']
    depto_id = request.form['depto_id']
    nueva_cantidad = int(request.form['cantidad'])
    
    carrito = session.get('carrito', [])
    
    if nueva_cantidad <= 0:
        session['carrito'] = [item for item in carrito 
                             if not (item['producto_id'] == producto_id and item['depto_id'] == depto_id)]
    else:
        for item in carrito:
            if item['producto_id'] == producto_id and item['depto_id'] == depto_id:
                item['cantidad'] = nueva_cantidad
                break
    
    session.modified = True
    
    carrito_actualizado = session.get('carrito', [])
    total = sum(item['precio'] * item['cantidad'] for item in carrito_actualizado)
    
    return jsonify({
        'success': True, 
        'total': total,
        'carrito_count': len(carrito_actualizado)
    })

@app.route('/eliminar_del_carrito/<depto_id>/<producto_id>')
def eliminar_del_carrito(depto_id, producto_id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    session['carrito'] = [item for item in session['carrito'] 
                         if not (item['producto_id'] == producto_id and item['depto_id'] == depto_id)]
    session.modified = True
    
    return redirect(url_for('carrito'))

@app.route('/pago')
def pago():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    carrito = session.get('carrito', [])
    if not carrito:
        return redirect(url_for('carrito'))
    
    total = sum(item['precio'] * item['cantidad'] for item in carrito)
    return render_template('pago.html', carrito=carrito, total=total)

@app.route('/procesar_pago', methods=['POST'])
def procesar_pago():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    return redirect(url_for('procesando_pago'))

@app.route('/procesando_pago')
def procesando_pago():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('procesando_pago.html')

@app.route('/pago_exitoso')
def pago_exitoso():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    session['carrito'] = []
    session.modified = True
    
    return render_template('pago_exitoso.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':

    app.run(debug=True, port=5000)



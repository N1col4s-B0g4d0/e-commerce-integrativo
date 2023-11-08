from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response, session
from flask_wtf import FlaskForm
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SelectField
from config import config
import json
import mercadopago
import secrets # libreria para crear claves seguras CSRF Token
 
app = Flask(__name__)
db = MySQL(app)

app.config['SECRET_KEY'] = '7811cb752097e9ea4a8ca184582ef8649a27aaab6648fc41' #clave secreta CSRF Token
# token de mercado pago
sdk = mercadopago.SDK("TEST-5622517270371211-101721-e12ed1d760b7ca0ff3573b39953fddb9-144586495")
ACCESS_TOKEN = "TEST-5622517270371211-101721-e12ed1d760b7ca0ff3573b39953fddb9-144586495"

carrito = []
productos_para_preferencia = []
precio_total_carrito = 0


# Crea ítems en la preferencia
preference_data = {
    "items": [
        {
            "title": "Mi producto",
            "quantity": 1,
            "unit_price": 75.56
        },
        {
            "title": "Mi producto2",
            "quantity": 2,
            "unit_price": 96.56
        }
    ]
}

# Crea la preferencia
preference_response = sdk.preference().create(preference_data)
preference = preference_response["response"]

@app.route('/', methods=['GET','POST'])
def home():
    mensaje = request.args.get('mensaje')
    return render_template('index.html', mensaje=mensaje)

@app.route('/agregar_al_carrito/<string:nombre_producto>/<int:producto_id>', methods=['POST'])
def agregar_al_carrito(nombre_producto, producto_id):
    # Verifica si el producto ya está en el carrito
    producto_existente = next((producto for producto in carrito if producto['nombre'] == nombre_producto), None)

    if producto_existente:
        producto_existente['cantidad'] += 1
    else:
        # Agrega el producto al carrito si no existe
        carrito.append({'nombre': nombre_producto, 'producto_id': producto_id, 'cantidad': 1})

    print(carrito)
    # Redirige de nuevo a la página del carrito
    return redirect('/ver_carrito')


@app.route('/ver_carrito', methods=['GET', 'POST'])
def ver_carrito():
    productos_en_carrito = []
    # Obtén la información de la compra almacenada en la cookie
    compra_cookie = request.cookies.get('compra')
    
    # Si hay información de compra en la cookie, puedes procesarla y agregarla al carrito
    if compra_cookie:
        compra = json.loads(compra_cookie)
        nombre_producto = compra['nombre_producto']
        producto_id = compra['producto_id']
        
        # Realiza las operaciones necesarias en el carrito con esta información
        producto_existente = next((producto for producto in carrito if producto['nombre'] == nombre_producto), None)
        
        if producto_existente:
            producto_existente['cantidad'] += 1
        else:
            # Agrega el producto al carrito si no existe
            carrito.append({'nombre': nombre_producto, 'producto_id': producto_id, 'cantidad': 1})

        # Limpia la cookie después de procesar la compra
        response = make_response(render_template('ver_carrito.html'))
        response.delete_cookie('compra')
        return response

    for item in carrito:
        producto_nombre = item['nombre']

        if producto_nombre == "Hamburguesas":
            producto_id = 1
            precio_producto = 3000
        elif producto_nombre == "Pizzas":
            producto_id = 2
            precio_producto = 3000
        elif producto_nombre == "Pastas":
            producto_id = 3
            precio_producto = 5000
        elif producto_nombre == "Parrillada":
            producto_id = 4
            precio_producto = 9000
        elif producto_nombre == "Tablas":
            producto_id = 5
            precio_producto = 8000
        elif producto_nombre == "Ensaladas":
            producto_id = 6
            precio_producto = 5000
        elif producto_nombre == "Pescados":
            producto_id = 7
            precio_producto = 12000
        elif producto_nombre == "Pizzanesas":
            producto_id = 8
            precio_producto = 6000
        elif producto_nombre == "Empanadas":
            producto_id = 9
            precio_producto = 500
        elif producto_nombre == "Tostados":
            producto_id = 10
            precio_producto = 4000
        elif producto_nombre == "Lomo":
            producto_id = 11
            precio_producto = 10000
        elif producto_nombre == "Pollo":
            producto_id = 12
            precio_producto = 8500
        else:
            # Si no coincide con ningún producto conocido, asigna un valor predeterminado
            producto_id = 0
            precio_producto = 0

        cantidad = item['cantidad']
        precio_total_producto = precio_producto * cantidad

        productos_en_carrito.append({
            'id': producto_id,
            'nombre': producto_nombre,
            'precio': precio_producto,
            'cantidad': cantidad,
            'precio_total': precio_total_producto
        })

    if request.method == 'POST':
        nombre_producto = request.form.get('producto_id')
        action = request.form.get('action')
        if nombre_producto:
            for item in carrito:
                if item['nombre'] == nombre_producto:
                    if action == 'sumar':
                        item['cantidad'] += 1
                    elif action == 'restar':
                        if item['cantidad'] > 0:
                            item['cantidad'] -= 1

    precio_total_carrito = sum(item['precio_total'] for item in productos_en_carrito)

    return render_template('ver_carrito.html', productos=productos_en_carrito, precio_total_carrito=precio_total_carrito)


@app.route('/actualizar_carrito', methods=['POST'])
def actualizar_carrito():
    nombre_producto = request.form.get('producto_id')  # Recibe el nombre del producto como cadena
    action = request.form.get('action')

    if nombre_producto:
        # Encuentra el producto en el carrito por su nombre
        producto_existente = next((producto for producto in carrito if producto['nombre'] == nombre_producto), None)

        if producto_existente:
            if action == 'sumar':
                producto_existente['cantidad'] += 1
            elif action == 'restar' and producto_existente['cantidad'] > 0:
                producto_existente['cantidad'] -= 1

    # Redirige de nuevo a la página del carrito
    return redirect('/ver_carrito')


@app.route('/eliminar_del_carrito/<int:producto_id>', methods=['POST'])
def eliminar_del_carrito(producto_id):
    if producto_id in carrito:
        del carrito[producto_id]
    return render_template('carrito.html', cart=carrito)


class Checkout(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    phone_number = StringField('Number')
    email = StringField('Email')
    address = StringField('Address')
    
    

@app.route('/checkout', methods=['GET','POST'])
def checkout():
    form = Checkout()
    if request.method == 'POST':
            first_name = form.first_name.data
            last_name = form.last_name.data
            phone_number = form.phone_number.data
            email = form.email.data
            address = form.address.data
            cur=db.connection.cursor()
            cur.execute("INSERT INTO `clientes` (`nombre`, `apellido`, `telefono`, `email`, `direccion`) VALUES (%s,%s,%s,%s,%s) WHERE 1",(first_name, last_name, phone_number, email, address))
            db.connection.commit()
            cur.close()
            carrito.clear()           

    return render_template('checkout.html', form=form)


@app.route('/procesar_pago', methods=['GET','POST'])
def procesar_pago():
    # Aquí procesas el pago y realizas cualquier acción necesaria
    
    # Luego, redirige al usuario a la página principal con un mensaje
    mensaje = "Compra exitosa. En unos minutos confirmaremos su compra a través de mensaje de WhatsApp."
    return redirect(url_for('home', mensaje=mensaje))   
"""
@app.route('/obtener_preference_id', methods=['POST'])
def obtener_preference_id():
    # Configurar tus credenciales de Mercado Pago
    mp = mercadopago.SDK(ACCESS_TOKEN)

    # Obtener la información del carrito
    carrito = session.get('carrito', [])
    precio_total_carrito = session['precio_total_carrito']

    # Crear una lista de items para la preferencia
    items = []
    # Calcular el precio total del carrito
    precio_total_carrito = sum(item['precio_total'] for item in carrito)

    for producto in carrito:
        item = {
            "title": producto['nombre'],  
            "quantity": producto['cantidad'],  
            
        }   
        
        items.append(item)
        

    # Crear la preferencia de pago con la lista de items
    preference_data = {
        "items": items,
        "back_urls": {
            "success": "URL_DE_EXITO",
            "failure": "URL_DE_FALLA",
        },
        "total_amount": precio_total_carrito,
    }

    preference = mp.preference().create(preference_data)
    print(preference)

    if 'response' in preference and 'id' in preference['response']:
        preference_id = preference['response']['id']
        return jsonify({'preferenceId': preference_id})
    else:
        return jsonify({'error': 'No se pudo obtener el preferenceId'})

    return jsonify({'preferenceId': preference_id})


# Genera una cadena segura de 24 bytes
# clave_secreta = secrets.token_hex(24)
# print(clave_secreta)
"""
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(debug=True)
    csrf.init_app(app)

from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
import json

app = Flask(__name__)
carrito = []

@app.route('/', methods=['GET','POST'])
def home():
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run(debug=True)

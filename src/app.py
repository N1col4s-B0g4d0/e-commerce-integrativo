from flask import Flask, request, jsonify, render_template, redirect, url_for
import mercadopago

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

carrito = {}
@app.route('/agregar_al_carrito/<int:producto_id>', methods=['POST'])
def agregar_al_carrito(producto_id):
    # Obtén la cantidad actual del producto en el carrito o establece en 0 si no existe
    cantidad_actual = carrito.get(producto_id, 0)

    # Incrementa la cantidad en 1
    cantidad_actual += 1

    # Actualiza el carrito con la nueva cantidad
    carrito[producto_id] = cantidad_actual

    # Redirige a la página de carrito
    return redirect(url_for('ver_carrito'))

@app.route('/ver_carrito', methods=['GET', 'POST'])
def ver_carrito():
    productos_en_carrito = []

    for producto_id, cantidad in carrito.items():
        if producto_id == 1:
            nombre_producto = "Hamburguesa"
            precio_producto = 3000
        elif producto_id == 2:
            nombre_producto = "Pizza"
            precio_producto = 1000
        elif producto_id == 3:
            nombre_producto = "Refresco"
            precio_producto = 1500

        productos_en_carrito.append({
            'id': producto_id,  # Agrega el ID del producto
            'nombre': nombre_producto,
            'precio': precio_producto,
            'cantidad': cantidad
        })

    if request.method == 'POST':
        producto_id = int(request.form.get('producto_id', -1))
        action = request.form.get('action')
        if producto_id != -1:
            if action == 'sumar':
                carrito[producto_id] += 1
            elif action == 'restar':
                if carrito[producto_id] > 0:
                    carrito[producto_id] -= 1

    return render_template('ver_carrito.html', productos=productos_en_carrito)

@app.route('/actualizar_carrito', methods=['POST'])
def actualizar_carrito():
    producto_id = int(request.form.get('producto_id', -1))
    action = request.form.get('action')

    if producto_id != -1:
        if producto_id in carrito:
            if action == 'sumar':
                carrito[producto_id] += 1
            elif action == 'restar':
                if carrito[producto_id] > 0:
                    carrito[producto_id] -= 1
        else:
            # Si el producto no está en el carrito, agrégalo
            carrito[producto_id] = 1

    # Redirige de nuevo a la página del carrito
    return redirect('/ver_carrito')




@app.route('/eliminar_del_carrito/<int:producto_id>', methods=['POST'])
def eliminar_del_carrito(producto_id):
    if producto_id in cart:
        del cart[producto_id]
    return render_template('carrito.html', cart=cart)



if __name__ == '__main__':
    app.run(debug=True)

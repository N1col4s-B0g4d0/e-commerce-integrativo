from flask import Flask, request, jsonify, render_template, redirect
import mercadopago

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/carrito')
def carrito():
    return render_template('carrito.html', cart=cart)

cart = {}
@app.route('/agregar_al_carrito<int:producto_id>', methods=['POST'])
def agregar_al_carrito(producto_id):
    data = request.get_json()  # Obtén los datos JSON enviados desde JavaScript
    nombre = data.get('nombre')
    precio = data.get('precio')
    
    if producto_id not in cart:
        cart[producto_id] = 1
    else:
        cart[producto_id] += 1

    return render_template('carrito.html', cart=cart)


@app.route('/eliminar_del_carrito/<int:producto_id>', methods=['POST'])
def eliminar_del_carrito(producto_id):
    if producto_id in cart:
        del cart[producto_id]
    return render_template('carrito.html', cart=cart)



if __name__ == '__main__':
    app.run(debug=True)

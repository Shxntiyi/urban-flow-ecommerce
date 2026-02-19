from django.shortcuts import render, redirect
from .firebase_client import db
import requests
from django.contrib import messages
# Referencia a la colección 'products' en Firestore
products_ref = db.collection('products')

# --- AUTENTICACIÓN ---

def login_page(request):
    # Si el usuario ya está logueado en la sesión, lo redirigimos al catálogo
    if 'uid' in request.session:
        return redirect('product_list')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # ⚠️ PEGA AQUÍ TU CLAVE DE API WEB DE FIREBASE
        api_key = "AIzaSyC02_mdoqaxC4ALSqU5RSXlIs1oKih6-Vs"
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
        
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        
        # Hacemos la petición a Firebase Auth
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            # Login exitoso: Guardamos el ID del usuario en la sesión de Django
            user_data = response.json()
            request.session['uid'] = user_data['localId']
            return redirect('product_list')
        else:
            # Fallo: Contraseña incorrecta o usuario inexistente
            messages.error(request, "Correo o contraseña incorrectos.")
            
    return render(request, 'store/login.html')

def logout_user(request):
    # Destruye la sesión actual
    request.session.flush()
    return redirect('landing')
# --- PÁGINAS PRINCIPALES ---

def landing_page(request):
    return render(request, 'store/landing.html')



# --- CRUD DE PRODUCTOS ---

def product_list(request):
    docs = products_ref.stream()
    products = []
    for doc in docs:
        data = doc.to_dict()
        data['id'] = doc.id
        products.append(data)
        
    return render(request, 'store/product_list.html', {'products': products})

def product_create(request):
    if 'uid' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        products_ref.add({
            'name': request.POST.get('name'),
            'description': request.POST.get('description'),
            'price': float(request.POST.get('price')),
            'stock': int(request.POST.get('stock'))
        })
        return redirect('product_list')
        
    return render(request, 'store/product_form.html')

def product_update(request, product_id):
    doc_ref = products_ref.document(product_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        return redirect('product_list')
        
    if request.method == 'POST':
        doc_ref.update({
            'name': request.POST.get('name'),
            'description': request.POST.get('description'),
            'price': float(request.POST.get('price')),
            'stock': int(request.POST.get('stock'))
        })
        return redirect('product_list')

    product_data = doc.to_dict()
    product_data['id'] = doc.id
    return render(request, 'store/product_form.html', {'product': product_data})

def product_delete(request, product_id):
    if request.method == 'POST':
        products_ref.document(product_id).delete()
    return redirect('product_list')
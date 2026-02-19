import requests
from django.contrib import messages
from django.shortcuts import redirect, render

from .firebase_client import db

FIREBASE_WEB_API_KEY = "AIzaSyC02_mdoqaxC4ALSqU5RSXlIs1oKih6-Vs"
products_ref = db.collection('products')


def landing_page(request):
    return render(request, 'store/landing.html')


def login_page(request):
    if 'uid' in request.session:
        return redirect('product_list')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            user_data = response.json()
            request.session['uid'] = user_data['localId']
            return redirect('product_list')
        else:
            messages.error(request, "Correo o contraseña incorrectos.")
            
    return render(request, 'store/login.html')


def register_page(request):
    if 'uid' in request.session:
        return redirect('product_list')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'store/register.html')

        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_WEB_API_KEY}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            user_data = response.json()
            request.session['uid'] = user_data['localId']
            return redirect('product_list')
        else:
            error_data = response.json()
            error_message = error_data.get('error', {}).get('message', '')
            
            if error_message == 'EMAIL_EXISTS':
                messages.error(request, "Este correo ya está registrado. Intenta iniciar sesión.")
            elif error_message == 'WEAK_PASSWORD : Password should be at least 6 characters':
                messages.error(request, "La contraseña es muy débil. Debe tener al menos 6 caracteres.")
            else:
                messages.error(request, "Ocurrió un error al registrarse. Intenta de nuevo.")
            
    return render(request, 'store/register.html')


def logout_user(request):
    request.session.flush()
    return redirect('landing')


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
    if 'uid' not in request.session:
        return redirect('login')
        
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
    if 'uid' not in request.session:
        return redirect('login')
        
    if request.method == 'POST':
        products_ref.document(product_id).delete()
    return redirect('product_list')
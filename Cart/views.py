from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import uuid
from django.shortcuts import render

import shelve

# Open shelve store
store = shelve.open('store.db', writeback=True)

# In-memory store
if not store.get('initialized'):
    store['carts'] = {}
    store['orders'] = []
    store['discount_codes'] = {}
    store['order_count'] = 0
    store['nth_order'] = 3  
    store['initialized'] = True


def cart_view(request):
    """Render the products page."""
    return render(request, 'Cart/product_list.html')


@csrf_exempt
def add_to_cart(request):
    """Add items to the user's cart."""
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        item_id = request.POST.get('item_id')
        price = float(request.POST.get('price', 0))
        quantity = int(request.POST.get('quantity', 1))

        if not user_id or not item_id or price <= 0 or quantity <= 0:
            return JsonResponse({'error': 'Invalid input'}, status=400)

        cart = store['carts'].setdefault('default_user', [])
        cart.append({
            'item_id': item_id,
            'price': price,
            'quantity': quantity
        })
        store.sync()  # Persist changes
        return JsonResponse({'message': 'Item added to cart', 'cart': cart})

@csrf_exempt
def checkout(request):
    """Checkout the user's cart."""
    if request.method == 'POST':
        user_id = 'default_user'
        discount_code = request.POST.get('discount_code', None)

        if not user_id or user_id != 'default_user':
            return JsonResponse({'error': 'Cart not found'}, status=404)

        cart = store['carts'][user_id]
        total_amount = sum(item['price'] * item['quantity'] for item in cart)
        discount = 0
        # Apply discount code if valid and latest
        if discount_code:
            code_data = store['discount_codes'].get(discount_code)
            latest_code = max(store['discount_codes'].keys(), default=None, key=lambda k: store['discount_codes'][k]['created_at'])
            if code_data and not code_data['used'] and discount_code == latest_code:
                discount = total_amount * 0.1
                code_data['used'] = True
            else:
                return JsonResponse({'error': 'Invalid, used, or outdated discount code'}, status=400)

        total_amount -= discount
        store['orders'].append({'user_id': user_id, 'cart': cart, 'total': total_amount, 'discount': discount})
        store['order_count'] += 1

        # Clear user's cart
        store['carts'][user_id] = []
        
        return JsonResponse({'message': 'Order placed successfully', 'total_amount': total_amount, 'discount': discount})


@csrf_exempt
def clear_store(request):
    """Clear all data in the store."""
    if request.method == 'POST':
        store['carts'] = {}
        store['orders'] = []
        store['discount_codes'] = {}
        store['order_count'] = 0
        store.sync()  # Persist changes
        return JsonResponse({'message': 'Store data cleared'})
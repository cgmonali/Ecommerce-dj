from django.http import JsonResponse
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
    store['nth_order'] = 5  
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

        cart = store['carts'].setdefault(user_id, [])
        cart.append({
            'item_id': item_id,
            'price': price,
            'quantity': quantity
        })
        print('store',store)
        store.sync()  # Persist changes
        return JsonResponse({'message': 'Item added to cart', 'cart': cart})

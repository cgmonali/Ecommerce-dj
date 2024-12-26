# Installation 
- Clone the Repository
`git clone https://github.com/cgmonali/Ecommerce-dj.git`

- Navigate to project directory.
`cd Ecommerce-dj`

- Setup virtual environment

```bash
python3 -m venv env #Create virtual environment 
source env/bin/activate #Activate virtual environment 
```
- Install django
```bash
  pip install django
  ```

## **API Documentation: Endpoint**

### 1. URL Input Endpoint: cart/add/
#### method: POST

 Adds an item to the user's cart. Requires 'user_id', 'item_id', 'price', and 'quantity' as POST parameters. If the input is invalid, it returns a 400 error. If the nth order is reached, a discount code is generated.
<img width="1512" alt="Screenshot 2024-12-26 at 10 43 00 PM" src="https://github.com/user-attachments/assets/39c9360c-4117-404a-b0cc-995ff2dc4f73" />

### 2. URL Input Endpoint: cart/checkout/
#### method: POST

This endpoint processes the checkout of the user's cart. It expects a POST request with an optional 'discount_code' in the request body. 
The endpoint calculates the total amount, applies any valid discount code, creates an order, and clears the user's cart.
Returns a JSON response indicating the success or failure of the checkout process.

<img width="1512" alt="Screenshot 2024-12-26 at 10 43 47 PM" src="https://github.com/user-attachments/assets/a0261f24-d9ae-4573-ad0c-84bf928cf795" />


### 3. URL Input Endpoint: cart/get_data
#### method: GET

This endpoint retrieves the store's data. It expects a GET request and returns a JSON response containing the total number of items purchased, the total purchase amount, the status of discount codes, and the total discount amount applied to orders.
 

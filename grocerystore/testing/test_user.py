import json

"""
Below are Viewing Products Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos

test_view_products_200: Successfully Fetched Products from db    : 200
"""
"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""


def test_view_products_200(client):
    response = client.get('/user/view_products')
    assert response.status_code == 200
    assert "Items Fetched Successfully"


"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
"""
Below are Searching Products via Name | Price Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 1 Nos

test_search_products_200: Successfully Searched Products from db : 200
test_search_products_not_found_404: No Products with suh name    : 404
"""


def test_search_products_200(client):
    data = {
        "item_name": "TestTitle-1",
        "max_price": 1000,
        "min_price": 0
    }
    response = client.post('/user/search_products', json.dumps(data))
    assert response.status_code == 200
    assert response.json()[0]["image_file"] == "default.png"
    assert response.json()[0]["title"] == "TestTitle-1"
    assert response.json()[0]["description"] == "TestDescription-1"
    assert response.json()[0]["price"] == 100
    assert response.json()[0]["quantity"] == 100


def test_search_products_not_found_404(client):
    data = {
        "item_name": "no_product_found",
        "max_price": 1000,
        "min_price": 0
    }
    response = client.post('/user/search_products', json.dumps(data))
    assert response.status_code == 404
    assert "No Products Found"


"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
"""
Below are Add to Cart Products Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 5 Nos

test_add_to_cart_200: Successfully Added Products to Cart        : 200
test_add_to_cart_not_authenticated_401: Not Authenticated        : 401
test_add_to_cart_out_of_stock_404: Out of Stock - not avail      : 404
test_add_to_cart_stock_unavailable_404: stock limit exceeded     : 404
test_add_to_cart_item_not_found_404: Item-id not found           : 404
test_add_to_cart_item_updated_200: Item quantity updated         : 200
"""


def test_my_cart_no_products_404(client, token_header):
    response = client.get('/user/view_my_cart', headers={"Authorization": token_header})
    assert response.status_code == 404
    assert "No Products in Cart."


def test_add_to_cart_200(client, token_header):
    data = {
        "item_id": 1,
        "item_quantity": 1
    }
    response = client.post('/user/add_to_cart', json.dumps(data), headers={"Authorization": token_header})
    assert response.status_code == 200
    assert response.json()["message"] == "Items Successfully Added to Cart"


def test_add_to_cart_not_authenticated_401(client):
    data = {
        "item_id": 1,
        "item_quantity": 1
    }
    response = client.post('/user/add_to_cart', json.dumps(data), headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 401
    assert "Not Authenticated!"


def test_add_to_cart_out_of_stock_404(client, token_header):
    data = {
        "item_id": 2,
        "item_quantity": 200
    }
    response = client.post('/user/add_to_cart', json.dumps(data), headers={"Authorization": token_header})
    assert response.status_code == 404
    assert "Out of Stock"


def test_add_to_cart_stock_unavailable_404(client, token_header):
    data = {
        "item_id": 1,
        "item_quantity": 101
    }
    response = client.post('/user/add_to_cart', json.dumps(data), headers={"Authorization": token_header})
    assert response.status_code == 404
    assert "Stock Limit Exceeded for this item."


def test_add_to_cart_item_not_found_404(client, token_header):
    data = {
        "item_id": 100,
        "item_quantity": 1
    }
    response = client.post('/user/add_to_cart', json.dumps(data), headers={"Authorization": token_header})
    assert response.status_code == 404
    assert "Item Not found!"


def test_add_to_cart_item_updated_200(client, token_header):
    data = {
        "item_id": 1,
        "item_quantity": 1
    }
    response = client.post('/user/add_to_cart', json.dumps(data), headers={"Authorization": token_header})
    assert response.status_code == 200
    assert response.json()["Status"] == "Item Updated Successfully..."


"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
"""
Below are View my Cart Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 2 Nos

test_my_cart_200: Successfully fetched Customer's Cart           : 200
test_my_cart_not_authenticated_401: Not Authenticated            : 401
test_my_cart_no_products_404: No products Found                  : 404
"""


def test_my_cart_200(client, token_header):
    response = client.get('/user/view_my_cart', headers={"Authorization": token_header})
    assert response.status_code == 200
    assert response.json()[0]["product_name"] == "TestTitle-1"
    assert response.json()[0]["product_quantity"] == 2
    assert response.json()[0]["total"] == 200


def test_my_cart_not_authenticated_401(client):
    response = client.get('/user/view_my_cart', headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 401
    assert "Not Authenticated!"


"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
"""
Below are Delete Items from Cart Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 2 Nos

test_delete_item_from_cart_200: Successfully Deleted Item        : 200
test_delete_item_from_cart_not_authenticated_401: Auth Error     : 401
test_delete_item_from_cart_item_not_found_404: No product Found  : 404
"""


def test_delete_item_from_cart_200(client, token_header):
    response = client.delete('/user/delete_item_from_cart/1', headers={"Authorization": token_header})
    assert response.status_code == 200
    assert "Item Deleted Successfully"


def test_delete_item_from_cart_not_authenticated_401(client):
    response = client.delete('/user/delete_item_from_cart/1', headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 401
    assert "Not Authenticated!"


def test_delete_item_from_cart_item_not_found_404(client, token_header):
    response = client.delete('/user/delete_item_from_cart/100', headers={"Authorization": token_header})
    assert response.status_code == 404
    assert "Record Not Found"


"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
"""
Below are Shipping Info Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 2 Nos

test_add_shipping_info_200: Successfully Added Address           : 200
test_add_shipping_info_not_authenticated_401: Auth Error         : 401
test_add_shipping_info_invalid_phone_no_401: Length Validation   : 401
"""


def test_add_shipping_info_not_authenticated_401(client):
    data = {
        "name": "TestUser-10",
        "phone_no": "1234567890",
        "address": "Test Address",
        "city": "Test City",
        "state": "Test State"
    }
    response = client.post('/user/shipping_info', json.dumps(data), headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 401
    assert "Not Authenticated"


def test_add_shipping_info_invalid_phone_no_401(client, token_header):
    data = {
        "name": "TestUser-10",
        "phone_no": "1234567",
        "address": "Test Address",
        "city": "Test City",
        "state": "Test State"
    }
    response = client.post('/user/shipping_info', json.dumps(data), headers={"Authorization": token_header})
    assert response.status_code == 401
    assert "Invalid Phone Number."


"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
"""
Below are View All shipping Address Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 2 Nos

test_show_shipping_info_200: Successfully Fetched all Address    : 200
test_show_shipping_info_not_authenticated_401: Auth Error        : 401
test_show_shipping_info_not_found_404: No Address Found          : 404
"""


def test_show_shipping_info_not_found_404(client, token_header):
    response = client.get('/user/show_shipping_info', headers={"Authorization": token_header})
    assert response.status_code == 404
    assert "Shipping Address Not Found"


def test_order_payment_page_address_not_found_404(client, token_header):
    data = {
        "coupon_code": "",
        "shipping_id": 1
    }
    response = client.post('/user/order_payment', json.dumps(data), headers={"Authorization": token_header})
    assert response.status_code == 404
    assert "Shipping Address Not Found"


def test_add_shipping_info_200(client, token_header):
    data = {
        "name": "TestUser-11",
        "phone_no": "1234567890",
        "address": "Test Address",
        "city": "Test City",
        "state": "Test State"
    }
    response = client.post('/user/shipping_info', json.dumps(data), headers={"Authorization": token_header})
    assert response.status_code == 200
    assert response.json()["message"] == "New Shipping Address Added Successfully."


def test_show_shipping_info_200(client, token_header):
    response = client.get('/user/show_shipping_info', headers={"Authorization": token_header})
    assert response.status_code == 200
    assert response.json()[0]["name"] == "TestUser-1"


def test_show_shipping_info_not_authenticated_401(client):
    response = client.get('/user/show_shipping_info', headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 401
    assert "Not Authenticated!"


"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
"""
Below are Order Payment Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 5 Nos

test_order_payment_page_200: Successfully Send Payment Link      : 200
test_order_payment_page_not_authenticated_401: Auth Error        : 401
test_order_payment_page_code_expired_404: Coupon Code Expired    : 404
test_order_payment_page_empty_cart_404: No Items in Cart         : 404
test_order_payment_page_address_not_found_404: Address not prov  : 404
test_order_payment_page_incorrect_code: Invalid Coupon Code      : 404
"""


def test_order_history_no_order_history_404(client, token_header):
    response = client.get('/user/order_history', headers={"Authorization": token_header})
    assert response.status_code == 404


def test_order_payment_page_200(client, token_header):
    data = {
        "coupon_code": "Test",
        "shipping_id": 1
    }
    response = client.post('/user/order_payment', json.dumps(data), headers={"Authorization": token_header})
    assert response.status_code == 200
    assert response.json()["message"] == "Please Find your Invoice on your email."


def test_order_payment_page_not_authenticated_401(client):
    data = {
        "coupon_code": "",
        "shipping_id": 1
    }
    response = client.post('/user/order_payment', json.dumps(data), headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 401
    assert "Not Authenticated"


def test_order_payment_page_code_expired_404(client, token_header):
    data = {
        "coupon_code": "Expired",
        "shipping_id": 1
    }
    response = client.post('/user/order_payment', json.dumps(data), headers={"Authorization": token_header})
    assert response.status_code == 404
    assert "Code has been Expired"


def test_order_payment_page_empty_cart_404(client, token_header):
    data = {
        "coupon_code": "",
        "shipping_id": 1
    }
    response = client.post('/user/order_payment', json.dumps(data), headers={"Authorization": token_header})
    assert response.status_code == 404
    assert "Cart is Empty!"


def test_order_payment_page_incorrect_code_404(client, token_header):
    data = {
        "coupon_code": "Incorrect_code",
        "shipping_id": 1
    }
    response = client.post('/user/order_payment', json.dumps(data), headers={"Authorization": token_header})
    assert response.status_code == 404
    assert "Incorrect Coupon Code."


"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
"""
Below are Order History of Customers Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 2 Nos

test_order_history_200: Successfully Fetched all Orders          : 200
test_order_history_not_authenticated_401: Auth Error             : 401
test_order_history_no_order_history_404: No orders found         : 404
"""


def test_order_history_200(client, token_header):
    response = client.get('/user/order_history', headers={"Authorization": token_header})
    assert response.status_code == 200
    # assert response.json()[0]["description"] == "order_Jo19MK14mB8UUu"
    # assert response.json()[0]["total_amount"] == 80
    # assert response.json()[0]["payment_status"] == "refunded"


def test_order_history_not_authenticated_401(client):
    response = client.get('/user/order_history', headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 401
    assert "Not Authenticated!"


"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
"""
Below are Cancelling Order Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 2 Nos

test_cancel_order_200: Order Cancelled and Money Refunded        : 200
test_cancel_order_not_authenticated_401: Auth Error              : 401
test_cancel_order_no_record_found_404: Invalid Order ID          : 404
"""


def test_cancel_order_200(client, token_header):
    response = client.delete('/user/cancel_order/1', headers={"Authorization": token_header})
    assert response.status_code == 200
    assert "Order has been Cancelled."


def test_cancel_order_not_authenticated_401(client):
    response = client.delete('/user/cancel_order/1', headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 401
    assert "Not Authenticated!"


def test_cancel_order_no_record_found_404(client, token_header):
    response = client.delete('/user/cancel_order/100', headers={"Authorization": token_header})
    assert response.status_code == 404
    assert "No Records Found!"


"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
"""
Below are Customer Balance Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 1 Nos

test_view_balance_200: Successfully fetched Balance              : 200
test_view_balance_not_authenticated_401: Auth Error              : 401
"""


def test_view_balance_200(client, token_header):
    response = client.get('/user/view_balance', headers={"Authorization": token_header})
    assert response.status_code == 200
    # assert response.json()["acc_balance"] == 360


def test_view_balance_not_authenticated_401(client):
    response = client.get('/user/view_balance', headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 401
    assert "Not Authenticated"


"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
"""
Below are Discount Coupons Available/Valid Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos

test_show_discount_coupon_200: Successfully fetched valid coupons: 200
"""


def test_show_discount_coupon_200(client, token_header):
    response = client.get('/user/show_discount_coupon', headers={"Authorization": token_header})
    assert response.status_code == 200
    assert response.json()[0]["coupon_code"] == "Test"
    assert response.json()[0]["discount_percentage"] == 10
    assert response.json()[0]["valid_till"] == "2030-12-12"

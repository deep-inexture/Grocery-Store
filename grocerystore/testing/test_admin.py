import json

"""
# Below are Show Products Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 1 Nos

test_all_products_200: Fetch All products in grocery             : 200
test_all_products_unauthorized_401: Except Admin. No Permission  : 401
"""
"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""


def test_all_products_200(client, admin_token_header):
    response = client.get('/admin/get_items', headers={"Authorization": admin_token_header})
    assert response.status_code == 200
    assert "Items Fetched Successfully"


def test_all_products_unauthorized_401(client):
    response = client.get('/admin/get_items', headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 401
    assert "UnAuthorized User"


"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
"""
# Below are Add Products to Grocery Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 1 Nos

test_add_product_201: Add the Listed Products to grocery         : 200
test_add_product_unauthorized_401: Except Admin. No Permission   : 401
"""


def test_add_product_201(client, admin_token_header):
    data = [{
        "image_file": "default.png",
        "title": "TestTitle-10",
        "description": "TestDescription-10",
        "price": 100,
        "quantity": 100
    }]
    response = client.post('/admin/create_items', json.dumps(data), headers={"Authorization": admin_token_header})
    assert response.status_code == 201
    assert response.json()["DB Status"] == "Item Added Successfully"


def test_add_product_unauthorized_401(client):
    data = [{
        "image_file": "default.png",
        "title": "TestTitle-10",
        "description": "TestDescription-10",
        "price": 100,
        "quantity": 100
    }]
    response = client.post('/admin/create_items', json.dumps(data), headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 401
    assert "UnAuthorized User"


"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
"""
# Below are Update Products in Grocery NAME | PRICE | QUANTITY etc. Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 3 Nos

test_update_product_200: Successfully Updated Products           : 200
test_update_product_unauthorized_401: Except Admin. No Permission: 401
test_update_product_not_found_404: Item ID entered, Not Found    : 404
test_update_product_no_changes_302: No Updates Detected          : 302
"""


def test_update_product_200(client, admin_token_header):
    data = {
        "image_file": "default.png",
        "title": "TestTitle-10-updated",
        "description": "TestDescription-10-updated",
        "price": 200,
        "quantity": 200
    }
    response = client.put('admin/update_item/4', json.dumps(data), headers={"Authorization": admin_token_header})
    assert response.status_code == 200
    assert "Items Updated Successfully"


def test_update_product_unauthorized_401(client):
    data = {
        "image_file": "default.png",
        "title": "TestTitle-10-updated",
        "description": "TestDescription-10-updated",
        "price": 200,
        "quantity": 200
    }
    response = client.put('admin/update_item/4', json.dumps(data), headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 401
    assert "UnAuthorized User"


def test_update_product_not_found_404(client, admin_token_header):
    data = {
        "image_file": "default.png",
        "title": "TestTitle-10",
        "description": "TestDescription-10",
        "price": 200,
        "quantity": 200
    }
    response = client.put('/update_item/100', json.dumps(data), headers={"Authorization": admin_token_header})
    assert response.status_code == 404
    assert "Item Not Found"


def test_update_product_no_changes_302(client, admin_token_header):
    data = {
        "image_file": "default.png",
        "title": "TestTitle-10-updated",
        "description": "TestDescription-10-updated",
        "price": 200,
        "quantity": 200
    }
    response = client.put('admin/update_item/4', json.dumps(data), headers={"Authorization": admin_token_header})
    assert response.status_code == 302
    assert "No Changes Detected"


"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
"""
# Below are Delete Products Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 2 Nos

test_delete_product_200: Successfully Deleted Products           : 200
test_delete_product_unauthorized_401: Except Admin. No Permission: 401
test_delete_product_not_found_404: Item ID entered, Not Found    : 404
"""


def test_delete_product_200(client, admin_token_header):
    response = client.delete('/admin/delete_item/4', headers={"Authorization": admin_token_header})
    assert response.status_code == 200
    assert "Item Deleted Successfully"


def test_delete_product_unauthorized_401(client):
    response = client.delete('/admin/delete_item/4', headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 401
    assert "UnAuthorized User"


def test_delete_product_not_found_404(client, admin_token_header):
    response = client.delete('/admin/delete_item/100', headers={"Authorization": admin_token_header})
    assert response.status_code == 404
    assert "Item Not Found"


"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
"""
# Below are Viewing Customers Orders Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 1 Nos

test_view_orders_200: successfully fetch customers orders        : 200
test_view_orders_not_authorized_401: Except Admin. No Permission : 401
test_delete_product_not_found_404: Item ID entered, Not Found    : 404
"""


def test_view_orders_200(client, admin_token_header):
    response = client.get('/admin/view_orders', headers={"Authorization": admin_token_header})
    assert response.status_code == 200
    assert "Items Fetched Successfully"


def test_view_orders_not_authorized_401(client):
    response = client.get('/admin/view_orders', headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 401
    assert "Not Authorized"


"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
"""
# Below are Adding Discount Coupons Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 2 Nos

test_add_discount_coupon_200: successfully Adding Coupons        : 200
test_add_discount_coupon_not_authorized_401: No User Permission  : 401
test_add_discount_coupon_invalid_date_401: Invalid Date Entered  : 401
"""


# def test_add_discount_coupon_200(client, admin_token_header):
#     data = [{
#         "coupon_code": "CoDe",
#         "discount_percentage": 10,
#         "valid_till": 2030-12-12
#     }]
#     response = client.post('/admin/add_discount_coupon', json.dumps(data), headers={"Authorization": admin_token_header})
#     assert response.status_code == 200
#     assert response.json()['status'] == 'Coupons Added Successfully'


def test_add_discount_coupon_not_authorized_401(client):
    data = [{
        "coupon_code": "CoDe",
        "discount_percentage": 10,
        "valid_till": 2022-12-12
    }]
    response = client.post('/admin/add_discount_coupon', json.dumps(data), headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 401
    assert "Not Authorized"


def test_add_discount_coupon_invalid_date_401(client, admin_token_header):
    data = [{
        "coupon_code": "Grocery",
        "discount_percentage": 10,
        "valid_till": 2022-10-10
    }]
    response = client.post('/admin/add_discount_coupon', json.dumps(data), headers={"Authorization": admin_token_header})
    assert response.status_code == 401
    assert "Invalid Date Entered"


"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
"""
# Below are Viewing Discount Coupons Test Cases;
+ve Test Cases : Return --> Json Response                        - 1 Nos
-ve Test Cases : Raises --> HTTP Exception Error Messages        - 1 Nos

test_show_discount_coupon_200: successfully fetched Coupons      : 200
test_show_discount_coupon_not_authorized_401: No User Permission : 401
"""


def test_show_discount_coupon_200(client, admin_token_header):
    response = client.get('/admin/show_discount_coupon', headers={"Authorization": admin_token_header})
    assert response.status_code == 200
    assert "Discount Coupons Fetched Successfully"


def test_show_discount_coupon_not_authorized_401(client):
    response = client.get('/admin/show_discount_coupon', headers={"Authorization": "Bearer fake_token"})
    assert response.status_code == 401
    assert "Not Authorized"


"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""

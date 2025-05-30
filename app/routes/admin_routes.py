from flask import Blueprint, render_template, request, session, redirect, url_for, flash, Response
import os
from app.controller.admin_controller import authenticate_admin, user_list_controller, product_list_controller, orders_list_controller
from app.controller.database_collection_controller import getUsersCollection, getCategoriesCollection, getOrderedProductsCollection
import io
import csv
from bson.objectid import ObjectId
admin_route = Blueprint('admin_route', __name__)

# Admin credentials accessing 
admin_name = os.getenv("ADMIN_NAME")
admin_pass = os.getenv("ADMIN_PASS")

@admin_route.route("/admin-authenticate", methods=["POST"])
def admin_authentication():
    username = request.form['username']
    password = request.form['password']
    success, message = authenticate_admin(username, password)
    if success:
        session['admin_logged_in'] = True
        flash(message, "success")
        return redirect(url_for("admin_route.admin_dashboard"))
    else:
        flash(message, "danger")
        return redirect(url_for("admin_route.admin_login"))


@admin_route.route("/admin/dashboard")
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_route.admin_login'))
    else:
        # real user count from the database
        users_collection = getUsersCollection()
        total_users = users_collection.find()
        total_users = list(total_users)
        
        count = 0
        for user in total_users:
            count += 1
            user['_id'] = str(user['_id'])
            
            
        # Real categories count from the database
        categories_collection = getCategoriesCollection()
        total_category = categories_collection.find()
        total_category = list(total_category)
        
        countC = 0
        for category in total_category:
            countC += 1
            category['_id'] = str(category['_id'])
            
        # Orders Collections
        orders_collection = getOrderedProductsCollection()
        orders_data = orders_collection.find()
        orders_data = list(orders_data)
        
        count_O = 0
        for order in orders_data:
            count_O += 1
            order['_id'] = str(order['_id'])
            
        return render_template(
            "Components/Admin/dashboard.html",
            total_users = count,
            total_products = countC,
            total_orders = count_O
        )
    

@admin_route.route("/admin/login")
def admin_login():
    return render_template('Components/Admin/admin_login.html')

@admin_route.route("/admin/users-list")
def admin_users_list():
    users = user_list_controller()
    return render_template('Components/Admin/users-list.html', users = users)

@admin_route.route("/admin/products-list")
def admin_products_list():
    products = product_list_controller()
    return render_template('Components/Admin/products-list.html', products = products)

@admin_route.route("/admin/orders-list")
def admin_orders_list():
    orders = orders_list_controller()
    return orders


@admin_route.route("/admin/add-product", methods=["POST"])
def admin_add_product():
    name = request.form['name']
    price = float(request.form['price'])
    category = request.form['category']
    image = request.form['image']
    
    products_collection = getCategoriesCollection()
    
    new_product = {
        'name': name,
        'price': price,
        'category': category,
        'image': image
    }

    products_collection.insert_one(new_product)
    flash("Product Added Successfully", "success")
    return redirect(url_for("admin_route.admin_products_list"))

@admin_route.route("/admin/update-product/<product_id>",methods=["POST"])
def admin_update_products(product_id):
    print(product_id)
    products_collection = getCategoriesCollection()
    product = products_collection.find_one({'_id': ObjectId(product_id)})
    
    if not product:
        flash('Product not found', 'danger')
        return redirect(url_for('admin_route.admin_products_list'))    
        
    name = request.form['name']
    price = float(request.form['price'])
    category = request.form['category']
    image_url = request.form['image']
    
    updated_product = {
        'name' : name,
        'price' : price,
        'category': category,
        'image': image_url
    }
    
    products_collection.update_one({'_id':ObjectId(product_id)}, {"$set" : updated_product})
    flash('Product updated successfully!', 'success')
    return redirect(url_for('admin_route.admin_products_list'))
    
    

@admin_route.route('/admin/delete-product/<product_id>', methods=['POST'])
def admin_delete_product(product_id):
    products = getCategoriesCollection()
    result = products.delete_one({'_id': ObjectId(product_id)})
    if result.deleted_count == 0:
        flash('Failed to delete product.', 'danger')
    else:
        flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin_route.admin_products_list'))


@admin_route.route('/admin/orders/export/<format>')
def export_orders(format):
    orders_collection = getOrderedProductsCollection()

    # Use same filtering logic
    search = request.args.get("search", "")
    filter_query = {
        "$or": [
            {"user_name": {"$regex": search, "$options": "i"}},
            {"user_email": {"$regex": search, "$options": "i"}},
            {"payment_method": {"$regex": search, "$options": "i"}},
        ]
    } if search else {}

    orders_cursor = orders_collection.find(filter_query).sort("created_at", -1)
    orders = list(orders_cursor)

    for order in orders:
        order['_id'] = str(order['_id'])

    if format == 'csv':
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(['Order ID', 'User Name', 'Email', 'Payment Method', 'Status', 'Created At'])

        for order in orders:
            writer.writerow([
                order.get('_id'),
                order.get('user_name'),
                order.get('user_email'),
                order.get('payment_method'),
                order.get('delivery_status'),
                order.get('created_at').strftime('%Y-%m-%d %H:%M') if order.get('created_at') else ''
            ])

        response = Response(output.getvalue(), content_type='text/csv')
        response.headers['Content-Disposition'] = 'attachment; filename=orders.csv'
        return response

    return "Export format not supported", 400



@admin_route.route("/admin/orders/<order_id>/update-delivery-status", methods=["POST"])
def update_delivery_status(order_id):
    new_status = request.form.get("delivery_status")

    if new_status not in ["Processing", "On the Way", "Delivered"]:
        flash("Invalid status selected!", "danger")
        return redirect(url_for("admin_route.admin_orders_list"))

    orders_collection = getOrderedProductsCollection()
    orders_collection.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"delivery_status": new_status}}
    )

    flash("Delivery status updated to '{}'.".format(new_status), "success")
    return redirect(url_for("admin_route.admin_orders_list"))


@admin_route.route("/admin-logout")
def admin_logout():
    session.pop('admin_logged_in')
    success = True
    flash("You have been logged out", "success" if success else "danger")
    return redirect(url_for('default_route.home_page'))  
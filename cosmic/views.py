from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
from django.conf import settings
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required,user_passes_test
from django.forms import formset_factory
from django.db.models import Sum
from django.http import JsonResponse,HttpResponse
from django.template.loader import get_template
from django.contrib.auth.models import User, auth

import os
# Create your views here.

def is_admin(user):
    return user.is_superuser

def create_customer(request):
    
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.errors:
            print(form.errors)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                print(f"Error: {e}")
            return redirect('create_customer')
    
    else:
        
        form = CustomerForm()
    return render(request, 'create_customer.html', {'form': form })

def display_customer(request):
    if request.method == 'GET':
        customers = cosmic_customer_profile.objects.all()
        context = {
                    'my_customer': customers,
                }
          
        return render(request, 'display_customer.html', context)

def display_customer_profile(request):
    if request.method == 'GET':
        name = request.GET['customer_name']
        
        customers = customer_profile.objects.get(customer_name= name)
         
        context = {
                        
                        'my_customer': customers,
                    }
    return render(request, 'customer_profile.html', context)       

def create_supplier(request):
    
    if request.method == 'POST':
        form = SupplierForm(request.POST)
       
        if form.is_valid():
            form.save()
            return redirect('create_supplier')
    
    else:
        
        form = SupplierForm()
    return render(request, 'create_supplier.html', {'form': form })

def display_supplier(request):
    if request.method == 'GET':
        customers = supplier_profile.objects.all()
        context = {
                    'my_supplier': customers,
                }
          
        return render(request, 'display_supplier.html', context)

def display_supplier_profile(request):
    if request.method == 'GET':
        name = request.GET['supplier_name']
        
        suppliers = supplier_profile.objects.get(supplier_name= name)
         
        context = {
                        
                        'my_supplier': suppliers,
                    }
    return render(request, 'supplier_profile.html', context) 

def create_order(request):
    if request.method == 'POST':
        form = CosmicOrderForm(request.POST)
        print(form.data)
        if form.errors:
            print(form.errors) 

        if form.is_valid():
            print(form.data,"val")
            customers_name = request.POST.get('customer_name') 
            customer = customer_profile.objects.get(customer_name=customers_name)
            form.instance.customer_name = customer
            form.save()
            return redirect('create_order')  # Redirect to the list of purchases or any other desired view
        else:
            print(form.data,"nval")
            errors = dict(form.errors.items())
            return JsonResponse({'form_errors': errors}, status=400)
        
    form = CosmicOrderForm()
    formset = OrderItemForm()

    return render(request, 'create_order.html', {'form': form, 'formset': formset, 'customers': customers,'suppliers':suppliers})

def display_order(request):
    if request.method == 'GET':
        orders = cosmic_order.objects.all()
        orders = orders.order_by('order_no')

        orders_data = []
        for order in orders:
            # Fetch all order items related to each cosmic order
            order_items = order_item.objects.filter(order_no=order.order_no)

            # Create a dictionary containing order details and items
            order_data = {
                'order_no': order.order_no,
                'date': order.date,  # Assuming 'date' is a field in CosmicOrder
                'order_items': order_items,  # Assuming a related name 'order_items' on CosmicOrder pointing to OrderItem
                'PR_before_vat': order.PR_before_vat,  # Assuming 'PR_before_vat' is a field in CosmicOrder
                'total_quantity': order.total_quantity,  # Assuming 'total_quantity' is a field in CosmicOrder
                'customer_name': order.customer_name,  # Assuming 'customer_name' is a field in CosmicOrder
                'status': order.status,  # Assuming 'status' is a field in CosmicOrder
            }
            orders_data.append(order_data)

    context = {
        'my_order': orders_data,
    }
    return render(request, 'display_order.html', context)

def create_order_items(request):
    
    if request.method == 'POST':
        formset = formset_factory(OrderItemForm, extra=1, min_num=1)
        
        formset = formset(request.POST or None,prefix="items")
        #print(formset.data,"r")
      
        if formset.errors:
            print(formset.errors)   
        
        # Check if 'PR_no' field is empty in each form within the formset
        for form in formset:
            print(form,"form")
        non_empty_forms = [form for form in formset if form.cleaned_data.get('item_name')]
       
        if non_empty_forms:
            print("yes")
            if formset.is_valid():
                final_quantity = 0.0
                pr_no = request.POST.get('order_no')
                print(pr_no,"pr")
                pr = cosmic_order.objects.get(order_no = pr_no)
                for form in non_empty_forms:
                    form.instance.remaining = form.cleaned_data['quantity']
                    form.instance.order_no = pr
                    final_quantity += form.cleaned_data['quantity']
                    
                    form.save()
                
                pr.total_quantity = final_quantity
                pr.remaining = final_quantity
                pr.save()
                #message.success("successful!")
            else:
                print(formset.data,"nval")
                errors = dict(formset.errors.items())
                return JsonResponse({'form_errors': errors}, status=400)
        
            pr_form = CosmicOrderForm(prefix="orders")
            formset = formset_factory(OrderItemForm, extra=1)
            formset = formset(prefix="items")

            context = {
                'pr_form': pr_form,
                'formset': formset,
                # 'message':success_message,
            }
            return render(request, 'create_order.html', context)
    else:
       
        formset = formset_factory(OrderItemForm, extra=1)
        formset = formset(prefix="items")

    context = {
        'formset': formset,
    }
    return render(request, 'create_order.html', context)

def display_single_order(request):
    if request.method == 'GET':
        pr_no = request.GET['order_no']
        orders = cosmic_order.objects.get(order_no=pr_no)
        pr_items = order_item.objects.all()
        pr_items = pr_items.filter(order_no=pr_no)
            
        
        if pr_items.exists():
            print(pr_items,"yes")
            context = {
                        'pr_items': pr_items,
                        'my_order': orders,
                    }
            return render(request, 'display_single_order.html', context)
        context = {
                        
                        'my_order': orders,
                    }
    return render(request, 'display_single_order.html', context)

def create_shipping(request):
    if request.method == 'POST':
        ship_form = ShippingForm(request.POST)
        number = request.POST.get('order_no') 
        if ship_form.errors:
            print(ship_form.errors) 
        if ship_form.is_valid():
            
            print(ship_form.data,"val")
            print(number) # Assuming you have a field with supplier_id in your form
            order = cosmic_order.objects.get(order_no=number)
            
            ship_form.instance.order_no = order
            
            ship_form.save()
            return redirect('shipping_details')  # Redirect to the list of purchases or any other desired view
        else:
            print(form.data,"nval")
    
        
    form = ShippingForm()
    formset = formset_factory(OrderItemForm, extra=1)
    formset = formset(prefix="items")

    # Render the form with the supplier choices
    customers = cosmic_customer_profile.objects.all()
    return render(request, 'shipping_details.html', {'form': form, 'formset': formset, 'customers': customers})

@login_required 
@user_passes_test(is_admin)
def order_approval(request):
    # Your custom logic here (e.g., fetching data)
    if not is_admin(request.user):
        # User is not authenticated to access this view
        messages.error(request, "You are not authorized to access this page.")
        return redirect('login')

    pending_orders = cosmic_order.objects.filter(status='Pending')
    # Handle form submission
    
    if request.method == 'POST':
        form = approvalForm(request.POST)
        if form.errors:
            print(form.errors)
        if form.is_valid():
            action = form.cleaned_data['action']
            approval_name = form.cleaned_data['approval']
            
            if action == 'approve':
                for pr_no in form.cleaned_data['selected_orders']:
                    stats = request.POST.get(f"{pr_no}_status")
                    purchase_order = cosmic_order.objects.get(order_no=pr_no.order_no)
                    purchase_order.status = 'approved'
                    purchase_order.approved_by = approval_name
                    purchase_order.save()
            elif action == 'reject':
                for pr_no in form.cleaned_data['selected_orders']:
                    purchase_order = cosmic_order.objects.get(order_no=pr_no.order_no)
                    purchase_order.status = 'rejected'
                    purchase_order.approved_by = approval_name
                    purchase_order.save()
            return redirect('order_approval')

    else:
        form = approvalForm()

    context = {
        'pending_orders': pending_orders,
        'form': form,
    }
    return render(request, 'admin/order_approval.html', context)

@login_required 
@user_passes_test(is_admin)
def order_status(request):
    # Your custom logic here (e.g., fetching data)
    if not is_admin(request.user):
        # User is not authenticated to access this view
        messages.error(request, "You are not authorized to access this page.")
        return redirect('login')

    pending_orders = cosmic_order.objects.filter(status='Pending')
    # Handle form submission
    
    if request.method == 'POST':
        form = approvalForm(request.POST)
        if form.errors:
            print(form.errors)
        if form.is_valid():
            action = form.cleaned_data['action']
            approval_name = form.cleaned_data['approval']
            
            if action == 'approve':
                for pr_no in form.cleaned_data['selected_orders']:
                    stats = request.POST.get(f"{pr_no}_status")
                    purchase_order = cosmic_order.objects.get(order_no=pr_no.order_no)
                    purchase_order.status = stats
                    purchase_order.approved_by = approval_name
                    purchase_order.save()
          
            return redirect('order_status')

    else:
        form = approvalForm()

    context = {
        'pending_orders': pending_orders,
        'form': form,
    }

   
    return render(request, 'admin/order_status.html', context)

def edit_order(request):

    if request.method == 'GET':
        order_no = request.GET.get('order_no')
        cosmic_order_instance = get_object_or_404(cosmic_order, order_no=order_no)
        items = order_item.objects.all()
        item = items.filter(order_no=cosmic_order_instance)
        item_names = []
        for name in item:
            item_names.append(name.item_name)
        print(item_names,"item")
        form = EditOrderForm(instance=cosmic_order_instance)  # Initialize the form with the instance data
        # ItemInlineFormset = inlineformset_factory(
        #     cosmic_order,  # Parent model
        #     order_item,    # Child model
        #     fields=('item_name', 'price', 'quantity'),
        #     extra=1       # Number of extra forms
        # )
        #formsets = ItemInlineFormset(instance=cosmic_order_instance,prefix='items')


        ship_form = ShippingForm(prefix="ship")
        customers = customer_profile.objects.all()
        last_shipping_info = shipping_info.objects.order_by('-invoice_num').first()
        print(last_shipping_info.invoice_num, "info")
        last_number = int(last_shipping_info.invoice_num.split('-')[-1]) if last_shipping_info else 0
        print(last_number,"last")
        new_number = last_number + 1
        generated_invoice_num = f"INV-{new_number:03d}"
        print(generated_invoice_num,"num")
        
    if request.method == 'POST':
        form = CosmicOrderForm(request.POST)
        

        order_no = request.POST.get('order_no')
        cosmic_order_instance = get_object_or_404(cosmic_order, order_no=order_no)
        # ItemInlineFormset = inlineformset_factory(
        #     cosmic_order,
        #     order_item,
        #     fields=('measurement', 'item_name', 'price', 'quantity'),
        #     extra=1
        # )
        # formset = ItemInlineFormset(request.POST, instance=cosmic_order_instance,prefix='items')
        # print(formset,"formset")
        #formset.management_form[ItemInlineFormset.TOTAL_FORM_COUNT] = len(formset.forms)
        # formset.management_form[ItemInlineFormset.INITIAL_FORM_COUNT] = formset.initial_form_count()
        # print(formset.management_form.cleaned_data) order_item_set-0-item_name

        #print(form,"valid")
        # Update the instance with form data and save it
        refs_no = request.POST.get('ref_no')
        cosmic_order_instance.ref_no = refs_no
        cosmic_order_instance.measurement_type = request.POST.get('measurement_type')
        cosmic_order_instance.shipment_type = request.POST.get('shipment_type')
        cosmic_order_instance.freight = request.POST.get('freight')
        cosmic_order_instance.payment_type = request.POST.get('payment_type')
        cosmic_order_instance.transporation = request.POST.get('transporation')
        cosmic_order_instance.country_of_origin = request.POST.get('country_of_origin')
        cosmic_order_instance.final_destination = request.POST.get('final_destination')
        cosmic_order_instance.port_of_discharge = request.POST.get('port_of_discharge')
        cosmic_order_instance.port_of_loading = request.POST.get('port_of_loading')
        consignees = request.POST.get('consignee')
        consignee = customer_profile.objects.get(customer_name=consignees)
        cosmic_order_instance.consignee = consignee
        print(cosmic_order_instance.consignee,"instance")
        notify_partys = request.POST.get('notify_party')
        notify_party = customer_profile.objects.get(customer_name=notify_partys)
        cosmic_order_instance.notify_party = notify_party
        notify_party2s = request.POST.get('notify_party2')
        try:
        
            notify_party2 = customer_profile.objects.get(customer_name=notify_party2s)
            cosmic_order_instance.notify_party2 = notify_party2
        except customer_profile.DoesNotExist:
            cosmic_order_instance.notify_party2  = None
        
        
        cosmic_order_instance.save()
       
        my_customers = request.POST.get('customer_name')
        suppliers = request.POST.get('supplier_name')
        customer = customer_profile.objects.get(customer_name=my_customers)
        cosmic_order_instance.customer_name = customer
        supplier = supplier_profile.objects.get(supplier_name=suppliers)
        cosmic_order_instance.supplier_name = supplier
        print(cosmic_order_instance.__dict__) 
        cosmic_order_instance.save()
        return redirect('success')  # Redirect to a success page or another URL
    
    formset = formset_factory(InvoiceItemForm, extra=1)
    formset = formset(prefix="items")
    
    return render(request, 'shipping_details.html', {'form': form, 'formset':formset, 'ship_form': ship_form,
                                               'cosmic_order_instance': cosmic_order_instance, 'item_names':item_names,
                                               'customers': customers,'new_inv':generated_invoice_num, 'item':item})
def print_order(request):
    if request.method == 'GET':
        pr_no = request.GET['order_no']
        try:
            orders = cosmic_order.objects.get(order_no=pr_no)
            pr_items = order_item.objects.all()
            pr_items = pr_items.filter(order_no=pr_no)
            print(pr_items)
        except cosmic_order.DoesNotExist:
            try:
                print("trial")
                orders = cosmic_purchase.objects.get(purchase_no=pr_no)
                
                pr_items = purchase_item.objects.all()
                pr_items = pr_items.filter(purchase_no=pr_no)
                print(pr_items)
            except cosmic_purchase.DoesNotExist:
                orders = None
        
        
        if hasattr(orders, 'PR_before_vat'):
            number = float(orders.PR_before_vat)
            print("yes")
        else:
            number = float(orders.before_vat)
            print(orders.before_vat)

        
        if pr_items.exists():
            print(pr_items,"yes")
            context = {
                        'pr_items': pr_items,
                        'my_order': orders,
                        'num': num,
                        'number':number,
                        # 'shipping':shipping,
                    }
            return render(request, 'print_order.html', context)
       
        context = {
                        
                        'my_order': orders,
                        'num': num,
                        'number':number,
                        # 'shipping':shipping,
                    }
       
    return render(request, 'print_order.html', context)

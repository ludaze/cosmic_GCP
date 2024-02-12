from django import forms
from .models import *

class CustomerForm(forms.ModelForm):
    
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'phone_number form-control' }))
    customer_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'customer_address form-control'}))

    customer_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter e-mail'}),
    )
    
    class Meta:
   
        model = customer_profile
        fields = ['customer_name','customer_address','email','phone_number','contact_person','comments']

class SupplierForm(forms.ModelForm):
    #phone_number = 
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'phone_number form-control' }))
    supplier_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'customer_address form-control'}))

    supplier_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter e-mail'}),
    )
    
    class Meta:
   
        model = supplier_profile
        fields = ['supplier_name','supplier_address','email','phone_number','contact_person','comments']

class CosmicOrderForm(forms.ModelForm):
    
    order_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'order_no form-control'}))

    class Meta:
   
        model = cosmic_order
        fields = ['freight_price','customer_name','supplier_name','order_no','date','payment_type','measurement_type','approved_by','PR_before_vat','total_quantity','transportation','shipment_type','freight','ref_no','notify_party','country_of_origin','final_destination','port_of_discharge','port_of_loading','notify_party2','consignee']
        
class OrderItemForm(forms.ModelForm):
   
    before_vat = forms.DecimalField(
        label='Total Price',
        required=False,
        widget=forms.TextInput(attrs={'class': 'before_vat form-control', 'readonly': 'readonly'})
    )
    measurement = forms.CharField(widget=forms.TextInput(attrs={'class': 'measurement form-control'}), required=False)
    quantity = forms.FloatField(widget=forms.TextInput(attrs={'class': 'quantity form-control' }))
    price = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'price form-control'}))

    item_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
    )
    
    
    class Meta:
   
        model = order_item
        fields = [ 'item_name','price','quantity','before_vat','measurement']

class CosmicPurchaseForm(forms.ModelForm):
    
    purchase_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'purchase_no form-control'}))

    class Meta:
   
        model = cosmic_purchase
        fields = ['supplier_name','purchase_no','date','payment_type','measurement_type','before_vat','transportation','shipment_type']

class ShippingForm(forms.ModelForm):
    
    class Meta:
   
        model = shipping_info
        fields = [ 'invoice_num','final_price','waybill_remark','packing_remark','lading_remark', 'invoice_remark','customer_no','invoice_date','vessel','container_no','truck_waybill_no']

class EditOrderForm(forms.ModelForm):
    
    total_quantity = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'total_quantity form-control' }),required=False)
    order_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'order_no form-control'}))

    
    class Meta:
   
        model = cosmic_order
        fields = ['customer_name','supplier_name','order_no','date','payment_type','measurement_type','approved_by','PR_before_vat','total_quantity','transportation','shipment_type','freight','ref_no','notify_party']
        exclude = ['order_no'] 

class approvalForm(forms.Form):
    selected_orders = forms.ModelMultipleChoiceField(
        queryset= cosmic_order.objects.filter(status='Pending'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    action = forms.ChoiceField(
        choices=[('approve', 'Approve'), ('reject', 'Reject')],
        widget=forms.RadioSelect,
    )
    approval = forms.CharField(
        widget=forms.TextInput,
        required=True 
    )

class InvoiceItemForm(forms.ModelForm):
   
    before_vat = forms.DecimalField(
        label='Total Price',
        required=False,
        widget=forms.TextInput(attrs={'class': 'before_vat form-control', 'readonly': 'readonly'})
    )
    measurement = forms.CharField(widget=forms.TextInput(attrs={'class': 'measurement form-control'}), required=False)
    quantity = forms.FloatField(widget=forms.TextInput(attrs={'class': 'quantity form-control' }))
    price = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'price form-control'}))
    bags = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'bags form-control'}))
    net_weight = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'net_weight form-control'}))
    gross_weight = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'gross_weight form-control'}))
    
    item_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name','size':'20'}),
    )
    hs_code = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'HS-CODE'}),
    )
    
    class Meta:
   
        model = invoice_item
        fields = ['item_name','hs_code','price','quantity','before_vat','measurement','bags','net_weight','gross_weight']

class restoreForm(forms.Form):
    selected_orders = forms.ModelMultipleChoiceField(
        queryset= cosmic_order.objects.filter(status='rejected'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    action = forms.ChoiceField(
        choices=[('approve', 'Approve'), ('delete', 'Delete'),('restore', 'Restore')],
        widget=forms.RadioSelect,
    )
    approval = forms.CharField(
        widget=forms.TextInput,
        required=True 
    )
class CosmicPurchaseForm(forms.ModelForm):
    
    total_quantity = forms.FloatField(widget=forms.TextInput(attrs={'class': 'total_quantity form-control' }),required=False)
    purchase_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'purchase_no form-control'}))

class CosmicItemForm(forms.ModelForm):
    
    item_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'item_name form-control'}))
    hs_code = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'hs_code form-control'}))
    
    class Meta:
   
        model = item_codes
        fields = ['item_name','hs_code']
        

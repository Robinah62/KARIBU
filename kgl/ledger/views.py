from django.shortcuts import render, redirect, get_object_or_404
# accessing all our models
from django.urls import reverse
from.models import *
from.forms import *
from django.db.models import Sum, Q
# borrowing decoretars from django so that we can restrict ou views

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.
#view for indexpage
def index(request):
    
    return render(request, "ledger/index.html")

#view for receiptpage
#@login_required
def receipt(request):
    sales = Sale.objects.all().order_by('-id')
    return render(request, 'ledger/receipt.html', {'sales':sales})

#view for addsales

def addsales(request):
    if request.method == 'POST':
        form = AddSaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('allsales')  # go back to allsales after saving
    else:
        form = AddSaleForm()
    return render(request, 'ledger/addsales.html', {'form': form})

#view for addstock

def addstock(request):
    if request.method == 'POST':
        form = UpdateStockForm(request.POST)
        if form.is_valid():
            # Handle adding stock logic
            added_quantity = int(request.POST['received_quantity'])
            item = form.save(commit=False)
            item.total_quantity += added_quantity
            item.save()
            return redirect('allstock')  # After adding stock, redirect to stock list page
    else:
        form = UpdateStockForm()

    return render(request, 'ledger/addstock.html', {'form': form})
#view all sales
def allsales(request):
    sales = Sale.objects.all()  # fetch all sales from the database
   
    return render(request, 'ledger/allsales.html', {'sales':sales})

#view all stock
def allstock(request):
    stocks =Stock.objects.all().order_by('-id')
    
    return render(request, 'ledger/allstock.html',{'stocks':stocks})


    

#view to handle a link for a particular item to sell an item
def  stockdetail(request, stock_id):
    stock =Stock.objects.get(id=stock_id)
    return render(request, 'ledger/stockdetail.html',{'stock':stock})

def issue_item(request,pk):
    #creating a variable issued item and access all entries in the stock model by their id
    issued_item= Stock.objects.get(id=pk)
    #accessing our form from forms.py
    sales_form =AddSaleForm(request.POST)
    
    if request.method== 'POST':

       if sales_form.is_valid():
            new_sale =sales_form.save(commit = False)
            new_sale.item_name = issued_item
            new_sale.unit_price = issued_item.unit_price
            new_sale.save()
            #To keep track of the stock after sales
            issued_quantity =int(request.POST['quantity'])
            issued_item.total_quantity -= issued_quantity
            issued_item.save()
            print(issued_item.item_name)
            print(request.POST['quantity'])
            print(issued_item.total_quantity)

            return redirect('receipt')
    return render(request, 'ledger/issue_item.html',{'sales_form':sales_form, 'issued_item':issued_item})

def receipt_detail(request, receipt_id):
    receipt = Sale.objects.get(id=receipt_id)
    return render(request, 'ledger/receipt_detail.html',{'receipt':receipt})

# view for loging in
def Login(request):
    if request.method =="POST":
        username =request.POST['username']
        password = request.POST['password']
        user =authenticate(request, username = username,password=password)
        if user is not None and user.is_owner==True:
            form =login(request,user)
            return redirect('/dashboard1')
        
        if user is not None and user.is_manager==True:
            form =login(request,user)
            return redirect('/dashboard2')
        
        if user is not None and user.is_salesagent==True:
            form =login(request,user)
            return redirect('/dashboard3')
        else:
            print("Sorry!, something went wrong")
    form = AuthenticationForm()
    return render(request, 'ledger/login.html',{"form":form})
# view for signup
def signup(request):
    if request.method == 'POST':
        form = UserCreation(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            return redirect('/login')
    else:
        form = UserCreation()
    return render(request, 'ledger/signup.html', {'form':form}) 

#def owner(request):
    return render(request, 'ledger/dashboard1.html')   
   


def manager(request):
    # Define a threshold for low stock
    low_stock_threshold = 10

    # Get all stock items where the quantity is below the threshold
    low_stock_items = Stock.objects.filter(total_quantity__lt=low_stock_threshold)

    # Pass the low stock items to the template
    return render(request, 'ledger/dashboard2.html', {'low_stock_items': low_stock_items})

def salesagent(request):
    return render(request, 'ledger/dashboard3.html')

def create_credit_sale(request):
    if request.method == 'POST':
        form = CreditSaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('credit_sale_list')  # after saving, go to list page
    else:
        form = CreditSaleForm()
    return render(request, 'ledger/create_credit_sale.html', {'form': form})

def credit_sale_list(request):
    credit_sales = CreditSale.objects.all()
    return render(request, 'ledger/credit_sale_list.html', {'credit_sales': credit_sales})


# calculating the totals
#@login_required
def owner_dashboard(request):
    # 1. Total Cash Sales
    total_cash_sales = Sale.objects.filter(payment_method='Cash').aggregate(
        total_cash=Sum('amount_received')
    )['total_cash'] or 0

    # 2. Total Credit Sales
    total_credit_sales = CreditSale.objects.aggregate(
        total_credit=Sum('amount_due')
    )['total_credit'] or 0

    # 3. Total Sales = Cash + Credit
    total_sales = total_cash_sales + total_credit_sales

    # 4. Total Stock Remaining
    total_stock = Stock.objects.aggregate(
        total_quantity=Sum('total_quantity')
    )['total_quantity'] or 0

    context = {
        'total_sales': total_sales,
        'total_credit_sales': total_credit_sales,
        'total_stock': total_stock,
    }
    return render(request, 'ledger/dashboard1.html', context)


def edit_stock(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    
    if request.method == 'POST':
        # Get category_name from the form (which will now be hidden)
        category_name_from_form = request.POST.get('category_name')
        
        # Find the Category instance from the database using the category_name
        category = Category.objects.get(category_name=category_name_from_form)
        
        # Update the stock fields
        stock.category_name = category  # Set the Category object
        stock.item_name = request.POST.get('item_name')
        stock.total_quantity = request.POST.get('total_quantity')
        stock.unit_price = request.POST.get('unit_price')
        stock.save()
        
        # Redirect to stock detail after update
        return redirect('stockdetail', stock_id=stock.pk)
    
    return render(request, 'ledger/edit_stock.html', {'stock': stock})

# delete view

def delete_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    if request.method == 'POST':
        stock.delete()
        return redirect('allstock')  # change if your stock list URL has a different name
    return render(request, 'ledger/delete_stock.html', {'item': stock})

def delete_sale(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    if request.method == 'POST':
        sale.delete()
        return redirect('allsales')  # change if your sales list URL has a different name
    return render(request, 'ledger/delete_sale.html', {'item': sale})
"""
URL configuration for kgl project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# accessing the views file from our application
from ledger import views
# borrowing the functionality of login from django
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    #below is the url for index page  
    path('',views.index, name='index'),

    #below is the url for sales page
    path('receipt/',views.receipt, name='receipt'),

    #url for stock page
    path('addsales/',views.addsales, name='addsales'),

    # url for receipt
    path('allsales/',views.allsales, name='allsales'),

    # url for all sales
    path('addstock/',views.addstock, name='addstock'),

    # url for add stock
    path('allstock/',views.allstock, name='allstock'),

    # handling a url for a particular url checkout item
    
    path('home/<int:stock_id>/',views.stockdetail, name="stockdetail"),
     # handling a url for a particular sell item
    path('issue_item/<str:pk>/', views.issue_item, name='issue_item'),

    path('receipt_detail/<int:receipt_id>/', views.receipt_detail, name='receipt_detail'),
    path('', auth_views.LoginView.as_view(template_name='ledger/login.html'), name='login'),
    # url for log out
    path('logout/', auth_views.LogoutView.as_view(template_name='ledger/logout.html'), name='logout'),
    path('login/', views.Login, name='Login'),
    # url for sign up
    path('signup/', views.signup, name='signup'),

    
    # url for manager
    path('dashboard2/', views.manager, name="manager"),
    path('dashboard3/', views.salesagent, name="salesagent"),

    path('create_credit_sale/', views.create_credit_sale, name='create_credit_sale'),
    path('credit_sales_list/', views.credit_sale_list, name='credit_sale_list'),
    path('dashboard1/', views.owner_dashboard, name='owner_dashboard'),
    path('edit_stock/<int:pk>/', views.edit_stock, name='edit_stock'),
    path('delete_stock/<int:stock_id>/', views.delete_stock, name='delete_stock'),
    path('delete_sale/<int:sale_id>/', views.delete_sale, name='delete_sale'),
    path('add_stock/', views.add_stock, name='add_stock'),
    path('edit-sale/<int:pk>/', views.edit_sale, name='edit_sale'),
]


 




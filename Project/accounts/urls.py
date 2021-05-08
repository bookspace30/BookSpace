from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
#     path('register/', views.registerPage, name="register"),
#     path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('login/', views.loginPage2, name="login"),
    path('signup/', views.registerPage2, name="signup"),

    path('', views.home, name="home"),

    path('home/', views.home, name="home"),
    path('user/', views.userPage, name="user-page"),

    path('account/', views.accountSettings, name="account"),
    path('orderdetails/', views.orderdetails, name="orderdetails"),

    path('products/', views.products, name='products'),
    path('customer/<str:pk_test>/', views.customer, name="customer"),

    path('aboutus/', views.aboutus, name='aboutus'),
    path('contactus/', views.index, name='contactus'),
    path('donate/', views.donate, name='donate'),
    path('shop/', views.shop, name='shop'),
    path('addtocart/', views.addtocart, name='addtocart'),
    path('comingsoon/', views.comingsoon, name='comingsoon'),

    path('halloffame/', views.halloffame, name='halloffame'),
    path('accountdetails/', views.accountdetails, name='accountdetails'),
    path('faq/', views.faq, name='faq'),
    path('privacy/', views.privacy, name='privacy'),
    path('license/', views.license, name='license'),


    path('createorder/<str:pk>/', views.createOrder, name="createorder"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
         name="password_reset_complete"),

    path('store/', views.store, name="store"),

    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),

    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),

    path("productdetail/<str:pk_test>/", views.productdetail, name="productdetail"),
    path('buynow/<str:pk_test>/', views.buynow, name="buynow"),


]

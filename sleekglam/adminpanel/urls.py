from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

urlpatterns = [
   path('adminlogin',views.adminslogins,name='adminlogin'),
   path('adminhome',views.adminhome,name='adminhome'),
   path('adminlogout',views.adminlogout,name='adminlogout'),
   path('user',views.users,name='user'),
   path('<int:id>',views.blockuser,name='block'),

   path('category_list/',views. CategoriesListView.as_view(),name='category_list'),
   path('category_create',views.CategoryCreate.as_view(),name='category_create'),
   path('category_update/<slug:pk>',views.CategoryUpdate.as_view(),name='category_update'),
   path('category_delete/<slug:pk>',views.CategoryDelete.as_view(),name='category_delete'),
   
  
   
   path('subcategory_list',views.SubCategoriesListView.as_view(),name='subcategory_list'),
   path('subcategory_create',views.SubCategoryCreate.as_view(),name='subcategory_create'),
   path('subcategory_update/<slug:pk>',views.SubCategoryUpdate.as_view(),name='subcategory_update'),
   path('subcategory_delete/<slug:pk>',views.SubCategoryDelete.as_view(),name='subcategory_delete'), 
   
   
   path('product',views.products,name='products_view'),
   path('add_product',views.add_product,name='add_product'),
   path('product_update/<int:id>',views.ProductUpdate,name='update'),
   path('delete_product/<int:id>', views.productdelete, name='prodelete'),
   
   path('order_management',views.order_management,name='order_management'),
   path('order_detail/<int:order_id>/',views.order_detail,name='order_detail'),
   
   path('add_banner',views.add_banner,name='add_banner'),
   path('banner',views.banners,name='banners'),
   path('banner/<int:banner_id>',views.delete_banner,name='banners'),
   path('update_banner/<int:id>',views.update_banner,name='update_banner'),
   
   path('add_coupon',views.add_coupon,name='add_coupon'),
   path('coupon_list',views.coupon_list,name='coupon_list'),
   path('coupon_edit/<int:id>',views.coupon_edit,name='coupon_edit'),
   path('coupon_disable/<int:id>',views.coupon_disable,name='coupon_disable'),
   path('add_cate_offer',views.add_cate_offer,name='add_cate_offer'),
   path('cat_list',views. cat_list,name='cat_list'),
   path('pro_list',views.pro_list,name='pro_list'),
   path('cat_offer_edit/<int:cat_id>',views.cat_offer_update,name='cat_offer_edit'),
   path('cat_offer_delete/<int:cat_id>',views.cat_offer_delete,name='cat_offer_delete'),
   path('add_pro_offer',views.add_pro_offer,name='add_pro_offer'),
   path('product_offer_delete/<int:pro_id>',views.product_offer_delete,name='product_offer_delete'),
   
   path('sales_report_date',views.sales_report_date,name='sales_report_date'),

   path('export_to_excel',views.export_to_excel,name='export_to_excel'),
   path('export_to_pdf',views.export_to_pdf,name='export_to_pdf'),
   path(' monthly_export_to_csv',views.monthly_export_to_csv,name='monthly_export_to_csv')
   # path('monthly_sales',views.monthly_sales,name='monthly_sales'),
   # path('export_to_excel1',views.export_to_excel1,name='export_to_excel1'),
   # path('export_to_pdf1',views.export_to_pdf1,name='export_to_pdf1'),
   
   
   
   
   
   
   
   
   
   
]
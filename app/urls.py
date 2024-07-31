from django.urls import path
from . import views

urlpatterns = [
	path('', views.home,name="home"),
	path('register/', views.register,name="register"),
    path('worker_register/',views.worker_register,name='worker_register'),
	path('Login/', views.user_login,name="user_login"),
	path('farmer_login/', views.farmer_login,name="farmer_login"),
	path('add_job/', views.add_job,name="add_job"),
    path('add_tractor/',views.add_tractor,name='add_tractor'),
	path('employee/', views.employee,name="employee"),
	path('delete_job/<int:pk>', views.delete_job,name="delete_job"),
	path('add_land/', views.add_land,name="add_land"),
	path('lands/', views.lands,name="lands"),
    path('view_tractor_details/',views.view_tractor_details,name='view_tractor_details'),
	path('edit_land/<int:pk>', views.edit_land,name="edit_land"),
	path('delete_land/<int:pk>', views.delete_land,name="delete_land"),
	path('logout/', views.logout,name="logout"),
	path('apply_job/', views.apply_job,name="apply_job"),
	path('apply/<int:pk>', views.apply,name="apply"),
	path('delete_land/<int:pk>', views.delete_land,name="delete_land"),
	path('job_details/', views.job_details,name="job_details"),
	path('user_logout/', views.user_logout,name="user_logout"),
	path('sale_land/', views.sale_land,name="sale_land"),
	path('enquiry/<int:pk>/<int:fid>/', views.enquiry,name="enquiry"),
	path('shortlist/', views.shortlist,name="shortlist"),
	path('accept/<int:pk>', views.accept,name="accept"),
	path('reject/<int:pk>', views.reject,name="reject"),
	path('edit_hire/<int:pk>', views.edit_hire,name="edit_hire"),
	path('farmer_land_sale/', views.farmer_land_sale,name="farmer_land_sale"),
	path('update_sale/<int:pk>/<int:land_id>/', views.update_sale,name="update_sale"),
	path('employee_attendance/', views.employee_attendance,name="employee_attendance"),
	path('show_attendance/', views.show_attendance,name="show_attendance"),
	path('employee_salary/', views.employee_salary,name="employee_salary"),
	path('calculate_salary/', views.calculate_salary,name="calculate_salary"),
	path('enquiry_land/', views.enquiry_land,name="enquiry_land"),
    path('worker_daily_attendance',views.worker_daily_attendance,name='worker_daily_attendance')




]

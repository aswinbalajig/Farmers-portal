from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages
import datetime
from django.db.models import Q
from django.db import connection
import random 
from django.db.models import Sum, Count
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.utils import timezone
def home(request):
	return render(request,'index.html',{})

def register(request):
	if request.method == 'POST':
		Name = request.POST.get('uname')
		Adddress = request.POST.get('address')
		Mobile= request.POST.get('mobile')
		Email = request.POST.get('email')
		Password = request.POST.get('pwd')
		utype = request.POST.get('user_type')
		crt = Register_Detail.objects.create(name=Name,
		address=Adddress,mobile=Mobile,password=Password,email=Email,user_type=utype)
		if crt:
			messages.success(request,'Registered Successfully')
	return render(request,'register.html',{})

def worker_register(request):
	if request.method == 'POST':
		name = request.POST.get('uname')
		email = request.POST.get('email')
		mobile= request.POST.get('mobile')
		username=request.POST.get('Username')
		password = request.POST.get('pwd')
		experience=request.POST.get('Experience')
		address = request.POST.get('address')
		crt = Worker_Detail.objects.create(name=name,
		address=address,mobile=mobile,password=password,email=email,username=username,experience=experience)
		if crt:
			messages.success(request,'Worker Registered Successfully')
	return render(request,'worker_register.html',{})

def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =  request.POST.get('password')
		user_type = request.POST.get('user_type')
		post = Register_Detail.objects.filter(name=username,password=password,user_type=user_type) or Worker_Detail.objects.filter(username=username,password=password,user_type=user_type)
		if post:
			if user_type == 'worker':
				username = request.POST.get('username')
				request.session['worker'] = username
				a = request.session['worker']
				sess = Worker_Detail.objects.only('id').get(name=a).id
				request.session['worker_id']=sess
				return redirect("worker_daily_attendance")
			elif user_type == 'public':
				username = request.POST.get('username')
				request.session['user'] = username
				a = request.session['user']
				sess = Register_Detail.objects.only('id').get(name=a).id
				request.session['user_id']=sess
				return redirect("enquiry_land")
		else:
			messages.success(request, 'Invalid Username or Password')
	return render(request,'login.html',{})

def farmer_login(request):
	if request.session.has_key('farmer'):
		return redirect("employee")
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =  request.POST.get('password')
			post = Register_Detail.objects.filter(name=username,password=password,user_type='farmer')
			if post:
				username = request.POST.get('username')
				request.session['farmer'] = username
				a = request.session['farmer']
				sess = Register_Detail.objects.only('id').get(name=a).id
				request.session['farmer_id']=sess
				return redirect("employee")
			else:
				messages.success(request, 'Invalid Username or Password')
	return render(request,'farmer_login.html',{})

def add_tractor(request):
	if request.session.has_key('user'):
		user_id = request.session['user_id']
		public_id = Register_Detail.objects.get(id=int(user_id))
		if request.method=='POST':
			title=request.POST.get('TractorName')
			desc=request.POST.get('Description')
			price=request.POST.get('Price')
			tractor_image=request.FILES['Image']
			data=Tractor.objects.create(user_id=public_id,title=title,desc=desc,price=price,tractor_image=tractor_image)
			if data:
				messages.success(request,'Tractor Added Successfully')
	return render(request,'add_tractor.html')

def add_job(request):
	if request.session.has_key('farmer'):
		user_id = request.session['farmer_id']
		farmer_id = Worker_Detail.objects.get(id=int(user_id))
		cursor =connection.cursor()
		post ='''SELECT u.email,u.id from app_register_detail as u WHERE u.user_type='worker' ORDER BY u.id DESC'''
		sql=cursor.execute(post)
		row = cursor.fetchone()
		email = row[0]
		if request.method == 'POST':
			title = request.POST.get('title')
			skill = request.POST.get('skill')
			exp= request.POST.get('exp')
			dat = request.POST.get('dat')
			des = request.POST.get('des')
			place = request.POST.get('place')
			crt = Job_Detail.objects.create(title=title,
			skill=skill,experience=exp,interview_date=dat,desc=des,place=place,farmer_id=farmer_id)
			if crt:
				messages.success(request,'Job Added Successfully')
		return render(request,'add_job.html',{})
	else:
		return render(request,'farmer_login.html',{})

def employee(request):
	if request.session.has_key('farmer'):
		user_id = request.session['farmer_id']
		detail = Worker_Detail.objects.all()
		return render(request,'jobs.html',{'detail':detail})
	else:
		return render(request,'farmer_login.html',{})
def delete_job(request,pk):
	if request.session.has_key('farmer'):
		user_id = request.session['farmer_id']
		detail = Worker_Detail.objects.filter(id=pk).delete()
		return redirect('employee')
	else:
		return render(request,'farmer_login.html',{})
def add_land(request):
	if request.session.has_key('farmer'):
		user_id = request.session['farmer_id']
		farmer_id = Register_Detail.objects.get(id=int(user_id))
		if request.method == 'POST':
			sqrtft = request.POST.get('sqrtft')
			type_land = request.POST.get('type_land')
			cultivation= request.POST.get('cultivation')
			acres = request.POST.get('acres')
			soil = request.POST.get('soil')
			pipes = request.POST.get('pipes')
			sale = request.POST.get('sale')
			amount = request.POST.get('amount')
			about_land = request.POST.get('about_land')
			place = request.POST.get('place')
			image = request.FILES['image']
			video = request.FILES['video']
			crt = Land_Detail.objects.create(sqrtft=sqrtft,
			type_land=type_land,cultivation=cultivation,acres=acres,soil=soil,pipes=pipes,farmer_id=farmer_id,sale=sale,
			amount=amount,about_land=about_land,place=place,saled_price='',status='',video=video,image=image)
			if crt:
				messages.success(request,'Land Detail Added Successfully')
		return render(request,'add_land.html',{})
	else:
		return render(request,'farmer_login.html',{})
def lands(request):
	if request.session.has_key('farmer'):
		user_id = request.session['farmer_id']
		detail = Land_Detail.objects.filter(farmer_id=int(user_id))
		return render(request,'lands.html',{'detail':detail})
	else:
		return render(request,'farmer_login.html',{})
	
def view_tractor_details(request):
	detail = Tractor.objects.all()
	return render(request,'view_tractor_details.html',{'detail':detail})

def edit_land(request,pk):
	if request.session.has_key('farmer'):
		user_id = request.session['farmer_id']
		farmer_id = Register_Detail.objects.get(id=int(user_id))
		detail = Land_Detail.objects.filter(id=pk)
		if request.method == 'POST':
			sqrtft = request.POST.get('sqrtft')
			type_land = request.POST.get('type_land')
			cultivation= request.POST.get('cultivation')
			acres = request.POST.get('acres')
			soil = request.POST.get('soil')
			pipes = request.POST.get('pipes')
			sale = request.POST.get('sale')
			amount = request.POST.get('amount')
			about_land = request.POST.get('about_land')
			place = request.POST.get('place')
			crt = Land_Detail.objects.filter(id=pk).update(sqrtft=sqrtft,
			type_land=type_land,cultivation=cultivation,acres=acres,soil=soil,pipes=pipes,sale=sale,
			amount=amount,about_land=about_land,place=place)
			if crt:
				messages.success(request,'Land Detail Updated Successfully')
		return render(request,'edit_land.html',{'detail':detail})
	else:
		return render(request,'farmer_login.html',{})
def delete_land(request,pk):
	if request.session.has_key('farmer'):
		user_id = request.session['farmer_id']
		detail = Land_Detail.objects.filter(id=pk).delete()
		return redirect('lands')
	else:
		return render(request,'farmer_login.html',{})
def logout(request):
    try:
        del request.session['farmer']
    except:
     pass
    return render(request, 'farmer_login.html', {})
def user_logout(request):
    try:
        del request.session['worker']
        del request.session['user']
    except:
     pass
    return render(request, 'login.html', {})
def apply_job(request):
	if request.session.has_key('worker'):
		detail = Job_Detail.objects.all()
		return render(request,'apply_job.html',{'detail':detail})
	else:
		return render(request,'login.html',{})
def apply(request,pk):
	if request.session.has_key('worker'):
		wid = request.session['worker_id']
		worker_id = Worker_Detail.objects.get(id=int(wid))
		job_id = Job_Detail.objects.get(id=pk)
		detail = Apply.objects.create(job_id=job_id,worker_id=worker_id,status='pending',job_status='',salary='')
		return redirect('job_details')
	else:
		return render(request,'login.html',{})
def job_details(request):
	if request.session.has_key('worker'):
		wid = request.session['worker_id']
		detail = Apply.objects.filter(worker_id=int(wid))
		return render(request,'job_details.html',{'detail':detail})
	else:
		return render(request,'login.html',{})
def shortlist(request):
	if request.session.has_key('farmer'):
		user_id = request.session['farmer_id']
		cursor = connection.cursor()
		sql = '''SELECT j.title,u.name,u.email,u.mobile,u.address,a.status,a.job_status,a.salary,a.id from app_job_detail as j INNER JOIN app_apply as a ON j.id=a.job_id_id 
		INNER JOIN app_worker_detail as u ON a.worker_id_id=u.id WHERE 
		j.farmer_id_id='%d' ''' % (int(user_id))
		post = cursor.execute(sql)
		detail = cursor.fetchall()
		return render(request,'shortlist.html',{'detail':detail})
	else:
		return render(request,'farmer_login.html',{})

def sale_land(request):
		detail = Land_Detail.objects.all()
		return render(request,'land_details.html',{'detail':detail})

def enquiry(request,pk,fid):
	if request.session.has_key('user'):
		user_id = request.session['user_id']
		farmer_id = Register_Detail.objects.get(id=fid)
		land_id = Land_Detail.objects.get(id=pk)
		detail = Sale_Land.objects.create(user_id=int(user_id),farmer_id=farmer_id,land_id=land_id,status='')
		return render(request,'enquiry.html',{})
	else:
		return render(request,'login.html',{})
def accept(request,pk):
	if request.session.has_key('farmer'):
		user_id = request.session['farmer_id']
		detail = Apply.objects.filter(id=pk).update(status='accept')
		return redirect('shortlist')
	else:
		return render(request,'farmer_login.html',{})
def reject(request,pk):
	if request.session.has_key('farmer'):
		user_id = request.session['farmer_id']
		detail = Apply.objects.filter(id=pk).update(status='reject')
		return redirect('shortlist')
	else:
		return render(request,'farmer_login.html',{})
def edit_hire(request,pk):
	if request.session.has_key('farmer'):
		user_id = request.session['farmer_id']
		if request.method == 'POST':
			a = request.POST.get('hire')
			b = request.POST.get('salary')
			detail = Apply.objects.filter(id=pk).update(job_status=a,salary=b)
			if detail:
				return redirect('shortlist')
		return render(request,'edit_hire.html',{})
	else:
		return render(request,'farmer_login.html',{})
def farmer_land_sale(request):
	if request.session.has_key('farmer'):
		user_id = request.session['farmer_id']
		cursor = connection.cursor()
		sql = '''SELECT d.id,d.sqrtft,u.name,u.mobile,d.amount,d.sale,d.acres,s.date,d.saled_price,s.status,s.id
		from app_land_detail as d INNER JOIN app_sale_land as s ON d.id=s.land_id_id 
		INNER JOIN app_register_detail as u ON s.user_id=u.id WHERE 
		d.farmer_id_id='%d' ''' % (int(user_id))
		post = cursor.execute(sql)
		detail = cursor.fetchall()
		return render(request,'farmer_land_sale.html',{'detail':detail})
	else:
		return render(request,'farmer_login.html',{})
def update_sale(request,pk,land_id):
	if request.session.has_key('farmer'):
		if request.method == 'POST':
			a = request.POST.get('sale')
			b = request.POST.get('price')
			Land_Detail.objects.filter(id=land_id).update(status=a,saled_price=b)
			detail = Sale_Land.objects.filter(id=pk).update(status=a)
			if detail:
				return redirect('farmer_land_sale')
		return render(request,'update_sale.html',{})
	else:
		return render(request,'farmer_login.html',{})
def employee_attendance(request):
    if request.session.has_key('farmer'):
        return render(request,'employee_attendance.html',{})
    else:
        return redirect("farmer_login")
	
def worker_daily_attendance(request):
    if request.session.has_key('worker'):
        worker_id = request.session['worker_id']
        # Assuming you want to fetch attendance details of the worker
        details = Attendance.objects.filter(employee_id=worker_id)
    return render(request, 'worker_daily_attendance.html', {'details': details})


def show_attendance(request):
	if request.session.has_key('farmer'):
		farmers_id = request.session['farmer_id']
		farmer_id=Register_Detail.objects.get(id=int(farmers_id))
		date = request.GET.get('date')
		detail = Apply.objects.filter(job_status='hired',farmer_id=farmer_id)
		if request.method == 'POST':
			student_id = request.POST.getlist('emp_id[]')
			attendance = request.POST.getlist('attendance[]')
			date = request.POST.get('date')
			month = request.POST.get('month')
			length=len(student_id)
			for row in range(0,length):
				s_id =  Worker_Detail.objects.get(id=int(student_id[row]))
				ad = Attendance.objects.create(farmer_id=farmer_id,employee_id=s_id,month=month,
				date=date,attendance=attendance[row])
				if ad:
					messages.success(request,'Added')
		att = Attendance.objects.filter(date=date,farmer_id=farmer_id)
		tot = Attendance.objects.filter(date=date,farmer_id=farmer_id).aggregate(Count('employee_id'))
		present = Attendance.objects.filter(date=date,attendance='yes',farmer_id=farmer_id).aggregate(Count('attendance'))
		absent = Attendance.objects.filter(date=date,attendance='no',farmer_id=farmer_id).aggregate(Count('attendance'))
	return render(request,'show_attendance.html',{'detail':detail,'att':att,'tot':tot,'present':present,'absent':absent})
def employee_salary(request):
	if request.session.has_key('farmer'):
		farmers_id = request.session['farmer_id']
		farmer_id=Register_Detail.objects.get(id=int(farmers_id))
		detail = Apply.objects.filter(job_status='hired',farmer_id=farmer_id)
		return render(request,'employee_salary.html',{'detail':detail})
	else:
		return render(request,'farmer_login.html',{})

def calculate_salary(request):
	if request.session.has_key('farmer'):
		emp_id = request.GET.get('id')
		from_date = request.GET.get('from')
		to_date = request.GET.get('to')
		extra = request.GET.get('extra')
		cursor = connection.cursor()
		sql_user = ''' SELECT COUNT(app_attendance.attendance) from app_attendance 
		where app_attendance.employee_id_id='%d' AND app_attendance.attendance='yes' AND app_attendance.date BETWEEN '%s' AND '%s'
		''' %(int(emp_id),from_date,to_date)
		post_user = cursor.execute(sql_user)
		row_user = cursor.fetchall()
		detail = Worker_Detail.objects.get(id=int(emp_id))
		return render(request,'calculate_salary.html',{'detail':detail,'row_user':row_user})
	else:
		return render(request,'farmer_login.html',{})
		
def enquiry_land(request):
	if request.session.has_key('user'):
		user_id = request.session['user_id']
		cursor = connection.cursor()
		sql = '''SELECT d.id,d.sqrtft,u.name,u.mobile,d.amount,d.sale,d.acres,s.date,d.saled_price,s.status,s.id
		from app_land_detail as d INNER JOIN app_sale_land as s ON d.id=s.land_id_id 
		INNER JOIN app_register_detail as u ON s.farmer_id_id=u.id WHERE 
		s.user_id='%d' ''' % (int(user_id))
		post = cursor.execute(sql)
		detail = cursor.fetchall()
		return render(request,'enquiry_land.html',{'detail':detail})
	else:
		return render(request,'farmer_login.html',{})
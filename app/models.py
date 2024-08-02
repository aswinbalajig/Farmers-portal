from django.db import models
from django.utils import timezone

class Register_Detail(models.Model):
	name = models.CharField(max_length=50,unique=True)
	address = models.CharField(max_length=50)
	mobile = models.CharField(max_length=20)
	password = models.CharField(max_length=50)
	email = models.EmailField(max_length=50)
	user_type = models.CharField(max_length=30,null=True)
	def __str__(self):
		return self.name

class Worker_Detail(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField(max_length=100)
	mobile = models.CharField(max_length=20)
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=50)
	experience = models.CharField(max_length=50)
	address = models.TextField(max_length=100)
	user_type = models.CharField(max_length=30,default='worker')
	def __str__(self):
		return self.name
	

	
class Job_Detail(models.Model):
	farmer_id = models.ForeignKey(Register_Detail, on_delete=models.CASCADE)
	title = models.CharField(max_length=50)
	skill = models.CharField(max_length=20)
	experience = models.CharField(max_length=50)
	interview_date = models.DateField()
	desc = models.TextField(max_length=1000)
	place = models.TextField(max_length=1000)
	posted_date = models.DateField(default=timezone.now())
	def __str__(self):
		return self.title
	def publish(self):
		self.posted_date = timezone.now()
		self.save()
class Land_Detail(models.Model):
	farmer_id = models.ForeignKey(Register_Detail, on_delete=models.CASCADE)
	sqrtft = models.CharField(max_length=50)
	type_land = models.CharField(max_length=200)
	cultivation = models.CharField(max_length=50)
	acres = models.CharField(max_length=100)
	soil = models.CharField(max_length=100)
	pipes = models.CharField(max_length=100)
	sale = models.CharField(max_length=100)
	amount = models.CharField(max_length=100)
	about_land = models.TextField(max_length=1000)
	place = models.TextField(max_length=1000)
	status = models.CharField(max_length=30)
	saled_price = models.CharField(max_length=100)
	posted_date = models.DateField(default=timezone.now())
	video = models.FileField('Upload Video',upload_to='documents/',null=True)
	image = models.FileField('Upload Image',upload_to='documents/',null=True)

	def __str__(self):
		return self.type_land
	def publish(self):
		self.posted_date = timezone.now()
		self.save()
class Apply(models.Model):
	job_id=models.ForeignKey(Job_Detail,on_delete=models.CASCADE,null=True)
	worker_id = models.ForeignKey(Worker_Detail, on_delete=models.CASCADE)
	farmer_id = models.ForeignKey(Register_Detail, on_delete=models.CASCADE,null=True,blank=True)
	status = models.CharField(max_length=50)
	job_status = models.CharField(max_length=20)
	salary = models.CharField(max_length=50)
	def __str__(self):
		return self.worker_id.name
class Sale_Land(models.Model):
	farmer_id = models.ForeignKey(Register_Detail, on_delete=models.CASCADE)
	land_id = models.ForeignKey(Land_Detail, on_delete=models.CASCADE)
	user_id = models.IntegerField()
	status = models.CharField(max_length=20)
	date = models.DateField(default=timezone.now())
	def __str__(self):
		return self.farmer_id.name
	def publish(self):
		self.date = timezone.now()
		self.save()
class Attendance(models.Model):
	farmer_id = models.ForeignKey(Register_Detail, on_delete=models.CASCADE,null=True,blank=True)
	employee_id = models.ForeignKey(Worker_Detail,on_delete=models.CASCADE)
	attendance = models.CharField(max_length=200)
	date = models.CharField(max_length=200)
	month = models.CharField(max_length=200)
	def __str__(self):
		return self.employee_id.name
	
class Tractor(models.Model):
    user_id = models.ForeignKey(Register_Detail,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    desc = models.TextField(max_length=2000)
    price = models.FloatField(max_length=100)
    tractor_image = models.FileField('Upload Image',upload_to='documents/',null=True)
    def __str__(self):
        return self.title

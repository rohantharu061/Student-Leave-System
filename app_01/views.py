from django.shortcuts import render, redirect
from .models import StudentLeave
from django.contrib import messages
from datetime import datetime, timedelta
from django.db.models import Q
from django.core.mail import send_mail, EmailMessage #attach file
from django.template.loader import render_to_string  #hit messsage automatic

# Create your views here.

def dashboard(request):
    
    
    searched= request.GET.get('searched')
    category= request.GET.get('category')
    
    
    if searched:
        if category=='full_name':
            student_leave=StudentLeave.objects.filter(is_delete=False,full_name__icontains=searched)
        elif category=='roll_number':
            
            student_leave=StudentLeave.objects.filter(is_delete=False,roll_number__icontains=searched)
        elif category=='semester':
            student_leave=StudentLeave.objects.filter(is_delete=False,semester__icontains=searched)
        elif category=='faculty':
            student_leave=StudentLeave.objects.filter(is_delete=False,faculty__icontains=searched)
        elif category=='reason':
            student_leave=StudentLeave.objects.filter(is_delete=False,reason__icontains=searched)
        elif category=='student_mail':
            student_leave=StudentLeave.objects.filter(is_delete=False,student_mail__icontains=searched)
        else:
            student_leave=StudentLeave.objects.filter(
                Q(full_name__icontains=searched)|
                Q(roll_number__icontains=searched)|
                Q(semester__icontains=searched)|
                Q(faculty__icontains=searched)|
                Q(reason__icontains=searched)|
                Q(student_mail__icontains=searched)  
            )
    else:
        student_leave=StudentLeave.objects.filter(is_delete=False)
    return render(request, 'index/dashboard.html', {'student_leave': student_leave})

def edit(request, id):
    data=StudentLeave.objects.get(id=id)
    
    if request.method =='POST':
        data.roll_number=request.POST.get('roll_number')
        data.full_name=request.POST.get('full_name')
        data.faculty=request.POST.get('faculty')
        data.semester=request.POST.get('semester')
        data.Leave_type=request.POST.get('Leave_type')
        data.reason=request.POST.get('reason')
        data.start_date=request.POST.get('start_date')
        data.end_date=request.POST.get('end_date')
        data.guardian_contact=request.POST.get('guardian_contact')
        data.student_mail=request.POST.get('student_mail')
        
        data.save() #updated data are saved to existing row
        messages.success(request, "Profile details update successfull!")
        
    
        return redirect('dashboard')
    
    return render(request, 'index/edit.html', {'data':data})

def contact(request):
    return render(request, 'index/contact.html')

def form(request):
    if request.method == 'POST':
        roll_number=request.POST.get('roll_number')
        full_name=request.POST.get('full_name')
        faculty=request.POST.get('faculty')
        semester=request.POST.get('semester')
        Leave_type=request.POST.get('Leave_type')
        reason=request.POST.get('reason')
        start_date=request.POST.get('start_date')
        end_date=request.POST.get('end_date')
        guardian_contact=request.POST.get('guardian_contact')
        student_mail=request.POST.get('student_mail')
        
        StudentLeave.objects.create (
            roll_number=roll_number,
            full_name=full_name,
            faculty=faculty,
            semester=semester,
            Leave_type=Leave_type,
            reason=reason,
            start_date=start_date,
            end_date=end_date,
            guardian_contact=guardian_contact,
            student_mail=student_mail,
        )
        
        send_mail(
            subject ='student_leave',
            message =render_to_string('index/mail.html',{
                            'roll_number':roll_number,
                            'full_name':full_name,
                            'faculty':faculty,
                            'semester':semester,
                            'Leave_type':Leave_type,
                            'reason':reason,
                            'start_date':start_date,
                            'end_date':end_date,
                            'guardian_contact':guardian_contact,
                            'student_mail':student_mail,
                            'date':datetime.now()
            }),
            from_email='rohantharu2061@gmail.com',
            recipient_list=[student_mail],
            fail_silently=True,
        )
        
        messages.success(request, "Form submitted successfull!")
        
    
    return render(request, 'index/form.html')

def delete_data(request,id):
    data= StudentLeave.objects.get(id=id)
    data.is_delete=True
    data.deleted_time= datetime.now()
    data.save()
    
    messages.success(request,f'{data.full_name} is deleted!')
    return redirect('dashboard')


def delete_all(request):
    current_time=datetime.now()
    StudentLeave.objects.all().update(is_delete=True, deleted_time=current_time)
    messages.success(request, 'all datas are deleted!!')
    return redirect('dashboard')

def recycle(request):
    student_leave=StudentLeave.objects.filter(is_delete= True)
    
    threshold=datetime.now()-timedelta(seconds=3000)
    expired=StudentLeave.objects.filter(is_delete=True, deleted_time__lt=threshold)
    
    deleted_count=expired.count()
    if deleted_count>0:
        expired.delete()
        messages.info(request,f'{deleted_count}numbers of datas are deleted')
    else:
        messages.info(request,'no expired records to auto-remove ')
    return render(request, 'index/recycle.html', {'student_leave': student_leave})

def restore(request, id):
    leave=StudentLeave.objects.get(id=id) 
    leave.is_delete=False
    leave.save()
    messages.info(request, f'{leave.full_name} is restored!')
    return redirect('dashboard')

def restore_all(request):
    restore=StudentLeave.objects.filter(is_delete=True)
    restore.update(is_delete=False)
    
    if restore:
        messages.success(request, "restored all data!")
    else:
        messages.info(request, "Nothing to restore!")
        
    return redirect('dashboard')

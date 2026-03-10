from django.shortcuts import render , redirect 
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.views.decorators.cache import never_cache

# Create your views here.
def landing(req):
    return render(req,'landing.html')

def register(req):
    if req.method =='POST':
        n=req.POST.get('name')
        e=req.POST.get('email')
        c=req.POST.get('contact')
        p=req.POST.get('password')
        cp=req.POST.get('cpassword')
        a=req.FILES.get('audio')
        v=req.FILES.get('video')
        d=req.FILES.get('resume')
        s=req.POST.get('state')
        q=req.POST.get('qualification')
        g=req.POST.get('gender')
        user=Employee.objects.filter(Email=e)
        if user:
            msg="Email already exist"
            return render(req,'register.html',{'msg':msg})
        else:
            if p==cp:
                Employee.objects.create(
                    Name=n,
                    Email=e,
                    Contact=c,
                    Password=p,
                    CPassword=cp,
                    Audio=a,
                    Video=v,
                    Resume=d,
                    State=s,
                    Qualification=q,
                    Gender=g 
                    )
                return redirect('login')
            else:
                msg = "password and confirm password not matched"
                return render(req,'register.html',{'pmsg':msg})
    return render(req, 'register.html')

def login(req):
    if req.method == 'POST':
        e=req.POST.get('email')
        p=req.POST.get('password')
        if e=='admin@gmail.com' and p=='admin':
            a_data={
                'id':1,
                'name':'Admin',
                'email':'admin@gmail.com',
                'password':'admin',
                'image':'images/TARESHP1.jpg',
            }
            req.session['a_data']=a_data
            return redirect('admindashboard')
        else:
            employee = Employee.objects.filter(Email=e)
            if employee:
                emp_data = Employee.objects.get(Email=e)
                if p==emp_data.Code:
                    req.session['emp_id']=emp_data.id
                    return redirect('empdashboard')
                else:
                    messages.warning(req,'Email & Password not match') 
                    return redirect('login')
            else:
                messages.warning(req,'Employee does not exist')
                return redirect('login')           
            # user =Employee.objects.filter(Email=e)
            # if not user:
            #     msg ="Register First"
            #     messages.warning(req,'Employee does not exist')
            #     return redirect('register')
            # else:
            #     userdata=Employee.objects.get(Email=e)
            #     if p==userdata.Code:
            #         req.session['user_id']=userdata.id
            #         return redirect('userdashboard')
            #     else:
            #         msg='Email & password not matched'
            #         return render(req,'login.html',{'x':msg})
    return render(req ,'login.html')

@never_cache
def empdashboard(req):
    if 'emp_id' in req.session:
        e_id = req.session.get('emp_id')
        emp_data = Employee.objects.get(id=e_id)
        return render(req,'empdashboard.html',{'data':emp_data})
    else:
        return redirect('login')

@never_cache
def profile(req):
    if 'emp_id' in req.session:
        e_id = req.session.get('emp_id')
        emp_data = Employee.objects.get(id=e_id)
        return render(req,'empdashboard.html',{'data':emp_data,'profile':True})
    else:
        return redirect('login')

@never_cache    
def edit_profile(req):
    return redirect('empdashboard')    

@never_cache    
def settings(req):
    if 'emp_id' in req.session:
        e_id = req.session.get('emp_id')
        emp_data = Employee.objects.get(id=e_id)
        return render(req,'empdashboard.html',{'data':emp_data,'settings':True})
    else:
        return redirect('login')

@never_cache
def userdashboard(req):
    if 'user_id' in req.session:
        x=req.session.get('user_id')
        userdata =Employee.objects.get(id=x)
        return render(req ,'userdashboard.html',{'data':userdata})
    return redirect(req,'login')

@never_cache
def logout(req):
    if 'user_id' in req.session:
        req.session.flush()
        return redirect('login')
    elif 'a_data' in req.session:
        req.session.flush()
        return redirect('login')
    else:
        return redirect('login')

@never_cache
def admindashboard(req):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        return render(req,'admindashboard.html',{'data':a_data})
    else:
        return redirect('login')

@never_cache      
def add_dep(req):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        return render(req,'admindashboard.html',{'data':a_data ,'add_dep':True})
    else:
        return redirect('login')  

@never_cache    
def save_dep(req):
    if 'a_data' in req.session:
        if req.method=='POST':
            dn = req.POST.get('dep_name')
            dd = req.POST.get('dep_desc')
            dh = req.POST.get('dep_head')
            dept = Department.objects.filter(Dep_name=dn)
            if dept:
                messages.warning(req,'Department already exist')
                a_data = req.session.get('a_data')
                return render(req,'admindashboard.html',{'data':a_data ,'add_dep':True})
            else:
                Department.objects.create(Dep_name=dn,Dep_desc=dd,Dep_head=dh)
                messages.success(req,'Department Created')
                a_data = req.session.get('a_data')
                return render(req,'admindashboard.html',{'data':a_data ,'add_dep':True})
    else:
        return redirect('login') 
@never_cache    
def show_dep(req):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        #Deprtment Model
        all_dept=Department.objects.all()
        return render(req,'admindashboard.html',{'data':a_data ,'show_dep':True,'all_dept':all_dept})
    else:
        return redirect('login')  
@never_cache
def add_emp(req):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        all_dept=Department.objects.all()
        return render(req,'admindashboard.html',{'data':a_data ,'add_emp':True,'all_dept':all_dept})
    else:
        return redirect('login')
@never_cache    
def save_emp(req):
    if 'a_data' in req.session:
        if req.method=='POST':
            en = req.POST.get('name')
            ee = req.POST.get('email')
            ec = req.POST.get('contact')
            ed = req.POST.get('dept')
            eco = req.POST.get('code')
            ei = req.FILES.get('image')
            emp = Employee.objects.filter(Email=ee)
            if emp:
                messages.warning(req,'Employee already exist')
                a_data = req.session.get('a_data')
                all_dept=Department.objects.all()
                return render(req,'admindashboard.html',{'data':a_data ,'add_emp':True,'all_dept':all_dept})
            else:
                Employee.objects.create(Name=en,Email=ee,Contact=ec,Image=ei,Code=eco,Dept=ed)
                messages.success(req,'Employee Created')
                send_mail(
                "Employee id and Password",
                f'your Employee id is {ee} and your Employee code is {eco} please do not share it with another person' ,
                "from@example.com",
                [ee],
                fail_silently=False,
                )
                a_data = req.session.get('a_data')
                all_dept=Department.objects.all()
                return render(req,'admindashboard.html',{'data':a_data ,'add_emp':True,'all_dept':all_dept})
    else:
        return redirect('login')
@never_cache    
def show_emp(req):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        emp_data = Employee.objects.all()
        return render(req,'admindashboard.html',{'a_data':a_data,'show_emp':True,'emp_data':emp_data})    
    else:
        return redirect('login')
    
def emp_all_query(req):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        emp_all_query = Query.objects.all()
        return render(req,'admindashboard.html',{'a_data':a_data,'emp_all_query':emp_all_query})    
    else:
        return redirect('login')
    
def reply(req,pk):
    if 'a_data' in req.session:
        a_data =req.session.get('a_data')
        q_data = Query.objects.get(id=pk)
        print(q_data)
        emp_all_query = Query.objects.all()
        return render(req,'admindashboard.html',{'data':a_data,'q_data':q_data,'emp_all_query':emp_all_query})
    else:
        return redirect('login')
    
def a_reply(req,pk):
    if 'a_data' in req.session:
        q_old_data = Query.objects.get(id=pk)
        if req.method == 'POST':
            ar=req.POST.get('reply')    
            q_old_data.Reply = ar
            q_old_data.Status = "Done"
            q_old_data.save()
        a_data = req.session.get('a_data')
        emp_all_query = Query.objects.all()
        return render(req,'admindashboard.html',{'a_data':a_data,'emp_all_query':emp_all_query}) 

    
def empquery(req):
    if 'emp_id' in req.session:
        e_id = req.session.get('emp_id')
        emp_data = Employee.objects.get(id=e_id)
        emp_dept = Department.objects.all()
        return render(req,'empdashboard.html',{'data':emp_data,'query':True,'emp_dept':emp_dept})
    else:
        return redirect('login')
    
def querydata(req):
    if req.method=='POST':
        if 'emp_id' in req.session:
            n = req.POST.get('name') 
            e = req.POST.get('email') 
            d = req.POST.get('department') 
            q = req.POST.get('query') 
            Query.objects.create(Name=n,Email=e,Dept=d,Query=q)
            messages.success(req,"Query created....")
            e_id = req.session.get('emp_id')
            emp_data = Employee.objects.get(id=e_id)
            emp_dept = Department.objects.all()
            return render(req,'empdashboard.html',{'data':emp_data,'query':True,'emp_dept':emp_dept})
    else:
        return redirect('login')
    
def allquery(req):
    if 'emp_id' in req.session:
        e_id = req.session.get('emp_id')
        emp_data = Employee.objects.get(id=e_id)
        all_query = Query.objects.filter(Email=emp_data.Email)
        return render(req,'empdashboard.html',{'data':emp_data,'all_q':True,'all_query':all_query})
    else:
        return redirect('login')

def search(req):
    if 'emp_id' in req.session:
        e_id=req.session.get('emp_id')
        emp_data = Employee.objects.get(id=e_id)
        if req.method == 'POST':
            s = req.POST.get('search')
            # all_query = Query.objects.filter(Email=emp_data.Email,Query=s)
            # all_query = Query.objects.filter(Email=emp_data.Email,Query = s,Departments=s)
            # all_query = Query.objects.filter(Email__icontains=emp_data.Email,Query__icontains = s)
            # all_query = Query.objects.filter(Email=emp_data.Email,Query__icontains = s)
            # all_query = Query.objects.filter(Email=emp_data.Email,Query__icontains = s,Dept__icontains = s)
            # return render(req,'empdashboard.html',{'data':emp_data,'all_query':all_query,'s':s,'all_q':True})
            # all_query = Query.objects.filter(Email=emp_data.Email and (Q(Query__icontains = s) | Q(Dept__icontains = s)))
            all_query = Query.objects.filter(Email=emp_data.Email).filter(Q(Query__icontains=s) | Q(Dept__icontains=s))
            print(all_query)
            return render(req,'empdashboard.html',{'data':emp_data,'all_query':all_query,'s':s,'all_q':True})
        else:
            e_id = req.session.get('emp_id')
            emp_data = Employee.objects.get(id=e_id)
            all_query = Query.objects.filter(Email=emp_data.Email)
            return render(req,'empdashboard.html',{'data':emp_data,'all_q':True,'all_query':all_query})
    else:
        return redirect('login')
    
def pendingquery(req):
    if 'emp_id' in req.session:
        e_id = req.session.get('emp_id')
        emp_data = Employee.objects.get(id=e_id)
        # all_query = Query.objects.filter(Email=emp_data.Email)
        pending=Query.objects.filter(Email=emp_data.Email,Status='pending')
        return render(req,'empdashboard.html',{'data':emp_data,'pendingquery':True,'pending':pending})
    else:
        return redirect('login')
    
def donequery(req):
    if 'emp_id' in req.session:
        e_id = req.session.get('emp_id')
        emp_data = Employee.objects.get(id=e_id)
        # all_query = Query.objects.filter(Email=emp_data.Email)
        done=Query.objects.filter(Email=emp_data.Email,Status='Done')
        return render(req,'empdashboard.html',{'data':emp_data,'donequery':True,'done':done})
    else:
        return redirect('login')    
    
def emp_q_edit(req,pk):
    if 'emp_id' in req.session:
        e_id = req.session.get('emp_id')
        emp_data = Employee.objects.get(id=e_id)
        old_querydata = Query.objects.get(id=pk)
        new_dept = Department.objects.all()
        all_query = Query.objects.filter(Email=emp_data.Email)
        return render(req,'empdashboard.html',{'data':emp_data,'old_querydata':old_querydata,'new_dept':new_dept,'all_query':all_query})
    else:
        return redirect('login')

def updated_querydata(req,pk):
    if 'emp_id' in req.session:
        e_id=req.session.get('emp_id')
        if req.method == "POST":
            d = req.POST.get('department') 
            q = req.POST.get('query') 
            old_q_data = Query.objects.get(id=pk)
            old_q_data.Dept, old_q_data.Query = d,q 
            old_q_data.save()
            # save = Query.objects.update(new_qdata)
            messages.success(req,"Query Updated....")
            e_id = req.session.get('emp_id')
            emp_data = Employee.objects.get(id=e_id)
            all_query = Query.objects.filter(Email=emp_data.Email)
            return render(req,'empdashboard.html',{'data':emp_data,'all_query':True,'all_query':all_query})  
        
def  emp_q_delete(req,pk):
    if 'emp_id' in req.session:
        e_id=req.session.get('emp_id')
        emp_data = Employee.objects.get(id=e_id)
        check_query = Query.objects.get(id=pk)
        check_query.delete()
        all_query = Query.objects.filter(Email=emp_data.Email)
        messages.success(req,'Query deleted')
        return render(req,'empdashboard.html',{'all_query':all_query})
    
def add_item(req):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        if req.method == "POST":
            name = req.POST.get('item_name')
            desc = req.POST.get('item_desc')
            price = req.POST.get('item_price')
            image = req.FILES.get('item_image')
            color = req.POST.get('item_color')
            category = req.POST.get('item_category')
            quantity = req.POST.get('item_quantity')

            Item.objects.create(
                Item_name=name,
                Item_desc=desc,
                Item_price=price,
                Item_image=image,
                Item_color=color,
                Item_category=category,
                Item_quantity=quantity
            )
            a_data = req.session.get('a_data')
            return render(req,'admindashboard.html',{'data':a_data,'add_item':True})
        else:
            a_data = req.session.get('a_data')
            return render(req,'admindashboard.html',{'data':a_data,'add_item':True})
    else:
        return redirect('login')
    
def show_items(req):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        all_items = Item.objects.all()
        return render(req,'admindashboard.html',{'data':a_data,'show_items':True,'all_items':all_items})
    else:
        return redirect('login')

        

from django.shortcuts import render, redirect
from django.contrib import auth
import pyrebase
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from datetime import datetime
import json
# Config key from Firebase

config = {
    'apiKey': "AIzaSyC1QjHN45mLMu1H3FcTuAcjrzUA_trRBYs",
    'authDomain': "exploar-a1371.firebaseapp.com",
    'databaseURL': "https://exploar-a1371.firebaseio.com",
    'projectId': "exploar-a1371",
    'storageBucket': "exploar-a1371.appspot.com",
    'messagingSenderId': "677368258488",
  }

# Firebase APP Initialization and Authencity

firebase = pyrebase.initialize_app(config)
db = firebase.database()
authe = firebase.auth()


def signIn(request):
    return render(request, 'signIn.html')


def postSignIn(request):
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        message = 'inavlid credentials'
        return render(request, 'signIn.html', {"messg": message})

    session_id = user['idToken']
    request.session['uid'] = str(session_id)

    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)

    a = a['users']
    a = a[0]
    a = a['localId']

    name = db.child('users').child(a).child('details').child('name').get().val()

    return render(request, 'home.html', {"email": name})

# Logout


def logout(request):
    auth.logout(request)
    return render(request, 'registration/signIn.html')


def signUp(request):
    return render(request, 'registration/signUp.html')


def postSignUp(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    passw = request.POST.get('pass')

    try:
        user = authe.create_user_with_email_and_password(email, passw)
    except:
        message = 'unable to create account try again'
        return render(request, 'registration/signUp.html', {"messg":message})

    uid = user['localId']

    data = {'Email': request.POST.get("email"),'profit': request.POST.get("prof"),
             'Birth_Date': request.POST.get("bdate"), 'Contactno': request.POST.get("num1"),
             'Company': request.POST.get("company"),
             'Designation': request.POST.get("des")}

    db.child("User_Details").child(uid).set(data)
    return render(request, 'registration/signIn.html')

# User Detail Page

def user_detail(request):
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    id=a['localId']
    user=db.child("User_Details").child(id).get()
    user=user.val()
    return render(request, 'user_detail.html', {
        'email': user['Email'],
        'Profit': user['profit'],
        'date': user['Birth_Date'],
        'contact': user['Contactno'],
        'company': user['Company'],
        'Desigantion': user['Designation'],
    })

# RFP Form

def rfp1(request):
    if request.method == 'POST':
        post1 = {'proj_name' : request.POST.get("p_name"), 'quantity' : request.POST.get("q"),
                    'goals' : request.POST.get("g"), 'date':request.POST.get("date"),
                    'Service' : request.POST.get("s"),
                    'c_name' : request.POST.get("c_name"), 'c_rep_name' : request.POST.get("cr_n"),
                    'c_rep_email': request.POST.get("cr_email"), 'c_rep_ph' : request.POST.get("cr_ph"),
                    'prod_name' : request.POST.get("prod_name"), 'proj_desc' : request.POST.get("proj_desc"),
                    'l_date_p' : request.POST.get("ld_p")}

        db.child("Product_Detail").child(f'{post1["prod_name"]}').set(post1)
        return redirect('user_detail')
    else:
        post1={}


    return render(request, 'rfp.html', post1)

def my_view_that_updates_pieFact(request):
    if request.method == 'POST':
        if 'pieFact' in request.POST:
            pieFact = request.POST['pieFact']
            # doSomething with pieFact here...
            return HttpResponse('success') # if everything is OK
    # nothing went well

# Dashboard Home - Page 1

def home(request):
    try:
        users = db.child("IngramAR").child("Interactions").get()
        user1 = db.child("Users").get()
        d = {}
        b12=[]
        for user in user1.each():
            dob = db.child("Users").child(f"{user.key()}").get()
            d['name'] = ''
            d['prod'] = 0
            d['name'] = user.key()
            try:
                prod1 = db.child("IngramAR").child("Interactions").child(f"{user.key()}").get()
                u = list(prod1)
                d['prod'] = len(u)
            except:
                d['prod'] = 0

            d1=dob.val()
            d3=dict(d1)
            d3.update(d)
            b12.append(d3)
            d = {}

        for i in range(len(b12)):
            s=b12[i]['TimeStamp']
            li=s.split(":")
            li1=s.split("/")
            b12[i]['date']=''
            b12[i]['date']=li1[0]
            el=li[-1].split(".")[0]
            s1=''
            for j in range(len(li)-1):
                s1=s1 + li[j] +":"
            s1=s1+el
            b12[i]['TimeStamp']=s1

        b12=json.loads(json.dumps(b12))
        b12.sort(key=lambda x: datetime.strptime(x['TimeStamp'], '%Y-%m-%d/%H:%M:%S'),reverse=True)
        for i in range(len(b12)):
            k=b12[i]['TimeStamp'].split('/')[-1]
            b12[i]['TimeStamp']=k
        return render(request, 'home.html', {
            'details': b12,
        })
    except:
        a = []
        return render(request, 'home.html', {
            'post': a,
        })


# Dashboard - Page 1 for re_path

def dashboard(request,name):
    prod= db.child("IngramAR").child("Interactions").child(f'{name}').get()
    a = []
    d = {}
    for user in prod.each():
        d['prod'] = ''
        d['prod'] = user.key()
        a.append(d)
        d = {}
    return render(request, 'dashboard1.html', {
        'post':a
    })

# Dashboard - Page 2

def dashboard1(request,name):
    prod= db.child("IngramAR").child("Interactions").child(f'{name}').get()
    a = []
    d = {}
    for user in prod.each():
        d['prod'] = ''
        d['prod'] = user.key()
        a.append(d)
        d = {}
    return render(request, 'dashboard1.html', {
        'post':a,
        'name':name,
    })


# Dashboard - Page 2 for re_path


def dashboard3(request,name,product):
    prod= db.child("IngramAR").child("Interactions").child(f'{name}').get()
    a = []
    d = {}
    for user in prod.each():
        d['prod'] = ''
        d['prod'] = user.key()
        a.append(d)
        d = {}
    return render(request, 'dashboard2.html', {
        'post':a
    })


# Dashboard - Page 3

def dashboard4(request,name,product):
    prod= db.child("IngramAR").child("Interactions").child(f'{name}').get()
    a = []
    d = {}

    for user in prod.each():
        d['prod'] = ''
        d['prod'] = user.key()
        a.append(d)
        d = {}
    return render(request, 'dashboard2.html', {
        'post':a,
        'name':name,
        'product': product,
    })

# RFP Generated Page

def rfp2(request):
    try:
        users = db.child("Product_Detail").get()
        a=[]
        for user in users.each():
            a.append(user.val())

        return render(request, 'rfp2.html', {
            'post':a,
        })
    except:
        a = []
        return render(request, 'rfp2.html', {
            'post': a,
        })

# Incoming RFP

def rfp_detail(request,name):
    prod= db.child("Product_Detail").child(f'{name}').get()
    return render(request, 'rfp_detail.html', {
        'post':prod
    })

# Incoming RFP for re_path

def rfp_detail1(request,name):
    prod= db.child("Product_Detail").child(f'{name}').get()
    return render(request, 'rfp_detail.html', {
        'post':prod.val()
    })

# Form after Creating RFP

def rfp_d(request):
    try:
        fields = db.child("Create_RFP").get()
        b2={}
        a = []
        for user in fields.each():
            a.append(user.val())

        for fld in a:
            b2[f'{fld["name"]}']=''
            b2[f'{fld["name"]}']=request.POST.get(f'{fld["name"]}')
        if request.method == 'POST':
            post1 = {'proj_name': request.POST.get("p_name"), 'quantity':request.POST.get("q"),
                            'goals':request.POST.get("g"), 'date':request.POST.get("date"),
                            'Service':request.POST.get("s"),
                            'c_name':request.POST.get("c_name"), 'c_rep_name':request.POST.get("cr_n"),
                            'c_rep_email':request.POST.get("cr_email"), 'c_rep_ph':request.POST.get("cr_ph"),
                            'prod_name':request.POST.get("prod_name"), 'proj_desc':request.POST.get("proj_desc"),
                            'l_date_p':request.POST.get("ld_p")}
            post1.update(b2)
            db.child("Product_Detail").child(f'{post1["prod_name"]}').set(post1)
            db.child("Create_RFP").remove()

        return render(request, "rfp.html", {"data": b2})

    except:
        b2={}
        post1 = {'proj_name': request.POST.get("p_name"), 'quantity': request.POST.get("q"),
                 'goals': request.POST.get("g"), 'date': request.POST.get("date"),
                 'Service': request.POST.get("s"),
                 'c_name': request.POST.get("c_name"), 'c_rep_name': request.POST.get("cr_n"),
                 'c_rep_email': request.POST.get("cr_email"), 'c_rep_ph': request.POST.get("cr_ph"),
                 'prod_name': request.POST.get("prod_name"), 'proj_desc': request.POST.get("proj_desc"),
                 'l_date_p': request.POST.get("ld_p")}
        db.child("Product_Detail").child(f'{post1["prod_name"]}').set(post1)
        return render(request, "rfp.html", {"data": b2})

#  Create RFP Page

def Createrfp(request):
    try:
        rfp= db.child("Create_RFP").get()
        a = []
        for user in rfp.each():
            a.append(user.val())
        post1={}
        if request.method == 'POST':
            return redirect('rfp.html',{"students": a})

        return render(request,"createrfp.html",{"students": a,'post':post1})
    except:
        a=[]
        post1 = {}
        if request.method == 'POST':
            return redirect('rfp.html', {"students": a})
        return render(request, "createrfp.html", {"students": a, 'post': post1})

# Insert data from Create RFP Page

@csrf_exempt
def Insert_data(request):
    name=request.POST.get("name")
    type=request.POST.get("type")
    try:

        data = {'name': name, 'type': type}
        db.child("Create_RFP").child(f"{name}").set(data)
        stuent_data={"error":False,"errorMessage":"Student Added Successfully"}
        return JsonResponse(stuent_data,safe=False)
    except:
        stuent_data={"error":True,"errorMessage":"Failed to Add Student"}
        return JsonResponse(stuent_data,safe=False)

# Delete data from Create RFP Page

@csrf_exempt
def delete_data(request):
    name = request.POST.get("name")
    try:
        db.child("Create_RFP").child(f"{name}").remove()
        stuent_data={"error":False,"errorMessage":"Deleted Successfully"}
        return JsonResponse(stuent_data,safe=False)
    except:
        stuent_data={"error":True,"errorMessage":"Failed to Delete Data"}
        return JsonResponse(stuent_data,safe=False)


# Function for Visualization Chart

def charts(request):
    return render(request, 'chart.html')


def population_chart(request):


    return JsonResponse(data={
        'labels': [],
        'data': [],
    })

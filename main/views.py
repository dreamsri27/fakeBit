from django.shortcuts import render , redirect
import qrcode
import qrcode.image.svg
from io import BytesIO
import hashlib
from .models import *
from django.contrib.auth.models import User , auth
from django.contrib import auth
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required


'''
1. Get All Data Related to Customer Bill
2. Concat all that data and pass it thru sha256 function
3. generate hash
'''
'''
mining function:
add new blocks to our existing blocks.
'''


def index(request):
    context = {}
    if request.method == "POST":
        factory = qrcode.image.svg.SvgImage
        name = request.POST.get("name")
        price = request.POST.get("price")
        product = request.POST.get("product")
        number = request.POST.get('number')
        quantity = request.POST.get('quantity')
        result = name+price+product+number+quantity
        result1 = hashlib.sha256(result.encode())
        hashgen = result1.hexdigest()
        mined = block_mining(hashgen,result)
        
        hashurl = "http://192.168.45.130/:8000/check/"+hashgen
        img = qrcode.make(hashurl, image_factory=factory, box_size=20)
        stream = BytesIO()
        img.save(stream)
        context["svg"] = stream.getvalue().decode()
        
        data1 = data(name = name , price=price,product=product,number=number,hash=hashgen)
        data1.save()

        context["name"] = name
        context["price"] = price
        context["product"]=product
        context["number"]=number
        return render(request, "check.html", context=context)
        
        

    return render(request, "index.html", context=context)

#mining fuction
def block_mining(hashgen,result):
    last_block_data = blocks_data.objects.last()
    last_block_hash = last_block_data.current_hash
    new_block = blocks_data(previous_hash=last_block_hash,current_hash=hashgen,data=result)
    new_block.save()
    new_txn_hash = last_block_hash+hashgen
    return new_txn_hash

    



def check(request,slug):
    info = data.objects.get(hash=slug)
    if(not(info)):
        print("NO")
    else:
        context = {}
        name = info.name
        price = info.price
        product = info.product
        number = info.number
        hash = info.hash
        product = info.product
        time = info.time
        print(name)
        factory = qrcode.image.svg.SvgImage
        hashurl = "http://192.168.45.130//check/"+hash
        img = qrcode.make(hashurl, image_factory=factory, box_size=20)
        stream = BytesIO()
        img.save(stream)
        context["svg"] = stream.getvalue().decode()
        context["name"] = info.name
        context["price"] = info.price
        context["product"]=info.product
        context["time"]=info.time
        context["number"]=info.number
        return render(request, "check.html", context=context)
        '''
        return render(request, "check.html",{'name':name,'price':price,'number':number,'hash':hash,'context':context,'product':product,'time':time})
        '''

def workflow(request):
    return render(request,"workflow.html")

def blockchains(request):
    blocks = blocks_data.objects.all()
    return render(request,"blockchainvisua.html",{'blocks':blocks})

def login(request):
    if request.method=="POST":
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request,user)

            return redirect("index")
        else:
            err= "Invalid Username or Password"
            return render(request,"login.html",{'err':err})
    else:
        return render(request,"login.html")

    return render(request,"login.html")

def register(request):
    if request.method=="POST":
        company = request.POST.get('companyname')
        username=request.POST.get('username','')
        password=request.POST.get('password','')

        if User.objects.filter(username=username).exists():
            err = "Username Taken"
            return render(request,"register.html",{'err':err})

        else:
            user_main = User.objects.create_user(username=username,password=password,first_name=company)
            user_main.save()
            user  =  user_DB(username=username ,company=company)
            user.save()
            return redirect("login")
        

    return render(request,"register.html")


def logout(request):
    auth.logout(request)
    return redirect("workflow")
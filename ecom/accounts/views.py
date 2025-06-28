from django.shortcuts import render,redirect
from .models import Account
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from django.http import HttpResponse
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage 
from django.contrib.auth.tokens import default_token_generator 
from cart.models import Cart,CartItem
from cart.views  import _cart_id
# Create your views here.
def register(request):
    
    if request.method == 'POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        phone=request.POST['phone']
        password=request.POST['pass']
        confirm_password=request.POST['confirm_pass']
        username=email.split('@')[0]
        if password==confirm_password:
            user=Account.objects.create_user(first_name=fname,last_name=lname,username=username,email=email,password=password)
            user.phone_number=phone
            user.save()
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('accounts/acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':default_token_generator.make_token(user),  
            })  
            to_email =email 
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Please confirm your email address to complete the registration')  
    return render(request,'accounts/register.html')


def signin(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        user=authenticate(email=email,password=password)
        if user is not None:#jab user ke credentials match ho gaye
            try:
                cart=Cart.objects.get(cart_id=_cart_id(request))#cart id fetch kiye
                is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()#idhr usi cart id ke fetch koye cart itens
                if is_cart_item_exists:
                    cart_item=CartItem.objects.filter(cart=cart)
                    print(f'hamara cart item is :{cart_item}')
                    product_variation=[]
                    for item in cart_item:
                        variation=item.variations.all()
                        product_variation.append(list(variation))
                    print(f'ye hai hamare variations:{product_variation}')
                    cart_item=CartItem.objects.filter(user=user)#ye wo cartitem hai jo login hone ke baad user sdalega
                    print(f'ye wo login wala item hai :{cart_item}')
                    
                    ex_var_list=[]                     
                    id=[]
                    for item in cart_item:
                        existing_variation=item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index=ex_var_list.index(pr)
                            item_id=id[index]
                            item=CartItem.objects.get(id=item_id)
                            item.quantity+=1
                            item.user=user
                            item.save()
                        else:
                            cart_item=CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user=user
                                item.save()
            except:
                pass
            auth.login(request,user)
            return redirect('checkout')
        else:
            return redirect('signin')
        
            
    return render(request,'accounts/login.html')


def signout(request):
    auth.logout(request)
    return redirect('signin')


def activate(request,uidb64,token):
    # user=get_user_model()
    try:
        uid=force_bytes(urlsafe_base64_decode(uidb64))#idahr decrypt hua aur uska user id fetch hua
        user=Account.objects.get(pk=uid)#isi user id ko database me lejakar compare kiya
    except Exception:
        user=None
    if user is not None and default_token_generator.check_token(user,token):#agar user hai database ,e aur usika token hai to if chalega
        user.is_active=True
        user.save()
        return HttpResponse("thank you for ur email confirmation and now u cna login in to ur account")
    else:
        return HttpResponse("activation failed")

def forgotpass(request):
    if request.method == 'POST':
        email=request.POST['email']
        try:
            user=Account.objects.get(email=email)
            if user is not None:
                current_site = get_current_site(request)  
                mail_subject = 'password reset link has been sent to your email id'  
                message = render_to_string('accounts/pass_reset.html', {  
                    'user': user,  
                    'domain': current_site.domain,  
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                    'token':default_token_generator.make_token(user),  
                })  
                to_email =email 
                email = EmailMessage(  
                            mail_subject, message, to=[to_email]  
                )  
                email.send()  
                return HttpResponse('Please check ur email for password reset link')
        except Exception:
            return HttpResponse('Incorrect Email Address')
            
    return render(request,'accounts/forgotpass.html')

def reset_pass(request,uidb64,token):
    # user=get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()#idahr decrypt hua aur uska user id fetch hua
        user=Account._default_manager.get(pk=uid)#isi user id ko database me lejakar compare kiya
    except Exception:
        user=None
        print(user)
    if user is not None and default_token_generator.check_token(user,token):#agar user hai database me aur usika token hai to if chalega
        request.session['uid']=uid
        
        return redirect('new_pass')
    else:
        return redirect('signin')

def new_pass(request):
    if request.method == 'POST':
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password == confirm_password:
            uid=request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            return redirect('signin')
        else:
            return redirect('reset_pass')
    return render(request,'accounts/new_pass.html')
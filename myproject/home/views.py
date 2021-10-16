from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import FoodItem, Contact, Order
from math import ceil
from datetime import datetime
from django.contrib import messages

###############Razorpay##########################
import razorpay
# from . models import Coffee

from django.views.decorators.csrf import csrf_exempt

#################Sending Email####################

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

############################sawo labs###############

from django.shortcuts import render
from sawo import createTemplate, getContext, verifyToken
import json
import os
from .models import Config

# Create your views here.
from django.http import HttpResponse
load = ''
loaded = 0

islogin = 0


def setislogin(tru):
    global islogin
    islogin = tru


def setPayload(payload):
    global load
    load = payload


def setLoaded(reset=False):
    global loaded
    if reset:
        loaded = 0
    else:
        loaded += 1


createTemplate("templates/partials")


def first(request):
    setislogin(0)
    allitems = []
    cat_items = FoodItem.objects.values('category', 'id')
    cats = {itemm['category'] for itemm in cat_items}
    for cat in cats:
        itm = FoodItem.objects.filter(category=cat)
        n = len(itm)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allitems.append([itm, range(1, nSlides), nSlides])
    params = {'allitems': allitems}

    return render(request, 'home2.html', params)


def login(request):
    config = Config.objects.order_by('-api_key')[:1]
    setLoaded()
    setPayload(load if loaded < 2 else '')

    context = {
        "sawo": getContext(config, "./receive/"), "load": load, "title": "HOME"
    }
    return render(request, "login.html", context)


def receive(request):
    if request.method == 'POST':
        payload = json.loads(request.body)["payload"]

        setLoaded(True)
        setPayload(payload)
        print(payload)
        # {'user_id': '003128d0-3bbd-4f04-be06-ed4bf38c3b28', 'created_on': '2021-10-06T16:07:53.782000Z', 'identifier': 'yashrathor5015@gmail.com', 'identifier_type': 'email', 'verification_token': 'T9KkF6XEjEZnuQ2UdHpMANw6IR3hPkQLIqSY', 'customFieldInputValues': {}}
        userid = payload['user_id']
        email = payload['identifier']
        date = payload['created_on'][:10]
        print(userid)
        print(email)
        print(date)
        setislogin(1)
        # contact = Contact(name=name, email=email, phone=phone,
        #                   desc=desc, feedback=feedback, date=datetime.today())
        # contact.save()
        # obj = UserInfo(user_id=userid, email=email, date=date)
        # obj.save()
        status = 200 if verifyToken(payload) else 404
        print(status)
        response_data = {"status": status}

        return HttpResponse(json.dumps(response_data), content_type="application/json")
        # return render(request, 'display.html')

###########################################################


def index(request):
    if islogin:
        allitems = []
        cat_items = FoodItem.objects.values('category', 'id')
        cats = {itemm['category'] for itemm in cat_items}
        for cat in cats:
            itm = FoodItem.objects.filter(category=cat)
            n = len(itm)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allitems.append([itm, range(1, nSlides), nSlides])
        params = {'allitems': allitems}

        return render(request, 'index.html', params)
    else:
        config = Config.objects.order_by('-api_key')[:1]
        setLoaded()
        setPayload(load if loaded < 2 else '')

        context = {
            "sawo": getContext(config, "./receive/"), "load": load, "title": "HOME"
        }
        return render(request, "login.html", context)


def product(request, id):
    product = FoodItem.objects.filter(id=id)
    print(product)
    return render(request, 'product.html', {'product': product[0]})
    return render(request, "shop/prodView.html", {'product': product[0]})


def about(request):

    if islogin:
        return render(request, 'about.html')
    else:
        config = Config.objects.order_by('-api_key')[:1]
        setLoaded()
        setPayload(load if loaded < 2 else '')

        context = {
            "sawo": getContext(config, "./receive/"), "load": load, "title": "HOME"
        }
        return render(request, "login.html", context)


def services(request):

    if islogin:
        return render(request, 'service.html')
    else:
        config = Config.objects.order_by('-api_key')[:1]
        setLoaded()
        setPayload(load if loaded < 2 else '')

        context = {
            "sawo": getContext(config, "./receive/"), "load": load, "title": "HOME"
        }
        return render(request, "login.html", context)


def contact(request):
    if islogin:
        if request.method == "POST":
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            desc = request.POST.get('desc')
            feedback = request.POST.get('feedback')
            contact = Contact(name=name, email=email, phone=phone,
                              desc=desc, feedback=feedback, date=datetime.today())
            contact.save()
            messages.success(request, 'Your message has been sent!')
        return render(request, 'contact.html')
    else:
        config = Config.objects.order_by('-api_key')[:1]
        setLoaded()
        setPayload(load if loaded < 2 else '')

        context = {
            "sawo": getContext(config, "./receive/"), "load": load, "title": "HOME"
        }
        return render(request, "login.html", context)


def order(request):
    if islogin:
        if request.method == "POST":
            items_json = request.POST.get('itemsJson', '')
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            address = request.POST.get('address1', '') + \
                " " + request.POST.get('address2', '')
            city = request.POST.get('city', '')
            state = request.POST.get('state', '')
            zip_code = request.POST.get('zip_code', '')
            phone = request.POST.get('phone', '')
            # amount = request.POST.get('amount')
            amount = int(request.POST.get("amount"))*100
            print(amount)
            client = razorpay.Client(
                auth=("rzp_test_URte1E6IFmQae1", "wNfteUPufGcDnxilLFvoNC98"))
            payment = client.order.create(
                {'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
            # print(payment)

            order = Order(items_json=items_json, name=name, email=email, address=address, city=city, state=state,
                          zip_code=zip_code, phone=phone, amount=amount/100, payment_id=payment['id'])
            order.save()
            # thank = True
            # id = order.order_id
            return render(request, "order.html", {'payment': payment})
            # return render(request, 'order.html', {'thank': thank, 'id': id})
        return render(request, 'order.html')
    else:
        config = Config.objects.order_by('-api_key')[:1]
        setLoaded()
        setPayload(load if loaded < 2 else '')

        context = {
            "sawo": getContext(config, "./receive/"), "load": load, "title": "HOME"
        }
        return render(request, "login.html", context)


@csrf_exempt
def success(request):
    if request.method == "POST":
        a = request.POST
        order_id = ""
        data = {}
        for key, val in a.items():
            if key == 'razorpay_order_id':
                data['razorpay_order_id'] = val
                order_id = val
            elif key == 'razorpay_payment_id':
                data['razorpay_payment_id'] = val
            elif key == 'razorpay_signature':
                data['razorpay_signature'] = val
        user = Order.objects.filter(payment_id=order_id).first()
        print(user)
        client = razorpay.Client(
            auth=("rzp_test_URte1E6IFmQae1", "wNfteUPufGcDnxilLFvoNC98"))
        check = client.utility.verify_payment_signature(data)

        if check:
            return render(request, "error.html")
        user.paid = True
        user.save()
        msg_plain = render_to_string('email.txt')

        msg_html = render_to_string(
            'email.html', {'name': user.name, 'amount': user.amount, 'email': user.email, 'address': user.address, 'payment_id': user.payment_id, 'phone': user.phone, 'order_id': order_id, 'city': user.city, 'state': user.state, 'zip_code': user.zip_code})
        send_mail("Your order has been recieved", msg_plain,
                  settings.EMAIL_HOST_USER, [user.email], html_message=msg_html, fail_silently=False)

    return render(request, "success.html")

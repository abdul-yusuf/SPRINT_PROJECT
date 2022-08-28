from datetime import date
from django.shortcuts import redirect, render
from django.db.models import Q, F
from django.core.exceptions import ObjectDoesNotExist

from administrator.forms import BlogForm
from administrator.models import Blog, Message, RestaurantService
from authentication.models import User
from decorators import administrator_only, is_logged_in
from django.contrib.messages import add_message, constants
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password,  make_password

from kitchen.models import Food, Kitchen, Ordered, Category
# Create your views here.

def generate_username_with_prefix(admin):
    # name
    name = ''.join(list(admin.name))
    if len(name) > 5:
        name = name[:6].lower() + str(admin.kitchen.attendants.count() + 1)
    return name

def initiate_admin_kitchen(request):
    admin = RestaurantService.objects.get(admin=request.user)
    kitchen_instance = admin.kitchen
    return admin, kitchen_instance

def get_this_week_sells(total):
    FROM = 9
    today = date.today()
    last_weeks = total.filter(
        order__ordered_date__year = today.year,
        order__ordered_date__month = today.month,
        order__ordered_date__day__gte = (today.day - FROM))
    return last_weeks

def get_total_sells(admin):
    return Ordered.objects.filter(kitchen = admin.kitchen, order__payment__is_payed = True)
def get_customers(sells):
    customers = set(sell.order.customer for sell in sells)
    return customers
   
@administrator_only
def Dashboard(request):
    admin,kitchen_instance = initiate_admin_kitchen(request)
    total_sell = get_total_sells(admin)
    this_week_sell = get_this_week_sells(total_sell)
    today_sell = this_week_sell.filter(order__ordered_date__day = (date.today().day))
    customers = get_customers(total_sell)
    last_few_recents = total_sell.order_by('order__ordered_date')[:10]
    activities = admin.activities.all()
    context = {
        'restaurant': kitchen_instance, 
        'customers':customers, 
        'today_sell':today_sell, 
        'this_week_sell':this_week_sell, 
        'total_sell':total_sell,
        'activities':activities,
        'last_few_recents':last_few_recents
        }
    return render(request, 'administrator/dashboard.html',context)

@administrator_only
def FoodifyChat(request):
    admin,_ = initiate_admin_kitchen(request)
    if request.method == 'POST':
        import datetime
        user = request.user.username
        text = request.POST.get('text')
        message  = Message()
        message.sender = user
        message.text = text
        message.timestamp = datetime.datetime.now()
        if request.FILES.get('file') != None:
            message.attached_file = request.FILES.get('file')
        message.save()
        admin.foodify_chat.add(message)
        admin.save()
        return redirect('administrator:foodify-chat')
    messages = admin.foodify_chat.all()[:15]
    return render(request, 'administrator/stemchat-public.html', {'msgs':messages})

@administrator_only
def StaffChat(request):
    admin,_ = initiate_admin_kitchen(request)
    if request.method == 'POST':
        import datetime
        user = request.user.username
        text = request.POST.get('text')
        message  = Message()
        message.sender = user
        message.text = text
        message.timestamp = datetime.datetime.now()
        if request.FILES.get('file') != None:
            message.attached_file = request.FILES.get('file')
        message.save()
        admin.staff_chat.add(message)
        admin.save()
        return redirect('administrator:staff-chat')
    messages = admin.staff_chat.all()[:15]
    return render(request, 'administrator/stemchat.html', {'msgs':messages})


@administrator_only
def UpdateProfile(request):
    return render(request, 'administrator/profile.html')

@administrator_only
def Orders(request):
    admin,kitchen_instance = initiate_admin_kitchen(request)
    total_sell = get_total_sells(admin)
    return render(request, 'administrator/orders.html', {'orders': total_sell})




# i do not touch

@administrator_only
def Profile(request):
    return render(request, 'administrator/profile-view.html')


@administrator_only
def Blogs(request):
    blogs = request.user.posts.all()
    return render(request, 'administrator/posts.html', {'posts': blogs})


@administrator_only
def NewBlog(request):
    form = BlogForm()
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
    return render(request, 'administrator/new-post.html', {'form': form})

@administrator_only
def UpdateBlog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    form = BlogForm(instance=blog)
    if request.method == 'DELET':
        blog.delete()
        return redirect('administrator:posts')
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
    return render(request, 'administrator/new-post.html', {'form': form})



@administrator_only
def NotAvailable(request):
    foods = RestaurantService.objects.get(admin=request.user).not_available_foods
    return render(request, 'administrator/not-available.html', {'foods': foods})


@administrator_only
def StudentCustomers(request):
    admin,kitchen_instance = initiate_admin_kitchen(request)
    total_sell = get_total_sells(admin)
    customers = get_customers(total_sell)
    return render(request, 'administrator/customers.html', {'customers': customers})


@administrator_only
def OrderSummary(request):

    orders = []
    restaurant = RestaurantService.objects.first()
    orders.extend(restaurant.orders_sum)
    return render(request, 'administrator/order-summary.html', {'summary': orders})

@administrator_only
def PrintOrderSummary(request, date):

    orders = RestaurantService.objects.first().orders_sum_print

    return render(request, 'administrator/components/print_orders.html', {'order': orders[date]})


@administrator_only
def Foods(request):
    admin = RestaurantService.objects.get(admin=request.user)
    kitchen_instance = Kitchen.objects.select_related().filter(restaurant_kitchen=admin)[0]

    foods = kitchen_instance.available_foods
    print(foods, kitchen_instance)
    return render(request, 'administrator/foods.html', {'foods': foods})


@administrator_only
def NewRestaurant(request):
    if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        phone_no = data.get('phone_no')
        address = data.get('address')
        rest = RestaurantService.objects.create(
            admin=request.user, name=name, address=address, phone_no=phone_no)
        return redirect('administrator:dashboard')
    return render(request, 'administrator/new-restaurant.html')

# !! YOU CAN'T CREATE MORE THAN ONE KITCHEN


@administrator_only
def NewKitchen(request):
    if request.method == 'POST':
        user = request.user
        data = request.POST
        name = data.get('name')
        phone_no = data.get('phone_no')
        address = data.get('address')
        image = request.FILES.get('image')
        kitchen = Kitchen.objects.create(
            image=image, name=name, address=address, phone_number=phone_no)
        user.restaurant.kitchens.add(kitchen)
        user.restaurant.save()
        return redirect('administrator:kitchens')
    return render(request, 'administrator/new-kitchen.html')


@administrator_only
def KitchenView(request):
    admin,kitchen = initiate_admin_kitchen(request)
    attendants = kitchen.attendants.all()
    return render(request, 'administrator/kitchen.html', {'kitchen': kitchen, 'attendants':attendants})


@administrator_only
def AssignKitchenAttendant(request):

    if request.method == 'POST':
        admin,kitchen = initiate_admin_kitchen(request)
        try:
            u = generate_username_with_prefix(admin)
            print(u)
            dob = request.POST.get('date_of_birth')
            f, l = request.POST.get('full_name').split(' ')

            e = request.POST.get('email')
            g = request.POST.get('gender')
            ph = request.POST.get('phone_no')
            p1 = request.POST.get('password')
            attendant = User.objects.create_user(
                username=u, 
                first_name=f,
                last_name=l,
                email=e,
                gender=g,
                date_of_birth=dob,
                phone_no=ph,
                password=p1,
                is_kitchen = True)
            kitchen.attendants.add(attendant)
            kitchen.save()
            attendant.save()
            return redirect('administrator:kitchen')
        except Exception as e:
            print(e)
            return redirect('administrator:dashboard')
    return render(request, 'administrator/new-kitchen-attendant.html')


@administrator_only
def KitchenOrders(request):

    kitchen = Kitchen.objects.first()
    orders = kitchen.ordered.all()
    return render(request, 'administrator/orders.html', {'orders': orders})


@administrator_only
def KitchenOrdersSummary(request):
    kitchen = Kitchen.objects.first()
    summary = kitchen.orders_sum
    print(summary)
    return render(request, 'administrator/order-summary.html', {'summary': summary})


def CustomerProfile(request, username):
    customer = User.objects.get(username=username)
    return render(request, 'administrator/customer-profile.html', {'customer': customer})

@login_required
def DeclinedOrder(request, order_id):
    ordered = Ordered.objects.get(id=order_id)
    try:
        order = ordered.kitchen.foods.get(name=ordered.name)
        order.quantity = F('quantity') + ordered.quantity
        order.save()
        ordered.delete()
    except ObjectDoesNotExist:
        ordered.delete()
    return redirect('administrator:orders')

@administrator_only
def Categories(request):
    categories = Category.objects.all()
    return render(request, 'administrator/categories.html', {'categories': categories})

@administrator_only
def NewCategory(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        name = request.POST.get('name')
        Category.objects.create(name=name, image=image)
        return redirect('administrator:category')
    return render(request, 'administrator/category.html')


def AddFood(request):
    return render(request, 'administrator/add-food.html')


def ChangePassword(request):
    if request.method == 'POST':
        user = request.user
        current_password = request.POST.get('current password')
        new_password = request.POST.get('new password')
        confirm_password = request.POST.get('confirm password')
        if check_password(current_password, user.password):
            if new_password == confirm_password:
                user.password = make_password(confirm_password)
                user.save()
                return redirect('administrator:dashboard')
            else:
                add_message(request, constants.ERROR, 'Passwords didnt match')

        else:
            add_message(request, constants.ERROR, 'Password is Incorrect')
    return render(request, 'administrator/change-password.html')


@is_logged_in
def AdminLogin(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            if user.is_admin == False:
                add_message(request, constants.ERROR,
                            'This is Account didnt have access to administrator dashboard')
                return redirect('administrator:login')
            login(request, user)
            add_message(request, constants.SUCCESS, 'login success')
            if user.is_kitchen:
                return redirect('kitchen:dashboard')
            elif user.is_admin:
                return redirect('administrator:dashboard')
            return redirect('restaurant:dashboard')
        add_message(request, constants.ERROR, 'Invalid credentials')
    return render(request, 'administrator/login.html')

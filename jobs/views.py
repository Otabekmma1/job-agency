from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, logout
from .models import *
from django.contrib.auth.models import Group, User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib import messages
from django.contrib.auth.decorators import login_required



#------------------ SIGNALS ----------------------
@receiver(post_save, sender=User)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        '''Yangi foydalanuchi ro'yxatdan o'tgan bo'lsa'''
        group, created = Group.objects.get_or_create(name='Users')
        instance.groups.add(group)

#----------------------------------------------------------------



#-------------------- User -------------------------------
def user_login(request):

    '''foydalanuvchi saytga kirishi'''
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        if form.errors:
            messages.error(request, "Taxallus yoki parol xato!")
    else:
        form = LoginForm()
    ctx = {
        'form': form,
        'title': 'Kirish'
    }
    return render(request, 'users/login.html', ctx)

def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz !!!")
            return redirect('login')
        if form.errors:
            messages.warning(request, "Xatolik! Iltimos, ma'lumotlaringizni qaytadan kiriting.")
    else:
        form = RegisterForm()
    ctx = {
        'form': form,
        'title': "Ro'yxatdan o'tish"
    }

    return render(request, 'users/register.html', ctx)

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('index')

@login_required(login_url='login')
def userprofile(request):
    user = User.objects.get(username=request.user.username)
    jobs = Jobs.objects.filter(author=user)

    ctx = {
        'jobs': jobs,
    }

    try:
        user_profile = UserProfile.objects.get(user=user)
        ctx['user_profile'] = user_profile
    except:
        pass
    return render(request, 'users/profile.html', ctx)

@login_required(login_url='login')
def update_profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
        profile.save()

    '''foydalanuvchi profilini tahrirlash'''
    req = request.POST
    if request.method == "POST":
        first_name = req.get('first_name')
        last_name = req.get('last_name')
        email = req.get('email')
        addres = req.get('addres')
        phone = req.get('phone')

        edit = UserProfile.objects.get(id=request.user.id)
        req_edit = User.objects.get(username=request.user.username)
        req_edit.first_name = first_name
        req_edit.last_name = last_name
        req_edit.email = email
        req_edit.save()
        edit.addres = addres
        edit.phone = phone
        edit.save()
        messages.warning(request, "Sahifa muvaffaqiyatli o'zgartirildi")
        return redirect("/profile")

    username = request.user.username
    user = User.objects.get(username=username)
    current_user = UserProfile.objects.get(user=user)

    context = {
        'current_user': current_user,
        'user': user,
    }
    return render(request, "users/update_profile.html", context)

@login_required(login_url='login')
def delete_profile(request):
    user = User.objects.get(username=request.user.username)
    user.delete()
    messages.error(request, 'Hisobingiz o\'chirildi')
    return redirect('login')

#------------------ end User ---------------------------



def index(request):
    jobs_index = Jobs.objects.order_by('-created')[0:6]
    if request.method == 'POST':
        text = request.POST.get('text')
        author = User.objects.get(username=request.user.username)
        if all([text, author]):
            CallBack.objects.create(
                author=author,
                text=text
            )
    ctx = {
        'jobs_index': jobs_index,
        'title': "Bosh sahifa"
    }
    return render(request, 'jobs/index.html', ctx)

def all_jobs(request):
    jobs = Jobs.objects.all()
    categories = Category.objects.all()
    ctx = {
        'jobs': jobs,
        'categories': categories,
        'title': "Barcha ishlar"
    }
    return render(request, 'jobs/jobs.html', ctx)

def jobs_by_category(request, category_id):
    jobs = Jobs.objects.filter(category_id=category_id)
    categories = Category.objects.all()
    ctx = {
        'jobs': jobs,
        'categories': categories
    }
    return render(request, 'jobs/jobs.html', ctx)


def contact(request):
    ctx = {
        'title': "Biz bilan bog'lanish"
    }
    return render(request, 'jobs/contact.html', ctx)

def job_detail(request, id):
    job = Jobs.objects.get(id=id)
    comments = Comments.objects.filter(job=job)
    user = User.objects.get(username=request.user.username)
    user1 = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        author = User.objects.get(username=request.user.username)
        text = request.POST.get('text')
        if all([author, text]):
            Comments.objects.create(
                author=author,
                text=text,
                job=job
            )
        messages.success(request, f"Izoh muvaffaqiyatli qo'shildi!")

    job.views += 1
    job.save()
    ctx = {
        'job': job,
        'comments': comments,
        'user': user,
        'user1': user1,
        'title': job.name
    }
    return render(request, 'jobs/job-details.html', ctx)



#--------------- crud -----------------------

@login_required(login_url='login')
def add_job(request):
    if request.user.is_authenticated:
        categories = Category.objects.all()
        post = request.POST
        if request.method == 'POST':
            name = post.get('name')
            category = post.get('category')
            category_instance = Category.objects.get(name=category)
            deman = post.get('deman')
            salary = post.get('salary')
            author = User.objects.get(username=request.user.username)
            if all([name, category_instance, deman, salary, author]):
                Jobs.objects.create(
                    name=name,
                    category=category_instance,
                    deman=deman,
                    salary=salary,
                    author=author
                )
                messages.info(request, "E'lon muvaffaqiyatli qo'shildi")
                return redirect('index')

    ctx = {
        'categories': categories,
    }
    return render(request, 'crud/add_jobs.html', ctx)

@login_required(login_url='login')
def update_job(request, id):
    if request.user.is_authenticated:

        post = request.POST
        if request.method == "POST":
            name = post.get('name')
            category = post.get('category')
            category_instance = Category.objects.get(name=category)
            deman = post.get('deman')
            salary = post.get('salary')

            edit = Jobs.objects.get(id=id)
            edit.name = name
            edit.deman = deman
            edit.category = category_instance
            edit.salary = salary
            edit.save()
            messages.warning(request, "E'lon muvaffaqiyatli o'zgartirildi")
            return redirect("/profile")
        job = Jobs.objects.get(id=id)
        categories = Category.objects.all()

        ctx={
            'job': job, 'categories': categories,
        }
        return render(request, "crud/edit_job.html",ctx)
    else:
        return redirect('login')
@login_required(login_url='login')
def delete_job(request, id):
    if request.user.is_authenticated:

        job = Jobs.objects.get(id=id)
        job.delete()
        messages.error(request, "E'lon o'chirildi")
        return redirect("/profile")
    else:
        return redirect('login')




def navbar(request):
    use = User.objects.get(username=request.user.username)
    user = UserProfile.objects.get(user=use)
    return render(request, 'components/header.html', {'user': user})
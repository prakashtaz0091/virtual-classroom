from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from .models import User, Profile, Withdrawal
from main.models import Post
from esewa_payment.models import EsewaTransaction
from django.db.models import Sum
from django.contrib import messages


def change_password(request):
    pass


def change_email(request):
    pass


def request_withdrawal(request):
    if request.method == "POST":
        withdrawal_amount = request.POST.get("amount")

        user_earnings = EsewaTransaction.objects.filter(receiver=request.user)
        total_earning_amount = user_earnings.aggregate(
            total_amount=Sum("notes__amount")
        ).get("total_amount")

        total_withdrawal_amount = (
            Withdrawal.objects.filter(user=request.user)
            .aggregate(total_amount=Sum("amount"))
            .get("total_amount")
        ) or 0
        print(total_withdrawal_amount, total_earning_amount)
        remaining_earnings = total_earning_amount - total_withdrawal_amount

        if float(withdrawal_amount) > remaining_earnings:
            messages.error(
                request, "You don't have enough remaining earnings to withdraw."
            )
            return redirect("profile_view")

        Withdrawal.objects.create(user=request.user, amount=withdrawal_amount)
        messages.success(request, "Withdrawal request sent successfully!")

    return redirect("profile_view")


def register_view(request):
    if request.method == "POST":
        data = request.POST
        username = data.get("username")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        role = data.get("role")
        firstname = data.get("firstname")
        lastname = data.get("lastname")

        form = CustomUserCreationForm(
            {"username": username, "password1": password, "password2": confirm_password}
        )

        if form.is_valid():
            user = User(
                username=username, role=role, first_name=firstname, last_name=lastname
            )
            user.set_password(password)
            user.save()
        else:
            return render(request, "account/register.html", {"form": form})

        # personal info
        bio = data.get("bio")
        profile_pic = request.FILES.get("profile_pic")

        try:
            Profile.objects.create(user=user, bio=bio, avatar=profile_pic)
        except Exception as e:
            print(e)
            context = {"error": "An error occurred while creating the profile."}
            return render(request, "account/register.html", context)

        return redirect("login_view")

    return render(request, "account/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember")

        # check if user exists with the provided credentials
        user = authenticate(request, username=username, password=password)

        # if user exists, log them in
        if user is not None:
            login(request, user)
            if remember_me:
                request.session.set_expiry(1209600)  # 14 days in seconds
            else:
                request.session.set_expiry(
                    0
                )  # Session expires at the end of the browser session
            return redirect("home")
        else:
            return render(
                request, "account/login.html", {"error": "Invalid username or password"}
            )

    return render(request, "account/login.html")


def logout_view(request):
    logout(request)
    return redirect("login_view")


def profile_view(request):
    user_posts_count = Post.objects.filter(
        classroom__in=request.user.classrooms.all()
    ).count()

    user_earnings = EsewaTransaction.objects.filter(receiver=request.user)
    total_earning_amount = user_earnings.aggregate(
        total_amount=Sum("notes__amount")
    ).get("total_amount")

    context = {
        "posts_count": user_posts_count,
        "earnings": user_earnings,
        "total_amount": total_earning_amount,
    }

    return render(request, "account/profile.html", context)

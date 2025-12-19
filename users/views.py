from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from products.models import Product
from orders.models import Order
from django.contrib.auth.models import User

def register(request):
    if request.user.is_authenticated:
        return redirect('home:home_page')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validation
        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'users/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'users/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return render(request, 'users/register.html')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create profile
        UserProfile.objects.create(user=user)
        
        messages.success(request, 'Account created successfully! Please login.')
        return redirect('users:login')
    
    return render(request, 'users/register.html')

# Login View
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home:home_page')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            
            # Redirect to next page or home
            next_page = request.GET.get('next', 'home:home_page')
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'users/login.html')

# Logout View
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home:home_page')
# Profile
@login_required
def profile(request):
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Get user statistics
    #total_orders = profile.get_total_orders()
    #pending_orders = profile.get_pending_orders()
    #total_spent = profile.get_total_spent()
    
    # Get recent orders
    #recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Get wishlist items
    #wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    
    if request.method == 'POST':
        # Update profile
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.postal_code = request.POST.get('postal_code')
        
        # Handle profile picture upload
        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES['profile_picture']
        
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('users:profile')
    
    context = {
        'profile': profile,
        #'total_orders': total_orders,
        #'pending_orders': pending_orders,
        #'total_spent': total_spent,
        #'recent_orders': recent_orders,
        #'wishlist_items': wishlist_items,
    }
    
    return render(request, 'users/profilepage.html', context)
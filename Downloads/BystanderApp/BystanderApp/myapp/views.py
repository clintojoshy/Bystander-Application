from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import User, MedicalHistory
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password

def landingpage(request):
    response = render(request, "landingpage.html")
    response['Cache-Control'] = 'no-store'
    return response

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        gender = request.POST.get("gender")
        user_type = request.POST.get("user_type")

        # Validate passwords
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('/reg/')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email is already taken")
            return redirect('/reg/')

        # Create the user
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=make_password(password),  # Hash the password
            phone=phone,
            address=address,
            city=city,
            state=state,
            gender=gender,
            user_type=user_type
        )
        user.save()

        messages.success(request, "User registered successfully!")
        return redirect('/login/')
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):  # Use the method provided by User model
                auth_login(request, user)
                request.session['user_id'] = user.id  # Store user ID in session
                messages.success(request, "Login success")
                
                # Redirect based on user type
                if user.user_type == "Patient":
                    return redirect('patient_dashboard')
                elif user.user_type == "Bystander":
                    return redirect('bystander_dashboard')
            else:
                # Invalid password
                messages.error(request, "Invalid credentials")
                return render(request, 'login.html')
        
        except User.DoesNotExist:
            # Email does not exist
            messages.error(request, "User with this email does not exist")
            return render(request, 'login.html')
    
    return render(request, 'login.html')

def render_dashboard(request, template_name, user):
    response = render(request, template_name, {"user": user})
    response['Cache-Control'] = 'no-store'
    return response

def patientdash(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            return render_dashboard(request, "patient_dashboard.html", user)
        except User.DoesNotExist:
            request.session.flush()
            return redirect('login')
    return redirect('login')

def bystanderdash(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            return render_dashboard(request, "bystander_dashboard.html", user)
        except User.DoesNotExist:
            request.session.flush()
            return redirect('login')
    return redirect('login')

def logout(request):
    request.session.flush()
    return redirect('login')

def profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('login')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        gender = request.POST.get('gender')
        
        # Update user details
        User.objects.filter(id=user_id).update(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            gender=gender
        )
        messages.success(request, 'Profile updated successfully')
        return redirect('patient_dashboard')
    
    response = render(request, 'profile_management.html', {'user': user})
    response['Cache-Control'] = 'no-store'
    return response

def medicalhistory(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    try:
        patient = User.objects.get(id=user_id, user_type="Patient")
    except User.DoesNotExist:
        return redirect('login')
    
    if request.method == "POST":
        condition = request.POST.get("condition")
        date_diagnosed = request.POST.get("date_diagnosed")
        medications = request.POST.get("medications")
        notes = request.POST.get("notes")
        status = request.POST.get("status")
        
        # Create the medical history entry
        medical_history = MedicalHistory(
            patient=patient,
            condition=condition,
            date_diagnosed=date_diagnosed,
            medications=medications,
            notes=notes,
            status=status
        )
        medical_history.save()
        messages.success(request, "Medical history added successfully")
        return redirect('medical_history')
    
    medical_history_records = MedicalHistory.objects.filter(patient=patient)
    return render(request, "medical_history.html", {
        "medical_history": medical_history_records
    })

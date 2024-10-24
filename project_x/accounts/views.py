from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import login


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('http://127.0.0.1:8000/')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})



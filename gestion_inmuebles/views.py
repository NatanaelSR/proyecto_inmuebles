from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Vista principal (Home)
def home(request):
    return render(request, 'web/home.html')

# Vista y formulario de registro
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
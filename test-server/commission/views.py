from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Commission  # Makes sure to import your model

def index(request):
    if request.method == 'POST':
        # 1. Grab text data from request.POST
        product_name = request.POST.get('product_name')
        email = request.POST.get('email')
        details = request.POST.get('details')
        
        # 2. Grab uploaded file data from request.FILES
        reference_image = request.FILES.get('reference_image')
        
        # 3. Create and save the new database row
        Commission.objects.create(
            product_name=product_name,
            email=email,
            details=details,
            reference_image=reference_image
        )
        
        # 4. Push a notification to the user interface
        messages.success(request, "Success! Your concept has been sent. Keep an eye on your inbox!")
        
        # 5. Redirect back to clear out the form inputs safely
        return redirect('commission:index')  # Assumes 'index' is the name matching your path in urls.py

    # If it's a GET request, just display the page normally
    return render(request, 'commission/comm_page.html')
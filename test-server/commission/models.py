from django.db import models

class Commission(models.Model):
    product_name = models.CharField(max_length=150)
    email = models.EmailField()
    details = models.TextField(help_text="Provide greater detail regarding your custom commission request.")
    
    # Stores uploaded files inside a "commissions/" directory inside your MEDIA_ROOT
    reference_image = models.ImageField(upload_to="commissions/", null=True, blank=True)
    
    # Tracking fields
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commission: {self.product_name} ({self.email})"
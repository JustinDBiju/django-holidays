from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings 
from .models import Profile

@receiver(post_save, sender=User)
def create_profile_and_send_email(sender, instance, created, **kwargs):
    
    # --- Logic for New User Creation (Registration) ---
    if created:
        # 1. Create the user Profile (Required for the 'instance.profile' relation to work)
        Profile.objects.create(user=instance)
        
        # 2. Send the registration email 📧
        subject = 'Welcome! You Successfully Registered'
        message = (f'Hello {instance.username},\n\n'
                   f'Thank you for registering on our site. Your account is now active.'
        )
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.email]

        if instance.email:
            try:
                # Attempt to send the mail
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                print(f"Registration email sent to {instance.email}") # For debugging success
            except Exception as e:
                # Log the error if sending fails (e.g., authentication issues)
                print(f"Failed to send registration email to {instance.email}: {e}")

    # --- Logic for Existing User Update ---
    # This runs when the User object is updated after creation.
    else:
        # Check if the profile exists before attempting to save it, 
        # which is safer than assuming it exists.
        try:
            # Only save the profile when the user is updated
            instance.profile.save()
        except Profile.DoesNotExist:
            # This handles the case where a User was created without the signal 
            # firing correctly, and an update is attempted.
            print(f"Warning: Profile missing for user {instance.username} during update.")
            pass # Or re-create the profile here: Profile.objects.create(user=instance)
# # signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from users.models import CheckoutSessionRecord
# from django.conf import settings
# import stripe
# import os

# stripe.api_key = os.environ['STRIPE_SECRET_KEY']


# @receiver(post_save, sender=CheckoutSessionRecord)
# def update_stripe_customer_id(sender, instance, created, **kwargs):
#     """
#     Update the stripe_customer_id field in the CheckoutSessionRecord model
#     when a new instance is created.
#     """
#     print('update_stripe_customer_id called')
#     user_email = instance.user.email
#     # Retrieve customer from Stripe
#     customers = stripe.Customer.list(email=user_email).data
#     print(f'{customers = }')
#     if customers:
#         print('customers')
#         stripe_customer_id = customers[0].id
#         instance.stripe_customer_id = stripe_customer_id
#         instance.save()

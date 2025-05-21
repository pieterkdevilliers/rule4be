import os
import json
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date
import stripe
from django.contrib.auth import login
from django.contrib.auth.models import User
from users.models import UserProfile, CheckoutSessionRecord


def subscribe(request) -> HttpResponse:
    """
    Renders the subscription page.
    """
    user = request.user

    context = {
        'user': user,
    }

    return render(request, 'rule4be/subscribe.html', context)


def cancel(request) -> HttpResponse:
    """
    Renders the cancel page.
    """
    return render(request, 'rule4be/cancel.html')


def success(request) -> HttpResponse:
    """
    Renders the success page.
    """

    print(f'{request.session = }')

    stripe_checkout_session_id = request.GET['session_id']
    user_profile = UserProfile.objects.get(user=request.user)
    user_profile.account_status = 'active_subscription'
    user_profile.subscription_activation_date = date.today()
    user_profile.save()

    customers = stripe.Customer.list(email=request.user.email).data
    if customers:
        stripe_customer_id = customers[0].id
        instance = CheckoutSessionRecord.objects.get(
            stripe_checkout_session_id=stripe_checkout_session_id
        )
        instance.stripe_customer_id = stripe_customer_id
        instance.is_completed = True
        instance.has_access = True
        instance.save()

    return render(request, 'rule4be/success.html')


def create_checkout_session(request) -> HttpResponse:
    """
    Creates a checkout session for the user to subscribe.
    """
    price_lookup_key = request.POST['price_lookup_key']
    try:
        prices = stripe.Price.list(
            lookup_keys=[price_lookup_key], expand=['data.product'])
        price_item = prices.data[0]

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {'price': price_item.id, 'quantity': 1},
                # You could add differently priced services here, e.g., standard, business, first-class.
            ],
            mode='subscription',
            success_url=DOMAIN + \
            reverse('success') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=DOMAIN + reverse('cancel')
        )

        # We connect the checkout session to the user who initiated the checkout.
        CheckoutSessionRecord.objects.create(
            user=request.user,
            stripe_checkout_session_id=checkout_session.id,
            stripe_price_id=price_item.id,
        )

        return redirect(
            checkout_session.url,  # Either the success or cancel url.
            code=303
        )
    except Exception as e:
        print(e)
        return HttpResponse("Server error", status=500)


def direct_to_customer_portal(request) -> HttpResponse:
    """
    Creates a customer portal for the user to manage their subscription.
    """
    checkout_record = CheckoutSessionRecord.objects.filter(
        user=request.user
    ).last()  # For demo purposes, we get the last checkout session record the user created.

    checkout_session = stripe.checkout.Session.retrieve(
        checkout_record.stripe_checkout_session_id)

    portal_session = stripe.billing_portal.Session.create(
        customer=checkout_session.customer,
        # Send the user here from the portal.
        return_url=DOMAIN + reverse('load_aols_page')
    )
    return redirect(portal_session.url, code=303)


@csrf_exempt
def collect_stripe_webhook(request) -> JsonResponse:
    """
    Stripe sends webhook events to this endpoint.
    We verify the webhook signature and updates the database record.
    """
    webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
    signature = request.META["HTTP_STRIPE_SIGNATURE"]
    payload = request.body
    # print(f'{payload = }')

    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=signature, secret=webhook_secret
        )
    except ValueError as e:  # Invalid payload.
        raise ValueError(e)
    except stripe.error.SignatureVerificationError as e:  # Invalid signature
        raise stripe.error.SignatureVerificationError(e)

    _update_record(event)

    return JsonResponse({'status': 'success'})


def _update_record(webhook_event) -> None:
    """
    We update our database record based on the webhook event.

    Use these events to update your database records.
    You could extend this to send emails, update user records, set up different access levels, etc.
    """
    data_object = webhook_event['data']['object']
    event_type = webhook_event['type']

    if event_type == 'checkout.session.completed':
        print('checkout.session.completed')
        checkout_record = CheckoutSessionRecord.objects.get(
            stripe_checkout_session_id=data_object['id']
        )
        checkout_record.stripe_customer_id = data_object['customer']
        checkout_record.has_access = True
        checkout_record.save()
        print('🔔 Payment succeeded!')

    elif event_type == 'customer.subscription.created':
        print('🎟️ Subscription created')

    elif event_type == 'customer.subscription.updated':
        print('✍️ Subscription updated')

    elif event_type == 'customer.subscription.deleted':
        checkout_record = CheckoutSessionRecord.objects.get(
            stripe_customer_id=data_object['customer']
        )
        checkout_record.has_access = False
        checkout_record.save()

        user_profile = UserProfile.objects.get(
            user=checkout_record.user)
        user_profile.account_status = 'cancelled_subscription'
        user_profile.subscription_cancellation_date = date.today()
        user_profile.save()
        print('✋ Subscription canceled: %s', data_object.id)

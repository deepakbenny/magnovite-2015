from django.conf import settings
from django.db import models

from app.main.models import Profile
from app.event.models import Event


def create_invoice(invoice_type, profile, event=None, workshop=None):
    invoice = Invoice(
        profile=profile,
        invoice_type=invoice_type,
    )

    if invoice_type == 'team':
        invoice.description = 'Registration for ' + event.title
        invoice.amount = 500
        invoice.event = event
    elif invoice_type == 'single':
        invoice.description = 'Subscription for Single Pack'
        invoice.amount = 100
    elif invoice_type == 'multiple':
        invoice.description = 'Subscription for Multiple Pack'
        invoice.amount = 200
    elif invoice_type == 'upgrade':
        # upgrade condition must be checked before calling this fn
        invoice.description = 'Upgrade to Multiple Pack'
        invoice.amount = 100
    elif invoice_type == 'test':
        invoice.description = 'Test Payment'
        invoice.amount = 20
    elif invoice_type == 'workshop':
        invoice.description = 'Workshop registration for ' + workshop.title
        invoice.amount = workshop.price

    else:
        return None

    invoice.save()
    return invoice


class Invoice(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    profile = models.ForeignKey(Profile)

    # if invoice is for a team event
    event = models.ForeignKey(Event, blank=True, null=True)

    invoice_type = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    amount = models.IntegerField(max_length=5)

    pending = models.BooleanField(default=True)
    success = models.BooleanField(default=False)

    status = models.CharField(max_length=50, blank=True)
    post_data = models.TextField()

    def get_id(self):
        if settings.DEBUG:
            return 'debug-' + str(self.id)
        else:
            return 'prod-' + str(self.id)

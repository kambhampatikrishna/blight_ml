from django import forms

class TicketForm(forms.Form):
    ticket_id = forms.CharField(label = "Enter the ticket Id", max_length=100)



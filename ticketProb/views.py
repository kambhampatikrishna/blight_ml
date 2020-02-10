from django.shortcuts import render
from .models  import BlightModel 
from .forms import TicketForm








# Create your views here.def main(request):
def ticketId(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket_id = form.cleaned_data['ticket_id']
            displayProbabality = BlightModel.objects.get(ticket_id=ticket_id)
            if(displayProbabality):
                displayErrorMessage = False
                displayMessage = displayProbabality.probability
            else:
                displayErrorMessage = True
                displayMessage = "Invalid Ticket Id"
            return render(request, template_name = 'display.html', context = {'displayErrorMessage': displayErrorMessage, 'displayMessage': displayMessage})
    else:
        form = TicketForm()
        return render(request,template_name = 'ticketSearch.html', context = {'form': form})
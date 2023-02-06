from django.shortcuts import render
from .models import WithdrawRequest

def withdraw(request):
    if request.method == "POST":
        value = request.POST.get("value")
        network_type = request.POST.get("network_type")
        address = request.POST.get("address")
        encryption = request.POST.get("encryption")
        withdraw_system = WithdrawSystem()
        result, message = withdraw_system.validate_input(value, network_type, address, encryption)
        if result:
            withdraw_request = WithdrawRequest(value=value, network_type=network_type, address=address, encryption=encryption)
            withdraw_request.save()
            withdraw_system.run(value, network_type, address, encryption)
            message = "Withdraw request submitted successfully."
        context = {"message": message}
        return render(request, "withdraw.html", context)
    return render(request, "withdraw.html")

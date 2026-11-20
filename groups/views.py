from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import subscription_required
from .models import Group, BillSpliting
from .form1 import BillSplitForm
from django.db.models import Sum
from notifications.utils import group_bill_message, group_member_links


@login_required
@subscription_required
def split_bill(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    members = group.members.all()

    if request.method == "POST":

        form = BillSplitForm(request.POST, group=group)

        if form.is_valid():

            bill_name = form.cleaned_data['bill_name']
            total_amount = form.cleaned_data['total_amount']
            paid_by = form.cleaned_data['paid_by']

            split_amount = total_amount / members.count()

            for member in members:
                status = 'received' if member == paid_by else 'pending'

                BillSpliting.objects.create(
                    group=group,
                    bill_name=bill_name,
                    total_amount=total_amount,
                    member=member,
                    split_amount=split_amount,
                    paid_by=paid_by,
                    status=status
                )

            return redirect('group_detail', group_id=group.id)

    else:

        form = BillSplitForm(group=group)

    return render(request, 'groups/split_bill.html', {
        'form': form,
        'group': group
    })


from .form1 import GroupForm


@login_required
@subscription_required
def create_group(request):
    if request.method == "POST":
        form = GroupForm(request.POST, user=request.user)
        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user
            group.save()
            form.save_m2m()
            return redirect('ledger_dashboard')
    else:
        form = GroupForm(user=request.user)

    return render(request, 'groups/create_group.html', {'form': form})


@login_required
@subscription_required
def group_list(request):
    groups = Group.objects.filter(created_by=request.user)

    return render(request, 'groups/group_list.html', {
        'groups': groups
    })


@login_required
@subscription_required
def group_detail(request, group_id):

    group = get_object_or_404(Group, id=group_id, created_by=request.user)

    bills = BillSpliting.objects.filter(group=group)

    summary = (
        BillSpliting.objects
        .filter(group=group)
        .values('member__name')
        .annotate(total=Sum('split_amount'))
    )

    latest_bill = bills.last()

    member_links = []

    if latest_bill:

        message = group_bill_message(
            request.user,
            group,
            latest_bill.bill_name,
            latest_bill.total_amount
        )

        # Only pending members
        pending_members = BillSpliting.objects.filter(
            group=group,
            bill_name=latest_bill.bill_name,
            status='pending'
        )

        for bill in pending_members:

            member = bill.member

            wa = None
            mail = None

            if member.phone:
                wa = f"https://wa.me/{member.phone}?text={message}"

            if member.email:
                mail = f"mailto:{member.email}?subject=Bill Reminder&body={message}"

            member_links.append({
                "name": member.name,
                "wa": wa,
                "mail": mail
            })

    return render(request, 'groups/group_details.html', {
        'group': group,
        'bills': bills,
        'summary': summary,
        'member_links': member_links
    })
def mark_received(request, bill_id):
    bill = get_object_or_404(BillSpliting, id=bill_id)

    bill.status = "received"
    bill.save()

    return redirect('group_detail', group_id=bill.group.id)

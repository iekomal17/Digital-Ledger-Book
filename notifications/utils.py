from urllib.parse import quote
import urllib.parse


def individual_transaction_message(user, contact, amount, transaction_type):
    message = f"""
Hello {contact.name},

A transaction has been recorded in Digital Ledger.

User: {user.username}
Type: {transaction_type}
Amount: ₹{amount}

Please check your records.

Digital Ledger System
"""

    return message


import urllib.parse


def whatsapp_link(phone, message):
    if not phone:
        return None

    phone = phone.replace("+", "").replace(" ", "")

    encoded_message = urllib.parse.quote(message)

    return f"https://wa.me/{phone}?text={encoded_message}"


def email_link(email, message):
    if not email:
        return None

    subject = quote("Ledger Notification")
    body = quote(message)

    return f"mailto:{email}?subject={subject}&body={body}"


def shop_transaction_message(shop, customer, amount, transaction_type):
    message = f"""
Hello {customer.name},

A transaction has been recorded with your shop account.

Shop: {shop.username}
Type: {transaction_type}
Amount: ₹{amount}

Please check your records.

Digital Ledger System
"""

    return message


def group_bill_message(user, group, bill_name, amount):
    message = f"""
Hello,

A new bill has been created in group "{group.name}".

Bill: {bill_name}
Total Amount: ₹{amount}

Created by: {user.username}

Please check and settle your share.

Thank you.
"""
    return message


def group_member_links(group, message):
    members = group.members.all()

    links = []

    for m in members:

        phone = getattr(m, 'phone', None)
        email = getattr(m, 'email', None)

        wa = None
        mail = None

        if phone:
            wa = whatsapp_link(phone, message)

        if email:
            mail = email_link(email, message)

        links.append({
            "name": m.name,
            "wa": wa,
            "mail": mail
        })

    return links

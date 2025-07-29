import razorpay
client = razorpay.Client(auth=("rzp_test_OuDQrJBFtx1FGW", "tpzFMQ1naRlyexmVUJ2k79iw"))

data=client.order.create({
  "amount": 50,
  "currency": "INR",
  "receipt": "receipt#1",
  "notes": {
    "key1": "value3",
    "key2": "value2"
  }
})


data2=client.order.fetch(data['id'])
data4=client.payment.fetch(paymentId)
data3=client.payment.capture(paymentId,{
  "amount" : 50,
  "currency" : "INR"
})

print(data)
print(data2)



# from flask import Flask, render_template_string, request, redirect, url_for
# import razorpay
# import os
#
# app = Flask(__name__)
#
# # Razorpay API credentials
# RAZORPAY_KEY_ID = "rzp_test_OuDQrJBFtx1FGW"
# RAZORPAY_KEY_SECRET = "tpzFMQ1naRlyexmVUJ2k79iw"
#
# # Initialize Razorpay client
# client = razorpay.Client(FinceptAuthModule=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
#
# # HTML template for the payment page
# payment_page = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>Razorpay Payment</title>
#     <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
# </head>
# <body>
#     <h1>Pay ₹500</h1>
#     <form action="{{ url_for('payment_success') }}" method="POST">
#         <script
#             src="https://checkout.razorpay.com/v1/checkout.js"
#             data-key="{{ key_id }}"
#             data-amount="{{ amount }}"
#             data-currency="INR"
#             data-order_id="{{ order_id }}"
#             data-buttontext="Pay with Razorpay"
#             data-name="Test Company"
#             data-description="Test Transaction"
#             data-image="https://your_logo_url.com/logo.png"
#             data-prefill.name="John Doe"
#             data-prefill.email="john.doe@example.com"
#             data-prefill.contact="9999999999"
#             data-theme.color="#F37254"
#         ></script>
#         <input type="hidden" name="order_id" value="{{ order_id }}">
#     </form>
# </body>
# </html>
# """
#
# @app.route('/')
# def home():
#     # Create a new order
#     order_amount = 50000  # Amount in paise (₹500)
#     order_currency = 'INR'
#     order_receipt = 'order_rcptid_11'
#
#     order = client.order.create({
#         'amount': order_amount,
#         'currency': order_currency,
#         'receipt': order_receipt,
#         'payment_capture': 1  # Auto-capture
#     })
#
#     order_id = order['id']
#
#     # Render the payment page with the order details
#     return render_template_string(payment_page, key_id=RAZORPAY_KEY_ID, amount=order_amount, order_id=order_id)
#
# @app.route('/payment/success/', methods=['POST'])
# def payment_success():
#     # Retrieve payment details from the request
#     payment_id = request.form.get('razorpay_payment_id')
#     order_id = request.form.get('order_id')
#     signature = request.form.get('razorpay_signature')
#
#     # Verify the payment signature
#     params_dict = {
#         'razorpay_order_id': order_id,
#         'razorpay_payment_id': payment_id,
#         'razorpay_signature': signature
#     }
#
#     try:
#         client.utility.verify_payment_signature(params_dict)
#         # Payment signature is valid. Proceed with order fulfillment.
#         return "Payment Successful"
#     except razorpay.errors.SignatureVerificationError:
#         # Invalid signature. Possible tampering detected.
#         return "Payment Verification Failed", 400
#
# if __name__ == '__main__':
#     app.run(debug=True)

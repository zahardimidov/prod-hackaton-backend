from yookassa import Configuration, Payment

Configuration.account_id = '986380'
Configuration.secret_key = 'test_-eujruQjhy1Ifg259CiC4osm25gIhbnvah88hZWeGuA'

payment = Payment.create({
    "amount": {
        "value": "100.00",
        "currency": "RUB"
    },
    "confirmation": {
        "type": "redirect",
        "return_url": "https://playcloud.pro"
    },
    "capture": True,
    "description": "Заказ №37",
    "metadata": {
      "order_id": "37"
    }
})

print(payment.confirmation.confirmation_url)
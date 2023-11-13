payload = "<?xml version='1.0' encoding='UTF-8'?>\r\n<TKKPG>\r\n    " \
                  "<Request>\r\n        <Operation>GetOrderStatus</Operation>\r\n        " \
                  "<Language>EN</Language>\r\n        " \
                  "<Order>\r\n            " \
                  "<Merchant>11070020</Merchant>\r\n            " \
                  "<OrderID>" + str(1111) + "</OrderID>\r\n            " \
                                                     "</Order>\r\n    " \
                                                     "<SessionID>" + str(
            "bank_session_id") + "</SessionID>\r\n            " \
                               "</Request>\r\n</TKKPG>\r\n"


print(payload)
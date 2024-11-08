from pychatgpt import ChatGPT

while True:
    chat = ChatGPT(headless=False, uc_driver=True)
    res = chat.predict("""
As a genius expert, your task is to understand the content and provide
        the parsed objects in json that match the following json_schema:


        {
  "$defs": {
    "CustomStatus": {
      "properties": {
        "status": {
          "anyOf": [
            {
              "enum": [
                "1C",
                "1F"
              ],
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Status"
        },
        "date": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Date"
        }
      },
      "title": "CustomStatus",
      "type": "object"
    },
    "CustomStatusHistory": {
      "properties": {
        "status_history": {
          "anyOf": [
            {
              "items": {
                "$ref": "#/$defs/CustomStatus"
              },
              "type": "array"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Status History"
        }
      },
      "title": "CustomStatusHistory",
      "type": "object"
    },
    "DeliveryInfo": {
      "properties": {
        "delivery_type": {
          "anyOf": [
            {
              "enum": [
                "UPS",
                "FEDEX",
                "USPS",
                "LTL"
              ],
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Delivery Type"
        },
        "carrier": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Carrier"
        },
        "qty": {
          "anyOf": [
            {
              "type": "integer"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Qty"
        },
        "unit": {
          "anyOf": [
            {
              "enum": [
                "PCS",
                "PLT"
              ],
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": "PCS",
          "title": "Unit"
        }
      },
      "title": "DeliveryInfo",
      "type": "object"
    },
    "ETA": {
      "properties": {
        "flight_number": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Flight Number"
        },
        "airport_code": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Airport Code"
        },
        "datetime": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Datetime"
        }
      },
      "title": "ETA",
      "type": "object"
    },
    "LastMile": {
      "properties": {
        "parts": {
          "anyOf": [
            {
              "items": {
                "$ref": "#/$defs/DeliveryInfo"
              },
              "type": "array"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Parts"
        }
      },
      "title": "LastMile",
      "type": "object"
    },
    "PickupDeliveryInfo": {
      "properties": {
        "pickup_carrier": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Pickup Carrier"
        },
        "pickup_cbm": {
          "anyOf": [
            {
              "type": "number"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Pickup Cbm"
        },
        "delivery_carrier": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Delivery Carrier"
        },
        "date": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Date"
        }
      },
      "title": "PickupDeliveryInfo",
      "type": "object"
    },
    "Quantity": {
      "properties": {
        "num_pcs": {
          "anyOf": [
            {
              "type": "integer"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Num Pcs"
        },
        "num_pallets": {
          "anyOf": [
            {
              "type": "integer"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Num Pallets"
        }
      },
      "title": "Quantity",
      "type": "object"
    },
    "TerminalCharge": {
      "properties": {
        "amount": {
          "anyOf": [
            {
              "type": "number"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Amount"
        },
        "payment_status": {
          "anyOf": [
            {
              "const": "PAID",
              "enum": [
                "PAID"
              ],
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Payment Status"
        }
      },
      "title": "TerminalCharge",
      "type": "object"
    },
    "Weight": {
      "properties": {
        "weight_chargable": {
          "anyOf": [
            {
              "type": "number"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Weight Chargable"
        },
        "weight_gross": {
          "anyOf": [
            {
              "type": "number"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Weight Gross"
        },
        "weight_unit": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": "KG",
          "title": "Weight Unit"
        }
      },
      "title": "Weight",
      "type": "object"
    }
  },
  "properties": {
    "order_date": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Order Date"
    },
    "airway_bill_number": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Airway Bill Number"
    },
    "order_status": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Order Status"
    },
    "eta": {
      "anyOf": [
        {
          "$ref": "#/$defs/ETA"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "airline": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Airline"
    },
    "customer": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Customer"
    },
    "quantity": {
      "anyOf": [
        {
          "$ref": "#/$defs/Quantity"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "weight": {
      "anyOf": [
        {
          "$ref": "#/$defs/Weight"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "last_free_date": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Last Free Date"
    },
    "terminal_cost": {
      "anyOf": [
        {
          "$ref": "#/$defs/TerminalCharge"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "custom_status": {
      "anyOf": [
        {
          "$ref": "#/$defs/CustomStatusHistory"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "pickup_delivery": {
      "anyOf": [
        {
          "$ref": "#/$defs/PickupDeliveryInfo"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "last_mile_info": {
      "anyOf": [
        {
          "$ref": "#/$defs/LastMile"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "note": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Note"
    },
    "operator": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Operator"
    }
  },
  "title": "AirShipment",
  "type": "object"
}

        Make sure to return an instance of the JSON, not the schema itself

Below is the corresponding values of different columns in a table row:
	DATE : 2023-07-01 00:00:00
	AWB #:  297-16131500
	STATUS: Invoiced
	ETA: 7/3 17:20
	HAWB#: nan
	AIRLINE: China Airline
	CUSTOMER: 九方
	PCS/PALLETS : 98PCS
	WEIGHT: 1967KGS
	LFD : 7/4 5PM
	T/C: 232.26
	1C/1F: 1C
	P/U DATE: 2023-07-04 00:00:00
	S/P OUT: nan
	PU/DO: 11.488CBM ATS 7.4
	DELIVERY INFO: 95 FEDEX + 1 (3PCS) LTL ATS 7.4
	NOTE: READY FOR PICKUP, 5SKIDS EXCH
	OP: ZY
	INV?: Y
	COST: 389.62
	REVENUE: 950.15
	PROFIT: 560.53
                       
Your response should be in json ONLY!
""")
    print("Final response:")
    print("\n".join([x["content"] for x in res["response"]]))
    chat._driver.quit()
    input()
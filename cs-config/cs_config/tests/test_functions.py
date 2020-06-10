from cs_kit import CoreTestFunctions

from cs_config import functions


class TestFunctions1(CoreTestFunctions):
    get_version = functions.get_version
    get_inputs = functions.get_inputs
    validate_inputs = functions.validate_inputs
    run_model = functions.run_model
    ok_adjustment = {
        "Model Parameters" : {
              "Days": [
                {"value": "1,2,3,4,5,6,7,8,9"}
              ],
              "NumTests":[
                {"value" : "1000,1000,2000,2000,3000,3000,4000,4000,5000"}
              ],
              "NumPositive":[
                {"value" : "500,500,700,700,1000,1000,1500,1500,3000"}
              ]
        }
    }
    bad_adjustment = {
      "Model Parameters" :
      {
      "Days": [
        {"value" : True}
      ]
      }
    }

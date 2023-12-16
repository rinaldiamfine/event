from apps.committee.models import (
    CommitteeModel
)

class CommitteeHelpers:
    def __init__(
        self,
        api=None,
        method=None,
    ):
        self.api = api
        self.method = method

    def authentication(self, values: dict):
        try:
            committee_id = CommitteeModel.query.filter(
                CommitteeModel.username==values.get('username'),
            ).first()
            result = {}
            if (committee_id):
                if (committee_id.password == values.get('password')):
                    result = {
                        "success": True,
                        "message": "Success login",
                        "data": {
                            "id_committee": committee_id.id,
                            "name": committee_id.name,
                            "role": committee_id.role,
                        },
                    }
                else:
                    result = {
                        "success": False,
                        "message": "Invalid, Password is not correct",
                        "data": None,
                    }
            else:
                result = {
                    "success": False,
                    "message": "Invalid, Please check your username again",
                    "data": None,
                }
            return True, result
        except Exception as e:
            return False, e
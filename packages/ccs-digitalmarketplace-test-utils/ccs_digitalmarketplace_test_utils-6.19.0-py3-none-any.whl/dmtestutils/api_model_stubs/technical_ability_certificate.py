from .base import BaseAPIModelStub


class TechnicalAbilityCertificateStub(BaseAPIModelStub):
    resource_name = "technicalAbilityCertificates"
    default_data = {
        "id": 123,
        "frameworkFamily": "g-cloud",
        "frameworkFramework": "g-cloud",
        "frameworkSlug": "g-cloud-15",
        "lotName": "Software as a Service (SaaS)",
        "lotNumber": "2b",
        "lotSlug": "saas",
        "supplierId": 886665,
        "supplierName": "Elma B.L.A.D.E",
        "status": "in_progress",
        "authenticationId": None,
        "sentAt": None,
        "electronicSigniture": None,
        "approvedAt": None,
    }
    optional_keys = [
        ("supplierId", "supplier_id"),
        ("supplierName", "supplier_name"),
        ("frameworkFamily", "framework_family"),
        ("frameworkFramework", "framework_framework"),
        ("frameworkSlug", "framework_slug"),
        ("lotSlug", "lot_slug"),
        ("lotName", "lot_name"),
        ("lotNumber", "lot_number"),
        ("status", "status"),
        ("authenticationId", "authentication_id"),
        ("electronicSigniture", "electronic_signiture"),
        ("sentAt", "sent_at"),
        ("approvedAt", "approved_at"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if kwargs.get("status") in ["awaiting_approval", "approved"]:
            if self.response_data["authenticationId"] is None:
                self.response_data["authenticationId"] = "AAABBBCCC"
            if self.response_data["sentAt"] is None:
                self.response_data["sentAt"] = "2025-05-16T12:00:00.000000Z"

        if kwargs.get("status") == "approved":
            if self.response_data["electronicSigniture"] is None:
                self.response_data["electronicSigniture"] = "Jack Vandham"
            if self.response_data["approvedAt"] is None:
                self.response_data["approvedAt"] = "2025-05-17T12:00:00.000000Z"

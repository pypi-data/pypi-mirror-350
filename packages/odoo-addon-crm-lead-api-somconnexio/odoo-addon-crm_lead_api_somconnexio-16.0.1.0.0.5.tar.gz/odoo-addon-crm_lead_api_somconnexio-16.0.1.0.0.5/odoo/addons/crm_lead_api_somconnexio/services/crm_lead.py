from werkzeug.exceptions import BadRequest
from odoo.addons.base_rest.http import wrapJsonException
from odoo.addons.component.core import Component
from . import schemas


class CRMLeadService(Component):
    _inherit = "base.rest.service"
    _name = "crm.lead.services"
    _usage = "crm-lead"
    _collection = "sc.api.key.services"
    _description = """
        CRMLead requests
    """

    # pylint: disable=method-required-super
    def create(self, **params):
        params = self._prepare_create(params)
        # tracking_disable=True in context is needed
        # to avoid to send a mail in CRMLead creation
        sr = self.env["crm.lead"].with_context(tracking_disable=True).create(params)
        return self._to_dict(sr)

    def _validator_create(self):
        return schemas.S_CRM_LEAD_CREATE

    def _validator_return_create(self):
        return schemas.S_CRM_LEAD_RETURN_CREATE

    @staticmethod
    def _to_dict(crm_lead):
        return {"id": crm_lead.id}

    def _get_country(self, code):
        country = self.env["res.country"].search([("code", "=", code)])
        if country:
            return country
        else:
            raise wrapJsonException(
                BadRequest("No country for isocode %s" % code),
                include_description=True,
            )

    def _get_state(self, code, country_id):
        state = self.env["res.country.state"].search(
            [("code", "=", code), ("country_id", "=", country_id)]
        )
        if state:
            return state
        else:
            raise wrapJsonException(
                BadRequest(
                    "No state for isocode %s and country id %s"
                    % (code, str(country_id))
                ),
                include_description=True,
            )

    def _prepare_adresss_from_partner(self, partner, key):
        country_id = partner.country_id.id
        state_id = partner.state_id.id
        return {
            "{}_street".format(key): partner.street,
            "{}_street2".format(key): partner.street2,
            "{}_zip_code".format(key): partner.zip,
            "{}_city".format(key): partner.city,
            "{}_state_id".format(key): state_id,
            "{}_country_id".format(key): country_id,
        }

    def _prepare_address(self, address, key):
        country_id = self._get_country(address["country"]).id
        state_id = self._get_state(address["state"], country_id).id
        return {
            "{}_street".format(key): address["street"],
            "{}_street2".format(key): address.get("street2"),
            "{}_zip_code".format(key): address["zip_code"],
            "{}_city".format(key): address["city"],
            "{}_state_id".format(key): state_id,
            "{}_country_id".format(key): country_id,
        }

    def _prepare_delivery_address(self, isp_info):
        if isp_info.get("delivery_address"):
            delivery_address = isp_info.pop("delivery_address")
            return self._prepare_address(delivery_address, "delivery")
        else:
            if isp_info.get("icc"):
                return {}
            elif self.partner_id:
                partner = self.env["res.partner"].browse(self.partner_id)
                invoice_address = self.env["res.partner"].search(
                    [("parent_id", "=", self.partner_id), ("type", "=", "invoice")]
                )
                return self._prepare_adresss_from_partner(
                    invoice_address or partner, "delivery"
                )
        raise wrapJsonException(
            BadRequest("ISP Info with neither delivery_address nor partner_id"),
            include_description=True,
        )

    def _prepare_create_mobile_isp_info(self, isp_info, without_fix=False):
        isp_info = self._prepare_create_isp_info(isp_info, without_fix)

        if "icc" in isp_info.keys():
            isp_info["has_sim"] = True
        return isp_info

    def _prepare_create_broadband_isp_info(self, isp_info, without_fix=False):
        isp_info = self._prepare_create_isp_info(isp_info, without_fix)

        if without_fix:
            isp_info["previous_phone_number"] = isp_info.get("phone_number", "-")
            isp_info["phone_number"] = "-"
        elif isp_info.get("phone_number") and isp_info["type"] == "portability":
            isp_info["keep_phone_number"] = True

        if "service_address" in isp_info.keys():
            service_address_dict = self._prepare_address(
                isp_info["service_address"], "service"
            )
            isp_info.pop("service_address")
            isp_info.update(service_address_dict)
        return isp_info

    def _prepare_create_isp_info(self, isp_info, without_fix=False):
        delivery_address_dict = self._prepare_delivery_address(isp_info)
        isp_info.update(delivery_address_dict)
        vals = isp_info.keys()

        if "invoice_address" in vals:
            invoice_address_dict = self._prepare_address(
                isp_info["invoice_address"], "invoice"
            )
            isp_info.pop("invoice_address")
            isp_info.update(invoice_address_dict)

        if "phone_number" not in vals and isp_info["type"] == "portability":
            isp_info["phone_number"] = "-"
            isp_info["no_previous_phone_number"] = True

        if "fiber_linked_to_mobile_offer" in vals:
            fiber_contract = self.env["contract.contract"].search(
                [("code", "=", isp_info["fiber_linked_to_mobile_offer"])]
            )
            isp_info.pop("fiber_linked_to_mobile_offer")
            isp_info["linked_fiber_contract_id"] = (
                fiber_contract.id if fiber_contract else False
            )

        return isp_info

    def _prepare_create_line(self, line, iban):
        product = self.env["product.product"].search(
            [("default_code", "=", line["product_code"])]
        )
        if not product:
            raise wrapJsonException(
                BadRequest("Product with code %s not found" % (line["product_code"],)),
                include_description=True,
            )
        response_line = {
            "name": product.name,
            "product_id": product.id,
            "product_tmpl_id": product.product_tmpl_id.id,
            "category_id": product.categ_id.id,
            "iban": iban,
        }
        if line.get("broadband_isp_info"):
            response_line["broadband_isp_info"] = (
                self.env["broadband.isp.info"]
                .create(
                    self._prepare_create_broadband_isp_info(
                        line["broadband_isp_info"], without_fix=product.without_fix
                    )
                )
                .id
            )
        elif not self._needs_mobile_isp_info(product):
            raise wrapJsonException(
                BadRequest(
                    "Broadband product %s needs a broadband_isp_info"
                    % (line["product_code"],)
                ),
                include_description=True,
            )

        if line.get("mobile_isp_info"):
            response_line["mobile_isp_info"] = (
                self.env["mobile.isp.info"]
                .create(self._prepare_create_mobile_isp_info(line["mobile_isp_info"]))
                .id
            )
        elif self._needs_mobile_isp_info(product.product_tmpl_id):
            raise wrapJsonException(
                BadRequest(
                    "Mobile product %s needs a mobile_isp_info"
                    % (line["product_code"],)
                ),
                include_description=True,
            )
        return response_line

    def _needs_mobile_isp_info(self, product_tmpl):
        mobile = self.env.ref("somconnexio.mobile_service")
        if mobile.id == product_tmpl.categ_id.id:
            return True

    def _partner_id(self, partner_id):
        if not partner_id:
            return False

        partner = self.env["res.partner"].search([("ref", "=", partner_id)])
        if not partner:
            raise wrapJsonException(
                BadRequest("Partner with id %s not found" % (partner_id)),
                include_description=True,
            )
        return partner.id

    def _get_tag_ids(self, codes):
        """Return the unic lead tag that we manage if a tag_code is provided."""
        # TODO: Review this logic after the migration and the tag code removal.
        if not codes:
            return []
        return [self.env.ref("crm_lead_api_somconnexio.first_month_free").id]

    def _get_team_id(self, is_company):
        return (
            self.env.ref("somconnexio.business").id
            if is_company
            else self.env.ref("somconnexio.residential").id
        )

    def _prepare_create(self, params):
        self.partner_id = self._partner_id(params.get("partner_id"))
        iban = params.get("iban")
        phone = params.get("phone")
        tag_ids = self._get_tag_ids(params.get("tag_codes", []))
        is_company = params.get("is_company", False)
        crm_lines_args = [
            self._prepare_create_line(line, iban) for line in params["lead_line_ids"]
        ]
        crm_lines = self.env["crm.lead.line"].create(crm_lines_args)
        return {
            # TODO: What do we want to put in the CRMLead name and CRMLeadName?
            "name": "New CRMLead",
            "partner_id": self.partner_id,
            "phone": phone,
            "lead_line_ids": [(6, 0, [line.id for line in crm_lines])],
            "tag_ids": [(6, 0, tag_ids)],
            "team_id": self._get_team_id(is_company),
        }

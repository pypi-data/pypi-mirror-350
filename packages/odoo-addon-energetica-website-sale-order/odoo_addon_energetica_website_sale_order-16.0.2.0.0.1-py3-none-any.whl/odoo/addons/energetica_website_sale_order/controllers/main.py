import base64

from odoo import http
from odoo.http import request


class WebsiteContract(http.Controller):
    @http.route(
        ["/contract-application",],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def display_page(self, **kwargs):
        values = self.fill_values()
        return request.render("energetica_website_sale_order.contract_template", values)

    def fill_values(self):
        partner = request.env.user.partner_id
        values = {}
        if partner.street:
            values["service_street"] = partner.street
            values["titular_street"] = partner.street
        if partner.city:
            values["service_city"] = partner.city
            values["titular_city"] = partner.city
        if partner.zip:
            values["service_zip_code"] = partner.zip
            values["titular_zip_code"] = partner.zip
        if partner.firstname:
            values["titular_firstname"] = partner.firstname
        if partner.lastname:
            values["titular_lastname"] = partner.lastname
        if partner.email:
            values["titular_email"] = partner.email
        if partner.phone:
            values["titular_phone"] = partner.phone
        values["service_states"] = self.get_states()
        values["titular_states"] = self.get_states()
        values["products"] = self.get_products()
        return values

    @http.route(
        ["/contract-application-created"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )  
    def create_contract(self, **kwargs):
        partner = request.env.user.partner_id
        SaleOrder = request.env["sale.order"]
        SaleOrderLine = request.env["sale.order.line"]
        IrAttachment = request.env["ir.attachment"]

        # List of file to add to ir_attachment once we have the ID
        post_file = []
        # Info to add after the message
        post_description = []

        for field_name, field_value in kwargs.items():
            if hasattr(field_value, "filename") and field_value:
                post_file.append(field_value)
        
        values = {
            "partner_id": partner.id,
            "cups": kwargs.get("cups"),
            "is_light": kwargs.get("is_light"),
            "service_street": kwargs.get("service_street"),
            "service_floor": kwargs.get("service_floor"),
            "service_door": kwargs.get("service_door"),
            "service_state_id": kwargs.get("service_state_id"),
            "service_city": kwargs.get("service_city"),
            "service_zip_code": kwargs.get("service_zip_code"),
            "is_home": kwargs.get("is_home"),
            "cnae": kwargs.get("cnae"),
            "cadastral_reference": kwargs.get("cadastral_reference"),
            "statement": kwargs.get("statement"),
            "power_type": kwargs.get("power_type"),
            "current_power_point": kwargs.get("current_power_point"),
            "current_power_valley": kwargs.get("current_power_valley"),
            "current_power_p1": kwargs.get("current_power_p1"),
            "current_power_p2": kwargs.get("current_power_p2"),
            "current_power_p3": kwargs.get("current_power_p3"),
            "current_power_p4": kwargs.get("current_power_p4"),
            "current_power_p5": kwargs.get("current_power_p5"),
            "current_power_p6": kwargs.get("current_power_p6"),
            "selfconsume": kwargs.get("selfconsume"),
            "installation": kwargs.get("installation"),
            "voltage_installation_type": kwargs.get("voltage_installation_type"),
            "cau": kwargs.get("cau"),
            "installation_power": kwargs.get("installation_power"),
            "installation_situation": kwargs.get("installation_situation"),
            "installation_type": kwargs.get("installation_type"),
            "auxiliar_service": kwargs.get("auxiliar_service"),
            "tariff": kwargs.get("tariff"),
            "titular_nif": kwargs.get("titular_nif"),
            "is_previous_titular": kwargs.get("is_previous_titular"),
            "titular_firstname": kwargs.get("titular_firstname"),
            "titular_lastname": kwargs.get("titular_lastname"),
            "titular_street": kwargs.get("titular_street"),
            "titular_floor": kwargs.get("titular_floor"),
            "titular_door": kwargs.get("titular_door"),
            "titular_state_id": kwargs.get("titular_state_id"),
            "titular_city": kwargs.get("titular_city"),
            "titular_zip_code": kwargs.get("titular_zip_code"),
            "titular_email": kwargs.get("titular_email"),
            "titular_phone": kwargs.get("titular_phone"),
            "iban": kwargs.get("iban"),
            "iban_statement": kwargs.get("iban_statement"),
            "conditions": kwargs.get("conditions"),
            "payment_conditions": kwargs.get("payment_conditions"),
            "privacy_policy": kwargs.get("privacy_policy"),
            "order_line": [
                (0, 0, {'name': "test", 'product_id': int(kwargs.get("tariff")), 'product_uom_qty': 1}),
            ],
        }
        sale_order_id = SaleOrder.sudo().create(values)

        for field_value in post_file:
            attachment_value = {
                "name": field_value.filename,
                "res_model": "sale.order",
                "res_id": sale_order_id,
                "datas": base64.encodebytes(field_value.read()),
            }
            IrAttachment.sudo().create(attachment_value)

        return request.render("energetica_website_sale_order.energetica_thanks", values)

    def get_states(self):
        # Show only spanish provinces
        states = (
            request.env["res.country.state"].sudo().search([("country_id", "=", 68)])
        )
        return states

    def get_products(self):
        # Show only spanish provinces
        products = (
            request.env["product.template"].sudo().search([("is_contract", "=", True)])
        )
        return products

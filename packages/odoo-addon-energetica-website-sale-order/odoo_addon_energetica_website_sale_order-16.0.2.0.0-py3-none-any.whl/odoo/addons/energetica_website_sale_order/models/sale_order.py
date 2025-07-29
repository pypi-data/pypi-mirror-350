from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    cups = fields.Char()
    is_light = fields.Boolean()
    service_street = fields.Char()
    service_floor = fields.Char()
    service_door = fields.Char()
    service_state_id = fields.Many2one("res.country.state", string="Service Province")
    service_city = fields.Char()
    service_zip_code = fields.Char()
    is_home = fields.Boolean()
    cnae = fields.Char()
    cadastral_reference = fields.Char()
    statement = fields.Boolean()
    voltage_installation_type = fields.Selection(
        selection=[
            ("1", "Monofásica"),
            ("2", "Trifásica")
        ],
    )
    power_type = fields.Char()
    current_power_point = fields.Char()
    current_power_valley = fields.Char()
    current_power_p1 = fields.Char()
    current_power_p2 = fields.Char()
    current_power_p3 = fields.Char()
    current_power_p4 = fields.Char()
    current_power_p5 = fields.Char()
    current_power_p6 = fields.Char()
    selfconsume = fields.Char()
    installation = fields.Char()
    cau = fields.Char()
    installation_power = fields.Char()
    installation_situation = fields.Selection(
        selection=[
            ("1", "Red interior"),
            ("2", "Red interior da varios consumidores (instalación de enlace)"),
            ("3", "Próxima a través de red"),
            ("4", "En red interior pero próxima a través de red del resto de los CUPS del colectivo"),
            ("5", "Próxima a traves de red pero en red interior de otro de los CUPS del colectivo")
        ],
    )
    installation_type = fields.Selection(
        selection=[
            ("1", "[B11] - Instalaciones que únicamente utilicen la radiación solar como energía primaria mediante la tecnología fotovoltaica"),
            ("2", "[B21] - Instalaciones eólicas ubicadas en tierra"),
            ("3", "Otras tecnologias")
        ],
    )
    auxiliar_service = fields.Boolean()
    titular_nif = fields.Char()
    is_previous_titular = fields.Boolean()
    titular_firstname = fields.Char()
    titular_lastname = fields.Char()
    titular_street = fields.Char()
    titular_floor = fields.Char()
    titular_door = fields.Char()
    titular_state_id = fields.Many2one("res.country.state", string="Service Province")
    titular_city = fields.Char()
    titular_zip_code = fields.Char()
    titular_email = fields.Char()
    titular_phone = fields.Char()
    conditions = fields.Boolean()
    payment_conditions = fields.Boolean()
    privacy_policy = fields.Boolean()
    tariff = fields.Many2one("product.template", string="Tariff")
    iban = fields.Char()
    iban_statement = fields.Boolean()


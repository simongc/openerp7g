# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from osv import osv, fields
import re

class hr_employee(osv.osv):
	# HERENCIA DE EMPLEADO EN NOMINA(HR)
	_inherit = 'hr.employee'
	_description = 'Employee'

	# FUNCIÓN PARA TOMAR EL NOMBRE COMPLETO Y REFLEJARLO EN EL CAMPO ORIGINAL DE "NAME" DE HR.EMPLOYEE
	def get_names(self, cr, uid, ids, first_name, first_surname, second_name, second_surname, context=None):
		res = ''
		names = [first_name, first_surname, second_name, second_surname]
		for name in names:
			if name:
				res = res + name + ' '
		return {'value':{'full_name':res}}

	def check_vat_ve(self, vat, context=None):
		""" Check Venezuelan VAT number, locally called RIF.
		RIF: JXXXXXXXXX RIF VENEZOLAN
			 IDENTIFICATION CARD: VXXXXXXXXX
			 FOREIGN IDENTIFICATION CARD: EXXXXXXXXX
		"""

		if context is None:
			context = {}
		if re.search(r'^[VJEGP][0-9]{9}$', vat):
			return True
		if re.search(r'^([VE][0-9]{1,8}|[D][0-9]{9})$', vat):
			return True
		return False

	def search_partner_seniat(self, cr, uid, ids, context=None):
		""" Check vat of the partner and update iva rate
		"""
		if context is None:
			context = {}
		this = self.browse(cr, uid, ids)[0]
		su_obj = self.pool.get('seniat.url')
		rp_obj = self.pool.get('hr.employee')
		vat = this.vat.upper()

		# PERMITE AÑADIR CEDULAS SIN PRECEDER UNA "V"
		newvat = []
		for letter in vat:
			newvat.append(letter)
		if 'V' not in newvat:
			vat = 'V' + vat


		res = {'name': ('The requested contributor does not exist'),
			   'vat_subjected': False, 'vat': vat, 'wh_iva_agent': False,
			   'wh_iva_rate': 0.0}

		if 'VE' in vat:
			vat = vat[2:]



		if rp_obj.check_vat_ve(vat, context=context):
			res = su_obj._dom_giver(cr, uid, vat, context)
		self.write(cr, uid, ids, res)

		return True


	_columns = {
		# CAMPOS NECESARIOS PARA LA FUNCIÓN DE BUSCAR RIF
		'wh_iva_agent': fields.boolean('Withholding Agent', invisible=True),
		'wh_iva_rate': fields.float('Percent of withholding', invisible=True),
		'vat_subjected': fields.boolean('Pay VAY', invisible=True),
		'vat': fields.char('Cédula', size=64, required=False),

		# OCULTA CAMPOS ORIGINALES DEL OPENERP
		'identification_id': fields.char(invisible=True ),
		'otherid': fields.char(invisible=True ),

		# CAMPOS PERSONALIZADOS
		'first_name': fields.char('1er Nombre', size=64, required=False, help='Primer nombre del empleado', ),
		'second_name': fields.char('2do Nombre', size=64, required=False, help='Segundo nombre del empleado',),
		'first_surname': fields.char('1er Apellido', size=64, required=False, help='Primer Apellido del empleado',),
		'second_surname': fields.char('2do Apellido', size=64, required=False, help='Segundo Apellido del empleado',),
		'full_name': fields.char('Nombre Completo', size=120, required=False, help='Nombre completo del empleado',),
		'address_home_id': fields.many2one('hr.address.custom', 'Dirección Particular', domain="[('employee_id.id','=',id)]", help='Dirección de habitación', ),
		'house_phone': fields.char('Teléfono de casa', size=16, required=False, help='Teléfono residencial', ),
		'movil_phone': fields.char('Teléfono Celular', size=16, required=False, help='Teléfono movil personal', ),
		'personal_mail': fields.char('Correo-e Personal', size=64, required=False, help='Correo electrónico personal', ),
		'supervisor': fields.boolean('Es un supervisor', help='Este empleado es un Supervisor ?', ),
		'handedness': fields.selection([('right','Diestro'),('left','Zurdo')],'Lateralidad', default='Derecho', help='Mano hábil del empleado', ),
		}

	_defaults = {
		'handedness': 'right',
		}
  
hr_employee()

# MODELO PARA EL CAMPO DE DIRECCIÓN
class hr_address_custom(osv.osv):

	_description = 'Direccion Particular'
	_name = 'hr.address.custom'
	_rec_name = 'address'

	def get_country(self, cr, uid, ids, state, context=None):
		if state <= 26:
			res = 240
		else:
			res = ''
		return {'value': {'country':res}}



	_columns = {
		'address': fields.char('Dirección', size=200, required=False, help='Dirección (Calle, Carrera, Avenida, Edificio o Casa', ),
		'zipcode': fields.integer('Código postal', size=5, required=False, help='Código postal', ),
		'city': fields.char('Ciudad', size=64, required=False, help='Ciudad', ),
		'state': fields.many2one('hr.state', 'Estado', help='Estado', ),
		'country': fields.many2one('res.country', 'País', help='País', ),
		'employee_id': fields.many2one('hr.employee', invisible=True),
		}

hr_address_custom()

# MODELO PARA EL CAMPO DE ESTADO
class hr_state(osv.osv):

	_description = 'Estado'
	_name = 'hr.state'
	_rec_name = 'state'

	_columns = {
		'state': fields.char('Estado', size=40, required=False),
		'country': fields.many2one('res.country', 'País', help='País', ),
		}

hr_state()




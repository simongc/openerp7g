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
import os
from dateutil.relativedelta import relativedelta
from datetime import date, datetime


class hr_family(osv.osv):

	_inherit = 'hr.employee'
	_description = 'Datos Familiares'

	_columns = {

		# INFORMACIÓN DE EMERGENCIA
		'emergency_contact': fields.char('Contacto de emergencia', size=64, required=False, help='Nombre de la persona de contacto de emergencia', ),
		'emergency_contact_link': fields.char('Parentesco', size=64, required=False, help='Parentesco que relaciona al contacto de emergencia con el empleado',  ),
		'emergency_contact_number': fields.char('Número de teléfono', size=12, required=False, help='Número teléfonico de la persona de contacto', ),
		# DESHABILITA EL CAMPO "NUMERO DE HIJOS"(CHILDREN) ORIGINAL DEL MODULO NÓMINA
		'children': fields.char('Nro de Hijos', size=1, invisible=True),
		# CAMPO DE SELECCIÓN DE NÚMERO DE HIJOS
		'children_custom': fields.char('Nro de Hijos', size=2, help='Número de hijos del empleado', ),

		# INFORMACIÓN DE LOS HIJOS
		'childs': fields.one2many('hr.children','employee_id','Hijos', ),

		# campo relación de prueba -- borrar luego si permite
		# 'employee_id': fields.many2one('hr.employee', invisible=True),

		# solo prueba -- borrar luego
		# 'hijos': fields.many2one('hr.children', 'hijos', domain="[('employee_id.id','=',id)]"),


		# UNIFORMES
		'shirt': fields.char('Camisa', size=20, required=False, help='Talla de camisa del empleado', ),
		'pant': fields.char('Pantalón', size=20, required=False, help='Talla de pantalón del empleado', ),
		'shoe': fields.char('Calzado', size=20, required=False, help='Talla de calzado del empleado', ),




		}

hr_family()

class hr_children(osv.osv):

	_name = 'hr.children'
	# _inherit = 'ir.attachment'
	_rec_name = 'child_name'
	_description = 'Hijos'


	# CALCULA LA EDAD DE CADA HIJO SEGÚN LA FECHA DE NACIMIENTO INTRODUCIDA. Y LA INGRESA EN EL CAMPO AGE
	def set_age(self, cr, uid, ids, birthday, context=None):
		if birthday:
			print(birthday)
			dt = birthday
			d1 = datetime.strptime(dt, "%Y-%m-%d").date()
			d2 = date.today()
		rd = relativedelta(d2, d1)
		if rd.years >= 1:
			age = str(rd.years) + " Año(s)"
		elif rd.months >= 1:
			age = str(rd.months) + " Mes(es)"
		else:
			age = str(rd.days) + " Día(s)"
		return {'value':{'age':age}}

	_columns = {
		'child_name': fields.char('Nombres', size=64, required=False, help='Nombre del hijo' ),
		'child_surname': fields.char('Apellidos', size=64, required=False, help='Apellido del hijo', ),
		'age': fields.char('Edad', size=10, required=False, help='Edad del hijo',  ),
		'employee_id': fields.many2one('hr.employee', invisible=True),
		'birthday': fields.date('Fecha de nacimiento', help='Fecha de nacimiento del hijo', ),
		'instruction_level': fields.many2one('hr.level','Nivel de Educación', help='Nivel de educación cursado por el hijo', ),
		# 'birth_certificate': fields.many2one('ir.attachment', string="Partida de nacimiento", help='Partida de nacimiento del hijo', ),
		'nursery': fields.many2one('nursery', 'Guarderia'),
		}

hr_children()

class nursery(osv.osv):


	_name = 'nursery'
	
	_description = 'Guarderia'

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
		'wh_iva_agent': fields.boolean('Withholding Agent', invisible=True),
		'wh_iva_rate': fields.float('Percent of withholding', invisible=True),
		'vat_subjected': fields.boolean('Pay VAY', invisible=True),
		'name': fields.char('Nombre', size=64, required=False, help='Nombre del registro de la Guarderia' ),
		'nursery': fields.char('Guarderia', size=64, required=False, help='Nombre de la Guarderia' ),
		'vat': fields.char('RIF', size=20, required=False, help='RIF en formato j00000000' ),
		'me_cod': fields.char('Código de ME', size=64, required=False, help='Código de registro de la guarderia en el ministerio de educación', ),
		}

nursery()

class hr_level(osv.osv):

	_name = 'hr.level'
	_description = 'Nivel Educativo'
	_rec_name = 'level'

	_columns = {
		'level': fields.char('Nivel Educativo', size=64, help='Nivel Educativo Cursado por el hijo', ),
		}
hr_level()

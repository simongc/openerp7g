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

class hr_bank(osv.osv):


	_inherit = 'hr.employee'
	_description = 'Datos Bancarios'

	_columns = {

		# DESHABILITA CAMPO CUENTA BANCARIA PREDETERMINADO DE OPENERP
		'bank_account_id': fields.char('Cuenta Bancaria', size=1, invisible=True),


		'bank_account_custom': fields.many2one('hr.bank.account', 'Cuenta Bancaria', domain="[('employee_id.id','=',active_id)]", help='Cuentas bancarias del empleado', ),
		
		}

hr_bank()

# DESCRIPCIÓN DE LOS CAMPOS DE CUENTA BANCARIA
class hr_bank_account(osv.osv):

	# _inherit = 'hr.employee'
	_name = 'hr.bank.account'
	_description = 'Cuenta Bancaria'

	# FUNCTION NAME_GET PARA MOSTRAR NOMBRE DEL BANCO CONCATENADO AL TIPO DE CUENTA
	def name_get(self, cr, uid, ids, context=None):
		if not ids:
			return []
		result = []
		account_default = ''
		for line in self.browse(cr, uid, ids, context=context):
			if line.default == True:
				account_default = '!!Por defecto'
			else:
				account_default = ''
			if line.bank.name:
				if line.account_type:
					result.append((line.id, account_default + ' ' + line.bank.name + ' ' + line.account_type))
				else:
					result.append((line.id, account_default + ' ' + line.bank.name))
		return result
		


	# FUNCIONES PARA TRAER DATOS DE CONTEXTO DEL EMPLEADO QUE SIENDO MODIFICADO, PARA LUEGO HACERLOS DEFAULT
	# def get_id(self, cr, uid, context):
	# 	return context.get('current_id', False)

	# def get_mail(self, cr, uid, context):
	# 	return context.get('current_mail', False)

	# def get_vat(self, cr, uid, context):
	# 	return context.get('current_vat', False)


	_columns = {
		'bank': fields.many2one('res.bank', 'Banco' ),
		'account_number': fields.char('Número de Cuenta', size=64, required=False ),
		'account_holder_id': fields.char('Cédula', size=12, required=False ),
		'account_holder_mail': fields.char('Correo Electrónico', size=64, required=False ),
		'account_type': fields.char('Tipo de Cuenta', size=64, required=False ),
		'employee_id': fields.many2one('hr.employee', 'Titular'),
		'default': fields.boolean('Por defecto'),

		}


	_defaults = {
	# FUNCIONES lambda PARA TRAER DATOS DE CONTEXTO DEL EMPLEADO QUE SIENDO MODIFICADO, PARA LUEGO HACERLOS DEFAULT

		'employee_id': lambda self, cr, uid, c: c.get('current_id', False),
		'account_holder_mail': lambda self, cr, uid, c: c.get('current_mail', False),
		'account_holder_id': lambda self, cr, uid, c: c.get('current_vat', False),
		}

hr_bank_account()


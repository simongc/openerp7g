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

# HORARIOS DE TRABAJO A SELECCIONAR
# hours = [
# 	(100, '1:00am'),
# 	(130, '1:30am'),
# 	(200, '2:00am'),
# 	(230, '2:30am'),
# 	(300, '3:00am'),
# 	(330, '3:30am'),
# 	(400, '4:00am'),
# 	(430, '4:30am'),
# 	(500, '5:00am'),
# 	(530, '5:30am'),
# 	(600, '6:00am'),
# 	(630, '6:30am'),
# 	(700, '7:00am'),
# 	(730, '7:30am'),
# 	(800, '8:00am'),
# 	(830, '8:30am'),
# 	(900, '9:00am'),
# 	(930, '9:30am'),
# 	(1000, '10:00am'),
# 	(1030, '10:30am'),
# 	(1100, '11:00am'),
# 	(1130, '11:30am'),
# 	(1200, '12:00pm'),
# 	(1230, '12:30pm'),
# 	(1300, '1:00pm'),
# 	(1330, '1:30pm'),
# 	(1400, '2:00pm'),
# 	(1430, '2:30pm'),
# 	(1500, '3:00pm'),
# 	(1530, '3:30pm'),
# 	(1600, '4:00pm'),
# 	(1630, '4:30pm'),
# 	(1700, '5:00pm'),
# 	(1730, '5:30pm'),
# 	(1800, '6:00pm'),
# 	(1830, '6:30pm'),
# 	(1900, '7:00pm'),
# 	(1930, '7:30pm'),
# 	(2000, '8:00pm'),
# 	(2030, '8:30pm'),
# 	(2100, '9:00pm'),
# 	(2130, '9:30pm'),
# 	(2200, '10:00pm'),
# 	(2230, '10:30pm'),
# 	(2300, '11:00pm'),
# 	(2330, '11:30pm'),
# 	(2400, '12:00am'),
# 	(2430, '12:30am'),
# 	]

class hr_contract(osv.osv):

	_inherit = 'hr.employee'
	_description = 'Employee Contract'

	def _get_wage(self, cr, uid, ids, name, args, context):
		if not ids: return {}
		res = {}
		for employee in self.browse(cr, uid, ids, context=context):
			if not employee.contract_ids:
				res[employee.id] = 0.0
				continue
			cr.execute( 'SELECT wage '\
						'FROM hr_contract '\
						'WHERE employee_id = %s ',
						 (employee.id,))
			result = dict(cr.dictfetchone())
			res[employee.id] = result['wage']
		return res


	_columns = {
		'contract_date_start': fields.date('Fecha de ingreso', required=False),
		# 'month_salary': fields.integer('Salario mensual', required=False),
		'wage': fields.function(_get_wage, type="float"  ),
		# HORARIO DE ENTRADA Y SALIDA
		# 'morning_entrance': fields.selection(hours, 'Entrada', label="False" ),
		# 'morning_exit': fields.selection(hours, 'Salida ' ),
		# 'afternoon_entrance': fields.selection(hours, 'Entrada' ),
		# 'afternoon_exit': fields.selection(hours, 'Salida' ),

	}

hr_contract()


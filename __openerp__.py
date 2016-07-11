# -*- encoding: utf-8 -*-
###########################################################################
#    Copyright (C) Helados Gilda, C.A. (<http://heladosgilda.com.ve>).
#    All Rights Reserved
###############Credits######################################################
#    Coded by: Simon Gomes xtgomes@gmail.com,
#    Audit by: Ana Iris Castro Ramírez anaguiris@hotmail.com,
#    Finance by: Helados Gilda, C.A. http://gilda.com.ve
#############################################################################
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################
{
	'name' : 'Nómina Custom',
	'version' : '0.1',
	'author' : 'Helados Gilda C.A.',
	'website' : 'http://gilda.com.ve',
	'category' : 'Human Resources',
	'description': '''
Custom module tab employee
Módulo Personalizado de ficha de empleado

hr_nominag:
	hr_employee->
		añade campo Cédula y verificado los datos con el Seniat para cargar automáticamente nombres y apellidos.
		añade campos para nombres y apellidos para tener un campo personalizado en caso de ser diferente por el dado de la pagina del seniat.
		añade campo de nombre completo, el cual concatena los 4 campos anteriormente descritos.
		añade campos de:
		Dirección particular
		Teléfono movil
		Teléfono residencial
		Correo electronico personal
		Lateralidad - se toma por defecto DIESTRO
		añade y modifica Checkbox para verificar si el empleado es supervisor o gerente
		añade filtros para ocultar campos de supervisor o gerente en caso de que el empleado sea alguno de ellos.

	hr_address_custom->
		añade dirección particular con campos: dirección código postal, ciudad, estado, país
	hr_state->
		añade estado y país

hr_nominag_contrato:
	añade fecha de ingreso del empleado y muestra salario según CONTRATO.

hr_family:
	añade campos de contacto de emergencia, parentesco y número teléfonico.
	oculta el campo original para el número de hijos
	añade campos para número de hijos
	añade campos para tallas de uniformes (pantalon, camisa, calzado)

	hr_children->
		añade campos para el modelo de hijos(nombre, apellido, edad, fecha de nacimiento, nivel educativo, guarderia)
		edad se calcula según fecha de nacimiento
	nursery->
		añade nombre del registro que toma según RIF
		añade nombre de la guarderia
		campos de RIF y codigo de registro en el ministerio de educación

hr_bank:
	deshabilita campo original de cuenta bancaria
	añade campo de cuenta bancaria

	hr_bank_account->
		campo banco conectado con el modelo original de banco
		campo número de cuenta
		campos cédula, empleado y correo electronico que trae automaticamente desde los datos del empleado
		campo de tipo de cuenta y cuenta por defecto.

hr_banco:
	exporta cuenta bancaria a nómina, y filtra por el empleado seleccionado

hr_state_data:
	introduce estados de venezuela
	
hr_level_data:
	introduce nivel educativo predeterminado

''',

	'data': [],
	'depends' : ['hr','hr_contract','l10n_ve_fiscal_requirements'],
	'update_xml': [
				'hr_nominag.xml', 
				'hr_nominag_contrato.xml',
				'hr_family.xml', 
				'hr_bank.xml', 
				'family_report.xml', 
				'hr_state_data.xml',
				'hr_level_data.xml',
				'hr_banco.xml',
								],
	'init_xml' : [ ],
	'demo_xml' : [ ],
	'installable': True,
	'active': False,
	'css': [  ],
}

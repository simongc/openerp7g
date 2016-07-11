from openerp.report import report_sxw
from openerp.report import *
import time


# This is the sample of our python file (Step3) for creating reports


class family_report(report_sxw.rml_parse):
	def __init__(self,cursor,user,name,context=None):
		super(family_report,self).__init__(cursor,user,name,context=context)
		self.localcontext.update(
			{
				'time':time,			
			}
			)

report_sxw.report_sxw('report.family.report','hr.employee','hr_nominag/report/family_report.rml',parser=family_report)


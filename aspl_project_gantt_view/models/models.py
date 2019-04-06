# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from odoo import models, api, fields, _
import datetime


class ProjectGanttView(models.Model):
    _inherit = 'project.project'

    @api.model
    def getTaskForProject(self, project_id):
        final_list = []
        linking = []
        linkid = 1
        search_domain = []
        if project_id:
            search_domain = self.search([('id','=',project_id)])
        else:
            search_domain = self.search([])
        if search_domain:
            for project in search_domain:
                project_deadline = None
                total_project_progress = total_spent_hour = total_planned_hour = 0.0
                for each in self.env['project.task'].search([('project_id', '=', project.id)]):
                    if each:
                        total_planned_hour += each.planned_hours
                        total_spent_hour += each.effective_hours
                if total_planned_hour > 0.0:
                    total_project_progress = round(100.0 * (total_spent_hour) / total_planned_hour)

                # IF PROJECT DOES NOT CONTAIN START DATE, CERATE DATE CONSIDER AS A START DATE
                if project.date_start:
                    projectdate = datetime.datetime.strptime(str(project.date_start), '%Y-%m-%d').strftime("%d-%m-%Y")
                    project_startdate = datetime.datetime.strptime(str(project.date_start), '%Y-%m-%d')
                else:
                    projectdate = datetime.datetime.strptime(str(project.create_date), '%Y-%m-%d %H:%M:%S.%f').strftime("%d-%m-%Y")
                    date_string = datetime.datetime.strftime(project.create_date, '%Y-%m-%d %H:%M:%S')
                    project_startdate = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
                if project.date:
                    project_deadline = datetime.datetime.strptime(str(project.date), '%Y-%m-%d')
                project_task = self.env['project.task'].search([('project_id', '=', project.id)])
                if project_task:
                    for task in project_task:
                        temp = {'id': task.id, 'text': task.name, 'open': "true", "progress": round(((task.progress) / 100), 2)}
                        if task.date_start:
                            temp['start'] = datetime.datetime.strptime(str(task.date_start), '%Y-%m-%d %H:%M:%S').strftime("%d-%m-%Y")
                            temp['start'] = temp['start'].split(" ")[0]  #SPLIT FOR GET DATE FROM DATE TIME
                        if task.date_deadline:
                            temp['end'] = datetime.datetime.strptime(str(task.date_deadline), '%Y-%m-%d').strftime("%d-%m-%Y")
                            temp['end'] = temp['end'].split(" ")[0]  #SPLIT FOR GET DATE FROM DATE TIME
                        #LINK ARROW TYPES
                        if task.parent_id:
                            temp['parent'] = task.parent_id.id
                            linking.append({'id': str(linkid), 'source': str(task.parent_id.id), 'target': str(task.id), 'type': '2'})
                        else:
                            temp['parent'] = project.id
                            linking.append({'id': str(linkid), 'source': str(project.id), 'target': str(task.id), 'type': '1'})
                        if task.date_start and task.date_deadline:  # date_start will always be there can be removed from condition
                            startdate = datetime.datetime.strptime(str(task.date_start), '%Y-%m-%d %H:%M:%S')
                            enddate = datetime.datetime.strptime(str(task.date_deadline), '%Y-%m-%d')
                            if not project_deadline:
                                if project_deadline < enddate:
                                    project_deadline = enddate
                                else:
                                    project_deadline = enddate
                            durationdays = (enddate - startdate).days
                            temp['start_date'] = datetime.datetime.strptime(str(task.date_start), '%Y-%m-%d %H:%M:%S').strftime(
                                "%d-%m-%Y")
                            temp['duration'] = durationdays
                        final_list.append(temp)
                        linkid = linkid + 1

                    final_list.append({'id': project.id,
                                       'text': project.name,
                                       "start_date": projectdate,
                                       "start": projectdate,
                                       "end":datetime.datetime.strptime(str(project_deadline), '%Y-%m-%d %H:%M:%S').strftime("%d-%m-%Y") if project_deadline else "",
                                       "duration": str((project_deadline - project_startdate).days) if project_deadline else "",
                                       "open": "true",
                                       "progress": str(total_project_progress / 100 if total_project_progress else 0.0)
                                       })
                else:
                    final_list.append({'id': project.id,
                                       'text': project.name,
                                       "start_date": projectdate,
                                       "start": projectdate,
                                       "end": datetime.datetime.strptime(str(project_deadline),
                                              '%Y-%m-%d %H:%M:%S').strftime("%d-%m-%Y") if project_deadline else "",
                                       "duration": str(
                                           (project_deadline - project_startdate).days) if project_deadline else "",
                                       "open": "true",
                                       "progress": str(total_project_progress / 100 if total_project_progress else 0.0)
                                       })
            if final_list:
                return [sorted(final_list, key=lambda k: k['id']), linking]

    @api.model
    def updateTask(self, taskid, name, startdate, enddate, level):
        # Splitting string to get the date
        startdate = startdate.split("T")[0]
        enddate = enddate.split("T")[0]
        startdate = datetime.datetime.strptime(startdate, '%Y-%m-%d')
        enddate = datetime.datetime.strptime(enddate, '%Y-%m-%d')

        if level == 0:
            self.env['project.project'].search([('id', '=', taskid)]).write({'date_start': startdate,
                                                                             'date': enddate})
        if level == 1:
            self.env['project.task'].search([('id', '=', taskid)]).write({'name' : name,
                                                                          'date_start' : startdate,
                                                                          'date_deadline' : enddate})
        return True

    @api.model
    def addTask(self, name, startdate, enddate, project_id, level):
        if startdate:
            startdate = datetime.datetime.strptime(startdate, '%m/%d/%Y')
            if enddate:
                enddate = datetime.datetime.strptime(enddate, '%m/%d/%Y')
            if not enddate:
                enddate = startdate
        else:
            startdate = datetime.datetime.today().strftime('%Y-%m-%d 00:00:00')
            enddate = False

        if project_id:
            if level == 1:
                task = self.env['project.task'].create({'name': name,
                                                        'date_start': startdate,
                                                        'date_deadline': enddate,
                                                        'project_id':int(project_id)})
                return {"id" : task.id}
            if level == 2:
                project_id = self.env['project.task'].browse(int(project_id))
                task = self.env['project.task'].create({'name': name,
                                                        'date_start': startdate,
                                                        'date_deadline': enddate,
                                                        'project_id': project_id.project_id.id,
                                                        'parent_id': int(project_id)})
                return {"id": task.id}
        else:
            self.env['project.project'].create({'name': name,
                                                'date_start': startdate,
                                                'date': enddate,
                                                })
            return True

    @api.model
    def update_link(self, chaild, parent):
        self.env['project.task'].search([('id', '=', int(chaild))]).write({'parent_id': int(parent)})
        return True

    @api.model
    def deleteTask(self, id, project_id):
        project = self.env['project.task'].search([('id', '=', int(id))])
        project.unlink()
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

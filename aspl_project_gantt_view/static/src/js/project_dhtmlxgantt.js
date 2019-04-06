odoo.define('aspl_project_gantt_view.project_dhtmlxgantt', function (require) {
   "use strict";
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var AbstractAction = require('web.AbstractAction');
    var Widget = require('web.Widget');
    var rpc = require('web.rpc');
    var kanbancontroller = require('web.KanbanController');
    var FormView = require('web.FormView');
    var core = require('web.core');
    var qweb = core.qweb;
    var _t = core._t;

    var ProjectForcast = AbstractAction.extend(ControlPanelMixin, {
        title: core._t('Gantt View'),
        template: 'ProjectGanttViewAction',

        init: function (parent, params) {
            this._super.apply(this, arguments);
            var self = this;
            this.action_manager = parent;
            this.params = params;
            this.task_id = false;
            var context = self.params.context;
        },

        start: function () {
            this._super.apply(this, arguments);
            this.set("title", this.title);
            this.update_control_panel({search_view_hidden: true}, {clear: true});
        },

        events: {
           'change .filter_gantt_view' : 'filterRenderGanttview',
        },

        filterRenderGanttview : function(event){
            var self = this;
            var filter_by = $(event.currentTarget).val();
            self.renderGanttview(filter_by)
        },

        renderGanttview : function(filter_by){
            var self = this;
            var url = window.location.href;;
            var project_id = false
            if(url.match('active_id') && url.match('active_id')[0]){
               project_id = parseInt(/id=(\d+)/.exec(url)[1]);
            }
            self.$el.find('#project_gantt_view').remove()
            self.$el.find('#append_project_gantt_view').append("<div id='project_gantt_view' style='width:100%; height:480px;'/>");
            var params = {
                model : 'project.project',
                method : 'getTaskForProject',
                args: [parseInt(project_id)],
            }
            rpc.query(params, {async : false}).then(function(records) {
                if(records){
                    var project_task = {"data": records[0],
                                        "links" : records[1]
                                        };
//                  ON AFTER TASK UPDATE
                    gantt.attachEvent("onaftertaskupdate", function(id, item){
                        function convert(d){
                            return d.getFullYear() + "-" + (d.getMonth()+1) + "-" + d.getDate();
                        }
                        var sd = convert(item.start_date);
                        var ed = convert(item.end_date);
                        var params = {
                        model : 'project.project',
                        method : 'updateTask',
                        args: [id, item.text, sd, ed, item.$level],
                        };
                        rpc.query(params, {async : false}).then(function(records){
                            return true;
                        });
                    });
                    var taskId = null;
                    gantt.showLightbox = function(id, item) {
                        $('#header_title').html('')
                        $('#model_title').html('')

                        if(item.parent){
                             if(item.$level == 1){
                                $('#header_title').html('Create Task')
                                $('#model_title').html('Task Name')
                                $('.activeSaveButton').attr('placeholder', 'Enter Task Name')
                            }else{
                                $('#header_title').html('Create Sub-Task')
                                $('#model_title').html('Sub-Task Name')
                                $('.activeSaveButton').attr('placeholder', 'Enter Sub-Task Name')
                            }
                        }else{
                            $('#header_title').html('Create Project')
                            $('#model_title').html('Project Name')
                            $('.activeSaveButton').attr('placeholder', 'Enter Project Name')
                        }
                        taskId = id;
                        self.task_id = taskId
                        var task = gantt.getTask(id);
                        $('#addProjectTask').modal('show');
                        var form = getForm();
                        var input = form.querySelector("[name='description']");
                        input.focus();
                        input.value = task.text;
                        form.style.display = "block";
                        form.querySelector("[name='save']").onclick = save;
                        form.querySelector("[name='close']").onclick = cancel;
                        gantt.refreshData();
                    };

                    function save() {
                        var task = gantt.getTask(taskId);
                        var text = getForm().querySelector("[name='description']").value;
                        var start = getForm().querySelector("[name='start_date']").value;
                        var end = getForm().querySelector("[name='end_date']").value;

                        var level = task.$level;
                        var params = {
                            model : 'project.project',
                            method : 'addTask',
                            args: [text, start, end, task.parent, task.$level],
                        };
                        rpc.query(params, {async : false}).then(function(records){
                           window.location.reload()
                            gantt.refreshData();
                        });
                    }
                    gantt.attachEvent("onBeforeTaskDelete", function(id, item){
                        return true;
                    });

                    function cancel(){
                        if(self.task_id){
                            gantt.deleteTask(self.task_id);
                            self.task_id = false;
                            gantt.refreshData();
                        }
//                        gantt.deleteTask(self.task_id);
//                        gantt.refreshData();
                    }

                    function remove() {
                        gantt.deleteTask(self.task_id);
                        gantt.refreshData();
                    }
                    gantt.hideLightbox = function(){
                        getForm().style.display = "";
                        taskId = null;
                    }

                    function getForm() {
                        return document.getElementById("addProjectTask");
                    };

                    //ON TASK DBL CKICK
                    gantt.attachEvent("onTaskDblClick", function(id,e){
                        //any custom logic here
                        return false;
                    });
                   //ON FILTER LINK ADD
                    gantt.attachEvent("onafterlinkadd", function(id,item){
                        var params = {
                            model : 'project.project',
                            method : 'update_link',
                            args: [item.target, item.source],
                        };
                        rpc.query(params, {async : false}).then(function(records){
                            if(records){
                                location.reload()
                            }
                        });
                    });

                   //ON AFTER TASK ADD
                    gantt.attachEvent("onaftertaskadd", function(id, item){
                        function convert(d){
                            return d.getFullYear() + "-" + (d.getMonth()+1) + "-" + d.getDate();
                        }
                        var sd = convert(item.start_date);
                        var ed = convert(item.end_date);
                        var params = {
                            model : 'project.project',
                            method : 'addTask',
                            args: [item.text, sd, ed, item.parent, item.$level],
                        };
                        rpc.query(params, {async : false}).then(function(records){
                            window.location.reload()
                            gantt.refreshData();
                        });
                    });

                    gantt.templates.task_class = function (st, end, item) {
                        return item.$level == 0 ? "gantt_project" : ""
                    };

                    if(filter_by == 'week'){
                       gantt.config.subscales = [
                            {unit:"week", step:1, date:"Week #%W"}
                       ];
                       gantt.config.scale_height = 45;
                       gantt.refreshData();
                    }
                    if(filter_by == 'year'){
                        gantt.config.scale_unit = "year";
                        gantt.config.step = 1;
                        gantt.config.date_scale = "%Y";
                        gantt.config.subscales = [
                            {unit: "month", step: 1, date: "%M"}
                        ];
                        gantt.refreshData();
                    }
                    if(filter_by === 'month'){
                        gantt.config.scale_unit = "month";
                        gantt.config.date_scale = "%F, %Y";
                        gantt.config.scale_height = 50;
                        gantt.config.subscales = [
                            {unit: "day", step: 1, date: "%j, %D"}
                        ];
                        gantt.refreshData();
                    }
                    if(filter_by === 'day'){
                        gantt.refreshData();
                        gantt.config.scale_unit = 'day';
                        gantt.config.date_scale = "%M %Y";
                        gantt.config.scale_height = 50;
                        gantt.config.subscales = [
                            {unit: "day", step: 1, date: "%d"}
                        ];
                        gantt.refreshData();
                    }

                    gantt.templates.tooltip_text = function(start,end,task){
                        var text = false;
                        if(task.$level==0){
                            text = 'Project Name : '
                        }else{
                            text = 'Task Name : '
                        }
                        return "<b>"+text+"</b>" + task.text +"<br/><b>Start date:</b> " +
                                task.start +"<br/><b>End date:</b> " +
                                task.end +"<br/><b>Duration:</b> " + task.duration;
                    };
                    gantt.config.drag_progress = false;
                    gantt.attachEvent("onBeforeParse", function(){
                        gantt.clearAll();
                    });

                    setTimeout(function(){
                        $('#project_gantt_view').dhx_gantt({
                            data: project_task
                        });
                    })
                    //gantt.config.readonly = true;
                }
            });
        },

        renderElement: function() {
            var self = this;
            this._super();
            self.renderGanttview('day')
            setTimeout(function(){
                $(function() {
                    $(".start-datepicker").datepicker({
                        onSelect: function(selected) {
                            $(".end-datepicker").datepicker("option", "minDate", selected)
                            $(".end-datepicker").removeAttr('disabled')
                        }
                    });
                    $(".end-datepicker").datepicker({
                        onSelect: function(selected) {
                           $(".start-datepicker").datepicker("option", "maxDate", selected)
                        }
                    });
                });

                $(document).on("keyup",'.activeSaveButton', function(e) {
                    var len = $(e.currentTarget).val()
                    if(len && len.length > 0){
                        $('.save_btn').removeAttr('disabled')
                    }else{
                        $('.save_btn').attr('disabled', 'disabled')
                    }
                })

                $(document).on("keyup",'.start-datepicker', function(e) {
                    var len = $(e.currentTarget).val()
                    if(len && len.length > 0){
                        $(".end-datepicker").removeAttr('disabled')
                    }else{
                        $('.end-datepicker').attr('disabled', 'disabled')
                    }
                })

                $(document).keyup(function(e) {
                    if (e.keyCode == 27) { // esc keycode
                        if(self.task_id){
                            gantt.deleteTask(self.task_id);
                            self.task_id = false;
                            gantt.refreshData();
                        }
                     }
                });
            })
        },
    });

    kanbancontroller.include({
        renderButtons: function ($node) {
            var self = this;
            this._super.apply(this, arguments);
            if(this.$buttons){
                this.$buttons.on('click', '.btn_dhtmlx_gantt_view', function () {
                    self.do_action({
                        'type': 'ir.actions.client',
                        'tag': 'project_gantt_view_action',
                        'context':{'active_id': self.initialState.context.active_id}
                    });
                });
            }
        },
    });

    core.action_registry.add('project_gantt_view_action', ProjectForcast);
    return {
        ProjectForcast: ProjectForcast,
    };
});

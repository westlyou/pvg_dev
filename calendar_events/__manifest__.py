# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

{
  "name"                 :  "Events: Calendar View",
  "summary"              :  "This module will provide a calender view for events. With a calendar view, customers can view events for a specific date. All events link to be shown in pop-up for each day.",
  "category"             :  "Marketing",
  "version"              :  "1.0.0",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://www.webkul.com/",
  "description"          :  """Events: Calendar View.""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=calendar_events&version=12.0",
  "depends"              :  [
                             'website_event',
                            ],
  "data"                 :  [
                                'views/event_on_web_template.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  15,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}

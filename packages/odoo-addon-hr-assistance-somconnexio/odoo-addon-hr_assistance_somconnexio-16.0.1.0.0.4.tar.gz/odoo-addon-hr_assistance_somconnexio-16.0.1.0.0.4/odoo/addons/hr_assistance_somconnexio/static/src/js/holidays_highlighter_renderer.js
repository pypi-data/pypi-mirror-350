/** @odoo-module **/

import { AttendeeCalendarRenderer } from "@calendar/views/attendee_calendar/attendee_calendar_renderer";
import { AttendeeCalendarCommonRenderer } from "@calendar/views/attendee_calendar/common/attendee_calendar_common_renderer";
export class HolidaysHighlighterRenderer extends AttendeeCalendarRenderer {}
export class HolidaysHighlighterCommonRenderer extends AttendeeCalendarCommonRenderer {
ex
    onDayRender(info) {
	 const date = luxon.DateTime.fromJSDate(info.date).toISODate();
         super.onDayRender(info);
         if (this.props.model.params.holiday_color) {
             document.documentElement.style.setProperty(
                     '--holiday-color',
                     this.props.model.params.holiday_color
             );
          }
          if (
              this.props.model.publicHolidays.includes(date) ||
              (this.props.model.params.weekend_enabled && [6,0].includes(info.date.getDay()))
          ) {

             info.el.classList.add("holiday");
          }
    }

}
HolidaysHighlighterRenderer.components = {
    ...AttendeeCalendarRenderer.components,
    day: HolidaysHighlighterCommonRenderer,
    month: HolidaysHighlighterCommonRenderer,
    week: HolidaysHighlighterCommonRenderer,
};

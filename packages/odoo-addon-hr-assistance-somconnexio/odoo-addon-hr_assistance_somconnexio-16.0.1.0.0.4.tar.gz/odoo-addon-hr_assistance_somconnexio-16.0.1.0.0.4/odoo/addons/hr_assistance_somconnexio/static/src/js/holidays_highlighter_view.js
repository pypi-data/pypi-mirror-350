/** @odoo-module **/

import { registry } from "@web/core/registry";
import { attendeeCalendarView } from "@calendar/views/attendee_calendar/attendee_calendar_view";
import { HolidaysHighlighterModel } from "@hr_assistance_somconnexio/js/holidays_highlighter_model";
import { HolidaysHighlighterRenderer } from "@hr_assistance_somconnexio/js/holidays_highlighter_renderer";

export const holidaysHighlighterView = {
    ...attendeeCalendarView,
    Model: HolidaysHighlighterModel,
    Renderer: HolidaysHighlighterRenderer,
};

registry.category("views").add("holidays_highlighter", holidaysHighlighterView);

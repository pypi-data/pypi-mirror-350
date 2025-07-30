/** @odoo-module **/

import { registry } from "@web/core/registry";
import { AttendeeCalendarModel } from "@calendar/views/attendee_calendar/attendee_calendar_model";

export class HolidaysHighlighterModel extends AttendeeCalendarModel {
    async updateData(data) {
        await super.updateData(data);
	data.publicHolidays = await this.loadPublicHolidays(data);
        data.params = await this.loadParams(data);
    }
    setup(params, services) {
	super.setup(params, services);
	this.data.publicHolidays = [];
	this.data.params = {}
    }
    get publicHolidays() {
        return this.data.publicHolidays;
    }
    get params() {
        return this.data.params;
    }
   //--------------------------------------------------------------------------

    /**
     * @protected
     */
    fetchPublicHolidays(data) {
        return this.orm.call('hr.holidays.public.line', "search_read", [
            [], ['date']
        ]);
    }
    /**
     * @protected
     */
    async loadPublicHolidays(data) {
        const publicHolidays = await this.fetchPublicHolidays(data);
        return publicHolidays.map(h => h.date);
    }

    //--------------------------------------------------------------------------

    /**
     * @protected
     */
    fetchHolidayColor(data) {
        return this.orm.call('ir.config_parameter', "get_param", [
             'sc_public_holiday_color'
        ]);
    }
    fetchWeekendEnabled(data) {
        return this.orm.call('ir.config_parameter', "get_param", [
            'sc_public_holiday_weekend_enabled'
        ]);
    }

    /**
     * @protected
     */
    async loadParams(data) {
        return {
            holiday_color: await this.fetchHolidayColor(data),
            weekend_enabled: await this.fetchWeekendEnabled(data),
        }
    }
    async updateData(data) {
	await super.updateData(data);
	data.publicHolidays = await this.loadPublicHolidays(data);    
        data.params = await this.loadParams(data);
    }
}


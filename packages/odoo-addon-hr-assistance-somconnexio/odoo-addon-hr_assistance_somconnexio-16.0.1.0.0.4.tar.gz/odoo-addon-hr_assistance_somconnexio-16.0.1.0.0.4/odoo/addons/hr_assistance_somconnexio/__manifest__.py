{
    "name": "HR Assistance - SomConnexio",
    "version": "16.0.1.0.0",
    "summary": """
    Expose the REST API used in Som Connexió to create and manage contracts in Odoo.
    """,
    "author": """
        Som Connexió SCCL,
        Coopdevs Treball SCCL
    """,
    "category": "Cooperative Management",
    "website": "https://git.coopdevs.org/coopdevs/som-connexio/odoo/odoo-somconnexio",
    "license": "AGPL-3",
    "depends": [
        "hr_contract",
        "hr_holidays",
        "hr_holidays_leave_auto_approve",
        "hr_holidays_public",
        "hr_timesheet",
        "hr_attendance_report_theoretical_time",
        "somconnexio",
        "calendar",
    ],
    "external_dependencies": {
        "python": [],
    },
    "data": [
        "views/hr_attendance.xml",
        "views/menus.xml",
        "views/calendar_view.xml",
        "data/hr_attendance_place.xml",
        "data/ir_config_parameter.xml",
        "security/ir.model.access.csv",
    ],
    "assets": {
        "web.assets_backend": [
            "hr_assistance_somconnexio/static/src/js/my_attendances.js",
            "hr_assistance_somconnexio/static/src/js/holidays_highlighter_model.js",
            "hr_assistance_somconnexio/static/src/js/holidays_highlighter_view.js",
            "hr_assistance_somconnexio/static/src/js/holidays_highlighter_renderer.js",
            "hr_assistance_somconnexio/static/src/css/holidays_highlighter.css",
            "hr_assistance_somconnexio/static/src/xml/attendance.xml",
        ]
    },
    "demo": [],
    "qweb": [],
    "application": False,
    "installable": True,
}

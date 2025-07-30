import base64
from odoo import _, http
from odoo.tools.pdf import merge_pdf


class UserController(http.Controller):
    @http.route(
        ["/web/binary/download_attachments"],
        auth="user",
        methods=["GET"],
        website=True,
    )
    def download_attachments(self, attachment_ids, **kw):
        attachment_ids = [int(id) for id in attachment_ids.split(",")]
        attachments = http.request.env["ir.attachment"].sudo().browse(attachment_ids)
        attachments_datas = [
            base64.b64decode(a.datas, validate=True) for a in attachments
        ]
        merged_attachments = merge_pdf(attachments_datas)
        filename = "{}.pdf".format(_("delivery_labels"))
        return http.request.make_response(
            merged_attachments,
            [
                ("Content-Type", "application/octet-stream"),
                ("Content-Disposition", http.content_disposition(filename)),
            ],
        )

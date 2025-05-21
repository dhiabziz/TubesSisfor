# -*- coding: utf-8 -*-
# from odoo import http


# class Sidebar(http.Controller):
#     @http.route('/sidebar/sidebar', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sidebar/sidebar/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sidebar.listing', {
#             'root': '/sidebar/sidebar',
#             'objects': http.request.env['sidebar.sidebar'].search([]),
#         })

#     @http.route('/sidebar/sidebar/objects/<model("sidebar.sidebar"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sidebar.object', {
#             'object': obj
#         })


# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Cat(models.Model):
    _name = 'cats.cat'
    _description = 'Deskripsi Kucing'


    name = fields.Char(string="Nama", required=True)
    color = fields.Selection(selection=[
        ('0', 'Merah'), ('1', 'Kuning'), ('2', 'Hijau'), ('3', 'Biru'), ('4', 'Ungu'), 
    ], string="Warna", required=True)
    type = fields.Many2one('cats.cat.type', string="Jenis")


class CatType(models.Model):
    _name = 'cats.cat.type'
    _description = 'Jenis Kucing'


    name = fields.Char(string="Nama")




# -*- coding: utf-8 -*-
"""
/***************************************************************************
    begin                :    13/05/19
    git sha              :    :%H$
    copyright            :    (C) 2019 by Yesid Polania
    email                :    yesidpol.3@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from .db_command_config_manager import DbCommandConfigManager
from qgis.PyQt.QtCore import QSettings


class PgCommandConfigManager(DbCommandConfigManager):

    _settings_base_path = 'QgisModelBaker/ili2pg/'

    def __init__(self, configuration):
        DbCommandConfigManager.__init__(self, configuration)

    def get_uri(self, su=False):
        uri = []

        uri += ['dbname=\'{}\''.format(self.configuration.database)]
        if su:
            uri += ['user={}'.format(self.configuration.base_configuration.super_pg_user)]
            if self.configuration.base_configuration.super_pg_password:
                uri += ['password={}'.format(self.configuration.base_configuration.super_pg_password)]
        else:
            uri += ['user={}'.format(self.configuration.dbusr)]
            if self.configuration.dbpwd:
                uri += ['password={}'.format(self.configuration.dbpwd)]
        uri += ['host={}'.format(self.configuration.dbhost)]
        if self.configuration.dbport:
            uri += ['port={}'.format(self.configuration.dbport)]

        return ' '.join(uri)

    def get_db_args(self, hide_password=False):
        db_args = list()
        db_args += ["--dbhost", self.configuration.dbhost]
        if self.configuration.dbport:
            db_args += ["--dbport", self.configuration.dbport]
        db_args += ["--dbusr", self.configuration.dbusr]
        if self.configuration.dbpwd:
            if hide_password:
                db_args += ["--dbpwd", '******']
            else:
                db_args += ["--dbpwd", self.configuration.dbpwd]
        db_args += ["--dbdatabase", self.configuration.database]
        db_args += ["--dbschema",
                    self.configuration.dbschema or self.configuration.database]
        return db_args

    def save_config_in_qsettings(self):
        settings = QSettings()
        # PostgreSQL specific options
        settings.setValue(self._settings_base_path + 'host', self.configuration.dbhost)
        settings.setValue(self._settings_base_path + 'port', self.configuration.dbport)
        settings.setValue(self._settings_base_path + 'user', self.configuration.dbusr)
        settings.setValue(self._settings_base_path + 'database', self.configuration.database)
        settings.setValue(self._settings_base_path + 'schema', self.configuration.dbschema)
        settings.setValue(self._settings_base_path + 'password', self.configuration.dbpwd)
        settings.setValue(self._settings_base_path + 'usesuperlogin', self.configuration.db_use_super_login)

    def load_config_from_qsettings(self):
        settings = QSettings()

        self.configuration.dbhost = settings.value(self._settings_base_path + 'host', 'localhost')
        self.configuration.dbport = settings.value(self._settings_base_path + 'port')
        self.configuration.dbusr = settings.value(self._settings_base_path + 'user')
        self.configuration.database = settings.value(self._settings_base_path + 'database')
        self.configuration.dbschema = settings.value(self._settings_base_path + 'schema')
        self.configuration.dbpwd = settings.value(self._settings_base_path + 'password')
        self.configuration.db_use_super_login = settings.value(
            self._settings_base_path + 'usesuperlogin', defaultValue=False, type=bool)

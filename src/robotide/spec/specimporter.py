#  Copyright 2008-2013 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import os
import shutil
import wx
from robotide.action import ActionInfo
from robotide.pluginapi import Plugin
from robotide.spec.xmlreaders import LIBRARY_XML_DIRECTORY
from robotide.utils import ET


class SpecImporterPlugin(Plugin):

    HEADER = 'Import Library Spec XML'

    def enable(self):
        self.register_action(ActionInfo('Tools', self.HEADER, self.execute_spec_import))

    def execute_spec_import(self, event):
        path = self._get_path_to_library_spec()
        if path and os.path.isfile(path):
            self._store_spec(path)
            self.model.update_namespace()

    def _get_path_to_library_spec(self):
        wildcard = ('Library Spec XML | *.xml')
        dlg = wx.FileDialog(self.frame,
                            message='Import Library Spec XML',
                            wildcard=wildcard,
                            defaultDir=self.model.default_dir,
                            style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
        else:
            path = None
        dlg.Destroy()
        return path

    def _store_spec(self, path):
        name = self._get_name_from_xml(path)
        if name:
            shutil.copy(path, os.path.join(LIBRARY_XML_DIRECTORY, name+'.xml'))
            wx.MessageBox('Library "%s" imported\nfrom "%s"' % (name, path), 'Info', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox('Could not import library from file "%s"' % path, 'Import failed', wx.OK | wx.ICON_ERROR)

    def _get_name_from_xml(self, path):
        try:
            root = ET.parse(path).getroot()
            name = root.get('name')
            return name
        except:
            return None

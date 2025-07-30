# -----------------------------------------------------------------------------
# Name:        menu.py (part of PyGMI)
#
# Author:      Patrick Cole
# E-Mail:      pcole@geoscience.org.za
#
# Copyright:   (c) 2013 Council for Geoscience
# Licence:     GPL-3.0
#
# This file is part of PyGMI
#
# PyGMI is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyGMI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------
"""Seis Menu Routines."""

from PySide6 import QtWidgets, QtGui

from pygmi.seis import del_rec
from pygmi.seis import iodefs
from pygmi.seis import beachball
from pygmi.seis import graphs
from pygmi.seis import utils


class MenuWidget():
    """
    Widget class to call the main interface.

    This widget class creates the seismology menus to be found on the main
    interface. Normal as well as context menus are defined here.

    Parameters
    ----------
    parent : pygmi.main.MainWidget, optional
        Reference to MainWidget class found in main.py. The default is None.
    """

    def __init__(self, parent=None):

        self.parent = parent
        self.parent.add_to_context('Seis')
        self.parent.add_to_context('MacroSeis')
        context_menu = self.parent.context_menu

        self.menu = QtWidgets.QMenu('Seismology')
        parent.menubar.addAction(self.menu.menuAction())

        self.action_import_seisan = QtGui.QAction('Import Seismic Data')
        self.menu.addAction(self.action_import_seisan)
        self.action_import_seisan.triggered.connect(self.import_seisan)

        self.action_import_genfps = QtGui.QAction('Import Generic FPS')
        self.menu.addAction(self.action_import_genfps)
        self.action_import_genfps.triggered.connect(self.import_genfps)

        self.menu.addSeparator()

        self.action_check_desc = QtGui.QAction('Correct SEISAN Type 3'
                                               ' Descriptions')
        self.menu.addAction(self.action_check_desc)
        self.action_check_desc.triggered.connect(self.correct_desc)

        self.action_filter_seisan = QtGui.QAction('Filter SEISAN Data')
        self.menu.addAction(self.action_filter_seisan)
        self.action_filter_seisan.triggered.connect(self.filter_seisan)

        self.menu.addSeparator()

        self.action_beachball = QtGui.QAction('Fault Plane Solutions')
        self.menu.addAction(self.action_beachball)
        self.action_beachball.triggered.connect(self.beachball)

        self.action_quarry = QtGui.QAction('Remove Quarry Events')
        self.menu.addAction(self.action_quarry)
        self.action_quarry.triggered.connect(self.quarry)

        # Context menus

        context_menu['MacroSeis'].addSeparator()

        self.action_show_iso_plots = QtGui.QAction('Show Isoseismic Plots')
        context_menu['MacroSeis'].addAction(self.action_show_iso_plots)
        self.action_show_iso_plots.triggered.connect(self.show_iso_plots)

        context_menu['Seis'].addSeparator()

        self.action_show_QC_plots = QtGui.QAction('Show QC Plots')
        context_menu['Seis'].addAction(self.action_show_QC_plots)
        self.action_show_QC_plots.triggered.connect(self.show_QC_plots)

        self.action_show_TP_plots = QtGui.QAction('Show Temporal b-value '
                                                  'Plots')
        context_menu['Seis'].addAction(self.action_show_TP_plots)
        self.action_show_TP_plots.triggered.connect(self.show_TP_plots)

        self.action_export_seisan = QtGui.QAction('Export SEISAN Data')
        context_menu['Seis'].addAction(self.action_export_seisan)
        self.action_export_seisan.triggered.connect(self.export_seisan)

        self.action_export_csv = QtGui.QAction('Export to CSV')
        context_menu['Seis'].addAction(self.action_export_csv)
        self.action_export_csv.triggered.connect(self.export_csv)

        self.action_sexport = QtGui.QAction('Export Summary to CSV, XLSX '
                                            'or SHP')
        context_menu['Seis'].addAction(self.action_sexport)
        self.action_sexport.triggered.connect(self.sexport)

    def export_seisan(self):
        """Export Seisan data."""
        self.parent.launch_context_item(iodefs.ExportSeisan)

    def export_csv(self):
        """Export Seisan data to csv."""
        self.parent.launch_context_item(iodefs.ExportCSV)

    def sexport(self):
        """Export Summary data."""
        self.parent.launch_context_item(iodefs.ExportSummary)

    def beachball(self):
        """Create Beachballs from Fault Plane Solutions."""
        self.parent.item_insert('Step', 'Fault Plane Solutions',
                                beachball.BeachBall)

    def import_seisan(self):
        """Import Seismic data."""
        self.parent.item_insert('Io', 'Import Seismic Data',
                                iodefs.ImportSeisan)

    def correct_desc(self):
        """Correct Seisan descriptions."""
        self.parent.item_insert('Step', 'Correct SEISAN Descriptions',
                                utils.CorrectDescriptions)

    def filter_seisan(self):
        """Filter Seisan."""
        self.parent.item_insert('Step', 'Filter SEISAN Data',
                                iodefs.FilterSeisan)

    def import_genfps(self):
        """Import Generic Fault Plane Solution."""
        self.parent.item_insert('Io', 'Import Generic FPS',
                                iodefs.ImportGenericFPS)

    def delete_recs(self):
        """Delete Records."""
        self.parent.item_insert('Step', 'Delete Records', del_rec.DeleteRecord)

    def quarry(self):
        """Remove quarry events."""
        self.parent.item_insert('Step', 'Remove Quarry Events', del_rec.Quarry)

    def show_QC_plots(self):
        """Show QC plots."""
        self.parent.launch_context_item(graphs.PlotQC)

    def show_iso_plots(self):
        """Show QC plots."""
        self.parent.launch_context_item(graphs.PlotIso)

    def show_TP_plots(self):
        """Show Temporal b-value plots."""
        self.parent.launch_context_item(graphs.PlotTempB)

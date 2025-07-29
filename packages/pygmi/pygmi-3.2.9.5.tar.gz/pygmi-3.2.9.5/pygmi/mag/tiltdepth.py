# -----------------------------------------------------------------------------
# Name:        tiltdepth.py (part of PyGMI)
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
"""
Tilt Depth Routine.

Based on work by EH Stettler

References
----------
Salem et al., 2007, Leading Edge, Dec,p1502-5
"""

import os
from math import pi
import numpy as np

from PySide6 import QtWidgets
from matplotlib import colormaps
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt import NavigationToolbar2QT
import matplotlib.pyplot as plt
from numba import jit
import geopandas as gpd

from pygmi.raster.cooper import vertical
from pygmi.raster.misc import lstack
from pygmi.mag.dataprep import rtp, nextpow2
from pygmi.misc import frm, BasicModule, ProgressBarText, ProgressBar


class TiltDepth(BasicModule):
    """
    Primary class for the Tilt Depth.

    Parameters
    ----------
    parent : parent, optional
        Reference to the parent routine. The default is None.

    Attributes
    ----------
    self.mmc : FigureCanvas
        main canvas containing the image
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.units = {}
        self.X = None
        self.Y = None
        self.Z = None
        self.depths = None
        self.cbar = colormaps['jet']

        self.x0 = None
        self.x1 = None
        self.x2 = None
        self.y0 = None
        self.y1 = None
        self.y2 = None

        self.figure = Figure()
        self.mmc = FigureCanvasQTAgg(self.figure)
        self.axes = self.figure.add_subplot(111)

        self.cmb_band1 = QtWidgets.QComboBox()
        self.cmb_cbar = QtWidgets.QComboBox(self)
        self.dsb_inc = QtWidgets.QDoubleSpinBox()
        self.dsb_dec = QtWidgets.QDoubleSpinBox()
        self.btn_apply = QtWidgets.QPushButton('Calculate Tilt Depth')
        self.btn_save = QtWidgets.QPushButton('Save Depths to Text File')
        self.cb_rtp = QtWidgets.QCheckBox('Perform RTP on data')
        self.pbar = ProgressBar()

        self.setupui()

    def setupui(self):
        """
        Set up UI.

        Returns
        -------
        None.

        """
        self.buttonbox.htmlfile = 'mag.dm.tiltdepth'
        self.buttonbox.buttonbox.hide()
        lbl_2 = QtWidgets.QLabel('Band to perform Tilt Depth:')
        lbl_c = QtWidgets.QLabel('Colour Bar:')
        lbl_inc = QtWidgets.QLabel('Inclination of Magnetic Field:')
        lbl_dec = QtWidgets.QLabel('Declination of Magnetic Field:')

        self.dsb_inc.setMaximum(90.0)
        self.dsb_inc.setMinimum(-90.0)
        self.dsb_inc.setValue(-67.)
        self.dsb_dec.setMaximum(360.0)
        self.dsb_dec.setMinimum(-360.0)
        self.dsb_dec.setValue(-17.)
        self.cb_rtp.setChecked(True)

        vbl_raster = QtWidgets.QVBoxLayout()
        hbl_all = QtWidgets.QHBoxLayout(self)
        vbl_right = QtWidgets.QVBoxLayout()

        mpl_toolbar = NavigationToolbar2QT(self.mmc, self)
        spacer = QtWidgets.QSpacerItem(20, 40,
                                       QtWidgets.QSizePolicy.Policy.Minimum,
                                       QtWidgets.QSizePolicy.Policy.Expanding)
        tmp = sorted(colormaps.keys())
        self.cmb_cbar.addItem('viridis')
        self.cmb_cbar.addItems(tmp)

        self.setWindowTitle('Tilt Depth Interpretation')

        vbl_raster.addWidget(lbl_2)
        vbl_raster.addWidget(self.cmb_band1)
        vbl_raster.addWidget(lbl_c)
        vbl_raster.addWidget(self.cmb_cbar)

        vbl_raster.addWidget(self.cb_rtp)
        vbl_raster.addWidget(lbl_inc)
        vbl_raster.addWidget(self.dsb_inc)
        vbl_raster.addWidget(lbl_dec)
        vbl_raster.addWidget(self.dsb_dec)
        vbl_raster.addWidget(self.btn_apply)
        vbl_raster.addWidget(self.pbar)
        vbl_raster.addItem(spacer)
        vbl_raster.addWidget(self.btn_save)
        vbl_raster.addWidget(self.buttonbox)
        vbl_right.addWidget(self.mmc)
        vbl_right.addWidget(mpl_toolbar)

        hbl_all.addLayout(vbl_raster)
        hbl_all.addLayout(vbl_right)

        self.cmb_cbar.currentIndexChanged.connect(self.change_cbar)
        self.btn_apply.clicked.connect(self.calculate)
        self.btn_save.clicked.connect(self.save_depths)
        self.cb_rtp.clicked.connect(self.rtp_choice)

    def rtp_choice(self):
        """
        Check if RTP must be done.

        Returns
        -------
        None.

        """
        if self.cb_rtp.isChecked():
            self.dsb_inc.setEnabled(True)
            self.dsb_dec.setEnabled(True)
        else:
            self.dsb_inc.setEnabled(False)
            self.dsb_dec.setEnabled(False)

    def save_depths(self):
        """
        Save depths.

        Returns
        -------
        bool
            True if successful, False otherwise.

        """
        if self.depths is None:
            return False

        ext = 'Text File (*.csv)'

        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self.parent,
                                                            'Save File',
                                                            '.', ext)
        if filename == '':
            return False

        os.chdir(os.path.dirname(filename))
        self.depths.to_csv(filename, index=False)

        QtWidgets.QMessageBox.information(self.parent, 'Information',
                                          'Save completed!')

        return True

    def change_cbar(self):
        """
        Change the colour map for the colour bar.

        Returns
        -------
        None.

        """
        if 'Vector' not in self.outdata:
            return

        gdf = self.outdata['Vector'][0]
        zout = self.indata['Raster'][0]
        txt = str(self.cmb_cbar.currentText())

        self.figure.clear()
        self.axes = self.figure.add_subplot(111)

        cmap = colormaps[txt]

        vmin = zout.data.mean() - 2.5 * zout.data.std()
        vmax = zout.data.mean() + 2.5 * zout.data.std()

        self.axes.imshow(zout.data, extent=zout.extent, cmap='gray',
                         interpolation='nearest', vmin=vmin, vmax=vmax)

        cmap = colormaps.get_cmap(txt)
        cmap2 = np.array([cmap(i) for i in range(cmap.N)])
        low = int(cmap.N * (45 / 180))
        high = int(cmap.N * (135 / 180))
        cmap2[low:high] = cmap2[int(cmap.N / 2)]

        ims = self.axes.scatter(gdf['x'], gdf['y'], c=gdf['depth'], cmap=cmap)

        self.axes.xaxis.set_major_formatter(frm)
        self.axes.yaxis.set_major_formatter(frm)

        self.figure.colorbar(ims, format=frm, label='Depth (m)')

        self.figure.tight_layout()

        self.figure.canvas.draw()

    def calculate(self):
        """
        Routine which occurs when apply button is pressed.

        Returns
        -------
        None.

        """
        txt = str(self.cmb_band1.currentText())

        self.btn_apply.setText('Calculating...')
        self.btn_apply.setEnabled(False)

        for i in self.indata['Raster']:
            if i.dataid == txt:
                dat = i
                break

        if self.cb_rtp.isChecked():
            inc = self.dsb_inc.value()
            dec = self.dsb_dec.value()
        else:
            inc = None
            dec = None

        self.depths = tiltdepth(dat, inc, dec, self.pbar)
        self.outdata['Vector'] = [self.depths]
        self.change_cbar()

        self.btn_apply.setEnabled(True)
        self.btn_apply.setText('Calculate Tilt Depth')

    def settings(self, nodialog=False):
        """
        Entry point into item.

        Parameters
        ----------
        nodialog : bool, optional
            Run settings without a dialog. The default is False.

        Returns
        -------
        bool
            True if successful, False otherwise.

        """
        if 'Raster' not in self.indata:
            self.showlog('No Raster Data.')
            return False

        self.indata['Raster'] = lstack(self.indata['Raster'])

        data = self.indata['Raster']
        blist = []
        for i in data:
            blist.append(i.dataid)

        self.cmb_band1.clear()
        self.cmb_band1.addItems(blist)

        if not nodialog:
            tmp = self.exec()
        else:
            tmp = 1

        if tmp != 1:
            return False

        return True

    def saveproj(self):
        """
        Save project data from class.

        Returns
        -------
        None.

        """
        self.saveobj(self.cmb_band1)
        self.saveobj(self.cmb_cbar)
        self.saveobj(self.dsb_inc)
        self.saveobj(self.dsb_dec)


def tiltdepth(data, inc=None, dec=None, pbar=None):
    """
    Calculate tilt depth.

    Output is stored in self.outdata.

    Parameters
    ----------
    data : pygmi.raster.datatypes.Data
        PyGMI raster dataset.

    Returns
    -------
    None.

    """
    if pbar is None:
        pbar = ProgressBarText()

    pbar.setValue(0)
    pbar.setMaximum(4)

    # RTP
    if inc is not None and dec is not None:
        zout = rtp(data, inc, dec)
    else:
        zout = data

    # Tilt
    pbar.setValue(1)

    nr, nc = zout.data.shape
    dy, dx = np.gradient(zout.data)
    dxtot = np.ma.sqrt(dx**2 + dy**2)

    nmax = np.max([nr, nc])
    npts = int(2**nextpow2(nmax))
    dz = vertical(zout.data, npts, 1)

    t1 = np.arctan(dz / dxtot)

    pbar.setValue(2)
    # A negative number implies we are straddling 0

    # Contour tilt
    x = zout.extent[0] + np.arange(nc) * zout.xdim + zout.xdim / 2
    y = zout.extent[-1] - np.arange(nr) * zout.ydim - zout.ydim / 2

    X, Y = np.meshgrid(x, y)
    Z = np.rad2deg(t1)

    cnt0 = plt.contour(X, Y, Z, [0])
    cnt45 = plt.contour(X, Y, Z, [45], alpha=0)
    cntm45 = plt.contour(X, Y, Z, [-45], alpha=0)

    pbar.setValue(3)

    gx0, gy0, cgrad0, cntid0 = vgrad(cnt0)
    gx45, gy45, _, _ = vgrad(cnt45)
    gxm45, gym45, _, _ = vgrad(cntm45)

    g0 = np.transpose([gx0, gy0])

    pbar.setValue(4)

    dmin1 = []
    dmin2 = []

    for i, j in pbar.iter(g0):
        dmin1.append(distpc(gx45, gy45, i, j, 0))
        dmin2.append(distpc(gxm45, gym45, i, j, 0))

    dx1 = gx45[dmin1] - gx0
    dy1 = gy45[dmin1] - gy0

    dx2 = gxm45[dmin2] - gx0
    dy2 = gym45[dmin2] - gy0

    grad = np.arctan2(dy1, dx1) * 180 / pi
    grad[grad > 90] -= 180
    grad[grad < -90] += 180
    gtmp1 = np.abs(90 - np.abs(grad - cgrad0))

    grad = np.arctan2(dy2, dx2) * 180 / pi
    grad[grad > 90] -= 180
    grad[grad < -90] += 180
    gtmp2 = np.abs(90 - np.abs(grad - cgrad0))

    gtmp = np.logical_and(gtmp1 <= 10, gtmp2 <= 10)

    gx0 = gx0[gtmp]
    gy0 = gy0[gtmp]
    cntid0 = cntid0[gtmp]
    dx1 = dx1[gtmp]
    dy1 = dy1[gtmp]
    dx2 = dx2[gtmp]
    dy2 = dy2[gtmp]

    dist1 = np.sqrt(dx1**2 + dy1**2)
    dist2 = np.sqrt(dx2**2 + dy2**2)

    dist = np.min([dist1, dist2], 0)

    tmp = {'x': gx0, 'y': gy0, 'id': cntid0.astype(int), 'depth': dist}

    gdf = gpd.GeoDataFrame(tmp, geometry=gpd.points_from_xy(gx0, gy0))

    return gdf


@jit(nopython=True)
def distpc(dx, dy, dx0, dy0, dcnt):
    """
    Find closest distances.

    Parameters
    ----------
    dx : numpy array
        X array.
    dy : numpy array
        Y array.
    dx0 : float
        X point to measure distance from.
    dy0 : float
        Y point to measure distance from.
    dcnt : int
        Starting index to measure distance from.

    Returns
    -------
    dcnt : int
        Index of closest distance found in x and y arrays.

    """
    num = dx.size
    dmin = (dx0 - dx[dcnt])**2 + (dy0 - dy[dcnt])**2

    for i in range(num):
        dist = (dx0 - dx[i])**2 + (dy0 - dy[i])**2
        if dmin > dist:
            dcnt = i
            dmin = dist

    return dcnt


def vgrad(cnt):
    """
    Get contour gradients at vertices.

    Parameters
    ----------
    cnt : axes.contour
        Output from Matplotlib's axes.contour.

    Returns
    -------
    gx : numpy array
        X gradients.
    gy : numpy array
        Y gradients.
    cgrad : numpy array
        Contour gradient.
    cntid : numpy array
        Contour index.

    """
    gx = []
    gy = []
    dx2 = []
    dy2 = []
    cntid = []

    n = 0
    for path in cnt.get_paths():

        cntv = path.vertices
        cntc = path.codes
        cnt2 = np.split(cntv, np.where(cntc == 1)[0][1:])
        for cntvert in cnt2:
            n += 1

            dx = np.diff(cntvert[:, 0])
            dy = np.diff(cntvert[:, 1])

            cntid.extend([n] * dx.size)

            gx.extend((cntvert[:, 0][:-1] + dx / 2).tolist())
            gy.extend((cntvert[:, 1][:-1] + dy / 2).tolist())
            dx2.extend(dx)
            dy2.extend(dy)

    cgrad = np.arctan2(dy2, dx2)
    cgrad = np.rad2deg(cgrad)
    cgrad[cgrad > 90] -= 180.
    cgrad[cgrad < -90] += 180.

    return np.array(gx), np.array(gy), cgrad, np.array(cntid)


def _testfn():
    """RTP testing routine."""
    import sys
    from pygmi.raster.iodefs import get_raster

    ifile = r"D:\Workdata\PyGMI Test Data\Magnetics\tilt\tilt.tif"

    dat = get_raster(ifile)

    _ = QtWidgets.QApplication(sys.argv)

    tmp1 = TiltDepth()
    tmp1.indata['Raster'] = dat
    tmp1.cb_rtp.setChecked(False)
    tmp1.dsb_inc.setValue(-63.)
    tmp1.dsb_dec.setValue(-16.)

    tmp1.settings()

    dat = tmp1.outdata


if __name__ == "__main__":
    _testfn()

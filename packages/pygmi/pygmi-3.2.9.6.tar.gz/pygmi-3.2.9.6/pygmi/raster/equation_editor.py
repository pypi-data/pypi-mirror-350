# -----------------------------------------------------------------------------
# Name:        equation_editor.py (part of PyGMI)
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
"""Equation editor."""

from PySide6 import QtWidgets, QtGui
import numpy as np
import numexpr as ne

from pygmi.misc import BasicModule
from pygmi.raster.misc import lstack


class EquationEditor(BasicModule):
    """
    Equation Editor.

    This class allows the input of equations using raster datasets as
    variables. This is commonly done in remote sensing applications, where
    there is a requirement for band ratioing etc. It uses the numexpr library.

    Parameters
    ----------
    parent : parent, optional
        Reference to the parent routine. The default is None.

    Attributes
    ----------
    equation : str
        string with the equation in it
    bands : dictionary
        dictionary of bands
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.equation = None
        self.bands = {}

        self.cmb_1 = QtWidgets.QComboBox()

        self.textbrowser = QtWidgets.QTextEdit()
        self.textbrowser2 = QtWidgets.QTextBrowser()
        self.lbl_bands = QtWidgets.QLabel(': iall')
        self.cmb_dtype = QtWidgets.QComboBox()

        self.setupui()

    def setupui(self):
        """
        Set up UI.

        Returns
        -------
        None.

        """
        gl_1 = QtWidgets.QGridLayout(self)

        lbl_1 = QtWidgets.QLabel('Data Band Key:')
        lbl_2 = QtWidgets.QLabel('Output Equation:')
        lbl_3 = QtWidgets.QLabel('Output Data Type:')
        self.cmb_dtype.addItems(['auto', 'uint8', 'int16', 'int32',
                                 'float32', 'float64'])
        self.buttonbox.htmlfile = 'raster.dm.equationeditor'

        self.textbrowser.setEnabled(True)
        self.resize(600, 480)

        ptmp = self.textbrowser2.palette()

        ptmp.setColor(ptmp.ColorGroup.Active,
                      ptmp.ColorRole.Base,
                      ptmp.color(QtGui.QPalette.ColorRole.Window))
        ptmp.setColor(ptmp.ColorGroup.Disabled,
                      ptmp.ColorRole.Base,
                      ptmp.color(QtGui.QPalette.ColorRole.Window))
        ptmp.setColor(ptmp.ColorGroup.Inactive,
                      ptmp.ColorRole.Base,
                      ptmp.color(QtGui.QPalette.ColorRole.Window))

        self.textbrowser2.setPalette(ptmp)
        self.textbrowser2.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

        self.setWindowTitle('Equation Editor')
        self.textbrowser.setText('iall')
        tmp = ('<h1>Instructions:</h1>'
               '<p>Equation editor uses the numexpr library. Use the variables'
               ' iall, i1, i2 etc in formulas. The combobox above shows which '
               'band is assigned to each variable.</p>'
               '<h2>Examples</h2>'
               '<p>Sum:</p>'
               '<pre>    i1 + 1000</pre>'
               '<p>Mean (can be any number of arguments):</p>'
               '<pre>    mean(i0, i1, i2) or mean(iall)</pre>'
               '<p>Standard Deviation (can be any number of arguments):</p>'
               '<pre>    std(i0, i1, i2) or std(iall)</pre>'
               '<p>Mosaic two bands into one:</p>'
               '<pre>    mosaic(i0, i1)</pre>'
               '<p>Threshold between values 1 and 98, substituting -999 as a '
               'value:</p>'
               '<pre>    where((i1 &gt; 1) &amp; (i1 &lt; 98) , i1, -999)'
               '</pre>'
               '<p>Replacing the value 0 with a nodata or null value:</p>'
               '<pre>    where(iall!=0, iall, nodata)</pre>'
               '<h2>Commands</h2>'
               '<ul>'
               ' <li> Logical operators: &amp;, |, ~</li>'
               ' <li> Comparison operators: &lt;, &lt;=, ==, !=, &gt;=, &gt;'
               '</li>'
               ' <li> Arithmetic operators: +, -, *, /, **, %, <<, >></li>'
               ' <li> where(bool, number1, number2) : number1 if the bool '
               'condition is true, number2 otherwise.</li>'
               ' <li> sin, cos, tan, arcsin, arccos, arctan, '
               'sinh, cosh, tanh, arctan2, arcsinh, arccosh, arctanh</li>'
               ' <li> log, log10, log1p, exp, expm1</li>'
               ' <li> sqrt, abs</li>'
               ' <li> nodata or null value of first band: nodata</li>'
               '</ul>')
        self.textbrowser2.setHtml(tmp)

        gl_1.addWidget(lbl_2, 0, 0, 1, 1)
        gl_1.addWidget(self.textbrowser, 1, 0, 1, 2)
        gl_1.addWidget(lbl_1, 3, 0, 1, 1)
        gl_1.addWidget(self.cmb_1, 4, 0, 1, 1)
        gl_1.addWidget(self.lbl_bands, 4, 1, 1, 1)
        gl_1.addWidget(self.cmb_dtype, 6, 0, 1, 1)
        gl_1.addWidget(lbl_3, 5, 0, 1, 1)
        gl_1.addWidget(self.textbrowser2, 7, 0, 1, 2)
        gl_1.addWidget(self.buttonbox, 8, 0, 1, 2)

        self.cmb_1.currentIndexChanged.connect(self.combo)

    def combo(self):
        """
        Update combo information.

        Returns
        -------
        None.

        """
        txt = self.cmb_1.currentText()
        if txt != '':
            self.lbl_bands.setText(': ' + self.bands[txt])

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
        self.bands = {}
        self.bands['all data'] = 'iall'

        self.cmb_1.clear()
        self.cmb_1.addItem('all data')

        if 'Cluster' in self.indata:
            intype = 'Cluster'
        elif 'Raster' in self.indata:
            intype = 'Raster'
        else:
            self.showlog('No raster data.')
            return False

        indata = self.indata[intype]

        for j, i in enumerate(indata):
            self.cmb_1.addItem(i.dataid)
            self.bands[i.dataid] = 'i' + str(j)

        if not nodialog:
            temp = self.exec()

            if temp == 0:
                return False

            self.equation = self.textbrowser.toPlainText()

        if self.equation == '':
            self.showlog('Error: You need to enter an equation.')
            return False

        dtype = self.cmb_dtype.currentText()

        outdata = eqedit(indata, self.equation, dtype, self.showlog)

        self.outdata[intype] = outdata

        return True

    def saveproj(self):
        """
        Save project data from class.

        Returns
        -------
        None.

        """
        self.saveobj(self.equation)
        self.saveobj(self.textbrowser)


def eqedit(data, equation, dtype='auto', showlog=print):
    """
    Use equations on raster data.

    Parameters
    ----------
    data : list
        List of PyGMI raster data.
    equation : str
        Equation to compute.
    dtype : str, optional
        The data type of the output dataset. The default is 'auto'.
    showlog : function, optional
        Show information using a function. The default is print.

    Returns
    -------
    list
        List of PyGMI raster data.

    """
    localdict = {}
    bandsall = []
    indata = lstack(data)

    for j, i in enumerate(indata):
        # self.bands[i.dataid] = 'i' + str(j)
        bandsall.append(i.data)
        localdict['i' + str(j)] = i.data

    localdict_list = list(localdict.keys())
    localdict['iall'] = np.ma.array(bandsall)

    if equation == '':
        return None

    if 'iall' in equation:
        usedbands = localdict_list
    else:
        usedbands = []
        for i in localdict_list:
            if i in equation:
                usedbands.append(i)

    mask = None
    for i in usedbands:
        if mask is None:
            mask = localdict[i].mask
        else:
            mask = np.logical_or(mask, localdict[i].mask)

    neweq = eq_fix(indata, equation, showlog)

    if 'mosaic' in neweq:
        findat = mosaic(neweq, localdict)
        mask = findat.mask
    elif 'mean' in neweq:
        findat = mean(neweq, localdict)
        mask = findat.mask
    elif 'std' in neweq:
        findat = std(neweq, localdict)
        mask = findat.mask
    else:
        try:
            findat = ne.evaluate(neweq, localdict)
        except Exception:
            findat = None

    if findat is None:
        showlog('Error: Nothing processed! '
                'Your equation most likely had an error.')
        return False

    outdata = []

    if np.size(findat) == 1:
        showlog('Warning: Nothing processed! Your equation outputs a single '
                'value instead of a minimum of one band.')
        return False
    if findat.ndim == 2:
        findat.shape = (1, findat.shape[0], findat.shape[1])

    for i, findati in enumerate(findat):
        findati = findati.astype(indata[i].data.dtype)
        findati[mask] = indata[i].nodata

        outdata.append(indata[i].copy())
        outdata[-1].data = np.ma.masked_equal(findati,
                                              indata[i].nodata)
        outdata[-1].nodata = indata[i].nodata

    # This is needed to get rid of bad, unmasked values etc.
    for i, outdatai in enumerate(outdata):
        outdatai.data.set_fill_value(indata[i].nodata)
        outdatai.data = np.ma.fix_invalid(outdatai.data)
        if dtype != 'auto':
            outdatai.data = outdatai.data.astype(dtype)

    if len(outdata) == 1:
        outdata[0].dataid = equation

    return outdata


def eq_fix(indata, equation, showlog=print):
    """
    Corrects names in equation to variable names.

    Parameters
    ----------
    indata : list of PyGMI Data.
        PyGMI raster dataset.
    equation : str
        Equation to fix.
    showlog : function, optional
        Show information using a function. The default is print.

    Returns
    -------
    neweq : str
        Corrected equation.

    """
    neweq = str(equation)
    neweq = neweq.replace('ln', 'log')
    neweq = neweq.replace('^', '**')
    neweq = neweq.replace('nodata', str(indata[0].nodata))

    if 'log' in neweq:
        showlog('Warning, if you have invalid log values, they will '
                'be masked out.')

    if 'sqrt' in neweq:
        showlog('Warning, if you have invalid sqrt values, they will '
                'be masked out.')

    neweq = neweq.strip()

    return neweq


def hmode(data):
    """
    Use a histogram to generate a fast mode estimate.

    Parameters
    ----------
    data : list
        list of values to generate the mode from.

    Returns
    -------
    mode2 : float
        mode value.
    """
    mmin = np.min(data)
    mmax = np.max(data)
    for _ in range(2):
        mhist = np.histogram(data, 255, range=(mmin, mmax))
        mtmp = mhist[0].tolist()
        mind = mtmp.index(max(mtmp))
        mmin = mhist[1][mind]
        mmax = mhist[1][mind + 1]

    mode2 = (mmax - mmin) / 2 + mmin

    return mode2


def mosaic(eq, localdict):
    """
    Mosaics data into a single band dataset.

    Parameters
    ----------
    eq : str
        Equation with mosaic command.
    localdict : dictionary
        Dictionary of data.

    Returns
    -------
    findat : numpy array
        Output array.

    """
    idx = eq.index('mosaic(') + 7
    eq2 = eq[idx:]
    idx = eq2.index(')')
    eq2 = eq2[:idx]
    eq2 = eq2.replace(' ', '')
    eq3 = eq2.split(',')

    localdict_list = list(localdict.keys())

    # Check for problems
    if 'iall' in eq:
        return None

    if len(eq3) < 2:
        return None

    eq4 = []
    mask = []
    for i in eq3:
        usedbands = []
        for j in localdict_list:
            if j in i:
                usedbands.append(j)
        mask1 = None
        for j in usedbands:
            if mask1 is None:
                mask1 = localdict[j].mask
            else:
                mask1 = np.logical_or(mask1, localdict[j].mask)

        mask.append(mask1)
        try:
            eq4.append(ne.evaluate(i, localdict))
        except Exception:
            return None
        eq4[-1] = np.ma.array(eq4[-1], mask=mask[-1])

    master = eq4.pop()
    for i in eq4[::-1]:
        master[~i.mask] = i.data[~i.mask]

    return master


def mean(eq, localdict):
    """
    Get mean pixel value of all input bands.

    Parameters
    ----------
    eq : str
        Equation with std command.
    localdict : dictionary
        Dictionary of data.

    Returns
    -------
    findat : numpy array
        Output array.

    """
    idx = eq.index('mean(') + 5
    eq2 = eq[idx:]
    idx = eq2.index(')')
    eq2 = eq2[:idx]
    eq2 = eq2.replace(' ', '')
    eq3 = eq2.split(',')

    stack = []
    mask = None
    for i in localdict:
        if i not in eq3:
            continue
        if mask is None:
            mask = localdict[i].mask
        else:
            mask = np.logical_and(mask, localdict[i].mask)

        if i == 'iall':
            stack.append(localdict[i])
        else:
            stack.append([localdict[i]])

    stack = np.ma.vstack(stack)
    findat = np.ma.mean(stack, 0)
    findat.mask = mask

    return findat


def std(eq, localdict):
    """
    Get standard deviation pixel value of all input bands.

    Parameters
    ----------
    eq : str
        Equation with std command.
    localdict : dictionary
        Dictionary of data.

    Returns
    -------
    findat : numpy array
        Output array.

    """
    idx = eq.index('std(') + 4
    eq2 = eq[idx:]
    idx = eq2.index(')')
    eq2 = eq2[:idx]
    eq2 = eq2.replace(' ', '')
    eq3 = eq2.split(',')

    stack = []
    mask = None
    for i in localdict:
        if i not in eq3:
            continue
        if mask is None:
            mask = localdict[i].mask
        else:
            mask = np.logical_and(mask, localdict[i].mask)

        if i == 'iall':
            stack.append(localdict[i])
        else:
            stack.append([localdict[i]])

    stack = np.ma.vstack(stack)
    findat = np.ma.std(stack, 0)
    findat.mask = mask

    return findat


def _test():
    """Test."""
    import sys
    import matplotlib.pyplot as plt
    from pygmi.raster.iodefs import get_raster
    print('Starting')

    ifile = r"C:\Workdata\testdata.hdr"

    dat = get_raster(ifile)

    _ = QtWidgets.QApplication(sys.argv)

    EE = EquationEditor()
    EE.indata['Raster'] = dat

    EE.settings()

    out = EE.outdata['Raster']

    plt.figure(dpi=300)
    plt.imshow(out[0].data)
    plt.show()


if __name__ == "__main__":
    _test()

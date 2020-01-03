
"""

Base object for maintaining a groundwater series

T.J. de Meij juni 2019

""" 

import os
import os.path
from collections import OrderedDict

import matplotlib as mpl
import matplotlib.pyplot as plt

from pandas import Series, DataFrame
import pandas as pd
import numpy as np

from ..read.dinogws import DinoGws


class GwSeries():
    """ Init signature: aq.GwSeries(heads=None,ppt=None,srname=None)

        Groundwater series container for groundwater level measurements and piezometer metadata.
        Stores and serves measurements in several units (mwelltop,mref,msurface)
    """

    def __repr__(self):
        #return (f'{self.__class__.__name__}(n={len(self._heads)})')
        return (f'{self.name()} (n={len(self._heads)})')

    locprops_cols = ['locname','filname','alias','east','north','height_datum','grid_reference']
    tubeprops_cols = ['startdate','mp','filtop','filbot','surfdate','surface']

    def __init__(self,heads=None,locprops=None,tubeprops=None):

        if locprops is None:
            self._locprops = Series(index=self.locprops_cols)
        elif isinstance(locprops,pd.Series):
            self._locprops = locprops
        else:
            raise TypeError(f'locprops is not a pandas Series but {type(locprops)}')


        if tubeprops is None:
            self._tubeprops = DataFrame(columns=self.tubeprops_cols)
        elif isinstance(tubeprops,pd.DataFrame):
            ##if tubeprops.empty:
            ##    self._tubeprops = DataFrame(data=[[np.nan]*len(self.tubeprops_cols)],columns=self.tubeprops_cols)
            ##    self._tubeprops.at[0,'startdate'] = heads.index[0]
            ##else:
            self._tubeprops = tubeprops
        else:
            #self._tubeprops = tubeprops
            raise TypeError(f'tubeprops is not a pandas DataFrame but {type(tubeprops)}')

        if heads is None: 
            self._heads = pd.Series()
            self._heads.index.name = 'datetime'
            self._heads.name = 'dummyname'
        elif isinstance(heads,pd.Series):
            self._heads = heads.copy()
            self._heads.index.name = 'datetime'
            self._heads.name = self.name()
        else:
            raise TypeError(f'heads is not a pandas Series but {type(heads)}')

    @classmethod
    def from_dinogws(cls,filepath):
        """ 
        read tno dinoloket csvfile with groundwater measurements and return data as gwseries object

        parameters
        ----------
        filepath : str


        returns
        -------
        result : GwSeries

        """

        # read dinofile to DinoGws object
        dn = DinoGws(filepath=filepath)

        # get location metadata
        locprops = Series(index=cls.locprops_cols)
        locprops['locname'] = dn.header().at[0,'nitgcode']
        locprops['filname'] = dn.header().at[0,'filter']
        locprops['east'] = dn.header().at[0,'xcoor']
        locprops['north'] = dn.header().at[0,'ycoor']
        locprops['alias'] = dn.header().at[0,'tnocode']
        locprops['grid_reference'] = 'RD'
        locprops['height_datum'] = 'mNAP'
        locprops = Series(locprops)

        # get piezometer metadata
        tubeprops = dn.header()
        coldict = {
            'mvcmnap':'surface',
            'mvdatum':'surfdate',
            'startdatum':'startdate',
            'einddatum':'enddate',
            'mpcmnap':'mp',
            'filtopcmnap':'filtop',
            'filbotcmnap':'filbot',
            }
        tubeprops = tubeprops.rename(index=str, columns=coldict)
        tubeprops = tubeprops[cls.tubeprops_cols]
        for col in ['mp','surface','filtop','filbot']:
                tubeprops[col] = pd.to_numeric(tubeprops[col],errors='coerce')/100.

        # get head measurements
        sr = dn.series(units="cmmp")/100.
        
        return cls(heads=sr,locprops=locprops,tubeprops=tubeprops)

    def name(self):
        """ Return groundwater series name """
        return self._locprops['locname']+'_'+self._locprops['filname']

    def heads(self,ref='datum'):
        """ 
        Return groundwater head measurements

        parameters
        ----------
        ref : {'mp','datum','surface'}, default 'datum'

        returns
        -------
        result : pandas time Series

        """

        if ref=='mp':
            heads = self._heads
        elif ref in ['datum','surface']:
            heads = self._heads
            for index,props in self._tubeprops.iterrows():
                mask = heads.index>=props['startdate']
                if ref=='datum':
                    heads = heads.mask(mask,props['mp']-self._heads)
                elif ref=='surface':
                    surfref = round(props['mp']-props['surface'],2)
                    heads = heads.mask(mask,self._heads-surfref)
        else:
            raise ValueError('%s is not a valid reference point name' %ref)
        return heads

    def to_csv(self,dirpath=None):
        """Export groundwater series and metadata to csv file

        parameters
        ----------
        dirpath : export directory

        """
        filepath = dirpath+self.name()+'_0.csv'
        self._heads.to_csv(filepath,index=True,index_label='datetime',header=['head'])

        filepath = dirpath+self.name()+'_1.csv'
        self._tubeprops.to_csv(filepath,index=False,header=True)

        filepath = dirpath+self.name()+'_2.csv'
        self._locprops.to_csv(filepath,index=True,header=False)

    @classmethod
    def from_csv(cls,filepath=None):
        """Import groundwater series and metadata from csv file

        parameters
        ----------
        filepath : filename of csv file with groundwater heads

        """
        _heads = pd.read_csv(filepath,header=0,index_col=0,squeeze=True)
        _heads.index = pd.to_datetime(_heads.index)


        filepath = filepath[:-6]+'_1.csv'
        #print(filepath)
        _tubeprops = pd.read_csv(filepath,header=0)

        filepath = filepath[:-6]+'_2.csv'
        #print(filepath)
        _locprops = pd.read_csv(filepath,header=None,index_col=0,squeeze=True)

        return cls(heads=_heads,locprops=_locprops,tubeprops=_tubeprops)



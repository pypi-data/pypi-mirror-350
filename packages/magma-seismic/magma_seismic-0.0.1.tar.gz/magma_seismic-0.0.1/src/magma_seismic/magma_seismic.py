import os
from datetime import datetime


class MagmaSeismic:
    structures = ['idds', 'sds']

    def __init__(self, station: str, channel: str, channel_type: str = 'D',
                 network: str = 'VG', location: str = '00', verbose: bool = False):

        self.station = station
        self.channel = channel
        self.network = network
        self.location = location
        self.channel_type = channel_type

        self.nslc = f'{network}.{station}.{location}.{channel}'
        self.sncl = f'{station}.{network}.{channel}.{location}'
        self.verbose = verbose

    def __str__(self):
        return f'{self.station} {self.channel} {self.channel_type} {self.network} {self.location}'

    def __repr__(self):
        return f'MagmaSeismic({self.station} {self.channel} {self.channel_type} {self.network} {self.location})'

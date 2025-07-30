"""
Enums for the Enemera API client.

This module defines enumerations used throughout the client library for
representing market types, areas, and other categorical data in a type-safe way.
"""

from enum import Enum


class Purpose(Enum):
    """Enum for exchange volume purpose.

    Used to distinguish between buy and sell purposes in exchange volume data.
    """
    SELL = "SELL"  # Sell purpose in the market
    BUY = "BUY"  # Buy purpose in the market

    def __str__(self):
        """Return the string representation of the enum value."""
        return self.value


class Market(Enum):
    """Enum for Italian energy market identifiers.

    Represents the different electricity markets in Italy's power exchange system
    including day-ahead, intraday, and ancillary services markets.
    """
    MGP = "MGP"  # Day-Ahead Market (Mercato del Giorno Prima)
    MI1 = "MI1"  # Intraday Market 1 (Mercato Infragiornaliero 1)
    MI2 = "MI2"  # Intraday Market 2 (Mercato Infragiornaliero 2)
    MI3 = "MI3"  # Intraday Market 3 (Mercato Infragiornaliero 3)
    MI4 = "MI4"  # Intraday Market 4 (Mercato Infragiornaliero 4)
    MI5 = "MI5"  # Intraday Market 5 (Mercato Infragiornaliero 5)
    MI6 = "MI6"  # Intraday Market 6 (Mercato Infragiornaliero 6)
    MI7 = "MI7"  # Intraday Market 7 (Mercato Infragiornaliero 7)
    # Ancillary Services Market (Mercato per il Servizio di Dispacciamento)
    MSD = "MSD"
    MB = "MB"  # Balancing Market (Mercato del Bilanciamento)
    MBa = "MBa"  # Balancing Market - altri servizi (other services)
    MBs = "MBs"  # Balancing Market - secondary reserve

    def __str__(self):
        return self.value


class Area(Enum):
    """Enum for Italian bidding zones and macrozones.

    Represents the geographical bidding zones in the Italian electricity market
    as well as macrozones used for imbalance pricing and other calculations.
    """
    # Standard bidding zones
    NORD = "NORD"  # North zone (Northern Italy)
    CNOR = "CNOR"  # Center-North zone (Central-Northern Italy)
    CSUD = "CSUD"  # Center-South zone (Central-Southern Italy)
    SUD = "SUD"  # South zone (Southern Italy)
    SICI = "SICI"  # Sicily zone
    SARD = "SARD"  # Sardinia zone
    CALA = "CALA"  # Calabria zone

    # Macro zones (used for imbalance pricing)
    NORTH = "NORD"  # North macrozone (alias for NORD)
    # South macrozone (includes SUD, CSUD, CNOR, SICI, SARD, CALA)
    SOUTH = "SUD"

    # Virtual zones
    BRNN = "BRNN"  # Brindisi
    FOGN = "FOGN"  # Foggia
    MONT = "MONT"  # Montalto
    PRGP = "PRGP"  # Priolo Gargallo
    ROSN = "ROSN"  # Rossano

    # Foreign virtual zones
    AUST = "AUST"  # Austria
    CORS = "CORS"  # Corsica
    COAC = "COAC"  # Corsica AC
    COAD = "COAD"  # Corsica DC
    FRAN = "FRAN"  # France
    GREC = "GREC"  # Greece
    SLOV = "SLOV"  # Slovenia
    SVIZ = "SVIZ"  # Switzerland
    MALT = "MALT"  # Malta

    def __str__(self):
        return self.value

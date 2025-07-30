"""This module provides the aliases of the sequences of all available models one might
want to connect to node sequences.

This file was automatically created by function |write_sequencealiases|.
"""

# import...
# ...from standard library
from typing import TYPE_CHECKING

# ...from HydPy
from hydpy.core.aliastools import LazyInOutSequenceImport

if TYPE_CHECKING:
    from hydpy.models.arma.arma_inlets import Q as arma_inlets_Q
    from hydpy.models.arma.arma_fluxes import QIn as arma_fluxes_QIn
    from hydpy.models.arma.arma_fluxes import QOut as arma_fluxes_QOut
    from hydpy.models.arma.arma_outlets import Q as arma_outlets_Q
    from hydpy.models.conv.conv_inlets import Inputs as conv_inlets_Inputs
    from hydpy.models.conv.conv_fluxes import (
        ActualConstant as conv_fluxes_ActualConstant,
    )
    from hydpy.models.conv.conv_fluxes import ActualFactor as conv_fluxes_ActualFactor
    from hydpy.models.conv.conv_outlets import Outputs as conv_outlets_Outputs
    from hydpy.models.dam.dam_inlets import Q as dam_inlets_Q
    from hydpy.models.dam.dam_inlets import S as dam_inlets_S
    from hydpy.models.dam.dam_inlets import R as dam_inlets_R
    from hydpy.models.dam.dam_inlets import E as dam_inlets_E
    from hydpy.models.dam.dam_receivers import Q as dam_receivers_Q
    from hydpy.models.dam.dam_receivers import D as dam_receivers_D
    from hydpy.models.dam.dam_receivers import S as dam_receivers_S
    from hydpy.models.dam.dam_receivers import R as dam_receivers_R
    from hydpy.models.dam.dam_receivers import OWL as dam_receivers_OWL
    from hydpy.models.dam.dam_receivers import RWL as dam_receivers_RWL
    from hydpy.models.dam.dam_factors import WaterLevel as dam_factors_WaterLevel
    from hydpy.models.dam.dam_factors import (
        OuterWaterLevel as dam_factors_OuterWaterLevel,
    )
    from hydpy.models.dam.dam_factors import (
        RemoteWaterLevel as dam_factors_RemoteWaterLevel,
    )
    from hydpy.models.dam.dam_factors import (
        WaterLevelDifference as dam_factors_WaterLevelDifference,
    )
    from hydpy.models.dam.dam_factors import (
        EffectiveWaterLevelDifference as dam_factors_EffectiveWaterLevelDifference,
    )
    from hydpy.models.dam.dam_fluxes import Precipitation as dam_fluxes_Precipitation
    from hydpy.models.dam.dam_fluxes import (
        AdjustedPrecipitation as dam_fluxes_AdjustedPrecipitation,
    )
    from hydpy.models.dam.dam_fluxes import (
        PotentialEvaporation as dam_fluxes_PotentialEvaporation,
    )
    from hydpy.models.dam.dam_fluxes import (
        AdjustedEvaporation as dam_fluxes_AdjustedEvaporation,
    )
    from hydpy.models.dam.dam_fluxes import (
        ActualEvaporation as dam_fluxes_ActualEvaporation,
    )
    from hydpy.models.dam.dam_fluxes import Inflow as dam_fluxes_Inflow
    from hydpy.models.dam.dam_fluxes import Exchange as dam_fluxes_Exchange
    from hydpy.models.dam.dam_fluxes import (
        TotalRemoteDischarge as dam_fluxes_TotalRemoteDischarge,
    )
    from hydpy.models.dam.dam_fluxes import (
        NaturalRemoteDischarge as dam_fluxes_NaturalRemoteDischarge,
    )
    from hydpy.models.dam.dam_fluxes import RemoteDemand as dam_fluxes_RemoteDemand
    from hydpy.models.dam.dam_fluxes import RemoteFailure as dam_fluxes_RemoteFailure
    from hydpy.models.dam.dam_fluxes import (
        RequiredRemoteRelease as dam_fluxes_RequiredRemoteRelease,
    )
    from hydpy.models.dam.dam_fluxes import (
        AllowedRemoteRelief as dam_fluxes_AllowedRemoteRelief,
    )
    from hydpy.models.dam.dam_fluxes import (
        RequiredRemoteSupply as dam_fluxes_RequiredRemoteSupply,
    )
    from hydpy.models.dam.dam_fluxes import (
        PossibleRemoteRelief as dam_fluxes_PossibleRemoteRelief,
    )
    from hydpy.models.dam.dam_fluxes import (
        ActualRemoteRelief as dam_fluxes_ActualRemoteRelief,
    )
    from hydpy.models.dam.dam_fluxes import (
        RequiredRelease as dam_fluxes_RequiredRelease,
    )
    from hydpy.models.dam.dam_fluxes import (
        TargetedRelease as dam_fluxes_TargetedRelease,
    )
    from hydpy.models.dam.dam_fluxes import ActualRelease as dam_fluxes_ActualRelease
    from hydpy.models.dam.dam_fluxes import (
        MissingRemoteRelease as dam_fluxes_MissingRemoteRelease,
    )
    from hydpy.models.dam.dam_fluxes import (
        ActualRemoteRelease as dam_fluxes_ActualRemoteRelease,
    )
    from hydpy.models.dam.dam_fluxes import FloodDischarge as dam_fluxes_FloodDischarge
    from hydpy.models.dam.dam_fluxes import FreeDischarge as dam_fluxes_FreeDischarge
    from hydpy.models.dam.dam_fluxes import (
        MaxForcedDischarge as dam_fluxes_MaxForcedDischarge,
    )
    from hydpy.models.dam.dam_fluxes import (
        MaxFreeDischarge as dam_fluxes_MaxFreeDischarge,
    )
    from hydpy.models.dam.dam_fluxes import (
        ForcedDischarge as dam_fluxes_ForcedDischarge,
    )
    from hydpy.models.dam.dam_fluxes import Outflow as dam_fluxes_Outflow
    from hydpy.models.dam.dam_states import WaterVolume as dam_states_WaterVolume
    from hydpy.models.dam.dam_outlets import Q as dam_outlets_Q
    from hydpy.models.dam.dam_outlets import S as dam_outlets_S
    from hydpy.models.dam.dam_outlets import R as dam_outlets_R
    from hydpy.models.dam.dam_senders import D as dam_senders_D
    from hydpy.models.dam.dam_senders import S as dam_senders_S
    from hydpy.models.dam.dam_senders import R as dam_senders_R
    from hydpy.models.dummy.dummy_inlets import Q as dummy_inlets_Q
    from hydpy.models.dummy.dummy_fluxes import Q as dummy_fluxes_Q
    from hydpy.models.dummy.dummy_outlets import Q as dummy_outlets_Q
    from hydpy.models.evap.evap_inputs import (
        ReferenceEvapotranspiration as evap_inputs_ReferenceEvapotranspiration,
    )
    from hydpy.models.evap.evap_inputs import (
        RelativeHumidity as evap_inputs_RelativeHumidity,
    )
    from hydpy.models.evap.evap_inputs import WindSpeed as evap_inputs_WindSpeed
    from hydpy.models.evap.evap_inputs import (
        AtmosphericPressure as evap_inputs_AtmosphericPressure,
    )
    from hydpy.models.evap.evap_inputs import (
        NormalAirTemperature as evap_inputs_NormalAirTemperature,
    )
    from hydpy.models.evap.evap_inputs import (
        NormalEvapotranspiration as evap_inputs_NormalEvapotranspiration,
    )
    from hydpy.models.evap.evap_factors import (
        MeanAirTemperature as evap_factors_MeanAirTemperature,
    )
    from hydpy.models.evap.evap_factors import WindSpeed2m as evap_factors_WindSpeed2m
    from hydpy.models.evap.evap_factors import (
        DailyWindSpeed2m as evap_factors_DailyWindSpeed2m,
    )
    from hydpy.models.evap.evap_factors import WindSpeed10m as evap_factors_WindSpeed10m
    from hydpy.models.evap.evap_factors import (
        DailyRelativeHumidity as evap_factors_DailyRelativeHumidity,
    )
    from hydpy.models.evap.evap_factors import (
        SunshineDuration as evap_factors_SunshineDuration,
    )
    from hydpy.models.evap.evap_factors import (
        PossibleSunshineDuration as evap_factors_PossibleSunshineDuration,
    )
    from hydpy.models.evap.evap_factors import (
        DailySunshineDuration as evap_factors_DailySunshineDuration,
    )
    from hydpy.models.evap.evap_factors import (
        DailyPossibleSunshineDuration as evap_factors_DailyPossibleSunshineDuration,
    )
    from hydpy.models.evap.evap_factors import (
        PsychrometricConstant as evap_factors_PsychrometricConstant,
    )
    from hydpy.models.evap.evap_factors import (
        AdjustedCloudCoverage as evap_factors_AdjustedCloudCoverage,
    )
    from hydpy.models.evap.evap_fluxes import (
        GlobalRadiation as evap_fluxes_GlobalRadiation,
    )
    from hydpy.models.evap.evap_fluxes import (
        ClearSkySolarRadiation as evap_fluxes_ClearSkySolarRadiation,
    )
    from hydpy.models.evap.evap_fluxes import (
        DailyGlobalRadiation as evap_fluxes_DailyGlobalRadiation,
    )
    from hydpy.models.evap.evap_fluxes import (
        MeanReferenceEvapotranspiration as evap_fluxes_MeanReferenceEvapotranspiration,
    )
    from hydpy.models.evap.evap_fluxes import (
        MeanPotentialEvapotranspiration as evap_fluxes_MeanPotentialEvapotranspiration,
    )
    from hydpy.models.evap.evap_states import CloudCoverage as evap_states_CloudCoverage
    from hydpy.models.exch.exch_inlets import Total as exch_inlets_Total
    from hydpy.models.exch.exch_receivers import WaterLevel as exch_receivers_WaterLevel
    from hydpy.models.exch.exch_receivers import (
        WaterLevels as exch_receivers_WaterLevels,
    )
    from hydpy.models.exch.exch_factors import (
        DeltaWaterLevel as exch_factors_DeltaWaterLevel,
    )
    from hydpy.models.exch.exch_fluxes import (
        PotentialExchange as exch_fluxes_PotentialExchange,
    )
    from hydpy.models.exch.exch_fluxes import (
        ActualExchange as exch_fluxes_ActualExchange,
    )
    from hydpy.models.exch.exch_fluxes import OriginalInput as exch_fluxes_OriginalInput
    from hydpy.models.exch.exch_fluxes import AdjustedInput as exch_fluxes_AdjustedInput
    from hydpy.models.exch.exch_outlets import Exchange as exch_outlets_Exchange
    from hydpy.models.exch.exch_outlets import Branched as exch_outlets_Branched
    from hydpy.models.ga.ga_inputs import Rainfall as ga_inputs_Rainfall
    from hydpy.models.ga.ga_inputs import CapillaryRise as ga_inputs_CapillaryRise
    from hydpy.models.ga.ga_inputs import Evaporation as ga_inputs_Evaporation
    from hydpy.models.ga.ga_fluxes import (
        TotalInfiltration as ga_fluxes_TotalInfiltration,
    )
    from hydpy.models.ga.ga_fluxes import TotalPercolation as ga_fluxes_TotalPercolation
    from hydpy.models.ga.ga_fluxes import (
        TotalSoilWaterAddition as ga_fluxes_TotalSoilWaterAddition,
    )
    from hydpy.models.ga.ga_fluxes import TotalWithdrawal as ga_fluxes_TotalWithdrawal
    from hydpy.models.ga.ga_fluxes import (
        TotalSurfaceRunoff as ga_fluxes_TotalSurfaceRunoff,
    )
    from hydpy.models.gland.gland_inputs import P as gland_inputs_P
    from hydpy.models.gland.gland_fluxes import E as gland_fluxes_E
    from hydpy.models.gland.gland_fluxes import EN as gland_fluxes_EN
    from hydpy.models.gland.gland_fluxes import PN as gland_fluxes_PN
    from hydpy.models.gland.gland_fluxes import PS as gland_fluxes_PS
    from hydpy.models.gland.gland_fluxes import EI as gland_fluxes_EI
    from hydpy.models.gland.gland_fluxes import ES as gland_fluxes_ES
    from hydpy.models.gland.gland_fluxes import AE as gland_fluxes_AE
    from hydpy.models.gland.gland_fluxes import PR as gland_fluxes_PR
    from hydpy.models.gland.gland_fluxes import PR9 as gland_fluxes_PR9
    from hydpy.models.gland.gland_fluxes import PR1 as gland_fluxes_PR1
    from hydpy.models.gland.gland_fluxes import Q10 as gland_fluxes_Q10
    from hydpy.models.gland.gland_fluxes import Perc as gland_fluxes_Perc
    from hydpy.models.gland.gland_fluxes import Q9 as gland_fluxes_Q9
    from hydpy.models.gland.gland_fluxes import Q1 as gland_fluxes_Q1
    from hydpy.models.gland.gland_fluxes import FD as gland_fluxes_FD
    from hydpy.models.gland.gland_fluxes import FR as gland_fluxes_FR
    from hydpy.models.gland.gland_fluxes import FR2 as gland_fluxes_FR2
    from hydpy.models.gland.gland_fluxes import QR as gland_fluxes_QR
    from hydpy.models.gland.gland_fluxes import QR2 as gland_fluxes_QR2
    from hydpy.models.gland.gland_fluxes import QD as gland_fluxes_QD
    from hydpy.models.gland.gland_fluxes import QH as gland_fluxes_QH
    from hydpy.models.gland.gland_fluxes import QV as gland_fluxes_QV
    from hydpy.models.gland.gland_states import I as gland_states_I
    from hydpy.models.gland.gland_states import S as gland_states_S
    from hydpy.models.gland.gland_states import R as gland_states_R
    from hydpy.models.gland.gland_states import R2 as gland_states_R2
    from hydpy.models.gland.gland_outlets import Q as gland_outlets_Q
    from hydpy.models.hland.hland_inputs import P as hland_inputs_P
    from hydpy.models.hland.hland_inputs import T as hland_inputs_T
    from hydpy.models.hland.hland_factors import ContriArea as hland_factors_ContriArea
    from hydpy.models.hland.hland_fluxes import InUZ as hland_fluxes_InUZ
    from hydpy.models.hland.hland_fluxes import Perc as hland_fluxes_Perc
    from hydpy.models.hland.hland_fluxes import Q0 as hland_fluxes_Q0
    from hydpy.models.hland.hland_fluxes import Q1 as hland_fluxes_Q1
    from hydpy.models.hland.hland_fluxes import GR2 as hland_fluxes_GR2
    from hydpy.models.hland.hland_fluxes import RG2 as hland_fluxes_RG2
    from hydpy.models.hland.hland_fluxes import GR3 as hland_fluxes_GR3
    from hydpy.models.hland.hland_fluxes import RG3 as hland_fluxes_RG3
    from hydpy.models.hland.hland_fluxes import InRC as hland_fluxes_InRC
    from hydpy.models.hland.hland_fluxes import OutRC as hland_fluxes_OutRC
    from hydpy.models.hland.hland_fluxes import RO as hland_fluxes_RO
    from hydpy.models.hland.hland_fluxes import RA as hland_fluxes_RA
    from hydpy.models.hland.hland_fluxes import RT as hland_fluxes_RT
    from hydpy.models.hland.hland_fluxes import QT as hland_fluxes_QT
    from hydpy.models.hland.hland_states import UZ as hland_states_UZ
    from hydpy.models.hland.hland_states import LZ as hland_states_LZ
    from hydpy.models.hland.hland_states import SG2 as hland_states_SG2
    from hydpy.models.hland.hland_states import SG3 as hland_states_SG3
    from hydpy.models.hland.hland_outlets import Q as hland_outlets_Q
    from hydpy.models.kinw.kinw_inlets import Q as kinw_inlets_Q
    from hydpy.models.kinw.kinw_fluxes import QZ as kinw_fluxes_QZ
    from hydpy.models.kinw.kinw_fluxes import QZA as kinw_fluxes_QZA
    from hydpy.models.kinw.kinw_fluxes import QA as kinw_fluxes_QA
    from hydpy.models.kinw.kinw_outlets import Q as kinw_outlets_Q
    from hydpy.models.lland.lland_inputs import Nied as lland_inputs_Nied
    from hydpy.models.lland.lland_inputs import TemL as lland_inputs_TemL
    from hydpy.models.lland.lland_inputs import (
        RelativeHumidity as lland_inputs_RelativeHumidity,
    )
    from hydpy.models.lland.lland_inputs import WindSpeed as lland_inputs_WindSpeed
    from hydpy.models.lland.lland_inlets import Q as lland_inlets_Q
    from hydpy.models.lland.lland_factors import (
        PossibleSunshineDuration as lland_factors_PossibleSunshineDuration,
    )
    from hydpy.models.lland.lland_factors import (
        SunshineDuration as lland_factors_SunshineDuration,
    )
    from hydpy.models.lland.lland_fluxes import QZ as lland_fluxes_QZ
    from hydpy.models.lland.lland_fluxes import QZH as lland_fluxes_QZH
    from hydpy.models.lland.lland_fluxes import (
        DailySunshineDuration as lland_fluxes_DailySunshineDuration,
    )
    from hydpy.models.lland.lland_fluxes import (
        DailyPossibleSunshineDuration as lland_fluxes_DailyPossibleSunshineDuration,
    )
    from hydpy.models.lland.lland_fluxes import (
        GlobalRadiation as lland_fluxes_GlobalRadiation,
    )
    from hydpy.models.lland.lland_fluxes import WindSpeed2m as lland_fluxes_WindSpeed2m
    from hydpy.models.lland.lland_fluxes import QDGZ as lland_fluxes_QDGZ
    from hydpy.models.lland.lland_fluxes import QDGZ1 as lland_fluxes_QDGZ1
    from hydpy.models.lland.lland_fluxes import QDGZ2 as lland_fluxes_QDGZ2
    from hydpy.models.lland.lland_fluxes import QIGZ1 as lland_fluxes_QIGZ1
    from hydpy.models.lland.lland_fluxes import QIGZ2 as lland_fluxes_QIGZ2
    from hydpy.models.lland.lland_fluxes import QBGZ as lland_fluxes_QBGZ
    from hydpy.models.lland.lland_fluxes import QDGA1 as lland_fluxes_QDGA1
    from hydpy.models.lland.lland_fluxes import QDGA2 as lland_fluxes_QDGA2
    from hydpy.models.lland.lland_fluxes import QIGA1 as lland_fluxes_QIGA1
    from hydpy.models.lland.lland_fluxes import QIGA2 as lland_fluxes_QIGA2
    from hydpy.models.lland.lland_fluxes import QBGA as lland_fluxes_QBGA
    from hydpy.models.lland.lland_fluxes import QAH as lland_fluxes_QAH
    from hydpy.models.lland.lland_fluxes import QA as lland_fluxes_QA
    from hydpy.models.lland.lland_states import SDG1 as lland_states_SDG1
    from hydpy.models.lland.lland_states import SDG2 as lland_states_SDG2
    from hydpy.models.lland.lland_states import SIG1 as lland_states_SIG1
    from hydpy.models.lland.lland_states import SIG2 as lland_states_SIG2
    from hydpy.models.lland.lland_states import SBG as lland_states_SBG
    from hydpy.models.lland.lland_outlets import Q as lland_outlets_Q
    from hydpy.models.meteo.meteo_inputs import (
        PossibleSunshineDuration as meteo_inputs_PossibleSunshineDuration,
    )
    from hydpy.models.meteo.meteo_inputs import (
        SunshineDuration as meteo_inputs_SunshineDuration,
    )
    from hydpy.models.meteo.meteo_inputs import (
        ClearSkySolarRadiation as meteo_inputs_ClearSkySolarRadiation,
    )
    from hydpy.models.meteo.meteo_inputs import (
        GlobalRadiation as meteo_inputs_GlobalRadiation,
    )
    from hydpy.models.meteo.meteo_inputs import Temperature as meteo_inputs_Temperature
    from hydpy.models.meteo.meteo_inputs import (
        Precipitation as meteo_inputs_Precipitation,
    )
    from hydpy.models.meteo.meteo_factors import (
        EarthSunDistance as meteo_factors_EarthSunDistance,
    )
    from hydpy.models.meteo.meteo_factors import (
        SolarDeclination as meteo_factors_SolarDeclination,
    )
    from hydpy.models.meteo.meteo_factors import (
        SunsetHourAngle as meteo_factors_SunsetHourAngle,
    )
    from hydpy.models.meteo.meteo_factors import (
        SolarTimeAngle as meteo_factors_SolarTimeAngle,
    )
    from hydpy.models.meteo.meteo_factors import (
        TimeOfSunrise as meteo_factors_TimeOfSunrise,
    )
    from hydpy.models.meteo.meteo_factors import (
        TimeOfSunset as meteo_factors_TimeOfSunset,
    )
    from hydpy.models.meteo.meteo_factors import (
        PossibleSunshineDuration as meteo_factors_PossibleSunshineDuration,
    )
    from hydpy.models.meteo.meteo_factors import (
        DailyPossibleSunshineDuration as meteo_factors_DailyPossibleSunshineDuration,
    )
    from hydpy.models.meteo.meteo_factors import (
        UnadjustedSunshineDuration as meteo_factors_UnadjustedSunshineDuration,
    )
    from hydpy.models.meteo.meteo_factors import (
        SunshineDuration as meteo_factors_SunshineDuration,
    )
    from hydpy.models.meteo.meteo_factors import (
        DailySunshineDuration as meteo_factors_DailySunshineDuration,
    )
    from hydpy.models.meteo.meteo_factors import (
        PortionDailyRadiation as meteo_factors_PortionDailyRadiation,
    )
    from hydpy.models.meteo.meteo_factors import (
        MeanTemperature as meteo_factors_MeanTemperature,
    )
    from hydpy.models.meteo.meteo_fluxes import (
        ExtraterrestrialRadiation as meteo_fluxes_ExtraterrestrialRadiation,
    )
    from hydpy.models.meteo.meteo_fluxes import (
        ClearSkySolarRadiation as meteo_fluxes_ClearSkySolarRadiation,
    )
    from hydpy.models.meteo.meteo_fluxes import (
        UnadjustedGlobalRadiation as meteo_fluxes_UnadjustedGlobalRadiation,
    )
    from hydpy.models.meteo.meteo_fluxes import (
        DailyGlobalRadiation as meteo_fluxes_DailyGlobalRadiation,
    )
    from hydpy.models.meteo.meteo_fluxes import (
        GlobalRadiation as meteo_fluxes_GlobalRadiation,
    )
    from hydpy.models.meteo.meteo_fluxes import (
        MeanPrecipitation as meteo_fluxes_MeanPrecipitation,
    )
    from hydpy.models.musk.musk_inlets import Q as musk_inlets_Q
    from hydpy.models.musk.musk_fluxes import Inflow as musk_fluxes_Inflow
    from hydpy.models.musk.musk_fluxes import Outflow as musk_fluxes_Outflow
    from hydpy.models.musk.musk_outlets import Q as musk_outlets_Q
    from hydpy.models.rconc.rconc_fluxes import Inflow as rconc_fluxes_Inflow
    from hydpy.models.rconc.rconc_fluxes import Outflow as rconc_fluxes_Outflow
    from hydpy.models.sw1d.sw1d_inlets import LongQ as sw1d_inlets_LongQ
    from hydpy.models.sw1d.sw1d_inlets import LatQ as sw1d_inlets_LatQ
    from hydpy.models.sw1d.sw1d_inlets import WaterLevel as sw1d_inlets_WaterLevel
    from hydpy.models.sw1d.sw1d_factors import MaxTimeStep as sw1d_factors_MaxTimeStep
    from hydpy.models.sw1d.sw1d_factors import TimeStep as sw1d_factors_TimeStep
    from hydpy.models.sw1d.sw1d_factors import WaterDepth as sw1d_factors_WaterDepth
    from hydpy.models.sw1d.sw1d_factors import WaterLevel as sw1d_factors_WaterLevel
    from hydpy.models.sw1d.sw1d_factors import (
        WaterLevelUpstream as sw1d_factors_WaterLevelUpstream,
    )
    from hydpy.models.sw1d.sw1d_factors import (
        WaterLevelDownstream as sw1d_factors_WaterLevelDownstream,
    )
    from hydpy.models.sw1d.sw1d_factors import (
        WaterVolumeUpstream as sw1d_factors_WaterVolumeUpstream,
    )
    from hydpy.models.sw1d.sw1d_factors import (
        WaterVolumeDownstream as sw1d_factors_WaterVolumeDownstream,
    )
    from hydpy.models.sw1d.sw1d_factors import WettedArea as sw1d_factors_WettedArea
    from hydpy.models.sw1d.sw1d_factors import (
        WettedPerimeter as sw1d_factors_WettedPerimeter,
    )
    from hydpy.models.sw1d.sw1d_fluxes import Inflow as sw1d_fluxes_Inflow
    from hydpy.models.sw1d.sw1d_fluxes import Outflow as sw1d_fluxes_Outflow
    from hydpy.models.sw1d.sw1d_fluxes import LateralFlow as sw1d_fluxes_LateralFlow
    from hydpy.models.sw1d.sw1d_fluxes import NetInflow as sw1d_fluxes_NetInflow
    from hydpy.models.sw1d.sw1d_fluxes import (
        DischargeUpstream as sw1d_fluxes_DischargeUpstream,
    )
    from hydpy.models.sw1d.sw1d_fluxes import (
        DischargeDownstream as sw1d_fluxes_DischargeDownstream,
    )
    from hydpy.models.sw1d.sw1d_fluxes import (
        DischargeVolume as sw1d_fluxes_DischargeVolume,
    )
    from hydpy.models.sw1d.sw1d_states import WaterVolume as sw1d_states_WaterVolume
    from hydpy.models.sw1d.sw1d_states import Discharge as sw1d_states_Discharge
    from hydpy.models.sw1d.sw1d_outlets import LongQ as sw1d_outlets_LongQ
    from hydpy.models.sw1d.sw1d_senders import WaterLevel as sw1d_senders_WaterLevel
    from hydpy.models.test.test_fluxes import Q as test_fluxes_Q
    from hydpy.models.test.test_states import S as test_states_S
    from hydpy.models.whmod.whmod_inputs import (
        Precipitation as whmod_inputs_Precipitation,
    )
    from hydpy.models.whmod.whmod_inputs import Temperature as whmod_inputs_Temperature
    from hydpy.models.whmod.whmod_fluxes import (
        CisternInflow as whmod_fluxes_CisternInflow,
    )
    from hydpy.models.whmod.whmod_fluxes import (
        CisternOverflow as whmod_fluxes_CisternOverflow,
    )
    from hydpy.models.whmod.whmod_fluxes import (
        CisternDemand as whmod_fluxes_CisternDemand,
    )
    from hydpy.models.whmod.whmod_fluxes import (
        CisternExtraction as whmod_fluxes_CisternExtraction,
    )
    from hydpy.models.whmod.whmod_fluxes import (
        ActualRecharge as whmod_fluxes_ActualRecharge,
    )
    from hydpy.models.whmod.whmod_fluxes import (
        DelayedRecharge as whmod_fluxes_DelayedRecharge,
    )
    from hydpy.models.whmod.whmod_states import (
        CisternWater as whmod_states_CisternWater,
    )
    from hydpy.models.whmod.whmod_states import DeepWater as whmod_states_DeepWater
    from hydpy.models.wland.wland_inputs import T as wland_inputs_T
    from hydpy.models.wland.wland_inputs import P as wland_inputs_P
    from hydpy.models.wland.wland_inputs import FXG as wland_inputs_FXG
    from hydpy.models.wland.wland_inputs import FXS as wland_inputs_FXS
    from hydpy.models.wland.wland_factors import DHS as wland_factors_DHS
    from hydpy.models.wland.wland_fluxes import PC as wland_fluxes_PC
    from hydpy.models.wland.wland_fluxes import PS as wland_fluxes_PS
    from hydpy.models.wland.wland_fluxes import PVE as wland_fluxes_PVE
    from hydpy.models.wland.wland_fluxes import PV as wland_fluxes_PV
    from hydpy.models.wland.wland_fluxes import PQ as wland_fluxes_PQ
    from hydpy.models.wland.wland_fluxes import ETVE as wland_fluxes_ETVE
    from hydpy.models.wland.wland_fluxes import ETV as wland_fluxes_ETV
    from hydpy.models.wland.wland_fluxes import ES as wland_fluxes_ES
    from hydpy.models.wland.wland_fluxes import ET as wland_fluxes_ET
    from hydpy.models.wland.wland_fluxes import GR as wland_fluxes_GR
    from hydpy.models.wland.wland_fluxes import FXS as wland_fluxes_FXS
    from hydpy.models.wland.wland_fluxes import FXG as wland_fluxes_FXG
    from hydpy.models.wland.wland_fluxes import CDG as wland_fluxes_CDG
    from hydpy.models.wland.wland_fluxes import FGSE as wland_fluxes_FGSE
    from hydpy.models.wland.wland_fluxes import FGS as wland_fluxes_FGS
    from hydpy.models.wland.wland_fluxes import FQS as wland_fluxes_FQS
    from hydpy.models.wland.wland_fluxes import RH as wland_fluxes_RH
    from hydpy.models.wland.wland_fluxes import R as wland_fluxes_R
    from hydpy.models.wland.wland_states import DVE as wland_states_DVE
    from hydpy.models.wland.wland_states import DV as wland_states_DV
    from hydpy.models.wland.wland_states import HGE as wland_states_HGE
    from hydpy.models.wland.wland_states import DG as wland_states_DG
    from hydpy.models.wland.wland_states import HQ as wland_states_HQ
    from hydpy.models.wland.wland_states import HS as wland_states_HS
    from hydpy.models.wland.wland_outlets import Q as wland_outlets_Q
    from hydpy.models.wq.wq_factors import WaterDepth as wq_factors_WaterDepth
    from hydpy.models.wq.wq_factors import WaterLevel as wq_factors_WaterLevel
    from hydpy.models.wq.wq_factors import WettedArea as wq_factors_WettedArea
    from hydpy.models.wq.wq_factors import WettedPerimeter as wq_factors_WettedPerimeter
    from hydpy.models.wq.wq_factors import SurfaceWidth as wq_factors_SurfaceWidth
    from hydpy.models.wq.wq_factors import (
        DischargeDerivative as wq_factors_DischargeDerivative,
    )
    from hydpy.models.wq.wq_factors import Celerity as wq_factors_Celerity
    from hydpy.models.wq.wq_fluxes import Discharge as wq_fluxes_Discharge
else:
    arma_inlets_Q = LazyInOutSequenceImport(
        modulename="hydpy.models.arma.arma_inlets",
        classname="Q",
        alias="arma_inlets_Q",
        namespace=locals(),
    )
    arma_fluxes_QIn = LazyInOutSequenceImport(
        modulename="hydpy.models.arma.arma_fluxes",
        classname="QIn",
        alias="arma_fluxes_QIn",
        namespace=locals(),
    )
    arma_fluxes_QOut = LazyInOutSequenceImport(
        modulename="hydpy.models.arma.arma_fluxes",
        classname="QOut",
        alias="arma_fluxes_QOut",
        namespace=locals(),
    )
    arma_outlets_Q = LazyInOutSequenceImport(
        modulename="hydpy.models.arma.arma_outlets",
        classname="Q",
        alias="arma_outlets_Q",
        namespace=locals(),
    )
    conv_inlets_Inputs = LazyInOutSequenceImport(
        modulename="hydpy.models.conv.conv_inlets",
        classname="Inputs",
        alias="conv_inlets_Inputs",
        namespace=locals(),
    )
    conv_fluxes_ActualConstant = LazyInOutSequenceImport(
        modulename="hydpy.models.conv.conv_fluxes",
        classname="ActualConstant",
        alias="conv_fluxes_ActualConstant",
        namespace=locals(),
    )
    conv_fluxes_ActualFactor = LazyInOutSequenceImport(
        modulename="hydpy.models.conv.conv_fluxes",
        classname="ActualFactor",
        alias="conv_fluxes_ActualFactor",
        namespace=locals(),
    )
    conv_outlets_Outputs = LazyInOutSequenceImport(
        modulename="hydpy.models.conv.conv_outlets",
        classname="Outputs",
        alias="conv_outlets_Outputs",
        namespace=locals(),
    )
    dam_inlets_Q = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_inlets",
        classname="Q",
        alias="dam_inlets_Q",
        namespace=locals(),
    )
    dam_inlets_S = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_inlets",
        classname="S",
        alias="dam_inlets_S",
        namespace=locals(),
    )
    dam_inlets_R = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_inlets",
        classname="R",
        alias="dam_inlets_R",
        namespace=locals(),
    )
    dam_inlets_E = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_inlets",
        classname="E",
        alias="dam_inlets_E",
        namespace=locals(),
    )
    dam_receivers_Q = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_receivers",
        classname="Q",
        alias="dam_receivers_Q",
        namespace=locals(),
    )
    dam_receivers_D = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_receivers",
        classname="D",
        alias="dam_receivers_D",
        namespace=locals(),
    )
    dam_receivers_S = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_receivers",
        classname="S",
        alias="dam_receivers_S",
        namespace=locals(),
    )
    dam_receivers_R = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_receivers",
        classname="R",
        alias="dam_receivers_R",
        namespace=locals(),
    )
    dam_receivers_OWL = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_receivers",
        classname="OWL",
        alias="dam_receivers_OWL",
        namespace=locals(),
    )
    dam_receivers_RWL = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_receivers",
        classname="RWL",
        alias="dam_receivers_RWL",
        namespace=locals(),
    )
    dam_factors_WaterLevel = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_factors",
        classname="WaterLevel",
        alias="dam_factors_WaterLevel",
        namespace=locals(),
    )
    dam_factors_OuterWaterLevel = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_factors",
        classname="OuterWaterLevel",
        alias="dam_factors_OuterWaterLevel",
        namespace=locals(),
    )
    dam_factors_RemoteWaterLevel = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_factors",
        classname="RemoteWaterLevel",
        alias="dam_factors_RemoteWaterLevel",
        namespace=locals(),
    )
    dam_factors_WaterLevelDifference = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_factors",
        classname="WaterLevelDifference",
        alias="dam_factors_WaterLevelDifference",
        namespace=locals(),
    )
    dam_factors_EffectiveWaterLevelDifference = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_factors",
        classname="EffectiveWaterLevelDifference",
        alias="dam_factors_EffectiveWaterLevelDifference",
        namespace=locals(),
    )
    dam_fluxes_Precipitation = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="Precipitation",
        alias="dam_fluxes_Precipitation",
        namespace=locals(),
    )
    dam_fluxes_AdjustedPrecipitation = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="AdjustedPrecipitation",
        alias="dam_fluxes_AdjustedPrecipitation",
        namespace=locals(),
    )
    dam_fluxes_PotentialEvaporation = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="PotentialEvaporation",
        alias="dam_fluxes_PotentialEvaporation",
        namespace=locals(),
    )
    dam_fluxes_AdjustedEvaporation = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="AdjustedEvaporation",
        alias="dam_fluxes_AdjustedEvaporation",
        namespace=locals(),
    )
    dam_fluxes_ActualEvaporation = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="ActualEvaporation",
        alias="dam_fluxes_ActualEvaporation",
        namespace=locals(),
    )
    dam_fluxes_Inflow = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="Inflow",
        alias="dam_fluxes_Inflow",
        namespace=locals(),
    )
    dam_fluxes_Exchange = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="Exchange",
        alias="dam_fluxes_Exchange",
        namespace=locals(),
    )
    dam_fluxes_TotalRemoteDischarge = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="TotalRemoteDischarge",
        alias="dam_fluxes_TotalRemoteDischarge",
        namespace=locals(),
    )
    dam_fluxes_NaturalRemoteDischarge = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="NaturalRemoteDischarge",
        alias="dam_fluxes_NaturalRemoteDischarge",
        namespace=locals(),
    )
    dam_fluxes_RemoteDemand = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="RemoteDemand",
        alias="dam_fluxes_RemoteDemand",
        namespace=locals(),
    )
    dam_fluxes_RemoteFailure = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="RemoteFailure",
        alias="dam_fluxes_RemoteFailure",
        namespace=locals(),
    )
    dam_fluxes_RequiredRemoteRelease = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="RequiredRemoteRelease",
        alias="dam_fluxes_RequiredRemoteRelease",
        namespace=locals(),
    )
    dam_fluxes_AllowedRemoteRelief = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="AllowedRemoteRelief",
        alias="dam_fluxes_AllowedRemoteRelief",
        namespace=locals(),
    )
    dam_fluxes_RequiredRemoteSupply = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="RequiredRemoteSupply",
        alias="dam_fluxes_RequiredRemoteSupply",
        namespace=locals(),
    )
    dam_fluxes_PossibleRemoteRelief = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="PossibleRemoteRelief",
        alias="dam_fluxes_PossibleRemoteRelief",
        namespace=locals(),
    )
    dam_fluxes_ActualRemoteRelief = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="ActualRemoteRelief",
        alias="dam_fluxes_ActualRemoteRelief",
        namespace=locals(),
    )
    dam_fluxes_RequiredRelease = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="RequiredRelease",
        alias="dam_fluxes_RequiredRelease",
        namespace=locals(),
    )
    dam_fluxes_TargetedRelease = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="TargetedRelease",
        alias="dam_fluxes_TargetedRelease",
        namespace=locals(),
    )
    dam_fluxes_ActualRelease = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="ActualRelease",
        alias="dam_fluxes_ActualRelease",
        namespace=locals(),
    )
    dam_fluxes_MissingRemoteRelease = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="MissingRemoteRelease",
        alias="dam_fluxes_MissingRemoteRelease",
        namespace=locals(),
    )
    dam_fluxes_ActualRemoteRelease = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="ActualRemoteRelease",
        alias="dam_fluxes_ActualRemoteRelease",
        namespace=locals(),
    )
    dam_fluxes_FloodDischarge = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="FloodDischarge",
        alias="dam_fluxes_FloodDischarge",
        namespace=locals(),
    )
    dam_fluxes_FreeDischarge = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="FreeDischarge",
        alias="dam_fluxes_FreeDischarge",
        namespace=locals(),
    )
    dam_fluxes_MaxForcedDischarge = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="MaxForcedDischarge",
        alias="dam_fluxes_MaxForcedDischarge",
        namespace=locals(),
    )
    dam_fluxes_MaxFreeDischarge = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="MaxFreeDischarge",
        alias="dam_fluxes_MaxFreeDischarge",
        namespace=locals(),
    )
    dam_fluxes_ForcedDischarge = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="ForcedDischarge",
        alias="dam_fluxes_ForcedDischarge",
        namespace=locals(),
    )
    dam_fluxes_Outflow = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_fluxes",
        classname="Outflow",
        alias="dam_fluxes_Outflow",
        namespace=locals(),
    )
    dam_states_WaterVolume = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_states",
        classname="WaterVolume",
        alias="dam_states_WaterVolume",
        namespace=locals(),
    )
    dam_outlets_Q = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_outlets",
        classname="Q",
        alias="dam_outlets_Q",
        namespace=locals(),
    )
    dam_outlets_S = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_outlets",
        classname="S",
        alias="dam_outlets_S",
        namespace=locals(),
    )
    dam_outlets_R = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_outlets",
        classname="R",
        alias="dam_outlets_R",
        namespace=locals(),
    )
    dam_senders_D = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_senders",
        classname="D",
        alias="dam_senders_D",
        namespace=locals(),
    )
    dam_senders_S = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_senders",
        classname="S",
        alias="dam_senders_S",
        namespace=locals(),
    )
    dam_senders_R = LazyInOutSequenceImport(
        modulename="hydpy.models.dam.dam_senders",
        classname="R",
        alias="dam_senders_R",
        namespace=locals(),
    )
    dummy_inlets_Q = LazyInOutSequenceImport(
        modulename="hydpy.models.dummy.dummy_inlets",
        classname="Q",
        alias="dummy_inlets_Q",
        namespace=locals(),
    )
    dummy_fluxes_Q = LazyInOutSequenceImport(
        modulename="hydpy.models.dummy.dummy_fluxes",
        classname="Q",
        alias="dummy_fluxes_Q",
        namespace=locals(),
    )
    dummy_outlets_Q = LazyInOutSequenceImport(
        modulename="hydpy.models.dummy.dummy_outlets",
        classname="Q",
        alias="dummy_outlets_Q",
        namespace=locals(),
    )
    evap_inputs_ReferenceEvapotranspiration = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_inputs",
        classname="ReferenceEvapotranspiration",
        alias="evap_inputs_ReferenceEvapotranspiration",
        namespace=locals(),
    )
    evap_inputs_RelativeHumidity = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_inputs",
        classname="RelativeHumidity",
        alias="evap_inputs_RelativeHumidity",
        namespace=locals(),
    )
    evap_inputs_WindSpeed = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_inputs",
        classname="WindSpeed",
        alias="evap_inputs_WindSpeed",
        namespace=locals(),
    )
    evap_inputs_AtmosphericPressure = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_inputs",
        classname="AtmosphericPressure",
        alias="evap_inputs_AtmosphericPressure",
        namespace=locals(),
    )
    evap_inputs_NormalAirTemperature = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_inputs",
        classname="NormalAirTemperature",
        alias="evap_inputs_NormalAirTemperature",
        namespace=locals(),
    )
    evap_inputs_NormalEvapotranspiration = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_inputs",
        classname="NormalEvapotranspiration",
        alias="evap_inputs_NormalEvapotranspiration",
        namespace=locals(),
    )
    evap_factors_MeanAirTemperature = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_factors",
        classname="MeanAirTemperature",
        alias="evap_factors_MeanAirTemperature",
        namespace=locals(),
    )
    evap_factors_WindSpeed2m = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_factors",
        classname="WindSpeed2m",
        alias="evap_factors_WindSpeed2m",
        namespace=locals(),
    )
    evap_factors_DailyWindSpeed2m = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_factors",
        classname="DailyWindSpeed2m",
        alias="evap_factors_DailyWindSpeed2m",
        namespace=locals(),
    )
    evap_factors_WindSpeed10m = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_factors",
        classname="WindSpeed10m",
        alias="evap_factors_WindSpeed10m",
        namespace=locals(),
    )
    evap_factors_DailyRelativeHumidity = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_factors",
        classname="DailyRelativeHumidity",
        alias="evap_factors_DailyRelativeHumidity",
        namespace=locals(),
    )
    evap_factors_SunshineDuration = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_factors",
        classname="SunshineDuration",
        alias="evap_factors_SunshineDuration",
        namespace=locals(),
    )
    evap_factors_PossibleSunshineDuration = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_factors",
        classname="PossibleSunshineDuration",
        alias="evap_factors_PossibleSunshineDuration",
        namespace=locals(),
    )
    evap_factors_DailySunshineDuration = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_factors",
        classname="DailySunshineDuration",
        alias="evap_factors_DailySunshineDuration",
        namespace=locals(),
    )
    evap_factors_DailyPossibleSunshineDuration = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_factors",
        classname="DailyPossibleSunshineDuration",
        alias="evap_factors_DailyPossibleSunshineDuration",
        namespace=locals(),
    )
    evap_factors_PsychrometricConstant = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_factors",
        classname="PsychrometricConstant",
        alias="evap_factors_PsychrometricConstant",
        namespace=locals(),
    )
    evap_factors_AdjustedCloudCoverage = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_factors",
        classname="AdjustedCloudCoverage",
        alias="evap_factors_AdjustedCloudCoverage",
        namespace=locals(),
    )
    evap_fluxes_GlobalRadiation = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_fluxes",
        classname="GlobalRadiation",
        alias="evap_fluxes_GlobalRadiation",
        namespace=locals(),
    )
    evap_fluxes_ClearSkySolarRadiation = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_fluxes",
        classname="ClearSkySolarRadiation",
        alias="evap_fluxes_ClearSkySolarRadiation",
        namespace=locals(),
    )
    evap_fluxes_DailyGlobalRadiation = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_fluxes",
        classname="DailyGlobalRadiation",
        alias="evap_fluxes_DailyGlobalRadiation",
        namespace=locals(),
    )
    evap_fluxes_MeanReferenceEvapotranspiration = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_fluxes",
        classname="MeanReferenceEvapotranspiration",
        alias="evap_fluxes_MeanReferenceEvapotranspiration",
        namespace=locals(),
    )
    evap_fluxes_MeanPotentialEvapotranspiration = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_fluxes",
        classname="MeanPotentialEvapotranspiration",
        alias="evap_fluxes_MeanPotentialEvapotranspiration",
        namespace=locals(),
    )
    evap_states_CloudCoverage = LazyInOutSequenceImport(
        modulename="hydpy.models.evap.evap_states",
        classname="CloudCoverage",
        alias="evap_states_CloudCoverage",
        namespace=locals(),
    )
    exch_inlets_Total = LazyInOutSequenceImport(
        modulename="hydpy.models.exch.exch_inlets",
        classname="Total",
        alias="exch_inlets_Total",
        namespace=locals(),
    )
    exch_receivers_WaterLevel = LazyInOutSequenceImport(
        modulename="hydpy.models.exch.exch_receivers",
        classname="WaterLevel",
        alias="exch_receivers_WaterLevel",
        namespace=locals(),
    )
    exch_receivers_WaterLevels = LazyInOutSequenceImport(
        modulename="hydpy.models.exch.exch_receivers",
        classname="WaterLevels",
        alias="exch_receivers_WaterLevels",
        namespace=locals(),
    )
    exch_factors_DeltaWaterLevel = LazyInOutSequenceImport(
        modulename="hydpy.models.exch.exch_factors",
        classname="DeltaWaterLevel",
        alias="exch_factors_DeltaWaterLevel",
        namespace=locals(),
    )
    exch_fluxes_PotentialExchange = LazyInOutSequenceImport(
        modulename="hydpy.models.exch.exch_fluxes",
        classname="PotentialExchange",
        alias="exch_fluxes_PotentialExchange",
        namespace=locals(),
    )
    exch_fluxes_ActualExchange = LazyInOutSequenceImport(
        modulename="hydpy.models.exch.exch_fluxes",
        classname="ActualExchange",
        alias="exch_fluxes_ActualExchange",
        namespace=locals(),
    )
    exch_fluxes_OriginalInput = LazyInOutSequenceImport(
        modulename="hydpy.models.exch.exch_fluxes",
        classname="OriginalInput",
        alias="exch_fluxes_OriginalInput",
        namespace=locals(),
    )
    exch_fluxes_AdjustedInput = LazyInOutSequenceImport(
        modulename="hydpy.models.exch.exch_fluxes",
        classname="AdjustedInput",
        alias="exch_fluxes_AdjustedInput",
        namespace=locals(),
    )
    exch_outlets_Exchange = LazyInOutSequenceImport(
        modulename="hydpy.models.exch.exch_outlets",
        classname="Exchange",
        alias="exch_outlets_Exchange",
        namespace=locals(),
    )
    exch_outlets_Branched = LazyInOutSequenceImport(
        modulename="hydpy.models.exch.exch_outlets",
        classname="Branched",
        alias="exch_outlets_Branched",
        namespace=locals(),
    )
    ga_inputs_Rainfall = LazyInOutSequenceImport(
        modulename="hydpy.models.ga.ga_inputs",
        classname="Rainfall",
        alias="ga_inputs_Rainfall",
        namespace=locals(),
    )
    ga_inputs_CapillaryRise = LazyInOutSequenceImport(
        modulename="hydpy.models.ga.ga_inputs",
        classname="CapillaryRise",
        alias="ga_inputs_CapillaryRise",
        namespace=locals(),
    )
    ga_inputs_Evaporation = LazyInOutSequenceImport(
        modulename="hydpy.models.ga.ga_inputs",
        classname="Evaporation",
        alias="ga_inputs_Evaporation",
        namespace=locals(),
    )
    ga_fluxes_TotalInfiltration = LazyInOutSequenceImport(
        modulename="hydpy.models.ga.ga_fluxes",
        classname="TotalInfiltration",
        alias="ga_fluxes_TotalInfiltration",
        namespace=locals(),
    )
    ga_fluxes_TotalPercolation = LazyInOutSequenceImport(
        modulename="hydpy.models.ga.ga_fluxes",
        classname="TotalPercolation",
        alias="ga_fluxes_TotalPercolation",
        namespace=locals(),
    )
    ga_fluxes_TotalSoilWaterAddition = LazyInOutSequenceImport(
        modulename="hydpy.models.ga.ga_fluxes",
        classname="TotalSoilWaterAddition",
        alias="ga_fluxes_TotalSoilWaterAddition",
        namespace=locals(),
    )
    ga_fluxes_TotalWithdrawal = LazyInOutSequenceImport(
        modulename="hydpy.models.ga.ga_fluxes",
        classname="TotalWithdrawal",
        alias="ga_fluxes_TotalWithdrawal",
        namespace=locals(),
    )
    ga_fluxes_TotalSurfaceRunoff = LazyInOutSequenceImport(
        modulename="hydpy.models.ga.ga_fluxes",
        classname="TotalSurfaceRunoff",
        alias="ga_fluxes_TotalSurfaceRunoff",
        namespace=locals(),
    )
    gland_inputs_P = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_inputs",
        classname="P",
        alias="gland_inputs_P",
        namespace=locals(),
    )
    gland_fluxes_E = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_fluxes",
        classname="E",
        alias="gland_fluxes_E",
        namespace=locals(),
    )
    gland_fluxes_EN = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_fluxes",
        classname="EN",
        alias="gland_fluxes_EN",
        namespace=locals(),
    )
    gland_fluxes_PN = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_fluxes",
        classname="PN",
        alias="gland_fluxes_PN",
        namespace=locals(),
    )
    gland_fluxes_PS = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_fluxes",
        classname="PS",
        alias="gland_fluxes_PS",
        namespace=locals(),
    )
    gland_fluxes_EI = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_fluxes",
        classname="EI",
        alias="gland_fluxes_EI",
        namespace=locals(),
    )
    gland_fluxes_ES = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_fluxes",
        classname="ES",
        alias="gland_fluxes_ES",
        namespace=locals(),
    )
    gland_fluxes_AE = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_fluxes",
        classname="AE",
        alias="gland_fluxes_AE",
        namespace=locals(),
    )
    gland_fluxes_PR = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_fluxes",
        classname="PR",
        alias="gland_fluxes_PR",
        namespace=locals(),
    )
    gland_fluxes_PR9 = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_fluxes",
        classname="PR9",
        alias="gland_fluxes_PR9",
        namespace=locals(),
    )
    gland_fluxes_PR1 = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_fluxes",
        classname="PR1",
        alias="gland_fluxes_PR1",
        namespace=locals(),
    )
    gland_fluxes_Q10 = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_fluxes",
        classname="Q10",
        alias="gland_fluxes_Q10",
        namespace=locals(),
    )
    gland_fluxes_Perc = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_fluxes",
        classname="Perc",
        alias="gland_fluxes_Perc",
        namespace=locals(),
    )
    gland_fluxes_Q9 = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_fluxes",
        classname="Q9",
        alias="gland_fluxes_Q9",
        namespace=locals(),
    )
    gland_fluxes_Q1 = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_fluxes",
        classname="Q1",
        alias="gland_fluxes_Q1",
        namespace=locals(),
    )
    gland_fluxes_FD = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_fluxes",
        classname="FD",
        alias="gland_fluxes_FD",
        namespace=locals(),
    )
    gland_fluxes_FR = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_fluxes",
        classname="FR",
        alias="gland_fluxes_FR",
        namespace=locals(),
    )
    gland_fluxes_FR2 = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_fluxes",
        classname="FR2",
        alias="gland_fluxes_FR2",
        namespace=locals(),
    )
    gland_fluxes_QR = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_fluxes",
        classname="QR",
        alias="gland_fluxes_QR",
        namespace=locals(),
    )
    gland_fluxes_QR2 = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_fluxes",
        classname="QR2",
        alias="gland_fluxes_QR2",
        namespace=locals(),
    )
    gland_fluxes_QD = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_fluxes",
        classname="QD",
        alias="gland_fluxes_QD",
        namespace=locals(),
    )
    gland_fluxes_QH = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_fluxes",
        classname="QH",
        alias="gland_fluxes_QH",
        namespace=locals(),
    )
    gland_fluxes_QV = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_fluxes",
        classname="QV",
        alias="gland_fluxes_QV",
        namespace=locals(),
    )
    gland_states_I = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_states",
        classname="I",
        alias="gland_states_I",
        namespace=locals(),
    )
    gland_states_S = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_states",
        classname="S",
        alias="gland_states_S",
        namespace=locals(),
    )
    gland_states_R = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_states",
        classname="R",
        alias="gland_states_R",
        namespace=locals(),
    )
    gland_states_R2 = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_states",
        classname="R2",
        alias="gland_states_R2",
        namespace=locals(),
    )
    gland_outlets_Q = LazyInOutSequenceImport(
        modulename="hydpy.models.gland.gland_outlets",
        classname="Q",
        alias="gland_outlets_Q",
        namespace=locals(),
    )
    hland_inputs_P = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_inputs",
        classname="P",
        alias="hland_inputs_P",
        namespace=locals(),
    )
    hland_inputs_T = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_inputs",
        classname="T",
        alias="hland_inputs_T",
        namespace=locals(),
    )
    hland_factors_ContriArea = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_factors",
        classname="ContriArea",
        alias="hland_factors_ContriArea",
        namespace=locals(),
    )
    hland_fluxes_InUZ = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_fluxes",
        classname="InUZ",
        alias="hland_fluxes_InUZ",
        namespace=locals(),
    )
    hland_fluxes_Perc = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_fluxes",
        classname="Perc",
        alias="hland_fluxes_Perc",
        namespace=locals(),
    )
    hland_fluxes_Q0 = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_fluxes",
        classname="Q0",
        alias="hland_fluxes_Q0",
        namespace=locals(),
    )
    hland_fluxes_Q1 = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_fluxes",
        classname="Q1",
        alias="hland_fluxes_Q1",
        namespace=locals(),
    )
    hland_fluxes_GR2 = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_fluxes",
        classname="GR2",
        alias="hland_fluxes_GR2",
        namespace=locals(),
    )
    hland_fluxes_RG2 = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_fluxes",
        classname="RG2",
        alias="hland_fluxes_RG2",
        namespace=locals(),
    )
    hland_fluxes_GR3 = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_fluxes",
        classname="GR3",
        alias="hland_fluxes_GR3",
        namespace=locals(),
    )
    hland_fluxes_RG3 = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_fluxes",
        classname="RG3",
        alias="hland_fluxes_RG3",
        namespace=locals(),
    )
    hland_fluxes_InRC = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_fluxes",
        classname="InRC",
        alias="hland_fluxes_InRC",
        namespace=locals(),
    )
    hland_fluxes_OutRC = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_fluxes",
        classname="OutRC",
        alias="hland_fluxes_OutRC",
        namespace=locals(),
    )
    hland_fluxes_RO = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_fluxes",
        classname="RO",
        alias="hland_fluxes_RO",
        namespace=locals(),
    )
    hland_fluxes_RA = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_fluxes",
        classname="RA",
        alias="hland_fluxes_RA",
        namespace=locals(),
    )
    hland_fluxes_RT = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_fluxes",
        classname="RT",
        alias="hland_fluxes_RT",
        namespace=locals(),
    )
    hland_fluxes_QT = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_fluxes",
        classname="QT",
        alias="hland_fluxes_QT",
        namespace=locals(),
    )
    hland_states_UZ = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_states",
        classname="UZ",
        alias="hland_states_UZ",
        namespace=locals(),
    )
    hland_states_LZ = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_states",
        classname="LZ",
        alias="hland_states_LZ",
        namespace=locals(),
    )
    hland_states_SG2 = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_states",
        classname="SG2",
        alias="hland_states_SG2",
        namespace=locals(),
    )
    hland_states_SG3 = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_states",
        classname="SG3",
        alias="hland_states_SG3",
        namespace=locals(),
    )
    hland_outlets_Q = LazyInOutSequenceImport(
        modulename="hydpy.models.hland.hland_outlets",
        classname="Q",
        alias="hland_outlets_Q",
        namespace=locals(),
    )
    kinw_inlets_Q = LazyInOutSequenceImport(
        modulename="hydpy.models.kinw.kinw_inlets",
        classname="Q",
        alias="kinw_inlets_Q",
        namespace=locals(),
    )
    kinw_fluxes_QZ = LazyInOutSequenceImport(
        modulename="hydpy.models.kinw.kinw_fluxes",
        classname="QZ",
        alias="kinw_fluxes_QZ",
        namespace=locals(),
    )
    kinw_fluxes_QZA = LazyInOutSequenceImport(
        modulename="hydpy.models.kinw.kinw_fluxes",
        classname="QZA",
        alias="kinw_fluxes_QZA",
        namespace=locals(),
    )
    kinw_fluxes_QA = LazyInOutSequenceImport(
        modulename="hydpy.models.kinw.kinw_fluxes",
        classname="QA",
        alias="kinw_fluxes_QA",
        namespace=locals(),
    )
    kinw_outlets_Q = LazyInOutSequenceImport(
        modulename="hydpy.models.kinw.kinw_outlets",
        classname="Q",
        alias="kinw_outlets_Q",
        namespace=locals(),
    )
    lland_inputs_Nied = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_inputs",
        classname="Nied",
        alias="lland_inputs_Nied",
        namespace=locals(),
    )
    lland_inputs_TemL = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_inputs",
        classname="TemL",
        alias="lland_inputs_TemL",
        namespace=locals(),
    )
    lland_inputs_RelativeHumidity = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_inputs",
        classname="RelativeHumidity",
        alias="lland_inputs_RelativeHumidity",
        namespace=locals(),
    )
    lland_inputs_WindSpeed = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_inputs",
        classname="WindSpeed",
        alias="lland_inputs_WindSpeed",
        namespace=locals(),
    )
    lland_inlets_Q = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_inlets",
        classname="Q",
        alias="lland_inlets_Q",
        namespace=locals(),
    )
    lland_factors_PossibleSunshineDuration = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_factors",
        classname="PossibleSunshineDuration",
        alias="lland_factors_PossibleSunshineDuration",
        namespace=locals(),
    )
    lland_factors_SunshineDuration = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_factors",
        classname="SunshineDuration",
        alias="lland_factors_SunshineDuration",
        namespace=locals(),
    )
    lland_fluxes_QZ = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="QZ",
        alias="lland_fluxes_QZ",
        namespace=locals(),
    )
    lland_fluxes_QZH = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="QZH",
        alias="lland_fluxes_QZH",
        namespace=locals(),
    )
    lland_fluxes_DailySunshineDuration = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="DailySunshineDuration",
        alias="lland_fluxes_DailySunshineDuration",
        namespace=locals(),
    )
    lland_fluxes_DailyPossibleSunshineDuration = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="DailyPossibleSunshineDuration",
        alias="lland_fluxes_DailyPossibleSunshineDuration",
        namespace=locals(),
    )
    lland_fluxes_GlobalRadiation = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="GlobalRadiation",
        alias="lland_fluxes_GlobalRadiation",
        namespace=locals(),
    )
    lland_fluxes_WindSpeed2m = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="WindSpeed2m",
        alias="lland_fluxes_WindSpeed2m",
        namespace=locals(),
    )
    lland_fluxes_QDGZ = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="QDGZ",
        alias="lland_fluxes_QDGZ",
        namespace=locals(),
    )
    lland_fluxes_QDGZ1 = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="QDGZ1",
        alias="lland_fluxes_QDGZ1",
        namespace=locals(),
    )
    lland_fluxes_QDGZ2 = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="QDGZ2",
        alias="lland_fluxes_QDGZ2",
        namespace=locals(),
    )
    lland_fluxes_QIGZ1 = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="QIGZ1",
        alias="lland_fluxes_QIGZ1",
        namespace=locals(),
    )
    lland_fluxes_QIGZ2 = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="QIGZ2",
        alias="lland_fluxes_QIGZ2",
        namespace=locals(),
    )
    lland_fluxes_QBGZ = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="QBGZ",
        alias="lland_fluxes_QBGZ",
        namespace=locals(),
    )
    lland_fluxes_QDGA1 = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="QDGA1",
        alias="lland_fluxes_QDGA1",
        namespace=locals(),
    )
    lland_fluxes_QDGA2 = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="QDGA2",
        alias="lland_fluxes_QDGA2",
        namespace=locals(),
    )
    lland_fluxes_QIGA1 = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="QIGA1",
        alias="lland_fluxes_QIGA1",
        namespace=locals(),
    )
    lland_fluxes_QIGA2 = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="QIGA2",
        alias="lland_fluxes_QIGA2",
        namespace=locals(),
    )
    lland_fluxes_QBGA = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="QBGA",
        alias="lland_fluxes_QBGA",
        namespace=locals(),
    )
    lland_fluxes_QAH = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="QAH",
        alias="lland_fluxes_QAH",
        namespace=locals(),
    )
    lland_fluxes_QA = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_fluxes",
        classname="QA",
        alias="lland_fluxes_QA",
        namespace=locals(),
    )
    lland_states_SDG1 = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_states",
        classname="SDG1",
        alias="lland_states_SDG1",
        namespace=locals(),
    )
    lland_states_SDG2 = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_states",
        classname="SDG2",
        alias="lland_states_SDG2",
        namespace=locals(),
    )
    lland_states_SIG1 = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_states",
        classname="SIG1",
        alias="lland_states_SIG1",
        namespace=locals(),
    )
    lland_states_SIG2 = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_states",
        classname="SIG2",
        alias="lland_states_SIG2",
        namespace=locals(),
    )
    lland_states_SBG = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_states",
        classname="SBG",
        alias="lland_states_SBG",
        namespace=locals(),
    )
    lland_outlets_Q = LazyInOutSequenceImport(
        modulename="hydpy.models.lland.lland_outlets",
        classname="Q",
        alias="lland_outlets_Q",
        namespace=locals(),
    )
    meteo_inputs_PossibleSunshineDuration = LazyInOutSequenceImport(
        modulename="hydpy.models.meteo.meteo_inputs",
        classname="PossibleSunshineDuration",
        alias="meteo_inputs_PossibleSunshineDuration",
        namespace=locals(),
    )
    meteo_inputs_SunshineDuration = LazyInOutSequenceImport(
        modulename="hydpy.models.meteo.meteo_inputs",
        classname="SunshineDuration",
        alias="meteo_inputs_SunshineDuration",
        namespace=locals(),
    )
    meteo_inputs_ClearSkySolarRadiation = LazyInOutSequenceImport(
        modulename="hydpy.models.meteo.meteo_inputs",
        classname="ClearSkySolarRadiation",
        alias="meteo_inputs_ClearSkySolarRadiation",
        namespace=locals(),
    )
    meteo_inputs_GlobalRadiation = LazyInOutSequenceImport(
        modulename="hydpy.models.meteo.meteo_inputs",
        classname="GlobalRadiation",
        alias="meteo_inputs_GlobalRadiation",
        namespace=locals(),
    )
    meteo_inputs_Temperature = LazyInOutSequenceImport(
        modulename="hydpy.models.meteo.meteo_inputs",
        classname="Temperature",
        alias="meteo_inputs_Temperature",
        namespace=locals(),
    )
    meteo_inputs_Precipitation = LazyInOutSequenceImport(
        modulename="hydpy.models.meteo.meteo_inputs",
        classname="Precipitation",
        alias="meteo_inputs_Precipitation",
        namespace=locals(),
    )
    meteo_factors_EarthSunDistance = LazyInOutSequenceImport(
        modulename="hydpy.models.meteo.meteo_factors",
        classname="EarthSunDistance",
        alias="meteo_factors_EarthSunDistance",
        namespace=locals(),
    )
    meteo_factors_SolarDeclination = LazyInOutSequenceImport(
        modulename="hydpy.models.meteo.meteo_factors",
        classname="SolarDeclination",
        alias="meteo_factors_SolarDeclination",
        namespace=locals(),
    )
    meteo_factors_SunsetHourAngle = LazyInOutSequenceImport(
        modulename="hydpy.models.meteo.meteo_factors",
        classname="SunsetHourAngle",
        alias="meteo_factors_SunsetHourAngle",
        namespace=locals(),
    )
    meteo_factors_SolarTimeAngle = LazyInOutSequenceImport(
        modulename="hydpy.models.meteo.meteo_factors",
        classname="SolarTimeAngle",
        alias="meteo_factors_SolarTimeAngle",
        namespace=locals(),
    )
    meteo_factors_TimeOfSunrise = LazyInOutSequenceImport(
        modulename="hydpy.models.meteo.meteo_factors",
        classname="TimeOfSunrise",
        alias="meteo_factors_TimeOfSunrise",
        namespace=locals(),
    )
    meteo_factors_TimeOfSunset = LazyInOutSequenceImport(
        modulename="hydpy.models.meteo.meteo_factors",
        classname="TimeOfSunset",
        alias="meteo_factors_TimeOfSunset",
        namespace=locals(),
    )
    meteo_factors_PossibleSunshineDuration = LazyInOutSequenceImport(
        modulename="hydpy.models.meteo.meteo_factors",
        classname="PossibleSunshineDuration",
        alias="meteo_factors_PossibleSunshineDuration",
        namespace=locals(),
    )
    meteo_factors_DailyPossibleSunshineDuration = LazyInOutSequenceImport(
        modulename="hydpy.models.meteo.meteo_factors",
        classname="DailyPossibleSunshineDuration",
        alias="meteo_factors_DailyPossibleSunshineDuration",
        namespace=locals(),
    )
    meteo_factors_UnadjustedSunshineDuration = LazyInOutSequenceImport(
        modulename="hydpy.models.meteo.meteo_factors",
        classname="UnadjustedSunshineDuration",
        alias="meteo_factors_UnadjustedSunshineDuration",
        namespace=locals(),
    )
    meteo_factors_SunshineDuration = LazyInOutSequenceImport(
        modulename="hydpy.models.meteo.meteo_factors",
        classname="SunshineDuration",
        alias="meteo_factors_SunshineDuration",
        namespace=locals(),
    )
    meteo_factors_DailySunshineDuration = LazyInOutSequenceImport(
        modulename="hydpy.models.meteo.meteo_factors",
        classname="DailySunshineDuration",
        alias="meteo_factors_DailySunshineDuration",
        namespace=locals(),
    )
    meteo_factors_PortionDailyRadiation = LazyInOutSequenceImport(
        modulename="hydpy.models.meteo.meteo_factors",
        classname="PortionDailyRadiation",
        alias="meteo_factors_PortionDailyRadiation",
        namespace=locals(),
    )
    meteo_factors_MeanTemperature = LazyInOutSequenceImport(
        modulename="hydpy.models.meteo.meteo_factors",
        classname="MeanTemperature",
        alias="meteo_factors_MeanTemperature",
        namespace=locals(),
    )
    meteo_fluxes_ExtraterrestrialRadiation = LazyInOutSequenceImport(
        modulename="hydpy.models.meteo.meteo_fluxes",
        classname="ExtraterrestrialRadiation",
        alias="meteo_fluxes_ExtraterrestrialRadiation",
        namespace=locals(),
    )
    meteo_fluxes_ClearSkySolarRadiation = LazyInOutSequenceImport(
        modulename="hydpy.models.meteo.meteo_fluxes",
        classname="ClearSkySolarRadiation",
        alias="meteo_fluxes_ClearSkySolarRadiation",
        namespace=locals(),
    )
    meteo_fluxes_UnadjustedGlobalRadiation = LazyInOutSequenceImport(
        modulename="hydpy.models.meteo.meteo_fluxes",
        classname="UnadjustedGlobalRadiation",
        alias="meteo_fluxes_UnadjustedGlobalRadiation",
        namespace=locals(),
    )
    meteo_fluxes_DailyGlobalRadiation = LazyInOutSequenceImport(
        modulename="hydpy.models.meteo.meteo_fluxes",
        classname="DailyGlobalRadiation",
        alias="meteo_fluxes_DailyGlobalRadiation",
        namespace=locals(),
    )
    meteo_fluxes_GlobalRadiation = LazyInOutSequenceImport(
        modulename="hydpy.models.meteo.meteo_fluxes",
        classname="GlobalRadiation",
        alias="meteo_fluxes_GlobalRadiation",
        namespace=locals(),
    )
    meteo_fluxes_MeanPrecipitation = LazyInOutSequenceImport(
        modulename="hydpy.models.meteo.meteo_fluxes",
        classname="MeanPrecipitation",
        alias="meteo_fluxes_MeanPrecipitation",
        namespace=locals(),
    )
    musk_inlets_Q = LazyInOutSequenceImport(
        modulename="hydpy.models.musk.musk_inlets",
        classname="Q",
        alias="musk_inlets_Q",
        namespace=locals(),
    )
    musk_fluxes_Inflow = LazyInOutSequenceImport(
        modulename="hydpy.models.musk.musk_fluxes",
        classname="Inflow",
        alias="musk_fluxes_Inflow",
        namespace=locals(),
    )
    musk_fluxes_Outflow = LazyInOutSequenceImport(
        modulename="hydpy.models.musk.musk_fluxes",
        classname="Outflow",
        alias="musk_fluxes_Outflow",
        namespace=locals(),
    )
    musk_outlets_Q = LazyInOutSequenceImport(
        modulename="hydpy.models.musk.musk_outlets",
        classname="Q",
        alias="musk_outlets_Q",
        namespace=locals(),
    )
    rconc_fluxes_Inflow = LazyInOutSequenceImport(
        modulename="hydpy.models.rconc.rconc_fluxes",
        classname="Inflow",
        alias="rconc_fluxes_Inflow",
        namespace=locals(),
    )
    rconc_fluxes_Outflow = LazyInOutSequenceImport(
        modulename="hydpy.models.rconc.rconc_fluxes",
        classname="Outflow",
        alias="rconc_fluxes_Outflow",
        namespace=locals(),
    )
    sw1d_inlets_LongQ = LazyInOutSequenceImport(
        modulename="hydpy.models.sw1d.sw1d_inlets",
        classname="LongQ",
        alias="sw1d_inlets_LongQ",
        namespace=locals(),
    )
    sw1d_inlets_LatQ = LazyInOutSequenceImport(
        modulename="hydpy.models.sw1d.sw1d_inlets",
        classname="LatQ",
        alias="sw1d_inlets_LatQ",
        namespace=locals(),
    )
    sw1d_inlets_WaterLevel = LazyInOutSequenceImport(
        modulename="hydpy.models.sw1d.sw1d_inlets",
        classname="WaterLevel",
        alias="sw1d_inlets_WaterLevel",
        namespace=locals(),
    )
    sw1d_factors_MaxTimeStep = LazyInOutSequenceImport(
        modulename="hydpy.models.sw1d.sw1d_factors",
        classname="MaxTimeStep",
        alias="sw1d_factors_MaxTimeStep",
        namespace=locals(),
    )
    sw1d_factors_TimeStep = LazyInOutSequenceImport(
        modulename="hydpy.models.sw1d.sw1d_factors",
        classname="TimeStep",
        alias="sw1d_factors_TimeStep",
        namespace=locals(),
    )
    sw1d_factors_WaterDepth = LazyInOutSequenceImport(
        modulename="hydpy.models.sw1d.sw1d_factors",
        classname="WaterDepth",
        alias="sw1d_factors_WaterDepth",
        namespace=locals(),
    )
    sw1d_factors_WaterLevel = LazyInOutSequenceImport(
        modulename="hydpy.models.sw1d.sw1d_factors",
        classname="WaterLevel",
        alias="sw1d_factors_WaterLevel",
        namespace=locals(),
    )
    sw1d_factors_WaterLevelUpstream = LazyInOutSequenceImport(
        modulename="hydpy.models.sw1d.sw1d_factors",
        classname="WaterLevelUpstream",
        alias="sw1d_factors_WaterLevelUpstream",
        namespace=locals(),
    )
    sw1d_factors_WaterLevelDownstream = LazyInOutSequenceImport(
        modulename="hydpy.models.sw1d.sw1d_factors",
        classname="WaterLevelDownstream",
        alias="sw1d_factors_WaterLevelDownstream",
        namespace=locals(),
    )
    sw1d_factors_WaterVolumeUpstream = LazyInOutSequenceImport(
        modulename="hydpy.models.sw1d.sw1d_factors",
        classname="WaterVolumeUpstream",
        alias="sw1d_factors_WaterVolumeUpstream",
        namespace=locals(),
    )
    sw1d_factors_WaterVolumeDownstream = LazyInOutSequenceImport(
        modulename="hydpy.models.sw1d.sw1d_factors",
        classname="WaterVolumeDownstream",
        alias="sw1d_factors_WaterVolumeDownstream",
        namespace=locals(),
    )
    sw1d_factors_WettedArea = LazyInOutSequenceImport(
        modulename="hydpy.models.sw1d.sw1d_factors",
        classname="WettedArea",
        alias="sw1d_factors_WettedArea",
        namespace=locals(),
    )
    sw1d_factors_WettedPerimeter = LazyInOutSequenceImport(
        modulename="hydpy.models.sw1d.sw1d_factors",
        classname="WettedPerimeter",
        alias="sw1d_factors_WettedPerimeter",
        namespace=locals(),
    )
    sw1d_fluxes_Inflow = LazyInOutSequenceImport(
        modulename="hydpy.models.sw1d.sw1d_fluxes",
        classname="Inflow",
        alias="sw1d_fluxes_Inflow",
        namespace=locals(),
    )
    sw1d_fluxes_Outflow = LazyInOutSequenceImport(
        modulename="hydpy.models.sw1d.sw1d_fluxes",
        classname="Outflow",
        alias="sw1d_fluxes_Outflow",
        namespace=locals(),
    )
    sw1d_fluxes_LateralFlow = LazyInOutSequenceImport(
        modulename="hydpy.models.sw1d.sw1d_fluxes",
        classname="LateralFlow",
        alias="sw1d_fluxes_LateralFlow",
        namespace=locals(),
    )
    sw1d_fluxes_NetInflow = LazyInOutSequenceImport(
        modulename="hydpy.models.sw1d.sw1d_fluxes",
        classname="NetInflow",
        alias="sw1d_fluxes_NetInflow",
        namespace=locals(),
    )
    sw1d_fluxes_DischargeUpstream = LazyInOutSequenceImport(
        modulename="hydpy.models.sw1d.sw1d_fluxes",
        classname="DischargeUpstream",
        alias="sw1d_fluxes_DischargeUpstream",
        namespace=locals(),
    )
    sw1d_fluxes_DischargeDownstream = LazyInOutSequenceImport(
        modulename="hydpy.models.sw1d.sw1d_fluxes",
        classname="DischargeDownstream",
        alias="sw1d_fluxes_DischargeDownstream",
        namespace=locals(),
    )
    sw1d_fluxes_DischargeVolume = LazyInOutSequenceImport(
        modulename="hydpy.models.sw1d.sw1d_fluxes",
        classname="DischargeVolume",
        alias="sw1d_fluxes_DischargeVolume",
        namespace=locals(),
    )
    sw1d_states_WaterVolume = LazyInOutSequenceImport(
        modulename="hydpy.models.sw1d.sw1d_states",
        classname="WaterVolume",
        alias="sw1d_states_WaterVolume",
        namespace=locals(),
    )
    sw1d_states_Discharge = LazyInOutSequenceImport(
        modulename="hydpy.models.sw1d.sw1d_states",
        classname="Discharge",
        alias="sw1d_states_Discharge",
        namespace=locals(),
    )
    sw1d_outlets_LongQ = LazyInOutSequenceImport(
        modulename="hydpy.models.sw1d.sw1d_outlets",
        classname="LongQ",
        alias="sw1d_outlets_LongQ",
        namespace=locals(),
    )
    sw1d_senders_WaterLevel = LazyInOutSequenceImport(
        modulename="hydpy.models.sw1d.sw1d_senders",
        classname="WaterLevel",
        alias="sw1d_senders_WaterLevel",
        namespace=locals(),
    )
    test_fluxes_Q = LazyInOutSequenceImport(
        modulename="hydpy.models.test.test_fluxes",
        classname="Q",
        alias="test_fluxes_Q",
        namespace=locals(),
    )
    test_states_S = LazyInOutSequenceImport(
        modulename="hydpy.models.test.test_states",
        classname="S",
        alias="test_states_S",
        namespace=locals(),
    )
    whmod_inputs_Precipitation = LazyInOutSequenceImport(
        modulename="hydpy.models.whmod.whmod_inputs",
        classname="Precipitation",
        alias="whmod_inputs_Precipitation",
        namespace=locals(),
    )
    whmod_inputs_Temperature = LazyInOutSequenceImport(
        modulename="hydpy.models.whmod.whmod_inputs",
        classname="Temperature",
        alias="whmod_inputs_Temperature",
        namespace=locals(),
    )
    whmod_fluxes_CisternInflow = LazyInOutSequenceImport(
        modulename="hydpy.models.whmod.whmod_fluxes",
        classname="CisternInflow",
        alias="whmod_fluxes_CisternInflow",
        namespace=locals(),
    )
    whmod_fluxes_CisternOverflow = LazyInOutSequenceImport(
        modulename="hydpy.models.whmod.whmod_fluxes",
        classname="CisternOverflow",
        alias="whmod_fluxes_CisternOverflow",
        namespace=locals(),
    )
    whmod_fluxes_CisternDemand = LazyInOutSequenceImport(
        modulename="hydpy.models.whmod.whmod_fluxes",
        classname="CisternDemand",
        alias="whmod_fluxes_CisternDemand",
        namespace=locals(),
    )
    whmod_fluxes_CisternExtraction = LazyInOutSequenceImport(
        modulename="hydpy.models.whmod.whmod_fluxes",
        classname="CisternExtraction",
        alias="whmod_fluxes_CisternExtraction",
        namespace=locals(),
    )
    whmod_fluxes_ActualRecharge = LazyInOutSequenceImport(
        modulename="hydpy.models.whmod.whmod_fluxes",
        classname="ActualRecharge",
        alias="whmod_fluxes_ActualRecharge",
        namespace=locals(),
    )
    whmod_fluxes_DelayedRecharge = LazyInOutSequenceImport(
        modulename="hydpy.models.whmod.whmod_fluxes",
        classname="DelayedRecharge",
        alias="whmod_fluxes_DelayedRecharge",
        namespace=locals(),
    )
    whmod_states_CisternWater = LazyInOutSequenceImport(
        modulename="hydpy.models.whmod.whmod_states",
        classname="CisternWater",
        alias="whmod_states_CisternWater",
        namespace=locals(),
    )
    whmod_states_DeepWater = LazyInOutSequenceImport(
        modulename="hydpy.models.whmod.whmod_states",
        classname="DeepWater",
        alias="whmod_states_DeepWater",
        namespace=locals(),
    )
    wland_inputs_T = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_inputs",
        classname="T",
        alias="wland_inputs_T",
        namespace=locals(),
    )
    wland_inputs_P = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_inputs",
        classname="P",
        alias="wland_inputs_P",
        namespace=locals(),
    )
    wland_inputs_FXG = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_inputs",
        classname="FXG",
        alias="wland_inputs_FXG",
        namespace=locals(),
    )
    wland_inputs_FXS = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_inputs",
        classname="FXS",
        alias="wland_inputs_FXS",
        namespace=locals(),
    )
    wland_factors_DHS = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_factors",
        classname="DHS",
        alias="wland_factors_DHS",
        namespace=locals(),
    )
    wland_fluxes_PC = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="PC",
        alias="wland_fluxes_PC",
        namespace=locals(),
    )
    wland_fluxes_PS = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="PS",
        alias="wland_fluxes_PS",
        namespace=locals(),
    )
    wland_fluxes_PVE = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="PVE",
        alias="wland_fluxes_PVE",
        namespace=locals(),
    )
    wland_fluxes_PV = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="PV",
        alias="wland_fluxes_PV",
        namespace=locals(),
    )
    wland_fluxes_PQ = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="PQ",
        alias="wland_fluxes_PQ",
        namespace=locals(),
    )
    wland_fluxes_ETVE = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="ETVE",
        alias="wland_fluxes_ETVE",
        namespace=locals(),
    )
    wland_fluxes_ETV = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="ETV",
        alias="wland_fluxes_ETV",
        namespace=locals(),
    )
    wland_fluxes_ES = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="ES",
        alias="wland_fluxes_ES",
        namespace=locals(),
    )
    wland_fluxes_ET = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="ET",
        alias="wland_fluxes_ET",
        namespace=locals(),
    )
    wland_fluxes_GR = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="GR",
        alias="wland_fluxes_GR",
        namespace=locals(),
    )
    wland_fluxes_FXS = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="FXS",
        alias="wland_fluxes_FXS",
        namespace=locals(),
    )
    wland_fluxes_FXG = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="FXG",
        alias="wland_fluxes_FXG",
        namespace=locals(),
    )
    wland_fluxes_CDG = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="CDG",
        alias="wland_fluxes_CDG",
        namespace=locals(),
    )
    wland_fluxes_FGSE = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="FGSE",
        alias="wland_fluxes_FGSE",
        namespace=locals(),
    )
    wland_fluxes_FGS = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="FGS",
        alias="wland_fluxes_FGS",
        namespace=locals(),
    )
    wland_fluxes_FQS = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="FQS",
        alias="wland_fluxes_FQS",
        namespace=locals(),
    )
    wland_fluxes_RH = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="RH",
        alias="wland_fluxes_RH",
        namespace=locals(),
    )
    wland_fluxes_R = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_fluxes",
        classname="R",
        alias="wland_fluxes_R",
        namespace=locals(),
    )
    wland_states_DVE = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_states",
        classname="DVE",
        alias="wland_states_DVE",
        namespace=locals(),
    )
    wland_states_DV = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_states",
        classname="DV",
        alias="wland_states_DV",
        namespace=locals(),
    )
    wland_states_HGE = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_states",
        classname="HGE",
        alias="wland_states_HGE",
        namespace=locals(),
    )
    wland_states_DG = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_states",
        classname="DG",
        alias="wland_states_DG",
        namespace=locals(),
    )
    wland_states_HQ = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_states",
        classname="HQ",
        alias="wland_states_HQ",
        namespace=locals(),
    )
    wland_states_HS = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_states",
        classname="HS",
        alias="wland_states_HS",
        namespace=locals(),
    )
    wland_outlets_Q = LazyInOutSequenceImport(
        modulename="hydpy.models.wland.wland_outlets",
        classname="Q",
        alias="wland_outlets_Q",
        namespace=locals(),
    )
    wq_factors_WaterDepth = LazyInOutSequenceImport(
        modulename="hydpy.models.wq.wq_factors",
        classname="WaterDepth",
        alias="wq_factors_WaterDepth",
        namespace=locals(),
    )
    wq_factors_WaterLevel = LazyInOutSequenceImport(
        modulename="hydpy.models.wq.wq_factors",
        classname="WaterLevel",
        alias="wq_factors_WaterLevel",
        namespace=locals(),
    )
    wq_factors_WettedArea = LazyInOutSequenceImport(
        modulename="hydpy.models.wq.wq_factors",
        classname="WettedArea",
        alias="wq_factors_WettedArea",
        namespace=locals(),
    )
    wq_factors_WettedPerimeter = LazyInOutSequenceImport(
        modulename="hydpy.models.wq.wq_factors",
        classname="WettedPerimeter",
        alias="wq_factors_WettedPerimeter",
        namespace=locals(),
    )
    wq_factors_SurfaceWidth = LazyInOutSequenceImport(
        modulename="hydpy.models.wq.wq_factors",
        classname="SurfaceWidth",
        alias="wq_factors_SurfaceWidth",
        namespace=locals(),
    )
    wq_factors_DischargeDerivative = LazyInOutSequenceImport(
        modulename="hydpy.models.wq.wq_factors",
        classname="DischargeDerivative",
        alias="wq_factors_DischargeDerivative",
        namespace=locals(),
    )
    wq_factors_Celerity = LazyInOutSequenceImport(
        modulename="hydpy.models.wq.wq_factors",
        classname="Celerity",
        alias="wq_factors_Celerity",
        namespace=locals(),
    )
    wq_fluxes_Discharge = LazyInOutSequenceImport(
        modulename="hydpy.models.wq.wq_fluxes",
        classname="Discharge",
        alias="wq_fluxes_Discharge",
        namespace=locals(),
    )

__all__ = [
    "arma_inlets_Q",
    "arma_fluxes_QIn",
    "arma_fluxes_QOut",
    "arma_outlets_Q",
    "conv_inlets_Inputs",
    "conv_fluxes_ActualConstant",
    "conv_fluxes_ActualFactor",
    "conv_outlets_Outputs",
    "dam_inlets_Q",
    "dam_inlets_S",
    "dam_inlets_R",
    "dam_inlets_E",
    "dam_receivers_Q",
    "dam_receivers_D",
    "dam_receivers_S",
    "dam_receivers_R",
    "dam_receivers_OWL",
    "dam_receivers_RWL",
    "dam_factors_WaterLevel",
    "dam_factors_OuterWaterLevel",
    "dam_factors_RemoteWaterLevel",
    "dam_factors_WaterLevelDifference",
    "dam_factors_EffectiveWaterLevelDifference",
    "dam_fluxes_Precipitation",
    "dam_fluxes_AdjustedPrecipitation",
    "dam_fluxes_PotentialEvaporation",
    "dam_fluxes_AdjustedEvaporation",
    "dam_fluxes_ActualEvaporation",
    "dam_fluxes_Inflow",
    "dam_fluxes_Exchange",
    "dam_fluxes_TotalRemoteDischarge",
    "dam_fluxes_NaturalRemoteDischarge",
    "dam_fluxes_RemoteDemand",
    "dam_fluxes_RemoteFailure",
    "dam_fluxes_RequiredRemoteRelease",
    "dam_fluxes_AllowedRemoteRelief",
    "dam_fluxes_RequiredRemoteSupply",
    "dam_fluxes_PossibleRemoteRelief",
    "dam_fluxes_ActualRemoteRelief",
    "dam_fluxes_RequiredRelease",
    "dam_fluxes_TargetedRelease",
    "dam_fluxes_ActualRelease",
    "dam_fluxes_MissingRemoteRelease",
    "dam_fluxes_ActualRemoteRelease",
    "dam_fluxes_FloodDischarge",
    "dam_fluxes_FreeDischarge",
    "dam_fluxes_MaxForcedDischarge",
    "dam_fluxes_MaxFreeDischarge",
    "dam_fluxes_ForcedDischarge",
    "dam_fluxes_Outflow",
    "dam_states_WaterVolume",
    "dam_outlets_Q",
    "dam_outlets_S",
    "dam_outlets_R",
    "dam_senders_D",
    "dam_senders_S",
    "dam_senders_R",
    "dummy_inlets_Q",
    "dummy_fluxes_Q",
    "dummy_outlets_Q",
    "evap_inputs_ReferenceEvapotranspiration",
    "evap_inputs_RelativeHumidity",
    "evap_inputs_WindSpeed",
    "evap_inputs_AtmosphericPressure",
    "evap_inputs_NormalAirTemperature",
    "evap_inputs_NormalEvapotranspiration",
    "evap_factors_MeanAirTemperature",
    "evap_factors_WindSpeed2m",
    "evap_factors_DailyWindSpeed2m",
    "evap_factors_WindSpeed10m",
    "evap_factors_DailyRelativeHumidity",
    "evap_factors_SunshineDuration",
    "evap_factors_PossibleSunshineDuration",
    "evap_factors_DailySunshineDuration",
    "evap_factors_DailyPossibleSunshineDuration",
    "evap_factors_PsychrometricConstant",
    "evap_factors_AdjustedCloudCoverage",
    "evap_fluxes_GlobalRadiation",
    "evap_fluxes_ClearSkySolarRadiation",
    "evap_fluxes_DailyGlobalRadiation",
    "evap_fluxes_MeanReferenceEvapotranspiration",
    "evap_fluxes_MeanPotentialEvapotranspiration",
    "evap_states_CloudCoverage",
    "exch_inlets_Total",
    "exch_receivers_WaterLevel",
    "exch_receivers_WaterLevels",
    "exch_factors_DeltaWaterLevel",
    "exch_fluxes_PotentialExchange",
    "exch_fluxes_ActualExchange",
    "exch_fluxes_OriginalInput",
    "exch_fluxes_AdjustedInput",
    "exch_outlets_Exchange",
    "exch_outlets_Branched",
    "ga_inputs_Rainfall",
    "ga_inputs_CapillaryRise",
    "ga_inputs_Evaporation",
    "ga_fluxes_TotalInfiltration",
    "ga_fluxes_TotalPercolation",
    "ga_fluxes_TotalSoilWaterAddition",
    "ga_fluxes_TotalWithdrawal",
    "ga_fluxes_TotalSurfaceRunoff",
    "gland_inputs_P",
    "gland_fluxes_E",
    "gland_fluxes_EN",
    "gland_fluxes_PN",
    "gland_fluxes_PS",
    "gland_fluxes_EI",
    "gland_fluxes_ES",
    "gland_fluxes_AE",
    "gland_fluxes_PR",
    "gland_fluxes_PR9",
    "gland_fluxes_PR1",
    "gland_fluxes_Q10",
    "gland_fluxes_Perc",
    "gland_fluxes_Q9",
    "gland_fluxes_Q1",
    "gland_fluxes_FD",
    "gland_fluxes_FR",
    "gland_fluxes_FR2",
    "gland_fluxes_QR",
    "gland_fluxes_QR2",
    "gland_fluxes_QD",
    "gland_fluxes_QH",
    "gland_fluxes_QV",
    "gland_states_I",
    "gland_states_S",
    "gland_states_R",
    "gland_states_R2",
    "gland_outlets_Q",
    "hland_inputs_P",
    "hland_inputs_T",
    "hland_factors_ContriArea",
    "hland_fluxes_InUZ",
    "hland_fluxes_Perc",
    "hland_fluxes_Q0",
    "hland_fluxes_Q1",
    "hland_fluxes_GR2",
    "hland_fluxes_RG2",
    "hland_fluxes_GR3",
    "hland_fluxes_RG3",
    "hland_fluxes_InRC",
    "hland_fluxes_OutRC",
    "hland_fluxes_RO",
    "hland_fluxes_RA",
    "hland_fluxes_RT",
    "hland_fluxes_QT",
    "hland_states_UZ",
    "hland_states_LZ",
    "hland_states_SG2",
    "hland_states_SG3",
    "hland_outlets_Q",
    "kinw_inlets_Q",
    "kinw_fluxes_QZ",
    "kinw_fluxes_QZA",
    "kinw_fluxes_QA",
    "kinw_outlets_Q",
    "lland_inputs_Nied",
    "lland_inputs_TemL",
    "lland_inputs_RelativeHumidity",
    "lland_inputs_WindSpeed",
    "lland_inlets_Q",
    "lland_factors_PossibleSunshineDuration",
    "lland_factors_SunshineDuration",
    "lland_fluxes_QZ",
    "lland_fluxes_QZH",
    "lland_fluxes_DailySunshineDuration",
    "lland_fluxes_DailyPossibleSunshineDuration",
    "lland_fluxes_GlobalRadiation",
    "lland_fluxes_WindSpeed2m",
    "lland_fluxes_QDGZ",
    "lland_fluxes_QDGZ1",
    "lland_fluxes_QDGZ2",
    "lland_fluxes_QIGZ1",
    "lland_fluxes_QIGZ2",
    "lland_fluxes_QBGZ",
    "lland_fluxes_QDGA1",
    "lland_fluxes_QDGA2",
    "lland_fluxes_QIGA1",
    "lland_fluxes_QIGA2",
    "lland_fluxes_QBGA",
    "lland_fluxes_QAH",
    "lland_fluxes_QA",
    "lland_states_SDG1",
    "lland_states_SDG2",
    "lland_states_SIG1",
    "lland_states_SIG2",
    "lland_states_SBG",
    "lland_outlets_Q",
    "meteo_inputs_PossibleSunshineDuration",
    "meteo_inputs_SunshineDuration",
    "meteo_inputs_ClearSkySolarRadiation",
    "meteo_inputs_GlobalRadiation",
    "meteo_inputs_Temperature",
    "meteo_inputs_Precipitation",
    "meteo_factors_EarthSunDistance",
    "meteo_factors_SolarDeclination",
    "meteo_factors_SunsetHourAngle",
    "meteo_factors_SolarTimeAngle",
    "meteo_factors_TimeOfSunrise",
    "meteo_factors_TimeOfSunset",
    "meteo_factors_PossibleSunshineDuration",
    "meteo_factors_DailyPossibleSunshineDuration",
    "meteo_factors_UnadjustedSunshineDuration",
    "meteo_factors_SunshineDuration",
    "meteo_factors_DailySunshineDuration",
    "meteo_factors_PortionDailyRadiation",
    "meteo_factors_MeanTemperature",
    "meteo_fluxes_ExtraterrestrialRadiation",
    "meteo_fluxes_ClearSkySolarRadiation",
    "meteo_fluxes_UnadjustedGlobalRadiation",
    "meteo_fluxes_DailyGlobalRadiation",
    "meteo_fluxes_GlobalRadiation",
    "meteo_fluxes_MeanPrecipitation",
    "musk_inlets_Q",
    "musk_fluxes_Inflow",
    "musk_fluxes_Outflow",
    "musk_outlets_Q",
    "rconc_fluxes_Inflow",
    "rconc_fluxes_Outflow",
    "sw1d_inlets_LongQ",
    "sw1d_inlets_LatQ",
    "sw1d_inlets_WaterLevel",
    "sw1d_factors_MaxTimeStep",
    "sw1d_factors_TimeStep",
    "sw1d_factors_WaterDepth",
    "sw1d_factors_WaterLevel",
    "sw1d_factors_WaterLevelUpstream",
    "sw1d_factors_WaterLevelDownstream",
    "sw1d_factors_WaterVolumeUpstream",
    "sw1d_factors_WaterVolumeDownstream",
    "sw1d_factors_WettedArea",
    "sw1d_factors_WettedPerimeter",
    "sw1d_fluxes_Inflow",
    "sw1d_fluxes_Outflow",
    "sw1d_fluxes_LateralFlow",
    "sw1d_fluxes_NetInflow",
    "sw1d_fluxes_DischargeUpstream",
    "sw1d_fluxes_DischargeDownstream",
    "sw1d_fluxes_DischargeVolume",
    "sw1d_states_WaterVolume",
    "sw1d_states_Discharge",
    "sw1d_outlets_LongQ",
    "sw1d_senders_WaterLevel",
    "test_fluxes_Q",
    "test_states_S",
    "whmod_inputs_Precipitation",
    "whmod_inputs_Temperature",
    "whmod_fluxes_CisternInflow",
    "whmod_fluxes_CisternOverflow",
    "whmod_fluxes_CisternDemand",
    "whmod_fluxes_CisternExtraction",
    "whmod_fluxes_ActualRecharge",
    "whmod_fluxes_DelayedRecharge",
    "whmod_states_CisternWater",
    "whmod_states_DeepWater",
    "wland_inputs_T",
    "wland_inputs_P",
    "wland_inputs_FXG",
    "wland_inputs_FXS",
    "wland_factors_DHS",
    "wland_fluxes_PC",
    "wland_fluxes_PS",
    "wland_fluxes_PVE",
    "wland_fluxes_PV",
    "wland_fluxes_PQ",
    "wland_fluxes_ETVE",
    "wland_fluxes_ETV",
    "wland_fluxes_ES",
    "wland_fluxes_ET",
    "wland_fluxes_GR",
    "wland_fluxes_FXS",
    "wland_fluxes_FXG",
    "wland_fluxes_CDG",
    "wland_fluxes_FGSE",
    "wland_fluxes_FGS",
    "wland_fluxes_FQS",
    "wland_fluxes_RH",
    "wland_fluxes_R",
    "wland_states_DVE",
    "wland_states_DV",
    "wland_states_HGE",
    "wland_states_DG",
    "wland_states_HQ",
    "wland_states_HS",
    "wland_outlets_Q",
    "wq_factors_WaterDepth",
    "wq_factors_WaterLevel",
    "wq_factors_WettedArea",
    "wq_factors_WettedPerimeter",
    "wq_factors_SurfaceWidth",
    "wq_factors_DischargeDerivative",
    "wq_factors_Celerity",
    "wq_fluxes_Discharge",
]

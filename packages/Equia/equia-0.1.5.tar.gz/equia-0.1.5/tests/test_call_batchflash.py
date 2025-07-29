import pytest
from typing import Union
from equia.models import (
    CalculationComposition, ProblemDetails,
    BatchFlashCalculationInput, BatchFlashCalculationResult, 
)
from equia.equia_client import EquiaClient
from equia.demofluids.demofluid1_nHexane_Ethylene_HDPE7 import demofluid1_nHexane_Ethylene_HDPE7
from equia.models.batchflash_calculation_item import BatchFlashCalculationItem
from utility.api_access import ApiAccess

@pytest.mark.asyncio
async def test_call_batchflash():
    client = EquiaClient(ApiAccess.url, ApiAccess.access_key)

    input: BatchFlashCalculationInput = client.get_batchflash_input()
    input.flashtype = "FixedTemperaturePressure"

    input.fluid = demofluid1_nHexane_Ethylene_HDPE7()
    input.units = "C(In,Massfraction);C(Out,Massfraction);T(In,Kelvin);T(Out,Kelvin);P(In,Bar);P(Out,Bar);H(In,kJ/Kg);H(Out,kJ/Kg);S(In,kJ/(Kg Kelvin));S(Out,kJ/(Kg Kelvin));Cp(In,kJ/(Kg Kelvin));Cp(Out,kJ/(Kg Kelvin));Viscosity(In,centiPoise);Viscosity(Out,centiPoise);Surfacetension(In,N/m);Surfacetension(Out,N/m)"

    item1 = BatchFlashCalculationItem()
    item1.temperature = 445
    item1.pressure = 20
    item1.components = [
        CalculationComposition(amount=0.78),
        CalculationComposition(amount=0.02),
        CalculationComposition(amount=0.20)
    ]

    input.points.append(item1)

    result: Union[BatchFlashCalculationResult, ProblemDetails] = await client.call_batchflash_async(input)

    await client.cleanup()

    #assert result.status == 400
    assert result.success is True
    assert len(result.points[0].phases) == 4

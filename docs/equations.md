# Mathematical Equations

## Environmental Factor

```
FFL = max(DistanceToCoastFactor, AltitudeFactor, TemperatureFactor, CorrosiveFactor, DustFactor)
```

## Load Factor

```
FEL = NormalLoad / MaximumPermissibleLoad
```

## Expected Asset Life

```
ExpectedLife = DesignLife / (FFL * FEL)
```

## Aging Rate

```
beta = ln(HI_EOL / HI_NEW) / ExpectedLife
HI_NEW = 0.5,  HI_EOL = 5.5
```

## Base Health Index

```
HI(t) = 0.5 * exp(beta * age)
```

## Health Modifiers

```
HM = sum(weight_i * input_i)
RM = sum(weight_i * input_i)
```

## Asset Health Index

```
AHI = HI * exp(HM + RM)
```

## Probability of Failure

```
H = max(4, AHI)
PoF = K * (1 + C*H + (C*H)^2/2 + (C*H)^3/6)
```

## Expenditure

```
OpEx = PoF * CorrectiveMaintenanceCost + PreventiveMaintenanceCost
CapEx = MajorMaintenanceTrigger * MajorMaintenanceCost
TotEx = AccumulatedOpEx + AccumulatedCapEx
```

## Future Health Index

```
beta_corrected = ln(CurrentAHI / 0.5) / CurrentAge
FHI = 0.5 * exp(beta_corrected * future_age)
```

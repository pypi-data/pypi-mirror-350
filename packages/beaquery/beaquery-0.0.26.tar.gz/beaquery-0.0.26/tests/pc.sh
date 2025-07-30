
#! /bin/sh
set -ex

/bin/rm -f /tmp/*.csv

python -mpdb beanipa.py --TableName T20100 --Frequency A --Year X --csvfn /tmp/NIPAT20100.csv

if [ ! -f /tmp/NIPAT20100.csv ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaniud.py --TableName U20406  --Frequency A --Year X \
       --csvfn /tmp/NIUnderlyingDetailU20406.csv

if [ ! -f /tmp/NIUnderlyingDetailU20406.csv ]; then
    echo no file
    exit 1
fi

read nada


python -mpdb beamne.py --SeriesID 22,23,24,25,26,27 \
                          --DirectionOfInvestment inward \
                          --Classification CountryByIndustry \
                          --Country 308 --Industry 3000 --Year 2013,2012,2011,2010 \
                          --csvfn /tmp/MNESeriesID16.csv

if [ ! -f /tmp/MNESeriesID16.csv ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beamne.py --SeriesID all --DirectionOfInvestment outward \
                          --Classification Country \
                          --Country 308 --Industry 5221 --Year all \
                          --csvfn /tmp/MNEIndustry5221.csv

if [ ! -f /tmp/MNEIndustry5221.csv ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beafixedassets.py --TableName FAAt101 --Year X \
       --csvfn /tmp/FixedAssetsFAAt101.csv

if [ ! -f /tmp/FixedAssetsFAAt101.csv ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaita.py --Indicator BalCurrAcct --AreaOrCountry ALL --Frequency A
--Year ALL \
      --csvfn /tmp/ITABalCurrAcct.csv

if [ ! -f /tmp/ITABalCurrAcct.csv ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaiip.py --TypeOfService  CurrAndDepAssets --Component ALL --Frequency A
--Year ALL \
    --csvfn /tmp/IIPCurrAndDepAssets.csv

if [ ! -f /tmp/IIPCurrAndDepAssets.csv ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beainputoutput.py --TableID 57 --Year ALL \
       --csvfn /tmp/InputOutput57.csv

if [ ! -f /tmp/InputOutput57.csv ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaistrade.py --TypeOfService Engineering --TradeDirection ALL \
      --Affiliation ALL --AreaOrCountry ALL --Year ALL \
      --csvfn /tmp/IntlServTradeEngineering.csv

if [ ! -f /tmp/IntlServTradeEngineering.csv ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaissta.py --Channel Trade  --Destination ALL --Industry AllInd \
     --AreaOrCountry ALL --Year ALL --csvfn /tmp/IntlServSTATrade.csv

if [ ! -f /tmp/IntlServSTATrade.csv ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beagdpbyind.py --TableID 1 --Industry ALL --Frequency A --Year ALL \
    --csvfn /tmp/GDPbyIndustry1.csv

if [ ! -f /tmp/GDPbyIndustry1.csv ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb bearegional.py --TableName CAINC4 --GeoFip COUNTY \
    --LineCode 30 --Year ALL --csvfn /tmp/RegionalCAINC4.csv

if [ ! -f /tmp/RegionalCAINC4.csv ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaugdpbyind.py --TableID 210 --Industry ALL --Frequency A --Year ALL \
       --csvfn /tmp/UnderlyingGDPbyInѕustry210.csv

if [ ! -f /tmp/UnderlyingGDPbyInѕustry210.csv ]; then
    echo no file
    exit 1
fi





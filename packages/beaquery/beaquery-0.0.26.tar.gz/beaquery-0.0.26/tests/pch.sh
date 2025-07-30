#! /bin/sh
set -ex

/bin/rm -f /tmp/*.html

# cd ../src/beaquery

python -mpdb beanipa.py --TableName T20100 --Frequency A --Year X \
    --htmlfn /tmp/NIPAT20100.html

if [ ! -f /tmp/NIPAT20100.html ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaniud.py --TableName U20406  --Frequency A --Year X \
       --htmlfn /tmp/NIUnderlyingDetailU20406.html

if [ ! -f /tmp/NIUnderlyingDetailU20406.html ]; then
    echo no file
    exit 1
fi

read nada


python -mpdb beamne.py --SeriesID 22,23,24,25,26,27 \
              --DirectionOfInvestment inward \
              --Classification CountryByIndustry \
              --Country 308 --Industry 3000 --Year 2013,2012,2011,2010 \
              --htmlfn /tmp/MNESeriesID16.html

if [ ! -f /tmp/MNESeriesID16.html ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beamne.py --SeriesID all --DirectionOfInvestment outward \
                          --Classification Country \
                          --Country 308 --Industry 5221 --Year all \
                          --htmlfn /tmp/MNEIndustry5221.html

if [ ! -f /tmp/MNEIndustry5221.html ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beamne.py --SeriesID 16 --DirectionOfInvestment outward \
    --Classification Country --Country 308 \
       --Industry 5221 --Year all --htmlfn /tmp/MNESeriesID16.html

read nada

python -mpdb beafixedassets.py --TableName FAAt101 --Year X \
       --htmlfn /tmp/FixedAssetsFAAt101.html

if [ ! -f /tmp/FixedAssetsFAAt101.html ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaita.py --Indicator BalCurrAcct --AreaOrCountry ALL \
    --Frequency A --Year ALL --htmlfn /tmp/ITABalCurrAcct.html

if [ ! -f /tmp/ITABalCurrAcct.html ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaiip.py --TypeOfInvestment CurrAndDepAssets --Component ALL \
    --Frequency A --Year ALL --htmlfn /tmp/IIPCurrAndDepAssets.html

if [ ! -f /tmp/IIPCurrAndDepAssets.html ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beainputoutput.py --TableID 57 --Year ALL \
       --htmlfn /tmp/InputOutput57.html

if [ ! -f /tmp/InputOutput57.html ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaistrade.py --TypeOfService Engineering --TradeDirection ALL \
    --Affiliation ALL --AreaOrCountry ALL --Year ALL \
    --htmlfn /tmp/IntlServTradeEngineering.html

if [ ! -f /tmp/IntlServTradeEngineering.html ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaissta.py --Channel Trade  --Destination ALL --Industry AllInd \
    --AreaOrCountry ALL --Year ALL --htmlfn /tmp/IntlServSTATrade.html

if [ ! -f /tmp/IntlServSTATrade.html ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beagdpbyind.py --TableID 1 --Industry ALL --Frequency A \
    --Year ALL --htmlfn /tmp/GDPbyIndustry1.html

if [ ! -f /tmp/GDPbyIndustry1.html ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb bearegional.py --TableName CAINC4 --GeoFips COUNTY \
    --LineCode 30 --Year ALL --htmlfn /tmp/RegionalCAINC4.html

if [ ! -f /tmp/RegionalCAINC4.html ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaugdpbyind.py --TableID 210 --Industry ALL --Frequency A \
    --Year ALL --htmlfn /tmp/UnderlyingGDPbyInѕustry210.html

if [ ! -f /tmp/UnderlyingGDPbyInѕustry210.html ]; then
    echo no file
    exit 1
fi





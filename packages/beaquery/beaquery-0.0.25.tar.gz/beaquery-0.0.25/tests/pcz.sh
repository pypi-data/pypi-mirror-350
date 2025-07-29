#! /bin/sh
set -ex

TD='/tmp/BEA'
/bin/rm -rf ${TD}
mkdir ${TD}

python -mpdb beanipa.py --TableName T20100 --Frequency A --Year X \
    --csvzipfn ${TD}/NIPAT20100.zip

if [ ! -f ${TD}/NIPAT20100.zip ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaniud.py --TableName U20406  --Frequency A --Year X \
       --csvzipfn ${TD}/NIUnderlyingDetailU20406.zip

if [ ! -f ${TD}/NIUnderlyingDetailU20406.zip ]; then
    echo no file
    exit 1
fi

read nada


python -mpdb beamne.py --SeriesID 22,23,24,25,26,27 \
                          --DirectionOfInvestment inward \
                          --Classification CountryByIndustry \
                          --Country 308 --Industry 3000 \
                          --Year 2013,2012,2011,2010 \
                          --csvzipfn ${TD}/MNESeriesID16.zip

if [ ! -f ${TD}/MNESeriesID16.zip ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beamne.py --SeriesID all --DirectionOfInvestment outward \
                          --Classification Country \
                          --Country 308 --Industry 5221 --Year all \
                          --csvzipfn ${TD}/MNEIndustry5221.zip

if [ ! -f ${TD}/MNEIndustry5221.zip ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beafixedassets.py --TableName FAAt101 --Year X \
       --csvzipfn ${TD}/FixedAssetsFAAt101.zip

if [ ! -f ${TD}/FixedAssetsFAAt101.zip ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaita.py --Indicator BalCurrAcct --AreaOrCountry ALL \
    --Frequency A --Year ALL \
    --csvzipfn ${TD}/ITABalCurrAcct.zip

if [ ! -f ${TD}/ITABalCurrAcct.zip ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaiip.py --TypeOfInvestment  CurrAndDepAssets --Component ALL \
    --Frequency A --Year ALL \
    --csvzipfn ${TD}/IIPCurrAndDepAssets.zip

if [ ! -f ${TD}/IIPCurrAndDepAssets.zip ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beainputoutput.py --TableID 57 --Year ALL \
       --csvzipfn ${TD}/InputOutput57.zip

if [ ! -f ${TD}/InputOutput57.zip ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaistrade.py --TypeOfService Engineering --TradeDirection ALL \
      --Affiliation ALL --AreaOrCountry ALL --Year ALL \
      --csvzipfn ${TD}/IntlServTradeEngineering.zip

if [ ! -f ${TD}/IntlServTradeEngineering.zip ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaissta.py --Channel Trade  --Destination ALL --Industry AllInd \
     --AreaOrCountry ALL --Year ALL --csvzipfn ${TD}/IntlServSTATrade.zip

if [ ! -f ${TD}/IntlServSTATrade.zip ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beagdpbyind.py --TableID 1 --Industry ALL --Frequency A \
    --Year ALL  --csvzipfn ${TD}/GDPbyIndustry1.zip

if [ ! -f ${TD}/GDPbyIndustry1.zip ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb bearegional.py --TableName CAINC4 --GeoFip COUNTY \
    --LineCode 30 --Year ALL --csvzipfn ${TD}/RegionalCAINC4.zip

if [ ! -f ${TD}/RegionalCAINC4.zip ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaugdpbyind.py --TableID 210 --Industry ALL --Frequency A \
    --Year ALL --csvzipfn ${TD}/UnderlyingGDPbyInѕustry210.zip

if [ ! -f ${TD}/UnderlyingGDPbyInѕustry210.zip ]; then
    echo no file
    exit 1
fi





#! /bin/sh
set -ex

TD='/tmp/BEA'

rm -rf ${TD}
mkdir ${TD}

python -mpdb beaqueryq.py --DatasetName NIPA --TableName T20100 \
    --Frequency A  --Year X --csvzipfn ${TD}/NIPAT20100.zip

if [ ! -f ${TD}/NIPAT20100.zip ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaqueryq.py --DatasetName NIUnderlyingDetail --TableName U20406  \
    --Frequency A --Year X --csvzipfn ${TD}/NIUnderlyingDetailU20406.zip

if [ ! -f ${TD}/NIUnderlyingDetailU20406.zip ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaqueryq.py --DatasetName MNE --SeriesID 22,23,24,25,26,27 \
      --DirectionOfInvestment inward \
      --Classification CountryByIndustry \
      --Country 308 --Industry 3000 --Year 2013,2012,2011,2010 \
      --csvzipfn ${TD}/MNESeriesID16.zip

if [ ! -f ${TD}/MNESeriesID16.zip ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaqueryq.py --Dataset MNE --SeriesID all \
    --DirectionOfInvestment outward  --Classification Country \
    --Country 308 --Industry 5221 --Year all \
    --csvzipfn ${TD}/MNEIndustry5221.zip

if [ ! -f ${TD}/MNEIndustry5221.zip ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaqueryq.py --DatasetName FixedAssets --TableName FAAt101 \
    --Year X --csvzipfn ${TD}/FixedAssetsFAAt101.zip

if [ ! -f ${TD}/FixedAssetsFAAt101.zip ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaqueryq.py --DatasetName ITA --Indicator BalCurrAcct \
    --AreaOrCountry ALL --Frequency A --Year ALL \
      --csvzipfn ${TD}/ITABalCurrAcct.zip

if [ ! -f ${TD}/ITABalCurrAcct.zip ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaqueryq.py --DatasetName IIP \
    --TypeOfInvestment CurrAndDepAssets --Component ALL \
    --Frequency A --Year ALL \
    --csvzipfn ${TD}/IIPCurrAndDepAssets.zip

if [ ! -f ${TD}/IIPCurrAndDepAssets.zip ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaqueryq.py --DatasetName InputOutput --TableID 57 \
    --Year ALL --csvzipfn ${TD}/InputOutput57.zip

if [ ! -f ${TD}/InputOutput57.zip ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaqueryq.py --DatasetName IntlServTrade \
    --TypeOfService Engineering --TradeDirection ALL \
    --Affiliation ALL --AreaOrCountry ALL --Year ALL \
    --csvzipfn ${TD}/IntlServTradeEngineering.zip

if [ ! -f ${TD}/IntlServTradeEngineering.zip ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaqueryq.py --DatasetName IntlServSTA --Channel Trade  \
    --Destination ALL --Industry AllInd  --AreaOrCountry ALL \
    --Year ALL --csvzipfn ${TD}/IntlServSTATrade.zip

if [ ! -f ${TD}/IntlServSTATrade.zip ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaqueryq.py --DatasetName GDPbyIndustry --TableID 1 \
    --Industry ALL --Frequency A --Year ALL \
    --csvzipfn ${TD}/GDPbyIndustry1.zip

if [ ! -f ${TD}/GDPbyIndustry1.zip ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaqueryq.py --DatasetName Regional --TableName CAINC4 \
    --GeoFips COUNTY  --LineCode 30 --Year ALL \
    --csvzipfn ${TD}/RegionalCAINC4.zip

if [ ! -f ${TD}/RegionalCAINC4.zip ]; then
    echo no file
    exit 1
fi

read nada

python -mpdb beaqueryq.py --DatasetName UnderlyingGDPbyIndustry \
    --TableID 210 --Industry ALL --Frequency A --Year ALL \
    --csvzipfn ${TD}/UnderlyingGDPbyInѕustry210.zip

if [ ! -f ${TD}/UnderlyingGDPbyInѕustry210.zip ]; then
    echo no file
    exit 1
fi





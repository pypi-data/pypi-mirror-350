#! /bin/sh
set -ex

/bin/rm -f /tmp/*.csv

beanipa --TableName T20100 --Frequency A --Year X --csvfn /tmp/NIPAT20100.csv

read nada

beaniud --TableName U20406 --Frequency A --Year X --csvfn /tmp/NIUnderlyingDetailU20406.csv

read nada

beamne --SeriesID 16 --DirectionOfInvestment outward --Classification
Country --Country 308 --Industry 5221 \
       --Year all --csvfn /tmp/MNESeriesID16.csv

read nada

beamne --SeriesID all --DirectionOfInvestment outward --Classification
Country --Country 308 --Industry 5221 \
       --Year all --csvfn /tmp/MNEIndustry5221.csv

read nada

beafixedassets --TableName FAAt101 --Year X --csvfn /tmp/FixedAssetsFAAt101.csv

read nada

beaita  --Indicator BalCurrAcct --AreaOrCountry ALL --Frequency A --Year ALL \
        --csvfn /tmp/ITABalCurrAcct.csv

read nada

beaiip --TypeOfInvestment CurrAndDepAssets --Component ALL --Frequency A --Year ALL \
       --csvfn /tmp/IIPCurrAndDepAssets.csv

read nada

beainputoutput --TableID 57 --Year ALL --csvfn /tmp/InputOutput57.csv

read nada

beaistrade --TypeOfService Engineering --TradeDirection ALL --Affiliation ALL
--AreaOrCountry ALL --Year ALL \
           --csvfn /tmp/IntlServTradeEngineering.csv

read nada

beaissta --Channel Trade --Destination ALL --Industry AllInd --AreaOrCountry ALL --Year ALL \
         --csvfn /tmp/IntlServSTATrade.csv

read nada

beagdpbyind --TableID 1 --Industry ALL --Frequency A --Year ALL \
            --csvfn /tmp/GDPbyIndustry1.csv

read nada

bearegional --TableName CAINC4 --GeoFipe COUNTY --LineCode  30 --Year ALL \
            --csvfn /tmp/RegionalCAINC4.csv

read nada

beaugdpbyind --TableID 210 --Industry ALL --Frequency A --Year ALL \
             --csvfn /tmp/UnderlyingGDPbyInѕustry210.csv





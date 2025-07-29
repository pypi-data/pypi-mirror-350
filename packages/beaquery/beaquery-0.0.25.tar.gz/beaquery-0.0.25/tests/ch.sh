#! /bin/sh
set -ex

/bin/rm -f /tmp/*.html

beanipa -h

beanipa --TableName T20100 --Frequency A --Year X --htmlfn /tmp/NIPAT20100.html

read nada

beaniud -h

beaniud --TableName U20406 --Frequency A --Year X --htmlfn /tmp/NIUnderlyingDetailU20406.html

read nada

beamne -h

beamne --SeriesID 22,23,24,25,26,27 --DirectionOfInvestment inward \
       --Classification CountryByIndustry \
       --Country 308 --Industry 3000 --Year 2013,2012,2011,2010 \
                          --htmlfn /tmp/MNESeriesID16.html

read nada

beamne -h

beamne --SeriesID all --DirectionOfInvestment outward --Classification \
       Country --Country 308 --Industry 5221 \
       --Year all --htmlfn /tmp/MNEIndustry5221.html

read nada

beamne -h

beamne --SeriesID 16 --DirectionOfInvestment outward --Classification \
       Country --Country 308 --Industry 5221 \
       --Year all --htmlfn /tmp/MNESeriesID16.html

read nada

beafixedassets -h

beafixedassets --TableName FAAt101 --Year X --htmlfn /tmp/FixedAssetsFAAt101.html

read nada

beaita  -h

beaita  --Indicator BalCurrAcct --AreaOrCountry ALL --Frequency A --Year ALL \
        --htmlfn /tmp/ITABalCurrAcct.html

read nada

beaiip -h

beaiip --TypeOfInvestment CurrAndDepAssets --Component ALL --Frequency A --Year ALL \
       --htmlfn /tmp/IIPCurrAndDepAssets.html

read nada

beainputoutput -h

beainputoutput --TableID 57 --Year ALL --htmlfn /tmp/InputOutput57.html

read nada

beaistrade -h

beaistrade --TypeOfService Engineering --TradeDirection ALL \
           --Affiliation ALL --AreaOrCountry ALL --Year ALL \
           --htmlfn /tmp/IntlServTradeEngineering.html

read nada

beaissta -h

beaissta --Channel Trade --Destination ALL --Industry AllInd --AreaOrCountry ALL --Year ALL \
         --htmlfn /tmp/IntlServSTATrade.html

read nada

beagdpbyind -h

beagdpbyind --TableID 1 --Industry ALL --Frequency A --Year ALL \
            --htmlfn /tmp/GDPbyIndustry1.html

read nada

bearegional -h

bearegional --TableName CAINC4 --GeoFips COUNTY --LineCode 30 --Year ALL \
                    --htmlfn /tmp/RegionalCAINC4.html

read nada

beaugdpbyind -h

beaugdpbyind --TableID 210 --Industry ALL --Frequency A --Year ALL \
             --htmlfn /tmp/UnderlyingGDPbyInѕustry210.html





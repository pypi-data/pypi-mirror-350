# BEAquery

[![PyPI - Version](https://img.shields.io/pypi/v/beaquery.svg)](https://pypi.org/project/beaquery)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/beaquery.svg)](https://pypi.org/project/beaquery)

-----

## Table of Contents

BEA query is a set of commands to investigate, retrieve, or view
datasets provided by BEA. 

beaillustrated collects information about all of the BEA datasets, their
parameters, and parameter values. It then displays this information in
your browser

The remaining commands retrieve and either store data in CSV files or
display the data along with interactive plots in your browser.

beaqueryq can be used to do all that the commands above do.

I have changed the arguments to the commands to correspond with those
used by BEA.

- [Installation](#installation)
- [License](#license)

## Installation
pip install beaquery

## Usage

<br/>
##<br/>
## beaillustrated<br/>
##<br/>
usage: beaillustrated [-h] [--format {json,XML}] [--directory DIRECTORY]<br/>
<br/>
display BEA data model<br/>
<br/>
options:<br/>
-h, --help            show this help message and exit<br/>
--format {json,XML}   requested BEA result format(json)<br/>
--directory DIRECTORY<br/>
where to store the generated html<br/>
<br/>
<br/>
##<br/>
## beafixedassets<br/>
##<br/>
usage: beafixedassets [-h] --TableName TABLENAME --Year YEAR<br/>
[--format {json,XML}] [--csvfn CSVFN]<br/>
[--csvzipfn CSVZIPFN] [--splitkey SPLITKEY]<br/>
[--xkey XKEY] [--ykey YKEY] [--unitskey UNITSKEY]<br/>
[--htmlfn HTMLFN]<br/>
<br/>
get BEA FixedAssets data<br/>
<br/>
options:<br/>
-h, --help            show this help message and exit<br/>
--TableName TABLENAME<br/>
FixedAssets table name<br/>
--Year YEAR           year YYYY or X for all years<br/>
--format {json,XML}   result format(json)<br/>
--csvfn CSVFN         name of file to store dataset CSV result<br/>
--csvzipfn CSVZIPFN   name of zip file to store dataset CSV results<br/>
--splitkey SPLITKEY   table column name(LineDescription) to use to split the<br/>
plots<br/>
--xkey XKEY           table column name(TimePeriod) to use to plot the data<br/>
--ykey YKEY           table column name(DataValue) to use to plot the data<br/>
--unitskey UNITSKEY   table column name(METRIC_NAME) to use to label the<br/>
data<br/>
--htmlfn HTMLFN       name of file to store dataset HTML result<br/>
<br/>
<br/>
##<br/>
## beagdpbyind<br/>
##<br/>
usage: beagdpbyind [-h] --TableID TABLEID --Industry INDUSTRY --Frequency<br/>
FREQUENCY --Year YEAR [--format {json,XML}]<br/>
[--csvfn CSVFN] [--csvzipfn CSVZIPFN]<br/>
[--splitkey SPLITKEY] [--xkey XKEY] [--ykey YKEY]<br/>
[--unitskey UNITSKEY] [--htmlfn HTMLFN]<br/>
<br/>
get BEA GDPbyIndustry data<br/>
<br/>
options:<br/>
-h, --help            show this help message and exit<br/>
--TableID TABLEID     table id<br/>
--Industry INDUSTRY   industry<br/>
--Frequency FREQUENCY<br/>
frequency M, Q, A or comma separated list<br/>
--Year YEAR           year YYYY or ALL<br/>
--format {json,XML}   query result format(json)<br/>
--csvfn CSVFN         name of file to store dataset CSV result<br/>
--csvzipfn CSVZIPFN   name of zip file to store dataset CSV results<br/>
--splitkey SPLITKEY   table column name(IndustrYDescription) to use to split<br/>
the plots<br/>
--xkey XKEY           table column name(Year) to use to plot the data<br/>
--ykey YKEY           table column name(DataValue) to use to plot the data<br/>
--unitskey UNITSKEY   y key units(Billions?) to use to label the plotdata<br/>
--htmlfn HTMLFN       name of file to store dataset HTML result<br/>
<br/>
<br/>
##<br/>
## beaiip<br/>
##<br/>
usage: beaiip [-h] --TypeOfInvestment TYPEOFINVESTMENT --Component<br/>
COMPONENT --Frequency FREQUENCY --Year YEAR<br/>
[--format {json,XML}] [--csvfn CSVFN] [--csvzipfn CSVZIPFN]<br/>
[--splitkey SPLITKEY] [--xkey XKEY] [--ykey YKEY]<br/>
[--unitskey UNITSKEY] [--htmlfn HTMLFN]<br/>
<br/>
get BEA IIP data<br/>
<br/>
options:<br/>
-h, --help            show this help message and exit<br/>
--TypeOfInvestment TYPEOFINVESTMENT<br/>
type of investment<br/>
--Component COMPONENT<br/>
component of changes of position<br/>
--Frequency FREQUENCY<br/>
frequency M, Q, A or comma separated list<br/>
--Year YEAR           year YYYY or ALL<br/>
--format {json,XML}   result format(json)<br/>
--csvfn CSVFN         name of file to store dataset CSV result<br/>
--csvzipfn CSVZIPFN   name of zip file to store dataset CSV results<br/>
--splitkey SPLITKEY   table column name(Component) to use to split the plots<br/>
--xkey XKEY           table column name(TimePeriod) to use to plot the data<br/>
--ykey YKEY           table column name(DataValue) to use to plot the data<br/>
--unitskey UNITSKEY   table column name(CL_UNIT) to use to label the data<br/>
--htmlfn HTMLFN       name of file to store dataset HTML result<br/>
<br/>
<br/>
##<br/>
## beainputoutput<br/>
##<br/>
usage: beainputoutput [-h] --TableID TABLEID --Year YEAR<br/>
[--format {json,XML}] [--csvfn CSVFN]<br/>
[--csvzipfn CSVZIPFN] [--splitkey SPLITKEY]<br/>
[--xkey XKEY] [--ykey YKEY] [--unitskey UNITSKEY]<br/>
[--htmlfn HTMLFN]<br/>
<br/>
get BEA InputOutput data<br/>
<br/>
options:<br/>
-h, --help           show this help message and exit<br/>
--TableID TABLEID    table id<br/>
--Year YEAR          year YYYY or ALL<br/>
--format {json,XML}  request result format(json)<br/>
--csvfn CSVFN        name of file to store dataset CSV result<br/>
--csvzipfn CSVZIPFN  name of zip file to store dataset CSV results<br/>
--splitkey SPLITKEY  table column name(ColDescr) to use to split the plots<br/>
--xkey XKEY          table column name(Year) to use to plot the data<br/>
--ykey YKEY          table column name(DataValue) to use to plot the data<br/>
--unitskey UNITSKEY  table column name(ColType) to y label the plot<br/>
--htmlfn HTMLFN      name of file to store dataset HTML result<br/>
<br/>
<br/>
##<br/>
## beaissta<br/>
##<br/>
usage: beaissta [-h] --Channel CHANNEL --Destination DESTINATION --Industry<br/>
INDUSTRY --AreaOrCountry AREAORCOUNTRY --Year YEAR<br/>
[--format {json,XML}] [--csvfn CSVFN] [--csvzipfn CSVZIPFN]<br/>
[--splitkey SPLITKEY] [--xkey XKEY] [--ykey YKEY]<br/>
[--unitskey UNITSKEY] [--htmlfn HTMLFN]<br/>
<br/>
get BEA IntlServSTA data<br/>
<br/>
options:<br/>
-h, --help            show this help message and exit<br/>
--Channel CHANNEL     channel<br/>
--Destination DESTINATION<br/>
destination<br/>
--Industry INDUSTRY   industry<br/>
--AreaOrCountry AREAORCOUNTRY<br/>
area or country<br/>
--Year YEAR           year YYYY or ALL<br/>
--format {json,XML}   query result format(json)<br/>
--csvfn CSVFN         name of file to store dataset CSV result<br/>
--csvzipfn CSVZIPFN   name of zip file to store dataset CSV results<br/>
--splitkey SPLITKEY   table column name(TimeSeriesDescription) to use to<br/>
split the plots<br/>
--xkey XKEY           table column name(Year) to use to plot the data<br/>
--ykey YKEY           table column name(DataValue) to use to plot the data<br/>
--unitskey UNITSKEY   table column name(CL_UNIT) to y label the plot<br/>
--htmlfn HTMLFN       name of file to store dataset HTML result<br/>
<br/>
<br/>
##<br/>
## beaistrade<br/>
##<br/>
usage: beaistrade [-h] --TypeOfService TYPEOFSERVICE<br/>
[--TradeDirection TRADEDIRECTION]<br/>
[--Affiliation AFFILIATION]<br/>
[--AreaOrCountry AREAORCOUNTRY] --Year YEAR<br/>
[--format {json,XML}] [--csvfn CSVFN]<br/>
[--csvzipfn CSVZIPFN] [--splitkey SPLITKEY] [--xkey XKEY]<br/>
[--ykey YKEY] [--unitskey UNITSKEY] [--htmlfn HTMLFN]<br/>
<br/>
get BEA IntlServTrade data<br/>
<br/>
options:<br/>
-h, --help            show this help message and exit<br/>
--TypeOfService TYPEOFSERVICE<br/>
type of service<br/>
--TradeDirection TRADEDIRECTION<br/>
trade direction<br/>
--Affiliation AFFILIATION<br/>
affiliation<br/>
--AreaOrCountry AREAORCOUNTRY<br/>
area or country<br/>
--Year YEAR           year YYYY or ALL<br/>
--format {json,XML}   query result format(json)<br/>
--csvfn CSVFN         name of file to store dataset CSV result<br/>
--csvzipfn CSVZIPFN   name of zip file to store dataset CSV results<br/>
--splitkey SPLITKEY   table column name(TimeSeriesDescription) to use to<br/>
split the plots<br/>
--xkey XKEY           table column name(Year) to use to plot the data<br/>
--ykey YKEY           table column name(DataValue) to use to plot the data<br/>
--unitskey UNITSKEY   table column name(CL_UNIT) to use to label the data<br/>
--htmlfn HTMLFN       name of file to store dataset HTML result<br/>
<br/>
<br/>
##<br/>
## beaita<br/>
##<br/>
usage: beaita [-h] --Indicator INDICATOR --AreaOrCountry AREAORCOUNTRY<br/>
--Frequency FREQUENCY --Year YEAR [--format {json,XML}]<br/>
[--csvfn CSVFN] [--csvzipfn CSVZIPFN] [--splitkey SPLITKEY]<br/>
[--xkey XKEY] [--ykey YKEY] [--unitskey UNITSKEY]<br/>
[--htmlfn HTMLFN]<br/>
<br/>
get BEA ITA data<br/>
<br/>
options:<br/>
-h, --help            show this help message and exit<br/>
--Indicator INDICATOR<br/>
ITA indicator<br/>
--AreaOrCountry AREAORCOUNTRY<br/>
ITA area or country<br/>
--Frequency FREQUENCY<br/>
frequency M, Q, A or comma separated list<br/>
--Year YEAR           year YYYY or ALL<br/>
--format {json,XML}   query result format(json)<br/>
--csvfn CSVFN         name of file to store dataset CSV result<br/>
--csvzipfn CSVZIPFN   name of zip file to store dataset CSV results<br/>
--splitkey SPLITKEY   table column name(TimeSeriesDescription) to use to<br/>
split the plots<br/>
--xkey XKEY           table column name(Year) to use to plot the data<br/>
--ykey YKEY           table column name(DataValue) to use to plot the data<br/>
--unitskey UNITSKEY   table column name({'option_strings': ['--unitskey'],<br/>
'dest': 'unitskey', 'nargs': None, 'const': None,<br/>
'default': 'CL_UNIT', 'type': None, 'choices': None,<br/>
'required': False, 'help': 'table column name(%s) to y<br/>
label the plot', 'metavar': None, 'container':<br/>
<argparse._ArgumentGroup object at 0x1017ef860>,<br/>
'prog': 'beaita'}) to y label the plot<br/>
--htmlfn HTMLFN       name of file to store dataset HTML result<br/>
<br/>
<br/>
##<br/>
## beamne<br/>
##<br/>
usage: beamne [-h] [--SeriesID SERIESID] --DirectionOfInvestment<br/>
DIRECTIONOFINVESTMENT --Classification CLASSIFICATION<br/>
[--Country COUNTRY] [--Industry INDUSTRY] --Year YEAR<br/>
[--format {json,XML}] [--csvfn CSVFN] [--csvzipfn CSVZIPFN]<br/>
[--splitkey SPLITKEY] [--xkey XKEY] [--ykey YKEY]<br/>
[--unitskey UNITSKEY] [--htmlfn HTMLFN]<br/>
<br/>
get BEA MNE data<br/>
<br/>
options:<br/>
-h, --help            show this help message and exit<br/>
--SeriesID SERIESID   MNE series id<br/>
--DirectionOfInvestment DIRECTIONOFINVESTMENT<br/>
direction of investment<br/>
--Classification CLASSIFICATION<br/>
classification<br/>
--Country COUNTRY     country<br/>
--Industry INDUSTRY   industry<br/>
--Year YEAR           year YYYY or all<br/>
--format {json,XML}   query result format(json)<br/>
--csvfn CSVFN         name of file to store dataset CSV result<br/>
--csvzipfn CSVZIPFN   name of zip file to store dataset CSV results<br/>
--splitkey SPLITKEY   table column name(SeriesName) to use to split the<br/>
plots<br/>
--xkey XKEY           table column name(Year) to use to plot the data<br/>
--ykey YKEY           table column name(DataValue) to use to plot the data<br/>
--unitskey UNITSKEY   table column name(TableScale) to to y label the plot<br/>
--htmlfn HTMLFN       name of file to store dataset HTML result<br/>
<br/>
<br/>
##<br/>
## beanipa<br/>
##<br/>
usage: beanipa [-h] --TableName TABLENAME [--ShowMillions SHOWMILLIONS]<br/>
--Frequency FREQUENCY --Year YEAR [--format {json,XML}]<br/>
[--csvfn CSVFN] [--csvzipfn CSVZIPFN] [--splitkey SPLITKEY]<br/>
[--xkey XKEY] [--ykey YKEY] [--unitskey UNITSKEY]<br/>
[--htmlfn HTMLFN]<br/>
<br/>
get BEA NIPA data<br/>
<br/>
options:<br/>
-h, --help            show this help message and exit<br/>
--TableName TABLENAME<br/>
NIPA table name<br/>
--ShowMillions SHOWMILLIONS<br/>
NIPA show millions<br/>
--Frequency FREQUENCY<br/>
frequency M, Q, A or comma separated list<br/>
--Year YEAR           year YYYY or X for all<br/>
--format {json,XML}   query result format(json)<br/>
--csvfn CSVFN         name of file to store dataset CSV result<br/>
--csvzipfn CSVZIPFN   name of zip file to store dataset CSV results<br/>
--splitkey SPLITKEY   table column name(LineDescription) to use to split the<br/>
plots<br/>
--xkey XKEY           table column name(TimePeriod) to use to plot the data<br/>
--ykey YKEY           table column name(DataValue) to use to plot the data<br/>
--unitskey UNITSKEY   table column name(METRIC_NAME) to y label the plot<br/>
--htmlfn HTMLFN       name of file to store dataset HTML result<br/>
<br/>
<br/>
##<br/>
## beaniud<br/>
##<br/>
usage: beaniud [-h] --TableName TABLENAME --Frequency FREQUENCY --Year YEAR<br/>
[--format {json,XML}] [--csvfn CSVFN] [--csvzipfn CSVZIPFN]<br/>
[--splitkey SPLITKEY] [--xkey XKEY] [--ykey YKEY]<br/>
[--unitskey UNITSKEY] [--htmlfn HTMLFN]<br/>
<br/>
get BEA NIUnderlyingDetail data<br/>
<br/>
options:<br/>
-h, --help            show this help message and exit<br/>
--TableName TABLENAME<br/>
NIUnderlyingDetail table name<br/>
--Frequency FREQUENCY<br/>
frequency M, Q, A or comma separated list<br/>
--Year YEAR           year YYYY or X or all<br/>
--format {json,XML}   query result format(json)<br/>
--csvfn CSVFN         name of file to store dataset CSV result<br/>
--csvzipfn CSVZIPFN   name of zip file to store dataset CSV results<br/>
--splitkey SPLITKEY   table column name({'option_strings': ['--splitkey'],<br/>
'dest': 'splitkey', 'nargs': None, 'const': None,<br/>
'default': 'LineDescription', 'type': None, 'choices':<br/>
None, 'required': False, 'help': 'table column<br/>
name(%s) to use to split the plots', 'metavar': None,<br/>
'container': <argparse._ArgumentGroup object at<br/>
0x102a0b770>, 'prog': 'beaniud'}) to use to split<br/>
the plots<br/>
--xkey XKEY           table column name(TimePeriod) to use to plot the data<br/>
--ykey YKEY           table column name(DataValue) to use to plot the data<br/>
--unitskey UNITSKEY   table column name(METRIC_NAME) to y label the plot<br/>
--htmlfn HTMLFN       name of file to store dataset HTML result<br/>
<br/>
<br/>
##<br/>
## bearegional<br/>
##<br/>
usage: bearegional [-h] --TableName TABLENAME --GeoFips GEOFIPS --LineCode<br/>
LINECODE --Year YEAR [--format {json,XML}]<br/>
[--csvfn CSVFN] [--csvzipfn CSVZIPFN]<br/>
[--splitkey SPLITKEY] [--xkey XKEY] [--ykey YKEY]<br/>
[--unitskey UNITSKEY] [--htmlfn HTMLFN]<br/>
<br/>
get BEA Regional data<br/>
<br/>
options:<br/>
-h, --help            show this help message and exit<br/>
--TableName TABLENAME<br/>
table name<br/>
--GeoFips GEOFIPS     geo fips<br/>
--LineCode LINECODE   line code<br/>
--Year YEAR           year YYYY or ALL<br/>
--format {json,XML}   query result format(json)<br/>
--csvfn CSVFN         name of file to store dataset CSV result<br/>
--csvzipfn CSVZIPFN   name of zip file to store dataset CSV results<br/>
--splitkey SPLITKEY   table column name(GeoName) to use to split the plots<br/>
--xkey XKEY           table column name(TimePeriod) to use to plot the data<br/>
--ykey YKEY           table column name(DataValue) to use to plot the data<br/>
--unitskey UNITSKEY   table column name(CL_UNIT) to y label the plot<br/>
--htmlfn HTMLFN       name of file to store dataset HTML result<br/>
<br/>
<br/>
##<br/>
## beaugdpbyind<br/>
##<br/>
usage: beaugdpbyind [-h] --TableID TABLEID --Industry INDUSTRY --Frequency<br/>
FREQUENCY --Year YEAR [--format {json,XML}]<br/>
[--csvfn CSVFN] [--csvzipfn CSVZIPFN]<br/>
[--splitkey SPLITKEY] [--xkey XKEY] [--ykey YKEY]<br/>
[--unitskey UNITSKEY] [--htmlfn HTMLFN]<br/>
<br/>
get BEA UnderlyingGDPbyIndustry data<br/>
<br/>
options:<br/>
-h, --help            show this help message and exit<br/>
--TableID TABLEID     table id<br/>
--Industry INDUSTRY   industry<br/>
--Frequency FREQUENCY<br/>
frequency M, Q, A or comma separated list<br/>
--Year YEAR           year YYYY or ALL<br/>
--format {json,XML}   result format<br/>
--csvfn CSVFN         name of file to store dataset CSV result<br/>
--csvzipfn CSVZIPFN   name of zip file to store dataset CSV results<br/>
--splitkey SPLITKEY   table column name(IndustrYDescription) to split the<br/>
plots<br/>
--xkey XKEY           table column name(Year) to use to plot the data<br/>
--ykey YKEY           table column name(DataValue) to use to plot the data<br/>
--unitskey UNITSKEY   name(Billions?) to y label the plot<br/>
--htmlfn HTMLFN       name of file to store dataset HTML result<br/>
<br/>
<br/>
##<br/>
## beaqueryq<br/>
##<br/>
usage: beaqueryq [-h]<br/>
[--DatasetName {NIPA,NIUnderlyingDetail,MNE,FixedAssets,ITA,IIP,InputOutput,IntlServTrade,IntlServSTA,GDPbyIndustry,Regional,UnderlyingGDPbyIndustry,APIDatasetMetaData}]<br/>
[--TableName TABLENAME] [--TableID TABLEID]<br/>
[--SeriesID SERIESID] [--ShowMillions SHOWMILLIONS]<br/>
[--Frequency FREQUENCY] [--Year YEAR]<br/>
[--DirectionOfInvestment {inward,outward,parent,state}]<br/>
[--Classification CLASSIFICATION] [--Industry INDUSTRY]<br/>
[--Country COUNTRY] [--Indicator INDICATOR]<br/>
[--AreaOrCountry AREAORCOUNTRY]<br/>
[--TypeOfInvestment TYPEOFINVESTMENT]<br/>
[--Component COMPONENT] [--TypeOfService TYPEOFSERVICE]<br/>
[--TradeDirection TRADEDIRECTION]<br/>
[--Affiliation AFFILIATION] [--Channel CHANNEL]<br/>
[--Destination DESTINATION] [--GeoFips GEOFIPS]<br/>
[--LineCode LINECODE] [--csvfn CSVFN]<br/>
[--csvzipfn CSVZIPFN] [--splitkey SPLITKEY] [--xkey XKEY]<br/>
[--ykey YKEY] [--unitskey UNITSKEY] [--htmlfn HTMLFN]<br/>
[--format {json,XML}] [--hierarchy] [--tableregister]<br/>
<br/>
get BEA data<br/>
<br/>
options:<br/>
-h, --help            show this help message and exit<br/>
--DatasetName {NIPA,NIUnderlyingDetail,MNE,FixedAssets,ITA,IIP,InputOutput,IntlServTrade,IntlServSTA,GDPbyIndustry,Regional,UnderlyingGDPbyIndustry,APIDatasetMetaData}<br/>
dataset name<br/>
--TableName TABLENAME<br/>
NIPA NIUnderlyingDetail FixedAssets Regional table<br/>
name<br/>
--TableID TABLEID     InputOutput GDPbyIndustry UnderlyingGDPbyIndustry<br/>
table id<br/>
--SeriesID SERIESID   MNE series id<br/>
--ShowMillions SHOWMILLIONS<br/>
NIPA show millions<br/>
--Frequency FREQUENCY<br/>
frequency M, Q, A or comma separated list<br/>
--Year YEAR           year YYYY X or all<br/>
--DirectionOfInvestment {inward,outward,parent,state}<br/>
MNE direction of investment<br/>
--Classification CLASSIFICATION<br/>
MNE classification<br/>
--Industry INDUSTRY   MNE IntlServSTA GDPbyIndustry UnderlyingGDPbyIndustry<br/>
Industry<br/>
--Country COUNTRY     MNE country<br/>
--Indicator INDICATOR<br/>
ITA indicator<br/>
--AreaOrCountry AREAORCOUNTRY<br/>
ITA IntlServTrade IntlServSTA area or country<br/>
--TypeOfInvestment TYPEOFINVESTMENT<br/>
IIP type of investment<br/>
--Component COMPONENT<br/>
IIP component<br/>
--TypeOfService TYPEOFSERVICE<br/>
IntlServTrade type of service<br/>
--TradeDirection TRADEDIRECTION<br/>
IntlServTrade trade direction<br/>
--Affiliation AFFILIATION<br/>
IntlServTrade affiliation<br/>
--Channel CHANNEL     IntlServSTA channel<br/>
--Destination DESTINATION<br/>
IntlServSTA destination<br/>
--GeoFips GEOFIPS     Regional geo FIPS<br/>
--LineCode LINECODE   Regional line code<br/>
--csvfn CSVFN         name of file to store dataset CSV result<br/>
--csvzipfn CSVZIPFN   name of zip file to store dataset CSV results<br/>
--splitkey SPLITKEY   table column name to use to split the table<br/>
--xkey XKEY           table column name to use to plot the data<br/>
--ykey YKEY           table column name to use to plot the data<br/>
--unitskey UNITSKEY   table column name to use to label the data<br/>
--htmlfn HTMLFN       name of file to store dataset HTML result<br/>
--format {json,XML}   query result format<br/>
--hierarchy           BEA data model<br/>
--tableregister       get NIPA table register<br/>
<br/>

var layerDataGeoJSONFormat = new ol.format.GeoJSON();

var windDataSource = new ol.source.Vector({
    format: layerDataGeoJSONFormat,
    projection: 'EPSG:3857',
    });

var windClusterDataSource = new ol.source.Cluster({source : windDataSource});

function getColorCodeForTemprature(tmp)
    {
    var strokeColor = [2,8,21,0.5];
    var twidth = 15;
    if(tmp <= 20) 
        {
        strokeColor = [2, 196, 21, 0.5];    //'#020815';
        twidth = 15;
        }
    else if(tmp>20 && tmp<25) 
        {
        strokeColor = [25, 140, 255,0.5];   //'#198cff';
        twidth = 17;
        }
    else if(tmp>=25) 
        {
        strokeColor = [270, 70 ,90, 0.5];//'#f61212';
        twidth = 20;
        }
    return [strokeColor,twidth];                        
    }

var wind10mLaye

var map = new ol.Map({
    target: 'map',
    layers: [
            new ol.layer.Tile({
            source: new ol.source.OSM()}),
            wind10mLayer
        ],
    view: new ol.View({
        center: ol.proj.fromLonLat([37.41, 8.82], 'EPSG:4326', 'EPSG:3857'),
        zoom: 4
        }),

    });rStyleFunction = function(feature)
    {
    var tval = Math.floor(parseFloat(feature.getProperties().features[0].getProperties().wd_10m));
    var ccodes = getColorCodeForTemprature(tval);

    var cStyle = new ol.style.Circle({
                fill: new ol.style.Fill({
                color: ccodes[0] //'#1b465a',
                }),
            stroke: new ol.style.Stroke({
                color: ccodes[0],
                width: 3
                }),
            radius: ccodes[1]
            });

    var cText = new ol.style.Text({
            text: tval.toString(),  // size.toString(),
            fill: new ol.style.Fill({color: '#fff'}),
            font: '15px sans-serif', 
            });

    return [new ol.style.Style({image: cStyle, text : cText})];     
    };


var wind10mLayer = new ol.layer.Vector({
        source: windClusterDataSource,
        style: wind10mLayerStyleFunction,
        layerid: 'wind10m'                    
        });

var map = new ol.Map({
    target: 'map',
    layers: [
            new ol.layer.Tile({
            source: new ol.source.OSM()}),
            wind10mLayer
        ],
    view: new ol.View({
        center: ol.proj.fromLonLat([37.41, 8.82], 'EPSG:4326', 'EPSG:3857'),
        zoom: 4
        }),

    });
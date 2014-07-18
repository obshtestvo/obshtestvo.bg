$(function () {
    var $skills = $('#joinSkills'),
        avatarPicker = $('#avatar'),
        avatarPrev = $('#prev_avatar'),
        location = $('#location'),
        geoLoc = JSON.parse(location.attr('value')),
    // The overlay layer for our marker, with a simple diamond as symbol
        overlay = new OpenLayers.Layer.Vector('Overlay', {
            styleMap: new OpenLayers.StyleMap({
                externalGraphic: '/static/img/map-marker.png',
                graphicWidth: 30, graphicHeight: 24, graphicYOffset: -24
            })
        }),



        myLocation = new OpenLayers.LonLat(geoLoc.location[0], geoLoc.location[1]),

    // Finally we create the map
        map = new OpenLayers.Map({
            div: "map",
            layers: [new OpenLayers.Layer.OSM(), overlay],
            center: myLocation, zoom: 3
        });

    myLocation.transform("EPSG:4326", "EPSG:900913");

    console.log(myLocation);

    // We add the marker with a tooltip text to the overlay
    overlay.addFeatures([
        new OpenLayers.Feature.Vector(myLocation)
    ]);

    new Select2Grouped($skills, $skills.data('choices'), $skills.data('selection'));

    avatarPrev.on('click', function () {
        avatarPicker.click();
    });

    avatarPrev.on('load', function () {
        window.URL.revokeObjectURL(avatarPrev.attr('src'));
    });

    avatarPicker.on('change', function () {
        var imgUrl = window.URL.createObjectURL(avatarPicker[0].files[0]);
        console.log(imgUrl);
        avatarPrev.attr('src', imgUrl);
    });

});
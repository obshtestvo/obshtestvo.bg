$(function () {
    var $skills = $('#joinSkills'),
        avatarPicker = $('#avatar'),
        avatarPrev = $('#prev_avatar'),

    // The overlay layer for our marker, with a simple diamond as symbol
        overlay = new OpenLayers.Layer.Vector('Overlay', {
            styleMap: new OpenLayers.StyleMap({
                externalGraphic: '/static/img/map-marker.png',
                graphicWidth: 30, graphicHeight: 24, graphicYOffset: -24
            })
        }),

        myLocation = new OpenLayers.Geometry.Point(10.2, 48.9)

    // Finally we create the map
        map = new OpenLayers.Map({
            div: "map",
            layers: [new OpenLayers.Layer.OSM(), overlay],
            center: myLocation.getBounds().getCenterLonLat(), zoom: 3
        });

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
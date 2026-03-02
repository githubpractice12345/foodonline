let autocomplete;

function initAutoComplete() {

    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
            types: ['geocode', 'establishment'],
            componentRestrictions: { country: ['in'] },
        }
    );

    // When user selects a suggestion
    autocomplete.addListener('place_changed', onPlaceChanged);
}


function onPlaceChanged() {

    var place = autocomplete.getPlace();

    // If user typed but didn't select suggestion
    if (!place.geometry) {
        $('#id_address').attr('placeholder', 'Start typing...');
        return;
    }

    // Set latitude and longitude using jQuery
    $('#id_latitude').val(place.geometry.location.lat());
    $('#id_longitude').val(place.geometry.location.lng());

    // Clear previous values first (good practice)
    $('#id_country').val('');
    $('#id_state').val('');
    $('#id_city').val('');
    $('#id_pin_code').val('');

    // Make sure address_components exists
    if (!place.address_components) return;

    // 🔁 Nested Loop
    for (var i = 0; i < place.address_components.length; i++) {

        var component = place.address_components[i];
        var types = component.types;

        for (var j = 0; j < types.length; j++) {

            // Country
            if (types[j] === 'country') {
                $('#id_country').val(component.long_name);
            }

            // State
            if (types[j] === 'administrative_area_level_1') {
                $('#id_state').val(component.long_name);
            }

            // City
            if (types[j] === 'locality') {
                $('#id_city').val(component.long_name);
            }

            // Postal Code
            if (types[j] === 'postal_code') {
                $('#id_pin_code').val(component.long_name);
            }
        }
    }
}



// let autocomplete;

// function initAutoComplete() {

//     const input = document.getElementById('id_address');

//     if (!input) {
//         console.error("Input element not found");
//         return;
//     }

//     autocomplete = new google.maps.places.Autocomplete(input, {
//         types: ['geocode', 'establishment'],
//         componentRestrictions: { country: ['in'] },
//     });

//     console.log("Autocomplete initialized");

//     autocomplete.addListener('place_changed', function () {

//         const place = autocomplete.getPlace();

//         console.log("Place changed triggered");
//         console.log(place);

//         if (!place.geometry) return;

//         // console.log("Latitude:", place.geometry.location.lat());
//         // console.log("Longitude:", place.geometry.location.lng());

//         $("#id_latitude").val(place.geometry.location.lat());
//         $("#id_longitude").val(place.geometry.location.lng());

//         console.log(place.address_components)
//         for(var i=0; i<place.address_components.length; i++){
//             for(var j=0; j<place.address_components[i].types[j].length; j++){
//                 //get country
//                 if(place.address_components[i].types[j] == 'country'){
//                     $('#id_country').val(place.address_components[i].long_name);
//                 }
//                 //get state
//                 if(place.address_components[i].types[j] == 'administrative_area_level_1'){
//                     $('#id_state').val(place.address_components[i].long_name);
//                 }
//                 //get city
//                 if(place.address_components[i].types[j] == 'locality'){
//                     $('#id_city').val(place.address_components[i].long_name);
//                 }
//                 //get pincode
//                 if(place.address_components[i].types[j] == 'postal_code'){
//                     $('#id_pin_code').val(place.address_components[i].long_name);
//                 }else{
//                     $('#id_pin_code').val('');
//                 }
//             }
//     }
//     });
    
// }


// let autocomplete;

// function initAutoComplete() {

//     const input = document.getElementById('id_address');

//     if (!input) {
//         console.error("Input element not found");
//         return;
//     }

//     autocomplete = new google.maps.places.Autocomplete(input, {
//         types: ['geocode', 'establishment'],
//         componentRestrictions: { country: ['in'] },
//     });

//     console.log("Autocomplete initialized");

//     autocomplete.addListener('place_changed', function () {

//         const place = autocomplete.getPlace();

//         console.log("Place changed triggered");
//         console.log(place);

//         if (!place.geometry) return;

//         // Set latitude & longitude
//         $("#id_latitude").val(place.geometry.location.lat());
//         $("#id_longitude").val(place.geometry.location.lng());

//         console.log(place.address_components);

//         // Clear pin first (optional safety)
//         $('#id_pin_code').val('');

//         for (var i = 0; i < place.address_components.length; i++) {

//             var component = place.address_components[i];
//             var types = component.types;

//             for (var j = 0; j < types.length; j++) {

//                 // Country
//                 if (types[j] === 'country') {
//                     $('#id_country').val(component.long_name);
//                 }

//                 // State
//                 if (types[j] === 'administrative_area_level_1') {
//                     $('#id_state').val(component.long_name);
//                 }

//                 // City
//                 if (types[j] === 'locality') {
//                     $('#id_city').val(component.long_name);
//                 }

//                 // Postal Code
//                 if (types[j] === 'postal_code') {
//                     $('#id_pin_code').val(component.long_name);
//                 }
//             }
//         }

//     });

// }
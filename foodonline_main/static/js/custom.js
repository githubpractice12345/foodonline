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

$(document).ready(function(){
    //ADD TO CART
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();

        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        // data = {
        //     food_id: food_id,
        // }
        $.ajax({
            type: 'GET',
            url: url,
            // data: data, as url will contain bydefault foof_id
            success: function(response){
                console.log(response)
                if(response.status == 'login_required'){
                    Swal.fire({title: response.message, text: "Only Login User", icon: "success"}).then(function(){
                        window.location = '/login';
                    })
                }else if(response.status == 'Success'){
                    // Update UI only if successful
                    console.log(response.cart_counter['cart_count'])
                    $('#cart-count').html(response.cart_counter['cart_count'])
                    $('#qty-'+food_id).html(response.qty)

                    // subtotal, tax and grand_total by calling the fun
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total'],
                    )
                }else{
                    // Handle the failure message
                    Swal.fire({title: response.message, text: " ", icon: "error"})
                }

                
            }
        })
    })

    //place the cart item quantity on load
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id');
        var qty = $(this).attr('data-qty');
        // console.log(qty)
        $('#'+the_id).html(qty)

    })
    

    //DECREASE CART
    $('.decrease_cart').on('click', function(e){
        e.preventDefault();

        food_id = $(this).attr('data-id');
        cart_id = $(this).attr('data-cartid');
        url = $(this).attr('data-url');

        // data = {
        //     food_id: food_id,
        // }
        $.ajax({
            type: 'GET',
            url: url,
            // data: data,
            success: function(response){
                console.log(response)
                if(response.status == 'login_required'){
                    Swal.fire({title: response.message, text: "Only Login User", icon: "success"}).then(function(){
                        window.location = '/login';
                    })
                }else if(response.status == 'Success'){
                    // Update UI only if successful
                    console.log(response.cart_counter['cart_count'])
                    // Update cart count
                    $('#cart-count').html(response.cart_counter['cart_count'])
                    // Update quantity
                    $('#qty-'+food_id).html(response.qty)

                    // subtotal, tax and grand_total by calling the fun
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total'],
                    )
                    
                    if(window.location.pathname == '/cart/'){
                        //calling the fun to remove cart and message if cart is empty
                        removeCartItem(response.qty, cart_id)
                        checkEmptyCart()
                    }

                }else{
                    // Handle the failure message
                    Swal.fire({title: response.message, text: " ", icon: "error"})
                }
                               
            }
        })
    })

    //DELETE CART ITEM
    $('.delete_cart').on('click', function(e){
        e.preventDefault();

        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            // data: data,
            success: function(response){
                console.log(response)
                //As we have used @login_required in Cart view no need for login condtion
                if(response.status == 'Success'){
                    // Update UI only if successful
                    console.log(response.cart_counter['cart_count'])
                    // Update cart count
                    $('#cart-count').html(response.cart_counter['cart_count'])
                    // Update quantity
                    // $('#qty-'+food_id).html(response.qty)
                    Swal.fire({title: response.message, text: " ", icon: "success"})

                    // subtotal, tax and grand_total by calling the fun
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total'],
                    )

                    //calling the function to remove or delete cart element after success
                    removeCartItem(0, cart_id)
                    //calling the function if cart count is 0
                    checkEmptyCart()

                }else{
                    // Handle the failure message
                    Swal.fire({title: response.message, text: " ", icon: "error"})
                }
                               
            }
        })
    })

    //Delete the cart item if the qty is 0
    function removeCartItem(cartItemQty, cart_id){
        if(cartItemQty<=0){
            //remove cart item element.
            // document.getElementById("cart-item-"+cart_id).remove()
            var el = document.getElementById("cart-item-"+cart_id)
            if(el){
                el.remove()
            }
        }
    }


    //check if the cart is empty show the message(i.e check if the count on cart icon on navbar is 0, read the value by id 'cart_count)
    // function checkEmptyCart(){
    //     var cart_counter = document.getElementById('cart-count').innerHTML
    //     if(cart_counter == 0){
    //         document.getElementById('empty-cart').style.display = "block";
    //     }
    // }

    function checkEmptyCart(){
        var cartElement = document.getElementById('cart-count')

        if(cartElement){
            var cart_counter = cartElement.innerHTML

            if(cart_counter == 0){
                var emptyCart = document.getElementById('empty-cart')
                if(emptyCart){
                    emptyCart.style.display = "block"
                }
            }
        }
    }

    //apply cart amounts
    function applyCartAmounts(subtotal, tax, grand_total){
        if(window.location.pathname == '/cart/'){
            $('#subtotal').html(subtotal)
            $('#tax').html(tax)
            $('#total').html(grand_total)
        }
        
    }


})
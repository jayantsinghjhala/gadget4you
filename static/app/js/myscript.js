$(document).ready(function () {

    $(".quantity").each(function () {
        var initial_quantity = parseInt($(this).text(), 10);
        $(this).prev(".minus-cart").prop("disabled", initial_quantity === 1);
        $(this).next(".plus-cart").prop("disabled", initial_quantity === 10);
    });
    $('#slider1, #slider2, #slider3').owlCarousel({
        loop: true,
        margin: 20,
        responsiveClass: true,
        responsive: {
            0: {
                items: 1,
                nav: false,
                autoplay: true,
            },
            600: {
                items: 3,
                nav: true,
                autoplay: true,
            },
            1000: {
                items: 5,
                nav: true,
                loop: true,
                autoplay: true,
            }
        }
    })

    function formatIndian(value) {
        try {
            // Convert the value to an integer
            var intValue = parseInt(value, 10);

            // Format the integer value using Indian number format
            var formattedValue = intValue.toLocaleString("en-IN");

            // Return the formatted value with the Indian Rupee symbol
            return '₹' + formattedValue;
        } catch (error) {
            // Handle any errors and return the original value in case of failure
            console.error("Error formatting Indian number:", error);
            return '₹' + value;
        }
    }

    function checkCartProducts() {
        var cartProductsDiv = $(".cart_products");
        var emptyMsgDiv = $(".empty_msg");
        console.log(cartProductsDiv.children().length);
        // Check if .cart_products has child elements
        if (cartProductsDiv.children().length === 0) {
            $(".place_order_btn").hide();
            cartProductsDiv.append(`<div class="col-12 text-center mt-5 pt-5 empty_msg">
            <p class="text-muted">
              No Products found in the Cart. <a class="fw-bold text-success text-decoration-none" href="/">Continue Shopping</a>
            </p>
          </div>`) // If empty, show .empty_msg
        }
    }
    // checkCartProducts();

    $('.plus-cart, .minus-cart,.remove_cart').click(function () {
        var action;
        var id = $(this).attr("cid");
        var clickedButton = $(this);  // Store the reference to the clicked button

        if (clickedButton.hasClass("plus-cart")) {
            if(clickedButton.hasClass("plus_cart_b")){
                action = "plus_b";
            }
            else{
                action = "plus";
            }
        } else if (clickedButton.hasClass("minus-cart")) {
            if(clickedButton.hasClass("minus_cart_b")){
                action = "minus_b";
            }
            else{
                action = "minus";
            }
        } else if (clickedButton.hasClass("remove_cart")) {
            var confirmed = confirm('Are you sure you want to remove this item from the cart?');
            if (!confirmed) {
                return;
            }
            action = "remove";
        }
        $.ajax({
            type: "GET",
            url: "/change_cart",
            data: {
                cart_id: id,
                action: action
            },
            success: function (data) {
                if (action == "remove") {
                    clickedButton.closest(".cart_product").remove();
                    $("#amount").text(formatIndian(data.amount));
                    $("#total_amount").text(formatIndian(data.total_amount));
                    $("#total_shipping").text(formatIndian(data.total_shipping));
                    $(".cart_unit").text(data.cart_unit);
                    
                    checkCartProducts();
                } else {
                    $(this).prop("disabled", false);
                    if (action == "plus" || action == "plus_b") {
                        clickedButton.closest(".quantity_block").find(".minus-cart").prop("disabled", false);
                    } else if (action == "minus" || action == "minus_b") {
                        clickedButton.closest(".quantity_block").find(".plus-cart").prop("disabled", false);
                    }

                    clickedButton.closest(".quantity_block").find(".quantity").text(data.quantity);
                    if (action == "minus" || action == "minus_b") {
                        clickedButton.closest(".quantity_block").find(".minus-cart").prop("disabled", data.quantity === 1);
                        $(this).prop("disabled", data.quantity === 10);
                    } else if (action == "plus" || action == "plus_b") {
                        clickedButton.closest(".quantity_block").find(".plus-cart").prop("disabled", data.quantity === 10);
                        $(this).prop("disabled", data.quantity === 1);
                    }

                    if (action == "minus_b" || action == "plus_b") {
                        product_price=$('.product_price').text();
                        $("#amount").text(product_price+' x '+data.quantity);
                    }else{
                        
                        $("#amount").text(formatIndian(data.amount));
                    }
                    $("#total_amount").text(formatIndian(data.total_amount));
                    $("#total_shipping").text(formatIndian(data.total_shipping));
                }

            },
            complete: function () {
                // Your complete callback logic here
            }
        });
    });
    $('.form-check-input:first').prop('checked', true);
    $('.address_card').on('click', function () {
        $('.address_card').removeClass('border-primary');
        $(this).addClass('border-primary');
        $(this).find('.form-check-input').prop('checked', true);
        $('.address_card').not(this).find('.form-check-input').prop('checked', false);
      });
});

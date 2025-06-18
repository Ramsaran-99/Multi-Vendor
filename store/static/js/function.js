$(document).ready(function () {

    function generateCartId() {
    const ls_cartid = localStorage.getItem("cartId");
    if (ls_cartid === null) {
        var cartId=""
    
        for (var i=0; i<10; i++) {
    
            cartId += Math.floor(Math.random() * 10);
        }
        localStorage.setItem("cartId", cartId);
    }

    return ls_cartid || cartId
    }
});

$(document).on("click",".add_to_cart", function(){
    
})
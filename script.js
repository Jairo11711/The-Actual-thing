"use strict";

const cards = document.querySelectorAll("div.item-purchased-row-ui");

for (let i = 0; i < cards.length; i++) {
    cards[i].addEventListener("mouseover", 
        function() {
        console.log("Mouse over card " + cards[i]);
    });

    cards[i].addEventListener("mouseout", 
        function() {
        console.log("Mouse out of card " + cards[i]);
    });

}
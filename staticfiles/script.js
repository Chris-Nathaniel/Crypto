document.addEventListener('DOMContentLoaded', function () {
    const slider = document.getElementById('percentage-slider');
    const input = document.getElementById('percentage-input');

    function updateSliderFill(value) {
        const percent = (value - slider.min) / (slider.max - slider.min) * 100;
        slider.style.background = `linear-gradient(to right, rgb(65,150,65) 0%, rgb(65,150,65) ${percent}%, #ddd ${percent}%, #ddd 100%)`;
    }

    // Initial fill
    updateSliderFill(slider.value);

    slider.addEventListener('input', function () {
        input.value = slider.value;
        updateSliderFill(slider.value);
    });

    input.addEventListener('input', function () {
        slider.value = input.value;
        updateSliderFill(input.value);
    });
});


function yieldSlider() {
    const rangeSlide = document.querySelector(".range-slide");
    const priceSlider = document.querySelector(".yield-slider");
    const tooltip = document.querySelector(".tooltip");
    const maxVal = parseFloat(rangeSlide.max);
    const minVal = parseFloat(rangeSlide.min);
    const value = parseFloat(rangeSlide.value);
    const center = (maxVal + minVal) / 2;
    const fillColor = value < center ? "rgb(150, 65, 65)" : value > center ? "#5d7e24" : "#aaa";

    // Update tooltip
    let progress = ((value - minVal) / (maxVal - minVal)) * 100;
    tooltip.innerHTML = value + "%";
    tooltip.style.left = progress + "%";
    tooltip.style.background = fillColor;
    priceSlider.style.color = "#FFF";

    // Update gradient fill
    let leftPercent, rightPercent;
    if (value < center) {
        leftPercent = ((center - value) / (center - minVal)) * 50;
        rightPercent = 0;
    } else {
        leftPercent = 0;
        rightPercent = ((value - center) / (maxVal - center)) * 50;
    }

    rangeSlide.style.background = `linear-gradient(to right, #ddd 0%, #ddd ${50 - leftPercent}%, ${fillColor} ${50 - leftPercent}%, ${fillColor} ${50 + rightPercent}%, #ddd ${50 + rightPercent}%, #ddd 100%)`;

    document.querySelectorAll("tr").forEach(row => {
        const balanceCell = row.querySelector(".balance");
        const gainsCell = row.querySelector(".gains");
        const sellingCell = row.querySelector(".selling");
        const itemQuantity = sellingCell ? parseFloat(sellingCell.getAttribute("data-item-quantity")) : null;

        if (balanceCell && gainsCell && sellingCell && itemQuantity) {
            const balance = parseFloat(balanceCell.textContent.replace(/,/g, ''));
            const margin = balance * (value / 100);
            const sellingPrice = (balance + margin) / (1 - 0.0033) / itemQuantity;

            sellingCell.textContent = sellingPrice.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });

            gainsCell.textContent = margin.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });

            // Apply color based on gain/loss
            if (margin > 0) {
                gainsCell.classList.add("green");
                gainsCell.classList.remove("red");
            } else if (margin < 0) {
                gainsCell.classList.add("red");
                gainsCell.classList.remove("green");
            } else {
                gainsCell.classList.remove("green", "red");
            }
        }
    });
}



window.onload = function () {
  yieldSlider();
};
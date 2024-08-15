const prevButton = document.querySelector('.prev');
const nextButton = document.querySelector('.next');
const carouselImages = document.querySelector('.carousel-images');
const images = document.querySelectorAll('.index-book');

let index = 0;
const visibleImages = 3; // Number of images to show at a time
const imageWidth = images[0].clientWidth;

function updateCarousel() {
    const offset = -index * imageWidth;
    carouselImages.style.transform = `translateX(${offset}px)`;
}

function checkButtons() {
    prevButton.disabled = index === 0;
    nextButton.disabled = index >= images.length;//-visibleImages
}

prevButton.addEventListener('click', () => {
    if (index > 0) {
        index--;
        updateCarousel();
        checkButtons();
    }
});

nextButton.addEventListener('click', () => {
    if (index < images.length ) {//-visibleImages
        index++;
        updateCarousel();
        checkButtons();
    }
});

window.addEventListener('resize', () => {
    // Update the width on resize
    const updatedImageWidth = images[0].clientWidth;
    updateCarousel();
});

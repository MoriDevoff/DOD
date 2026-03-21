// static/mainpage/script.js

// Увеличивай число при замене картинок с тем же именем (image1.jpg и т.д.),
// иначе браузер может показывать старые файлы из кэша.
const BG_CACHE_VERSION = '1';

console.log("Скрипт фона загружен — проверка"); // отладка

const backgrounds = [
    `/static/mainpage/image1.jpg?v=${BG_CACHE_VERSION}`,
    `/static/mainpage/image2.jpg?v=${BG_CACHE_VERSION}`,
    `/static/mainpage/image3.jpg?v=${BG_CACHE_VERSION}`,
    `/static/mainpage/image4.jpg?v=${BG_CACHE_VERSION}`,
    // добавь все свои новые картинки сюда ТОЧНО так, как они называются
    // пример: '/static/mainpage/bg1.webp', '/static/mainpage/bg2.png' и т.д.
];

let currentIndex = 0;
const slider = document.querySelector('.background-slider');

function changeBackground() {
    if (!slider) {
        console.error("Элемент .background-slider НЕ НАЙДЕН!");
        return;
    }
    const url = backgrounds[currentIndex];
    console.log("Меняем фон на:", url); // отладка
    slider.style.backgroundImage = `url(${url})`;
    currentIndex = (currentIndex + 1) % backgrounds.length;
}

// Запускаем сразу и каждые 10 секунд
changeBackground();
setInterval(changeBackground, 10000);
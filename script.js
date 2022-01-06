const button = document.getElementById('button');
const list = document.getElementById('dropdown');
const image = document.getElementById('image');

const setImage = (element) => () => {
  image.src = element.dataset.image;
  image.style.display = 'block';
}

button.addEventListener('click', () => {
  list.classList.toggle('active')
});

list.querySelectorAll("li").forEach((item) => {
  item.addEventListener('click', setImage(item));
});
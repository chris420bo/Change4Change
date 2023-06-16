const arrow = document.querySelector('.arrow-btn');
const content = document.querySelector('#content');

arrow.addEventListener('click', () => {
        const expanded = arrow.getAttribute('aria-expanded') === 'true' || false;
        arrow.setAttribute('aria-expanded', !expanded);
        content.style.display = expanded ? 'none' : 'grid';
});
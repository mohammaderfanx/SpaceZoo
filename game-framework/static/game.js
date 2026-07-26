const gameArea = document.getElementById('game-area');
const player = document.getElementById('player-character');

let position = { x: 120, y: 120 };
const step = 24;

function updatePlayerPosition() {
    player.style.left = `${position.x}px`;
    player.style.top = `${position.y}px`;
}

function movePlayer(dx, dy) {
    const maxX = gameArea.clientWidth - 48;
    const maxY = gameArea.clientHeight - 48;
    position.x = Math.min(maxX, Math.max(0, position.x + dx));
    position.y = Math.min(maxY, Math.max(0, position.y + dy));
    updatePlayerPosition();
}

window.addEventListener('keydown', (event) => {
    const key = event.key.toLowerCase();
    if (['arrowup', 'w'].includes(key)) {
        movePlayer(0, -step);
        event.preventDefault();
    } else if (['arrowdown', 's'].includes(key)) {
        movePlayer(0, step);
        event.preventDefault();
    } else if (['arrowleft', 'a'].includes(key)) {
        movePlayer(-step, 0);
        event.preventDefault();
    } else if (['arrowright', 'd'].includes(key)) {
        movePlayer(step, 0);
        event.preventDefault();
    }
});

updatePlayerPosition();

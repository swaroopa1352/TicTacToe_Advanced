// static/game/script.js
const boardEl = document.getElementById('game');
const statusEl = document.getElementById('status');
const restartBtn = document.getElementById('restart');

function render(board, currentPlayer, winner) {
  const cells = boardEl.querySelectorAll('.cell');
  board.forEach((val, i) => {
    cells[i].textContent = val === '-' ? '' : val;
  });

  // game over?
  if (winner) {
    statusEl.textContent = `Winner: ${winner}`;
    boardEl.classList.add('disabled');
  } else if (!board.includes('-')) {
    statusEl.textContent = `It's a tie!`;
    boardEl.classList.add('disabled');
  } else {
    statusEl.textContent = `Player ${currentPlayer}'s turn`;
    boardEl.classList.remove('disabled');
  }
}

boardEl.addEventListener('click', async (e) => {
  const cell = e.target.closest('.cell');
  if (!cell) return;

  const pos = parseInt(cell.dataset.index, 10);
  try {
    const res = await fetch(`/move/${pos}/`);
    const data = await res.json();
    if (data.error) {
      // invalid move or game already over – just ignore
      return;
    }
    render(data.board, data.player, data.winner);
  } catch (err) {
    console.error(err);
  }
});

restartBtn.addEventListener('click', async () => {
  try {
    const res = await fetch(`/restart/`);
    const data = await res.json();
    render(data.board, data.player, data.winner);
  } catch (err) {
    console.error(err);
  }
});

// First paint: load server state (fresh game)
(async () => {
  try {
    const res = await fetch(`/restart/`);
    const data = await res.json();
    render(data.board, data.player, data.winner);
  } catch (err) {
    console.error(err);
  }
})();



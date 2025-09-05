// static/game/script.js
const boardEl = document.getElementById('game');
const statusEl = document.getElementById('status');
const restartBtn = document.getElementById('restart');

const STATE_URL   = boardEl.dataset.stateUrl;
const MOVE_URL    = boardEl.dataset.moveUrl;
const RESTART_URL = boardEl.dataset.restartUrl;

let lastState = null;

function csrftoken() {
  const m = document.cookie.match(/csrftoken=([^;]+)/);
  return m ? m[1] : '';
}

function render(data) {
  lastState = data;
  const cells = boardEl.querySelectorAll('.cell');
  cells.forEach(c => { c.textContent = ''; c.classList.remove('win'); });

  data.board.forEach((val, i) => {
    cells[i].textContent = val === '-' ? '' : val;
  });

  // winner highlight
  const lines = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
  if (data.winner) {
    for (const [a,b,c] of lines) {
      if (data.board[a] !== '-' && data.board[a] === data.board[b] && data.board[b] === data.board[c]) {
        [a,b,c].forEach(i => cells[i].classList.add('win'));
      }
    }
  }

  if (data.winner) {
    statusEl.textContent = `Winner: ${data.winner}`;
    boardEl.classList.add('disabled');
  } else if (!data.board.includes('-')) {
    statusEl.textContent = `It's a tie!`;
    boardEl.classList.add('disabled');
  } else {
    const tag = data.ai_enabled
      ? (data.player === data.ai_player ? '(Computer)' : '(You)')
      : '';
    statusEl.textContent = `Player ${data.player}'s turn ${tag}`;
    boardEl.classList.remove('disabled');
  }
}

boardEl.addEventListener('click', async (e) => {
  const cell = e.target.closest('.cell');
  if (!cell || boardEl.classList.contains('disabled')) return;

  // If AI's turn (shouldn't happen because server auto-plays),
  // just ignore clicks defensively.
  if (lastState && lastState.ai_enabled && lastState.player === lastState.ai_player) return;

  const pos = parseInt(cell.dataset.index, 10);
  const res = await fetch(MOVE_URL, {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken(),
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams({ pos }).toString()
  });
  render(await res.json());
});

restartBtn.addEventListener('click', async () => {
  const res = await fetch(RESTART_URL, {
    method: 'POST',
    headers: { 'X-CSRFToken': csrftoken() }
  });
  render(await res.json());
});

// initial paint
(async () => {
  const res = await fetch(STATE_URL);
  render(await res.json());
})();

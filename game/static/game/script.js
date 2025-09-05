// Improved interactivity: subtle animations, winner glow, spinner while we wait
const boardEl   = document.getElementById('game');
const statusEl  = document.getElementById('status');
const restartEl = document.getElementById('restart');
const overlayEl = document.getElementById('overlay');

const STATE_URL   = boardEl.dataset.stateUrl;
const MOVE_URL    = boardEl.dataset.moveUrl;
const RESTART_URL = boardEl.dataset.restartUrl;

let lastState = null;

function csrftoken(){
  const m = document.cookie.match(/csrftoken=([^;]+)/);
  return m ? m[1] : '';
}

function render(data){
  const cells = boardEl.querySelectorAll('.cell');

  // clear classes
  cells.forEach((c,i) => { c.classList.remove('x','o','win','pulse'); });

  // draw board + simple "last move" pulse
  data.board.forEach((val, i) => {
    const cell = cells[i];
    const prev = lastState?.board?.[i] ?? '-';
    cell.textContent = val === '-' ? '' : val;
    if (val === 'X') cell.classList.add('x');
    if (val === 'O') cell.classList.add('o');
    if (prev !== val && val !== '-') cell.classList.add('pulse');
  });

  // highlight winner line
  const lines = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
  if (data.winner){
    for (const [a,b,c] of lines){
      if (data.board[a] !== '-' && data.board[a] === data.board[b] && data.board[b] === data.board[c]){
        [a,b,c].forEach(i => boardEl.children[i].classList.add('win'));
      }
    }
  }

  // set status + enable/disable board
  if (data.winner){
    statusEl.textContent = `Winner: ${data.winner}`;
    boardEl.classList.add('disabled');
  } else if (!data.board.includes('-')){
    statusEl.textContent = `It's a tie!`;
    boardEl.classList.add('disabled');
  } else {
    const tag = data.ai_enabled ? (data.player === data.ai_player ? '(Computer)' : '(You)') : '';
    statusEl.textContent = `Player ${data.player}'s turn ${tag}`;
    boardEl.classList.remove('disabled');
  }

  lastState = data;
}

async function getState(){
  const res = await fetch(STATE_URL);
  return res.json();
}

async function post(url, body){
  overlayEl.classList.remove('hidden'); // show spinner while waiting
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken(),
      ...(body ? {'Content-Type':'application/x-www-form-urlencoded'} : {})
    },
    body
  });
  const data = await res.json();
  overlayEl.classList.add('hidden'); // hide spinner
  return data;
}

boardEl.addEventListener('click', async e => {
  const cell = e.target.closest('.cell');
  if (!cell || boardEl.classList.contains('disabled')) return;

  // Prevent human click if it's AI turn (server usually handles this, but this is a guard)
  if (lastState?.ai_enabled && lastState.player === lastState.ai_player) return;

  const pos = parseInt(cell.dataset.index, 10);
  const data = await post(MOVE_URL, new URLSearchParams({pos}).toString());
  render(data);
});

restartEl.addEventListener('click', async () => {
  const data = await post(RESTART_URL);
  render(data);
});

// First paint
(async () => {
  render(await getState());
})();


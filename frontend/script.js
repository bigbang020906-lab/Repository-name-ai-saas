const API = "https://your-backend-url/kai";

async function send() {
  const input = document.getElementById("input");
  const chat = document.getElementById("chat");

  const msg = input.value;
  input.value = "";

  chat.innerHTML += `<p>🧑 ${msg}</p>`;

  const res = await fetch(API, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message: msg })
  });

  const data = await res.json();

  chat.innerHTML += `<p>🧠 ${data.reply}</p>`;
}

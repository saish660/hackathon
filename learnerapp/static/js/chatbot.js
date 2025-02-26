chatbot_button = document.querySelector("#chat_button")
user_prompt = document.querySelector("#user_prompt")
chat_window = document.querySelector("#chat_window")

chatbot_button.addEventListener("click", function () {
    let prompt = user_prompt.value
    chat_window.innerHTML += `<p class="prompt">${prompt}</p>`
    user_prompt.value = ""
    let response = get_response(prompt)
    if (response === "Error") {
        chat_window.innerHTML += `<p class="response">"An error occured"</p>`
    }
});


async function get_response(prompt) {
    fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": "Bearer <openrouter api key>",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        "model": "google/gemini-2.0-pro-exp-02-05:free",
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "text": `Explain in simple words in not more than 200 words (Give the output as html text and don't format it): ${prompt}`
              }
            ]
          }
        ]
      })
    })
  .then(response => {
    if (!response.ok) {
      return "Error"
    }
    return response.json();
  })
  .then(userData => {
    // Process the retrieved user data
   chat_window.innerHTML += `<p class="response">${userData["choices"][0]["message"]["content"]}</p>`
      console.log(userData["choices"][0]["message"]["content"])
  })
}





async function askAI() {

    const input = document.getElementById("question");
    const chat = document.getElementById("chat");
    const button = document.querySelector("button");

    const question = input.value.trim();

    if (!question) {
        return;
    }

    // Show user question
    chat.innerHTML += `
        <div class="user">
            <b>You:</b> ${question}
        </div>
    `;

    input.value = "";

    // Disable button while AI is answering
    button.disabled = true;
    button.innerText = "Thinking...";

    // Show loading message
    const loading = document.createElement("div");
    loading.className = "ai";
    loading.innerHTML = "<b>AI:</b> Thinking...";
    chat.appendChild(loading);

    chat.scrollTop = chat.scrollHeight;

    try {

        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        // Remove loading
        loading.remove();

        chat.innerHTML += `
            <div class="ai">
                <b>AI:</b> ${data.answer}
            </div>
        `;

    } catch (error) {

        loading.innerHTML = `
            <b>AI:</b> Sorry, something went wrong.
        `;

    } finally {

        button.disabled = false;
        button.innerText = "Ask AI";

    }

    chat.scrollTop = chat.scrollHeight;
}
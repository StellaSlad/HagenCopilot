document.addEventListener("DOMContentLoaded", (event) => {
    const chatbotToggler = document.querySelector(".chatbot-toggler");
    const closeBtn = document.querySelector(".close-btn");
    const historyCloseBtn = document.querySelector(".history-close-btn");
    const chatbox = document.querySelector(".chatbox");
    const chatbotHistory = document.querySelector(".chatbot-history");
    const chatInput = document.querySelector(".chat-input textarea");
    const sendChatBtn = document.querySelector(".chat-input span");

    let userMessage = null; // Variable to store user's message
    const inputInitHeight = chatInput.scrollHeight;

    const createChatLi = (message, className) => {
        // Create a chat <li> element with passed message and className
        const chatLi = document.createElement("li");
        chatLi.classList.add("chat", `${className}`);
        let chatContent = className === "outgoing" ? `<p></p>` : `<span class="material-symbols-outlined"></span><p></p>`;
        chatLi.innerHTML = chatContent;
        chatLi.querySelector("p").textContent = message;
        return chatLi; // return chat <li> element
    }

    const generateResponse = (chatElement) => {
        const API_URL = "http://127.0.0.1:5000/query";
        const messageElement = chatElement.querySelector("p");
        const messageElementChild = document.createElement("span");

        // Define the properties and message for the API request
        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ input: userMessage })
        }

        // Send POST request to API, get response and set the reponse as paragraph text
        fetch(API_URL, requestOptions).then(res => res.json()).then(data => {

            if (data.response?.context !== "undefined") {
                messageElementChild.innerHTML = "<br/><br/><b>Quellenangabe:</b><br/>";
                const metadataToDisplay = ["page", "source"];
                data.response.context.forEach((element, index) => {
                    messageElementChild.innerHTML += "<b>" + parseInt(index + 1) + ":  </b>";
                    for (const [key, value] of Object.entries(element.metadata)) {
                        if (metadataToDisplay.indexOf(key) > -1) {
                            messageElementChild.innerHTML += "<b>" + key + ":</b> " + value + "  ";
                        }
                    }
                    messageElementChild.innerHTML += "<hr>";
                });
                //messageElement.textContent = data.response.answer;
                //messageElement.appendChild(messageElementChild);
                
                const tempMessageElement = document.createElement("p");
                tempMessageElement.textContent = data.response.answer;
                tempMessageElement.appendChild(messageElementChild);

                textTypingEffect(messageElement, tempMessageElement.innerHTML, 30);

            }
        }).catch(() => {
            messageElement.classList.add("error");
            messageElement.textContent = "Oops! Etwas ist schief gelaufen, probiere es noch einmal.";
        }).finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
    }

    const handleChat = () => {
        userMessage = chatInput.value.trim(); // Get user entered message and remove extra whitespace
        if (!userMessage) return;

        // Clear the input textarea and set its height to default
        chatInput.value = "";
        chatInput.style.height = `${inputInitHeight}px`;

        // Append the user's message to the chatbox
        chatbox.appendChild(createChatLi(userMessage, "outgoing"));
        chatbox.scrollTo(0, chatbox.scrollHeight);

        setTimeout(() => {
            // Display "Thinking..." message while waiting for the response
            const incomingChatLi = createChatLi("Antwort wird gesucht...", "incoming");
            chatbox.appendChild(incomingChatLi);
            chatbox.scrollTo(0, chatbox.scrollHeight);
            setTimeout(() => {generateResponse(incomingChatLi);}, 600);
        }, 600);
    }

    chatInput.addEventListener("input", () => {
        // Adjust the height of the input textarea based on its content
        chatInput.style.height = `${inputInitHeight}px`;
        chatInput.style.height = `${chatInput.scrollHeight}px`;
    });

    chatInput.addEventListener("keydown", (e) => {
        // If Enter key is pressed without Shift key and the window 
        // width is greater than 800px, handle the chat
        if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
            e.preventDefault();
            handleChat();
        }
    });

    sendChatBtn.addEventListener("click", handleChat);
    closeBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));

    historyCloseBtn.addEventListener("click", () => {
        chatbotHistory.classList.toggle("show-chatbotHistory");
        document.body.classList.toggle("transite-content");
    });

    chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));

    const textTypingEffect = (element, sentence, speed = 30) => {
        let index = 0;

        let timer = setInterval(function () {
            const char = sentence[index];

            if (char === '<') {
                index = sentence.indexOf('>', index);  // skip to greater-than
            }

            element.innerHTML = sentence.slice(0, index);
            chatbox.scrollTo(0, chatbox.scrollHeight);

            if (++index === sentence.length) {
                clearInterval(timer);
            }
        }, speed);
    }
});